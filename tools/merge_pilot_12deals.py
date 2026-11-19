#!/usr/bin/env python3
"""Merge and validate the 12 pilot 2023-2024 micro-mechanism records."""
import json
import pandas as pd
from pathlib import Path

extracted_dir = Path("pipeline/downloads/pilot_2023_2024/extracted")
out_dir = Path("analysis/out")
out_dir.mkdir(parents=True, exist_ok=True)

codes = [
    "0300.HK", "6959.HK", "2402.HK", "2469.HK", "1405.HK", "2409.HK",
    "2228.HK", "1541.HK", "6979.HK", "9676.HK", "2498.HK", "2433.HK"
]

rows = []
missing_codes = []

for code in codes:
    p = extracted_dir / f"{code}.json"
    if not p.exists():
        missing_codes.append(code)
        continue
    data = json.loads(p.read_text(encoding="utf-8"))
    # Separate evidence from flat columns
    evidence = data.pop("evidence", {})
    data["evidence_json"] = json.dumps(evidence, ensure_ascii=False)
    rows.append(data)

print(f"Loaded {len(rows)}/12 records. Missing: {missing_codes}")

if rows:
    df = pd.DataFrame(rows)
    # Save flat table
    out_csv = out_dir / "pilot_2023_2024_mechanism_12deals.csv"
    df.to_csv(out_csv, index=False)
    print(f"Saved {len(df)} records to {out_csv}")
    print(df[["stock_code", "company_name", "final_offer_price_hkd", "pricing_structure", "clawback_triggered", "clawback_mechanism_type", "retail_subscription_ratio", "one_lot_ballot_allocation_pct", "pool_b_cutoff_allocation_pct"]])
