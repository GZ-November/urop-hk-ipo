#!/usr/bin/env python3
"""按老师手册的「数据来源」逻辑重新归类个别列。

老师逻辑（Data Construction Manual_students.docx）：
  浅绿 theme6@0.8  = HKEx 新上市页
  浅蓝 theme4@0.8  = 招股书
  深蓝 FF00B0F0    = 招股书里没有、必须自己另外找（配发结果/市场数据/监管规则归类）
  另外：中文名必须放**最后一列**。

本次移动：
  Offer mechanism                    -> 深蓝（Mechanism A/B 是港交所新回拨制度的监管归类）
  Applicable IPO rules / transition basis -> 深蓝（按刊发日判断适用哪版制度）
两列插入到「Company Chinese Name」之前，保证中文名仍是最后一列。
"""
from __future__ import annotations

import datetime as dt
import shutil
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.styles import PatternFill
from openpyxl.styles.colors import Color
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent / "HKIPO-MB2026Q1.xlsx"

# 需归入深蓝的列 -> (要移动的表头, 插到哪一列之前)，保持同一主题相邻
MOVES = [
    ("Earliest cornerstone unlock date (dd/mm/yy)", "Subscription Ratio (times)"),
    ("Net IPO proceeds to issuer (HK$)", "Public shareholding at listing (%)"),
]
SKYBLUE = "FF00B0F0"
LAST_MUST_BE = "Company Chinese Name"
STYLE_ATTRS = ("font", "fill", "border", "alignment", "protection")


def main() -> None:
    backup = BOOK.with_name(f"{BOOK.stem}.backup-before-reclass-{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    first = 12  # L

    # 快照
    order: list[str] = []
    snap: dict[str, dict] = {}
    for c in range(first, ws.max_column + 1):
        letter = get_column_letter(c)
        hc = ws.cell(1, c)
        if hc.value in (None, ""):
            continue
        name = str(hc.value).strip()
        dc = ws.cell(2, c)
        order.append(name)
        snap[name] = {
            "header": hc.value,
            "orig_col": letter,
            "hstyle": {a: copy(getattr(hc, a)) for a in STYLE_ATTRS},
            "width": ws.column_dimensions[letter].width,
            "dstyle": {a: copy(getattr(dc, a)) for a in STYLE_ATTRS},
            "fmt": dc.number_format,
        }

    # 记录数据验证
    dv_by_col: dict[str, tuple] = {}
    for dv in ws.data_validations.dataValidation:
        spec = (dv.type, dv.operator, dv.formula1, dv.formula2)
        for rng in str(dv.sqref).replace(",", " ").split():
            col = "".join(ch for ch in rng.split(":")[0] if ch.isalpha())
            if col:
                dv_by_col.setdefault(col, spec)
    ws.data_validations.dataValidation = []

    # 新顺序：其余保持原序，把 MOVES 里每一列插到指定锚点之前
    moved = [m[0] for m in MOVES]
    target = [h for h in order if h not in moved]
    assert target[-1] == LAST_MUST_BE, f"最后一列不是 {LAST_MUST_BE}，而是 {target[-1]}"
    for header, before in MOVES:
        assert before in target, f"找不到插入锚点 {before}"
        target.insert(target.index(before), header)

    # 重写
    max_row = ws.max_row
    for i, name in enumerate(target):
        col = first + i
        letter = get_column_letter(col)
        s = snap[name]
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
        if name in moved:                       # 改色为深蓝
            hc.fill = PatternFill(fill_type="solid", fgColor=Color(rgb=SKYBLUE))

    # 重挂数据验证
    grouped: dict[tuple, list[str]] = {}
    for i, name in enumerate(target):
        spec = dv_by_col.get(snap[name]["orig_col"])
        if spec:
            grouped.setdefault(spec, []).append(get_column_letter(first + i))
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
    print(f"已把 {moved} 移入深蓝块；末列仍为 {LAST_MUST_BE}（{get_column_letter(first+len(target)-1)}）")


if __name__ == "__main__":
    main()
