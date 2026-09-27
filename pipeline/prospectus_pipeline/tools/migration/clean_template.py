#!/usr/bin/env python3
"""清理工作簿，只保留三类有来源的列，输出干净版本。

删除：
  1) 9 个无填充的溯源/元数据列（Issuer ID、IPO event ID、Security ID、Collection status、
     Source prospectus URL/filename、Source allotment URL/filename、Market data source）
  2) AT 指引列（基石迁移完成后留下的占位说明）
  3) 全部条件格式（原模板遗留的 cellIs 规则，既无填充也无字体，不产生任何效果）
  4) 指向被删列的失效数据验证

保留并重排：
  浅绿 A:K（HKEx 新上市报告，原样不动）
  浅蓝 L:?（招股书）
  天蓝 ?:?（需自己上网找：配发结果 / 市场 / 需求）
"""
from __future__ import annotations

import datetime as dt
import shutil
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.formatting.formatting import ConditionalFormattingList
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parent
BOOK = ROOT.parent / "HKIPO-MB2026Q1.xlsx"

DROP_HEADERS = {
    "Issuer ID", "IPO event ID", "Security ID", "Collection status",
    "Source prospectus URL", "Source prospectus filename",
    "Source allotment URL", "Source allotment filename",
    "Market data source / series",
    # 基石迁移后留下的占位说明列
    "See BS (sky-blue, extra-data block): Cornerstone investor names",
}

STYLE_ATTRS = ("font", "fill", "border", "alignment", "protection")


def main() -> None:
    backup = BOOK.with_name(f"{BOOK.stem}.backup-before-clean-{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    first = 12  # L：A:K 是老师浅绿块，完全不动
    last = ws.max_column

    # 1) 快照 L..最后一列（跳过要删除的列），保持当前顺序
    order: list[str] = []
    snap: dict[str, dict] = {}
    for col in range(first, last + 1):
        letter = get_column_letter(col)
        hc = ws.cell(1, col)
        header = hc.value
        if header in (None, ""):
            continue
        name = str(header).strip()
        if name in DROP_HEADERS:
            continue
        dc = ws.cell(2, col)
        order.append(name)
        snap[name] = {
            "header": header,
            "orig_col": letter,
            "hstyle": {a: copy(getattr(hc, a)) for a in STYLE_ATTRS},
            "width": ws.column_dimensions[letter].width,
            "dstyle": {a: copy(getattr(dc, a)) for a in STYLE_ATTRS},
            "fmt": dc.number_format,
        }

    # 2) 记录有效的数据验证（键为原列字母），随后清空重挂
    dv_by_col: dict[str, tuple] = {}
    for dv in ws.data_validations.dataValidation:
        spec = (dv.type, dv.operator, dv.formula1, dv.formula2)
        for rng in str(dv.sqref).replace(",", " ").split():
            col = "".join(ch for ch in rng.split(":")[0] if ch.isalpha())
            if col:
                dv_by_col.setdefault(col, spec)
    ws.data_validations.dataValidation = []

    # 3) 清掉全部条件格式
    ws.conditional_formatting = ConditionalFormattingList()

    # 4) 按保留顺序重写到 L 起
    max_row = ws.max_row
    for i, name in enumerate(order):
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

    new_last = first + len(order) - 1

    # 5) 物理删掉右侧多余的旧列，避免留下空壳样式
    if last > new_last:
        ws.delete_cols(new_last + 1, last - new_last)

    # 6) 重新挂数据验证（只挂保留下来的列）
    grouped: dict[tuple, list[str]] = {}
    for i, name in enumerate(order):
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
    print(f"保留 {len(order)} 列：L:{get_column_letter(new_last)}；删除 {len(DROP_HEADERS)} 列 + 条件格式")


if __name__ == "__main__":
    main()
