#!/usr/bin/env python3
"""按老师模板的「数据来源三色」规则整理工作簿。

老师模板的原始颜色要求（HKIPO-MB-template-students.xlsx + Data Construction Manual_students.docx）：
  theme6@0.8 浅绿  A:K   → HKEx 新上市报告
  theme4@0.8 浅蓝  L:AR  → 招股书
  FF00B0F0   天蓝  AS:AT → 需要自己上网找（老师放的正是 Subscription Ratio 与 Company Chinese Name）

本模块做两件事：
  1) 把**全部**表头按来源重新上色（浅绿保持；招股书→浅蓝；配发结果/市场/需求→天蓝）；
     纯溯源元数据（ID、来源 URL、采集状态）不在老师三色体系内，统一不填充。
  2) 在 BV 之后追加审查 §3 必加项，去掉与现有列重复或可由现有列推导的字段。

去重说明（这些字段**不再**单独建列）：
  Public subscription multiple      = 现有 BF Subscription Ratio (times)
  Public float denominator shares   = 现有 BE Share base used for both ratios
  Year-1..3 period duration months  = 由 period start/end 推导（Year-1 另有 BG 系数）
  Initial/Final public allocation fraction = 由公开/配售股数推导
  Listing status                    = 本表只收已上市公司，恒为 Listed
  Other applicable listing chapters = 与 AS Listing route 重叠
  Offer size adjustment exercised   = 由 M 与 Final global offering shares 推导
"""
from __future__ import annotations

import datetime as dt
import shutil
from pathlib import Path

import openpyxl
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.styles.colors import Color
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent / "HKIPO-MB2026Q1.xlsx"

LIGHTGREEN = Color(theme=6, tint=0.7999816888943144, type="theme")
LIGHTBLUE = Color(theme=4, tint=0.7999816888943144, type="theme")
SKYBLUE = "FF00B0F0"

HDR_FONT = Font(name="Arial", size=12)
DATA_FONT = Font(name="Arial", size=12)
DATA_FONT_NUM = Font(name="Times New Roman", size=12)
HDR_ALIGN = Alignment(horizontal="center", vertical="center", wrap_text=True)
DATA_ALIGN = Alignment(horizontal="center", vertical="top", wrap_text=True)
DATA_ALIGN_L = Alignment(horizontal="left", vertical="top", wrap_text=True)

# 现有 A:BV 表头按来源重上色（未列出的列保持原色：A:K 浅绿、L:AR/AU:AZ 浅蓝）
RECOLOR_EXISTING = {
    "BA": SKYBLUE,   # Company Chinese Name —— 老师把它放在天蓝
    "BB": LIGHTBLUE, "BC": SKYBLUE, "BD": LIGHTBLUE, "BE": LIGHTBLUE, "BF": SKYBLUE,
    "BG": LIGHTBLUE, "BH": LIGHTBLUE, "BI": LIGHTBLUE, "BJ": LIGHTBLUE, "BK": LIGHTBLUE,
    "BL": LIGHTBLUE, "BM": LIGHTBLUE, "BN": LIGHTBLUE, "BO": LIGHTBLUE, "BP": LIGHTBLUE,
    "BQ": SKYBLUE,   # HSI return —— 市场数据
    "BR": SKYBLUE,   # HK ordinary IPO count —— 市场/上市事件
    "BS": SKYBLUE,   # Cornerstone names —— 需与配发结果核对
    "BT": SKYBLUE, "BU": SKYBLUE, "BV": SKYBLUE,
}

# (表头, 组, 数字格式, 对齐, 数据验证键, 列宽)
COLS = [
    # ---- 溯源 / ID（不在老师三色体系内 → 不填充） ----
    ("Issuer ID", "meta", "General", "L", None, 16),
    ("IPO event ID", "meta", "General", "L", None, 14),
    ("Security ID", "meta", "General", "L", None, 14),
    ("Collection status", "meta", "General", "L", "status", 14),
    ("Source prospectus URL", "meta", "General", "L", None, 40),
    ("Source prospectus filename", "meta", "General", "L", None, 26),
    ("Source allotment URL", "meta", "General", "L", None, 40),
    ("Source allotment filename", "meta", "General", "L", None, 26),
    ("Market data source / series", "meta", "General", "L", None, 28),
    # ---- 上市身份 / 公司背景 / 财报口径 / 发行流程（招股书 → 浅蓝） ----
    ("Listing board", "prospectus", "General", "C", "board", 12),
    ("Share class", "prospectus", "General", "L", None, 14),
    ("A+H issuer flag", "prospectus", "0", "C", "flag01", 10),
    ("WVR flag", "prospectus", "0", "C", "flag01", 10),
    ("Chapter 18A flag", "prospectus", "0", "C", "flag01", 10),
    ("Chapter 18C flag", "prospectus", "0", "C", "flag01", 10),
    ("Industry classification code", "prospectus", "General", "C", None, 14),
    ("Industry classification system and version", "prospectus", "General", "L", None, 18),
    ("Incorporation date", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Place of incorporation", "prospectus", "General", "L", None, 18),
    ("Principal place of business", "prospectus", "General", "L", None, 24),
    ("Financial statement unit multiplier", "prospectus", "#,##0", "C", "whole", 12),
    ("Accounting standard", "prospectus", "General", "C", "accounting", 14),
    ("Year-3 financial period start", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Year-3 financial period end", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Year-2 financial period start", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Year-2 financial period end", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Year-1 financial period start", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Year-1 net sales (original, pre-annualization)", "prospectus", "#,##0.00", "C", None, 16),
    ("Year-1 profit before tax (original)", "prospectus", "#,##0.00", "C", None, 16),
    ("Year-1 profit for period (original)", "prospectus", "#,##0.00", "C", None, 16),
    ("Offer mechanism", "prospectus", "General", "C", "mechanism", 14),
    ("Applicable IPO rules / transition basis", "prospectus", "General", "L", None, 20),
    ("Subscription opening date", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("Subscription closing date", "prospectus", "dd/mm/yy", "C", "date", 12),
    ("H shares after IPO (base; no options)", "prospectus", "#,##0", "C", "whole", 16),
    ("Gross profit in year-1", "prospectus", "#,##0.00", "C", None, 16),
    ("Capital expenditure in year-1", "prospectus", "#,##0.00", "C", None, 16),
    ("Audit opinion (year-1)", "prospectus", "General", "L", "audit", 18),
    ("Listing expenses (HK$)", "prospectus", "#,##0.00", "C", None, 16),
    # ---- 配发结果 / 需求 / 市场（需自己找 → 天蓝） ----
    ("Public applicants", "extra", "#,##0", "C", "whole", 14),
    ("Public valid applied shares", "extra", "#,##0", "C", "whole", 16),
    ("Public subscription original wording", "extra", "General", "L", None, 24),
    ("Free float denominator description", "extra", "General", "L", None, 22),
    ("Free float denominator shares", "extra", "#,##0", "C", "whole", 16),
    ("Pricing date", "extra", "dd/mm/yy", "C", "date", 12),
    ("Allotment announcement date", "extra", "dd/mm/yy", "C", "date", 12),
    ("Final global offering shares (before over-allotment)", "extra", "#,##0", "C", "whole", 18),
    ("Final public offer shares", "extra", "#,##0", "C", "whole", 14),
    ("Final placing shares", "extra", "#,##0", "C", "whole", 14),
    ("Actual clawback / reallocation description", "extra", "General", "L", None, 24),
    ("Over-allotment shares actually issued", "extra", "#,##0", "C", "whole", 14),
    ("First trading day opening price (HK$)", "extra", "0.0000", "C", "ge0", 14),
    ("First trading day high (HK$)", "extra", "0.0000", "C", "ge0", 12),
    ("First trading day low (HK$)", "extra", "0.0000", "C", "ge0", 12),
    ("First trading day volume (shares)", "extra", "#,##0", "C", "whole", 16),
    ("First trading day turnover (HK$)", "extra", "#,##0.00", "C", "ge0", 16),
]

GROUP_FILL = {"meta": None, "prospectus": LIGHTBLUE, "extra": SKYBLUE}

VALIDATIONS = {
    "whole": dict(type="whole", operator="greaterThanOrEqual", formula1="0"),
    "ge0": dict(type="decimal", operator="greaterThanOrEqual", formula1="0"),
    "pct": dict(type="decimal", operator="between", formula1="0", formula2="1"),
    "flag01": dict(type="whole", operator="between", formula1="0", formula2="1"),
    "date": dict(type="date", operator="greaterThan", formula1="1900-01-01"),
    "board": dict(type="list", formula1='"Main Board,GEM"'),
    "status": dict(type="list", formula1='"待查,已填,未披露,不适用"'),
    "accounting": dict(type="list", formula1='"IFRS,HKFRS,US GAAP,CAS,Other"'),
    "mechanism": dict(type="list", formula1='"Mechanism A,Mechanism B,Pre-reform"'),
    "audit": dict(type="list", formula1='"Unqualified,Qualified,Adverse,Disclaimer,NA"'),
}


def apply_fill(cell, fill):
    if fill is None:
        cell.fill = PatternFill(fill_type=None)
    else:
        cell.fill = PatternFill(fill_type="solid", fgColor=fill)


def new_dv(spec):
    dv = DataValidation(type=spec["type"], operator=spec.get("operator"),
                        formula1=spec["formula1"], formula2=spec.get("formula2"),
                        allow_blank=True, showErrorMessage=True)
    dv.error = "输入值不符合该字段口径，请核对。"
    dv.errorTitle = "数据校验"
    return dv


def main() -> None:
    backup = BOOK.with_name(f"{BOOK.stem}.backup-before-align-{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    assert ws["AT1"].value and "See BS" in str(ws["AT1"].value), "AT 指引文字缺失，可能不是预期的底稿"

    # 1) 现有表头按来源重上色
    for col, fill in RECOLOR_EXISTING.items():
        apply_fill(ws[f"{col}1"], fill)

    # 2) 追加去重后的新列
    start_col = 74 + 1
    for i, (header, group, fmt, align, vkey, width) in enumerate(COLS):
        col = start_col + i
        letter = get_column_letter(col)
        hc = ws.cell(1, col)
        hc.value = header
        hc.font = HDR_FONT
        hc.alignment = HDR_ALIGN
        apply_fill(hc, GROUP_FILL[group])

        font = DATA_FONT_NUM if fmt not in ("General", "0") else DATA_FONT
        alignment = DATA_ALIGN_L if align == "L" else DATA_ALIGN
        for r in range(2, ws.max_row + 1):
            c = ws.cell(r, col)
            c.number_format = fmt
            c.font = font
            c.alignment = alignment
        ws.column_dimensions[letter].width = width

        if vkey:
            dv = new_dv(VALIDATIONS[vkey])
            ws.add_data_validation(dv)
            dv.add(f"{letter}2:{letter}{ws.max_row}")

    # 3) 已有关键列的数据校验（审查 §5）
    def add_dv(cols, spec):
        dv = new_dv(spec)
        ws.add_data_validation(dv)
        for c in cols:
            dv.add(f"{c}2:{c}{ws.max_row}")

    add_dv(list("LMNOPQRS"), VALIDATIONS["whole"])
    add_dv(["T", "U"], VALIDATIONS["ge0"])
    add_dv("AO AP AQ AZ BC BD BK BL BO BP BQ BT".split(), VALIDATIONS["pct"])
    add_dv("DE AU BH".split(), VALIDATIONS["date"])
    add_dv(["BI"], VALIDATIONS["flag01"])
    add_dv(["BR"], VALIDATIONS["whole"])
    add_dv(["V"], dict(type="list", formula1='"RMB,HKD,USD,Other"'))
    add_dv(["BJ"], dict(type="list",
                        formula1='"Central state-owned,Local state-owned,Family,Individual,No controller,Other"'))
    add_dv(["BN"], dict(type="list",
                        formula1='"Research,Prototype,Pilot,Commercial sales,Not applicable,Unclear"'))

    wb.save(BOOK)
    wb.close()
    print(f"backup: {backup.name}")
    print(f"追加 {len(COLS)} 列（{get_column_letter(start_col)}:{get_column_letter(start_col+len(COLS)-1)}）；"
          f"现有表头重上色 {len(RECOLOR_EXISTING)} 列")


if __name__ == "__main__":
    main()
