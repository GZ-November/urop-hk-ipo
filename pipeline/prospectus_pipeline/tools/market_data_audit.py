#!/usr/bin/env python3
"""Integrity audit of cached market data for the 2026 listings at an explicit cutoff.

For every issuer (raw first-day file, adjusted aftermarket cache) and the HSI/HSTECH benchmarks it checks
chronological order, duplicates, nonpositive/nonfinite prices, the first bar against the workbook listing and
day-1 raw close, gaps against the exchange calendar (HSI trading days), bars after the cutoff, last observed
date, abnormal one-day jumps, volume/turnover availability and price-basis labels. Findings are classified,
never repaired: a gap is not filled and a suspension is not a delisting.

    python tools/market_data_audit.py --as-of 2026-09-30
Writes pipeline/reports/repair_handoff/market_data_audit.csv and market_data_audit_summary.md.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]
sys.path[:0] = [str(ROOT), str(ROOT / "src")]
from as_of import resolve_as_of  # noqa: E402

MARKET = ROOT / "data" / "market"
JUMP = 0.5            # |one-day close change| above this is flagged for review, not corrected
OVERRIDES = ROOT / "schema" / "listing_status_overrides.json"


def load(path: Path):
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    for row in rows:
        row["_d"] = dt.date.fromisoformat(str(row["date"])[:10])
    return rows


def finite(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def audit_series(rows, as_of, calendar, first_expected=None):
    notes = []
    if rows is None:
        return {"status": "file_missing"}, ["file_missing"]
    dates = [r["_d"] for r in rows]
    if dates != sorted(dates):
        notes.append("not_chronological")
    if len(set(dates)) != len(dates):
        notes.append("duplicate_dates")
    bad = [r["date"] for r in rows if not all(finite(r.get(k)) and r[k] > 0 for k in ("open", "high", "low", "close"))]
    if bad:
        notes.append(f"nonpositive_or_nonfinite_price:{len(bad)}")
    after = [r for r in rows if r["_d"] > as_of]
    if after:
        notes.append(f"bars_after_cutoff:{len(after)}")
    live = [r for r in rows if r["_d"] <= as_of]
    stats = {"n_bars": len(live), "first_date": live[0]["_d"].isoformat() if live else "",
             "last_date": live[-1]["_d"].isoformat() if live else ""}
    if live and first_expected and live[0]["_d"] != first_expected:
        notes.append(f"first_bar_{live[0]['_d']}_not_listing_{first_expected}")
    if live and calendar:
        have = {r["_d"] for r in live}
        missing = [d for d in calendar if live[0]["_d"] <= d <= live[-1]["_d"] and d not in have]
        stats["missing_vs_hsi_calendar"] = len(missing)
        if missing:
            notes.append(f"gaps_vs_exchange_calendar:{len(missing)}")
        stats["trailing_days_without_bar"] = len([d for d in calendar if d > live[-1]["_d"] and d <= as_of])
    jumps = []
    for prev, cur in zip(live, live[1:]):
        if finite(prev.get("close")) and finite(cur.get("close")) and prev["close"] > 0:
            change = cur["close"] / prev["close"] - 1
            if abs(change) > JUMP:
                jumps.append(f"{cur['date']}:{change:+.0%}")
    stats["large_jumps"] = ";".join(jumps)
    if jumps:
        notes.append(f"large_one_day_moves:{len(jumps)}")
    null_turn = sum(1 for r in live if r.get("turnover") is None)
    zero_vol = sum(1 for r in live if finite(r.get("volume")) and r["volume"] == 0)
    stats.update(turnover_null_days=null_turn, zero_volume_days=zero_vol)
    stats["price_basis"] = ";".join(sorted({str(r.get("price_basis", "unlabelled")) for r in live}))
    return stats, notes


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--as-of", default=None)
    ap.add_argument("--out-dir", default=str(REPO / "pipeline" / "reports" / "repair_handoff"))
    args = ap.parse_args(argv)
    as_of = resolve_as_of(args.as_of)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    hsi = load(MARKET / "aftermarket" / "hsi_bars.json") or []
    calendar = sorted(r["_d"] for r in hsi if r["_d"] <= as_of)
    status_overrides = json.loads(OVERRIDES.read_text(encoding="utf-8")) if OVERRIDES.exists() else {}
    with (REPO / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv").open(encoding="utf-8-sig") as fh:
        issuers = [r for r in csv.DictReader(fh) if r["Date of Listing (dd/mm/yy)"].startswith("2026")]

    rows = []
    for issuer in issuers:
        code = issuer["Stock Code"]
        sym = "hk" + code.split(".")[0].zfill(5)
        listing = dt.date.fromisoformat(issuer["Date of Listing (dd/mm/yy)"][:10])
        record = {"code": code, "cohort": issuer["cohort"], "listing_date": listing.isoformat(), "as_of": as_of.isoformat()}
        adj_stats, adj_notes = audit_series(load(MARKET / "aftermarket" / f"{sym}.json"), as_of, calendar, listing)
        raw = load(MARKET / f"{sym}.json")
        raw_stats, raw_notes = audit_series(raw, as_of, None, listing)
        record.update({f"adj_{k}": v for k, v in adj_stats.items()})
        record.update({f"raw_{k}": v for k, v in raw_stats.items() if k in ("n_bars", "first_date", "last_date", "price_basis", "turnover_null_days")})
        # Day-1 raw close vs the workbook; adjusted day-1 close ratio shows corporate-action adjustment.
        try:
            wb_close = float(issuer["First trading day closing price (HK$)"])
        except ValueError:
            wb_close = None
        raw_close = next((r["close"] for r in raw or [] if r["_d"] == listing), None)
        record["workbook_day1_close"] = wb_close if wb_close is not None else ""
        record["raw_day1_close"] = raw_close if raw_close is not None else ""
        if raw_close is not None and wb_close is not None and abs(raw_close - wb_close) > 1e-6:
            raw_notes.append("raw_day1_close_differs_from_workbook")
        if raw_close is None:
            raw_notes.append("raw_day1_bar_missing")
        adj = load(MARKET / "aftermarket" / f"{sym}.json") or []
        adj_close = next((r["close"] for r in adj if r["_d"] == listing), None)
        record["adj_over_raw_day1_close"] = round(adj_close / raw_close, 6) if adj_close and raw_close else ""
        try:
            offer = float(issuer["IPO Subscription Price (HK$)"])
            record["raw_day1_return"] = round(raw_close / offer - 1, 6) if raw_close and offer else ""
        except ValueError:
            record["raw_day1_return"] = ""
        override = status_overrides.get(code)
        if override:
            adj_notes.append(f"status_override:{override['status']}_from_{override['effective_date']}")
        record["findings"] = ";".join(adj_notes + [f"raw:{n}" for n in raw_notes])
        record["classification"] = ("suspension_documented" if override else
                                    "clean" if not (adj_notes or raw_notes) else "review")
        rows.append(record)

    bench = {}
    for name in ("hsi_bars", "hstech_bars"):
        stats, notes = audit_series(load(MARKET / "aftermarket" / f"{name}.json"), as_of, None)
        bench[name] = (stats, notes)

    keys = list(dict.fromkeys(k for r in rows for k in r))
    with (out_dir / "market_data_audit.csv").open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=keys)
        writer.writeheader()
        writer.writerows(rows)

    from collections import Counter
    classes = Counter(r["classification"] for r in rows)
    lines = [f"# Market data audit at {as_of} (HKT cutoff)\n",
             f"Issuers: {len(rows)}; clean {classes['clean']}, documented suspension {classes['suspension_documented']}, "
             f"needing review {classes['review']}.\n", "## Benchmarks\n"]
    for name, (stats, notes) in bench.items():
        lines.append(f"- {name}: {stats.get('n_bars')} bars {stats.get('first_date')} to {stats.get('last_date')}; "
                     f"findings: {', '.join(notes) or 'none'}")
    lines += ["", "## Issuers needing review\n", "| code | findings |", "|---|---|"]
    for r in rows:
        if r["classification"] == "review":
            lines.append(f"| {r['code']} | {r['findings']} |")
    lines += ["", "Gaps are measured against HSI trading days; a gap is reported, never filled. Large moves are flagged "
              "for review only. Raw (as-traded) first-day closes are compared with the workbook; the adjusted cache is "
              "forward-adjusted and is not an as-traded price series.\n"]
    (out_dir / "market_data_audit_summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
