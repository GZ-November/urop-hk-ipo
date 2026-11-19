import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
m = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/pipeline/exports/HKIPO-MB-MASTER_clean.csv", low_memory=False)
t4 = pd.read_csv(os.path.join(OUT_DIR, "table4_2026_all113_retail_ballot_returns.csv"))

# Parse listing month for clustering
m["listing_dt"] = pd.to_datetime(m["Date of Listing (dd/mm/yy)"], errors="coerce")
m["listing_ym"] = m["listing_dt"].dt.to_period("M").astype(str)

for c in m.columns:
    if c not in [
        "cohort", "Stock Code", "Company Name at time of listing", "Date of Prospectus (dd/mm/yy)",
        "Date of Listing (dd/mm/yy)", "Sponsor(s)", "Reporting Accountants", "Valuer(s)",
        "currency in financial information", "Principal business / industry",
        "Listing route / applicable chapter", "Ultimate controller type", "Place of incorporation",
        "Principal place of business", "Offer mechanism", "Applicable IPO rules / transition basis",
        "Lead sponsor name", "listing_dt", "listing_ym"
    ]:
        m[c] = pd.to_numeric(m[c], errors="coerce")

m["gross_proceeds_hkd"] = m["Funds Raised HK (a)"].fillna(0) + m["Funds Raised Int.(b)"].fillna(0)
mask_zero = m["gross_proceeds_hkd"] <= 0
m.loc[mask_zero, "gross_proceeds_hkd"] = m.loc[mask_zero, "IPO Subscription Price (HK$)"] * m.loc[mask_zero, "Global Offering (without option)"]
m["proceeds_hkd_m"] = m["gross_proceeds_hkd"] / 1e6
m["log_proceeds"] = np.log(m["proceeds_hkd_m"])
m["log_age"] = np.log1p(m["Firm age at IPO (years)"])
m["ir_raw"] = m["First-day return / Underpricing (%)"]
m["ir_pct"] = m["ir_raw"] * 100
m["log_ir"] = np.log1p(m["ir_raw"])
m["hsi_20d_pct"] = m["HSI return over 20 trading days before prospectus (%)"] * 100
m["hibor_1m"] = m["1-month HIBOR before prospectus (%)"]
m["ipo_wave_90d"] = m["HK ordinary IPO count in 90 calendar days before prospectus"]
m["is_ah"] = m["A+H issuer flag"].fillna(0)
m["is_18a"] = m["Chapter 18A flag"].fillna(0)
m["is_18c"] = m["Chapter 18C flag"].fillna(0)
m["is_vc_pe"] = m["Pre-IPO VC/PE backing (1=yes; 0=no)"].fillna(0)
m["cornerstone_pct"] = m["Final cornerstone allocation (% of base offer)"].fillna(0) * 100
m["free_float_pct"] = m["Unrestricted public shareholding at listing (%)"].fillna(0) * 100
m["public_final_pct"] = m["public_offer_fraction"].fillna(0) * 100
m["post_aug2025"] = (m["listing_dt"] >= pd.Timestamp("2025-08-04")).astype(int)
m["log_sub"] = np.log1p(m["Subscription Ratio (times)"])

# Pricing mechanism indicators
def get_price_type(r):
    plo, phi, p0 = r["Minimum Offer Price"], r["Maximum Offer Price"], r["IPO Subscription Price (HK$)"]
    if pd.isna(plo) or pd.isna(phi) or plo == phi:
        return "Fixed"
    pos = (p0 - plo) / (phi - plo) if phi > plo else 0
    if np.isclose(pos, 1.0, atol=1e-2):
        return "Cap"
    elif np.isclose(pos, 0.0, atol=1e-2):
        return "Bottom"
    return "Inside"

m["p_type"] = m.apply(get_price_type, axis=1)
m["is_fixed_price"] = (m["p_type"] == "Fixed").astype(int)
m["is_priced_at_cap"] = (m["p_type"] == "Cap").astype(int)
m["is_priced_at_bottom"] = (m["p_type"] == "Bottom").astype(int)

print("=================================================================")
print("4. MULTIVARIATE OLS REGRESSIONS OF LOG INITIAL RETURN log(1 + IR)")
print("=================================================================")
reg_vars = [
    "log_ir", "ir_pct", "log_proceeds", "log_age", "hsi_20d_pct", "hibor_1m",
    "is_ah", "is_18a", "is_18c", "is_vc_pe", "is_fixed_price", "is_priced_at_cap",
    "cornerstone_pct", "free_float_pct", "post_aug2025", "log_sub", "listing_ym"
]
est = m.dropna(subset=reg_vars).copy()
print(f"Common complete-case estimation sample: N = {len(est)}, Listing-month clusters G = {est['listing_ym'].nunique()}")

formulas = {
    "M1_Baseline": "log_ir ~ log_proceeds + log_age + is_ah + is_18a + is_18c + is_vc_pe + hsi_20d_pct + hibor_1m",
    "M2_Pricing": "log_ir ~ log_proceeds + log_age + is_ah + is_18a + is_18c + is_vc_pe + hsi_20d_pct + hibor_1m + is_fixed_price + is_priced_at_cap",
    "M3_Float_Reform": "log_ir ~ log_proceeds + log_age + is_ah + is_18a + is_18c + is_vc_pe + hsi_20d_pct + hibor_1m + is_fixed_price + is_priced_at_cap + cornerstone_pct + free_float_pct + post_aug2025",
    "M4_Full_Demand": "log_ir ~ log_proceeds + log_age + is_ah + is_18a + is_18c + is_vc_pe + hsi_20d_pct + hibor_1m + is_fixed_price + is_priced_at_cap + cornerstone_pct + free_float_pct + post_aug2025 + log_sub",
}

for name, fml in formulas.items():
    fit_hc3 = smf.ols(fml, data=est).fit(cov_type="HC3")
    fit_cl = smf.ols(fml, data=est).fit(cov_type="cluster", cov_kwds={"groups": est["listing_ym"]})
    print(f"\n--- {name} (N={int(fit_hc3.nobs)}, R2={fit_hc3.rsquared:.3f}, Adj_R2={fit_hc3.rsquared_adj:.3f}) ---")
    for k in fit_hc3.params.index:
        print(f"  {k:20s}: coef={fit_hc3.params[k]:+.4f} | t_HC3={fit_hc3.tvalues[k]:+.2f} (p={fit_hc3.pvalues[k]:.3f}) | t_Cluster={fit_cl.tvalues[k]:+.2f} (p={fit_cl.pvalues[k]:.3f})")

print("\n=================================================================")
print("5. WINNER'S CURSE BY OVERSUBSCRIPTION QUINTILES (N=113 BALLOTS)")
print("=================================================================")
# Merge subscription ratio into t4 if not already there
df226 = pd.read_csv(os.path.join(OUT_DIR, "hkipo_2025Q1_2026Q3_complete_226.csv"))
sub_map = df226.set_index("Stock Code")["Subscription Ratio (times)"].to_dict()
t4["sub_x"] = t4["code"].map(sub_map)
t4["sub_q"] = pd.qcut(t4["sub_x"], 5, labels=["Q1 (Lowest Sub)", "Q2", "Q3", "Q4", "Q5 (Highest Sub)"])
wc_tab = t4.groupby("sub_q", observed=False).agg(
    N=("code", "size"),
    Sub_Range=("sub_x", lambda s: f"{s.min():.0f}x-{s.max():.0f}x"),
    Median_Sub_x=("sub_x", "median"),
    Mean_Headline_IR_Pct=("ir_pct", "mean"),
    Median_Headline_IR_Pct=("ir_pct", "median"),
    Mean_1Lot_Prob_Pct=("alloc_rate_1lot_pct", "mean"),
    Median_1Lot_Prob_Pct=("alloc_rate_1lot_pct", "median"),
    Mean_1Lot_CapRet_Pct=("cap_ret_1lot_pct", "mean"),
    Median_1Lot_CapRet_Pct=("cap_ret_1lot_pct", "median"),
    Mean_10Lot_CapRet_Pct=("cap_ret_10lot_pct", "mean"),
    Mean_PoolB_CapRet_Pct=("cap_ret_poolB_min_pct", "mean"),
).round(2)
print(wc_tab.to_string())

# Paired tests between Headline IR and 1-Lot / Pool-B Net Return
diff_1lot = t4["ir_pct"] - t4["cap_ret_1lot_pct"]
t_stat, p_val = stats.ttest_rel(t4["ir_pct"], t4["cap_ret_1lot_pct"])
w_stat, w_pval = stats.wilcoxon(t4["ir_pct"], t4["cap_ret_1lot_pct"])
print(f"\nPaired Test (Headline IR vs 1-Lot Capital Return, N={len(t4)}): Mean Diff = {diff_1lot.mean():+.2f}%, Paired t = {t_stat:.2f} (p = {p_val:.4e}), Wilcoxon p = {w_pval:.4e}")

print("\n=================================================================")
print("6. AFTERMARKET STABILIZATION (+30D), LIQUIDITY DECAY & +180D UNLOCK")
print("=================================================================")
m["stab_buy"] = m["Stabilization purchases occurred"].fillna(0)
m["full_greenshoe"] = (m["Over-allotment exercise percentage (%)"].fillna(0) >= 0.99).astype(int)

def stab_group(r):
    if r["full_greenshoe"] == 1:
        return "1. Full Greenshoe Exercised (Hot Debut)"
    if r["stab_buy"] == 1:
        return "2. Stabilization Purchases Executed (Price Support)"
    return "3. No Stabilization / Partial or Zero Greenshoe"

m["stab_regime"] = m.apply(stab_group, axis=1)
stab_tab = m.groupby("stab_regime").agg(
    N=("Stock Code", "size"),
    Mean_Day1_IR_Pct=("ir_pct", "mean"),
    Median_Day1_IR_Pct=("ir_pct", "median"),
    Zero_IR_Share_Pct=("ir_pct", lambda s: (s.abs() < 0.05).mean()*100),
    Break_Rate_Pct=("ir_pct", lambda s: (s < 0).mean()*100),
    Mean_Day1_Flipping_Pct=("First-day flipping ratio (%)", lambda s: s.dropna().mean()*100),
    Mean_PostStab_Cliff_5d_Pct=("Post-stabilization cliff return [-5, +5] (%)", lambda s: s.dropna().mean()*100),
    Mean_PostStab_20d_Pct=("Post-stabilization 20-day return [0, +20] (%)", lambda s: s.dropna().mean()*100),
    Mean_1M_BHR_Pct=("1-month BHR from Day-1 close (%)", lambda s: s.dropna().mean()*100),
    Mean_6M_BHR_Pct=("6-month BHR from Day-1 close (%)", lambda s: s.dropna().mean()*100),
).round(2)
print("Aftermarket Stabilization Regimes:")
print(stab_tab.to_string())

# Cornerstone Unlock Event Study (Day +180)
unlock_df = m.dropna(subset=["Cornerstone unlock CAR [-5, +5] (%)"]).copy()
unlock_df["car5"] = unlock_df["Cornerstone unlock CAR [-5, +5] (%)"] * 100
unlock_df["car20"] = unlock_df["Cornerstone unlock CAR [-20, +20] (%)"] * 100
unlock_df["vol_shock"] = unlock_df["Cornerstone unlock volume shock ratio"]
unlock_df["high_cs"] = (unlock_df["cornerstone_pct"] >= unlock_df["cornerstone_pct"].median()).map({True: "High Cornerstone (>=Median)", False: "Low Cornerstone (<Median)"})
print(f"\nCornerstone Lockup Expiry (+180d) Event Study (Matured Cohort N = {len(unlock_df)}):")
for lbl, g in unlock_df.groupby("high_cs"):
    t5, p5 = stats.ttest_1samp(g["car5"].dropna(), 0)
    t20, p20 = stats.ttest_1samp(g["car20"].dropna(), 0)
    print(f"  {lbl} (N={len(g)}): CAR[-5,+5] Mean={g['car5'].mean():+.2f}% (Med={g['car5'].median():+.2f}%, t={t5:+.2f}, p={p5:.3f}) | CAR[-20,+20] Mean={g['car20'].mean():+.2f}% (t={t20:+.2f}, p={p20:.3f}) | Vol Shock={g['vol_shock'].mean():.2f}x")
t5_all, p5_all = stats.ttest_1samp(unlock_df["car5"].dropna(), 0)
t20_all, p20_all = stats.ttest_1samp(unlock_df["car20"].dropna(), 0)
print(f"  All Matured Unlock IPOs (N={len(unlock_df)}): CAR[-5,+5]={unlock_df['car5'].mean():+.2f}% (t={t5_all:+.2f}, p={p5_all:.3f}) | CAR[-20,+20]={unlock_df['car20'].mean():+.2f}% (t={t20_all:+.2f}, p={p20_all:.3f}) | Vol Shock={unlock_df['vol_shock'].mean():.2f}x (Med={unlock_df['vol_shock'].median():.2f}x)")

# Liquidity decay from Day 1 to 6M
liq = m["Liquidity decay ratio (6M vs Day-1 turnover)"].dropna()
print(f"\nLiquidity Decay Ratio (6M Avg Daily Turnover / Day-1 Turnover, N={len(liq)}): Mean = {liq.mean()*100:.2f}%, Median = {liq.median()*100:.2f}%")
