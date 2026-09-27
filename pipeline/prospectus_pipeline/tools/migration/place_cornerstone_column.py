#!/usr/bin/env python3
"""把基石名单列放到与同色（紫色）单元格相邻的位置。

背景：基石名单原在浅蓝区 `AT`。按要求迁到右侧紫色额外信息栏时先落在了 `BV`，
但 `BV` 左侧是市场数据的天蓝块 `BS:BU`，导致紫色列被隔开、看起来孤立。

本脚本做一次**同色归位**（不插入/删除列，只重排表头与列样式，因为这几列数据行是空的）：

    BS ← 基石名单（紫色 FFE4DFEC，紧接紫色块 BG:BR）
    BT ← 1-month HIBOR           （天蓝）
    BU ← 银行体系总结余          （天蓝）
    BV ← 首日收盘价              （天蓝）

结果：紫色 BG:BS 连续，天蓝 BT:BV 连续。
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
from copy import copy
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent
WS = ROOT.parent
BOOK = WS / "HKIPO-MB2026Q1.xlsx"
SCHEMA = ROOT / "schema" / "fields.json"

PURPLE = "FFE4DFEC"
SKYBLUE = "FF00B0F0"
COLS = ["BS", "BT", "BU", "BV"]


def main() -> None:
    backup = BOOK.with_name(f"{BOOK.stem}.backup-before-cornerstone-move-"
                           f"{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(BOOK, backup)

    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]

    # 1) 快照这四列的表头文字、表头样式、数据格样式、列宽
    snap = {}
    for name in COLS:
        col = ws[f"{name}1"].column
        snap[name] = {
            "header": ws[f"{name}1"].value,
            "header_style": {
                a: copy(getattr(ws[f"{name}1"], a))
                for a in ("font", "fill", "border", "alignment", "protection")
            },
            "data_style": {
                a: copy(getattr(ws[f"{name}2"], a))
                for a in ("font", "fill", "border", "alignment", "protection")
            },
            "number_format": ws[f"{name}2"].number_format,
            "width": ws.column_dimensions[name].width,
        }

    # 2) 紫色表头以紫色块为准（BG:BR），天蓝表头以 BS:BU 为准
    purple_header = {
        a: copy(getattr(ws["BR1"], a))
        for a in ("font", "fill", "border", "alignment", "protection")
    }
    purple_context = {
        a: copy(getattr(ws["BR1"], a))
        for a in ("font", "fill", "border", "alignment", "protection")
    }
    purple_header["fill"] = copy(ws["BR1"].fill)
    purple_header["fill"].fgColor.rgb = PURPLE
    purple_data = {
        a: copy(getattr(ws["BJ2"], a))
        for a in ("font", "fill", "border", "alignment", "protection")
    }
    purple_data["alignment"] = copy(ws["BJ2"].alignment)

    # 3) 目标排布：BS=基石（紫），BT/BU/BV=原 BS/BT/BU（天蓝）
    target = {
        "BS": {"header": "Cornerstone investor names",
               "header_style": purple_header,
               "data_style": purple_data,
               "number_format": "General",
               "width": max(snap["BV"]["width"] or 12, 24)},
        "BT": {"header": snap["BS"]["header"], "header_style": snap["BS"]["header_style"],
               "data_style": snap["BS"]["data_style"],
               "number_format": snap["BS"]["number_format"],
               "width": snap["BS"]["width"]},
        "BU": {"header": snap["BT"]["header"], "header_style": snap["BT"]["header_style"],
               "data_style": snap["BT"]["data_style"],
               "number_format": snap["BT"]["number_format"],
               "width": snap["BT"]["width"]},
        "BV": {"header": snap["BU"]["header"], "header_style": snap["BU"]["header_style"],
               "data_style": snap["BU"]["data_style"],
               "number_format": snap["BU"]["number_format"],
               "width": snap["BU"]["width"]},
    }

    for name, spec in target.items():
        col = ws[f"{name}1"].column
        head = ws.cell(1, col)
        head.value = spec["header"]
        for attr, value in spec["header_style"].items():
            setattr(head, attr, value)
        for r in range(2, ws.max_row + 1):
            cell = ws.cell(r, col)
            cell.value = None
            for attr, value in spec["data_style"].items():
                setattr(cell, attr, value)
            cell.number_format = spec["number_format"]
        if spec["width"]:
            ws.column_dimensions[name].width = spec["width"]

    # 4) 原先落在 BV 的基石表头/样式已被覆盖，确认 BV 现在是天蓝
    wb.save(BOOK)
    wb.close()

    # 5) schema：col_BV -> col_BS
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    for field in schema["fields"]:
        if field["key"] == "col_BV":
            field["key"] = "col_BS"
            field["col"] = "BS"
    groups = {}
    for field in schema["fields"]:
        groups.setdefault(field["group"], []).append(field["col"])
    schema["groups"] = {g: {"columns": c} for g, c in groups.items()}
    schema["note"] = ("Prospectus-derived fields. Columns resolved by normalized header at "
                      "runtime. Cornerstone investor names live in the purple block at BS "
                      "(originally AT).")
    SCHEMA.write_text(json.dumps(schema, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"backup: {backup.name}")
    for name in ["BR", "BS", "BT", "BU", "BV"]:
        c = ws2 = None
    wb = openpyxl.load_workbook(BOOK)
    ws = wb["NLR"]
    for name in ["BR", "BS", "BT", "BU", "BV"]:
        c = ws[f"{name}1"]
        fg = c.fill.fgColor
        print(f"  {name}1 = {str(c.value)[:52]!r:56s} fill={fg.rgb}")
    wb.close()


if __name__ == "__main__":
    main()
