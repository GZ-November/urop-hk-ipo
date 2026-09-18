"""【历史脚本 · 请勿重跑】基石列迁移的第一步：AT -> 额外信息栏。

工作簿已经完成两步迁移，本脚本对当前文件**不再适用**：
  1) 本脚本（已执行）：把基石名单从浅蓝区 AT 移到额外信息栏并留指引文字；
  2) tools_place_cornerstone_column.py（已执行）：把基石列同色归位到紫色块末列 BS，
     天蓝市场数据块顺延为 BT:BV。

如需从原始模板重做，请按 1 -> 2 顺序执行。当前权威列契约见 schema/fields.json。
"""
from __future__ import annotations

import json
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
WS = ROOT.parent
BOOK = WS / "HKIPO-MB2026Q1.xlsx"
SCHEMA = ROOT / "schema" / "fields.json"


def norm_header(v):
    return " ".join(str(v or "").replace("\n", " ").split()).strip().lower()


def field_meta(col: str, header: str, group: str) -> dict:
    # 严格类型/单位/期间契约；字段值仍由 AI 提供 page/quote/confidence。
    if col in {"L", "M", "N", "O", "P", "Q", "R", "S"}:
        kind, unit = "integer", "shares"
    elif col in {"T", "U"}:
        kind, unit = "number", "HKD_per_share"
    elif col == "V":
        kind, unit = "text", "currency_code"
    elif col in {"W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN"}:
        kind, unit = "number", "basic_currency_units"
    elif col in {"AO", "AP", "AQ", "AZ"}:
        kind, unit = "number", "decimal"
    elif col in {"AU"}:
        kind, unit = "date", "date"
    elif col in {"AV", "AW", "AX", "AY"}:
        kind, unit = "number", "basic_currency_units"
    elif col == "BV":
        kind, unit = "text", "investor_names"
    elif col in {"AR", "AS", "BA"}:
        kind, unit = "text", "text"
    else:
        kind, unit = "text", "text"

    meta = {
        "key": f"col_{col}",
        "col": col,
        "header": header,
        "group": group,
        "kind": kind,
        "unit": unit,
        "source": "prospectus",
        "missing": "NA" if kind in {"text", "date"} else "NaN",
        "section_keywords": [],
    }
    if col in {"W", "Z", "AC", "AF", "AI", "AL"}:
        meta.update({"period": "year-3", "annualize": False})
    elif col in {"X", "AA", "AD", "AG", "AJ", "AM"}:
        meta.update({"period": "year-2", "annualize": False})
    elif col in {"Y", "AB", "AE", "AH", "AK", "AN"}:
        meta.update({"period": "year-1", "annualize": "sales_profit_only_if_partial"})
    elif col in {"AV", "AX", "AY"}:
        meta.update({"period": "year-1_original", "annualize": False})
    elif col == "AU":
        meta.update({"period": "year-1_original_end", "annualize": False})
    elif col == "AZ":
        meta.update({"period": "year-1_original", "annualize": False})
    return meta


def main():
    # 先由目标工作簿生成可运行时核验的字段契约。
    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    # 将 AT 的数据字段物理移到 BU 之后的 BV，复制紫色额外信息区的样式。
    src_header = ws["AT1"]
    src_data = ws["AT2"]
    dest_header = ws["BV1"]
    dest_data = ws["BV2"]
    for attr in ("font", "fill", "border", "alignment", "protection"):
        setattr(dest_header, attr, copy(getattr(ws["BJ1"], attr)))
        setattr(dest_data, attr, copy(getattr(ws["BJ2"], attr)))
    dest_header.value = "Cornerstone investor names"
    dest_data.value = None
    dest_header.alignment = Alignment(horizontal="center", vertical="top", wrap_text=True)
    dest_data.alignment = Alignment(horizontal="left", vertical="top", wrap_text=True)
    dest_data.number_format = "General"
    dest_header.fill = PatternFill(fill_type="solid", fgColor="FFE4DFEC")
    dest_header.font = Font(name="Arial", size=12)
    ws.column_dimensions["BV"].width = max(ws.column_dimensions["AT"].width or 12, 24)
    # AT 保留醒目标识，避免使用者误以为旧位置仍会填数据。
    src_header.value = "See BV (purple): Cornerstone investor names"
    src_header.font = copy(ws["AR1"].font)
    src_header.fill = copy(ws["AR1"].fill)
    src_header.alignment = copy(ws["AR1"].alignment)
    for r in range(2, ws.max_row + 1):
        ws[f"AT{r}"].value = None
    # 扩展自动筛选范围（若存在）。
    if ws.auto_filter.ref:
        start, _ = ws.auto_filter.ref.split(":")
        ws.auto_filter.ref = f"{start}:BV{ws.max_row}"
    wb.save(BOOK)
    wb.close()

    wb = openpyxl.load_workbook(BOOK, read_only=True, data_only=False)
    ws = wb["NLR"]
    fields = []
    # 保持原 L:BA 顺序，但排除迁出的 AT。
    for col in range(12, 54):
        letter = get_column_letter(col)
        if letter == "AT":
            continue
        header = ws.cell(1, col).value
        if header in (None, ""):
            continue
        group = ""
        if letter in set("LMNOPQRS"):
            group = "share_structure"
        elif letter in {"T", "U"}:
            group = "price"
        elif letter in {"V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN"}:
            group = "financials"
        elif letter in {"AO", "AP", "AQ"}:
            group = "underwriting"
        elif letter in {"AR", "AS"}:
            group = "business"
        elif letter in {"AU", "AV", "AW", "AX", "AY", "AZ"}:
            group = "extra_financial"
        elif letter == "BA":
            group = "chinese_name"
        else:
            continue
        fields.append(field_meta(letter, str(header), group))
    fields.append(field_meta("BV", ws["BV1"].value, "extra_financial"))
    wb.close()

    kw = {
        "share_structure": ["SHARE CAPITAL", "GLOBAL OFFERING STATISTICS", "STATISTICS OF THE GLOBAL OFFERING", "IMPORTANT"],
        "price": ["__cover__", "IMPORTANT", "OFFER PRICE", "MAXIMUM OFFER PRICE", "MINIMUM OFFER PRICE"],
        "financials": ["SUMMARY OF HISTORICAL FINANCIAL INFORMATION", "DISCUSSION OF SELECTED ITEMS FROM THE CONSOLIDATED BALANCE", "CONSOLIDATED BALANCE SHEETS", "CONSOLIDATED STATEMENTS OF COMPREHENSIVE LOSS", "HISTORICAL FINANCIAL INFORMATION OF THE GROUP", "INDEBTEDNESS"],
        "underwriting": ["UNDERWRITING ARRANGEMENTS AND EXPENSES", "UNDERWRITING COMMISSION", "UNDERWRITING"],
        "business": ["BUSINESS", "SUMMARY", "HISTORY AND DEVELOPMENT", "BASIS OF LISTING"],
        "extra_financial": ["CONSOLIDATED STATEMENTS OF CASH FLOWS", "CASH FLOW ANALYSIS", "R&D EXPENDITURE AND TOTAL OPERATING EXPENDITURE", "INTANGIBLE ASSETS", "CAPITALIZED DEVELOPMENT", "CUSTOMERS AND SUPPLIERS", "CORNERSTONE INVESTORS", "THE CORNERSTONE INVESTORS", "CORNERSTONE PLACING"],
        "chinese_name": ["__cover__"],
    }
    for f in fields:
        f["section_keywords"] = kw.get(f["group"], [])
    groups = {}
    for f in fields:
        groups.setdefault(f["group"], []).append(f["col"])
    payload = {
        "workbook": BOOK.name,
        "sheet": "NLR",
        "header_row": 1,
        "field_count": len(fields),
        "note": "Prospectus-derived fields; columns are resolved by normalized headers at runtime. AT was moved to purple BV.",
        "groups": {g: {"columns": cols} for g, cols in groups.items()},
        "fields": fields,
    }
    SCHEMA.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")
    print(f"reconfigured workbook and schema: {len(fields)} fields; cornerstone -> BV")


if __name__ == "__main__":
    main()
