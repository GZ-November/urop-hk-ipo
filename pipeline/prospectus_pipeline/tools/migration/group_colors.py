#!/usr/bin/env python3
"""把同色维度按老师逻辑归并到一起。

老师模板的顺序逻辑是「按来源分块，块内按手册字段顺序」：
    A:K  浅绿 = HKEx 新上市报告
    然后 浅蓝 = 招股书
    然后 天蓝 FF00B0F0 = 需要自己上网找
本工作簿在老师模板之上做了扩展，导致同色列被拆成多段（例如中文名 BA、
认购倍数 BF、基石 BC/BS 夹在浅蓝块里）。本脚本把 130 列重排成四段连续块：

    绿 A:K (11)  →  蓝 84 列  →  天 26 列  →  无填充(元数据) 9 列

L 列之后的数据行全为空，因此只需搬运表头、表头样式、列宽、数据格样式与数字格式，
不需要移动任何数据；A:K 完全不碰。
"""
from __future__ import annotations

import datetime as dt
import shutil
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent / "HKIPO-MB2026Q1.xlsx"

BLUE = [
    "Total (without option)",
    "Global Offering (without option)",
    "Number of offer shares under the capitalization Issue",
    "Number of offer shares under Capitalization Rest",
    "Sale Shares",
    "New shares",
    "Placing Shares",
    "Public Offer shares",
    "Maximum Offer Price",
    "Minimum Offer Price",
    "currency in financial information",
    "total assets in year-3 (3 years before IPO)",
    "total assets in year-2",
    "total assets in year-1",
    "total equity in year-3",
    "total equity in year-2",
    "total equity in year-1",
    "total liability in year-3",
    "total liability in year-2",
    "total liability in year-1",
    "Net sales in year-3",
    "Net sales in year-2",
    "Net sales in year-1",
    "Profit before tax in year-3",
    "Profit before tax in year-2",
    "Profit before tax in year-1",
    "Profit for the year in year-3",
    "Profit for the year in year-2",
    "Profit for the year in year-1",
    "Underwriting Commission (% of fund raised HK (a)",
    "Underwriting Commission (% of fund raised Int.(b)",
    "Over-allotment Option (%)",
    "Principal business / industry",
    "Listing route / applicable chapter",
    "See BS (sky-blue, extra-data block): Cornerstone investor names",
    "Year-1 financial period end (dd/mm/yy)",
    "Operating cash flow in year-1 (before annualization)",
    "Cash and cash equivalents at year-1 end",
    "R&D expensed in year-1 (before annualization)",
    "Development costs capitalized in year-1 (additions, before annualization)",
    "Top 5 customers (% of year-1 revenue)",
    "Net IPO proceeds to issuer (HK$)",
    "Public shareholding at listing (%)",
    "Share base used for both public shareholding ratios",
    "Comments (nearest sales& profit adjustment factor - original data duration in year, eg. 6 month pls input 0.5)",
    "Earliest cornerstone unlock date (dd/mm/yy)",
    "Pre-IPO VC/PE backing (1=yes; 0=no)",
    "Ultimate controller type",
    "Controller economic interest at listing (%)",
    "Controller voting rights at listing (%)",
    "Interest-bearing debt at year-1 end",
    "Technology commercialization stage",
    "Debt repayment (% of planned net IPO proceeds)",
    "Unrestricted public shareholding at listing (%)",
    "Listing board",
    "Share class",
    "A+H issuer flag",
    "WVR flag",
    "Chapter 18A flag",
    "Chapter 18C flag",
    "Industry classification code",
    "Industry classification system and version",
    "Incorporation date",
    "Place of incorporation",
    "Principal place of business",
    "Financial statement unit multiplier",
    "Accounting standard",
    "Year-3 financial period start",
    "Year-3 financial period end",
    "Year-2 financial period start",
    "Year-2 financial period end",
    "Year-1 financial period start",
    "Year-1 net sales (original, pre-annualization)",
    "Year-1 profit before tax (original)",
    "Year-1 profit for period (original)",
    "Offer mechanism",
    "Applicable IPO rules / transition basis",
    "Subscription opening date",
    "Subscription closing date",
    "H shares after IPO (base; no options)",
    "Gross profit in year-1",
    "Capital expenditure in year-1",
    "Audit opinion (year-1)",
    "Listing expenses (HK$)",
]

SKY = [
    "Cornerstone investor names",
    "Final cornerstone allocation (% of base offer)",
    "Subscription Ratio (times)",
    "Public applicants",
    "Public valid applied shares",
    "Public subscription original wording",
    "Pricing date",
    "Allotment announcement date",
    "Final global offering shares (before over-allotment)",
    "Final public offer shares",
    "Final placing shares",
    "Over-allotment shares actually issued",
    "Actual clawback / reallocation description",
    "Free float denominator description",
    "Free float denominator shares",
    "HSI return over 20 trading days before prospectus (%)",
    "HK ordinary IPO count in 90 calendar days before prospectus",
    "1-month HIBOR before prospectus (%)",
    "Banking system aggregate balance before prospectus (HK$)",
    "First trading day closing price (HK$)",
    "First trading day opening price (HK$)",
    "First trading day high (HK$)",
    "First trading day low (HK$)",
    "First trading day volume (shares)",
    "First trading day turnover (HK$)",
    "Company Chinese Name",
]

META = [
    "Issuer ID",
    "IPO event ID",
    "Security ID",
    "Collection status",
    "Source prospectus URL",
    "Source prospectus filename",
    "Source allotment URL",
    "Source allotment filename",
    "Market data source / series",
]

STYLE_ATTRS = ("font", "fill", "border", "alignment", "protection")


def main() -> None:
    backup = BOOK.with_name(f"{BOOK.stem}.backup-before-group-{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    first = 12  # L
    last = ws.max_column

    # 1) 快照 L..最后一列：表头、样式、列宽、数据格样式、数字格式
    snap: dict[str, dict] = {}
    for col in range(first, last + 1):
        letter = get_column_letter(col)
        hc = ws.cell(1, col)
        header = hc.value
        if header in (None, ""):
            continue
        dc = ws.cell(2, col)
        # 老师原始表头带尾随空格（如 "New shares "），按去空格后的名字索引
        snap[str(header).strip()] = {
            "header": header,
            "orig_col": letter,
            "hstyle": {a: copy(getattr(hc, a)) for a in STYLE_ATTRS},
            "width": ws.column_dimensions[letter].width,
            "dstyle": {a: copy(getattr(dc, a)) for a in STYLE_ATTRS},
            "fmt": dc.number_format,
        }

    # 2) 记录每列现有的数据验证
    dv_by_col: dict[str, tuple] = {}
    for dv in ws.data_validations.dataValidation:
        spec = (dv.type, dv.operator, dv.formula1, dv.formula2)
        for rng in str(dv.sqref).replace(",", " ").split():
            head = rng.split(":")[0]
            col = "".join(ch for ch in head if ch.isalpha())
            if col:
                dv_by_col.setdefault(col, spec)
    ws.data_validations.dataValidation = []

    # 3) 目标顺序
    target = BLUE + SKY + META
    existing = set(snap)
    missing = [h for h in target if h not in existing]
    extra = [h for h in existing if h not in set(target)]
    if missing or extra:
        raise SystemExit(f"目标顺序与原表头不一致\n  缺失: {missing}\n  多余: {extra}")

    # 4) 按目标顺序重写（数据行为空，直接覆盖样式即可）
    max_row = ws.max_row
    for i, header in enumerate(target):
        col = first + i
        letter = get_column_letter(col)
        s = snap[header]
        hc = ws.cell(1, col)
        hc.value = s["header"]
        for attr, value in s["hstyle"].items():
            setattr(hc, attr, value)
        if s["width"]:
            ws.column_dimensions[letter].width = s["width"]
        for r in range(2, max_row + 1):
            c = ws.cell(r, col)
            for attr, value in s["dstyle"].items():
                setattr(c, attr, value)
            c.number_format = s["fmt"]

    # 5) 还原数据验证到新列位置
    grouped: dict[tuple, list[str]] = {}
    for header in target:
        s = snap[header]
        spec = dv_by_col.get(s["orig_col"])
        if spec:
            new_letter = get_column_letter(first + target.index(header))
            grouped.setdefault(spec, []).append(new_letter)
    for (dtype, op, f1, f2), letters in grouped.items():
        dv = DataValidation(type=dtype, operator=op, formula1=f1, formula2=f2,
                            allow_blank=True, showErrorMessage=True)
        dv.error = "输入值不符合该字段口径，请核对。"
        dv.errorTitle = "数据校验"
        ws.add_data_validation(dv)
        for letter in letters:
            dv.add(f"{letter}2:{letter}{max_row}")

    wb.save(BOOK)
    wb.close()
    print(f"backup: {backup.name}")
    print(f"重排 {len(target)} 列：蓝 {len(BLUE)} / 天 {len(SKY)} / 元数据 {len(META)}")


if __name__ == "__main__":
    main()
