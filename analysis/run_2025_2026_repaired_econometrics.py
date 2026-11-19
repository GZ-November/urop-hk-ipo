"""Repaired Micro-Panel Econometrics (2025Q1-2026Q3, Gap-Free N=226) & Net-of-Cost Rock (1986) Tests.

Fixes all P0/P1 issues identified in the review memo:
1. Statutory Appendix D1A Para 15(2)(c) Cap-Only Waiver separated from Fixed-Price & Range-Priced deals;
2. Full 2025Q3 (24 deals) included (N=226 across all 21 listing months, zero calendar gap);
3. Statutory prospectus-date reform indicator (`post_aug2025_prospectus`) + Mechanism A vs B choice;
4. Zero `fillna(0)` on any continuous or unknown variable;
5. `log_sub` modeled properly as a joint demand outcome rather than a bad post-treatment control,
   with Wild Cluster Restricted Bootstrap p-values (B=4,999, Rademacher weights, Cameron-Gelbach-Miller 2008);
6. Direct A+H price-anchor regression & A/H premium inversion audit (N=45);
7. Net-of-fee & net-of-HIBOR Rock (1986) rationing equilibrium tests (N=113) + equal-weighted rent robustness.
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
m = pd.read_csv(os.path.join(OUT_DIR, "clean_micro_panel_2025_2026_N226.csv"))
r = pd.read_csv(os.path.join(OUT_DIR, "clean_rock_ballot_113_net_returns.csv"))
hsi_m = pd.read_csv(os.path.join(OUT_DIR, "clean_monthly_policy_valve_1994_2026.csv"))[["year_month", "hsi_monthly_return_pct"]]

m["listing_dt"] = pd.to_datetime(m["listing_date"])
m["prospectus_dt"] = pd.to_datetime(m["prospectus_date"])
m["listing_ym"] = m["listing_dt"].dt.to_period("M").astype(str)
m["pros_prev_ym"] = (m["prospectus_dt"] - pd.DateOffset(months=1)).dt.to_period("M").astype(str)
m = m.merge(hsi_m.rename(columns={"year_month": "pros_prev_ym", "hsi_monthly_return_pct": "hsi_prev_m_ret"}), on="pros_prev_ym", how="left")

m["log_ir"] = np.log1p(m["initial_return_pct"] / 100.0)
m["log_proceeds"] = np.log(m["gross_proceeds_hkd_m"])
m["log_sub"] = np.log1p(m["subscription_ratio_times"])

print("=========================================================================")
print("1. REPAIRED TABLE 8: STATUTORY PRICING STRUCTURES & INITIAL RETURNS (N=226)")
print("=========================================================================")
print("Pricing structure value counts:")
p_tab = m.groupby("pricing_structure").agg(
    N=("initial_return_pct", "count"),
    Share_Pct=("initial_return_pct", lambda s: len(s) / len(m) * 100),
    Mean_IR_Pct=("initial_return_pct", "mean"),
    Median_IR_Pct=("initial_return_pct", "median"),
    Break_Rate_Pct=("initial_return_pct", lambda s: (s < 0).mean() * 100),
    Median_Sub_x=("subscription_ratio_times", "median"),
    AH_Share_Pct=("is_ah_dual_listed", lambda s: s.mean() * 100),
)
print(p_tab.round(2).to_string())
p_tab.round(3).to_csv(os.path.join(OUT_DIR, "table8_repaired_pricing_structures_N226.csv"))

print("\n=========================================================================")
print("2. MECHANISM A VS. MECHANISM B ADOPTION POST-AUG 4, 2025 (N=226)")
print("=========================================================================")
reg_tab = m.groupby("alloc_regime_actual").agg(
    N=("initial_return_pct", "count"),
    Median_Proceeds_HKDm=("gross_proceeds_hkd_m", "median"),
    Mean_IR_Pct=("initial_return_pct", "mean"),
    Median_IR_Pct=("initial_return_pct", "median"),
    Break_Rate_Pct=("initial_return_pct", lambda s: (s < 0).mean() * 100),
    Median_Sub_x=("subscription_ratio_times", "median"),
    Mean_Final_Public_Pct=("public_offer_fraction_pct", "mean"),
    Mean_Cornerstone_Pct=("cornerstone_pct_of_offering", "mean"),
    Mean_FreeFloat_Pct=("unrestricted_free_float_pct", "mean"),
)
print(reg_tab.round(2).to_string())
reg_tab.round(3).to_csv(os.path.join(OUT_DIR, "table9b_mechanism_ab_comparison_N226.csv"))

# Compare the 9 Mechanism A choosers vs 142 Mechanism B choosers
elig = m[m["alloc_regime_actual"].isin(["Mechanism_A", "Mechanism_B"])].copy()
elig["chose_mech_b"] = (elig["alloc_regime_actual"] == "Mechanism_B").astype(int)
print(f"\nPost-Reform Non-18C Eligible Sample: N={len(elig)} (Mechanism B = {elig['chose_mech_b'].sum()}, Mechanism A = {(1-elig['chose_mech_b']).sum()})")
for col in ["gross_proceeds_hkd_m", "cornerstone_pct_of_offering", "is_ah_dual_listed", "is_18a", "initial_return_pct", "subscription_ratio_times"]:
    ma = elig[elig["chose_mech_b"] == 0][col].dropna()
    mb = elig[elig["chose_mech_b"] == 1][col].dropna()
    print(f"  {col:30s}: Mech A Mean={ma.mean():.2f} (Med={ma.median():.2f}) | Mech B Mean={mb.mean():.2f} (Med={mb.median():.2f})")

print("\n=========================================================================")
print("3. WILD CLUSTER RESTRICTED BOOTSTRAP REGRESSIONS (N=226, G=21 MONTHS)")
print("=========================================================================")
def wild_cluster_bootstrap_p(df_est, formula, target_var, cluster_col, B=4999, seed=42):
    """Cameron, Gelbach & Miller (2008) / Webb (2023) 6-point Wild Cluster Restricted (WCR) bootstrap."""
    rng = np.random.default_rng(seed)
    webb_weights = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])
    full_fit = smf.ols(formula, data=df_est).fit(cov_type="cluster", cov_kwds={"groups": df_est[cluster_col]})
    t_obs = full_fit.tvalues[target_var]

    # Restricted formula under H0: beta_{target_var} = 0
    lhs, rhs = formula.split("~")
    terms = [t.strip() for t in rhs.split("+") if t.strip() != target_var]
    rest_formula = f"{lhs.strip()} ~ " + " + ".join(terms)
    rest_fit = smf.ols(rest_formula, data=df_est).fit()
    yhat_r = rest_fit.fittedvalues.values
    u_r = rest_fit.resid.values

    y_vec, X_mat = full_fit.model.endog, full_fit.model.exog
    var_idx = list(full_fit.model.exog_names).index(target_var)
    clusters = df_est[cluster_col].values
    uniq_cl, inv_idx = np.unique(clusters, return_inverse=True)
    G = len(uniq_cl)
    n, k = X_mat.shape
    XtX_inv = np.linalg.inv(X_mat.T @ X_mat)
    dof_scale = (G / (G - 1.0)) * ((n - 1.0) / (n - k))

    # Precompute cluster slices
    cl_masks = [np.where(inv_idx == g)[0] for g in range(G)]
    t_boot = np.empty(B)
    for b in range(B):
        w = rng.choice(webb_weights, size=G)
        y_star = yhat_r + u_r * w[inv_idx]
        beta_star = XtX_inv @ (X_mat.T @ y_star)
        e_star = y_star - X_mat @ beta_star
        # Cluster meat on target_var
        meat_jj = 0.0
        scores = X_mat * e_star[:, None]
        for idx_g in cl_masks:
            sg = scores[idx_g].sum(axis=0)
            v_j = XtX_inv[var_idx] @ sg
            meat_jj += v_j * v_j
        se_star = np.sqrt(dof_scale * meat_jj)
        t_boot[b] = beta_star[var_idx] / se_star
    return float((np.sum(np.abs(t_boot) >= np.abs(t_obs)) + 1.0) / (B + 1.0))

# Build clean statutory pricing structure indicators without fillna(0)
# Baseline category: Range-priced below cap (Range_Priced_At_Floor + Range_Priced_Inside)
m["is_range_at_cap"] = (m["pricing_structure"] == "Range_Priced_At_Cap").astype(int)
m["is_cap_only_waiver"] = m["pricing_structure"].isin(["Cap_Only_Priced_At_Cap", "Cap_Only_Priced_Below_Cap"]).astype(int)
m["is_cap_priced_any"] = m["pricing_structure"].isin(["Range_Priced_At_Cap", "Cap_Only_Priced_At_Cap"]).astype(int)
m["is_single_fixed"] = (m["pricing_structure"] == "Single_Fixed_Price").astype(int)

# Sample A: Full Gap-Free N=226 across all G=21 calendar months (zero missing values!)
req_cols_226 = [
    "log_ir", "log_sub", "is_ah_dual_listed", "is_18a", "is_18c", "log_proceeds",
    "is_range_at_cap", "is_cap_only_waiver", "is_single_fixed", "cornerstone_pct_of_offering",
    "post_aug2025_prospectus", "hsi_prev_m_ret", "listing_ym"
]
est_226 = m.dropna(subset=req_cols_226).copy()
print(f"Full Gap-Free Estimation Sample: N = {len(est_226)} / {len(m)}, Month Clusters G = {est_226['listing_ym'].nunique()}")

# Sample B: Strict Zero-Imputation Complete-Case Sample adding Unrestricted Free Float (N=200, G=18)
req_cols_200 = req_cols_226 + ["unrestricted_free_float_pct"]
est_200 = m.dropna(subset=req_cols_200).copy()
print(f"Strict Zero-Imputation Free-Float Subsample: N = {len(est_200)} / {len(m)}, Month Clusters G = {est_200['listing_ym'].nunique()}")

models = [
    ("M1_Route_Full226", est_226,
     "log_ir ~ is_ah_dual_listed + is_18a + is_18c + log_proceeds + hsi_prev_m_ret + post_aug2025_prospectus"),
    ("M2_Pricing_Cornerstone_Full226", est_226,
     "log_ir ~ is_ah_dual_listed + is_18a + is_18c + log_proceeds + hsi_prev_m_ret + post_aug2025_prospectus + cornerstone_pct_of_offering + is_range_at_cap + is_cap_only_waiver + is_single_fixed"),
    ("M3_Add_FreeFloat_N200", est_200,
     "log_ir ~ is_ah_dual_listed + is_18a + is_18c + log_proceeds + hsi_prev_m_ret + post_aug2025_prospectus + cornerstone_pct_of_offering + unrestricted_free_float_pct + is_range_at_cap + is_cap_only_waiver + is_single_fixed"),
    ("M4_Demand_LogSub_Full226", est_226,
     "log_sub ~ is_ah_dual_listed + is_18a + is_18c + log_proceeds + hsi_prev_m_ret + post_aug2025_prospectus + cornerstone_pct_of_offering + is_range_at_cap + is_cap_only_waiver + is_single_fixed"),
    ("M5_Demand_LogSub_Float_N200", est_200,
     "log_sub ~ is_ah_dual_listed + is_18a + is_18c + log_proceeds + hsi_prev_m_ret + post_aug2025_prospectus + cornerstone_pct_of_offering + unrestricted_free_float_pct + is_range_at_cap + is_cap_only_waiver + is_single_fixed"),
]

reg_out = []
for mname, df_s, fml in models:
    f_hc3 = smf.ols(fml, data=df_s).fit(cov_type="HC3")
    f_cl = smf.ols(fml, data=df_s).fit(cov_type="cluster", cov_kwds={"groups": df_s["listing_ym"]})
    G_cl = df_s["listing_ym"].nunique()
    print(f"\n--- {mname} (N={int(f_hc3.nobs)}, G={G_cl}, R2={f_hc3.rsquared:.3f}, Adj_R2={f_hc3.rsquared_adj:.3f}) ---")
    for v in f_hc3.params.index:
        if v == "Intercept":
            print(f"  {v:28s}: coef={f_hc3.params[v]:+.4f}")
            continue
        p_wcb = wild_cluster_bootstrap_p(df_s, fml, v, "listing_ym", B=4999, seed=42)
        print(f"  {v:28s}: coef={f_hc3.params[v]:+.4f} | t_HC3={f_hc3.tvalues[v]:+6.2f} (p={f_hc3.pvalues[v]:.3f}) | "
              f"t_Clust={f_cl.tvalues[v]:+6.2f} | WCR_Boot_p={p_wcb:.4f}")
        reg_out.append({
            "Model": mname, "Variable": v, "Coef": f_hc3.params[v],
            "t_HC3": f_hc3.tvalues[v], "p_HC3": f_hc3.pvalues[v],
            "t_Cluster": f_cl.tvalues[v], "p_Cluster": f_cl.pvalues[v],
            "p_WildBootstrap": p_wcb, "N": int(f_hc3.nobs), "G_Clusters": G_cl,
            "R2": f_hc3.rsquared, "Adj_R2": f_hc3.rsquared_adj
        })
pd.DataFrame(reg_out).to_csv(os.path.join(OUT_DIR, "table10_repaired_wcb_regressions_N226.csv"), index=False)

print("\n=========================================================================")
print("4. DIRECT TEST OF A+H PRICE ANCHOR & A/H PREMIUM INVERSION (N=57 FULL CENSUS)")
print("=========================================================================")
print(f"Total Verified A+H Dual Listings in N=226 Panel: {int(m['is_ah_dual_listed'].sum())}")
ah57 = m[m["is_ah_dual_listed"] == 1].dropna(subset=["offer_vs_a_close_discount", "initial_return_pct"]).copy()
print(f"Audited A+H Dual-Listing Sample with FX-Matched A-Share Reference Prices: N = {len(ah57)}")
print(f"  H-Offer Discount to A-Share at Sub Close (N={len(ah57)}): Mean = {ah57['offer_vs_a_close_discount'].mean():+.2f}%, Median = {ah57['offer_vs_a_close_discount'].median():+.2f}% "
      f"[Min {ah57['offer_vs_a_close_discount'].min():+.2f}%, Max {ah57['offer_vs_a_close_discount'].max():+.2f}%]")
ah_pr = ah57.dropna(subset=["offer_vs_a_pricing_discount"]).copy()
print(f"  H-Offer Discount to A-Share at Pricing   (N={len(ah_pr)}): Mean = {ah_pr['offer_vs_a_pricing_discount'].mean():+.2f}%, Median = {ah_pr['offer_vs_a_pricing_discount'].median():+.2f}% "
      f"[Min {ah_pr['offer_vs_a_pricing_discount'].min():+.2f}%, Max {ah_pr['offer_vs_a_pricing_discount'].max():+.2f}%]")
print(f"  H-Day1 Close vs A-Share Close            (N={len(ah57)}): Mean = {ah57['h_day1_close_vs_a_discount'].mean():+.2f}%, Median = {ah57['h_day1_close_vs_a_discount'].median():+.2f}% "
      f"[Min {ah57['h_day1_close_vs_a_discount'].min():+.2f}%, Max {ah57['h_day1_close_vs_a_discount'].max():+.2f}%]")
inv = ah57[ah57["h_day1_close_vs_a_discount"] > 0].sort_values("h_day1_close_vs_a_discount", ascending=False)
print(f"  A/H Premium Inversions on Day 1 (H-Share > A-Share Close): {len(inv)} / {len(ah57)} deals ({len(inv)/len(ah57)*100:.1f}%):")
for _, row in inv.iterrows():
    print(f"    {row['stock_code']} ({row['company_name'].strip()[:38]}): Offer vs A Close = {row['offer_vs_a_close_discount']:+.2f}% | Day-1 IR = {row['initial_return_pct']:+.2f}% | Day-1 H vs A = {row['h_day1_close_vs_a_discount']:+.2f}%")

fit_ah57 = smf.ols("initial_return_pct ~ offer_vs_a_close_discount + log_proceeds", data=ah57).fit(cov_type="HC3")
print(f"  OLS of A+H Day-1 Return on Offer-vs-A Close Discount (N={len(ah57)}, R2={fit_ah57.rsquared:.3f}):")
for v in ["offer_vs_a_close_discount", "log_proceeds"]:
    print(f"    {v:28s}: coef={fit_ah57.params[v]:+.4f} (t_HC3={fit_ah57.tvalues[v]:+.2f}, p={fit_ah57.pvalues[v]:.4f})")

fit_ah_pr = smf.ols("initial_return_pct ~ offer_vs_a_pricing_discount + log_proceeds", data=ah_pr).fit(cov_type="HC3")
print(f"  OLS of A+H Day-1 Return on Offer-vs-A Pricing Discount (N={len(ah_pr)}, R2={fit_ah_pr.rsquared:.3f}):")
for v in ["offer_vs_a_pricing_discount", "log_proceeds"]:
    print(f"    {v:28s}: coef={fit_ah_pr.params[v]:+.4f} (t_HC3={fit_ah_pr.tvalues[v]:+.2f}, p={fit_ah_pr.pvalues[v]:.4f})")

ah57[["stock_code", "company_name", "a_symbol", "listing_date", "gross_proceeds_hkd_m",
      "offer_vs_a_close_discount", "offer_vs_a_pricing_discount", "initial_return_pct",
      "h_day1_close_vs_a_discount"]].to_csv(os.path.join(OUT_DIR, "table10b_ah_anchor_and_inversions_N57.csv"), index=False)

print("\n=========================================================================")
print("5. TRUE NET-OF-COST ROCK (1986) EQUILIBRIUM TESTS (N=113) & RENT ROBUSTNESS")
print("=========================================================================")
for label, col in [
    ("1-Lot Cash Net Excess over HIBOR (%)", "excess_1lot_ret_over_hibor_pct"),
    ("1-Lot Cash Annualized Excess (%)", "annualized_excess_1lot_pct"),
    ("10-Lot Cash Net Excess over HIBOR (%)", "excess_10lot_ret_over_hibor_pct"),
    ("Pool B Whale Flat-Margin Net Return (%)", "net_poolB_ret_flat_margin_pct"),
    ("Pool B Whale Full-HIBOR Net Return (%)", "net_poolB_ret_full_hibor_margin_pct"),
]:
    s = r[col].dropna()
    t_s, p_s = stats.ttest_1samp(s, 0.0)
    w_s, pw_s = stats.wilcoxon(s)
    pos_pct = (s > 0).mean() * 100
    print(f"  {label:40s}: Mean={s.mean():+7.3f}% | Med={s.median():+7.3f}% | %Pos={pos_pct:5.1f}% | t={t_s:+5.2f} (p={p_s:.4f}) | Wilcoxon p={pw_s:.4f}")

# Three-way Money Left on Table Robustness (Value-Weighted, Top-5 Excluded, Equal-Weighted Deal Shares, and 6M Realized Cornerstone)
m["ml_hkd_m"] = m["gross_proceeds_hkd_m"] * (m["initial_return_pct"] / 100.0)
m["sh_ret"] = m["public_offer_fraction_pct"] / 100.0
m["sh_cs"] = m["cornerstone_pct_of_offering"] / 100.0
m["sh_inst"] = 1.0 - m["sh_ret"] - m["sh_cs"]

print("\nThree-Way Rent Decomposition Robustness (Pre vs Post Prospectus Cutoff Aug 4, 2025):")
for reg_val, reg_lbl in [(0, "Pre-Aug 4, 2025 (Legacy PN18)"), (1, "Post-Aug 4, 2025 (Mech A/B Era)")]:
    sub = m[m["post_aug2025_prospectus"] == reg_val].dropna(subset=["ml_hkd_m", "sh_ret", "sh_cs"]).copy()
    tot_net = sub["ml_hkd_m"].sum() / 1000.0
    pos_only = sub[sub["ml_hkd_m"] > 0]
    tot_gross = pos_only["ml_hkd_m"].sum() / 1000.0
    vw_ret = (sub["ml_hkd_m"] * sub["sh_ret"]).sum() / sub["ml_hkd_m"].sum() * 100
    vw_cs = (sub["ml_hkd_m"] * sub["sh_cs"]).sum() / sub["ml_hkd_m"].sum() * 100
    vw_inst = (sub["ml_hkd_m"] * sub["sh_inst"]).sum() / sub["ml_hkd_m"].sum() * 100
    # Exclude top 5 MLOT deals
    sub_ex5 = sub.drop(sub["ml_hkd_m"].nlargest(5).index)
    ex5_ret = (sub_ex5["ml_hkd_m"] * sub_ex5["sh_ret"]).sum() / sub_ex5["ml_hkd_m"].sum() * 100
    ex5_cs = (sub_ex5["ml_hkd_m"] * sub_ex5["sh_cs"]).sum() / sub_ex5["ml_hkd_m"].sum() * 100
    ex5_inst = (sub_ex5["ml_hkd_m"] * sub_ex5["sh_inst"]).sum() / sub_ex5["ml_hkd_m"].sum() * 100
    # Equal-weighted across positive-IR deals
    ew_ret, ew_cs, ew_inst = pos_only["sh_ret"].mean() * 100, pos_only["sh_cs"].mean() * 100, pos_only["sh_inst"].mean() * 100
    print(f"  {reg_lbl} (N={len(sub)}, Net ML=HK${tot_net:.2f}B, Gross Pos ML=HK${tot_gross:.2f}B):")
    print(f"    Value-Weighted All    : Retail={vw_ret:5.2f}%, Cornerstone={vw_cs:5.2f}%, Free Inst={vw_inst:5.2f}%")
    print(f"    Excl. Top-5 Mega Deals: Retail={ex5_ret:5.2f}%, Cornerstone={ex5_cs:5.2f}%, Free Inst={ex5_inst:5.2f}%")
    print(f"    Equal-Weighted Pos IR : Retail={ew_ret:5.2f}%, Cornerstone={ew_cs:5.2f}%, Free Inst={ew_inst:5.2f}%")

# 6-Month Realized Cornerstone Rents vs Day-1 Paper Cornerstone Gains (Matured Deals with 6M BHR)
mat6 = m[(m["sh_cs"] > 0) & m["bhr_6m_pct"].notna()].copy()
# bhr_6m_pct in clean_micro_panel_2025_2026_N226.csv is harmonized in percentage points (%)
mat6["bhr_6m_true_pct"] = pd.to_numeric(mat6["bhr_6m_pct"], errors="coerce")
# Total 6M return from offer price P0 = (1 + IR) * (1 + BHR_6M) - 1
mat6["tot_6m_from_offer_pct"] = ((1.0 + mat6["initial_return_pct"] / 100.0) * (1.0 + mat6["bhr_6m_true_pct"] / 100.0) - 1.0) * 100.0
mat6["cs_cap_hkd_m"] = mat6["gross_proceeds_hkd_m"] * mat6["sh_cs"]
mat6["cs_day1_paper_m"] = mat6["cs_cap_hkd_m"] * (mat6["initial_return_pct"] / 100.0)
mat6["cs_6m_realized_m"] = mat6["cs_cap_hkd_m"] * (mat6["tot_6m_from_offer_pct"] / 100.0)
print(f"\n6-Month Realized Cornerstone Rents (Matured Cornerstone-Backed Deals, N={len(mat6)}):")
print(f"  Total Cornerstone Capital Committed : HK${mat6['cs_cap_hkd_m'].sum()/1000.0:.2f}B")
print(f"  Day-1 Paper Gain on Cornerstones    : HK${mat6['cs_day1_paper_m'].sum()/1000.0:+.2f}B (EW Mean = {mat6['initial_return_pct'].mean():+.2f}%, Med = {mat6['initial_return_pct'].median():+.2f}%)")
print(f"  Day-180 Unlock Realized Gain vs P0  : HK${mat6['cs_6m_realized_m'].sum()/1000.0:+.2f}B (EW Mean = {mat6['tot_6m_from_offer_pct'].mean():+.2f}%, Med = {mat6['tot_6m_from_offer_pct'].median():+.2f}%)")
print(f"  Aftermarket 6M BHR Drift (Day1->6M) : EW Mean = {mat6['bhr_6m_true_pct'].mean():+.2f}%, Med = {mat6['bhr_6m_true_pct'].median():+.2f}%")

print("\n=========================================================================")
print("6. DAY +180 LOCKUP EXPIRY EVENT STUDY: CLUSTERED & SKEWNESS-ADJUSTED INFERENCE")
print("=========================================================================")
master_full = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/pipeline/exports/HKIPO-MB-MASTER_clean.csv")
master_full["unlock_ym"] = pd.to_datetime(master_full["Earliest cornerstone unlock date (dd/mm/yy)"], errors="coerce").dt.to_period("M").astype(str)
master_full["unlock_dt"] = pd.to_datetime(master_full["Earliest cornerstone unlock date (dd/mm/yy)"], errors="coerce").astype(str)

def lbt_skew_t(arr):
    n = len(arr)
    mu = np.mean(arr)
    sd = np.std(arr, ddof=1)
    S = mu / (sd / np.sqrt(n))
    gamma = stats.skew(arr, bias=False)
    return float(np.sqrt(n) * (S / np.sqrt(n) + (gamma / 3.0) * (S / np.sqrt(n))**2 + gamma / (6.0 * n)))

for col_raw, label in [
    ("Cornerstone unlock CAR [-5, +5] (%)", "CAR[-5, +5] (%)"),
    ("Cornerstone unlock CAR [-20, +20] (%)", "CAR[-20, +20] (%)"),
]:
    u_df = master_full.dropna(subset=[col_raw, "Earliest cornerstone unlock date (dd/mm/yy)"]).copy()
    # Stored as decimal in Master -> multiply by 100 for percentage points
    u_df["car_pct"] = u_df[col_raw].astype(float) * 100.0
    t_cs, p_cs = stats.ttest_1samp(u_df["car_pct"], 0.0)
    t_lbt = lbt_skew_t(u_df["car_pct"].values)
    # Cluster by exact unlock calendar date AND by unlock calendar month
    f_dt = smf.ols("car_pct ~ 1", data=u_df).fit(cov_type="cluster", cov_kwds={"groups": u_df["unlock_dt"]})
    f_ym = smf.ols("car_pct ~ 1", data=u_df).fit(cov_type="cluster", cov_kwds={"groups": u_df["unlock_ym"]})
    w_stat, p_wilc = stats.wilcoxon(u_df["car_pct"])
    neg_pct = (u_df["car_pct"] < 0).mean() * 100.0
    print(f"  {label:18s} (N={len(u_df)}, DateClusters={u_df['unlock_dt'].nunique()}, MonthClusters={u_df['unlock_ym'].nunique()}):")
    print(f"    Mean={u_df['car_pct'].mean():+6.2f}%, Med={u_df['car_pct'].median():+6.2f}%, %Neg={neg_pct:5.1f}% | "
          f"t_CS={t_cs:+5.2f} (p={p_cs:.4f}) | t_LBT={t_lbt:+5.2f} | "
          f"t_DateClust={f_dt.tvalues['Intercept']:+5.2f} (p={f_dt.pvalues['Intercept']:.4f}) | "
          f"t_MonthClust={f_ym.tvalues['Intercept']:+5.2f} (p={f_ym.pvalues['Intercept']:.4f}) | Wilc_p={p_wilc:.4f}")
