import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
m2865 = pd.read_csv(os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv"), low_memory=False)

print("=================================================================")
print("7. DIFFERENCE-IN-DIFFERENCES: GEM PLACING-ONLY ABOLITION (2011-2022)")
print("=================================================================")
# Window: 2013-2016 (Pre-Intervention Placing-Only Boom) vs 2018-2021 (Post-Feb 2018 GEM Reform)
sub = m2865[m2865["cohort_year"].between(2013, 2021) & (m2865["cohort_year"] != 2017)].copy()
sub = sub.dropna(subset=["ir_close"]).copy()
sub["ir_pct"] = sub["ir_close"] * 100
sub["log_ir"] = np.log1p(sub["ir_close"].clip(lower=-0.95))
sub["is_gem"] = (sub["board"] == "GEM").astype(int)
sub["post_2018"] = (sub["cohort_year"] >= 2018).astype(int)
sub["gem_x_post"] = sub["is_gem"] * sub["post_2018"]
sub["log_funds"] = np.log(sub["funds_raised_total_hkd"].clip(lower=1e5))

did_raw = smf.ols("ir_pct ~ is_gem + post_2018 + gem_x_post", data=sub).fit(cov_type="HC3")
did_log = smf.ols("log_ir ~ is_gem + post_2018 + gem_x_post + log_funds", data=sub).fit(cov_type="HC3")

print(f"DiD Sample (2013-2016 vs 2018-2021, excl. 2017 transition): N = {len(sub)}")
print("--- DiD Model 1: Raw Initial Return (%) ---")
for k in did_raw.params.index:
    print(f"  {k:15s}: coef={did_raw.params[k]:+8.2f}% | se={did_raw.bse[k]:6.2f} | t={did_raw.tvalues[k]:+6.2f} | p={did_raw.pvalues[k]:.4e}")
print(f"  R2 = {did_raw.rsquared:.3f}")

print("\n--- DiD Model 2: Log Initial Return log(1+IR) controlling for log(Proceeds) ---")
for k in did_log.params.index:
    print(f"  {k:15s}: coef={did_log.params[k]:+8.4f}  | se={did_log.bse[k]:6.4f} | t={did_log.tvalues[k]:+6.2f} | p={did_log.pvalues[k]:.4e}")
print(f"  R2 = {did_log.rsquared:.3f}")

print("\n=================================================================")
print("8. SHELL FACTORY BUNCHING AT MINIMUM PROCEEDS / CAP FLOORS (1994-2026)")
print("=================================================================")
# At 25% public float:
# Pre-May 2018 Main Board min market cap = HK$200m -> 25% offer size = HK$50m (bunching window: HK$40m-100m)
# Post-May 2018 Main Board min market cap = HK$500m -> 25% offer size = HK$125m (bunching window: HK$110m-160m)
mb = m2865[m2865["board"] == "Main Board"].copy()
mb["proceeds_m"] = mb["funds_raised_total_hkd"] / 1e6
mb["small_shell_50_100m"] = mb["proceeds_m"].between(40, 100).astype(int)
mb["bunch_110_160m"] = mb["proceeds_m"].between(110, 160).astype(int)
mb["micro_under_150m"] = (mb["proceeds_m"] <= 150).astype(int)

periods = [
    ("1994-2004 (Epoch II)", (1994, 2004)),
    ("2005-2012 (Early Epoch III: SOE Mega-Banks)", (2005, 2012)),
    ("2013-2017 (Late Epoch III: Shell Factory Peak)", (2013, 2017)),
    ("2018-2020 (Post-HK$500m Cap Hike & 125m Floor)", (2018, 2020)),
    ("2021-2026 (Post-HK$80m Profit Hike & H-Share Era)", (2021, 2026)),
]
shell_rows = []
for lbl, (y1, y2) in periods:
    g = mb[mb["cohort_year"].between(y1, y2)]
    shell_rows.append({
        "Period": lbl,
        "MB_IPOs_N": len(g),
        "Median_Proceeds_M": round(g["proceeds_m"].median(), 1),
        "Share_HK40m_100m_Pct (Old HK$200m Cap Shell Zone)": round(g["small_shell_50_100m"].mean()*100, 1),
        "Share_HK110m_160m_Pct (New HK$500m Cap Zone)": round(g["bunch_110_160m"].mean()*100, 1),
        "Share_Under_HK150m_Pct": round(g["micro_under_150m"].mean()*100, 1),
        "PRC_H_Share_Pct": round(g["is_prc_joint_stock"].mean()*100, 1),
    })
print(pd.DataFrame(shell_rows).to_string(index=False))

print("\n=================================================================")
print("9. FINI SETTLEMENT REFORM STRUCTURAL BREAK IN PROSPECTUS-TO-LISTING LAG")
print("=================================================================")
# Compare prospectus_to_listing_days before vs after FINI (2023-11-22)
m2865["listing_dt"] = pd.to_datetime(m2865["listing_date"], errors="coerce")
mb_recent = m2865[(m2865["board"] == "Main Board") & (m2865["cohort_year"] >= 2018)].dropna(subset=["prospectus_to_listing_days", "listing_dt"]).copy()
mb_recent["post_fini"] = (mb_recent["listing_dt"] >= pd.Timestamp("2023-11-22")).astype(int)
pre_lag = mb_recent[mb_recent["post_fini"] == 0]["prospectus_to_listing_days"]
post_lag = mb_recent[mb_recent["post_fini"] == 1]["prospectus_to_listing_days"]
t_lag, p_lag = stats.ttest_ind(post_lag, pre_lag, equal_var=False)
u_lag, pu_lag = stats.mannwhitneyu(post_lag, pre_lag)
print(f"Pre-FINI (2018-2023.11, N={len(pre_lag)}): Mean = {pre_lag.mean():.2f} days, Median = {pre_lag.median():.1f} days, IQR = [{pre_lag.quantile(0.25):.1f}, {pre_lag.quantile(0.75):.1f}]")
print(f"Post-FINI (2023.11-2026, N={len(post_lag)}): Mean = {post_lag.mean():.2f} days, Median = {post_lag.median():.1f} days, IQR = [{post_lag.quantile(0.25):.1f}, {post_lag.quantile(0.75):.1f}]")
print(f"Difference: {post_lag.mean() - pre_lag.mean():+.2f} days | Welch t = {t_lag:.2f} (p = {p_lag:.4e}) | Mann-Whitney p = {pu_lag:.4e}")
