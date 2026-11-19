import os
import re
import pandas as pd

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
IN_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/in/bloomberg"

print("=================================================================")
print("STEP 1: MERGING BLOOMBERG ECDR PART 1 AND PART 2")
print("=================================================================")

f1_path = os.path.join(IN_DIR, "ecdr_export_part1.csv")
f2_path = os.path.join(IN_DIR, "ecdr_export_part2.csv")

df1 = pd.read_csv(f1_path)
df2 = pd.read_csv(f2_path)

print(f"Loaded Part 1: {df1.shape}")
print(f"Loaded Part 2: {df2.shape}")

# Ensure clean common keys
df1["ticker_key"] = df1["Ticker"].astype(str).str.strip()
df2["ticker_key"] = df2["Issuer Ticker"].astype(str).str.strip()

# Deduplicate if any, keeping first
df1 = df1.drop_duplicates(subset=["ticker_key"])
df2 = df2.drop_duplicates(subset=["ticker_key"])

# Columns in df2 to add to df1
cols_to_add = [
    c for c in df2.columns
    if c not in df1.columns and c not in ["Issuer Ticker", "Issuer Name", "Offer Type", "Offer Price", "Priced Range", "Primary Exchange", "First Selling Stockholder"]
]

df_bbg = pd.merge(df1, df2[["ticker_key"] + cols_to_add], on="ticker_key", how="left")
print(f"Merged Bloomberg Dataset Shape: {df_bbg.shape}")

# Clean and standardize columns
df_bbg["bbg_ticker"] = df_bbg["ticker_key"]
df_bbg["bbg_offer_price"] = pd.to_numeric(df_bbg["Offer Price"], errors="coerce")
df_bbg["bbg_offer_size_m"] = pd.to_numeric(df_bbg["Offer Size (M)"], errors="coerce")
df_bbg["bbg_gross_spread_pct"] = pd.to_numeric(df_bbg["Gross Spread %"], errors="coerce")
df_bbg["bbg_retail_sub_ratio"] = pd.to_numeric(df_bbg["Retail Subscription Ratio"], errors="coerce")
df_bbg["bbg_ir_close_pct"] = pd.to_numeric(df_bbg["Offer To 1st Close"], errors="coerce")
df_bbg["bbg_ir_open_pct"] = pd.to_numeric(df_bbg["Offer To 1st Open"], errors="coerce")
df_bbg["bbg_bhr_1m_pct"] = pd.to_numeric(df_bbg["Offer To Month 1"], errors="coerce")
df_bbg["bbg_bhr_3m_pct"] = pd.to_numeric(df_bbg["Offer To Month 3"], errors="coerce")
df_bbg["bbg_bhr_6m_pct"] = pd.to_numeric(df_bbg["Offer To 1st 6 Months"], errors="coerce")
df_bbg["bbg_bhr_1y_pct"] = pd.to_numeric(df_bbg["Offer To 1st Year"], errors="coerce")
df_bbg["bbg_pricing_date"] = pd.to_datetime(df_bbg["Pricing Date"], errors="coerce")
df_bbg["bbg_announced_date"] = pd.to_datetime(df_bbg["Announced Date"], errors="coerce")
df_bbg["bbg_trade_date"] = pd.to_datetime(df_bbg["Trade Date (US)"], errors="coerce")

print("Bloomberg Return Coverage Summary:")
print("  Offer to 1st Close valid:", df_bbg["bbg_ir_close_pct"].notna().sum())
print("  Offer to 1st Open valid :", df_bbg["bbg_ir_open_pct"].notna().sum())
print("  Gross Spread % valid    :", df_bbg["bbg_gross_spread_pct"].notna().sum())
print("  Offer to 1M valid       :", df_bbg["bbg_bhr_1m_pct"].notna().sum())
print("  Offer to 3M valid       :", df_bbg["bbg_bhr_3m_pct"].notna().sum())
print("  Offer to 6M valid       :", df_bbg["bbg_bhr_6m_pct"].notna().sum())
print("  Offer to 1Y valid       :", df_bbg["bbg_bhr_1y_pct"].notna().sum())

# Save combined Bloomberg file
bbg_out_path = os.path.join(OUT_DIR, "bloomberg_ecdr_merged_1994_2026.csv")
df_bbg.to_csv(bbg_out_path, index=False)
print(f"Saved merged Bloomberg ECDR file to: {bbg_out_path}")

print("\n=================================================================")
print("STEP 2: ALIGNING WITH OFFICIAL HKEX MASTER SAMPLE (N=2,865)")
print("=================================================================")

master_path = os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv")
df_master = pd.read_csv(master_path)
print(f"Loaded Master Sample: {df_master.shape}")

def master_code_to_ticker(c):
    if pd.isna(c): return ""
    try:
        val = int(float(c))
        return f"{val} HK"
    except:
        return str(c).strip()

df_master["bbg_ticker_std"] = df_master["raw_code"].apply(master_code_to_ticker)

def clean_name(n):
    if pd.isna(n): return ""
    s = str(n).upper()
    for w in ["LIMITED", "LTD", "HOLDINGS", "GROUP", "CO", "CORP", "CORPORATION", "INTERNATIONAL", "COMPANY", "INC", "H SHARES", "- H SHARES", "THE"]:
        s = re.sub(r"\b" + w + r"\b", "", s)
    return re.sub(r"[^A-Z0-9]", "", s)

df_master["clean_name"] = df_master["company_name"].apply(clean_name)
df_bbg["clean_name"] = df_bbg["Issuer Name"].apply(clean_name)

# Primary match on standard ticker
merged_master = pd.merge(df_master, df_bbg, left_on="bbg_ticker_std", right_on="bbg_ticker", how="left", suffixes=("", "_bbg_dup"))
direct_matched = merged_master["bbg_ir_close_pct"].notna().sum()
print(f"Direct Standard Ticker Matches: {direct_matched} / {len(df_master)} ({direct_matched/len(df_master)*100:.1f}%)")

unmatched_mask = merged_master["bbg_ir_close_pct"].isna()
unmatched_indices = merged_master[unmatched_mask].index

print(f"Attempting secondary company-name matching for {len(unmatched_indices)} unaligned deals...")

bbg_name_dict = df_bbg[df_bbg["clean_name"] != ""].drop_duplicates(subset=["clean_name"]).set_index("clean_name")

cols_to_fill = [c for c in df_bbg.columns if c not in ["clean_name"]]

recovered = 0
for idx in unmatched_indices:
    cname = merged_master.loc[idx, "clean_name"]
    if cname in bbg_name_dict.index:
        bbg_row = bbg_name_dict.loc[cname]
        for col in cols_to_fill:
            if col in merged_master.columns:
                merged_master.loc[idx, col] = bbg_row[col]
        recovered += 1

print(f"Recovered through clean company name alignment: {recovered}")
total_aligned = merged_master["bbg_ir_close_pct"].notna().sum()
print(f"Total Master Alignment: {total_aligned} / {len(df_master)} ({total_aligned/len(df_master)*100:.1f}%)")

# Overwrite / patch the master columns with Bloomberg raw unadjusted returns
merged_master["ir_close_bbg_clean"] = merged_master["bbg_ir_close_pct"]
merged_master["ir_open_bbg_clean"] = merged_master["bbg_ir_open_pct"]
merged_master["gross_spread_bbg"] = merged_master["bbg_gross_spread_pct"]
merged_master["sub_ratio_bbg"] = merged_master["bbg_retail_sub_ratio"]
merged_master["bhr_1m_bbg"] = merged_master["bbg_bhr_1m_pct"]
merged_master["bhr_3m_bbg"] = merged_master["bbg_bhr_3m_pct"]
merged_master["bhr_6m_bbg"] = merged_master["bbg_bhr_6m_pct"]
merged_master["bhr_1y_bbg"] = merged_master["bbg_bhr_1y_pct"]

aligned_master_path = os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_aligned_bloomberg.csv")
merged_master.to_csv(aligned_master_path, index=False)
print(f"\nSaved aligned master dataset to: {aligned_master_path}")

print("\n=================================================================")
print("STEP 3: QUANTIFYING PITFALL 1 (REVERSE SPLITS DISTORTION)")
print("=================================================================")
# Compare old naive Yahoo/EOD-adjusted returns with Bloomberg unadjusted returns
has_both = merged_master[merged_master["ir_close"].notna() & merged_master["ir_close_bbg_clean"].notna()].copy()
print(f"Deals with both Naive Return and Clean Bloomberg Return: N = {len(has_both)}")

has_both["diff"] = (has_both["ir_close"] * 100) - has_both["ir_close_bbg_clean"]
severe_distortions = has_both[has_both["diff"].abs() > 50]
print(f"Severe Distortions (> 50 percentage points gap): {len(severe_distortions)} deals!")

print("\nTop 5 Extreme Reverse-Split Distortions (Naive vs Bloomberg Truth):")
for _, r in severe_distortions.sort_values(by="diff", ascending=False).head(5).iterrows():
    print(f"  {r['stock_code']} ({r['company_name']}): Naive = {r['ir_close']*100:+.1f}% | Bloomberg Truth = {r['ir_close_bbg_clean']:+.1f}% | Distortion = {r['diff']:+.1f} pp")

print("\nSummary by Epoch: Naive vs Clean Mean IR")
has_both["naive_pct"] = has_both["ir_close"] * 100
epoch_comp = has_both.groupby("epoch").agg(
    N=("naive_pct", "size"),
    Naive_Mean_IR=("naive_pct", "mean"),
    Clean_BBG_Mean_IR=("ir_close_bbg_clean", "mean"),
    Naive_Median_IR=("naive_pct", "median"),
    Clean_BBG_Median_IR=("ir_close_bbg_clean", "median")
)
print(epoch_comp.round(2).to_string())
