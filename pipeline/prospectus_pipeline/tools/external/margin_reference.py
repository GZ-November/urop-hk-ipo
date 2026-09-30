"""Export source-reported margin snapshots with one fixed, pre-clawback denominator.

The curated source ledger contains media surveys, not complete broker histories.
Out-of-sample/window records are logged, never relabelled to fit the sample.
"""
import json
from pathlib import Path

import pandas as pd

REPO = Path(__file__).resolve().parents[4]
LEDGER = REPO / "pipeline/prospectus_pipeline/data/margin/reported_snapshots.json"


def export() -> None:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    master = pd.read_csv(REPO / "pipeline/exports/HKIPO-MB-MASTER_clean.csv")
    sample = master[pd.to_datetime(master["Date of Listing (dd/mm/yy)"]).dt.year == 2026].set_index("Stock Code")
    rows, exclusions = [], []
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
            if reason:
                exclusions.append({**item, "date": day, "source": source["url"], "reason": reason})
                continue
            base = float(issuer["Public Offer shares"]) * float(issuer["Maximum Offer Price"])
            if not base > 0:
                raise ValueError(f"Missing initial public tranche denominator: {code}")
            total = float(item["amount_100m_hkd"]) * 1e8
            rows.append({"stock_code": code, "date": day, "margin_total_hkd": total,
                         "margin_multiple": total / base, "initial_public_value_hkd": base,
                         "source": source["url"], "source_group": source["survey"],
                         "source_type": source["source_type"], "published_date": source["published_date"],
                         "retrieved_on": ledger["retrieved_on"]})
    frame = pd.DataFrame(rows).sort_values(["stock_code", "date"])
    frame.to_csv(REPO / "pipeline/exports/HKIPO-2026-margin-daily.csv", index=False)
    (REPO / "pipeline/reports/margin_review/source_exclusions.json").write_text(json.dumps(exclusions, indent=2) + "\n")
    print(f"Margin snapshots: {len(frame)} rows / {frame.stock_code.nunique()} issuers; {len(exclusions)} excluded")


if __name__ == "__main__":
    export()
