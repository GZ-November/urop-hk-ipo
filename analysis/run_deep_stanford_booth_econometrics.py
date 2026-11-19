import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

OUT_DIR = "/Users/georgezhu/Desktop/UROP HK IPO/analysis/out/overview_1994_2026"
m = pd.read_csv("/Users/georgezhu/Desktop/UROP HK IPO/pipeline/exports/HKIPO-MB-MASTER_clean.csv", low_memory=False)
m2865 = pd.read_csv(os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv"), low_memory=False)
t4_ballot = pd.read_csv(os.path.join(OUT_DIR, "table4_2026_all113_retail_ballot_returns.csv"))

# 1. Exact unit normalization on m (N=202)
for c in m.columns:
    if c not in [
        "cohort", "Stock Code", "Company Name at time of listing", "Date of Prospectus (dd/mm/yy)",
        "Date of Listing (dd/mm/yy)", "Sponsor(s)", "Reporting Accountants", "Valuer(s)",
        "currency in financial information", "Principal business / industry",
        "Listing route / applicable chapter", "Ultimate controller type", "Place of incorporation",
        "Principal place of business", "Offer mechanism", "Applicable IPO rules / transition basis",
        "Lead sponsor name"
    ]:
        m[c] = pd.to_numeric(m[c], errors="coerce")

m["gross_proceeds_hkd"] = m["Funds Raised HK (a)"].fillna(0) + m["Funds Raised Int.(b)"].fillna(0)
mask_zero = m["gross_proceeds_hkd"] <= 0
m.loc[mask_zero, "gross_proceeds_hkd"] = m.loc[mask_zero, "IPO Subscription Price (HK$)"] * m.loc[mask_zero, "Global Offering (without option)"]
m["proceeds_hkd_m"] = m["gross_proceeds_hkd"] / 1e6
m["log_proceeds_m"] = np.log(m["proceeds_hkd_m"])
m["mkt_cap_at_ipo_m"] = (m["IPO Subscription Price (HK$)"] * m["Total (without option)"]) / 1e6

# Convert decimal percentage columns (0.035 -> 3.5%)
m["uw_comm_hk_pct"] = m["Underwriting Commission (% of fund raised HK (a)"] * 100
m["uw_comm_int_pct"] = m["Underwriting Commission (% of fund raised Int.(b)"] * 100
m["uw_base_fee_pct"] = m["Underwriting base commission rate (%)"] * 100
m["uw_incentive_fee_pct"] = m["Underwriting discretionary incentive fee rate (%)"] * 100
m["uw_total_fee_pct"] = m["Total underwriting fee rate (%)"] * 100
# Effective gross spread: use uw_comm_int_pct (which has deal-by-deal variation) and uw_total_fee_pct
m["gross_spread_pct"] = m["uw_comm_int_pct"].combine_first(m["uw_comm_hk_pct"]).combine_first(m["uw_total_fee_pct"])
m["total_expense_pct"] = (m["Listing expenses (HK$)"] / m["gross_proceeds_hkd"]) * 100
m.loc[m["total_expense_pct"] > 60, "total_expense_pct"] = np.nan # guard against unit mismatch outliers
m["non_uw_expense_pct"] = (m["total_expense_pct"] - m["gross_spread_pct"]).clip(lower=0)

m["ir_pct"] = m["First-day return / Underpricing (%)"] * 100
m["log_ir"] = np.log1p(m["First-day return / Underpricing (%)"])
m["cornerstone_pct"] = m["Final cornerstone allocation (% of base offer)"].fillna(0) * 100
m["public_final_pct"] = m["public_offer_fraction"] * 100
m["free_float_pct"] = m["Unrestricted public shareholding at listing (%)"] * 100
m["range_width_pct"] = m["Filing range width (%)"] * 100
m["greenshoe_ex_pct"] = m["Over-allotment exercise percentage (%)"] * 100
m["flipping_pct"] = m["First-day flipping ratio (%)"] * 100
m["bhr_1m_pct"] = m["1-month BHR from Day-1 close (%)"] * 100
m["bhr_3m_pct"] = m["3-month BHR from Day-1 close (%)"] * 100
m["bhr_6m_pct"] = m["6-month BHR from Day-1 close (%)"] * 100
m["post_stab_cliff_pct"] = m["Post-stabilization cliff return [-5, +5] (%)"] * 100
m["post_stab_20d_pct"] = m["Post-stabilization 20-day return [0, +20] (%)"] * 100
m["unlock_car_5d_pct"] = m["Cornerstone unlock CAR [-5, +5] (%)"] * 100
m["unlock_car_20d_pct"] = m["Cornerstone unlock CAR [-20, +20] (%)"] * 100
m["hsi_20d_pre_pct"] = m["HSI return over 20 trading days before prospectus (%)"] * 100
m["roa_pct"] = m["roa_y1"] * 100
m["rd_int_pct"] = m["rd_expense_intensity_y1"] * 100
m["is_profitable"] = (m["Profit for the year in year-1"] > 0).astype(float)
m.loc[m["Profit for the year in year-1"].isna(), "is_profitable"] = np.nan

def classify_route(r):
    if r.get("A+H issuer flag") == 1:
        return "1. A+H Dual Listing"
    if r.get("Chapter 18A flag") == 1:
        return "2. Chapter 18A Biotech"
    if r.get("Chapter 18C flag") == 1:
        return "3. Chapter 18C Specialist Tech"
    if r.get("WVR flag") == 1:
        return "4. Chapter 8A WVR (Non-18A/18C)"
    return "5. Standard Main Board (Rule 8.05)"

m["route_group"] = m.apply(classify_route, axis=1)

print("=== TABLE A: ISSUER FUNDAMENTALS & GOVERNANCE BY LISTING ROUTE (N=202) ===")
tab_a = m.groupby("route_group").agg(
    N=("Stock Code", "size"),
    Mean_Proceeds_M=("proceeds_hkd_m", "mean"),
    Median_Proceeds_M=("proceeds_hkd_m", "median"),
    Median_MktCap_M=("mkt_cap_at_ipo_m", "median"),
    Mean_Age=("Firm age at IPO (years)", "mean"),
    Profitable_Pct=("is_profitable", lambda s: s.dropna().mean()*100),
    Median_ROA_Pct=("roa_pct", "median"),
    Median_RD_Int_Pct=("rd_int_pct", "median"),
    VC_PE_Pct=("Pre-IPO VC/PE backing (1=yes; 0=no)", lambda s: s.dropna().mean()*100),
    State_Backed_Pct=("Pre-IPO State/Gov backing (1=yes; 0=no)", lambda s: s.dropna().mean()*100),
    Mean_Cornerstone_Pct=("cornerstone_pct", "mean"),
    Mean_Gross_Spread_Pct=("gross_spread_pct", "mean"),
    Mean_Total_Exp_Pct=("total_expense_pct", "mean"),
    Mean_IR_Pct=("ir_pct", "mean"),
    Median_IR_Pct=("ir_pct", "median"),
).round(2)
print(tab_a.to_string())

print("\n=== TABLE B: DIRECT ISSUANCE COSTS & GROSS SPREAD BY DEAL SIZE QUARTILE ===")
m["proceeds_q"] = pd.qcut(m["proceeds_hkd_m"], 4, labels=["Q1 (Small: <HK$285m)", "Q2 (HK$285m-605m)", "Q3 (HK$605m-1,515m)", "Q4 (Large: >HK$1,515m)"])
tab_b = m.groupby("proceeds_q", observed=False).agg(
    N=("Stock Code", "size"),
    Median_Proceeds_M=("proceeds_hkd_m", "median"),
    Mean_Gross_Spread_Pct=("gross_spread_pct", "mean"),
    Median_Gross_Spread_Pct=("gross_spread_pct", "median"),
    Mean_Base_Comm_Pct=("uw_base_fee_pct", "mean"),
    Mean_Incentive_Pct=("uw_incentive_fee_pct", "mean"),
    Mean_NonUW_Cost_Pct=("non_uw_expense_pct", "mean"),
    Mean_Total_Direct_Cost_Pct=("total_expense_pct", "mean"),
    Median_Total_Direct_Cost_Pct=("total_expense_pct", "median"),
    Mean_Joint_Sponsors=("Joint sponsor count", "mean"),
).round(2)
print(tab_b.to_string())

sp = m["gross_spread_pct"].dropna()
print(f"\nGross Spread Distribution (N={len(sp)}): Mean={sp.mean():.2f}%, SD={sp.std():.2f}%, P10={sp.quantile(0.1):.2f}%, P25={sp.quantile(0.25):.2f}%, Median={sp.median():.2f}%, P75={sp.quantile(0.75):.2f}%, P90={sp.quantile(0.9):.2f}%")
print(f"Share exactly at 7.0% ([6.95%, 7.05%]): {((sp>=6.95)&(sp<=7.05)).mean()*100:.2f}% | Share < 4.0%: {(sp<4.0).mean()*100:.1f}%")

# OLS regression of Gross Spread and Total Expense Ratio
reg_cost_df = m.dropna(subset=["gross_spread_pct", "log_proceeds_m", "Firm age at IPO (years)", "Joint sponsor count"]).copy()
reg_cost_df["is_ah"] = reg_cost_df["A+H issuer flag"].fillna(0)
reg_cost_df["is_18a_18c"] = ((reg_cost_df["Chapter 18A flag"].fillna(0) == 1) | (reg_cost_df["Chapter 18C flag"].fillna(0) == 1)).astype(int)
reg_cost_df["is_state"] = reg_cost_df["Pre-IPO State/Gov backing (1=yes; 0=no)"].fillna(0)
mod_spread = smf.ols("gross_spread_pct ~ log_proceeds_m + is_ah + is_18a_18c + is_state + Q('Joint sponsor count')", data=reg_cost_df).fit(cov_type="HC3")
print("\nOLS Regression: Gross Underwriting Spread (%) [HC3 Robust SE]:")
for k in mod_spread.params.index:
    print(f"  {k:28s}: coef={mod_spread.params[k]:+.3f}, se={mod_spread.bse[k]:.3f}, t={mod_spread.tvalues[k]:+.2f}, p={mod_spread.pvalues[k]:.4f}")
print(f"  N = {int(mod_spread.nobs)}, R2 = {mod_spread.rsquared:.3f}, Adj R2 = {mod_spread.rsquared_adj:.3f}")

mod_totcost = smf.ols("total_expense_pct ~ log_proceeds_m + is_ah + is_18a_18c + is_state + Q('Joint sponsor count')", data=reg_cost_df.dropna(subset=["total_expense_pct"])).fit(cov_type="HC3")
print("\nOLS Regression: Total Direct Listing Expense (% of Proceeds) [HC3 Robust SE]:")
for k in mod_totcost.params.index:
    print(f"  {k:28s}: coef={mod_totcost.params[k]:+.3f}, se={mod_totcost.bse[k]:.3f}, t={mod_totcost.tvalues[k]:+.2f}, p={mod_totcost.pvalues[k]:.4f}")
print(f"  N = {int(mod_totcost.nobs)}, R2 = {mod_totcost.rsquared:.3f}, Adj R2 = {mod_totcost.rsquared_adj:.3f}")
