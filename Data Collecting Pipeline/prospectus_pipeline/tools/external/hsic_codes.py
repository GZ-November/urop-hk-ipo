#!/usr/bin/env python3
"""【离线入表】BN / BO：恒生行业分类（HSICS 2026）代码与版本离线映射并安全写入工作簿。

数据源（纯确定性）：
  1. 港交所行业英文字段：out/hsic.json（由 tools/external/hsic.py 在线抓取）
  2. 恒生行业分类规范：data/manual/hsics.json（对照 docs/specs/Hang_Seng_Industry_Classification_System_2026.pdf）

做法：港交所给的是英文名称（如 "Semiconductors"），
本脚本用 HSIC_EN2CODE 把英文名映射到 HSICS 的 6 位码（如 703010）。
21 个实际出现的子类别均为一一对应，无歧义。

写入字段：
  - BN = 6 位码（文本，因 052020/053040 等含前导零）；
  - BO = "HSICS (Hang Seng Industry Classification System) 2026"。
同时把三层分类（行业/业务类别/业务子类别）写进 out/hsic_codes.json 供 cross_check / report 审计分析。
"""
from __future__ import annotations

import datetime as dt
import json
import shutil
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))
from contracts import normalize_code  # noqa: E402
from run import load_cfg  # noqa: E402

SYSTEM = "HSICS (Hang Seng Industry Classification System) 2026"

# 港交所 HSIC 英文名 → HSICS 6 位码（对照 data/manual/hsics.json）
HSIC_EN2CODE = {
    "Semiconductors": "703010",
    "Semiconductor Equipment & Materials": "703020",
    "Application Software": "702030",
    "Internet Services and Infrastructure": "702025",
    "Digital Solution Services": "702015",
    "Consumer Telecommunication Equipment & Components": "701010",
    "Robotic Systems & Solutions": "701030",
    "Industrial Components & Equipment": "101020",
    "Electrical & Electronic Components": "101025",
    "Printing & Packaging": "103020",
    "Auto Parts": "231020",
    "Toys & Leisure Products": "232030",
    "Packaged Foods": "251010",
    "Non-alcoholic Beverages": "251030",
    "Poultry & Meat": "252010",
    "Specialty Chemicals": "053040",
    "Copper": "052020",
    "Property Investment": "601030",
    "Biotechnology": "281020",
    "Medical Devices & Supplies": "282010",
    "Medical & Aesthetic Services": "282020",
    # 2026Q2 补全：HSICS 码取自恒生指数公司公开分类表
    # （B_HSICSe.pdf 与本仓库 x 交叉验证；未猜测）
    "Advertising & Marketing": "235010",
    "Computers & Peripherals": "701020",
    "Consumer Electronics": "232020",
    "Energy Storage Units": "101070",
    "Environmental Engineering": "101030",
    "Gold & Precious Metals": "051010",
    "Insurance": "502010",
    "Other Retailers": "237050",
    "Pharma & Biotech Contract Services": "281050",
    "Pharmaceuticals": "281010",
}

HEADERS = {"BN": "Industry classification code",
           "BO": "Industry classification system and version"}


def norm(s) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip().lower()


import argparse
from workbook_transaction import workbook_transaction


def main() -> int:
    cfg = load_cfg()
    ap = argparse.ArgumentParser(description="Map and inject HSICS codes")
    ap.add_argument("--dry-run", action="store_true", help="Do not mutate workbook")
    ap.add_argument("--book", default=str(WS / cfg["workbook"]), help="Path to workbook")
    ap.add_argument("--only", nargs="*", default=None, help="Filter by stock code(s)")
    args = ap.parse_args()

    book = Path(args.book)
    dry = args.dry_run

    hsic = json.loads((cfg["paths"]["out"] / "hsic.json").read_text(encoding="utf-8"))
    taxonomy_path = cfg["paths"]["data"] / "manual" / "hsics.json"
    if not taxonomy_path.is_file():
        taxonomy_path = ROOT / "data" / "manual" / "hsics.json"
    tax = {r["code"]: r for r in json.loads(taxonomy_path.read_text(encoding="utf-8"))}

    missing_map = sorted({v["hsic_sub"] for v in hsic.values()
                          if v.get("hsic_sub") and v["hsic_sub"] not in HSIC_EN2CODE})
    if missing_map:
        raise SystemExit(f"有子类别未映射，请补 HSIC_EN2CODE：{missing_map}")

    wb_read = openpyxl.load_workbook(book, data_only=True)
    ws_read = wb_read[cfg["sheet"]]
    col_of = {}
    for c in range(1, ws_read.max_column + 1):
        v = ws_read.cell(1, c).value
        if v in (None, ""):
            continue
        for k, h in HEADERS.items():
            if norm(v) == norm(h):
                col_of[k] = c
    if set(col_of) != {"BN", "BO"}:
        wb_read.close()
        raise SystemExit(f"找不到 BN/BO 列：{col_of}")

    ci_code = openpyxl.utils.column_index_from_string(cfg["id_columns"]["stock_code"])
    row_of = {}
    for r in range(cfg["data_start_row"], ws_read.max_row + 1):
        v = ws_read.cell(r, ci_code).value
        if v not in (None, ""):
            norm_c = normalize_code(str(v).strip())
            if args.only and norm_c not in [normalize_code(x) for x in args.only]:
                continue
            row_of[norm_c] = r
    wb_read.close()

    audit, n = {}, 0
    print(f"{'code':9s} {'HSICS码':9s} {'业务类别':30s} {'子类别':28s} 行业")
    for code, r in sorted(row_of.items()):
        rec = hsic.get(code) or {}
        sub = rec.get("hsic_sub")
        if not sub:
            print(f"{code:9s} 缺 HSIC 数据，跳过")
            continue
        c6 = HSIC_EN2CODE[sub]
        t = tax.get(c6, {})
        audit[code] = {
            "code": c6,
            "sub_sector": t.get("name"),
            "category": t.get("category"),
            "industry": t.get("industry"),
            "hkex_hsic_ind": rec.get("hsic_ind"),
            "hkex_hsic_sub": sub,
            "system": SYSTEM,
        }
        n += 1
        print(f"{code:9s} {c6:9s} {str(t.get('category'))[:28]:30s} "
              f"{str(t.get('name'))[:26]:28s} {t.get('industry')}")

    outj = cfg["paths"]["out"] / "hsic_codes.json"
    outj.write_text(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    print(f"\n定码 {n} 家 -> {outj}")

    if dry:
        print("--dry-run：未写回")
        return 0

    with workbook_transaction(book, operation="hsic") as wb:
        ws = wb[cfg["sheet"]]
        for code, rec in audit.items():
            r = row_of[code]
            ws.cell(r, col_of["BN"]).value = rec["code"]
            ws.cell(r, col_of["BO"]).value = SYSTEM

    print(f"已写回 BN/BO（{len(audit)} 家） -> {book.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
