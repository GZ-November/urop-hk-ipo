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
  - 新增列采用规范的深蓝 (FF00B0F0) 表头与格式化数字/百分比/日期。
"""
from __future__ import annotations

import argparse
import logging
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
from expansion_mapping import EXPANSION_COLUMNS, ExpansionValueMapper

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

class WorkbookExpansionWriter:
    """Excel 交付物学术扩展列写回引擎。"""

    def __init__(self, book_path: Path | None = None, cfg: dict | None = None) -> None:
        from cohort import load_cfg
        self.cfg = cfg or load_cfg()
        configured_book = self.cfg.get("workbook_path") or self.cfg.get("_workbook_path")
        self.book_path = Path(book_path or configured_book or (ROOT.parent / self.cfg["workbook"]))
        self.out_master = self.cfg["paths"]["out"] / "master"
        self.mapper = ExpansionValueMapper(self.out_master)

    def write_expansion(self) -> int:
        """执行事务级写回。"""
        self.mapper.load_sources()
        logger.info(f"Opening transaction on {self.book_path}...")
        from cohort import read_companies
        company_rows = read_companies(self.cfg)

        with workbook_transaction(self.book_path, operation="academic_expansion") as wb:
            ws = wb[self.cfg["sheet"]]
            max_col = ws.max_column
            logger.info(f"Existing workbook: max_row={ws.max_row}, max_column={max_col}")

            # 1. 写入表头 (Row 1)
            for col_idx, header, num_format, desc in EXPANSION_COLUMNS:
                cell = ws.cell(row=1, column=col_idx, value=header)
                cell.fill = HEADER_FILL
                cell.font = HEADER_FONT
                cell.alignment = HEADER_ALIGN
                cell.border = THIN_BORDER
                col_letter = get_column_letter(col_idx)
                ws.column_dimensions[col_letter].width = max(len(header) + 3, 14)

            # 2. 只写入当前配置日期范围内的发行人行。
            written_cells = 0
            for company in company_rows:
                r = company["row"]
                code_str = str(company["code"]).strip()
                if not code_str.endswith(".HK"):
                    digits = "".join(ch for ch in code_str if ch.isdigit())
                    code_str = f"{int(digits):04d}.HK"

                for col_idx, header, field_format, desc in EXPANSION_COLUMNS:
                    val, cell_format = self.mapper.value_for(code_str, col_idx)
                    if cell_format != field_format:
                        raise ValueError(
                            f"Expansion field {col_idx} format mismatch: "
                            f"catalog={field_format!r}, mapper={cell_format!r}"
                        )
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

            logger.info(f"Successfully populated {written_cells} cells across columns 162-202 ({len(company_rows)} issuers)")

        print(f"\n=======================================================")
        print(f"Workbook Academic Expansion Complete (Cols 162 - 202)")
        print(f"=======================================================")
        print(f"Target Workbook : {self.book_path}")
        print(f"New Columns     : 41 academic fields added (Col 162 to Col 202)")
        print(f"Cells Written   : {len(company_rows)} companies × 41 columns = {written_cells:,} data cells")
        return 0


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    from cohort import load_cfg
    parser = argparse.ArgumentParser(description="Write academic expansion columns to the configured workbook")
    parser.add_argument("--workbook")
    parser.add_argument("--period-start")
    parser.add_argument("--period-end")
    args = parser.parse_args()
    writer = WorkbookExpansionWriter(cfg=load_cfg(args.workbook, args.period_start, args.period_end))
    sys.exit(writer.write_expansion())
