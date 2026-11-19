#!/usr/bin/env python3
"""
verify_pilot_48_extraction.py
Deterministic reconciliation of 48-issuer historical extractions against
clean 33-year benchmark panel (Section 0 ground truth).
"""

import pandas as pd

PANEL_CSV = "analysis/out/overview_1994_2026/clean_33y_hkipo_panel_1994_2026_enriched.csv"
EXTRACTED_CSV = "analysis/out/pilot_48_extracted_dataset.csv"
OUTPUT_REPORT_MD = "analysis/out/pilot_48_reconciliation_report.md"

def normalize_domicile(val):
    if pd.isna(val) or val is None:
        return "UNKNOWN"
    s = str(val).lower()
    if "cayman" in s:
        return "Cayman Islands"
    if "bermuda" in s:
        return "Bermuda"
    if "prc" in s or "china" in s or "people's republic" in s:
        return "PRC"
    if "hong kong" in s:
        return "Hong Kong"
    return str(val)

def main():
    print("Loading datasets for reconciliation...")
    panel = pd.read_csv(PANEL_CSV)
    ext = pd.read_csv(EXTRACTED_CSV)
    probe = pd.read_csv("analysis/out/overview_1994_2026/pilot_48_source_probe.csv")
    
    # Use probe to disambiguate exact listing dates for the 48 pilot issuers
    pilot_keys = probe[["batch_id", "stock_code", "listing_date", "cohort_year", "funds_raised_total_hkd", "retail_sub_ratio_clean"]].copy()
    
    # Merge ext with pilot_keys first
    ext_keyed = pd.merge(ext, pilot_keys, on=["batch_id", "stock_code"], suffixes=("", "_probe"))
    
    # Merge with full panel on stock_code and listing_date
    merged = pd.merge(ext_keyed, panel, on=["stock_code", "listing_date"], suffixes=("_ext", "_panel"))
    print(f"Successfully matched exactly {len(merged)} unique deals between extracted dataset and panel benchmark.")
    
    reconciliation_results = []
    
    for idx, row in merged.iterrows():
        code = row["stock_code"]
        name = row["company_name_ext"]
        batch = row["batch_id"]
        epoch = row["epoch_ext"]
        board = row["board_ext"]
        
        # 1. Offer Price Check
        ext_price = row.get("col_T")
        pan_price = row.get("offer_price_hkd")
        price_diff = None
        price_match = False
        if pd.notna(ext_price) and pd.notna(pan_price):
            price_diff = abs(float(ext_price) - float(pan_price))
            price_match = price_diff < 0.05 or (price_diff / float(pan_price)) < 0.02
        elif pd.isna(ext_price) and pd.isna(pan_price):
            price_match = True
            
        # 2. Domicile Check
        ext_dom = normalize_domicile(row.get("col_BQ"))
        pan_dom = normalize_domicile(row.get("isin_domicile_jurisdiction"))
        dom_match = (ext_dom == pan_dom) or ("UNKNOWN" in [ext_dom, pan_dom])
        
        # 3. Secondary Sale Check
        ext_p = row.get("col_P")
        ext_has_sec = (float(ext_p) > 0) if pd.notna(ext_p) else None
        pan_has_sec = bool(row.get("bbg_secondary_sale_flag")) if pd.notna(row.get("bbg_secondary_sale_flag")) else None
        sec_match = (ext_has_sec == pan_has_sec) if (ext_has_sec is not None and pan_has_sec is not None) else True
        
        # 4. Retail Subscription Ratio Check
        ext_sub = row.get("col_CM")
        pan_sub = row.get("retail_sub_ratio_clean")
        if pd.isna(pan_sub):
            pan_sub = row.get("gem_subscription_ratio")
        sub_match = False
        if pd.notna(ext_sub) and pd.notna(pan_sub):
            sub_diff = abs(float(ext_sub) - float(pan_sub))
            sub_match = sub_diff < 0.5 or (sub_diff / (float(pan_sub) + 1e-4)) < 0.05
        elif pd.isna(ext_sub) and pd.isna(pan_sub):
            sub_match = True
            
        # 5. Financial Balance Sheet Identity (Assets >= Equity)
        y = row.get("col_Y")
        ab = row.get("col_AB")
        ae = row.get("col_AE")
        fin_valid = True
        if pd.notna(y) and pd.notna(ab):
            fin_valid = float(y) >= (float(ab) - 1.0)
            
        reconciliation_results.append({
            "stock_code": code,
            "company_name": name,
            "batch_id": batch,
            "epoch": epoch,
            "board": board,
            "ext_price": ext_price,
            "pan_price": pan_price,
            "price_match": price_match,
            "ext_dom": ext_dom,
            "pan_dom": pan_dom,
            "dom_match": dom_match,
            "ext_has_sec": ext_has_sec,
            "pan_has_sec": pan_has_sec,
            "sec_match": sec_match,
            "ext_sub": ext_sub,
            "pan_sub": pan_sub,
            "sub_match": sub_match,
            "fin_valid": fin_valid
        })
        
    res_df = pd.DataFrame(reconciliation_results)
    
    # Generate Markdown Report
    total_deals = len(res_df)
    price_acc = res_df["price_match"].mean() * 100
    dom_acc = res_df["dom_match"].mean() * 100
    sec_acc = res_df["sec_match"].mean() * 100
    sub_matched_rows = res_df[res_df["pan_sub"].notna()]
    sub_acc = sub_matched_rows["sub_match"].mean() * 100 if len(sub_matched_rows) > 0 else 100.0
    fin_acc = res_df["fin_valid"].mean() * 100
    
    lines = [
        "# Pilot 48 Historical Micro-Mechanism Reconciliation Report",
        "Deterministic benchmark validation against official 33-year Section 0 ground truth (`clean_33y_hkipo_panel_1994_2026_enriched.csv`).",
        "",
        "## 1. Executive Summary & Verification Metrics",
        f"- **Total Pilot Sample Size**: {total_deals} stratified issuers (1994–2024)",
        f"- **Offer Price Concordance Rate**: **{price_acc:.1f}%** ({res_df['price_match'].sum()}/{total_deals})",
        f"- **Jurisdiction / Domicile Concordance Rate**: **{dom_acc:.1f}%** ({res_df['dom_match'].sum()}/{total_deals})",
        f"- **Secondary Divestment Flag Concordance Rate**: **{sec_acc:.1f}%** ({res_df['sec_match'].sum()}/{total_deals})",
        f"- **Retail Oversubscription Concordance Rate**: **{sub_acc:.1f}%** (among deals with benchmark records)",
        f"- **Accounting Balance Sheet Identity Compliance**: **{fin_acc:.1f}%** (Total Assets >= Total Equity)",
        "",
        "## 2. Cohort-by-Cohort Reconciliation Breakdown",
        "| Cohort Batch | Era | Deals | Offer Price Match | Domicile Match | Secondary Match | BS Identity Match |",
        "|---|---|---|---|---|---|---|"
    ]
    
    for b in sorted(res_df["batch_id"].unique()):
        sub = res_df[res_df["batch_id"] == b]
        b_name = sub["epoch"].iloc[0]
        n = len(sub)
        p_m = f"{sub['price_match'].mean()*100:.1f}%"
        d_m = f"{sub['dom_match'].mean()*100:.1f}%"
        s_m = f"{sub['sec_match'].mean()*100:.1f}%"
        f_m = f"{sub['fin_valid'].mean()*100:.1f}%"
        lines.append(f"| Batch {b} | {b_name} | {n} | {p_m} | {d_m} | {s_m} | {f_m} |")
        
    lines.extend([
        "",
        "## 3. Detailed Audit Table (48 Issuers)",
        "| Stock Code | Company Name | Batch | Extracted Price | Panel Price | Price Match | Domicile (Ext / Pan) | Sec Sale (Ext / Pan) | Retail Sub (Ext / Pan) |",
        "|---|---|---|---|---|---|---|---|---|"
    ])
    
    for idx, r in res_df.iterrows():
        p_str = f"HK$ {r['ext_price']:.2f}" if pd.notna(r['ext_price']) else "N/A"
        pp_str = f"HK$ {r['pan_price']:.2f}" if pd.notna(r['pan_price']) else "N/A"
        p_icon = "PASS" if r['price_match'] else "FAIL"
        dom_str = f"{r['ext_dom']} / {r['pan_dom']}"
        sec_str = f"{r['ext_has_sec']} / {r['pan_has_sec']}"
        sub_str = f"{r['ext_sub'] if pd.notna(r['ext_sub']) else 'N/A'} / {r['pan_sub'] if pd.notna(r['pan_sub']) else 'N/A'}"
        lines.append(f"| `{r['stock_code']}` | {r['company_name']} | Batch {r['batch_id']} | {p_str} | {pp_str} | **{p_icon}** | {dom_str} | {sec_str} | {sub_str} |")
        
    with open(OUTPUT_REPORT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
        
    print(f"Reconciliation complete! Written to {OUTPUT_REPORT_MD}")

if __name__ == "__main__":
    main()
