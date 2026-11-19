#!/usr/bin/env python3
"""
aggregate_pilot_48_dataset.py
Aggregates all 48 pilot historical micro-mechanism extraction JSONs
into analysis/out/pilot_48_extracted_dataset.csv and generates
a comprehensive field coverage and quality report.
"""

import os
import json
import glob
import pandas as pd

EXTRACTED_DIR = "analysis/out/pilot_48_extracted"
OUTPUT_CSV = "analysis/out/pilot_48_extracted_dataset.csv"
OUTPUT_AUDIT_MD = "analysis/out/pilot_48_coverage_audit.md"

ALL_FIELDS = [
    # 14 Issuer Characteristics
    "founding_year", "col_BP", "col_BQ", "col_BR", "col_AR", "col_AS",
    "col_AT", "col_Y", "col_AB", "col_AE", "col_AH", "col_AK", "col_AN", "col_AU",
    # 14 Offering Mechanisms
    "col_L", "col_M", "col_Q", "col_P", "col_R", "col_S", "col_T", "col_U",
    "col_AQ", "col_CK", "col_CM", "col_CP", "col_CT", "col_CW",
    # 4 Bonus Financial Fields
    "col_AG", "col_AF", "col_AM", "col_AL"
]

def main():
    json_files = sorted(glob.glob(os.path.join(EXTRACTED_DIR, "*.json")))
    print(f"Found {len(json_files)} extracted JSON files in {EXTRACTED_DIR}")

    records = []
    for fpath in json_files:
        fname = os.path.basename(fpath)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"Error loading {fname}: {e}")
            continue

        stock_code = data.get("stock_code")
        company_name = data.get("company_name")
        batch_id = data.get("batch_id")
        epoch = data.get("epoch")
        board = data.get("board")
        harvest_status = data.get("harvest_status")
        fields = data.get("fields", {})

        row = {
            "file": fname,
            "stock_code": stock_code,
            "company_name": company_name,
            "batch_id": batch_id,
            "epoch": epoch,
            "board": board,
            "harvest_status": harvest_status
        }

        for fld in ALL_FIELDS:
            finfo = fields.get(fld, {})
            if isinstance(finfo, dict):
                row[fld] = finfo.get("value")
                row[f"{fld}__page"] = finfo.get("page")
                row[f"{fld}__quote"] = finfo.get("quote")
            else:
                row[fld] = finfo
                row[f"{fld}__page"] = None
                row[f"{fld}__quote"] = None

        records.append(row)

    df = pd.DataFrame(records)
    df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
    print(f"Saved {len(df)} deals to {OUTPUT_CSV}")

    # Generate coverage audit
    audit_lines = [
        "# Pilot 48 Historical Micro-Mechanism Extraction Audit",
        f"Generated from {len(df)} extracted deals across 4 cohorts (1994–2024).\n",
        "## 1. Batch & Cohort Summary",
        "| Batch | Epoch | Total Extracted | Target Deals | Completion Rate | Status |",
        "|---|---|---|---|---|---|"
    ]

    batch_targets = {1: 12, 2: 12, 3: 12, 4: 12}
    batch_epochs = {1: "2018-2024", 2: "2008-2017", 3: "2002-2007", 4: "1994-2001"}

    for b in [1, 2, 3, 4]:
        sub_df = df[df["batch_id"] == b] if "batch_id" in df else pd.DataFrame()
        n = len(sub_df)
        target = batch_targets[b]
        rate = f"{n / target * 100:.1f}%"
        status = "COMPLETE" if n == target else f"{n}/{target} running"
        audit_lines.append(f"| Batch {b} | {batch_epochs[b]} | {n} | {target} | {rate} | {status} |")

    audit_lines.append(f"| **Total** | **1994–2024 (33 Years)** | **{len(df)}** | **48** | **{len(df)/48*100:.1f}%** | **{'COMPLETE' if len(df)==48 else 'IN PROGRESS'}** |\n")

    audit_lines.append("## 2. Field-Level Coverage Across All Available Deals")
    audit_lines.append("| Field Category | Field ID | Description | Non-Null Count | Coverage % | Online Electronic Coverage (Excl Pre-1999) |")
    audit_lines.append("|---|---|---|---|---|---|")

    field_desc = {
        "founding_year": ("Issuer", "Earliest establishment year"),
        "col_BP": ("Issuer", "Incorporation date of listing vehicle"),
        "col_BQ": ("Issuer", "Place of incorporation (domicile)"),
        "col_BR": ("Issuer", "Headquarters country/region"),
        "col_AR": ("Issuer", "Business description"),
        "col_AS": ("Issuer", "Listing rule chapter / track record test"),
        "col_AT": ("Issuer", "Audited year-1 stub/annual end date"),
        "col_Y": ("Financial", "Total assets at year-1 end"),
        "col_AB": ("Financial", "Total equity / net assets at year-1 end"),
        "col_AE": ("Financial", "Total liabilities at year-1 end"),
        "col_AH": ("Financial", "Revenue of year-1 (annualised if stub)"),
        "col_AK": ("Financial", "Profit before tax of year-1 (annualised)"),
        "col_AN": ("Financial", "Profit for period / net income of year-1"),
        "col_AU": ("Financial", "Operating cash flow (unannualised stub)"),
        "col_L": ("Mechanism", "Total issued share capital post-IPO"),
        "col_M": ("Mechanism", "Total offer shares"),
        "col_Q": ("Mechanism", "New shares issued by company"),
        "col_P": ("Mechanism", "Vendor / secondary shares offered"),
        "col_R": ("Mechanism", "Placing shares initially available"),
        "col_S": ("Mechanism", "Hong Kong public offer shares initially available"),
        "col_T": ("Mechanism", "Maximum offer price (HKD)"),
        "col_U": ("Mechanism", "Minimum offer price (HKD)"),
        "col_AQ": ("Mechanism", "Greenshoe / over-allotment %"),
        "col_CK": ("Mechanism", "Cornerstone allocation %"),
        "col_CM": ("Mechanism", "Retail oversubscription ratio"),
        "col_CP": ("Mechanism", "Retail application count / announcement text"),
        "col_CT": ("Mechanism", "Final public offer shares post-clawback"),
        "col_CW": ("Mechanism", "Clawback / reallocation explanation text"),
        "col_AG": ("Bonus Fin", "Revenue of year-2"),
        "col_AF": ("Bonus Fin", "Revenue of year-3"),
        "col_AM": ("Bonus Fin", "Profit for the year of year-2"),
        "col_AL": ("Bonus Fin", "Profit for the year of year-3"),
    }

    online_df = df[df["harvest_status"] != "pre_1999_physical_cutoff"]

    for fld in ALL_FIELDS:
        cat, desc = field_desc.get(fld, ("Other", fld))
        total_cnt = df[fld].notna().sum()
        total_pct = f"{total_cnt / len(df) * 100:.1f}%" if len(df) > 0 else "0.0%"
        online_cnt = online_df[fld].notna().sum() if len(online_df) > 0 else 0
        online_pct = f"{online_cnt / len(online_df) * 100:.1f}%" if len(online_df) > 0 else "0.0%"
        audit_lines.append(f"| {cat} | `{fld}` | {desc} | {total_cnt}/{len(df)} | {total_pct} | {online_cnt}/{len(online_df)} ({online_pct}) |")

    with open(OUTPUT_AUDIT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(audit_lines) + "\n")

    print(f"Generated coverage audit at {OUTPUT_AUDIT_MD}")

if __name__ == "__main__":
    main()
