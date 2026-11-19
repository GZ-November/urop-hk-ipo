"""Mainland China Policy Shocks & the 'A-Share Freeze Valve' Econometrics (1994M01-2026M09, T=393).

Tests whether CSRC onshore A-share IPO moratoria and cross-border regulatory shocks
divert Mainland Chinese equity issuance to HKEX, accounting for:
1. Contemporaneous market crashes vs. 6-to-12-month institutional IPO preparation lags;
2. Within-HKEX falsification/difference comparison (PRC H-Share IPOs vs. Non-H-Share IPOs);
3. Jorda (2005) Dynamic Local Projections with Newey-West HAC standard errors.
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
df = pd.read_csv(os.path.join(OUT_DIR, "clean_monthly_policy_valve_1994_2026.csv"))
df = df.sort_values("year_month").reset_index(drop=True)

# Construct macro controls and policy exposure variables
df["hsi_ret_6m_lag"] = df["hsi_monthly_return_pct"].rolling(6).sum().shift(1)
df["hsi_vol_lag1"] = df["hsi_20d_realized_vol_pct"].shift(1)
df["any_onshore_restriction"] = np.maximum(df["csrc_freeze_strict_pct"], df["csrc_tightening_pct"])
df["strict_freeze_share"] = df["csrc_freeze_strict_pct"]

# Pipeline gestation window: mean onshore restriction intensity over months [t-12, t-6]
df["freeze_strict_lag6_12"] = df["strict_freeze_share"].shift(6).rolling(7, min_periods=4).mean()
df["restriction_all_lag6_12"] = df["any_onshore_restriction"].shift(6).rolling(7, min_periods=4).mean()

# H-share share of HKEX IPOs (defined when hk_total_ipos > 0)
df["hshare_count_share_pct"] = np.where(
    df["hk_total_ipos"] > 0, df["hk_hshare_ipos"] / df["hk_total_ipos"] * 100.0, np.nan
)
df["hshare_proceeds_share_pct"] = np.where(
    df["hk_total_proceeds_hkd_m"] > 0,
    df["hk_hshare_proceeds_hkd_m"] / df["hk_total_proceeds_hkd_m"] * 100.0,
    np.nan,
)
df["log_hshare_ipos"] = np.log1p(df["hk_hshare_ipos"])
df["log_non_hshare_ipos"] = np.log1p(df["hk_non_hshare_ipos"])
df["log_hshare_proceeds"] = np.log1p(df["hk_hshare_proceeds_hkd_m"])
df["diff_log_h_vs_nonh"] = df["log_hshare_ipos"] - df["log_non_hshare_ipos"]
df["time_trend"] = np.arange(len(df)) / 12.0  # years since 1994

print("=========================================================================")
print("1. DESCRIPTIVE ANATOMY ACROSS MAINLAND CROSS-BORDER POLICY REGIMES (T=393)")
print("=========================================================================")

def classify_policy_era(r):
    ym = r["year_month"]
    if ym >= "2024-04":
        return "5. CSRC 8.27 Tightening + Apr 2024 5 HK Measures (2024.04-2026.09)"
    if ym >= "2023-04":
        return "4. CSRC Unified Overseas Filing + 8.27 Onset (2023.04-2024.03)"
    if ym >= "2021-07":
        return "3. CAC Data Review & US HFCAA Window (2021.07-2023.03)"
    if r["csrc_a_share_freeze_strict"] == 1:
        return "2. Historical CSRC A-Share Moratoria Months (1994-2015, Contemporaneous)"
    return "1. Normal Onshore A-Share Issuance Months (1994-2021.06)"

df["policy_era"] = df.apply(classify_policy_era, axis=1)
era_tab = df.groupby("policy_era").agg(
    Months=("year_month", "count"),
    Mean_Total_IPOs_pm=("hk_total_ipos", "mean"),
    Mean_HShare_IPOs_pm=("hk_hshare_ipos", "mean"),
    Mean_NonH_IPOs_pm=("hk_non_hshare_ipos", "mean"),
    HShare_Deal_Share_Pct=("hshare_count_share_pct", "mean"),
    Mean_HShare_Proceeds_HKDm_pm=("hk_hshare_proceeds_hkd_m", "mean"),
    HShare_Proceeds_Share_Pct=("hshare_proceeds_share_pct", "mean"),
)
print(era_tab.round(2).to_string())
era_tab.round(3).to_csv(os.path.join(OUT_DIR, "table_policy_valve_regimes.csv"))

print("\n=========================================================================")
print("2. NEWEY-WEST HAC TIME-SERIES REGRESSIONS: CONTEMPORANEOUS VS PIPELINE LAG")
print("=========================================================================")

reg_df = df.dropna(subset=["restriction_all_lag6_12", "hsi_ret_6m_lag", "hsi_vol_lag1"]).copy()
reg_df["post_decree43_202304"] = (reg_df["year_month"] >= "2023-04").astype(int)
print(f"Estimation sample after 12M lag initialization: T = {len(reg_df)} months ({reg_df['year_month'].min()} to {reg_df['year_month'].max()})")

specs = [
    ("M1: Log(1 + H-Share IPOs) — All Restrictions",
     "log_hshare_ipos ~ any_onshore_restriction + restriction_all_lag6_12 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df),
    ("M2: Log(1 + Non-H-Share IPOs) — Placebo / Within-HK Control",
     "log_non_hshare_ipos ~ any_onshore_restriction + restriction_all_lag6_12 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df),
    ("M3: Within-HK Diff [Log H-Share - Log Non-H]",
     "diff_log_h_vs_nonh ~ any_onshore_restriction + restriction_all_lag6_12 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df),
    ("M4: H-Share % of Monthly HKEX Deals (Active Months)",
     "hshare_count_share_pct ~ any_onshore_restriction + restriction_all_lag6_12 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df.dropna(subset=["hshare_count_share_pct"])),
    ("M5: Pre-2023 Historical Strict Freezes Only (1995-2022)",
     "hshare_count_share_pct ~ strict_freeze_share + freeze_strict_lag6_12 + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df[reg_df["year"] <= 2022].dropna(subset=["hshare_count_share_pct"])),
    ("M6: H-Share % Regime Decomposition (Decree 43 Interaction + 5 Measures)",
     "hshare_count_share_pct ~ any_onshore_restriction * post_decree43_202304 + restriction_all_lag6_12 * post_decree43_202304 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df.dropna(subset=["hshare_count_share_pct"])),
    ("M7: Within-HK Diff Regime Decomposition (Decree 43 Interaction + 5 Measures)",
     "diff_log_h_vs_nonh ~ any_onshore_restriction * post_decree43_202304 + restriction_all_lag6_12 * post_decree43_202304 + post_csrc_hk_cooperation_5_measures + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
     reg_df),
]

reg_rows = []
for title, fml, sub in specs:
    fit = smf.ols(fml, data=sub).fit(cov_type="HAC", cov_kwds={"maxlags": 12})
    print(f"\n--- {title} (T={int(fit.nobs)}, R2={fit.rsquared:.3f}) ---")
    for v in ["any_onshore_restriction", "restriction_all_lag6_12", "strict_freeze_share",
              "freeze_strict_lag6_12", "post_decree43_202304",
              "any_onshore_restriction:post_decree43_202304",
              "restriction_all_lag6_12:post_decree43_202304",
              "post_csrc_hk_cooperation_5_measures",
              "hsi_ret_6m_lag", "hsi_vol_lag1", "time_trend"]:
        if v in fit.params.index:
            print(f"  {v:36s}: coef={fit.params[v]:+8.4f} | t_HAC={fit.tvalues[v]:+6.2f} (p={fit.pvalues[v]:.4f})")
            reg_rows.append({
                "Model": title, "Variable": v, "Coef": fit.params[v],
                "SE_HAC": fit.bse[v], "t_HAC": fit.tvalues[v], "p_HAC": fit.pvalues[v],
                "T": int(fit.nobs), "R2": fit.rsquared
            })
pd.DataFrame(reg_rows).to_csv(os.path.join(OUT_DIR, "table_policy_valve_hac_regressions.csv"), index=False)

print("\n=========================================================================")
print("3. JORDA (2005) DYNAMIC LOCAL PROJECTIONS: ONSHORE RESTRICTION SHOCK (h=0..15)")
print("=========================================================================")
lp_rows = []
for h in [0, 3, 6, 9, 12, 15]:
    tmp = df.copy()
    tmp["y_hshare_lead"] = tmp["hshare_count_share_pct"].shift(-h)
    tmp["y_diff_lead"] = tmp["diff_log_h_vs_nonh"].shift(-h)
    tmp["y_h_count_lead"] = tmp["hk_hshare_ipos"].shift(-h)
    sub_h = tmp.dropna(subset=["y_hshare_lead", "hsi_ret_6m_lag", "hsi_vol_lag1", "hshare_count_share_pct"]).copy()
    sub_d = tmp.dropna(subset=["y_diff_lead", "hsi_ret_6m_lag", "hsi_vol_lag1"]).copy()

    fit_sh = smf.ols(
        "y_hshare_lead ~ any_onshore_restriction + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
        data=sub_h
    ).fit(cov_type="HAC", cov_kwds={"maxlags": h + 6})

    fit_df = smf.ols(
        "y_diff_lead ~ any_onshore_restriction + hsi_ret_6m_lag + hsi_vol_lag1 + time_trend + C(month)",
        data=sub_d
    ).fit(cov_type="HAC", cov_kwds={"maxlags": h + 6})

    b_sh, t_sh, p_sh = fit_sh.params["any_onshore_restriction"], fit_sh.tvalues["any_onshore_restriction"], fit_sh.pvalues["any_onshore_restriction"]
    b_df, t_df, p_df = fit_df.params["any_onshore_restriction"], fit_df.tvalues["any_onshore_restriction"], fit_df.pvalues["any_onshore_restriction"]
    print(f"  Horizon t+{h:2d}m (T={int(fit_df.nobs)}): "
          f"H-Share % Response = {b_sh:+6.2f} pp (t_HAC={t_sh:+5.2f}, p={p_sh:.4f}) | "
          f"Diff Log(H - NonH) = {b_df:+6.3f} (t_HAC={t_df:+5.2f}, p={p_df:.4f})")
    lp_rows.append({
        "horizon_months": h, "T_share": int(fit_sh.nobs), "T_diff": int(fit_df.nobs),
        "beta_hshare_pct": b_sh, "se_hshare_pct": fit_sh.bse["any_onshore_restriction"], "t_hshare_pct": t_sh, "p_hshare_pct": p_sh,
        "beta_diff_log": b_df, "se_diff_log": fit_df.bse["any_onshore_restriction"], "t_diff_log": t_df, "p_diff_log": p_df,
    })
pd.DataFrame(lp_rows).to_csv(os.path.join(OUT_DIR, "table_policy_valve_local_projections.csv"), index=False)
