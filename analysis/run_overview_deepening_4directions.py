#!/usr/bin/env python3
"""
Four-Direction Empirical Deepening Suite for the 1994-2026 Hong Kong IPO Overview Monograph:
  Direction 1: Multivariate Cross-Sectional & Pre-Unlock Run-Up Regressions for the Day +180
               Two-Stage Statutory Lockup Natural Experiment (Cayman 6M vs. PRC H-Share 12M, N=58)
  Direction 2: Counterfactual Avoided Clawback Supply Shock (Delta_Clawback_Avoided) & High-Demand
               Difference-in-Differences Around the August 4, 2025 Mechanism A/B Reform (N=226)
  Direction 3: Bipartite Cornerstone Investor Network Degree Centrality (Repeat Hub Cornerstones
               vs. One-Off Relational Cornerstones) and Strictly Backward-Looking Sponsor Propensity
  Direction 4: Biais-Hillion-Spatt (1999) Opening Auction Unbiasedness Regressions (33-Year N=2,113
               and Modern N=226) & Intraday Price Discovery Across Statutory Allocation Regimes
"""

from __future__ import annotations

import re
import sys
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

BASE_DIR = Path("/Users/georgezhu/Desktop/UROP HK IPO")
if str(BASE_DIR / "analysis") not in sys.path:
    sys.path.insert(0, str(BASE_DIR / "analysis"))

from run_frontier_5modules_econometrics import canon_cs

OUT_MAIN = BASE_DIR / "analysis" / "out" / "overview_1994_2026"
OUT_EXT = BASE_DIR / "analysis" / "out" / "overview_extensions"


def canon_sponsor_from_col_h(raw: object) -> str:
    """Canonicalize lead sponsor directly from prospectus-verified Sponsor(s) (col_H)."""
    if pd.isna(raw) or not str(raw).strip():
        return "Other"
    first = str(raw).split("/")[0].replace("\n", " ").strip()
    u = first.upper()
    if "CHINA INTERNATIONAL CAPITAL" in u or "CICC" in u:
        return "CICC"
    if "CITIC" in u or "CLSA" in u:
        return "CITIC / CLSA"
    if "HUATAI" in u:
        return "Huatai International"
    if "MORGAN STANLEY" in u:
        return "Morgan Stanley"
    if "GOLDMAN SACHS" in u:
        return "Goldman Sachs"
    if "UBS" in u:
        return "UBS"
    if "J.P. MORGAN" in u or "JP MORGAN" in u:
        return "J.P. Morgan"
    if "MERRILL LYNCH" in u or "BAML" in u or "BOFA" in u:
        return "BofA Securities"
    if "CITIGROUP" in u or "CITI " in u:
        return "Citigroup"
    if "CMB INTERNATIONAL" in u or "CMBI" in u:
        return "CMB International"
    if "CMBC" in u:
        return "CMBC International"
    if "HAITONG" in u:
        return "Haitong International"
    if "GUOTAI JUNAN" in u:
        return "Guotai Junan"
    if "CHINA SECURITIES" in u or "CSC" in u:
        return "CSC Financial"
    if "CCB INTERNATIONAL" in u or "CCBI" in u:
        return "CCB International"
    if "ICBC" in u:
        return "ICBC International"
    if "SHENWAN" in u:
        return "Shenwan Hongyuan"
    if "CHINA MERCHANTS" in u or "CMS" in u:
        return "China Merchants Securities"
    if "SINOLINK" in u:
        return "Sinolink Securities"
    if "CEB " in u or "EVERBRIGHT" in u:
        return "China Everbright"
    if "ABC" in u and "INT" in u:
        return "ABC International"
    if "BOC" in u and "INT" in u:
        return "BOC International"
    if "DEUTSCHE" in u:
        return "Deutsche Bank"
    if "JEFFERIES" in u:
        return "Jefferies"
    if "PING AN" in u:
        return "Ping An Capital"
    return first[:35]


def load_panels() -> tuple[pd.DataFrame, pd.DataFrame]:
    m = pd.read_csv(BASE_DIR / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv", low_memory=False)
    m226 = pd.read_csv(OUT_MAIN / "clean_micro_panel_2025_2026_N226.csv", low_memory=False)
    cols_226 = [c for c in m226.columns if c not in m.columns and c != "stock_code"]
    df = m.merge(m226[["stock_code"] + cols_226], left_on="Stock Code", right_on="stock_code", how="left").copy()
    df33 = pd.read_csv(OUT_MAIN / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
    return df, df33


def run_direction1_unlock_multivariate(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 80)
    print("DIRECTION 1: Day +180 (N=123) & Paired 12M-6M (N=64) Lockup Multivariate Regressions")
    print("=" * 80)

    u = df[df["Cornerstone unlock CAR [-20, +20] (%)"].notna()].copy()
    u["car20_pct"] = pd.to_numeric(u["Cornerstone unlock CAR [-20, +20] (%)"], errors="coerce") * 100.0
    u["car5_pct"] = pd.to_numeric(u["Cornerstone unlock CAR [-5, +5] (%)"], errors="coerce") * 100.0
    u["cayman_6m_unlock"] = (u["is_prc_h_share"] == 0).astype(int)
    u["log_proc"] = np.log(pd.to_numeric(u["gross_proceeds_hkd_m"], errors="coerce"))
    u["cs_pct"] = pd.to_numeric(u["cornerstone_pct_of_offering"], errors="coerce").fillna(0.0)
    u["is_tech_18ac"] = ((u["is_18a"] == 1) | (u["is_18c"] == 1)).astype(int)
    u["bhr_3m_pct_val"] = pd.to_numeric(u["3-month BHR from Day-1 close (%)"], errors="coerce") * 100.0
    u["pre_ipo_inst_pct"] = pd.to_numeric(u["Pre-IPO institutional shareholding (%)"], errors="coerce")
    u["cayman_x_preipo_inst"] = u["cayman_6m_unlock"] * u["pre_ipo_inst_pct"]

    specs = [
        ("M1_Baseline_Univariate", ["cayman_6m_unlock"]),
        ("M2_Deal_and_Route_Controls", ["cayman_6m_unlock", "cs_pct", "log_proc", "is_ah_dual_listed", "is_tech_18ac"]),
        ("M3_Full_With_PreUnlock_Runup", ["cayman_6m_unlock", "cs_pct", "log_proc", "is_ah_dual_listed", "is_tech_18ac", "bhr_3m_pct_val"]),
        ("M4_PreIPO_Institutional_Interaction", ["cayman_6m_unlock", "cayman_x_preipo_inst", "pre_ipo_inst_pct", "cs_pct", "log_proc"]),
    ]

    rows = []
    for m_name, cols in specs:
        sub = u.dropna(subset=["car20_pct"] + cols).copy()
        X = sm.add_constant(sub[cols])
        fit = sm.OLS(sub["car20_pct"], X).fit(cov_type="HC3")
        for v in cols + ["const"]:
            rows.append({
                "Model": m_name,
                "Dep_Var": "Unlock_CAR_m20_p20_Pct",
                "Variable": v,
                "Coef_pp": round(float(fit.params[v]), 3),
                "SE_HC3": round(float(fit.bse[v]), 3),
                "t_HC3": round(float(fit.tvalues[v]), 2),
                "p_HC3": round(float(fit.pvalues[v]), 4),
                "N": len(sub),
                "R2": round(float(fit.rsquared), 4),
                "Adj_R2": round(float(fit.rsquared_adj), 4),
            })

    # M5: Paired Within-Firm 12M minus 6M Unlock CAR[-20, +20] (N=64 matured at both horizons)
    paired_csv = OUT_EXT / "clean_2025_2026_paired_6m_12m_lockup_panel.csv"
    if paired_csv.exists():
        p_raw = pd.read_csv(paired_csv)
        deal_ctrl = df[[
            "Stock Code", "is_prc_h_share", "cornerstone_pct_of_offering",
            "gross_proceeds_hkd_m", "is_ah_dual_listed", "is_18a", "is_18c"
        ]].drop_duplicates(subset=["Stock Code"])
        p_df = p_raw.merge(deal_ctrl, left_on="stock_code", right_on="Stock Code", how="left")
        p_df = p_df[p_df["car20_6m_bars"].notna() & p_df["car20_12m_bars"].notna()].copy()
        p_df["diff_12m_minus_6m_pct"] = (
            pd.to_numeric(p_df["car20_12m_bars"], errors="coerce")
            - pd.to_numeric(p_df["car20_6m_bars"], errors="coerce")
        ) * 100.0
        p_df["cayman_6m_unlock"] = (p_df["is_prc_h_share"] == 0).astype(int)
        p_df["cs_pct"] = pd.to_numeric(p_df["cornerstone_pct_of_offering"], errors="coerce").fillna(0.0)
        p_df["log_proc"] = np.log(pd.to_numeric(p_df["gross_proceeds_hkd_m"], errors="coerce"))
        p_df["is_tech_18ac"] = ((p_df["is_18a"] == 1) | (p_df["is_18c"] == 1)).astype(int)
        m5_cols = ["cayman_6m_unlock", "cs_pct", "log_proc", "is_ah_dual_listed", "is_tech_18ac"]
        sub5 = p_df.dropna(subset=["diff_12m_minus_6m_pct"] + m5_cols).copy()
        fit5 = sm.OLS(sub5["diff_12m_minus_6m_pct"], sm.add_constant(sub5[m5_cols])).fit(cov_type="HC3")
        for v in m5_cols + ["const"]:
            rows.append({
                "Model": "M5_Paired_Within_Firm_12M_minus_6M",
                "Dep_Var": "Paired_CAR20_12M_minus_6M_Pct",
                "Variable": v,
                "Coef_pp": round(float(fit5.params[v]), 3),
                "SE_HC3": round(float(fit5.bse[v]), 3),
                "t_HC3": round(float(fit5.tvalues[v]), 2),
                "p_HC3": round(float(fit5.pvalues[v]), 4),
                "N": len(sub5),
                "R2": round(float(fit5.rsquared), 4),
                "Adj_R2": round(float(fit5.rsquared_adj), 4),
            })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_MAIN / "table_14c_unlock_multivariate_controls_n123.csv", index=False)
    print(out.to_string(index=False))
    return out


def run_direction2_avoided_clawback_did(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 80)
    print("DIRECTION 2: Counterfactual Avoided Clawback Shock & Aug 2025 DiD (N=226)")
    print("=" * 80)

    d = df.copy()
    sub_x = pd.to_numeric(d["subscription_ratio_times"], errors="coerce")
    pn18_cf = np.where(
        sub_x >= 100.0, 50.0,
        np.where(sub_x >= 50.0, 40.0, np.where(sub_x >= 15.0, 30.0, 10.0))
    )
    pn18_cf = np.where(
        d["is_18c"] == 1,
        np.where(sub_x >= 50.0, 20.0, np.where(sub_x >= 10.0, 10.0, 5.0)),
        pn18_cf
    )
    d["pn18_counterfactual_public_pct"] = pn18_cf
    d["actual_final_public_pct"] = pd.to_numeric(d["public_offer_fraction_pct"], errors="coerce")
    d["avoided_clawback_pp"] = np.maximum(0.0, d["pn18_counterfactual_public_pct"] - d["actual_final_public_pct"])
    d["flip_pct"] = pd.to_numeric(d["First-day flipping ratio (%)"], errors="coerce") * 100.0
    d["log_ir"] = np.log1p(pd.to_numeric(d["initial_return_pct"], errors="coerce") / 100.0)
    d["log_sub"] = np.log1p(sub_x)
    d["log_proc"] = np.log(pd.to_numeric(d["gross_proceeds_hkd_m"], errors="coerce"))
    d["high_sub_100x"] = (sub_x >= 100.0).astype(int)
    d["post_x_high100"] = d["post_aug2025_prospectus"] * d["high_sub_100x"]
    d["listing_ym"] = pd.to_datetime(d["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    rows = []
    # 0. Strictly Pre-Determined Reform Effect (NO endogenous post-pricing oversubscription control)
    for dep_col, dep_label in [
        ("actual_final_public_pct", "Final_Public_Share_Pct"),
        ("flip_pct", "Day1_Flipping_Ratio_Pct"),
        ("log_ir", "Log_1_plus_Day1_IR"),
    ]:
        exog_pre = ["post_aug2025_prospectus", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]
        sub_d = d.dropna(subset=[dep_col, "listing_ym"] + exog_pre).copy()
        fit = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_pre])).fit(cov_type="HC3")
        fit_cl = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_pre])).fit(
            cov_type="cluster", cov_kwds={"groups": sub_d["listing_ym"]}
        )
        for v in ["post_aug2025_prospectus", "log_proc"]:
            rows.append({
                "Spec_Type": "PreDetermined_PostAug2025_NoDemandCtrl",
                "Dep_Var": dep_label,
                "Variable": v,
                "Coef": round(float(fit.params[v]), 4),
                "SE_HC3": round(float(fit.bse[v]), 4),
                "t_HC3": round(float(fit.tvalues[v]), 2),
                "p_HC3": round(float(fit.pvalues[v]), 4),
                "SE_MonthCluster": round(float(fit_cl.bse[v]), 4),
                "t_MonthCluster": round(float(fit_cl.tvalues[v]), 2),
                "p_MonthCluster": round(float(fit_cl.pvalues[v]), 4),
                "N": len(sub_d),
                "Clusters_YM": int(sub_d["listing_ym"].nunique()),
                "R2": round(float(fit.rsquared), 4),
            })

    # 1. DiD Specifications (Pre vs Post Aug 4, 2025 x High Demand >=100x)
    for dep_col, dep_label in [
        ("actual_final_public_pct", "Final_Public_Share_Pct"),
        ("flip_pct", "Day1_Flipping_Ratio_Pct"),
        ("log_ir", "Log_1_plus_Day1_IR"),
    ]:
        exog_did = ["post_aug2025_prospectus", "high_sub_100x", "post_x_high100", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]
        sub_d = d.dropna(subset=[dep_col, "listing_ym"] + exog_did).copy()
        fit = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_did])).fit(cov_type="HC3")
        fit_cl = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_did])).fit(
            cov_type="cluster", cov_kwds={"groups": sub_d["listing_ym"]}
        )
        for v in ["post_aug2025_prospectus", "high_sub_100x", "post_x_high100", "log_proc"]:
            rows.append({
                "Spec_Type": "DiD_PostAug2025_x_HighSub100x",
                "Dep_Var": dep_label,
                "Variable": v,
                "Coef": round(float(fit.params[v]), 4),
                "SE_HC3": round(float(fit.bse[v]), 4),
                "t_HC3": round(float(fit.tvalues[v]), 2),
                "p_HC3": round(float(fit.pvalues[v]), 4),
                "SE_MonthCluster": round(float(fit_cl.bse[v]), 4),
                "t_MonthCluster": round(float(fit_cl.tvalues[v]), 2),
                "p_MonthCluster": round(float(fit_cl.pvalues[v]), 4),
                "N": len(sub_d),
                "Clusters_YM": int(sub_d["listing_ym"].nunique()),
                "R2": round(float(fit.rsquared), 4),
            })

    # 2. Continuous Dose-Response on Counterfactual Avoided Clawback (avoided_clawback_pp)
    for dep_col, dep_label in [
        ("flip_pct", "Day1_Flipping_Ratio_Pct"),
        ("log_ir", "Log_1_plus_Day1_IR"),
    ]:
        exog_cf = ["avoided_clawback_pp", "log_sub", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]
        sub_d = d.dropna(subset=[dep_col, "listing_ym"] + exog_cf).copy()
        fit = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_cf])).fit(cov_type="HC3")
        fit_cl = sm.OLS(sub_d[dep_col], sm.add_constant(sub_d[exog_cf])).fit(
            cov_type="cluster", cov_kwds={"groups": sub_d["listing_ym"]}
        )
        for v in ["avoided_clawback_pp", "log_sub", "log_proc"]:
            rows.append({
                "Spec_Type": "DoseResponse_Avoided_Clawback_pp",
                "Dep_Var": dep_label,
                "Variable": v,
                "Coef": round(float(fit.params[v]), 4),
                "SE_HC3": round(float(fit.bse[v]), 4),
                "t_HC3": round(float(fit.tvalues[v]), 2),
                "p_HC3": round(float(fit.pvalues[v]), 4),
                "SE_MonthCluster": round(float(fit_cl.bse[v]), 4),
                "t_MonthCluster": round(float(fit_cl.tvalues[v]), 2),
                "p_MonthCluster": round(float(fit_cl.pvalues[v]), 4),
                "N": len(sub_d),
                "Clusters_YM": int(sub_d["listing_ym"].nunique()),
                "R2": round(float(fit.rsquared), 4),
            })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_MAIN / "table_9f_avoided_clawback_shock_did_n226.csv", index=False)
    print(out.to_string(index=False))
    return out


def run_direction3_repeat_cornerstone_network(df: pd.DataFrame, df33: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 80)
    print("DIRECTION 3: Bipartite Cornerstone Network Centrality & Pre-Determined Sponsor IV")
    print("=" * 80)

    d = df.copy()

    def parse_cs_list(raw: object) -> list[str]:
        if pd.isna(raw) or str(raw).strip() in ("", "0", "None", "N/A", "nan"):
            return []
        parts = [
            canon_cs(p) for p in re.split(r"[;\n,]", str(raw))
            if len(p.strip()) > 3 and p.strip().upper() not in ("LTD.", "LIMITED", "L.P.", "INC.", "CORP.")
        ]
        return list(dict.fromkeys([p for p in parts if len(p) > 2]))

    d["cs_list"] = d["Cornerstone investor names"].apply(parse_cs_list)
    all_cs_counts = Counter([e for lst in d["cs_list"] for e in lst])
    d["max_cs_degree"] = d["cs_list"].apply(lambda lst: max([all_cs_counts[e] for e in lst]) if lst else 0)
    d["repeat_hub_cs_count"] = d["cs_list"].apply(lambda lst: sum(1 for e in lst if all_cs_counts[e] >= 3))
    d["has_repeat_hub_cs"] = (d["repeat_hub_cs_count"] >= 1).astype(int)
    d["cs_pct"] = pd.to_numeric(d["cornerstone_pct_of_offering"], errors="coerce").fillna(0.0)
    d["one_off_cs_only"] = ((d["cs_pct"] > 0) & (d["has_repeat_hub_cs"] == 0)).astype(int)
    d["car20"] = pd.to_numeric(d["Cornerstone unlock CAR [-20, +20] (%)"], errors="coerce") * 100.0
    d["bhr_6m"] = pd.to_numeric(d["bhr_6m_pct"], errors="coerce")

    # Strictly pre-determined sponsor cornerstone propensity (listing_date < prospectus_date_i), seeded with 2018-2024 Main Board deals
    hist_mb = df33[(df33["board"] == "Main Board") & (df33["cohort_year"].between(2018, 2024))].copy()
    hist_sp_col = hist_mb["col_H"] if "col_H" in hist_mb.columns else hist_mb["lead_sponsor"]
    hist_mb["true_lead_sp"] = hist_sp_col.fillna(hist_mb["lead_sponsor"]).apply(canon_sponsor_from_col_h)
    hist_mb["list_dt"] = pd.to_datetime(hist_mb["listing_date"], errors="coerce")
    cs_hist_col = "ext_cornerstone_pct" if "ext_cornerstone_pct" in hist_mb.columns else "ext_cornerstone_shares"
    hist_mb["cs_pct"] = pd.to_numeric(hist_mb[cs_hist_col], errors="coerce")
    hist_seed = hist_mb[["true_lead_sp", "list_dt", "cs_pct"]].dropna(subset=["list_dt", "cs_pct"])

    d["true_lead_sp"] = d["Sponsor(s)"].apply(canon_sponsor_from_col_h)
    d["list_dt"] = pd.to_datetime(d["listing_date"], errors="coerce")
    d["pros_dt"] = pd.to_datetime(d.get("prospectus_date"), errors="coerce")
    d = d.sort_values("list_dt").reset_index(drop=True)

    all_seed = pd.concat([hist_seed, d[["true_lead_sp", "list_dt", "cs_pct"]]], ignore_index=True)
    z_backward = []
    for _, row in d.iterrows():
        cutoff_dt = row["pros_dt"] if pd.notna(row["pros_dt"]) else row["list_dt"]
        prior = all_seed[all_seed["list_dt"] < cutoff_dt]
        sp_prior = prior[prior["true_lead_sp"] == row["true_lead_sp"]]
        if len(sp_prior) >= 2:
            z_backward.append(float(sp_prior["cs_pct"].mean()))
        elif len(prior) >= 1:
            z_backward.append(float(prior["cs_pct"].mean()))
        else:
            z_backward.append(float(d["cs_pct"].mean()))
    d["z_sp_cs_backward"] = z_backward

    rows = []
    for label, grp in [
        ("1. Repeat Hub Cornerstone Backed (Degree >= 3 IPOs)", d[d["has_repeat_hub_cs"] == 1]),
        ("2. One-Off / Low-Degree Cornerstone Only (Degree 1-2)", d[d["one_off_cs_only"] == 1]),
        ("3. Zero Cornerstone Tranche (0% Cornerstone)", d[d["cs_pct"] == 0]),
    ]:
        ir = grp["initial_return_pct"].dropna()
        sub = grp["subscription_ratio_times"].dropna()
        c20 = grp["car20"].dropna()
        b6 = grp["bhr_6m"].dropna()
        rows.append({
            "Network_Tier": label,
            "N_Deals": len(grp),
            "Mean_CS_Share_Pct": round(float(grp["cs_pct"].mean()), 2),
            "Mean_Repeat_Hub_CS_Count": round(float(grp["repeat_hub_cs_count"].mean()), 2),
            "Mean_Max_CS_Degree": round(float(grp["max_cs_degree"].mean()), 1),
            "Median_Retail_Sub_x": round(float(sub.median()), 1),
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 2),
            "Mean_Unlock_CAR20_Pct": round(float(c20.mean()), 2) if len(c20) > 0 else np.nan,
            "Unlock_N": len(c20),
            "Mean_6M_BHR_Pct": round(float(b6.mean()), 2) if len(b6) > 0 else np.nan,
            "Matured_6M_N": len(b6),
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_EXT / "ext_table16c_repeat_cornerstone_network_centrality.csv", index=False)
    print(out.to_string(index=False))
    return out


def run_direction4_opening_auction_and_intraday(df: pd.DataFrame, df33: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 80)
    print("DIRECTION 4: Opening Auction Unbiasedness & Intraday Price Discovery Regimes")
    print("=" * 80)

    d = df.copy()
    p0 = pd.to_numeric(d["IPO Subscription Price (HK$)"], errors="coerce")
    p_open = pd.to_numeric(d["First trading day opening price (HK$)"], errors="coerce")
    p_high = pd.to_numeric(d["First trading day high (HK$)"], errors="coerce")
    p_low = pd.to_numeric(d["First trading day low (HK$)"], errors="coerce")
    p_close = pd.to_numeric(d["First trading day closing price (HK$)"], errors="coerce")

    d["r_open_pct"] = (p_open / p0 - 1.0) * 100.0
    d["r_close_pct"] = (p_close / p0 - 1.0) * 100.0
    d["r_intraday_pct"] = (p_close / p_open - 1.0) * 100.0
    d["intraday_range_pct"] = ((p_high - p_low) / p_open) * 100.0
    d["bhr_d5_pct"] = pd.to_numeric(d["Day-5 BHR from Day-1 close (%)"], errors="coerce") * 100.0
    d["flip_pct"] = pd.to_numeric(d["First-day flipping ratio (%)"], errors="coerce") * 100.0

    clean33 = df33[
        (df33["flag_reverse_split_distortion"] == 0)
        & (df33["flag_recycled_or_transferred_ticker"] == 0)
    ].copy()

    rows = []
    # Panel A: Unbiasedness Regressions (R_close = alpha + beta * R_open)
    for sample_name, sub_u, open_col, close_col in [
        ("Panel A1: 33-Year Main Board Clean Population (1994-2026)", clean33[clean33["board"] == "Main Board"], "ir_open_pct", "ir_close_pct"),
        ("Panel A2: 33-Year GEM Clean Population (1999-2026)", clean33[clean33["board"] == "GEM"], "ir_open_pct", "ir_close_pct"),
        ("Panel A3: Modern 2025-2026 Main Board Panel (N=226)", d, "r_open_pct", "r_close_pct"),
    ]:
        u_sub = sub_u.dropna(subset=[open_col, close_col]).copy()
        u_sub = u_sub[u_sub[open_col] > -99.9].copy()
        fit = sm.OLS(u_sub[close_col], sm.add_constant(u_sub[open_col])).fit(cov_type="HC3")
        b1 = float(fit.params[open_col])
        se1 = float(fit.bse[open_col])
        t_vs_1 = (b1 - 1.0) / se1
        intra_s = ((1.0 + u_sub[close_col] / 100.0) / (1.0 + u_sub[open_col] / 100.0) - 1.0) * 100.0
        rows.append({
            "Panel_and_Regime": sample_name,
            "N": len(u_sub),
            "Mean_Open_IR_Pct": round(float(u_sub[open_col].mean()), 2),
            "Mean_Close_IR_Pct": round(float(u_sub[close_col].mean()), 2),
            "Mean_Intraday_Drift_Pct": round(float(intra_s.mean()), 2),
            "Median_Intraday_Drift_Pct": round(float(intra_s.median()), 2),
            "Unbiased_Beta_Ropen": round(b1, 4),
            "SE_HC3_Beta": round(se1, 4),
            "t_Test_Beta_eq_1": round(t_vs_1, 2),
            "R2_Open_Explains_Close": round(float(fit.rsquared), 4),
            "Mean_Intraday_Range_Pct": np.nan,
            "Mean_Flipping_Ratio_Pct": np.nan,
            "Mean_Day5_Aftermarket_BHR_Pct": np.nan,
        })

    # Panel B: Modern 2025-2026 Intraday Price Discovery Across Statutory Allocation Regimes
    for reg_lbl, sub_g in [
        ("Panel B1: Legacy PN18 (Pre-Aug 4, 2025; Compulsory Clawback to 50%)", d[d["alloc_regime_actual"] == "Legacy_PN18"]),
        ("Panel B2: Mechanism A (Post-Aug 4, 2025; Clawback 5% -> 35%)", d[d["alloc_regime_actual"] == "Mechanism_A"]),
        ("Panel B3: Mechanism B (Post-Aug 4, 2025; Fixed ~10% Retail, Zero Clawback)", d[d["alloc_regime_actual"] == "Mechanism_B"]),
        ("Panel B4: Ch. 18C Specialist Tech (Rule 18C.09; Capped 5% -> 20% Clawback)", d[d["alloc_regime_actual"] == "Ch18C_Special"]),
    ]:
        fit_g = sm.OLS(sub_g["r_close_pct"], sm.add_constant(sub_g["r_open_pct"])).fit(cov_type="HC3") if len(sub_g) >= 8 else None
        b1_g = float(fit_g.params["r_open_pct"]) if fit_g is not None else np.nan
        se1_g = float(fit_g.bse["r_open_pct"]) if fit_g is not None else np.nan
        rows.append({
            "Panel_and_Regime": reg_lbl,
            "N": len(sub_g),
            "Mean_Open_IR_Pct": round(float(sub_g["r_open_pct"].mean()), 2),
            "Mean_Close_IR_Pct": round(float(sub_g["r_close_pct"].mean()), 2),
            "Mean_Intraday_Drift_Pct": round(float(sub_g["r_intraday_pct"].mean()), 2),
            "Median_Intraday_Drift_Pct": round(float(sub_g["r_intraday_pct"].median()), 2),
            "Unbiased_Beta_Ropen": round(b1_g, 4) if pd.notna(b1_g) else np.nan,
            "SE_HC3_Beta": round(se1_g, 4) if pd.notna(se1_g) else np.nan,
            "t_Test_Beta_eq_1": round((b1_g - 1.0) / se1_g, 2) if pd.notna(b1_g) and se1_g > 0 else np.nan,
            "R2_Open_Explains_Close": round(float(fit_g.rsquared), 4) if fit_g is not None else np.nan,
            "Mean_Intraday_Range_Pct": round(float(sub_g["intraday_range_pct"].mean()), 2),
            "Mean_Flipping_Ratio_Pct": round(float(sub_g["flip_pct"].mean()), 2),
            "Mean_Day5_Aftermarket_BHR_Pct": round(float(sub_g["bhr_d5_pct"].mean()), 2),
        })

    out = pd.DataFrame(rows)
    out.to_csv(OUT_MAIN / "table_9a2_opening_auction_unbiasedness_and_intraday_regimes.csv", index=False)
    print(out.to_string(index=False))
    return out


def main() -> None:
    df, df33 = load_panels()
    run_direction1_unlock_multivariate(df)
    run_direction2_avoided_clawback_did(df)
    run_direction3_repeat_cornerstone_network(df, df33)
    run_direction4_opening_auction_and_intraday(df, df33)
    print("\nALL 4 DEEPENING EMPIRICAL DIRECTIONS COMPLETED AND SAVED.")


if __name__ == "__main__":
    main()
