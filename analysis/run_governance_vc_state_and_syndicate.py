#!/usr/bin/env python3
"""
Deep Frontier Empirical Suite (Part B):
1. Pre-IPO Financing Ecosystem: Private VC/PE, Corporate VC, Municipal/State Guidance Funds & SOE Cornerstones
2. Ultimate Controller Governance, Control Wedges, Customer Concentration & Debt-Repayment Signaling (Drucker & Puri, 2005)
3. Post-2022 Syndicate Fee Contracting (Fixed Base vs. Discretionary Incentive Fees, Rule 3A.35)
4. HKMA Interbank Liquidity (Aggregate Balance & HIBOR), Day-1 Flipping & 6-Month Liquidity Decay

Reads strictly from HKIPO-MB-MASTER_clean.csv and clean_micro_panel_2025_2026_N226.csv;
writes outputs exclusively to analysis/out/overview_extensions/.
"""
import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

EXT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_extensions"
os.makedirs(EXT_DIR, exist_ok=True)

master = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/pipeline/exports/HKIPO-MB-MASTER_clean.csv", low_memory=False)
m226 = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026/clean_micro_panel_2025_2026_N226.csv")

df = master.merge(
    m226[["stock_code", "p0_offer_price_hkd", "gross_proceeds_hkd_m", "initial_return_pct",
          "subscription_ratio_times", "is_ah_dual_listed", "is_18a", "is_18c", "is_wvr",
          "cornerstone_pct_of_offering", "post_aug2025_prospectus"]],
    left_on="Stock Code", right_on="stock_code", how="inner"
)

# Convert decimal percentages in master to percentage points [0, 100]
df["top5_cust_pct"] = pd.to_numeric(df["Top 5 customers (% of year-1 revenue)"], errors="coerce") * 100.0
df["debt_repay_pct"] = pd.to_numeric(df["Debt repayment (% of planned net IPO proceeds)"], errors="coerce") * 100.0
df["has_debt_repay"] = np.where(df["debt_repay_pct"].notna(), (df["debt_repay_pct"] > 0).astype(float), np.nan)
df["uw_comm_pct"] = pd.to_numeric(df["Underwriting Commission (% of fund raised HK (a)"], errors="coerce") * 100.0
df["listing_exp_hkd_m"] = pd.to_numeric(df["Listing expenses (HK$)"], errors="coerce") / 1e6
df["total_exp_ratio_pct"] = np.where(
    (df["listing_exp_hkd_m"] > 0) & (df["gross_proceeds_hkd_m"] > 0),
    df["listing_exp_hkd_m"] / df["gross_proceeds_hkd_m"] * 100.0,
    np.nan
)
df["non_uw_overhead_pct"] = np.where(
    df["total_exp_ratio_pct"].notna() & df["uw_comm_pct"].notna(),
    np.maximum(df["total_exp_ratio_pct"] - df["uw_comm_pct"], 0.0),
    np.nan
)

df["flip_day1_pct"] = pd.to_numeric(df["First-day flipping ratio (%)"], errors="coerce") * 100.0
df["liq_decay_6m_pct"] = pd.to_numeric(df["Liquidity decay ratio (6M vs Day-1 turnover)"], errors="coerce") * 100.0
df["hibor_1m_pct"] = pd.to_numeric(df["1-month HIBOR before prospectus (%)"], errors="coerce") * 100.0
df["hkma_agg_bal_bn"] = pd.to_numeric(df["Banking system aggregate balance before prospectus (HK$)"], errors="coerce") / 1e9
df["log_hkma_bal"] = np.log(df["hkma_agg_bal_bn"])
df["rd_int_pct"] = pd.to_numeric(df["rd_expense_intensity_y1"], errors="coerce") * 100.0
df["roa_pct"] = pd.to_numeric(df["roa_y1"], errors="coerce") * 100.0
df["wedge_pct"] = pd.to_numeric(df["voting_cashflow_wedge"], errors="coerce") * 100.0
df["bhr_6m_pct"] = pd.to_numeric(df["6-month BHR from Day-1 close (%)"], errors="coerce") * 100.0
df["bhr_1m_pct"] = pd.to_numeric(df["1-month BHR from Day-1 close (%)"], errors="coerce") * 100.0

df["vc_pe"] = pd.to_numeric(df["Pre-IPO VC/PE backing (1=yes; 0=no)"], errors="coerce")
df["vc_only"] = pd.to_numeric(df["Pre-IPO VC backing (1=yes; 0=no)"], errors="coerce")
df["pe_only"] = pd.to_numeric(df["Pre-IPO PE backing (1=yes; 0=no)"], errors="coerce")
df["cvc_back"] = pd.to_numeric(df["Pre-IPO CVC backing (1=yes; 0=no)"], errors="coerce")
# Combine explicit Pre-IPO State/Gov backing and Pre-IPO state-owned backing flag cleanly
st_pre1 = pd.to_numeric(df["Pre-IPO State/Gov backing (1=yes; 0=no)"], errors="coerce")
st_pre2 = pd.to_numeric(df["Pre-IPO state-owned backing flag"], errors="coerce")
df["state_preipo"] = np.where(st_pre1.notna() | st_pre2.notna(), np.nanmax(np.vstack([st_pre1, st_pre2]), axis=0), np.nan)
df["toptier_vc"] = pd.to_numeric(df["Top-tier VC/PE backing (1=yes; 0=no)"], errors="coerce")
df["soe_cornerstone"] = pd.to_numeric(df["Cornerstone state-owned presence flag"], errors="coerce")
df["preipo_dur_yrs"] = pd.to_numeric(df["Pre-IPO holding duration (years)"], errors="coerce")
df["bank_sponsor"] = pd.to_numeric(df["Sponsor commercial bank affiliate flag"], errors="coerce")
df["joint_sponsors_n"] = pd.to_numeric(df["Joint sponsor count"], errors="coerce")

df["log_proc"] = np.log(df["gross_proceeds_hkd_m"])
df["log_sub"] = np.log(df["subscription_ratio_times"])
df["log_ir"] = np.log1p(np.maximum(df["initial_return_pct"] / 100.0, -0.95))

# Classify Ultimate Controller Type
def classify_controller(val):
    s = str(val).lower()
    if any(k in s for k in ["sasac", "国资", "state", "government", "ministry", "provincial", "municipal", "soe", "central huijin", "财政"]):
        return "State / SASAC Controlled"
    if any(k in s for k in ["none", "no controlling", "widely held", "无控股", "无实际控制", "nil", "dispersed"]):
        return "Widely Held / No Controlling Shareholder"
    return "Founder / Individual / Family Controlled"

df["controller_group"] = df["Ultimate controller type"].apply(classify_controller)

def route_label(r):
    # Mutually exclusive statutory chapter priority matching Main Manuscript Table 6B:
    # 18A (26) -> 18C (23) -> Conventional A+H (55; excl. 2493.HK [18A+AH] & 6727.HK [18C+AH]) -> Standard Main Board (122; incl. 7 non-18C WVR)
    if r["is_18a"] == 1:
        return "1. Ch. 18A Pre-Revenue Biotech"
    if r["is_18c"] == 1:
        return "2. Ch. 18C Specialist Hard-Tech"
    if r["is_ah_dual_listed"] == 1:
        return "3. A+H Dual-Listed (Conventional)"
    return "4. Standard Main Board (Rule 8.05 / 8A)"

df["route_cat"] = df.apply(route_label, axis=1)

# ==============================================================================
# 1. PRE-IPO PRIVATE VC/PE VS. STATE GUIDANCE FUNDS & SOE CORNERSTONES
# ==============================================================================
print("=========================================================================")
print(f"1. PRE-IPO PRIVATE VC/PE, CVC, STATE GUIDANCE FUNDS & SOE CORNERSTONES (N={len(df)})")
print("=========================================================================")
vc_rows = []
for cat in sorted(df["route_cat"].unique()) + ["All Audited 2025-2026 IPOs"]:
    sub = df if cat.startswith("All") else df[df["route_cat"] == cat]
    vc_rows.append({
        "Listing_Route": cat,
        "N": len(sub),
        "VC_PE_Backed_Pct": sub["vc_pe"].dropna().mean() * 100,
        "CVC_Backed_Pct": sub["cvc_back"].dropna().mean() * 100,
        "State_Guidance_PreIPO_Pct": sub["state_preipo"].dropna().mean() * 100,
        "SOE_Cornerstone_Pct": sub["soe_cornerstone"].dropna().mean() * 100,
        "Med_PreIPO_Duration_Yrs": sub["preipo_dur_yrs"].dropna().median(),
        "Med_Top5_Customer_Pct": sub["top5_cust_pct"].dropna().median(),
        "Mean_Debt_Repay_Share_Pct": sub["debt_repay_pct"].dropna().mean(),
    })
vc_tab = pd.DataFrame(vc_rows)
print(vc_tab.round(2).to_string(index=False))
vc_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table5_vc_state_and_fundamentals_by_route.csv"), index=False)

# Controller Governance Table
ctrl_tab = df.groupby("controller_group").agg(
    N=("stock_code", "size"),
    Share_Pct=("stock_code", lambda s: len(s) / len(df) * 100),
    Mean_Control_Wedge_Pct=("wedge_pct", lambda s: s.dropna().mean()),
    SOE_Cornerstone_Pct=("soe_cornerstone", lambda s: s.dropna().mean() * 100),
    Mean_IR_Pct=("initial_return_pct", "mean"),
    Med_IR_Pct=("initial_return_pct", "median"),
    Break_Rate_Pct=("initial_return_pct", lambda s: (s < 0).mean() * 100),
    Mean_6M_BHR_Pct=("bhr_6m_pct", lambda s: s.dropna().mean()),
).reset_index()
print(f"\nUltimate Controller Governance Anatomy (N={len(df)}):")
print(ctrl_tab.round(2).to_string(index=False))
ctrl_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table6_controller_governance.csv"), index=False)


# ==============================================================================
# 2. DEBT-REPAYMENT SIGNALING & UNIVERSAL BANK SPONSOR TEST (DRUCKER & PURI 2005)
# ==============================================================================
print("\n=========================================================================")
print("2. USE OF PROCEEDS (DEBT REPAYMENT) & COMMERCIAL-BANK SPONSOR CONFLICT TEST")
print("=========================================================================")
debt_df = df.dropna(subset=["debt_repay_pct", "bank_sponsor", "initial_return_pct", "subscription_ratio_times"]).copy()
for flag, lbl in [(0, "Zero Debt Repayment (100% Growth/R&D/Working Cap)"), (1, "Positive Debt Repayment (>0% of Net Proceeds)")]:
    s = debt_df[debt_df["has_debt_repay"] == flag]
    print("  {:50s} (N={:3d}, {:5.1f}%): Mean DebtShare={:5.1f}% | BankSponsor={:5.1f}% | MedSub={:6.1f}x | MeanIR={:+6.2f}% | Break={:5.1f}% | 6M_BHR={:+6.2f}%".format(
        lbl, len(s), len(s)/len(debt_df)*100,
        s["debt_repay_pct"].mean(), s["bank_sponsor"].mean()*100,
        s["subscription_ratio_times"].median(), s["initial_return_pct"].mean(),
        (s["initial_return_pct"] < 0).mean()*100, s["bhr_6m_pct"].dropna().mean()
    ))

fit_debt_ir = smf.ols("log_ir ~ debt_repay_pct + bank_sponsor + log_proc + is_ah_dual_listed + is_18a", data=debt_df).fit(cov_type="HC3")
fit_debt_sub = smf.ols("log_sub ~ debt_repay_pct + bank_sponsor + log_proc + is_ah_dual_listed + is_18a", data=debt_df).fit(cov_type="HC3")
fit_bank_debt = smf.ols("debt_repay_pct ~ bank_sponsor + log_proc + roa_pct + is_ah_dual_listed", data=debt_df).fit(cov_type="HC3")
print("  OLS log(1+IR) on Debt Repayment % : beta={:+.4f} (t_HC3={:+.2f}, p={:.4f})".format(
    fit_debt_ir.params["debt_repay_pct"], fit_debt_ir.tvalues["debt_repay_pct"], fit_debt_ir.pvalues["debt_repay_pct"]
))
print("  OLS log(Sub) on Debt Repayment %  : beta={:+.4f} (t_HC3={:+.2f}, p={:.4f})".format(
    fit_debt_sub.params["debt_repay_pct"], fit_debt_sub.tvalues["debt_repay_pct"], fit_debt_sub.pvalues["debt_repay_pct"]
))
print("  OLS Debt Repayment % on Bank-Affiliated Sponsor: beta={:+.2f} pp (t_HC3={:+.2f}, p={:.4f})".format(
    fit_bank_debt.params["bank_sponsor"], fit_bank_debt.tvalues["bank_sponsor"], fit_bank_debt.pvalues["bank_sponsor"]
))


# ==============================================================================
# 3. RITTER (1987) TOTAL DIRECT GOING-PUBLIC COST DECOMPOSITION (N=198)
# ==============================================================================
print("\n=========================================================================")
print("3. RITTER (1987) DIRECT GOING-PUBLIC COSTS: UNDERWRITING VS FIXED OVERHEAD")
print("=========================================================================")
cost_df = df.dropna(subset=["total_exp_ratio_pct", "uw_comm_pct", "non_uw_overhead_pct", "gross_proceeds_hkd_m"]).copy()
cost_df = cost_df[cost_df["total_exp_ratio_pct"] <= 60.0].copy()
cost_df["size_q"] = pd.qcut(cost_df["gross_proceeds_hkd_m"], q=4, labels=[
    "Q1 Smallest (<P25)", "Q2 Lower-Mid (P25-P50)", "Q3 Upper-Mid (P50-P75)", "Q4 Largest (>P75)"
])
cost_rows = []
for q_lbl in list(cost_df["size_q"].cat.categories) + ["All Audited IPOs"]:
    s = cost_df if q_lbl.startswith("All") else cost_df[cost_df["size_q"] == q_lbl]
    cost_rows.append({
        "Deal_Size_Quartile": q_lbl,
        "N": len(s),
        "Med_Proceeds_HKDm": s["gross_proceeds_hkd_m"].median(),
        "Mean_Total_Expense_HKDm": s["listing_exp_hkd_m"].mean(),
        "Med_Total_Expense_HKDm": s["listing_exp_hkd_m"].median(),
        "Mean_UW_Spread_Pct": s["uw_comm_pct"].mean(),
        "Mean_NonUW_Legal_Audit_Sponsor_Pct": s["non_uw_overhead_pct"].mean(),
        "Mean_Total_Direct_Cost_Pct": s["total_exp_ratio_pct"].mean(),
        "Med_Total_Direct_Cost_Pct": s["total_exp_ratio_pct"].median(),
    })
cost_tab = pd.DataFrame(cost_rows)
print(cost_tab.round(2).to_string(index=False))
cost_tab.round(4).to_csv(os.path.join(EXT_DIR, "ext_table7_ritter1987_direct_cost_decomposition.csv"), index=False)
print("  Mean Joint Sponsors per Deal       : {:.2f} (Median {:.1f}, >=2 Sponsors in {:.1f}% of deals)".format(
    df["joint_sponsors_n"].dropna().mean(), df["joint_sponsors_n"].dropna().median(),
    (df["joint_sponsors_n"].dropna() >= 2).mean() * 100
))


# ==============================================================================
# 4. HKMA INTERBANK LIQUIDITY, HIBOR, DAY-1 FLIPPING & 6M LIQUIDITY COLLAPSE
# ==============================================================================
print("\n=========================================================================")
print("4. HKMA INTERBANK LIQUIDITY, HIBOR, DAY-1 FLIPPING & 6M LIQUIDITY DECAY")
print("=========================================================================")
print("Day-1 Flipping Ratio (% of Offering Traded on Day 1, N={}): Mean={:.2f}% | Median={:.2f}% | P75={:.2f}%".format(
    df["flip_day1_pct"].notna().sum(), df["flip_day1_pct"].mean(), df["flip_day1_pct"].median(), df["flip_day1_pct"].quantile(0.75)
))
print("6-Month Liquidity Decay Ratio (6M Daily Turnover / Day-1 Turnover, N={}): Mean={:.2f}% | Median={:.2f}%".format(
    df["liq_decay_6m_pct"].notna().sum(), df["liq_decay_6m_pct"].mean(), df["liq_decay_6m_pct"].median()
))

fit_hibor_sub = smf.ols(
    "log_sub ~ hibor_1m_pct + post_aug2025_prospectus + log_proc + is_ah_dual_listed",
    data=df.dropna(subset=["hibor_1m_pct", "log_sub", "log_proc"])
).fit(cov_type="HC3")
fit_flip = smf.ols(
    "flip_day1_pct ~ log_sub + cornerstone_pct_of_offering + post_aug2025_prospectus + log_proc + is_ah_dual_listed",
    data=df.dropna(subset=["flip_day1_pct", "log_sub", "cornerstone_pct_of_offering", "log_proc"])
).fit(cov_type="HC3")
print("\nMacro-Micro Liquidity & Flipping Regressions:")
print("  1M HIBOR (%) -> log(Retail Sub Ratio): beta={:+.3f} (t_HC3={:+.2f}, p={:.4f}, R2={:.3f})".format(
    fit_hibor_sub.params["hibor_1m_pct"], fit_hibor_sub.tvalues["hibor_1m_pct"], fit_hibor_sub.pvalues["hibor_1m_pct"], fit_hibor_sub.rsquared
))
print("  Day-1 Flipping (%) Drivers (N={}, R2={:.3f}):".format(int(fit_flip.nobs), fit_flip.rsquared))
for k in ["log_sub", "cornerstone_pct_of_offering", "post_aug2025_prospectus", "is_ah_dual_listed"]:
    print("    {:30s}: {:+7.3f} | t_HC3={:+6.2f} (p={:.4f})".format(
        k, fit_flip.params[k], fit_flip.tvalues[k], fit_flip.pvalues[k]
    ))
