#!/usr/bin/env python3
"""
Deep Frontier Empirical Suite (Part A):
1. Quarter-Century Hard-Cap Truncation (0 / 1,942 Priced Above Range) & Convex Demand Spillover
2. 33-Year Greenshoe Option Exercising (N=1,811), Zero-Return Pegging (IR=0%), & Cap. 571W Stabilization Cliff
3. Strategic Board-Lot Entry-Ticket Engineering (N=113) & Pre-Listing Margin Herding Cascades (Welch, 1992)
4. 33-Year Long-Run Equity Distress (1Y Loss >= 50%) & Delisting Determinants

Reads strictly from finalized CSVs; writes outputs to analysis/out/overview_extensions/.
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

IN_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
EXT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_extensions"
os.makedirs(EXT_DIR, exist_ok=True)

df = pd.read_csv(os.path.join(IN_DIR, "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"), low_memory=False)
rock = pd.read_csv(os.path.join(IN_DIR, "clean_rock_ballot_113_net_returns.csv"))
m226 = pd.read_csv(os.path.join(IN_DIR, "clean_micro_panel_2025_2026_N226.csv"))
margin_d = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/pipeline/exports/HKIPO-2026-margin-daily.csv")

df["proceeds_hkd_m"] = np.where(
    df["funds_raised_total_hkd"].notna() & (df["funds_raised_total_hkd"] > 0),
    df["funds_raised_total_hkd"] / 1e6,
    df["bbg_offer_size_m"]
)
df["log_proceeds_m"] = np.where(df["proceeds_hkd_m"] > 0, np.log(df["proceeds_hkd_m"]), np.nan)
df["is_gem"] = (df["board"] == "GEM").astype(int)
df["is_h_share"] = df["is_prc_joint_stock"].fillna(0).astype(int)

# ==============================================================================
# MODULE 1: QUARTER-CENTURY HARD-CAP TRUNCATION & CONVEX DEMAND SPILLOVER
# ==============================================================================
print("=========================================================================")
print("1. QUARTER-CENTURY HARD-CAP TRUNCATION (N=1,942) & CONVEX DEMAND SPILLOVER")
print("=========================================================================")
rng_df = df.dropna(subset=["bbg_priced_range_raw"]).copy()
print("Bloomberg 33-Year Range Pricing Outcomes (N = {}):".format(len(rng_df)))
print("  Priced Above Range : {:4d} ({:5.2f}%)  [vs. U.S. Ritter 1980-2025 ~25%!]".format(
    (rng_df["bbg_priced_range_raw"] == "Priced Above Range").sum(),
    (rng_df["bbg_priced_range_raw"] == "Priced Above Range").mean() * 100
))

rng_summary = []
for cat in ["Priced Below Range", "Priced Within Range"]:
    sub = rng_df[rng_df["bbg_priced_range_raw"] == cat]
    gs_sub = sub[sub["greenshoe_facility_m"] > 0]
    gs_rate = (gs_sub["greenshoe_shares_exercised_m"] / gs_sub["greenshoe_facility_m"]).clip(0, 1.15).mean() * 100
    rng_summary.append({
        "Range_Outcome": cat,
        "N": len(sub),
        "Share_Pct": len(sub) / len(rng_df) * 100,
        "Mean_Open_IR_Pct": sub["ir_open_pct"].dropna().mean(),
        "Mean_Close_IR_Pct": sub["ir_close_pct"].dropna().mean(),
        "Med_Close_IR_Pct": sub["ir_close_pct"].dropna().median(),
        "Day1_Break_Pct": (sub["ir_close_pct"].dropna() < 0).mean() * 100,
        "Med_Retail_Sub_x": sub["retail_sub_ratio_clean"].dropna().median(),
        "Mean_Greenshoe_Ex_Pct": gs_rate,
        "Mean_1Y_BHAR_Pct": sub["after_bhar_1y_pct"].dropna().mean(),
    })
rng_tab = pd.DataFrame(rng_summary)
print(rng_tab.round(2).to_string(index=False))
rng_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table1_33y_range_truncation.csv"), index=False)

# Convex Demand Spillover on Main Board (Retail Subscription Tiers -> Open Jump vs Intraday vs 1Y BHAR)
mb_sub = df[(df["board"] == "Main Board") & (df["retail_sub_ratio_clean"] > 0)].dropna(
    subset=["retail_sub_ratio_clean", "ir_open_pct", "ir_close_pct", "ir_intraday_pct"]
).copy()
mb_sub["log_sub"] = np.log(mb_sub["retail_sub_ratio_clean"])
mb_sub["log_sub_sq"] = mb_sub["log_sub"] ** 2
mb_sub["sub_tier"] = pd.cut(
    mb_sub["retail_sub_ratio_clean"],
    bins=[0, 1, 5, 15, 50, 100, 500, 1e9],
    labels=[
        "1. Undersubscribed (<1x)",
        "2. Mild (1x-5x)",
        "3. Moderate (5x-15x, Pre-Clawback)",
        "4. Warm (15x-50x, 30% Clawback)",
        "5. Hot (50x-100x, 40% Clawback)",
        "6. Very Hot (100x-500x, 50% Clawback)",
        "7. Super-Hot (>=500x)"
    ]
)
spill_tab = mb_sub.groupby("sub_tier", observed=True).agg(
    N=("ir_close_pct", "size"),
    Mean_Open_Jump_Pct=("ir_open_pct", "mean"),
    Med_Open_Jump_Pct=("ir_open_pct", "median"),
    Mean_Intraday_Ret_Pct=("ir_intraday_pct", "mean"),
    Med_Intraday_Ret_Pct=("ir_intraday_pct", "median"),
    Mean_Day1_Close_Pct=("ir_close_pct", "mean"),
    Day1_Break_Rate_Pct=("ir_close_pct", lambda s: (s < 0).mean() * 100),
    Mean_1Y_BHAR_Pct=("after_bhar_1y_pct", lambda s: s.dropna().mean()),
).reset_index()
print("\nMain Board Retail Demand Spillover Curve (Opening Auction vs Intraday Drift vs 1Y Reversal, N={}):".format(len(mb_sub)))
print(spill_tab.round(2).to_string(index=False))
spill_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table2_convex_demand_spillover.csv"), index=False)

fit_conv_open = smf.ols("ir_open_pct ~ log_sub + log_sub_sq + log_proceeds_m + C(cohort_year)", data=mb_sub).fit(cov_type="HC3")
fit_conv_intra = smf.ols("ir_intraday_pct ~ log_sub + log_sub_sq + log_proceeds_m + C(cohort_year)", data=mb_sub).fit(cov_type="HC3")
print("Convexity Test (Open Jump): beta_log_sub={:+.3f} (t={:+.2f}), beta_log_sub_sq={:+.3f} (t={:+.2f})".format(
    fit_conv_open.params["log_sub"], fit_conv_open.tvalues["log_sub"],
    fit_conv_open.params["log_sub_sq"], fit_conv_open.tvalues["log_sub_sq"]
))
print("Convexity Test (Intraday) : beta_log_sub={:+.3f} (t={:+.2f}), beta_log_sub_sq={:+.3f} (t={:+.2f})".format(
    fit_conv_intra.params["log_sub"], fit_conv_intra.tvalues["log_sub"],
    fit_conv_intra.params["log_sub_sq"], fit_conv_intra.tvalues["log_sub_sq"]
))


# ==============================================================================
# MODULE 2: 33-YEAR GREENSHOE EXERCISING, ZERO-RETURN PEGGING & CAP. 571W CLIFF
# ==============================================================================
print("\n=========================================================================")
print("2. 33-YEAR GREENSHOE EXERCISING (N=1,811), ZERO PEGGING & STABILIZATION CLIFF")
print("=========================================================================")
ir_valid = df.dropna(subset=["ir_close_pct"]).copy()
n_exact_zero = (ir_valid["ir_close_pct"].abs() <= 0.05).sum()
n_just_above = ((ir_valid["ir_close_pct"] > 0.05) & (ir_valid["ir_close_pct"] <= 2.00)).sum()
n_just_below = ((ir_valid["ir_close_pct"] >= -2.00) & (ir_valid["ir_close_pct"] < -0.05)).sum()
binom_res = stats.binomtest(n_just_above + n_exact_zero, n_just_above + n_exact_zero + n_just_below, 0.5)
print("Day-1 Return Asymmetry Around Offer Price P0 (N = {}):".format(len(ir_valid)))
print("  Exact Offer-Price Close ([-0.05%, +0.05%]): {:4d} deals ({:5.2f}% of all HKEX IPOs!)".format(
    n_exact_zero, n_exact_zero / len(ir_valid) * 100
))
print("  Just Below [-2.00%, -0.05%) = {:3d} vs. Non-Negative [0.00%, +2.00%] = {:3d} (Binomial p = {:.2e})".format(
    n_just_below, n_just_above + n_exact_zero, binom_res.pvalue
))

gs_df = df[(df["greenshoe_facility_m"] > 0) & df["ir_close_pct"].notna()].copy()
gs_df["shoe_ratio_pct"] = (gs_df["greenshoe_shares_exercised_m"] / gs_df["greenshoe_facility_m"]).clip(0, 1.15) * 100.0
gs_df["post_stab_1m_to_3m_bhar"] = gs_df["after_bhar_3m_pct"] - gs_df["after_bhar_1m_pct"]
gs_df["post_stab_1m_to_6m_bhar"] = gs_df["after_bhar_6m_pct"] - gs_df["after_bhar_1m_pct"]

def classify_day1_stab(r):
    ir = r["ir_close_pct"]
    if ir < -2.0:
        return "1. Broken Below -2% (Failed/Withdrawn Bid)"
    elif ir < -0.05:
        return "2. Mild Break [-2%, -0.05%)"
    elif ir <= 0.50:
        return "3. Pegged at P0 [-0.05%, +0.50%] (Active Support Zone)"
    elif ir <= 10.0:
        return "4. Modest Gain (+0.50%, +10%]"
    else:
        return "5. Hot Unstabilized (> +10%)"

gs_df["stab_zone"] = gs_df.apply(classify_day1_stab, axis=1)
gs_zone_tab = gs_df.groupby("stab_zone", observed=True).agg(
    N=("shoe_ratio_pct", "size"),
    Zero_Shoe_Pct=("shoe_ratio_pct", lambda s: (s == 0).mean() * 100),
    Full_Shoe_Pct=("shoe_ratio_pct", lambda s: (s >= 99.0).mean() * 100),
    Mean_Shoe_Ratio_Pct=("shoe_ratio_pct", "mean"),
    BHAR_StabWindow_1M_Pct=("after_bhar_1m_pct", lambda s: s.dropna().mean()),
    BHAR_PostExpiry_1M_to_3M_Pct=("post_stab_1m_to_3m_bhar", lambda s: s.dropna().mean()),
    BHAR_PostExpiry_1M_to_6M_Pct=("post_stab_1m_to_6m_bhar", lambda s: s.dropna().mean()),
    Mean_1Y_BHAR_Pct=("after_bhar_1y_pct", lambda s: s.dropna().mean()),
).reset_index()
print("\n33-Year Greenshoe Exercise & Cap. 571W Post-Stabilization Expiry Path (N = {}):".format(len(gs_df)))
print(gs_zone_tab.round(2).to_string(index=False))
gs_zone_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table3_33y_greenshoe_stabilization.csv"), index=False)

# Formal test on Pegged Zero-Shoe Deals (Active Stabilization Footprint: |IR| <= 0.50% and Zero Shoe Exercised)
pegged_zero = gs_df[(gs_df["ir_close_pct"].between(-0.05, 0.50)) & (gs_df["shoe_ratio_pct"] == 0)].copy()
t_1m3m, p_1m3m = stats.ttest_1samp(pegged_zero["post_stab_1m_to_3m_bhar"].dropna(), 0.0)
t_1m6m, p_1m6m = stats.ttest_1samp(pegged_zero["post_stab_1m_to_6m_bhar"].dropna(), 0.0)
t_1y_pz, p_1y_pz = stats.ttest_1samp(pegged_zero["after_bhar_1y_pct"].dropna(), 0.0)
print("Stabilized Pegged Zero-Shoe Deals (N={}):".format(len(pegged_zero)))
print("  During Active 30-Day Window (Day1->1M BHAR): {:+.2f}%".format(pegged_zero["after_bhar_1m_pct"].dropna().mean()))
print("  Post-Expiry Cliff (1M->3M BHAR)            : {:+.2f}% (t={:+.2f}, p={:.4f})".format(
    pegged_zero["post_stab_1m_to_3m_bhar"].dropna().mean(), t_1m3m, p_1m3m
))
print("  Post-Expiry Drift (1M->6M BHAR)            : {:+.2f}% (t={:+.2f}, p={:.4f})".format(
    pegged_zero["post_stab_1m_to_6m_bhar"].dropna().mean(), t_1m6m, p_1m6m
))
print("  Full 1-Year Aftermarket BHAR               : {:+.2f}% (Med={:+.2f}%, t={:+.2f}, p={:.4f})".format(
    pegged_zero["after_bhar_1y_pct"].dropna().mean(), pegged_zero["after_bhar_1y_pct"].dropna().median(), t_1y_pz, p_1y_pz
))


# ==============================================================================
# MODULE 3: STRATEGIC BOARD-LOT ENTRY TICKET DESIGN & PRE-LISTING MARGIN CASCADES
# ==============================================================================
print("\n=========================================================================")
print("3. BOARD-LOT ENTRY TICKET ENGINEERING (N=113) & MARGIN CASCADES (WELCH 1992)")
print("=========================================================================")
r_m = rock.merge(
    m226[["stock_code", "subscription_ratio_times", "gross_proceeds_hkd_m", "is_ah_dual_listed", "is_18a", "is_18c"]],
    on="stock_code", how="left"
)
r_m["log_entry_ticket"] = np.log(r_m["entry_1lot_cost_hkd"])
r_m["log_proc"] = np.log(r_m["gross_proceeds_hkd_m"])
r_m["log_sub"] = np.log(r_m["subscription_ratio_times"])
r_m["ticket_tier"] = pd.qcut(r_m["entry_1lot_cost_hkd"], q=3, labels=[
    "Low Entry Ticket (T1)", "Medium Entry Ticket (T2)", "High Entry Ticket (T3)"
])
lot_tab = r_m.groupby("ticket_tier", observed=True).agg(
    N=("stock_code", "size"),
    Min_Ticket_HKD=("entry_1lot_cost_hkd", "min"),
    Med_Ticket_HKD=("entry_1lot_cost_hkd", "median"),
    Max_Ticket_HKD=("entry_1lot_cost_hkd", "max"),
    Med_Sub_Ratio_x=("subscription_ratio_times", "median"),
    Mean_1Lot_Alloc_Pct=("alloc_rate_1lot_pct", "mean"),
    Mean_Day1_IR_Pct=("initial_return_pct", "mean"),
    Mean_1Lot_Net_Excess_Pct=("excess_1lot_ret_over_hibor_pct", "mean"),
    Med_1Lot_Net_Excess_Pct=("excess_1lot_ret_over_hibor_pct", "median"),
).reset_index()
print("Board-Lot Minimum Entry Ticket Terciles (2026 All 113 IPOs):")
print(lot_tab.round(2).to_string(index=False))
lot_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table4_board_lot_entry_ticket.csv"), index=False)

fit_lot_alloc = smf.ols("alloc_rate_1lot_pct ~ log_entry_ticket + log_proc + log_sub", data=r_m).fit(cov_type="HC3")
fit_lot_sub = smf.ols("log_sub ~ log_entry_ticket + log_proc + is_ah_dual_listed", data=r_m).fit(cov_type="HC3")
print("OLS 1-Lot Allocation Rate on log(Entry Ticket) controlling for Size & Oversub: beta={:+.2f}% (t={:+.2f}, p={:.4f})".format(
    fit_lot_alloc.params["log_entry_ticket"], fit_lot_alloc.tvalues["log_entry_ticket"], fit_lot_alloc.pvalues["log_entry_ticket"]
))
print("OLS log(Retail Oversub) on log(Entry Ticket) controlling for Size & A+H      : beta={:+.3f} (t={:+.2f}, p={:.4f})".format(
    fit_lot_sub.params["log_entry_ticket"], fit_lot_sub.tvalues["log_entry_ticket"], fit_lot_sub.pvalues["log_entry_ticket"]
))

# Margin Daily Cascades (HKIPO-2026-margin-daily.csv)
margin_d["stock_code_clean"] = margin_d["stock_code"].astype(str).str.strip()
# Standardize stock_code format
if not margin_d["stock_code_clean"].iloc[0].endswith(".HK"):
    margin_d["stock_code_clean"] = margin_d["stock_code_clean"].str.replace(".HK", "", regex=False).str.zfill(4) + ".HK"
md_valid = margin_d[margin_d["available_before_deadline"] == True].copy() if "available_before_deadline" in margin_d.columns else margin_d.copy()
# Group by stock_code: earliest observed pre-deadline margin multiple vs peak pre-deadline margin multiple
mg_agg = margin_d.sort_values(["stock_code_clean", "days_to_deadline"], ascending=[True, False]).groupby("stock_code_clean").agg(
    n_obs=("margin_multiple", "size"),
    max_days_before=("days_to_deadline", "max"),
    early_margin_x=("margin_multiple", "first"),
    peak_margin_x=("margin_multiple", "max"),
).reset_index().rename(columns={"stock_code_clean": "stock_code"})

mg_merged = mg_agg.merge(m226, on="stock_code", how="inner").dropna(subset=["early_margin_x", "subscription_ratio_times", "initial_return_pct"])
mg_merged = mg_merged[mg_merged["early_margin_x"] > 0].copy()
mg_merged["log_early_margin"] = np.log1p(mg_merged["early_margin_x"])
mg_merged["log_final_sub"] = np.log1p(mg_merged["subscription_ratio_times"])
mg_merged["cascade_multiplier"] = mg_merged["subscription_ratio_times"] / np.maximum(mg_merged["early_margin_x"], 0.1)
if len(mg_merged) >= 10:
    fit_casc1 = smf.ols("log_final_sub ~ log_early_margin", data=mg_merged).fit(cov_type="HC3")
    fit_casc2 = smf.ols("initial_return_pct ~ log_early_margin + is_ah_dual_listed", data=mg_merged).fit(cov_type="HC3")
    print("\nPre-Deadline Margin Cascade Analysis (N = {} unique 2026 IPOs, {} daily observations):".format(
        len(mg_merged), len(margin_d)
    ))
    print("  Early Margin -> Final Total Oversubscription Elasticity: beta={:+.3f} (t_HC3={:+.2f}, R2={:.3f})".format(
        fit_casc1.params["log_early_margin"], fit_casc1.tvalues["log_early_margin"], fit_casc1.rsquared
    ))
    print("  Early Margin -> Day-1 Initial Return (%)               : beta={:+.2f}% per log unit (t_HC3={:+.2f}, p={:.4f}, R2={:.3f})".format(
        fit_casc2.params["log_early_margin"], fit_casc2.tvalues["log_early_margin"], fit_casc2.pvalues["log_early_margin"], fit_casc2.rsquared
    ))
    print("  Median Final-Sub / Early-Margin Amplification Ratio    : {:.2f}x (Mean {:.2f}x)".format(
        mg_merged["cascade_multiplier"].median(), mg_merged["cascade_multiplier"].mean()
    ))


# ==============================================================================
# MODULE 4: 33-YEAR SEVERE EQUITY DISTRESS (1Y LOSS >= 50%) & DELISTING HAZARD
# ==============================================================================
print("\n=========================================================================")
print("4. 33-YEAR SEVERE 1-YEAR EQUITY DISTRESS (LOSS >= 50%) & DELISTING DETERMINANTS")
print("=========================================================================")
dist_df = df.dropna(subset=["after_bhr_1y_pct", "log_proceeds_m", "ir_close_pct"]).copy()
dist_df["severe_crash_1y"] = (dist_df["after_bhr_1y_pct"] <= -50.0).astype(int)
dist_df["shell_era_2013_2017"] = dist_df["cohort_year"].between(2013, 2017).astype(int)
dist_df["log_ir_d1"] = np.log1p(np.maximum(dist_df["ir_close_pct"] / 100.0, -0.95))

print("Overall 1-Year Severe Crash Rate (Aftermarket BHR <= -50% from Day-1 Close, N={}): {:.2f}%".format(
    len(dist_df), dist_df["severe_crash_1y"].mean() * 100
))
print("  Main Board Severe 1Y Crash Rate: {:.2f}% (N={})".format(
    dist_df[dist_df["is_gem"] == 0]["severe_crash_1y"].mean() * 100, (dist_df["is_gem"] == 0).sum()
))
print("  GEM Severe 1Y Crash Rate       : {:.2f}% (N={})".format(
    dist_df[dist_df["is_gem"] == 1]["severe_crash_1y"].mean() * 100, (dist_df["is_gem"] == 1).sum()
))
print("  2013-2017 GEM Shell Bubble Crash Rate: {:.2f}% (N={})!".format(
    dist_df[(dist_df["is_gem"] == 1) & (dist_df["shell_era_2013_2017"] == 1)]["severe_crash_1y"].mean() * 100,
    ((dist_df["is_gem"] == 1) & (dist_df["shell_era_2013_2017"] == 1)).sum()
))

fit_crash = smf.ols(
    "severe_crash_1y ~ is_gem * shell_era_2013_2017 + is_h_share + log_proceeds_m + log_ir_d1",
    data=dist_df
).fit(cov_type="HC3")
print("\nLinear Probability Model of Severe 1-Year Crash (Loss >= 50% from P1, N={}, R2={:.3f}):".format(
    int(fit_crash.nobs), fit_crash.rsquared
))
for k in ["Intercept", "is_gem", "shell_era_2013_2017", "is_gem:shell_era_2013_2017", "is_h_share", "log_proceeds_m", "log_ir_d1"]:
    print("  {:28s}: {:+7.4f} ({:+6.2f} pp) | t_HC3={:+6.2f} (p={:.4f})".format(
        k, fit_crash.params[k], fit_crash.params[k]*100, fit_crash.tvalues[k], fit_crash.pvalues[k]
    ))

# Pre-2020 cohort long-run Delisting / Acquisition Probability (giving >=6 years seasoning)
seasoned = df[df["cohort_year"] <= 2019].dropna(subset=["log_proceeds_m"]).copy()
seasoned["delisted_int"] = seasoned["flag_delisted_or_acquired"].astype(int)
fit_delist = smf.ols(
    "delisted_int ~ is_gem + is_h_share + log_proceeds_m + C(epoch)",
    data=seasoned
).fit(cov_type="HC3")
print("\nLong-Run Delisting/Acquisition LPM (1994-2019 Seasoned Cohorts, N={}):".format(int(fit_delist.nobs)))
for k in ["is_gem", "is_h_share", "log_proceeds_m"]:
    print("  {:28s}: {:+7.4f} ({:+6.2f} pp) | t_HC3={:+6.2f} (p={:.4f})".format(
        k, fit_delist.params[k], fit_delist.params[k]*100, fit_delist.tvalues[k], fit_delist.pvalues[k]
    ))

# Also check Week 1 vs Month 1 stabilization decay on Pegged Zero-Shoe Deals
print("\nPegged Zero-Shoe Stabilization Decay Path (N={}):".format(len(pegged_zero)))
for col_nm, lbl in [("after_bhar_1w_pct", "Day 1 -> Week 1 BHAR"), ("after_bhar_1m_pct", "Day 1 -> Month 1 BHAR"), ("after_bhar_3m_pct", "Day 1 -> Month 3 BHAR")]:
    s_tmp = pegged_zero[col_nm].dropna()
    t_s, p_s = stats.ttest_1samp(s_tmp, 0.0)
    print("  {:24s}: Mean={:+.2f}% | Med={:+.2f}% | t={:+.2f} (p={:.4f})".format(lbl, s_tmp.mean(), s_tmp.median(), t_s, p_s))
