#!/usr/bin/env python3
"""从已有产物确定性推导 7 个空列（不花 token）。

推导来源：
  BH Listing board            ← col_AS（上市途径）是否含 Main Board / GEM
  BJ A+H issuer flag          ← col_AS 是否含 "A+H"
  BK WVR flag                 ← col_AS 是否含 "Chapter 8A"
  BL Chapter 18A flag         ← col_AS 是否含 "Chapter 18A"
  BM Chapter 18C flag         ← col_AS 是否含 "Chapter 18C"
  BQ Place of incorporation   ← 招股书前几页 "incorporated in ..."
  CL Earliest cornerstone unlock date ← 上市日 + 6 个月（港交所规则；
                                无基石的 4 家填 NA，依据 cornerstone_absence.json）

只赋值，不改 font/fill/number_format。写前备份。
证据落到 out/derived_flags.json 供审计。
"""
from __future__ import annotations

import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

import openpyxl
import yaml

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
sys.path.insert(0, str(ROOT / "src"))

from contracts import normalize_code  # noqa: E402

HEADERS = {
    "BH": "Listing board",
    "BJ": "A+H issuer flag",
    "BK": "WVR flag",
    "BL": "Chapter 18A flag",
    "BM": "Chapter 18C flag",
    "BQ": "Place of incorporation",
    "CL": "Earliest cornerstone unlock date (dd/mm/yy)",
}
LOCKUP_MONTHS = 6


def norm(s) -> str:
    return " ".join(str(s or "").replace("\n", " ").split()).strip().lower()


def add_months(d: dt.date, months: int) -> dt.date:
    """月末安全加月：2026-08-31 + 6 → 2027-02-28。"""
    y, m = divmod(d.month - 1 + months, 12)
    y, m = d.year + y, m + 1
    import calendar
    return dt.date(y, m, min(d.day, calendar.monthrange(y, m)[1]))


def digits(code: str) -> str:
    return "".join(c for c in str(code) if c.isdigit())


def place_of_incorporation(code: str) -> tuple[str, str]:
    """扫前若干页判断注册地；返回 (值, 证据)。"""
    f = ROOT / "data" / "text" / f"HKIPO-MB{digits(code)}.jsonl"
    if not f.exists():
        return "NA", "缺页级文本"
    head = ""
    for i, line in enumerate(f.open(encoding="utf-8")):
        if i >= 6:
            break
        head += json.loads(line)["text"] + "\n"
    flat = " ".join(head.split())
    # 封面措辞不统一：incorporated / established / organised / formed / registered 都见过
    VERB = r"(?:incorporated|established|organi[sz]ed|formed|registered|constituted)"
    pats = [
        (rf"{VERB}\s+in\s+the\s+People.{{0,3}}s\s+Republic\s+of\s+China", "PRC"),
        (rf"{VERB}\s+in\s+(?:the\s+)?Cayman\s+Islands", "Cayman Islands"),
        (rf"{VERB}\s+in\s+(?:the\s+)?Bermuda", "Bermuda"),
        (rf"{VERB}\s+in\s+the\s+British\s+Virgin\s+Islands", "British Virgin Islands"),
        (rf"{VERB}\s+in\s+Hong\s+Kong", "Hong Kong"),
        # 兜底：直接看 "People's Republic of China with limited liability"
        (r"People.{0,3}s\s+Republic\s+of\s+China\s+with\s+limited\s+liability", "PRC"),
    ]
    for pat, val in pats:
        m = re.search(pat, flat, re.I)
        if m:
            return val, flat[max(0, m.start() - 60):m.end() + 60]
    return "NA", "前 6 页未见注册地表述"


def main() -> int:
    dry = "--dry-run" in sys.argv
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    book = WS / cfg["workbook"]

    # 基石「确认无」的公司
    ca_path = ROOT / "out" / "allot" / "cornerstone_absence.json"
    no_cornerstone = set()
    if ca_path.exists():
        for code, rec in json.loads(ca_path.read_text(encoding="utf-8")).items():
            if rec.get("verdict") == "none":
                no_cornerstone.add(normalize_code(code))

    wb = openpyxl.load_workbook(book)
    ws = wb[cfg["sheet"]]
    col_of = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v in (None, ""):
            continue
        for key, h in HEADERS.items():
            if norm(v) == norm(h):
                col_of[key] = c
    missing = [k for k in HEADERS if k not in col_of]
    if missing:
        wb.close()
        raise SystemExit(f"工作簿找不到列：{missing}")

    # 行号 + 上市日
    row_of, listing = {}, {}
    ci_code = openpyxl.utils.column_index_from_string(cfg["id_columns"]["stock_code"])
    ci_list = openpyxl.utils.column_index_from_string(cfg["id_columns"]["listing_date"])
    for r in range(cfg["data_start_row"], ws.max_row + 1):
        code = ws.cell(r, ci_code).value
        if code in (None, ""):
            continue
        code = str(code).strip()
        row_of[normalize_code(code)] = r
        ld = ws.cell(r, ci_list).value
        if isinstance(ld, dt.datetime):
            ld = ld.date()
        listing[normalize_code(code)] = ld if isinstance(ld, dt.date) else None

    audit, n = {}, 0
    print(f"{'code':9s} {'board':10s} {'A+H':4s} {'WVR':4s} {'18A':4s} {'18C':4s} "
          f"{'注册地':14s} 基石解禁")
    for code, r in sorted(row_of.items()):
        jf = ROOT / "out" / "extracted" / f"HKIPO-MB{digits(code)}.json"
        if not jf.exists():
            print(f"{code:9s} 缺抽取 JSON，跳过")
            continue
        asv = str(json.loads(jf.read_text(encoding="utf-8"))["fields"]["col_AS"]["value"])
        board = "GEM" if re.search(r"\bGEM\b", asv, re.I) else "Main Board"
        a_plus_h = 1 if "A+H" in asv else 0
        wvr = 1 if re.search(r"Chapter\s+8A", asv) else 0
        c18a = 1 if re.search(r"Chapter\s+18A", asv) else 0
        c18c = 1 if re.search(r"Chapter\s+18C", asv) else 0
        inc, inc_ev = place_of_incorporation(code)
        ld = listing.get(code)
        if code in no_cornerstone:
            unlock, unlock_note = "NA", "确认无基石，无解禁日"
        elif ld:
            unlock = add_months(ld, LOCKUP_MONTHS)
            unlock_note = f"上市日 {ld} + {LOCKUP_MONTHS} 个月"
        else:
            unlock, unlock_note = "NA", "缺上市日"
        vals = {"BH": board, "BJ": a_plus_h, "BK": wvr, "BL": c18a, "BM": c18c,
                "BQ": inc, "CL": unlock}
        audit[code] = {"values": {k: str(v) for k, v in vals.items()},
                       "evidence": {"col_AS": asv, "incorporation": inc_ev,
                                    "unlock": unlock_note}}
        # 日期列写成本日期
        if unlock != "NA":
            dtv = unlock
        else:
            dtv = "NA"
        order = ["BH", "BJ", "BK", "BL", "BM", "BQ", "CL"]
        for k in order:
            ws.cell(r, col_of[k]).value = vals[k] if k != "CL" else dtv
        n += 1
        print(f"{code:9s} {board:10s} {a_plus_h:4d} {wvr:4d} {c18a:4d} {c18c:4d} "
              f"{inc:14s} {str(unlock)}")

    outj = ROOT / "out" / "derived_flags.json"
    outj.write_text(json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                    encoding="utf-8")
    print(f"\n推导 {n} 家；证据 -> {outj}")

    if dry:
        wb.close()
        print("--dry-run：未写回")
        return 0

    wb.close()
    backup_dir = book.parent / "backups" / "excel_snapshots"

    backup_dir.mkdir(parents=True, exist_ok=True)

    backup = backup_dir / (f"{book.stem}.backup-before-flags-"
                            f"{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(book, backup)
    wb = openpyxl.load_workbook(book)
    ws = wb[cfg["sheet"]]
    col_of = {}
    for c in range(1, ws.max_column + 1):
        v = ws.cell(1, c).value
        if v in (None, ""):
            continue
        for key, h in HEADERS.items():
            if norm(v) == norm(h):
                col_of[key] = c
    for code, rec in audit.items():
        r = row_of[code]
        for k in ["BH", "BJ", "BK", "BL", "BM", "BQ"]:
            v = rec["values"][k]
            ws.cell(r, col_of[k]).value = int(v) if v.lstrip("-").isdigit() else v
        u = rec["values"]["CL"]
        if u == "NA":
            ws.cell(r, col_of["CL"]).value = "NA"
        else:
            y, m, d = (int(x) for x in u.split("-"))
            ws.cell(r, col_of["CL"]).value = dt.date(y, m, d)
    tmp = book.with_suffix(".saving.xlsx")
    wb.save(tmp)
    wb.close()
    tmp.replace(book)
    print(f"已写回 7 列（{len(audit)} 家）\n备份：{backup.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
