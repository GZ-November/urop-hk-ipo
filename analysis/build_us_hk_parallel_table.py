import os
import pandas as pd
import numpy as np

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
hk_df = pd.read_csv(os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv"), low_memory=False)
ann_df = pd.read_csv(os.path.join(OUT_DIR, "table1_annual_1994_2026.csv"))

# US IPO Annual Series:
# 1994-2016: Exact figures from Lowry, Michaely & Volkova (2017, Table 3.1, pp. 173-174)
# 2017-2025: Jay Ritter "Initial Public Offerings: Updated Statistics" (operating companies, offer price >= $5, excl. ADRs/SPACs/REITs/CEFs)
us_data = {
    1994: (443, 9.0, 23.22, "Lowry et al. (2017) Table 3.1"),
    1995: (495, 21.0, 36.79, "Lowry et al. (2017) Table 3.1"),
    1996: (723, 17.0, 57.19, "Lowry et al. (2017) Table 3.1"),
    1997: (493, 14.0, 38.94, "Lowry et al. (2017) Table 3.1"),
    1998: (316, 20.0, 41.70, "Lowry et al. (2017) Table 3.1"),
    1999: (480, 71.0, 74.90, "Lowry et al. (2017) Table 3.1"),
    2000: (377, 56.0, 74.74, "Lowry et al. (2017) Table 3.1"),
    2001: (80, 13.0, 42.90, "Lowry et al. (2017) Table 3.1"),
    2002: (73, 8.0, 28.20, "Lowry et al. (2017) Table 3.1"),
    2003: (69, 12.0, 13.01, "Lowry et al. (2017) Table 3.1"),
    2004: (178, 13.0, 38.80, "Lowry et al. (2017) Table 3.1"),
    2005: (167, 10.0, 34.54, "Lowry et al. (2017) Table 3.1"),
    2006: (152, 13.0, 32.34, "Lowry et al. (2017) Table 3.1"),
    2007: (154, 14.0, 34.07, "Lowry et al. (2017) Table 3.1"),
    2008: (23, 4.0, 25.66, "Lowry et al. (2017) Table 3.1"),
    2009: (43, 12.0, 13.73, "Lowry et al. (2017) Table 3.1"),
    2010: (104, 9.0, 34.84, "Lowry et al. (2017) Table 3.1"),
    2011: (87, 14.0, 28.42, "Lowry et al. (2017) Table 3.1"),
    2012: (104, 19.0, 34.42, "Lowry et al. (2017) Table 3.1"),
    2013: (175, 20.0, 41.26, "Lowry et al. (2017) Table 3.1"),
    2014: (220, 16.0, 47.34, "Lowry et al. (2017) Table 3.1"),
    2015: (126, 20.0, 21.64, "Lowry et al. (2017) Table 3.1"),
    2016: (57, 10.0, 10.54, "Lowry et al. (2017) Table 3.1"),
    2017: (107, 13.0, 23.03, "Ritter Table 1 (Updated July 2026)"),
    2018: (134, 18.5, 33.47, "Ritter Table 1 (Updated July 2026)"),
    2019: (113, 23.5, 39.28, "Ritter Table 1 (Updated July 2026)"),
    2020: (165, 41.6, 61.86, "Ritter Table 1 (Updated July 2026; PW=47.9%)"),
    2021: (311, 32.1, 119.36, "Ritter Table 1 (Updated July 2026)"),
    2022: (38, 48.9, 6.99, "Ritter Table 1 (Updated July 2026)"),
    2023: (54, 11.9, 11.92, "Ritter Table 1 (Updated July 2026)"),
    2024: (73, 15.3, 20.90, "Ritter Table 1 (Updated July 2026)"),
    2025: (90, 29.3, 38.97, "Ritter Table 1 (Updated July 2026)"),
    2026: (np.nan, np.nan, np.nan, "Pending Ritter update (thru Sep 2026)"),
}

# Compute proceeds-weighted IR and split-screened IR for HK Main Board each year
mb = hk_df[hk_df["board"] == "Main Board"].copy()
# Flag split-adjusted suspects (fractional non-tick d1_close >= 1.0 or |IR| > 3.0)
def is_split_suspect(r):
    d1 = r.get("d1_close")
    ir = r.get("ir_close")
    if pd.isna(d1) or pd.isna(ir):
        return False
    rem = round(abs(d1 * 100 - round(d1 * 100)), 4)
    return (d1 >= 1.0 and rem > 0.01) or (abs(ir) > 3.0)

mb["split_suspect"] = mb.apply(is_split_suspect, axis=1)

rows = []
for _, r in ann_df.iterrows():
    yr = int(r["Year"])
    sub = mb[mb["cohort_year"] == yr]
    sub_valid = sub.dropna(subset=["ir_close", "funds_raised_total_hkd"])
    pw_ir = (
        (sub_valid["ir_close"] * sub_valid["funds_raised_total_hkd"]).sum()
        / sub_valid["funds_raised_total_hkd"].sum() * 100
        if len(sub_valid) and sub_valid["funds_raised_total_hkd"].sum() > 0 else np.nan
    )
    sub_clean = sub[~sub["split_suspect"]]["ir_close"].dropna() * 100
    clean_ew_ir = sub_clean.mean() if len(sub_clean) else np.nan

    us_n, us_ir, us_proc, us_src = us_data.get(yr, (np.nan, np.nan, np.nan, ""))
    hk_total_n = int(r["MB_Ordinary_IPOs"]) + int(r["GEM_Ordinary_IPOs"])
    hk_total_usd_bn = (float(r["MB_Proceeds_HKD_bn"]) + float(r["GEM_Proceeds_HKD_bn"])) / 7.80

    rows.append({
        "Year": yr,
        "HK_Total_IPOs": hk_total_n,
        "HK_MB_IPOs": int(r["MB_Ordinary_IPOs"]),
        "HK_GEM_IPOs": int(r["GEM_Ordinary_IPOs"]),
        "HK_Total_Proceeds_HKD_bn": round(float(r["MB_Proceeds_HKD_bn"]) + float(r["GEM_Proceeds_HKD_bn"]), 2),
        "HK_Total_Proceeds_USD_bn": round(hk_total_usd_bn, 2),
        "HK_MB_Naive_EW_IR_Pct": round(float(r["MB_Mean_IR_Pct"]), 2),
        "HK_MB_Screened_EW_IR_Pct": round(clean_ew_ir, 2) if pd.notna(clean_ew_ir) else np.nan,
        "HK_MB_PW_IR_Pct": round(pw_ir, 2) if pd.notna(pw_ir) else np.nan,
        "HK_MB_Median_IR_Pct": round(float(r["MB_Median_IR_Pct"]), 2),
        "HK_MB_Break_Rate_Pct": round(float(r["MB_Break_Rate_Pct"]), 1),
        "US_IPOs": int(us_n) if pd.notna(us_n) else np.nan,
        "US_EW_IR_Pct": us_ir,
        "US_Proceeds_USD_bn": round(us_proc, 2) if pd.notna(us_proc) else np.nan,
        "US_Source": us_src,
    })

out = pd.DataFrame(rows)
out.to_csv(os.path.join(OUT_DIR, "table_us_hk_parallel_1994_2026.csv"), index=False)
print("Saved table_us_hk_parallel_1994_2026.csv")
print(out.to_string(index=False))
