#!/usr/bin/env python3
"""
update_manuscript_33y_and_n226_tables.py
========================================
Author: Overview Manuscript & Econometrics Integration Engineer
Project: UROP HK IPO Empirical Research Infrastructure
Date: November 2026

Purpose:
1. Computes Table 6A2 (33-Year Statutory Filing Domicile, Primary Share Capital Formation,
   Statutory Pricing Structures, and Pre-IPO Financial Fundamentals) from
   analysis/out/overview_1994_2026/hkipo_33y_master_panel_1994_2026_tier1_complete.csv (N=2,866)
   and pipeline/exports/HKIPO-MB-MASTER_clean.csv (N=226).
2. Computes Table 9C (Practice Note 18 Clawback First-Stage Supply Expansion, Local Linear
   RD Jumps, and Fuzzy RD / 2SLS Verification) across the statutory 1998-2025.07 Main Board era (N=1,529).
3. Re-runs Table 2D (Panel A quartiles & Panel B OLS cost regressions), Table 6B (Issuer Fundamentals
   by Route), Table 13 (Greenshoe Exercise Regimes), and Table 15B Panel B (IAS 38 / Rule 8.05 bunchers)
   on the full N=226 modern dataset.
4. Audits Policy Valve maxlags, Ritter Table 10 moderate-size benchmark cases, and stale text occurrences.
"""

import bisect
import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.formula.api as smf

REPO_ROOT = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
OUT_DIR.mkdir(parents=True, exist_ok=True)

MASTER_33Y_CSV = OUT_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
CLEAN_226_CSV = REPO_ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"

TABLE_6A2_CSV = OUT_DIR / "table6a2_33y_filing_domicile_pricing_fundamentals.csv"
TABLE_9C_CSV = OUT_DIR / "table9c_pn18_firststage_and_2sls_filing_verified.csv"
TABLE_2D_CSV = OUT_DIR / "table_2d_n226_cost_anatomy_and_regressions.csv"
TABLE_6B_CSV = OUT_DIR / "table_sec4_issuer_fundamentals_by_route.csv"
TABLE_13_CSV = OUT_DIR / "table_13_greenshoe_regimes_n226.csv"
TABLE_15B_CSV = OUT_DIR / "table_15b_r805_bunchers_n226.csv"
MICRO_226_CSV = OUT_DIR / "clean_micro_panel_2025_2026_N226.csv"


def main():
    print("=" * 80)
    print("STARTING MANUSCRIPT 33-YEAR & N=226 TABLE RECOMPUTATION & AUDIT")
    print("=" * 80)

    # 1. Load Data
    print(f"Loading 33-year master panel: {MASTER_33Y_CSV}")
    df33 = pd.read_csv(MASTER_33Y_CSV, low_memory=False)
    print(f"  Shape: {df33.shape} (Expected 2,866 rows)")

    print(f"Loading N=226 clean modern panel: {CLEAN_226_CSV}")
    df226 = pd.read_csv(CLEAN_226_CSV, low_memory=False)
    print(f"  Shape: {df226.shape} (Expected 226 rows)")
    assert len(df226) == 226, f"Expected 226 rows, got {len(df226)}"

    mic = pd.read_csv(MICRO_226_CSV, low_memory=False)
    mic_map = mic.set_index("stock_code").to_dict("index")

    # 2. Table 6A2: 33-Year Filing-Verified Population Analytics
    print("\n" + "=" * 60)
    print("1. COMPUTING TABLE 6A2: 33-YEAR POPULATION ANALYTICS")
    print("=" * 60)

    def get_epoch_label(r):
        if r["board"] == "GEM":
            return "GEM All (1999-2026Q3)"
        y = r["cohort_year"]
        if y <= 2004:
            return "Epoch II (1994-2004)"
        elif y <= 2017:
            return "Epoch III (2005-2017)"
        elif y <= 2022:
            return "Epoch IV (2018-2022)"
        else:
            return "Epoch V (2023-2026Q3)"

    df33["manuscript_epoch"] = df33.apply(get_epoch_label, axis=1)

    p_hi_all = pd.to_numeric(df33["col_T"], errors="coerce")
    p_lo_all = pd.to_numeric(df33["col_U"], errors="coerce")
    p_off_all = pd.to_numeric(df33["offer_price_hkd"], errors="coerce")

    def get_p_cat(idx, r):
        sc = r["stock_code"]
        if sc in mic_map and r["cohort_year"] >= 2025:
            ps = str(mic_map[sc].get("pricing_structure", ""))
            if "Fixed" in ps:
                return "Fixed"
            if "Cap_Only" in ps:
                return "Cap_Waiver"
            return "Range"
        hi, lo = p_hi_all.loc[idx], p_lo_all.loc[idx]
        if pd.notna(hi) and pd.notna(lo):
            return "Fixed" if np.isclose(hi, lo, atol=1e-4) else "Range"
        return np.nan

    df33["p_cat_verified"] = [get_p_cat(i, r) for i, r in df33.iterrows()]

    col_s_all = pd.to_numeric(df33["col_S"], errors="coerce")
    col_ct_all = pd.to_numeric(df33["col_CT"], errors="coerce")
    col_m_all = pd.to_numeric(df33["col_M"], errors="coerce")
    # For Main Board IPOs prior to 2002 (physical/early NLR summaries), legacy SEHK New Listing Reports
    # pooled placing + public offer proceeds into col_S / col_CT without separate tranche splits.
    # Restrict Main Board retail tranche share statistics to 2002-2026Q3 digital prospectus-verified cohorts.
    tranche_verified_mask = (df33["board"] != "Main Board") | (df33["cohort_year"] >= 2002)
    df33["init_ret_pct"] = np.where(
        tranche_verified_mask & (col_m_all > 0) & (col_s_all >= 0) & (col_s_all <= col_m_all * 1.05),
        np.clip(col_s_all / col_m_all * 100.0, 0.0, 100.0),
        np.nan,
    )
    df33["final_ret_pct"] = np.where(
        tranche_verified_mask & (col_m_all > 0) & (col_ct_all >= 0) & (col_ct_all <= col_m_all * 1.05),
        np.clip(col_ct_all / col_m_all * 100.0, 0.0, 100.0),
        np.nan,
    )

    epochs = [
        "Epoch II (1994-2004)",
        "Epoch III (2005-2017)",
        "Epoch IV (2018-2022)",
        "Epoch V (2023-2026Q3)",
        "Main Board All (1994-2026Q3)",
        "GEM All (1999-2026Q3)",
    ]

    t6a2_rows = []
    for ep in epochs:
        if ep == "Main Board All (1994-2026Q3)":
            sub = df33[df33["board"] == "Main Board"]
        elif ep == "GEM All (1999-2026Q3)":
            sub = df33[df33["board"] == "GEM"]
        else:
            sub = df33[df33["manuscript_epoch"] == ep]

        n_tot = len(sub)
        dom_valid = sub.loc[
            sub["ext_domicile"].notna() & (sub["ext_domicile"].astype(str).str.upper() != "UNKNOWN"),
            "ext_domicile",
        ]
        dv = dom_valid.value_counts(normalize=True) * 100.0
        hk_pct = dv.get("Hong Kong", 0.0)
        bmd_pct = dv.get("Bermuda", 0.0)
        cay_pct = dv.get("Cayman Islands", 0.0)
        prc_pct = dv.get("PRC", 0.0)
        oth_pct = max(0.0, 100.0 - (hk_pct + bmd_pct + cay_pct + prc_pct))

        p_sec = pd.to_numeric(sub["col_P"], errors="coerce")
        q_pri = pd.to_numeric(sub["col_Q"], errors="coerce")
        m_tot = pd.to_numeric(sub["col_M"], errors="coerce")
        valid_pq = p_sec.notna() & q_pri.notna() & (m_tot > 0)
        pure_pri_pct = (p_sec[valid_pq] == 0).mean() * 100.0
        pri_share_pct = (q_pri[valid_pq] / m_tot[valid_pq] * 100.0).mean()
        bbg_sec_pct = sub["bbg_first_selling_stockholder_raw"].notna().mean() * 100.0

        pcat = sub["p_cat_verified"].dropna()
        fix_sh = (pcat == "Fixed").mean() * 100.0
        rng_sh = (pcat != "Fixed").mean() * 100.0

        hi_s, lo_s, off_s = p_hi_all.loc[sub.index], p_lo_all.loc[sub.index], p_off_all.loc[sub.index]
        bv = hi_s.notna() & lo_s.notna() & off_s.notna()
        bound_rate = ((lo_s[bv] - 0.05 <= off_s[bv]) & (off_s[bv] <= hi_s[bv] + 0.05)).mean() * 100.0

        init_r = sub["init_ret_pct"].dropna().mean()
        fin_r = sub["final_ret_pct"].dropna().mean()

        t6a2_rows.append({
            "Epoch": ep,
            "N": n_tot,
            "Dom_N": len(dom_valid),
            "HK_Pct": round(hk_pct, 1),
            "Bermuda_Pct": round(bmd_pct, 1),
            "Cayman_Pct": round(cay_pct, 1),
            "PRC_Pct": round(prc_pct, 1),
            "Other_Pct": round(oth_pct, 1),
            "Pure_Primary_Pct": round(pure_pri_pct, 1),
            "Mean_Primary_Share_Pct": round(pri_share_pct, 1),
            "BBG_Selling_Holder_Flag_Pct": round(bbg_sec_pct, 1),
            "Price_Verified_N": len(pcat),
            "Fixed_Price_Pct": round(fix_sh, 1),
            "Bookbuilding_Range_or_Cap_Pct": round(rng_sh, 1),
            "Price_Bounded_Rate_Pct": round(bound_rate, 1),
            "Retail_Tranche_Verified_N": int(sub["final_ret_pct"].notna().sum()),
            "Mean_Init_Retail_Pct": round(init_r, 1),
            "Mean_Final_Retail_Pct": round(fin_r, 1),
        })

    df_t6a2 = pd.DataFrame(t6a2_rows)
    df_t6a2.to_csv(TABLE_6A2_CSV, index=False)
    print(df_t6a2.to_string(index=False))
    print(f"Saved Table 6A2 to: {TABLE_6A2_CSV}")

    # 3. Table 9C: PN18 First-Stage & Fuzzy RD / 2SLS Verification
    print("\n" + "=" * 60)
    print("2. COMPUTING TABLE 9C: PN18 CLAWBACK FIRST-STAGE & 2SLS")
    print("=" * 60)

    df33["listing_dt"] = pd.to_datetime(df33["listing_date"])
    pn18_sub = df33[
        (df33["board"] == "Main Board") &
        (df33["listing_dt"] >= "1998-06-22") &
        (df33["listing_dt"] < "2025-08-04") &
        (df33["retail_sub_ratio_clean"].notna()) &
        (df33["pn18_allocation_sample"] == 1)
    ].copy()

    print(f"PN18 statutory sample size: N = {len(pn18_sub)}")

    col_s = pd.to_numeric(pn18_sub["col_S"], errors="coerce")
    col_ct = pd.to_numeric(pn18_sub["col_CT"], errors="coerce")
    col_m = pd.to_numeric(pn18_sub["col_M"], errors="coerce")

    pn18_sub["init_pub_pct"] = np.clip(col_s / col_m * 100.0, 0.0, 100.0)
    pn18_sub["final_pub_pct"] = np.clip(col_ct / col_m * 100.0, 0.0, 100.0)
    pn18_sub["log_ir"] = np.log1p(np.maximum(pd.to_numeric(pn18_sub["ir_close_pct"], errors="coerce") / 100.0, -0.99))

    def pn18_tier(x):
        if x < 15:
            return "1. <15x (10% Public, No Clawback)"
        if x < 50:
            return "2. 15x-50x (30% Clawback)"
        if x < 100:
            return "3. 50x-100x (40% Clawback)"
        return "4. >=100x (50% Max Clawback)"

    pn18_sub["clawback_bracket"] = pn18_sub["retail_sub_ratio_clean"].apply(pn18_tier)

    # Panel A: Bracket summary
    p18_bracket_rows = []
    for brk, grp in pn18_sub.groupby("clawback_bracket"):
        p18_bracket_rows.append({
            "Clawback_Bracket": brk,
            "N": len(grp),
            "Median_Sub_x": round(float(grp["retail_sub_ratio_clean"].median()), 2),
            "Initial_Public_Share_Mean_Pct": round(float(grp["init_pub_pct"].mean()), 2),
            "Initial_Public_Share_Median_Pct": round(float(grp["init_pub_pct"].median()), 2),
            "Final_Public_Share_Mean_Pct": round(float(grp["final_pub_pct"].mean()), 2),
            "Final_Public_Share_Median_Pct": round(float(grp["final_pub_pct"].median()), 2),
            "Mean_Day1_IR_Pct": round(float(grp["ir_close_pct"].mean()), 2),
            "Median_Day1_IR_Pct": round(float(grp["ir_close_pct"].median()), 2)
        })

    # Compute pre-IPO 30-trading-day HSI return for covariate balance checks
    hsi_path = OUT_DIR / "market_cache" / "hkHSI_1994_2026.json"
    hsi_map = json.loads(hsi_path.read_text()) if hsi_path.exists() else {}
    hsi_dates = sorted(hsi_map.keys())

    def _pre30_hsi(ld_s: object) -> float:
        ds = str(ld_s)[:10]
        idx = bisect.bisect_left(hsi_dates, ds) - 1
        if idx < 30:
            return np.nan
        p1, p0 = hsi_map[hsi_dates[idx]], hsi_map[hsi_dates[idx - 30]]
        return (p1 / p0 - 1.0) * 100.0 if (p0 and p0 > 0) else np.nan

    pn18_sub["hsi_ret_pre30td_pct"] = pn18_sub["listing_date"].apply(_pre30_hsi)
    pn18_sub["log_proceeds"] = np.log(np.maximum(pd.to_numeric(pn18_sub["funds_raised_total_hkd"], errors="coerce") / 1e6, 1e-3))
    pn18_sub["has_cornerstone"] = pd.to_numeric(pn18_sub["ext_has_cornerstone"], errors="coerce").fillna(0.0)
    pn18_clean = pn18_sub.dropna(subset=["final_pub_pct", "log_ir", "retail_sub_ratio_clean"]).copy()

    # Panel B: RD Jumps and 2SLS across cutoffs and bandwidth grid [0.35, 0.45, 0.55, 0.65, 0.85] + Quadratic
    rd_rows = []
    for cutoff in [15.0, 50.0, 100.0]:
        z = np.log(np.maximum(pn18_clean["retail_sub_ratio_clean"], 0.01)) - np.log(cutoff)
        spec_list = [(bw_val, "Linear") for bw_val in [0.35, 0.45, 0.55, 0.65, 0.85]] + [(0.65, "Quadratic")]
        for bw_val, poly in spec_list:
            sub = pn18_clean[np.abs(z) <= bw_val].copy()
            sub["z"] = z[np.abs(z) <= bw_val]
            sub["z2"] = sub["z"] ** 2
            sub["above"] = (sub["retail_sub_ratio_clean"] >= cutoff).astype(int)

            rhs = "above * z" if poly == "Linear" else "above * z + above * z2"
            fs = smf.ols(f"final_pub_pct ~ {rhs}", data=sub).fit(cov_type="HC3")
            fs_jump = fs.params["above"]
            fs_t = fs.tvalues["above"]
            fs_p = fs.pvalues["above"]

            rf = smf.ols(f"log_ir ~ {rhs}", data=sub).fit(cov_type="HC3")
            rf_jump = rf.params["above"]
            rf_t = rf.tvalues["above"]
            rf_p = rf.pvalues["above"]

            # 2SLS estimate with structural residuals u = y - X_actual @ beta_2sls (proper HC3 2SLS covariance)
            sub["p_hat"] = fs.fittedvalues
            sub["az"] = sub["above"] * sub["z"]
            cols_hat = [np.ones(len(sub)), sub["p_hat"].values, sub["z"].values, sub["az"].values]
            cols_act = [np.ones(len(sub)), sub["final_pub_pct"].values, sub["z"].values, sub["az"].values]
            if poly == "Quadratic":
                sub["az2"] = sub["above"] * sub["z2"]
                cols_hat.extend([sub["z2"].values, sub["az2"].values])
                cols_act.extend([sub["z2"].values, sub["az2"].values])
            X_hat = np.column_stack(cols_hat)
            X_act = np.column_stack(cols_act)
            y_vec = sub["log_ir"].values
            XtX_inv = np.linalg.inv(X_hat.T @ X_hat)
            beta_2sls = XtX_inv @ (X_hat.T @ y_vec)
            u_struct = y_vec - (X_act @ beta_2sls)
            h_diag = np.sum((X_hat @ XtX_inv) * X_hat, axis=1)
            hc3_weights = (u_struct ** 2) / np.maximum((1.0 - h_diag) ** 2, 1e-8)
            vcov_2sls_hc3 = XtX_inv @ (X_hat.T * hc3_weights @ X_hat) @ XtX_inv
            iv_coef = float(beta_2sls[1])
            iv_se = float(np.sqrt(vcov_2sls_hc3[1, 1]))
            iv_t = iv_coef / iv_se if iv_se > 0 else np.nan

            # Suppress weak-IV Wald ratio when |fs_t| < 2.0 (arbitrary noise sign inversions at 50x / 100x)
            wald = (rf_jump / fs_jump) if (fs_jump != 0 and abs(fs_t) >= 2.0) else np.nan

            rd_rows.append({
                "Cutoff_x": cutoff,
                "Bandwidth_log_pts": f"{bw_val:.2f}" if poly == "Linear" else f"{bw_val:.2f}_Quad",
                "Local_N": len(sub),
                "First_Stage_Jump_pp": round(float(fs_jump), 2),
                "First_Stage_t_HC3": round(float(fs_t), 2),
                "First_Stage_p_val": round(float(fs_p), 4),
                "Reduced_Form_Jump": round(float(rf_jump), 4),
                "Reduced_Form_t_HC3": round(float(rf_t), 2),
                "Reduced_Form_p_val": round(float(rf_p), 4),
                "Local_Linear_2SLS_Coef": round(float(iv_coef), 4) if abs(fs_t) >= 2.0 else np.nan,
                "Local_Linear_2SLS_t": round(float(iv_t), 2) if abs(fs_t) >= 2.0 else np.nan,
                "Wald_Ratio": round(float(wald), 4) if pd.notna(wald) else np.nan,
            })

    # Panel C: PN18 15x RD Validity Diagnostics (Binomial Density Tests & Covariate Balance)
    val_rows = []
    z15 = np.log(np.maximum(pn18_sub["retail_sub_ratio_clean"], 0.01)) - np.log(15.0)
    for bw_d in [0.35, 0.45, 0.65, 0.85]:
        s_d = pn18_sub[np.abs(z15) <= bw_d]
        n_b = int((s_d["retail_sub_ratio_clean"] < 15.0).sum())
        n_a = int((s_d["retail_sub_ratio_clean"] >= 15.0).sum())
        p_bin = float(stats.binomtest(n_a, n_a + n_b, 0.5).pvalue) if (n_a + n_b) > 0 else np.nan
        val_rows.append({
            "Test_Type": "Density Binomial Test (15x Cutoff)",
            "Variable_or_Window": f"|log(Sub/15)| <= {bw_d:.2f} (Below={n_b}, Above={n_a})",
            "Local_N": n_a + n_b,
            "Estimate_or_ShareAbove": round(n_a / max(1, n_a + n_b), 4),
            "SE_HC3": np.nan,
            "t_stat": np.nan,
            "p_value": round(p_bin, 4),
        })
    sub15 = pn18_sub[np.abs(z15) <= 0.65].copy()
    sub15["z"] = z15[np.abs(z15) <= 0.65]
    sub15["above"] = (sub15["retail_sub_ratio_clean"] >= 15.0).astype(int)
    for cov_col, cov_lbl in [
        ("log_proceeds", "Log Gross Proceeds (HK$M)"),
        ("is_prc_joint_stock", "PRC Joint-Stock H-Share Dummy"),
        ("has_cornerstone", "Has Cornerstone Tranche Dummy"),
        ("init_pub_pct", "Initial Public Offer Share (%)"),
        ("hsi_ret_pre30td_pct", "Pre-Listing 30-TD HSI Return (%)"),
    ]:
        sc_df = sub15.dropna(subset=[cov_col, "z", "above"])
        mc = smf.ols(f"{cov_col} ~ above * z", data=sc_df).fit(cov_type="HC3")
        val_rows.append({
            "Test_Type": "Covariate Balance RD (15x, |z|<=0.65)",
            "Variable_or_Window": cov_lbl,
            "Local_N": int(mc.nobs),
            "Estimate_or_ShareAbove": round(float(mc.params["above"]), 4),
            "SE_HC3": round(float(mc.bse["above"]), 4),
            "t_stat": round(float(mc.tvalues["above"]), 2),
            "p_value": round(float(mc.pvalues["above"]), 4),
        })
    cov_controls = ["log_proceeds", "is_prc_joint_stock", "has_cornerstone", "init_pub_pct"]
    cov_rhs_controls = " + ".join(cov_controls)
    for bw_adj, poly_adj in [(0.35, "Linear"), (0.45, "Linear"), (0.55, "Linear"), (0.65, "Linear"), (0.85, "Linear"), (0.65, "Quadratic")]:
        z_all = np.log(np.maximum(pn18_clean["retail_sub_ratio_clean"], 0.01)) - np.log(15.0)
        s_adj = pn18_clean[np.abs(z_all) <= bw_adj].copy()
        s_adj["z"] = z_all[np.abs(z_all) <= bw_adj]
        s_adj["z2"] = s_adj["z"] ** 2
        s_adj["above"] = (s_adj["retail_sub_ratio_clean"] >= 15.0).astype(int)
        s_adj = s_adj.dropna(subset=cov_controls).copy()
        rhs_rd = "above * z" if poly_adj == "Linear" else "above * z + above * z2"
        bw_tag = f"|z|<={bw_adj:.2f}" if poly_adj == "Linear" else f"|z|<={bw_adj:.2f}_Quad"

        fs_adj = smf.ols(f"final_pub_pct ~ {rhs_rd} + {cov_rhs_controls}", data=s_adj).fit(cov_type="HC3")
        rf_adj = smf.ols(f"log_ir ~ {rhs_rd} + {cov_rhs_controls}", data=s_adj).fit(cov_type="HC3")

        # Covariate-adjusted local-linear / quadratic 2SLS with HC3 structural residuals
        s_adj["p_hat"] = fs_adj.fittedvalues
        s_adj["az"] = s_adj["above"] * s_adj["z"]
        cols_hat_adj = [np.ones(len(s_adj)), s_adj["p_hat"].values, s_adj["z"].values, s_adj["az"].values]
        cols_act_adj = [np.ones(len(s_adj)), s_adj["final_pub_pct"].values, s_adj["z"].values, s_adj["az"].values]
        if poly_adj == "Quadratic":
            s_adj["az2"] = s_adj["above"] * s_adj["z2"]
            cols_hat_adj.extend([s_adj["z2"].values, s_adj["az2"].values])
            cols_act_adj.extend([s_adj["z2"].values, s_adj["az2"].values])
        for cc in cov_controls:
            cols_hat_adj.append(s_adj[cc].values)
            cols_act_adj.append(s_adj[cc].values)

        Xh_adj = np.column_stack(cols_hat_adj)
        Xa_adj = np.column_stack(cols_act_adj)
        y_adj = s_adj["log_ir"].values
        XtXi_adj = np.linalg.inv(Xh_adj.T @ Xh_adj)
        b2sls_adj = XtXi_adj @ (Xh_adj.T @ y_adj)
        u2sls_adj = y_adj - (Xa_adj @ b2sls_adj)
        hd_adj = np.sum((Xh_adj @ XtXi_adj) * Xh_adj, axis=1)
        hc3w_adj = (u2sls_adj ** 2) / np.maximum((1.0 - hd_adj) ** 2, 1e-8)
        vcov_adj = XtXi_adj @ (Xh_adj.T * hc3w_adj @ Xh_adj) @ XtXi_adj
        iv_c_adj = float(b2sls_adj[1])
        iv_se_adj = float(np.sqrt(vcov_adj[1, 1]))
        iv_t_adj = iv_c_adj / iv_se_adj if iv_se_adj > 0 else np.nan
        iv_p_adj = float(2.0 * (1.0 - stats.norm.cdf(abs(iv_t_adj)))) if pd.notna(iv_t_adj) else np.nan

        val_rows.append({
            "Test_Type": f"Covariate-Adjusted FS RD (15x, {bw_tag})",
            "Variable_or_Window": "Final Retail Share Jump (+ Proceeds, H-Share, CS, InitPub)",
            "Local_N": int(fs_adj.nobs),
            "Estimate_or_ShareAbove": round(float(fs_adj.params["above"]), 4),
            "SE_HC3": round(float(fs_adj.bse["above"]), 4),
            "t_stat": round(float(fs_adj.tvalues["above"]), 2),
            "p_value": round(float(fs_adj.pvalues["above"]), 4),
        })
        val_rows.append({
            "Test_Type": f"Covariate-Adjusted RF RD (15x, {bw_tag})",
            "Variable_or_Window": "Log(1+IR) Jump (+ Proceeds, H-Share, CS, InitPub)",
            "Local_N": int(rf_adj.nobs),
            "Estimate_or_ShareAbove": round(float(rf_adj.params["above"]), 4),
            "SE_HC3": round(float(rf_adj.bse["above"]), 4),
            "t_stat": round(float(rf_adj.tvalues["above"]), 2),
            "p_value": round(float(rf_adj.pvalues["above"]), 4),
        })
        val_rows.append({
            "Test_Type": f"Covariate-Adjusted 2SLS RD (15x, {bw_tag})",
            "Variable_or_Window": "Log(1+IR) per +1pp Retail Share (+ Proceeds, H-Share, CS, InitPub)",
            "Local_N": int(rf_adj.nobs),
            "Estimate_or_ShareAbove": round(iv_c_adj, 4),
            "SE_HC3": round(iv_se_adj, 4),
            "t_stat": round(iv_t_adj, 2),
            "p_value": round(iv_p_adj, 4),
        })

    df_p18_brk = pd.DataFrame(p18_bracket_rows)
    df_rd = pd.DataFrame(rd_rows)
    df_val = pd.DataFrame(val_rows)

    # Save combined table 9C
    with open(TABLE_9C_CSV, "w", encoding="utf-8") as f:
        f.write("# Panel A: PN18 Bracket Summary\n")
        df_p18_brk.to_csv(f, index=False)
        f.write("\n# Panel B: Local Linear RD Jumps and 2SLS\n")
        df_rd.to_csv(f, index=False)
        f.write("\n# Panel C: PN18 15x RD Validity Diagnostics\n")
        df_val.to_csv(f, index=False)

    print("Panel A: PN18 Brackets Summary:")
    print(df_p18_brk.to_string(index=False))
    print("\nPanel B: Local Linear RD Jumps and 2SLS Estimates:")
    print(df_rd.to_string(index=False))
    print("\nPanel C: PN18 15x RD Validity Diagnostics:")
    print(df_val.to_string(index=False))
    print(f"Saved Table 9C to: {TABLE_9C_CSV}")

    # 4. Re-run Table 2D (Panel A quartiles & Panel B regressions on full N=226)
    print("\n" + "=" * 60)
    print("3. RE-RUNNING TABLE 2D (COST ANATOMY & OLS) ON FULL N=226")
    print("=" * 60)

    p0 = pd.to_numeric(df226["IPO Subscription Price (HK$)"], errors="coerce")
    sh_base = pd.to_numeric(df226["Final global offering shares (before over-allotment)"], errors="coerce")
    gross_from_sh = (p0 * sh_base) / 1e6
    net_proc = pd.to_numeric(df226["Net IPO proceeds to issuer (HK$)"], errors="coerce") / 1e6
    list_exp = pd.to_numeric(df226["Listing expenses (HK$)"], errors="coerce") / 1e6
    gross_from_net = net_proc + list_exp
    df226["gross_proc_m"] = gross_from_sh.fillna(gross_from_net)
    df226["list_exp_m"] = list_exp
    df226["list_exp_pct"] = (df226["list_exp_m"] / df226["gross_proc_m"]) * 100.0
    df226.loc[(df226["list_exp_pct"] <= 0) | (df226["list_exp_pct"] > 50), "list_exp_pct"] = np.nan

    uw_hk = pd.to_numeric(df226["Underwriting Commission (% of fund raised HK (a)"], errors="coerce")
    df226["uw_hk_pct"] = np.where(uw_hk <= 1.0, uw_hk * 100.0, uw_hk)
    df226.loc[(df226["uw_hk_pct"] <= 0) | (df226["uw_hk_pct"] > 20), "uw_hk_pct"] = np.nan

    base_fee = pd.to_numeric(df226["Underwriting base commission rate (%)"], errors="coerce")
    df226["base_fee_pct"] = np.where(base_fee <= 1.0, base_fee * 100.0, base_fee)

    df226["non_uw_prof_pct"] = df226["list_exp_pct"] - df226["uw_hk_pct"]
    df226["sponsors_count"] = pd.to_numeric(df226["Joint sponsor count"], errors="coerce").fillna(1)
    df226["log_proceeds"] = np.log(df226["gross_proc_m"])

    ah_flag_s = (pd.to_numeric(df226["A+H issuer flag"], errors="coerce").fillna(0) == 1)
    c18a_flag_s = (pd.to_numeric(df226["Chapter 18A flag"], errors="coerce").fillna(0) == 1)
    c18c_flag_s = (pd.to_numeric(df226["Chapter 18C flag"], errors="coerce").fillna(0) == 1)
    wvr_flag_s = (pd.to_numeric(df226["WVR flag"], errors="coerce").fillna(0) == 1)
    df226["is_ah"] = ah_flag_s.astype(int)
    df226["is_rd"] = (c18a_flag_s | c18c_flag_s).astype(int)
    df226["state_backed"] = pd.to_numeric(df226["Pre-IPO State/Gov backing (1=yes; 0=no)"], errors="coerce").fillna(0).astype(int)

    # Quartiles
    df226["quartile"] = pd.qcut(df226["gross_proc_m"], 4, labels=["Q1", "Q2", "Q3", "Q4"])

    q_rows = []
    for q, grp in list(df226.groupby("quartile", observed=False)) + [("All Main Board (N=226)", df226)]:
        p_min, p_max = grp["gross_proc_m"].min(), grp["gross_proc_m"].max()
        if q == "Q1":
            lbl = f"Q1 (Smallest: < HK${p_max:.0f}m)"
        elif q == "Q4":
            lbl = f"Q4 (Largest: > HK${p_min:.0f}m)"
        elif "All" in q:
            lbl = q
        else:
            lbl = f"{q} (HK${p_min:.0f}m - HK${p_max:.0f}m)"

        q_rows.append({
            "Quartile": lbl,
            "IPOs_N": len(grp),
            "Median_Proceeds_HKDm": round(float(grp["gross_proc_m"].median()), 2),
            "Median_Total_Expense_HKDm": round(float(grp["list_exp_m"].median()), 2),
            "Mean_Gross_Spread_Pct": round(float(grp["uw_hk_pct"].mean()), 2),
            "Median_Gross_Spread_Pct": round(float(grp["uw_hk_pct"].median()), 2),
            "Mean_Base_Fee_Pct": round(float(grp["base_fee_pct"].mean()), 2),
            "Mean_Non_UW_Prof_Cost_Pct": round(float(grp["non_uw_prof_pct"].mean()), 2),
            "Mean_Total_Direct_Cost_Pct": round(float(grp["list_exp_pct"].mean()), 2),
            "Median_Total_Direct_Cost_Pct": round(float(grp["list_exp_pct"].median()), 2),
            "Mean_Joint_Sponsors": round(float(grp["sponsors_count"].mean()), 2)
        })

    df_t2d_q = pd.DataFrame(q_rows)

    # Regressions
    sub1 = df226.dropna(subset=["uw_hk_pct", "log_proceeds", "is_ah", "is_rd", "state_backed", "sponsors_count"]).copy()
    m1 = smf.ols("uw_hk_pct ~ log_proceeds + is_ah + is_rd + state_backed + sponsors_count", data=sub1).fit(cov_type="HC3")

    sub2 = df226.dropna(subset=["list_exp_pct", "log_proceeds", "is_ah", "is_rd", "state_backed", "sponsors_count"]).copy()
    m2 = smf.ols("list_exp_pct ~ log_proceeds + is_ah + is_rd + state_backed + sponsors_count", data=sub2).fit(cov_type="HC3")

    reg_rows = [
        {"Variable": "log(Gross Proceeds in HK$m)", "M1_UW_Spread_Coef": round(float(m1.params["log_proceeds"]), 3), "M1_SE": round(float(m1.bse["log_proceeds"]), 3), "M1_t": round(float(m1.tvalues["log_proceeds"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["log_proceeds"]), 3), "M2_SE": round(float(m2.bse["log_proceeds"]), 3), "M2_t": round(float(m2.tvalues["log_proceeds"]), 2)},
        {"Variable": "A+H Dual Listing Indicator", "M1_UW_Spread_Coef": round(float(m1.params["is_ah"]), 3), "M1_SE": round(float(m1.bse["is_ah"]), 3), "M1_t": round(float(m1.tvalues["is_ah"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["is_ah"]), 3), "M2_SE": round(float(m2.bse["is_ah"]), 3), "M2_t": round(float(m2.tvalues["is_ah"]), 2)},
        {"Variable": "Chapter 18A / 18C R&D Indicator", "M1_UW_Spread_Coef": round(float(m1.params["is_rd"]), 3), "M1_SE": round(float(m1.bse["is_rd"]), 3), "M1_t": round(float(m1.tvalues["is_rd"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["is_rd"]), 3), "M2_SE": round(float(m2.bse["is_rd"]), 3), "M2_t": round(float(m2.tvalues["is_rd"]), 2)},
        {"Variable": "Pre-IPO State/Gov Backing", "M1_UW_Spread_Coef": round(float(m1.params["state_backed"]), 3), "M1_SE": round(float(m1.bse["state_backed"]), 3), "M1_t": round(float(m1.tvalues["state_backed"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["state_backed"]), 3), "M2_SE": round(float(m2.bse["state_backed"]), 3), "M2_t": round(float(m2.tvalues["state_backed"]), 2)},
        {"Variable": "Joint Sponsor Count", "M1_UW_Spread_Coef": round(float(m1.params["sponsors_count"]), 3), "M1_SE": round(float(m1.bse["sponsors_count"]), 3), "M1_t": round(float(m1.tvalues["sponsors_count"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["sponsors_count"]), 3), "M2_SE": round(float(m2.bse["sponsors_count"]), 3), "M2_t": round(float(m2.tvalues["sponsors_count"]), 2)},
        {"Variable": "Intercept", "M1_UW_Spread_Coef": round(float(m1.params["Intercept"]), 3), "M1_SE": round(float(m1.bse["Intercept"]), 3), "M1_t": round(float(m1.tvalues["Intercept"]), 2), "M2_Total_Cost_Coef": round(float(m2.params["Intercept"]), 3), "M2_SE": round(float(m2.bse["Intercept"]), 3), "M2_t": round(float(m2.tvalues["Intercept"]), 2)},
        {"Variable": "N / R2 / Adj R2", "M1_UW_Spread_Coef": f"N={int(m1.nobs)}", "M1_SE": f"R2={m1.rsquared:.3f}", "M1_t": f"Adj={m1.rsquared_adj:.3f}", "M2_Total_Cost_Coef": f"N={int(m2.nobs)}", "M2_SE": f"R2={m2.rsquared:.3f}", "M2_t": f"Adj={m2.rsquared_adj:.3f}"}
    ]
    df_t2d_reg = pd.DataFrame(reg_rows)

    with open(TABLE_2D_CSV, "w", encoding="utf-8") as f:
        f.write("# Panel A: Cost Anatomy by Gross Proceeds Quartile (N=226)\n")
        df_t2d_q.to_csv(f, index=False)
        f.write("\n# Panel B: Cross-Sectional OLS Cost Regressions (N=226)\n")
        df_t2d_reg.to_csv(f, index=False)

    print("Panel A: Quartiles on N=226:")
    print(df_t2d_q.to_string(index=False))
    print("\nPanel B: OLS Regressions on N=226:")
    print(df_t2d_reg.to_string(index=False))
    print(f"Saved Table 2D to: {TABLE_2D_CSV}")

    # 5. Table 6B: Fundamentals by Listing Route (N=226)
    print("\n" + "=" * 60)
    print("4. RE-RUNNING TABLE 6B (FUNDAMENTALS BY ROUTE) ON FULL N=226")
    print("=" * 60)

    # Map listing routes using audited binary flags in HKIPO-MB-MASTER_clean.csv
    # Mutually exclusive priority: 18A (26) -> 18C (23) -> A+H Conventional (55; excl. 2493.HK [18A+AH] & 6727.HK [18C+AH]) -> 8A WVR Conventional (7; excl. 0100.HK [18C+WVR]) -> Main Board Conventional (115)
    def clean_route_row(r):
        if float(r.get("Chapter 18A flag", 0) or 0) == 1:
            return "Chapter 18A Biotech"
        if float(r.get("Chapter 18C flag", 0) or 0) == 1:
            return "Chapter 18C Specialist Tech"
        if float(r.get("A+H issuer flag", 0) or 0) == 1:
            return "Chapter 19A A+H Dual-Listed"
        if float(r.get("WVR flag", 0) or 0) == 1:
            return "Chapter 8A WVR (Conventional)"
        return "Main Board Conventional"

    df226["clean_route"] = df226.apply(clean_route_row, axis=1)
    print("Route counts:")
    print(df226["clean_route"].value_counts())

    curr226 = df226["currency in financial information"].astype(str).str.upper()
    fx226 = np.where(curr226.str.contains(r"USD|US\$"), 7.80, np.where(curr226.str.contains("HKD"), 1.0, 1.08))

    rev1 = pd.to_numeric(df226["Net sales in year-1"], errors="coerce") * fx226 / 1e6
    prof1 = pd.to_numeric(df226["Profit for the year in year-1"], errors="coerce") * fx226 / 1e6
    assets1 = pd.to_numeric(df226["total assets in year-1"], errors="coerce") * fx226 / 1e6
    rd_exp1 = pd.to_numeric(df226["R&D expensed in year-1 (before annualization)"], errors="coerce")
    rd_cap1 = pd.to_numeric(df226["Development costs capitalized in year-1 (additions, before annualization)"], errors="coerce")
    rd_tot1 = (rd_exp1.fillna(0) + rd_cap1.fillna(0)) * fx226 / 1e6

    df226["rev1_hkdm"] = rev1
    df226["prof1_hkdm"] = prof1
    df226["assets1_hkdm"] = assets1
    df226["rd_tot1_hkdm"] = rd_tot1
    df226["rd_intensity"] = np.where(rev1 > 0, (rd_tot1 / rev1) * 100.0, np.nan)
    df226["age"] = pd.to_numeric(df226["Firm age at IPO (years)"], errors="coerce")
    # Preserve NaN for missing VC/PE disclosures rather than zero-filling
    df226["vc_backed"] = pd.to_numeric(df226["Pre-IPO VC/PE backing (1=yes; 0=no)"], errors="coerce")
    ctrl_v = pd.to_numeric(df226["Controller voting rights at listing (%)"], errors="coerce")
    ctrl_e = pd.to_numeric(df226["Controller economic interest at listing (%)"], errors="coerce")
    ctrl_v = np.where(ctrl_v <= 1.0, ctrl_v * 100.0, ctrl_v)
    ctrl_e = np.where(ctrl_e <= 1.0, ctrl_e * 100.0, ctrl_e)
    df226["ctrl_vote"] = np.where(pd.notna(ctrl_v), ctrl_v, ctrl_e)

    route_order = [
        "Chapter 18A Biotech",
        "Chapter 18C Specialist Tech",
        "Chapter 19A A+H Dual-Listed",
        "Chapter 8A WVR (Conventional)",
        "Main Board Conventional"
    ]

    t6b_rows = []
    for rt in route_order + ["All 2025-2026 Cohort (N=226)"]:
        grp = df226[df226["clean_route"] == rt] if rt != "All 2025-2026 Cohort (N=226)" else df226
        t6b_rows.append({
            "Listing_Route": rt,
            "N": len(grp),
            "Median_Age_Years": round(float(grp["age"].median()), 1),
            "Median_Revenue_HKDm": round(float(grp["rev1_hkdm"].median()), 1),
            "Median_Net_Profit_HKDm": round(float(grp["prof1_hkdm"].median()), 1),
            "Median_Total_Assets_HKDm": round(float(grp["assets1_hkdm"].median()), 1),
            "Unprofitable_Share_Pct": round(float((grp["prof1_hkdm"] < 0).mean() * 100.0), 1),
            "Median_RD_Intensity_Pct": round(float(grp["rd_intensity"].dropna().median()), 1) if grp["rd_intensity"].notna().any() else 0.0,
            "Median_Direct_Cost_Pct": round(float(grp["list_exp_pct"].dropna().median()), 1),
            "VC_PE_Backed_Pct": round(float(grp["vc_backed"].mean() * 100.0), 1),
            "State_Backed_Pct": round(float(grp["state_backed"].mean() * 100.0), 1),
            "Ctrl_Voting_Median_Pct": round(float(grp["ctrl_vote"].dropna().median()), 1)
        })

    df_t6b = pd.DataFrame(t6b_rows)
    df_t6b.to_csv(TABLE_6B_CSV, index=False)
    print(df_t6b.to_string(index=False))
    print(f"Saved Table 6B to: {TABLE_6B_CSV}")

    # 6. Table 13: Stabilization Regimes (N=226)
    print("\n" + "=" * 60)
    print("5. RE-RUNNING TABLE 13 (GREENSHOE EXERCISE REGIMES) ON FULL N=226")
    print("=" * 60)

    gs_pct = pd.to_numeric(df226["Over-allotment exercise percentage (%)"], errors="coerce").fillna(0)
    ir_close = pd.to_numeric(df226["First-day return / Underpricing (%)"], errors="coerce")
    ir_close_pct = np.where(abs(ir_close) <= 10.0, ir_close * 100.0, ir_close)

    df226["ir_close_pct"] = ir_close_pct
    df226["is_full_shoe"] = gs_pct >= 0.99

    full_grp = df226[df226["is_full_shoe"]]
    non_full_grp = df226[~df226["is_full_shoe"]]

    print(f"Full Greenshoe Exercised: N = {len(full_grp)}")
    print(f"Zero / Partial Greenshoe: N = {len(non_full_grp)}")
    print(f"Total: N = {len(full_grp) + len(non_full_grp)} (Expected 226)")
    assert len(full_grp) + len(non_full_grp) == 226

    t13_rows = []
    for lbl, grp in [
        ("Full 15% Greenshoe Exercised", full_grp),
        ("Partial / Zero / No Option", non_full_grp),
        ("All 2025-2026 Main Board Deals (N=226)", df226),
    ]:
        ir = grp["ir_close_pct"].dropna()
        flip = pd.to_numeric(grp["First-day flipping ratio (%)"], errors="coerce").dropna() * 100.0
        c5 = pd.to_numeric(grp["Post-stabilization cliff return [-5, +5] (%)"], errors="coerce").dropna() * 100.0
        c20 = pd.to_numeric(grp["Post-stabilization 20-day return [0, +20] (%)"], errors="coerce").dropna() * 100.0
        b1 = pd.to_numeric(grp["1-month BHR from Day-1 close (%)"], errors="coerce").dropna() * 100.0
        b6 = pd.to_numeric(grp["6-month BHR from Day-1 close (%)"], errors="coerce").dropna() * 100.0
        t13_rows.append({
            "Stabilization_Regime": lbl,
            "N": len(grp),
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Exact_0pct_Close_Pct": round(float((ir.abs() < 0.05).mean() * 100.0), 2),
            "Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 2),
            "Day1_Turnover_Pct_Offer": round(float(flip.mean()), 2),
            "Stab_End_CAR_5_5_Pct": round(float(c5.mean()), 2),
            "Stab_End_N": len(c5),
            "Post_Stab_20d_Ret_Pct": round(float(c20.mean()), 2),
            "Mean_1M_BHR_Pct": round(float(b1.mean()), 2),
            "BHR_1M_N": len(b1),
            "Mean_6M_BHR_Pct": round(float(b6.mean()), 2),
            "BHR_6M_N": len(b6),
        })
    df_t13 = pd.DataFrame(t13_rows)
    df_t13.to_csv(TABLE_13_CSV, index=False)
    print(df_t13.to_string(index=False))
    liq_decay = pd.to_numeric(df226["Liquidity decay ratio (6M vs Day-1 turnover)"], errors="coerce").dropna() * 100.0
    print(f"Matured 6M Liquidity Decay (N={len(liq_decay)}): Mean={liq_decay.mean():.2f}%, Median={liq_decay.median():.2f}%")
    print(f"Saved Table 13 to: {TABLE_13_CSV}")

    # 6. Table 15B Panel B: IAS 38 R&D Capitalization & Rule 8.05 Profit Threshold Bunchers (N=226)
    print("\n" + "=" * 60)
    print("5B. RE-RUNNING TABLE 15B PANEL B (IAS 38 & RULE 8.05 BUNCHERS) ON N=226")
    print("=" * 60)

    p3 = pd.to_numeric(df226["Profit for the year in year-3"], errors="coerce")
    p2 = pd.to_numeric(df226["Profit for the year in year-2"], errors="coerce")
    p1 = pd.to_numeric(df226["Profit for the year in year-1"], errors="coerce")
    p1_orig = pd.to_numeric(df226["Year-1 profit for period (original)"], errors="coerce").fillna(p1)
    a1 = pd.to_numeric(df226["total assets in year-1"], errors="coerce")
    cfo1 = pd.to_numeric(df226["Operating cash flow in year-1 (before annualization)"], errors="coerce")
    s3 = pd.to_numeric(df226["Net sales in year-3"], errors="coerce")
    s1 = pd.to_numeric(df226["Net sales in year-1"], errors="coerce")
    rd_exp = pd.to_numeric(df226["R&D expensed in year-1 (before annualization)"], errors="coerce").fillna(0.0)
    rd_cap = pd.to_numeric(df226["Development costs capitalized in year-1 (additions, before annualization)"], errors="coerce").fillna(0.0)

    df226["cum_3y_profit_hkd_m"] = ((p3.fillna(0) + p2.fillna(0) + p1.fillna(0)) * fx226) / 1e6
    df226["has_rd_cap"] = (rd_cap > 0).astype(int)
    df226["sales_cagr_3y_pct"] = np.where((s3 > 0) & (s1 > 0), ((s1 / s3) ** 0.5 - 1.0) * 100.0, np.nan)
    df226["total_accruals_pct_assets"] = ((p1_orig - cfo1) / a1) * 100.0
    df226["cfo_to_assets_pct"] = (cfo1 / a1) * 100.0
    df226["cfo_to_profit_ratio"] = np.where(p1_orig > 0, cfo1 / p1_orig, np.nan)

    t15b_rows = []
    rd_active = df226[(rd_exp + rd_cap) > 0].copy()
    for flag, lbl in [
        (0, "Panel B1: 100% R&D Expensed on Income Statement (Conservative, N=172)"),
        (1, "Panel B2: IAS 38 R&D Development Capitalized onto Balance Sheet (N=30)")
    ]:
        grp = rd_active[rd_active["has_rd_cap"] == flag]
        ir = grp["ir_close_pct"].dropna()
        t15b_rows.append({
            "Accounting_Cohort": lbl,
            "N_Deals": len(grp),
            "Median_3Y_Sales_CAGR_Pct": round(float(grp["sales_cagr_3y_pct"].dropna().median()), 2),
            "Median_Accruals_Pct_Assets": round(float(grp["total_accruals_pct_assets"].median()), 2),
            "Median_CFO_to_Assets_Pct": round(float(grp["cfo_to_assets_pct"].median()), 2),
            "Median_CFO_to_Profit_x": round(float(grp["cfo_to_profit_ratio"].dropna().median()), 2) if grp["cfo_to_profit_ratio"].notna().any() else np.nan,
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 1),
        })

    r805_prof = df226[
        (pd.to_numeric(df226["Chapter 18A flag"], errors="coerce").fillna(0) == 0)
        & (pd.to_numeric(df226["Chapter 18C flag"], errors="coerce").fillna(0) == 0)
        & (df226["cum_3y_profit_hkd_m"] >= 75.0)
    ].copy()
    r805_prof["profit_band"] = np.where(
        r805_prof["cum_3y_profit_hkd_m"] <= 200.0,
        "Panel C1: Rule 8.05(1) Threshold Bunchers (3Y Cum. Profit HK$75M-200M)",
        "Panel C2: Large Cushioned Profitable Issuers (3Y Cum. Profit > HK$200M)"
    )
    for lbl, grp in r805_prof.groupby("profit_band"):
        ir = grp["ir_close_pct"].dropna()
        t15b_rows.append({
            "Accounting_Cohort": lbl,
            "N_Deals": len(grp),
            "Median_3Y_Sales_CAGR_Pct": round(float(grp["sales_cagr_3y_pct"].dropna().median()), 2),
            "Median_Accruals_Pct_Assets": round(float(grp["total_accruals_pct_assets"].median()), 2),
            "Median_CFO_to_Assets_Pct": round(float(grp["cfo_to_assets_pct"].median()), 2),
            "Median_CFO_to_Profit_x": round(float(grp["cfo_to_profit_ratio"].dropna().median()), 2) if grp["cfo_to_profit_ratio"].notna().any() else np.nan,
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 1),
        })

    df_t15b = pd.DataFrame(t15b_rows)
    df_t15b.to_csv(TABLE_15B_CSV, index=False)
    print(df_t15b.to_string(index=False))
    print(f"Saved Table 15B Panel B to: {TABLE_15B_CSV}")

    # 7. Audit Items Summary
    print("\n" + "=" * 60)
    print("6. SPECIAL AUDIT ITEMS VERIFICATION")
    print("=" * 60)

    # Audit Item A: Policy Valve maxlags
    pv_script = REPO_ROOT / "analysis" / "run_policy_valve_econometrics.py"
    with open(pv_script) as f:
        pv_code = f.read()
    print("Audit Item A (Policy Valve maxlags):")
    if 'cov_kwds={"maxlags": 12}' in pv_code:
        print("  - Table 7B (HAC Regressions): maxlags = 12 (verified in code line 103)")
    if 'cov_kwds={"maxlags": h + 6}' in pv_code:
        print("  - Table 7C (Local Projections): maxlags = h + 6 (verified in code lines 132, 137)")

    # Audit Item B: Ritter Moderate-Size Benchmark
    sp = df33[df33["gross_spread_clean_pct"] > 0].copy()
    sp["proceeds_hkd_m"] = sp["funds_raised_total_hkd"] / 1e6
    sp["is_mb"] = (sp["board"] == "Main Board").astype(int)
    sp["is_moderate_size"] = ((sp["proceeds_hkd_m"] >= 234.0) & (sp["proceeds_hkd_m"] <= 1248.0)).astype(int)
    sp["exact_7pct"] = ((sp["gross_spread_clean_pct"] >= 6.95) & (sp["gross_spread_clean_pct"] <= 7.05)).astype(int)
    sp["exact_2_5pct"] = ((sp["gross_spread_clean_pct"] >= 2.45) & (sp["gross_spread_clean_pct"] <= 2.55)).astype(int)

    m1 = sp[(sp["is_mb"] == 1) & (sp["is_moderate_size"] == 1) & (sp["cohort_year"] >= 2001)]
    m2 = sp[(sp["is_mb"] == 1) & (sp["is_moderate_size"] == 1) & (sp["cohort_year"] >= 2001) & (sp["cohort_year"] <= 2025)]

    print("\nAudit Item B (Ritter Moderate-Size Benchmark, $30M-$160M / HK$234M-1,248M):")
    print(f"  - Case 1: year >= 2001 (including 2026): N = {len(m1)}, Mean = {m1['gross_spread_clean_pct'].mean():.2f}%, Median = {m1['gross_spread_clean_pct'].median():.2f}%, 7.00% Share = {m1['exact_7pct'].mean()*100:.2f}% ({m1['exact_7pct'].sum()}/{len(m1)}), 2.50% Share = {m1['exact_2_5pct'].mean()*100:.2f}% ({m1['exact_2_5pct'].sum()}/{len(m1)})")
    print(f"  - Case 2: 2001 <= year <= 2025 (strictly excluding 2026): N = {len(m2)}, Mean = {m2['gross_spread_clean_pct'].mean():.2f}%, Median = {m2['gross_spread_clean_pct'].median():.2f}%, 7.00% Share = {m2['exact_7pct'].mean()*100:.2f}% ({m2['exact_7pct'].sum()}/{len(m2)}), 2.50% Share = {m2['exact_2_5pct'].mean()*100:.2f}% ({m2['exact_2_5pct'].sum()}/{len(m2)})")

    # Audit Item C: Stale occurrences in Companion
    comp_file = REPO_ROOT / "docs" / "overview_paper" / "HK_IPO_Overview_Deep_Extensions_1994_2026.md"
    with open(comp_file) as f:
        comp_lines = f.readlines()

    print("\nAudit Item C (Stale string occurrences in Companion):")
    for i, line in enumerate(comp_lines):
        for pattern in ["2,649", "26 superstar", "-15.78", "-0.40"]:
            if pattern in line:
                print(f"  - Pattern '{pattern}' found at Line {i+1}: {line.strip()[:100]}...")

    print("\n" + "=" * 80)
    print("ALL MANUSCRIPT & COMPANION TABLE RECOMPUTATIONS COMPLETED SUCCESSFULLY")
    print("=" * 80)

if __name__ == "__main__":
    main()
