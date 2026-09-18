"""把严格校验通过的抽取结果写回工作簿。

原则（依据手册 + 老师模板）：
  1. 只给单元格赋值，绝不改写 font / fill / alignment / number_format —— 目标列的格式
     就是老师模板的格式，改写会破坏它。
  2. 手册要求不得留空：数值缺失写 NaN，非数值/日期缺失写 NA。因此默认 fill_missing=True，
     并且会覆盖该格可能残留的旧值。
  3. 写回前必须有同一内容哈希的 extracted / validated / reviewed 三份通过记录。
  4. 列位置由**规范化表头**在运行时解析并核对，不依赖硬编码列字母。
  5. 备份带时间戳、不覆盖历史；保存先写临时文件再原子替换。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import shutil
from pathlib import Path

import openpyxl

from contracts import is_missing, normalize_code, strict_load_file
from storage import official_files

TEXT_KINDS = {"text"}
DATE_KINDS = {"date"}
NUMERIC_KINDS = {"integer", "number"}


def norm_header(v) -> str:
    return " ".join(str(v or "").replace("\n", " ").split()).strip().lower()


def resolve_columns(ws, schema: dict) -> tuple[dict, list[str]]:
    """把 schema 的 key 通过规范化表头解析成真实列字母；返回 (映射, 问题列表)。"""
    header_to_cols: dict[str, list[str]] = {}
    for col in range(1, ws.max_column + 1):
        val = ws.cell(1, col).value
        if val in (None, ""):
            continue
        if ws.cell(1, col).fill.fill_type != "solid":
            continue
        header_to_cols.setdefault(norm_header(val), []).append(
            openpyxl.utils.get_column_letter(col))
    mapping, issues = {}, []
    for field in schema["fields"]:
        cols = header_to_cols.get(norm_header(field["header"]), [])
        if len(cols) == 1:
            mapping[field["key"]] = cols[0]
        elif not cols:
            issues.append(f"{field['key']}: header not found: {field['header']!r}")
        else:
            issues.append(f"{field['key']}: header ambiguous: {field['header']!r} -> {cols}")
    return mapping, issues


def parse_date(value):
    if isinstance(value, dt.datetime):
        return value.date()
    if isinstance(value, dt.date):
        return value
    s = str(value).strip()
    for fmt in ("%d/%m/%y", "%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d %b %Y", "%d %B %Y"):
        try:
            return dt.datetime.strptime(s, fmt).date()
        except ValueError:
            continue
    raise ValueError(f"unparseable date: {value!r}")


def coerce(entry: dict, field: dict):
    """按字段类型返回可写入值；缺失返回手册哨兵。"""
    kind = field.get("kind", "text")
    value = entry.get("value")
    if is_missing(value, kind):
        return "NA" if kind in TEXT_KINDS | DATE_KINDS else "NaN"
    if kind == "integer":
        return int(round(float(value)))
    if kind == "number":
        return float(value)
    if kind == "date":
        return parse_date(value)
    return str(value).strip()


def write_all(cfg: dict, fill_missing: bool = True, only: list[str] | None = None,
              limit: int = 0, target: str = "prospectus", log=print) -> int:
    if target == "allot":
        schema = strict_load_file(cfg["_root"] / "schema" / "allot_fields.json")
        ext_dir: Path = cfg["paths"]["allot_out"] / "extracted"
        gate_file: Path = cfg["paths"]["allot_out"] / "validation.json"
    else:
        schema = strict_load_file(cfg["_root"] / "schema" / "fields.json")
        ext_dir = cfg["paths"]["out"] / "extracted"
        gate_file = cfg["paths"]["out"] / "validation.json"
    book = cfg["_ws"] / cfg["workbook"]

    wb = openpyxl.load_workbook(book)
    ws = wb[cfg["sheet"]]

    # 目标行：股票代码 -> 行号
    code_col = cfg["id_columns"]["stock_code"]
    row_of = {}
    for r in range(cfg["data_start_row"], ws.max_row + 1):
        v = ws[f"{code_col}{r}"].value
        if v not in (None, ""):
            row_of[normalize_code(v)] = r

    # 列解析核对
    mapping, col_issues = resolve_columns(ws, schema)
    if col_issues:
        wb.close()
        log("列解析失败，已中止写回：")
        for issue in col_issues:
            log("   - " + issue)
        raise SystemExit(2)

    wanted = [normalize_code(x) for x in only] if only else sorted(row_of)
    if limit:
        wanted = wanted[:limit]

    files = official_files(ext_dir)
    targets = [c for c in wanted if c in files]
    missing_records = [c for c in wanted if c not in files]
    unmatched = [c for c in wanted if c not in row_of]
    if missing_records or unmatched:
        wb.close()
        details = []
        if missing_records:
            details.append("缺少抽取 JSON：" + ", ".join(missing_records))
        if unmatched:
            details.append("工作簿无对应行：" + ", ".join(unmatched))
        raise SystemExit("拒绝部分写回；" + "；".join(details))
    # Revalidate the current bytes immediately before writing. Authorization is
    # per company and hash-bound, so a different or subsequently modified JSON
    # can never inherit an old green report.
    from validate import validate_all
    from state import authorized, save_record
    fresh = validate_all(cfg, only=targets, target=target, log=lambda *_: None)
    by_code = {r["code"]: r for r in fresh.get("records", [])}
    blocked_targets = []
    for code in targets:
        try:
            authorized(cfg, code, target, by_code.get(code, {}))
        except ValueError as exc:
            blocked_targets.append(str(exc))
    if blocked_targets:
        wb.close()
        raise SystemExit("写回授权失败：" + " | ".join(blocked_targets))

    backup_dir = cfg["_ws"] / "backups" / "excel_snapshots"
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup = backup_dir / f"{book.stem}.backup-before-extract-{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx"
    shutil.copy2(book, backup)
    log(f"备份 -> backups/excel_snapshots/{backup.name}")

    written = 0
    for code in targets:
        rec = strict_load_file(files[code])
        row = row_of[code]
        n = 0
        for field in schema["fields"]:
            key = field["key"]
            entry = rec.get("fields", {}).get(key)
            if not isinstance(entry, dict):
                continue
            value = coerce(entry, field)
            if value is None and not fill_missing:
                continue
            cell = ws[f"{mapping[key]}{row}"]
            cell.value = value          # 只赋值：字体/填充/对齐/数字格式保持老师模板
            n += 1
        written += 1
        cols = sorted(mapping.values(), key=lambda c: ws[f"{c}1"].column)
        log(f"{code:9s} 行 {row:3d} 写入 {n:2d} 列（{cols[0]}…{cols[-1]}）")

    tmp = book.with_suffix(".saving.xlsx")
    wb.save(tmp)
    wb.close()
    os.replace(tmp, book)
    for code in targets:
        save_record(cfg, target, code, "written",
                    {**by_code[code], "target": target, "gate_pass": True})
    log(f"\n写回完成：{written} 家 -> {book.name}")
    return written


if __name__ == "__main__":
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from run import load_cfg
    ap = argparse.ArgumentParser()
    ap.add_argument("--fill-missing", action="store_true", default=True)
    ap.add_argument("--no-fill-missing", dest="fill_missing", action="store_false")
    ap.add_argument("--only", nargs="*", default=None)
    ap.add_argument("--limit", type=int, default=0)
    a = ap.parse_args()
    write_all(load_cfg(), fill_missing=a.fill_missing, only=a.only, limit=a.limit)
