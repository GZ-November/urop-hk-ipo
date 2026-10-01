"""Export source-reported margin snapshots with one fixed, pre-clawback denominator.

The curated source ledger contains media surveys, not complete broker histories.
Out-of-sample/window records are logged, never relabelled to fit the sample.
"""
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[4]
LEDGER = REPO / "pipeline/prospectus_pipeline/data/margin/reported_snapshots.json"


TIMETABLES = REPO / "pipeline/prospectus_pipeline/data/manual/subscription_timetables.json"


def availability(obs_day: str, published_at: str, close_day: str, close_time: str) -> str:
    """Whether the snapshot was demonstrably public before the subscription deadline.

    An article from an earlier calendar day than the closing day is public before the deadline. On the
    closing day it counts only when its publication time is known and earlier than a documented deadline.
    A later article could not have informed a decision at the deadline. Unknown times stay unknown.
    """
    published_day = (published_at or obs_day)[:10]
    if published_day < close_day:
        return "yes_published_before_closing_day"
    if published_day > close_day:
        return "no_published_after_closing_day"
    if not published_at or not close_time:
        return "unknown_closing_day_time_missing"
    return "yes_before_deadline" if published_at[11:16] < close_time else "no_after_deadline"


def export() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    master = pd.read_csv(REPO / "pipeline/exports/HKIPO-MB-MASTER_clean.csv")
    sample = master[pd.to_datetime(master["Date of Listing (dd/mm/yy)"]).dt.year == 2026].set_index("Stock Code")
    timetables = json.loads(TIMETABLES.read_text(encoding="utf-8")) if TIMETABLES.exists() else {}
    rows, exclusions, seen = [], [], {}
    for source in ledger["sources"]:
        for item in source["observations"]:
            code, day = item["stock_code"], source["date"]
            reason = ""
            if code not in sample.index:
                reason = "outside stored 2026 Main Board sample"
            else:
                issuer = sample.loc[code]
                if not issuer["Subscription opening date"] <= day <= issuer["Subscription closing date"]:
                    reason = "outside subscription window"
            total = float(item["amount_100m_hkd"]) * 1e8
            if not reason and (code, day) in seen:
                if abs(seen[(code, day)]["margin_total_hkd"] - total) > 1:
                    reason = "duplicate issuer/date with a different amount (unresolved conflict; neither ingested)"
                    rows.remove(seen[(code, day)])
                else:
                    reason = "duplicate issuer/date with an equal amount (single record kept)"
            if reason:
                exclusions.append({**item, "date": day, "source": source["url"], "reason": reason})
                continue
            base = float(issuer["Public Offer shares"]) * float(issuer["Maximum Offer Price"])
            if not base > 0:
                raise ValueError(f"Missing initial public tranche denominator: {code}")
            close_day = issuer["Subscription closing date"]
            close_time = (timetables.get(code) or {}).get("close_time_hkt") or ""
            pricing = issuer.get("Pricing date")
            published_at = source.get("published_at_hkt", "")
            row = {"stock_code": code, "date": day, "margin_total_hkd": total,
                   "margin_multiple": total / base, "initial_public_value_hkd": base,
                   "source": source["url"], "source_group": source["survey"],
                   "source_type": source["source_type"], "published_date": source["published_date"],
                   "published_at_hkt": published_at,
                   "measurement_wording": source.get("measurement_wording", ""),
                   "survey_scope_wording": source.get("survey_scope_wording", ""),
                   "scope_class": source.get("scope_class", ""),
                   "subscription_close_date": close_day,
                   "subscription_deadline_hkt": f"{close_day}T{close_time}+08:00" if close_time else "",
                   "pricing_date": "" if pd.isna(pricing) else str(pricing)[:10],
                   "pricing_time_hkt": "",
                   "days_to_deadline": (pd.Timestamp(close_day) - pd.Timestamp(day)).days,
                   "available_before_deadline": availability(day, published_at, close_day, close_time),
                   "retrieved_on": ledger["retrieved_on"]}
            rows.append(row)
            seen[(code, day)] = row
    frame = pd.DataFrame(rows).sort_values(["stock_code", "date"])
    frame.to_csv(REPO / "pipeline/exports/HKIPO-2026-margin-daily.csv", index=False)
    (REPO / "pipeline/reports/margin_review/source_exclusions.json").write_text(json.dumps(exclusions, indent=2) + "\n")
    print(f"Margin snapshots: {len(frame)} rows / {frame.stock_code.nunique()} issuers; {len(exclusions)} excluded; "
          f"availability: {frame.available_before_deadline.value_counts().to_dict()}")


if __name__ == "__main__":
    export()
