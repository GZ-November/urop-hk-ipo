import os
import pandas as pd

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
df = pd.read_csv(os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_aligned_bloomberg.csv"))

print("=================================================================")
print("TABLE 4: METHODOLOGICAL PITFALLS QUANTIFICATION (1994-2026)")
print("=================================================================")

# 1. Reverse split distortion
df["naive_ir"] = df["ir_close"] * 100
df["clean_ir"] = df["ir_close_bbg_clean"]

print("\n--- Panel A: Naive Return vs Bloomberg Clean Unadjusted Return ---")
for ep, g in df.groupby("epoch"):
    n_tot = len(g)
    n_clean = g["clean_ir"].notna().sum()
    n_naive = g["naive_ir"].notna().sum()
    mean_clean = g["clean_ir"].mean()
    med_clean = g["clean_ir"].median()
    mean_naive = g["naive_ir"].mean()
    med_naive = g["naive_ir"].median()
    severe = (g["naive_ir"] - g["clean_ir"]).abs() > 50
    print(f"{ep}: Total N={n_tot} | Clean N={n_clean} | Clean Mean={mean_clean:.2f}% (Med={med_clean:.2f}%) | Naive Mean={mean_naive:.2f}% | Severe Distortions={severe.sum()}")

print("\n--- Panel B: Long-Run Returns by Epoch (Bloomberg Clean BHR) ---")
longrun_tab = df.groupby("epoch").agg(
    N=("bbg_bhr_1m_pct", "count"),
    Mean_1M=("bbg_bhr_1m_pct", "mean"),
    Med_1M=("bbg_bhr_1m_pct", "median"),
    Mean_3M=("bbg_bhr_3m_pct", "mean"),
    Med_3M=("bbg_bhr_3m_pct", "median"),
    Mean_6M=("bbg_bhr_6m_pct", "mean"),
    Med_6M=("bbg_bhr_6m_pct", "median"),
    Mean_1Y=("bbg_bhr_1y_pct", "mean"),
    Med_1Y=("bbg_bhr_1y_pct", "median")
)
print(longrun_tab.round(2).to_string())

# Save clean summary
longrun_tab.to_csv(os.path.join(OUT_DIR, "table_longrun_bhr_clean_1994_2026.csv"))
