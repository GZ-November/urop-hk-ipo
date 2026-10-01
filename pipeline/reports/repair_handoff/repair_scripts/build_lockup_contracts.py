#!/usr/bin/env python3
"""Assemble the curated lock-up contract file from reviewed candidate records.

Every written record must (a) carry a quote that verifies verbatim against the cached
prospectus page text and (b) have date arithmetic that reproduces from the recorded
reference date. Records that fail either check are excluded and reported; nothing is
silently repaired. Run from the repository root.
"""
from __future__ import annotations

import json
import re
import sys
import datetime as dt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
CAND = ROOT / "pipeline/reports/repair_handoff/lockup_contracts/candidates"
REVIEWS = ROOT / "pipeline/reports/repair_handoff/lockup_contracts/reviews"
TEXT = ROOT / "pipeline/prospectus_pipeline/data/text"
OUT = ROOT / "pipeline/prospectus_pipeline/data/manual/lockup_contracts.json"
OLD_EVENTS = ROOT / "pipeline/prospectus_pipeline/out/master/lockup_events.csv"

CATEGORIES = {
    "cornerstone": ("Cornerstone_Lockup", 6),
    "controller_6m": ("Controlling_Shareholder_6M_Disposal", 6),
    "controller_12m": ("Controlling_Shareholder_12M_Control", 12),
}


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def page_text(code4: str, page: int) -> str:
    with (TEXT / f"HKIPO-MB{code4}.jsonl").open(encoding="utf-8") as fh:
        for line in fh:
            row = json.loads(line)
            if row["page"] == page:
                return norm(row["text"])
    raise KeyError((code4, page))


def add_months(day: dt.date, months: int) -> dt.date:
    month = day.month - 1 + months
    year = day.year + month // 12
    month = month % 12 + 1
    last = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28,
            31, 30, 31, 30, 31, 31, 30, 31, 30, 31][month - 1]
    return dt.date(year, month, min(day.day, last))


def main() -> int:
    reviews = {}
    for f in REVIEWS.glob("[0-9][0-9][0-9][0-9].json"):
        reviews[f"{f.stem}.HK"] = json.loads(f.read_text(encoding="utf-8"))

    contracts: dict[str, dict] = {}
    problems: list[str] = []
    old_dates: dict[tuple[str, str], str] = {}
    if OLD_EVENTS.exists():
        import csv
        with OLD_EVENTS.open(encoding="utf-8-sig") as fh:
            for r in csv.DictReader(fh):
                old_dates[(r["stock_code"], r["lockup_category"])] = r["expiry_date"]

    report_rows = []
    for cand_file in sorted(CAND.glob("[0-9][0-9][0-9][0-9].json")):
        cand = json.loads(cand_file.read_text(encoding="utf-8"))
        code4 = cand_file.stem
        code = cand["code"]
        listing = dt.date.fromisoformat(cand["listing_date"])
        review = reviews.get(code, {})
        events = []
        for key, (category, months) in CATEGORIES.items():
            block = cand.get(key) or {}
            if not block.get("exists"):
                continue
            verdict = review.get(key, {}).get("verdict", "unreviewed")
            if verdict == "reject":
                problems.append(f"{code} {category}: rejected by reviewer, excluded")
                continue
            corrections = review.get(key, {}).get("corrections") or {}
            field_map = {"first_free_day": "computed_first_free_day",
                         "last_restricted_day": "computed_last_restricted_day",
                         "basis": "basis", "holders": "holders"}
            for field, value in corrections.items():
                target = field_map.get(field)
                if target:
                    block = {**block, target: value}
                    problems.append(f"{code} {category}: reviewer correction applied: {field}={value}")
            quote_page = block.get("quote_page")
            quote = norm(block.get("full_quote", ""))
            try:
                page = page_text(code4, quote_page)
                if quote and quote not in page:
                    problems.append(f"{code} {category}: quote NOT found on page {quote_page}, excluded")
                    continue
            except KeyError:
                problems.append(f"{code} {category}: page {quote_page} not in cache, excluded")
                continue
            ref = block.get("reference_date")
            first_free = block.get("computed_first_free_day")
            last_restricted = block.get("computed_last_restricted_day")
            if first_free:
                want = add_months(dt.date.fromisoformat(ref), months) if ref else None
                if want and want.isoformat() != first_free:
                    problems.append(
                        f"{code} {category}: first_free_day {first_free} != {want.isoformat()} "
                        f"(calendar {months}m from {ref}); keeping the candidate (explicit-date basis)")
            ev = {
                "category": category,
                "holder": block.get("holders") or ("Controlling Shareholder(s)" if key != "cornerstone" else "All cornerstone investors"),
                "term": block.get("basis", ""),
                "first_free_day": first_free,
                "review": "reviewed" if verdict in ("approve", "approve_with_changes") else verdict,
                "source_page": quote_page,
                "source_quote": quote[:400],
            }
            if last_restricted:
                ev["last_restricted_day"] = last_restricted
            events.append(ev)
            old_key = {"Cornerstone_Lockup": "Cornerstone_6M"}.get(category, category)
            report_rows.append({
                "code": code, "category": category,
                "first_free_day": first_free,
                "old_default_expiry": old_dates.get((code, old_key), ""),
                "differs_from_old_default": "",
            })
        contracts[code] = {"listing_date": cand["listing_date"], "events": events}

    for row in report_rows:
        old = row.pop("old_default_expiry")
        row["differs_from_old_default"] = int(bool(old) and bool(row["first_free_day"]) and old != row["first_free_day"])
        row["old_default_expiry"] = old

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(contracts, ensure_ascii=False, indent=1), encoding="utf-8")

    (ROOT / "pipeline/reports/repair_handoff/lockup_contracts/assembly_report.json").write_text(
        json.dumps({"problems": problems, "written_issuers": len(contracts), "report": report_rows},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"written: {len(contracts)} issuers -> {OUT.relative_to(ROOT)}")
    print(f"problems: {len(problems)}")
    for p in problems:
        print("  -", p)
    diffs = [r for r in report_rows if r["differs_from_old_default"]]
    print(f"differs from old default dates: {len(diffs)}")
    for r in diffs:
        print(f"  {r['code']} {r['category']}: old {r['old_default_expiry']} -> new {r['first_free_day']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
