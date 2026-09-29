#!/usr/bin/env python3
"""将 Phase A 学术扩展高价值字段安全写回至配置的主交付物工作簿.

新增字段范围：Col 162 – Col 202 (共 41 个核心学术与微观结构变量)
分类涵盖：
  1. 稳价与超额配售 (Col 162–172)
  2. 微观结构与短期/中期跨期表现 (Col 173–184)
  3. 多重法定解禁日程与事件窗冲击 (Col 185–189)
  4. 承销辛迪加、费用分拆与银企关联 (Col 190–195)
  5. 机构投资者网络与国资背景 (Col 196–200)
  6. 宏观监管制度分期 (Col 201–202)

安全保证：
  - 采用 workbook_transaction 进行文件级互斥锁与时间戳快照；
  - 严格保持前 161 列内容与单元格格式 100% 不受影响；
  - 缺来源的字段写 None，绝不代填；若会以 None/占位值覆盖非空人工整理单元格，
    默认整体拒绝写回（--force-overwrite 显式放行）；
  - 新增列采用规范的深蓝 (FF00B0F0) 表头与格式化数字/百分比/日期。
"""
from __future__ import annotations

import argparse
import logging
from dataclasses import dataclass
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

logger = logging.getLogger("write_back_expansion")

ROOT = Path(__file__).resolve().parent.parent
sys_src = ROOT / "src"
import sys
if str(sys_src) not in sys.path:
    sys.path.insert(0, str(sys_src))

from workbook_transaction import workbook_transaction
from expansion_mapping import (
    CORNERSTONE_ALLOCATION_HEADER,
    CORNERSTONE_EVENT_COLS,
    CORNERSTONE_UNLOCK_HEADER,
    EXPANSION_COLUMNS,
    ExpansionValueMapper,
    is_no_cornerstone,
)

HEADER_FILL = PatternFill(start_color="FF00B0F0", end_color="FF00B0F0", fill_type="solid")
HEADER_FONT = Font(name="Arial", size=11, bold=True, color="000000")
HEADER_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DATA_ALIGN_CENTER = Alignment(horizontal="center", vertical="center")
DATA_ALIGN_RIGHT = Alignment(horizontal="right", vertical="center")
DATA_ALIGN_LEFT = Alignment(horizontal="left", vertical="center")
DATA_FONT = Font(name="Arial", size=10)

THIN_BORDER = Border(
    left=Side(style="thin", color="D9D9D9"),
    right=Side(style="thin", color="D9D9D9"),
    top=Side(style="thin", color="D9D9D9"),
    bottom=Side(style="thin", color="D9D9D9"),
)

# 历史映射器/上游面板代填的占位值标记（如 "CICC / Sponsor-OC"），不得写入工作簿。
PLACEHOLDER_MARKERS = ("sponsor-oc",)


def _is_blank(value) -> bool:
    return value is None or (isinstance(value, str) and not value.strip())


def is_placeholder(value) -> bool:
    return isinstance(value, str) and any(m in value.lower() for m in PLACEHOLDER_MARKERS)


@dataclass(frozen=True)
class OverwriteConflict:
    row: int
    code: str
    col: int
    existing: object
    incoming: object

    def describe(self) -> str:
        return (f"row {self.row} {self.code} col {self.col}: "
                f"{self.existing!r} -> {self.incoming!r}")


class ExpansionOverwriteError(RuntimeError):
    """写回会抹掉人工整理值或写入占位值时拒绝提交（fail closed）。"""

    def __init__(self, conflicts: list[OverwriteConflict], limit: int = 20) -> None:
        self.conflicts = conflicts
        lines = [c.describe() for c in conflicts[:limit]]
        if len(conflicts) > limit:
            lines.append(f"... and {len(conflicts) - limit} more")
        super().__init__(
            f"Refusing to write {len(conflicts)} expansion cell(s): curated values would be "
            f"cleared or replaced with placeholders (rerun with --force-overwrite to override):\n  "
            + "\n  ".join(lines)
        )


def find_overwrite_conflicts(ws, planned: list[tuple[int, str, int, object]]) -> list[OverwriteConflict]:
    """planned = [(row, code, col, incoming)]。

    冲突：(a) 非空、非占位的现有单元格将被 None/空串/占位值覆盖；
         (b) 占位值将写入任何单元格（现有值已相同者除外）。
    """
    conflicts = []
    for row, code, col, incoming in planned:
        existing = ws.cell(row=row, column=col).value
        if is_placeholder(incoming):
            if existing != incoming:
                conflicts.append(OverwriteConflict(row, code, col, existing, incoming))
        elif _is_blank(incoming) and not _is_blank(existing) and not is_placeholder(existing):
            conflicts.append(OverwriteConflict(row, code, col, existing, incoming))
    return conflicts


class WorkbookExpansionWriter:
    """Excel 交付物学术扩展列写回引擎。"""

    def __init__(self, book_path: Path | None = None, cfg: dict | None = None) -> None:
        from cohort import load_cfg
        self.cfg = cfg or load_cfg()
        configured_book = self.cfg.get("workbook_path") or self.cfg.get("_workbook_path")
        self.book_path = Path(book_path or configured_book or (ROOT.parent / self.cfg["workbook"]))
        self.out_master = self.cfg["paths"]["out"] / "master"
        from cornerstone import confirmed_absent
        self.mapper = ExpansionValueMapper(self.out_master, confirmed_absent(self.cfg))

    @staticmethod
    def _select(columns: set[int] | None) -> list:
        """解析要写的扩展列集合；未知列号直接报错。"""
        selected = [c for c in EXPANSION_COLUMNS if columns is None or c[0] in columns]
        if columns is not None and len(selected) != len(columns):
            unknown = sorted(columns - {c[0] for c in EXPANSION_COLUMNS})
            raise ValueError(f"Unknown expansion columns: {unknown}")
        return selected

    def _workbook_no_cornerstone(self, company_rows: list[dict], selected: list) -> set[str]:
        """从工作簿的基石解禁日/最终配售列识别无基石发行人（仅当写回含 Col 187-189 时）。

        fail closed：缺列即报错，避免无基石发行人被写入解禁 CAR / 成交量冲击。
        """
        if not any(c[0] in CORNERSTONE_EVENT_COLS for c in selected):
            return set()
        wb = openpyxl.load_workbook(self.book_path, read_only=True, data_only=True)
        try:
            ws = wb[self.cfg["sheet"]]
            header_col = {
                " ".join(str(v or "").split()).lower(): i
                for i, v in enumerate(next(ws.iter_rows(min_row=1, max_row=1, values_only=True)), start=1)
            }
            cols = {}
            for header in (CORNERSTONE_UNLOCK_HEADER, CORNERSTONE_ALLOCATION_HEADER):
                c = header_col.get(" ".join(header.split()).lower())
                if c is None:
                    raise ValueError(f"Workbook missing cornerstone column: {header!r}")
                cols[header] = c
            absent = set()
            for company in company_rows:
                r = company["row"]
                if is_no_cornerstone(ws.cell(r, cols[CORNERSTONE_UNLOCK_HEADER]).value,
                                     ws.cell(r, cols[CORNERSTONE_ALLOCATION_HEADER]).value):
                    absent.add(self._norm_code(company["code"]))
            return absent
        finally:
            wb.close()

    @staticmethod
    def _norm_code(code) -> str:
        code_str = str(code).strip()
        if not code_str.endswith(".HK"):
            digits = "".join(ch for ch in code_str if ch.isdigit())
            code_str = f"{int(digits):04d}.HK"
        return code_str

    def _plan(self, company_rows: list[dict],
              selected: list) -> list[tuple[int, str, int, object, str]]:
        """解析全部待写单元格 (row, code, col, value, format)，不触碰工作簿。"""
        planned = []
        for company in company_rows:
            r = company["row"]
            code_str = str(company["code"]).strip()
            if not code_str.endswith(".HK"):
                digits = "".join(ch for ch in code_str if ch.isdigit())
                code_str = f"{int(digits):04d}.HK"

            for col_idx, header, field_format, desc in selected:
                val, cell_format = self.mapper.value_for(code_str, col_idx, company.get("listing_date"))
                if cell_format != field_format:
                    raise ValueError(
                        f"Expansion field {col_idx} format mismatch: "
                        f"catalog={field_format!r}, mapper={cell_format!r}"
                    )
                planned.append((r, code_str, col_idx, val, cell_format))
        return planned

    def write_expansion(self, columns: set[int] | None = None, force_overwrite: bool = False,
                        dry_run: bool = False) -> int:
        """执行事务级写回；columns 非空时只写这些列（其余扩展列保持原值）。

        默认 fail closed：若会以 None/占位值覆盖非空人工整理单元格，或写入占位值，
        则在任何修改前抛出 ExpansionOverwriteError，工作簿保持不变。
        force_overwrite=True 时仅记录警告并照常写入。
        """
        selected = self._select(columns)
        self.mapper.load_sources()
        logger.info(f"Opening transaction on {self.book_path}...")
        from cohort import read_companies
        company_rows = read_companies(self.cfg)
        self.mapper.no_cornerstone |= self._workbook_no_cornerstone(company_rows, selected)
        planned = self._plan(company_rows, selected)

        with workbook_transaction(self.book_path, operation="academic_expansion", dry_run=dry_run) as wb:
            ws = wb[self.cfg["sheet"]]
            max_col = ws.max_column
            logger.info(f"Existing workbook: max_row={ws.max_row}, max_column={max_col}")

            # 0. 覆盖保护：先检查、后写入，抛错即放弃整个事务。
            conflicts = find_overwrite_conflicts(ws, [(r, code, col, val) for r, code, col, val, _ in planned])
            if conflicts and not force_overwrite:
                raise ExpansionOverwriteError(conflicts)
            if conflicts:
                logger.warning(f"--force-overwrite: overriding {len(conflicts)} protected cell(s)")
            if dry_run:
                print(f"[dry-run] {len(planned):,} expansion cells planned for {len(company_rows)} issuers; "
                      f"{len(conflicts)} protected-cell override(s); workbook not modified.")
                return 0

            # 1. 写入表头 (Row 1)
            for col_idx, header, num_format, desc in selected:
                cell = ws.cell(row=1, column=col_idx, value=header)
                cell.fill = HEADER_FILL
                cell.font = HEADER_FONT
                cell.alignment = HEADER_ALIGN
                cell.border = THIN_BORDER
                col_letter = get_column_letter(col_idx)
                ws.column_dimensions[col_letter].width = max(len(header) + 3, 14)

            # 2. 只写入当前配置日期范围内的发行人行。
            written_cells = 0
            for r, code_str, col_idx, val, cell_format in planned:
                cell = ws.cell(row=r, column=col_idx)
                cell.value = val
                cell.font = DATA_FONT
                cell.border = THIN_BORDER

                # 对齐与格式
                if cell_format in ("0.00%", "0.000", "#,##0", "0.000000"):
                    cell.alignment = DATA_ALIGN_RIGHT
                    cell.number_format = cell_format
                elif cell_format in ("0", "yyyy-mm-dd"):
                    cell.alignment = DATA_ALIGN_CENTER
                    cell.number_format = cell_format
                else:
                    cell.alignment = DATA_ALIGN_LEFT
                    cell.number_format = "@"

                written_cells += 1

            col_span = f"{selected[0][0]}-{selected[-1][0]}" if selected else "none"
            logger.info(f"Successfully populated {written_cells} cells across columns {col_span} ({len(company_rows)} issuers)")

        print(f"\n=======================================================")
        print(f"Workbook Academic Expansion Complete (Cols {col_span})")
        print(f"=======================================================")
        print(f"Target Workbook : {self.book_path}")
        print(f"Columns Written : {', '.join(str(c[0]) for c in selected)}")
        print(f"Cells Written   : {len(company_rows)} companies × {len(selected)} columns = {written_cells:,} data cells")
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from cohort import load_cfg
    parser = argparse.ArgumentParser(description="Write academic expansion columns to the configured workbook")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    parser.add_argument("--dry-run", action="store_true",
                        help="只解析并检查覆盖冲突，不保存工作簿")
    parser.add_argument("--force-overwrite", action="store_true",
                        help="允许以 None/占位值覆盖非空人工整理单元格（默认拒绝）")
    parser.add_argument("--columns", nargs="+", type=int,
                        help="只写回这些扩展列（如 201 202），其余扩展列保持不变")
    args = parser.parse_args()
    writer = WorkbookExpansionWriter(cfg=load_cfg(args.workbook, args.period_start, args.period_end))
    try:
        sys.exit(writer.write_expansion(columns=set(args.columns) if args.columns else None,
                                        force_overwrite=args.force_overwrite,
                                        dry_run=args.dry_run))
    except ExpansionOverwriteError as exc:
        print(f"错误: {exc}", file=sys.stderr)
        sys.exit(2)
