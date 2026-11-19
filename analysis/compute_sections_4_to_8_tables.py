import os
import pandas as pd
import numpy as np

OUT_DIR = "analysis/out/overview_1994_2026"
ord_df = pd.read_csv(os.path.join(OUT_DIR, "hkex_ordinary_ipos_market_1994_2026.csv"), low_memory=False)
cand_df = pd.read_csv(os.path.join(OUT_DIR, "hkex_all_candidates_1994_2026.csv"), low_memory=False)
panel226 = pd.read_csv(os.path.join(OUT_DIR, "hkipo_2025Q1_2026Q3_complete_226.csv"), low_memory=False)
master = pd.read_csv("pipeline/exports/HKIPO-MB-MASTER_clean.csv", low_memory=False)

def get_epoch(yr):
    if yr <= 2004: return "Epoch II (1994-2004)"
    elif yr <= 2017: return "Epoch III (2005-2017)"
    elif yr <= 2022: return "Epoch IV (2018-2022)"
    else: return "Epoch V (2023-2026)"

cand_df["epoch"] = cand_df["cohort_year"].apply(get_epoch)
wf = cand_df.groupby(["board", "epoch"]).agg(
    Total_Candidates=("stock_code", "count"),
    Excluded_Transfer=("exclusion_reason", lambda s: s.astype(str).str.contains("Transfer", na=False).sum()),
    Excluded_Intro=("exclusion_reason", lambda s: s.astype(str).str.contains("Introduction", na=False).sum()),
    Excluded_SPAC=("exclusion_reason", lambda s: s.astype(str).str.contains("SPAC", na=False).sum()),
    Included_Ordinary=("inclusion_status", lambda s: (s == "INCLUDED").sum())
).reset_index()
wf.to_csv(os.path.join(OUT_DIR, "table_sec3_waterfall_1994_2026.csv"), index=False)
print("=== SECTION 3: WATERFALL ===")
print(wf.to_string(index=False))

print("\n=== SECTION 4: ISSUER FUNDAMENTALS & OWNERSHIP IN 2025-2026 MASTER (N=202) ===")
master = master.copy()
master["rev_y1_m"] = pd.to_numeric(master["Net sales in year-1"], errors="coerce") / 1e6
master["pat_y1_m"] = pd.to_numeric(master["Profit for the year in year-1"], errors="coerce") / 1e6
master["assets_y1_m"] = pd.to_numeric(master["total assets in year-1"], errors="coerce") / 1e6
master["age"] = pd.to_numeric(master["Firm age at IPO (years)"], errors="coerce")
master["loss_making"] = (pd.to_numeric(master["Profit for the year in year-1"], errors="coerce") < 0).astype(float) * 100
master["vc_pe"] = pd.to_numeric(master["Pre-IPO VC/PE backing (1=yes; 0=no)"], errors="coerce") * 100
master["state_back"] = pd.to_numeric(master["Pre-IPO State/Gov backing (1=yes; 0=no)"], errors="coerce") * 100
master["rd_int"] = pd.to_numeric(master["rd_expense_intensity_y1"], errors="coerce") * 100
master["lev"] = pd.to_numeric(master["leverage_y1"], errors="coerce") * 100
master["ctrl_econ"] = pd.to_numeric(master["Controller economic interest at listing (%)"], errors="coerce")
master["ctrl_vote"] = pd.to_numeric(master["Controller voting rights at listing (%)"], errors="coerce")
if master["ctrl_econ"].median() <= 1.0:
    master["ctrl_econ"] *= 100
    master["ctrl_vote"] *= 100

print("Controller types:", master["Ultimate controller type"].value_counts(dropna=False).to_dict())
print("Place of incorporation:", master["Place of incorporation"].value_counts(dropna=False).head(8).to_dict())

# Categorize route
def get_route(r):
    if r.get("Chapter 18A flag") == 1: return "Chapter 18A Biotech"
    if r.get("Chapter 18C flag") == 1: return "Chapter 18C Specialist Tech"
    if r.get("A+H issuer flag") == 1: return "Chapter 19A A+H Dual-Listed"
    if r.get("WVR flag") == 1: return "Chapter 8A WVR (Conventional)"
    return "Main Board Conventional"

master["route_cat"] = master.apply(get_route, axis=1)
sec4_rows = []
for rt, grp in list(master.groupby("route_cat")) + [("All 2025-2026 Cohort (N=202)", master)]:
    sec4_rows.append({
        "Route": rt,
        "N": len(grp),
        "Age_Median_Yrs": round(grp["age"].median(), 1),
        "Rev_Y1_Median_m": round(grp["rev_y1_m"].median(), 1),
        "PAT_Y1_Median_m": round(grp["pat_y1_m"].median(), 1),
        "Assets_Y1_Median_m": round(grp["assets_y1_m"].median(), 1),
        "Loss_Making_Pct": round(grp["loss_making"].mean(), 1),
        "R_and_D_Intensity_Median_Pct": round(grp["rd_int"].median(), 1),
        "Leverage_Median_Pct": round(grp["lev"].median(), 1),
        "VC_PE_Backed_Pct": round(grp["vc_pe"].mean(), 1),
        "State_Backed_Pct": round(grp["state_back"].mean(), 1),
        "Ctrl_Voting_Median_Pct": round(grp["ctrl_vote"].median(), 1),
    })
df_sec4 = pd.DataFrame(sec4_rows)
df_sec4.to_csv(os.path.join(OUT_DIR, "table_sec4_issuer_fundamentals_by_route.csv"), index=False)
print(df_sec4.to_string(index=False))

print("\n=== SECTION 5: LISTING EXPENSES & UNDERWRITING SPREADS BY DEAL SIZE TIER (N=202) ===")
p0 = pd.to_numeric(master["IPO Subscription Price (HK$)"], errors="coerce")
sh_base = pd.to_numeric(master["Final global offering shares (before over-allotment)"], errors="coerce")
gross_from_sh = (p0 * sh_base) / 1e6
net_proc = pd.to_numeric(master["Net IPO proceeds to issuer (HK$)"], errors="coerce") / 1e6
list_exp = pd.to_numeric(master["Listing expenses (HK$)"], errors="coerce") / 1e6
gross_from_net = net_proc + list_exp
master["gross_proc_m"] = gross_from_sh.fillna(gross_from_net)
master["list_exp_m"] = list_exp
master["list_exp_pct"] = (master["list_exp_m"] / master["gross_proc_m"]) * 100
master.loc[(master["list_exp_pct"] <= 0) | (master["list_exp_pct"] > 50), "list_exp_pct"] = np.nan

uw_hk = pd.to_numeric(master["Underwriting Commission (% of fund raised HK (a)"], errors="coerce")
master["uw_hk_pct"] = np.where(uw_hk <= 1.0, uw_hk * 100, uw_hk)
master.loc[(master["uw_hk_pct"] <= 0) | (master["uw_hk_pct"] > 20), "uw_hk_pct"] = np.nan

uw_inc = pd.to_numeric(master["Underwriting discretionary incentive fee rate (%)"], errors="coerce")
master["uw_inc_pct"] = np.where(uw_inc <= 0.5, uw_inc * 100, uw_inc)

bins = [0, 250, 500, 1000, 3000, 1000000]
labels = ["< HK$250m", "HK$250m-500m", "HK$500m-1,000m", "HK$1,000m-3,000m", "> HK$3,000m"]
master["size_tier"] = pd.cut(master["gross_proc_m"], bins=bins, labels=labels)
sec5_rows = []
for st, grp in list(master.groupby("size_tier", observed=False)) + [("All Deals (N=202)", master)]:
    sec5_rows.append({
        "Deal_Size_Tier": str(st),
        "N": len(grp),
        "Median_Proceeds_HKDm": round(grp["gross_proc_m"].median(), 1),
        "Median_Listing_Expenses_HKDm": round(grp["list_exp_m"].median(), 1),
        "Total_Direct_Cost_Mean_Pct": round(grp["list_exp_pct"].mean(), 2),
        "Total_Direct_Cost_Median_Pct": round(grp["list_exp_pct"].median(), 2),
        "UW_Base_Spread_Mean_Pct": round(grp["uw_hk_pct"].mean(), 2),
        "UW_Base_Spread_Median_Pct": round(grp["uw_hk_pct"].median(), 2),
        "UW_Incentive_Mean_Pct": round(grp["uw_inc_pct"].mean(), 2),
        "Non_UW_Prof_Fees_Median_Pct": round((grp["list_exp_pct"] - grp["uw_hk_pct"]).median(), 2),
        "Mean_First_Day_IR_Pct": round(pd.to_numeric(grp["First-day return / Underpricing (%)"], errors="coerce").apply(lambda x: x*100 if abs(x)<10 else x).mean(), 2)
    })
df_sec5 = pd.DataFrame(sec5_rows)
df_sec5.to_csv(os.path.join(OUT_DIR, "table_sec5_direct_costs_by_size.csv"), index=False)
print(df_sec5.to_string(index=False))

print("\n=== SECTION 6: THREE-WAY RENT DECOMPOSITION IN 2025-2026 MASTER (N=202) ===")
master["mlot_m"] = pd.to_numeric(master["Money left on the table (HK$)"], errors="coerce") / 1e6
cs_raw = pd.to_numeric(master["Final cornerstone allocation (% of base offer)"], errors="coerce")
master["cs_share"] = np.where(cs_raw <= 1.0, cs_raw, cs_raw / 100.0)
master["pub_sh"] = pd.to_numeric(master["Final public offer shares"], errors="coerce")
master["tot_sh"] = pd.to_numeric(master["Final global offering shares (before over-allotment)"], errors="coerce")
master["pub_share"] = master["pub_sh"] / master["tot_sh"]
master["inst_free_share"] = (1.0 - master["pub_share"] - master["cs_share"].fillna(0)).clip(lower=0.0)

master["mlot_retail_m"] = master["mlot_m"] * master["pub_share"]
master["mlot_cs_m"] = master["mlot_m"] * master["cs_share"].fillna(0)
master["mlot_inst_m"] = master["mlot_m"] * master["inst_free_share"]

master["listing_dt"] = pd.to_datetime(master["Date of Listing (dd/mm/yy)"], format="mixed", dayfirst=True, errors="coerce")
master["post_aug2025"] = np.where(master["listing_dt"] >= pd.Timestamp("2025-08-04"), "Post-Aug 2025 Reform", "Pre-Aug 2025 (PN18)")

sec6_rows = []
for reg, grp in list(master.groupby("post_aug2025")) + [("Full 2025-2026 Sample", master)]:
    vm = grp.dropna(subset=["mlot_m", "pub_share"])
    pos = vm[vm["mlot_m"] > 0]
    sec6_rows.append({
        "Regime": reg,
        "N": len(vm),
        "Net_MLOT_HKDbn": round(vm["mlot_m"].sum() / 1e3, 2),
        "Gross_Positive_MLOT_HKDbn": round(pos["mlot_m"].sum() / 1e3, 2),
        "Retail_Share_of_Shares_Mean_Pct": round(vm["pub_share"].mean() * 100, 2),
        "Cornerstone_Share_of_Shares_Mean_Pct": round(vm["cs_share"].fillna(0).mean() * 100, 2),
        "Inst_Placee_Share_of_Shares_Mean_Pct": round(vm["inst_free_share"].mean() * 100, 2),
        "Retail_Captured_Net_MLOT_HKDbn": round(vm["mlot_retail_m"].sum() / 1e3, 2),
        "Retail_Captured_Share_Pct": round(vm["mlot_retail_m"].sum() / vm["mlot_m"].sum() * 100, 2),
        "Cornerstone_Paper_MLOT_HKDbn": round(vm["mlot_cs_m"].sum() / 1e3, 2),
        "Cornerstone_Captured_Share_Pct": round(vm["mlot_cs_m"].sum() / vm["mlot_m"].sum() * 100, 2),
        "Inst_Placee_Captured_MLOT_HKDbn": round(vm["mlot_inst_m"].sum() / 1e3, 2),
        "Inst_Placee_Captured_Share_Pct": round(vm["mlot_inst_m"].sum() / vm["mlot_m"].sum() * 100, 2),
    })
df_sec6 = pd.DataFrame(sec6_rows)
df_sec6.to_csv(os.path.join(OUT_DIR, "table_sec6_mlot_three_way_decomposition.csv"), index=False)
print(df_sec6.to_string(index=False))
