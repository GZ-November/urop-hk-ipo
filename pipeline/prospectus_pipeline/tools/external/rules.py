#!/usr/bin/env python3
"""DN / DO：发售机制与适用规则（确定性，不联网）。

判定：
  DN Offer mechanism（招股书规则优先，配发回拨只作兜底）
    1. 招股书出现 follows/under Mechanism B → B
    2. 招股书出现 follows/under Mechanism A → A
    3. 否则用配发公告 col_CW：明确回拨发生（triggered Yes / 回拨股数>0 / 最终公开占比≥15%）→ A；
       明确未回拨且最终公开≈10% → B
    4. 再否则 NA
  DO Applicable IPO rules / transition basis
    - 按每家公司的招股书日期判断 FINI 与 2025-08-04 定价改革的适用性；
      2025-08-04 pricing reform (Mechanism A/B clawback; six-month cornerstone lock-up retained)
    - 具体机制名附在后面。

港交所 2025-08-04 改革明确：**未采纳**分阶段/3 个月基石解禁，仍为 6 个月。
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[2] if Path(__file__).resolve().parent.name == "external" else Path(__file__).resolve().parent
WS = ROOT.parent
sys.path.insert(0, str(ROOT))
from run import load_cfg

_cfg = load_cfg()
_configured_book = Path(_cfg["workbook"])
BOOK = _configured_book if _configured_book.is_absolute() else WS / _configured_book
SHEET = _cfg.get("sheet", "NLR")
TEXT_DIR = _cfg["paths"]["text"]
ALLOT_OUT = _cfg["paths"]["allot_out"]
DN_HEADER = "Offer mechanism"
DO_HEADER = "Applicable IPO rules / transition basis"
FINI = dt.date(2023, 11, 22)
REFORM = dt.date(2025, 8, 4)
PAT_B = re.compile(r"follows\s+Mechanism\s+B|under\s+Mechanism\s+B|Mechanism\s+B\s+set\s+out", re.I)
PAT_A = re.compile(r"follows\s+Mechanism\s+A|under\s+Mechanism\s+A|Mechanism\s+A\s+set\s+out", re.I)


def to_date(v) -> dt.date | None:
    if isinstance(v, dt.datetime):
        return v.date()
    if isinstance(v, dt.date):
        return v
    return None


def prospectus_mechanism(code: str) -> str | None:
    f = TEXT_DIR / f"HKIPO-MB{''.join(ch for ch in code if ch.isdigit())}.jsonl"
    if not f.exists():
        return None
    text = "\n".join(json.loads(x)["text"] for x in f.open(encoding="utf-8"))
    if PAT_B.search(text):
        return "B"
    if PAT_A.search(text):
        return "A"
    return None


def allot_mechanism(code: str) -> str | None:
    """配发公告回拨描述作兜底。实际发生分档回拨 → A；明确未回拨且公开约 10% → B。"""
    p = ALLOT_OUT / "extracted" / (
        f"HKIPO-MB{''.join(ch for ch in code if ch.isdigit())}.json")
    if not p.exists():
        return None
    rec = json.loads(p.read_text(encoding="utf-8"))
    f = rec.get("fields") or {}
    cw = str((f.get("col_CW") or {}).get("value") or "")
    t = cw.lower().replace("—", "-")
    try:
        ratio = float(f["col_CT"]["value"]) / float(f["col_CS"]["value"])
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        ratio = None
    nums = [int(x.replace(",", "")) for x in
            re.findall(r"reallocated[^\d]{0,80}(\d{1,3}(?:,\d{3})+|\d{4,})", t)]
    moved = max(nums) if nums else 0
    if "claw-back triggered: yes" in t or "reallocation procedure was applied" in t or moved > 0:
        return "A"
    if ratio is not None and ratio >= 0.14:
        return "A"
    if any(k in t for k in ("claw-back triggered: n/a", "claw-back triggered n/a",
                            "claw-back triggered: no", "reallocation: no", "reallocation: n/a",
                            "no claw-back", "no reallocation")):
        return "B"
    if "reallocated" in t and re.search(r"\b0\b", t):
        return "B"
    return None


def rules_text(pd: dt.date, mech: str) -> str:
    parts = []
    if pd >= REFORM:
        parts.append("FINI (from 22/11/2023)")
        parts.append("2025-08-04 pricing reform (Mechanism A/B; six-month cornerstone lock-up retained)")
    elif pd >= FINI:
        parts.append("FINI (from 22/11/2023)")
    else:
        parts.append("Pre-FINI (PN18 statutory clawback; CCASS T+5; six-month cornerstone lock-up)")
    if mech in ("A", "B"):
        parts.append(f"this IPO: Mechanism {mech}")
    return "; ".join(parts) if parts else "NA"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--only", nargs="*", default=None, help="只处理指定股票代码")
    args = ap.parse_args()
    book = Path(args.book)

    wb_read = openpyxl.load_workbook(book, data_only=True)
    ws_read = wb_read[SHEET]
    col = {}
    for c in range(1, ws_read.max_column + 1):
        v = " ".join(str(ws_read.cell(1, c).value or "").replace("\n", " ").split()).strip().lower()
        if v == DN_HEADER.lower():
            col["DN"] = c
        elif v == DO_HEADER.lower():
            col["DO"] = c
        elif v == "chapter 18c flag":
            col["18C"] = c
    if not {"DN", "DO", "18C"}.issubset(col):
        wb_read.close()
        raise SystemExit(f"找不到 DN/DO 列，实得 {col}")

    companies = []
    for r in range(2, ws_read.max_row + 1):
        code = ws_read[f"B{r}"].value
        pd = to_date(ws_read[f"D{r}"].value)
        if code in (None, "") or pd is None:
            continue
        c_str = str(code).strip()
        if args.only and c_str not in args.only:
            continue
        companies.append((r, c_str, pd, ws_read.cell(r, col["18C"]).value))
    wb_read.close()

    print(f"{'code':9s} {'招股书':12s} {'来源':12s} {'机制':4s}  规则")
    values = []
    for r, code, pd, is_18c in companies:
        if pd < REFORM:
            src, mech = "listing date", None
            dn = "Chapter 18C.09 clawback" if is_18c == 1 else "PN18 statutory clawback"
        else:
            src, mech = "prospectus", prospectus_mechanism(code)
            if mech is None:
                mech = allot_mechanism(code)
                src = "allot-CW" if mech else "unknown"
            dn = f"Mechanism {mech}" if mech else "NA"
        do = rules_text(pd, mech or "")
        values.append((r, dn, do))
        print(f"{code:9s} {str(pd):12s} {src:12s} {dn:12s}  {do}")

    if args.dry_run:
        print("\n--dry-run：未写回")
        return 0

    sys.path.insert(0, str(ROOT / "src"))
    from workbook_transaction import workbook_transaction

    with workbook_transaction(book, operation="rules") as wb:
        ws = wb[SHEET]
        for r, dn, do in values:
            ws.cell(r, col["DN"]).value = dn
            ws.cell(r, col["DO"]).value = do

    print(f"\n已写回 DN/DO（{len(values)} 家） -> {book.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
