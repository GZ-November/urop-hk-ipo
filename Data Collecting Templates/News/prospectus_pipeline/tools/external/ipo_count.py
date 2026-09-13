#!/usr/bin/env python3
"""DE = 招股书日前 90 个自然日内港股主板普通 IPO 家数。

来源：HKEx New Listing Information `NLR2025_Eng.xlsx` + `NLR2026_Eng.xlsx`。
窗口：[D−90, D)，按**上市日**计；同一股票代码只计一次。
剔除：介绍上市 / 无募资（募资额两行均为空或 0，或公司名含 Introduction）。
"""
from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
BOOK = WS / "HKIPO-MB2026Q1.xlsx"
NLR_FILES = [WS / "sources" / "NLR2025_Eng.xlsx" if (WS / "sources" / "NLR2025_Eng.xlsx").exists() else WS / "NLR2025_Eng.xlsx", WS / "sources" / "NLR2026_Eng.xlsx" if (WS / "sources" / "NLR2026_Eng.xlsx").exists() else WS / "NLR2026_Eng.xlsx"]
SHEET = "NLR"
HEADER = "HK ordinary IPO count in 90 calendar days before prospectus"


def to_date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return None


def load_listings(path: Path) -> list[dict]:
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb[wb.sheetnames[0]]
    rows = list(ws.iter_rows(values_only=True))
    wb.close()
    # 找表头行
    hdr_i = None
    for i, r in enumerate(rows[:8]):
        vals = [str(x or "").lower() for x in r[:6]]
        if any("stock code" in v for v in vals):
            hdr_i = i
            break
    if hdr_i is None:
        raise SystemExit("NLR 表找不到 Stock Code 表头")
    out, current = [], None
    for r in rows[hdr_i + 1:]:
        code = r[1]
        name = r[2]
        listing = to_date(r[4])
        funds = r[8]
        if code not in (None, "", '"') and str(code).strip() not in ('"',):
            if current:
                out.append(current)
            d = "".join(ch for ch in str(code) if ch.isdigit())
            current = {
                "code": f"{int(d):04d}.HK" if d else str(code),
                "name": str(name or ""),
                "listing": listing,
                "funds": 0.0,
            }
            try:
                current["funds"] += float(funds or 0)
            except (TypeError, ValueError):
                pass
        elif current is not None:
            try:
                current["funds"] += float(funds or 0)
            except (TypeError, ValueError):
                pass
    if current:
        out.append(current)
    # 剔除介绍上市 / 无募资
    kept = []
    for rec in out:
        nm = rec["name"].lower()
        if "introduction" in nm or "介绍上市" in rec["name"]:
            continue
        if rec["listing"] is None:
            continue
        if rec["funds"] <= 0:
            continue
        kept.append(rec)
    return kept


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--nlr", nargs="*", default=[str(p) for p in NLR_FILES])
    args = ap.parse_args()
    book = Path(args.book)

    listings, seen = [], set()
    for path in args.nlr:
        recs = load_listings(Path(path))
        print(f"{Path(path).name}: {len(recs)} 家")
        for rec in recs:
            if rec["code"] in seen:
                continue
            seen.add(rec["code"])
            listings.append(rec)
    print(f"合计普通 IPO {len(listings)} 家，上市日 "
          f"{min(x['listing'] for x in listings)} ~ {max(x['listing'] for x in listings)}")

    wb = openpyxl.load_workbook(book)
    ws = wb[SHEET]
    col = None
    for c in range(1, ws.max_column + 1):
        v = " ".join(str(ws.cell(1, c).value or "").replace("\n", " ").split()).strip().lower()
        if v == HEADER.lower():
            col = c
            break
    if col is None:
        wb.close()
        raise SystemExit(f"找不到列 {HEADER!r}")

    companies = []
    for r in range(2, ws.max_row + 1):
        code = ws[f"B{r}"].value
        pd = to_date(ws[f"D{r}"].value)
        if code in (None, "") or pd is None:
            continue
        companies.append((r, str(code).strip(), pd))

    print(f"\n{'code':9s} {'招股书':12s} {'窗口':26s} {'家数':>4s}")
    values = []
    for r, code, pd in companies:
        lo, hi = pd - dt.timedelta(days=90), pd
        n = sum(1 for x in listings if lo <= x["listing"] < hi)
        values.append((r, n))
        print(f"{code:9s} {str(pd):12s} [{lo} , {hi}) {n:4d}")

    if args.dry_run:
        wb.close()
        print("\n--dry-run：未写回")
        return 0

    wb.close()
    backup_dir = book.parent / "backups" / "excel_snapshots"

    backup_dir.mkdir(parents=True, exist_ok=True)

    backup = backup_dir / (f"{book.stem}.backup-before-ipocount-"
                            f"{dt.datetime.now():%Y%m%d-%H%M%S}.xlsx")
    shutil.copy2(book, backup)
    wb = openpyxl.load_workbook(book)
    ws = wb[SHEET]
    for r, n in values:
        ws.cell(r, col).value = int(n)
    tmp = book.with_suffix(".saving.xlsx")
    wb.save(tmp)
    wb.close()
    tmp.replace(book)
    print(f"\n已写回 DE（{len(values)} 家）\n备份：{backup.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
