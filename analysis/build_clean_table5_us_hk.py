"""Build clean Table 5: 33-Year Parallel Comparison of HK (Main Board & GEM) vs. U.S. (Ritter Table 1)."""
import os
import numpy as np
import pandas as pd

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
hk = pd.read_csv(os.path.join(OUT_DIR, "clean_33y_hkipo_panel_1994_2026.csv"), low_memory=False)
us = pd.read_csv(os.path.join(OUT_DIR, "clean_us_ritter_annual_1994_2025.csv"))

hk["proceeds_hkd_m"] = hk["funds_raised_total_hkd"] / 1e6
mask_miss = hk["proceeds_hkd_m"].isna() | (hk["proceeds_hkd_m"] <= 0)
hk.loc[mask_miss, "proceeds_hkd_m"] = hk.loc[mask_miss, "bbg_offer_size_m"]
hk["proceeds_usd_bn"] = hk["proceeds_hkd_m"] / 7.80 / 1000.0

rows = []
for y in range(1994, 2027):
    mb = hk[(hk["cohort_year"] == y) & (hk["board"] == "Main Board")]
    gm = hk[(hk["cohort_year"] == y) & (hk["board"] == "GEM")]
    mb_ir = mb.dropna(subset=["ir_close_pct", "proceeds_hkd_m"])
    if len(mb_ir) > 0:
        w = np.maximum(mb_ir["proceeds_hkd_m"].values, 1e-3)
        vw_ir = np.sum(w * mb_ir["ir_close_pct"].values) / w.sum()
    else:
        vw_ir = np.nan

    us_row = us[us["year"] == y]
    rows.append({
        "Year": y,
        "HK_MB_N": len(mb),
        "HK_MB_Proceeds_USD_Bn": mb["proceeds_usd_bn"].sum(),
        "HK_MB_EW_IR_Pct": mb["ir_close_pct"].mean(),
        "HK_MB_VW_IR_Pct": vw_ir,
        "HK_MB_Med_IR_Pct": mb["ir_close_pct"].median(),
        "HK_GEM_N": len(gm),
        "HK_GEM_EW_IR_Pct": gm["ir_close_pct"].mean() if len(gm) > 0 else np.nan,
        "HK_GEM_Med_IR_Pct": gm["ir_close_pct"].median() if len(gm) > 0 else np.nan,
        "US_Ritter_N": int(us_row["ritter_table1_n_ipos"].iloc[0]) if len(us_row) > 0 else np.nan,
        "US_Proceeds_USD_Bn": float(us_row["ritter_table1_gross_proceeds_usd_bn"].iloc[0]) if len(us_row) > 0 else np.nan,
        "US_EW_IR_Pct": float(us_row["ritter_table1_mean_ir_ew_pct"].iloc[0]) if len(us_row) > 0 else np.nan,
        "US_VW_IR_Pct": float(us_row["ritter_table1_mean_ir_pw_pct"].iloc[0]) if len(us_row) > 0 else np.nan,
        "US_Med_IR_Pct": float(us_row["ritter_table1_median_ir_pct"].iloc[0]) if len(us_row) > 0 else np.nan,
    })

t5 = pd.DataFrame(rows)
t5.round(2).to_csv(os.path.join(OUT_DIR, "table5_us_hk_parallel_clean_1994_2026.csv"), index=False)
print("33-Year Parallel Summary (1994-2025 Comparable Full Years):")
c = t5[t5["Year"] <= 2025]
print(f"  HK Main Board Total IPOs (1994-2025): {c['HK_MB_N'].sum()} | Proceeds: US${c['HK_MB_Proceeds_USD_Bn'].sum():.2f}B | Mean Annual EW IR: {c['HK_MB_EW_IR_Pct'].mean():.2f}%")
print(f"  HK GEM Total IPOs (1999-2025)       : {c['HK_GEM_N'].sum()}")
print(f"  US Ritter Operating IPOs (1994-2025): {int(c['US_Ritter_N'].sum())} | Proceeds: US${c['US_Proceeds_USD_Bn'].sum():.2f}B | Mean Annual EW IR: {c['US_EW_IR_Pct'].mean():.2f}%")
print("\nPost-2000 'Listing Gap' Test (1994-2000 vs 2001-2025 Annual Average Listings):")
pre00 = c[c["Year"] <= 2000]
post00 = c[c["Year"] >= 2001]
print(f"  U.S. Annual Mean IPOs : {pre00['US_Ritter_N'].mean():.1f}/yr (1994-2000) -> {post00['US_Ritter_N'].mean():.1f}/yr (2001-2025) [{(post00['US_Ritter_N'].mean()/pre00['US_Ritter_N'].mean()-1)*100:+.1f}%]")
print(f"  HK MB Annual Mean IPOs: {pre00['HK_MB_N'].mean():.1f}/yr (1994-2000) -> {post00['HK_MB_N'].mean():.1f}/yr (2001-2025) [{(post00['HK_MB_N'].mean()/pre00['HK_MB_N'].mean()-1)*100:+.1f}%]")
print("\nRecent Years (2018-2026Q3):")
print(t5[t5["Year"] >= 2018].round(2).to_string(index=False))
