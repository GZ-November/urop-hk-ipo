"""
run_hibor_fini_144a_and_bessembinder_econometrics.py

Frontier econometric suite for Modules E6.3 (upgraded), E7, E8, and E9 of the
1994-2026 Hong Kong IPO Overview Monograph:
  1. Upgraded Calendar-Time Portfolio (CTP) Alphas using official HKMA 1-month
     HIBOR risk-free rates (Equal-Month Newey-West HAC OLS vs. Mitchell &
     Stafford 2000 / Loughran & Ritter 2000 Deal-Count WLS).
  2. Module E7: 33-Year Monetary Transmission, IPO Pre-Funding Interbank
     Liquidity Squeezes (Delta 1W-HIBOR & 1W-3M Inversion), and the November
     2023 FINI T+2 Natural Experiment.
  3. Module E8: Loughran & Ritter (2002) Public-Information Pass-Through Under
     Hong Kong's Statutory Hard Price Cap + Lowry & Schwert (2002) / Pastor &
     Veronesi (2005) Monthly Hot-Issue Cycle Regressions (T = 393 Months).
  4. Module E9: Global Capital Market Segmentation & Decoupling (Rule 144A vs.
     Reg S-Only), Vanishing Secondary Share Sales, and Bessembinder (2018, JFE)
     Multi-Decade Lifetime Wealth Concentration.
"""

from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf

BASE_DIR = Path(__file__).resolve().parent.parent
EXT_DIR = BASE_DIR / "analysis" / "out" / "overview_extensions"
VALVE_CSV = BASE_DIR / "analysis" / "out" / "overview_1994_2026" / "clean_monthly_policy_valve_1994_2026.csv"
PANEL_CSV = EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv"
CTP_RF_CSV = EXT_DIR / "clean_monthly_ctp_with_hibor_rf_1994_2026.csv"


def run_upgraded_ctp_with_hkma_rf(ctp: pd.DataFrame) -> pd.DataFrame:
    print("=" * 78)
    print("1. UPGRADED CTP ALPHAS WITH OFFICIAL HKMA 1M HIBOR RF (OLS vs. DEAL-COUNT WLS)")
    print("=" * 78)

    ctp = ctp.copy()
    ctp["mkt_excess"] = ctp["hsi_monthly_return_pct"] - ctp["rf_monthly_pct"]

    specs = [
        ("ctp_12m_mb_ew_ret", "n_ctp_12m_mb", "MB 12M Equal-Weighted"),
        ("ctp_12m_mb_vw_ret", "n_ctp_12m_mb", "MB 12M Value-Weighted"),
        ("ctp_36m_mb_ew_ret", "n_ctp_36m_mb", "MB 36M Equal-Weighted"),
        ("ctp_36m_mb_vw_ret", "n_ctp_36m_mb", "MB 36M Value-Weighted"),
        ("ctp_12m_gem_ew_ret", "n_ctp_12m_gem", "GEM 12M Equal-Weighted"),
        ("ctp_12m_gem_vw_ret", "n_ctp_12m_gem", "GEM 12M Value-Weighted"),
        ("ctp_36m_gem_ew_ret", "n_ctp_36m_gem", "GEM 36M Equal-Weighted"),
        ("ctp_36m_gem_vw_ret", "n_ctp_36m_gem", "GEM 36M Value-Weighted"),
    ]

    rows = []
    for ret_col, n_col, label in specs:
        sub = ctp.dropna(subset=[ret_col, "rf_monthly_pct", "mkt_excess", "hk_smb_proxy_pct"]).copy()
        y_exc = sub[ret_col] - sub["rf_monthly_pct"]
        X1 = sm.add_constant(sub[["mkt_excess"]])
        X2 = sm.add_constant(sub[["mkt_excess", "hk_smb_proxy_pct"]])

        # Equal-month OLS with Newey-West 6-lag HAC
        m1_ols = sm.OLS(y_exc, X1).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        m2_ols = sm.OLS(y_exc, X2).fit(cov_type="HAC", cov_kwds={"maxlags": 6})

        # Mitchell & Stafford (2000) / Loughran & Ritter (2000) Deal-Count WLS (weights = active IPO count N_t)
        w = sub[n_col].clip(lower=1.0).astype(float)
        m2_wls = sm.WLS(y_exc, X2, weights=w).fit(cov_type="HC3")

        rows.append({
            "Portfolio": label,
            "Months_T": int(m2_ols.nobs),
            "Mean_Raw_Ret_Pct": round(float(sub[ret_col].mean()), 3),
            "Mean_Excess_Ret_Pct": round(float(y_exc.mean()), 3),
            "CAPM_Alpha_Pct": round(float(m1_ols.params["const"]), 3),
            "CAPM_t_NW": round(float(m1_ols.tvalues["const"]), 2),
            "TwoFactor_OLS_Alpha_Pct": round(float(m2_ols.params["const"]), 3),
            "TwoFactor_OLS_t_NW": round(float(m2_ols.tvalues["const"]), 2),
            "TwoFactor_WLS_Alpha_Pct": round(float(m2_wls.params["const"]), 3),
            "TwoFactor_WLS_t_HC3": round(float(m2_wls.tvalues["const"]), 2),
            "Beta_MKT": round(float(m2_ols.params["mkt_excess"]), 3),
            "Beta_SMB": round(float(m2_ols.params["hk_smb_proxy_pct"]), 3),
            "t_SMB": round(float(m2_ols.tvalues["hk_smb_proxy_pct"]), 2),
            "R2_OLS": round(float(m2_ols.rsquared), 4),
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(EXT_DIR / "ext_table10b_legacy_2f_calendar_time_portfolio_alphas.csv", index=False)
    print(out_df.to_string(index=False))
    return out_df


def run_module_e7_hibor_and_fini(df: pd.DataFrame) -> None:
    print("\n" + "=" * 78)
    print("2. MODULE E7: 33Y HIBOR DEMAND TRANSMISSION & FINI INTERBANK FREEZE EXPERIMENT")
    print("=" * 78)

    mb = df[df["board"] == "Main Board"].copy()
    mb["listing_dt"] = pd.to_datetime(mb["listing_date"])
    mb["post_fini"] = (mb["listing_dt"] >= pd.Timestamp("2023-11-22")).astype(int)
    mb["log_proceeds"] = np.log(pd.to_numeric(mb["funds_raised_total_hkd"], errors="coerce") / 1e6)
    mb["is_h"] = (mb["is_prc_joint_stock"] == 1).astype(int)
    mb["log_sub"] = np.log1p(pd.to_numeric(mb["retail_sub_ratio_clean"], errors="coerce"))
    mb["log_locked_bn"] = np.log1p(pd.to_numeric(mb["locked_retail_hkd_bn"], errors="coerce").clip(lower=0))

    # A. 33-Year Retail Demand Elasticity to HKMA 1M HIBOR & Post-FINI Shift
    dem = mb.dropna(subset=["log_sub", "hibor_1m_open", "hsi_ret_pre30td_pct", "log_proceeds", "epoch"]).copy()
    m_dem1 = smf.ols("log_sub ~ hibor_1m_open + hsi_ret_pre30td_pct + log_proceeds + is_h + C(epoch)", data=dem).fit(cov_type="HC3")
    m_dem2 = smf.ols("log_sub ~ hibor_1m_open * post_fini + hsi_ret_pre30td_pct + log_proceeds + is_h + C(epoch)", data=dem).fit(cov_type="HC3")

    print(f"\n--- E7A: Retail Subscription Demand Regressions with Epoch FEs (N = {int(m_dem2.nobs)}) ---")
    for label, mod in [("Within-Epoch 33Y", m_dem1), ("Within-Epoch + Post-FINI Interaction", m_dem2)]:
        print(f"[{label}] R2 = {mod.rsquared:.4f}")
        for k in [p for p in mod.params.index if not p.startswith("C(epoch)")]:
            print(f"  {k:28s}: coef={mod.params[k]:+.4f} (t_HC3={mod.tvalues[k]:+.2f}, p={mod.pvalues[k]:.4f})")

    # B. Systemic Interbank Liquidity Freeze Test: Post-AFC HKAB Fixing Era (1999-2026)
    # Exclude 1997-1998 Asian Financial Crisis currency-peg defense (+169 pp spike) so interbank rate changes reflect money-market liquidity
    post99 = mb[(mb["cohort_year"] >= 1999) & mb["locked_retail_hkd_bn"].notna()].copy()
    post99["ym"] = post99["listing_dt"].dt.to_period("M").astype(str)

    # Descriptive bins by Locked Retail Capital Pre-FINI vs Post-FINI
    bins_rows = []
    for regime_val, regime_name in [(0, "Pre-FINI (1999-2023.11, Escrow Lockup)"), (1, "Post-FINI (2023.11-2026, Credit Cap T+2)")]:
        g = post99[post99["post_fini"] == regime_val]
        for tier_name, mask in [
            ("Cold/Mod (< HK$10B Subscribed)", g["locked_retail_hkd_bn"] < 10),
            ("Warm (HK$10B - HK$100B)", (g["locked_retail_hkd_bn"] >= 10) & (g["locked_retail_hkd_bn"] < 100)),
            ("Hot Mega-Freeze (>= HK$100B)", g["locked_retail_hkd_bn"] >= 100),
        ]:
            sub_t = g[mask]
            if len(sub_t) == 0:
                continue
            bins_rows.append({
                "Settlement_Regime": regime_name,
                "Subscription_Capital_Tier": tier_name,
                "N_Deals": len(sub_t),
                "Median_Subscribed_HKD_Bn": round(float(sub_t["locked_retail_hkd_bn"].median()), 2),
                "Mean_Delta_1W_HIBOR_bps": round(float(sub_t["delta_hibor_1w_freeze_pp"].mean() * 100), 1),
                "Median_Delta_1W_HIBOR_bps": round(float(sub_t["delta_hibor_1w_freeze_pp"].median() * 100), 1),
                "Mean_1W_Minus_3M_Spread_bps": round(float(sub_t["hibor_1w_3m_spread_peak_pp"].mean() * 100), 1),
                "Share_1W_Surge_Over_25bps_Pct": round(float((sub_t["delta_hibor_1w_freeze_pp"] >= 0.25).mean() * 100), 1),
            })

    df_freeze = pd.DataFrame(bins_rows)
    df_freeze.to_csv(EXT_DIR / "ext_table11_hibor_liquidity_freeze_fini.csv", index=False)
    print("\n--- E7B: Systemic Interbank 1W-HIBOR Freeze Spikes Pre-FINI vs. Post-FINI ---")
    print(df_freeze.to_string(index=False))

    # Regress Delta 1W HIBOR (in bps) and 1W-3M Spread (in bps) on log(1 + Locked HKD Bn) * Post-FINI
    post99["delta_1w_bps"] = post99["delta_hibor_1w_freeze_pp"] * 100.0
    post99["spread_1w_3m_bps"] = post99["hibor_1w_3m_spread_peak_pp"] * 100.0

    m_frz1 = smf.ols("delta_1w_bps ~ log_locked_bn * post_fini + hibor_3m_open", data=post99).fit(cov_type="HC3")
    m_frz1_yfe = smf.ols("delta_1w_bps ~ log_locked_bn * post_fini + hibor_3m_open + C(cohort_year)", data=post99).fit(
        cov_type="cluster", cov_kwds={"groups": post99["ym"]}
    )
    m_frz2 = smf.ols("spread_1w_3m_bps ~ log_locked_bn * post_fini", data=post99).fit(cov_type="HC3")
    m_frz2_yfe = smf.ols("spread_1w_3m_bps ~ log_locked_bn * post_fini + hibor_3m_open + C(cohort_year)", data=post99).fit(
        cov_type="cluster", cov_kwds={"groups": post99["ym"]}
    )
    m_frz1_cl = smf.ols("delta_1w_bps ~ log_locked_bn * post_fini + hibor_3m_open", data=post99).fit(
        cov_type="cluster", cov_kwds={"groups": post99["ym"]}
    )
    m_frz2_cl = smf.ols("spread_1w_3m_bps ~ log_locked_bn * post_fini", data=post99).fit(
        cov_type="cluster", cov_kwds={"groups": post99["ym"]}
    )

    hibor_reg_rows = []
    for spec_lbl, mod_hc, mod_cl in [
        ("1. Delta 1W HIBOR (bps) Baseline", m_frz1, m_frz1_cl),
        ("2. Delta 1W HIBOR (bps) + Year FE", m_frz1_yfe, m_frz1_yfe),
        ("3. 1W-3M Spread (bps) Baseline", m_frz2, m_frz2_cl),
        ("4. 1W-3M Spread (bps) + HIBOR_3M + Year FE", m_frz2_yfe, m_frz2_yfe),
    ]:
        for k in ["log_locked_bn", "post_fini", "log_locked_bn:post_fini", "hibor_3m_open"]:
            if k not in mod_cl.params.index:
                continue
            hibor_reg_rows.append({
                "Model": spec_lbl,
                "Variable": k,
                "Coef_bps": round(float(mod_cl.params[k]), 3),
                "SE_HC3_or_Cl": round(float(mod_hc.bse[k]), 3),
                "t_HC3_or_Cl": round(float(mod_hc.tvalues[k]), 2),
                "t_MonthClust": round(float(mod_cl.tvalues[k]), 2),
                "p_MonthClust": round(float(mod_cl.pvalues[k]), 4),
                "N": int(mod_cl.nobs),
                "R2": round(float(mod_cl.rsquared), 4),
            })
    pd.DataFrame(hibor_reg_rows).to_csv(EXT_DIR / "ext_table11b_hibor_fini_regressions.csv", index=False)

    print(f"\n[Interbank 1W-HIBOR Surge Regression (bps), N = {int(m_frz1.nobs)}, R2 = {m_frz1.rsquared:.4f}]")
    for k in m_frz1.params.index:
        print(f"  {k:28s}: coef={m_frz1.params[k]:+.2f} bps | t_HC3={m_frz1.tvalues[k]:+.2f} | t_MonthClust={m_frz1_cl.tvalues[k]:+.2f}")
    print(f"\n[Interbank 1W-HIBOR + Year FE (bps), N = {int(m_frz1_yfe.nobs)}, R2 = {m_frz1_yfe.rsquared:.4f}]")
    for k in ["log_locked_bn", "post_fini", "log_locked_bn:post_fini", "hibor_3m_open"]:
        if k in m_frz1_yfe.params.index:
            print(f"  {k:28s}: coef={m_frz1_yfe.params[k]:+.2f} bps | t_MonthClust={m_frz1_yfe.tvalues[k]:+.2f} (p={m_frz1_yfe.pvalues[k]:.4f})")
    print(f"\n[Short-End 1W-minus-3M HIBOR Inversion Regression (bps), N = {int(m_frz2.nobs)}, R2 = {m_frz2.rsquared:.4f}]")
    for k in m_frz2.params.index:
        print(f"  {k:28s}: coef={m_frz2.params[k]:+.2f} bps | t_HC3={m_frz2.tvalues[k]:+.2f} | t_MonthClust={m_frz2_cl.tvalues[k]:+.2f}")
    print(f"\n[Short-End 1W-minus-3M HIBOR + Year FE (bps), N = {int(m_frz2_yfe.nobs)}, R2 = {m_frz2_yfe.rsquared:.4f}]")
    for k in ["log_locked_bn", "post_fini", "log_locked_bn:post_fini", "hibor_3m_open"]:
        if k in m_frz2_yfe.params.index:
            print(f"  {k:28s}: coef={m_frz2_yfe.params[k]:+.2f} bps | t_MonthClust={m_frz2_yfe.tvalues[k]:+.2f} (p={m_frz2_yfe.pvalues[k]:.4f})")


def run_module_e8_public_info_and_cycles(df: pd.DataFrame) -> None:
    print("\n" + "=" * 78)
    print("3. MODULE E8: LOUGHRAN-RITTER (2002) HARD-CAP PASS-THROUGH & HOT-ISSUE CYCLES")
    print("=" * 78)

    # Filter out recycled & split-distorted tickers for clean return regressions
    clean = df[(df["flag_recycled_or_transferred_ticker"] == 0) & (df["flag_reverse_split_distortion"] == 0)].copy()
    mb = clean[(clean["board"] == "Main Board") & (clean["has_exact_prospectus_date"] == True)].copy()
    mb["ir_wins"] = pd.to_numeric(mb["ir_close_pct"], errors="coerce").clip(lower=-90, upper=300)
    mb["log_ir"] = np.log1p(pd.to_numeric(mb["ir_close_pct"], errors="coerce").clip(lower=-95) / 100.0)
    mb["log_proceeds"] = np.log(pd.to_numeric(mb["funds_raised_total_hkd"], errors="coerce") / 1e6)

    # Piece-wise spline of Post-Prospectus Subscription-Window HSI Return (after P_max is printed!)
    mb["hsi_sub_pos"] = mb["hsi_ret_sub_window_pct"].clip(lower=0)
    mb["hsi_sub_neg"] = mb["hsi_ret_sub_window_pct"].clip(upper=0)
    mb["hsi_pre30_pos"] = mb["hsi_ret_pre30td_pct"].clip(lower=0)
    mb["hsi_pre30_neg"] = mb["hsi_ret_pre30td_pct"].clip(upper=0)

    sub_lr = mb.dropna(subset=["ir_wins", "log_ir", "hsi_ret_sub_window_pct", "hsi_ret_pre30td_pct", "log_proceeds"]).copy()
    sub_lr["day1_break"] = (sub_lr["ir_wins"] < 0).astype(int)

    m_sym = smf.ols("ir_wins ~ hsi_ret_sub_window_pct + hsi_ret_pre30td_pct + log_proceeds", data=sub_lr).fit(cov_type="HC3")
    m_asym = smf.ols("ir_wins ~ hsi_sub_pos + hsi_sub_neg + hsi_pre30_pos + hsi_pre30_neg + log_proceeds", data=sub_lr).fit(cov_type="HC3")
    m_log_asym = smf.ols("log_ir ~ hsi_sub_pos + hsi_sub_neg + hsi_pre30_pos + hsi_pre30_neg + log_proceeds", data=sub_lr).fit(cov_type="HC3")
    m_brk_asym = smf.ols("day1_break ~ hsi_sub_pos + hsi_sub_neg + hsi_pre30_pos + hsi_pre30_neg + log_proceeds", data=sub_lr).fit(cov_type="HC3")

    print(f"--- E8A: Public Market Return Pass-Through on Main Board (N = {int(m_asym.nobs)}) ---")
    for name, mod in [("Symmetric IR (%)", m_sym), ("Piece-wise Spline IR (%)", m_asym), ("Piece-wise Log(1+IR)", m_log_asym), ("Day-1 Break LPM", m_brk_asym)]:
        print(f"[{name}] R2 = {mod.rsquared:.4f}")
        for k in mod.params.index:
            print(f"  {k:26s}: coef={mod.params[k]:+.4f} (t_HC3={mod.tvalues[k]:+.2f}, p={mod.pvalues[k]:.4f})")

    # Test equality of positive vs negative slope during subscription window
    wald = m_asym.t_test("hsi_sub_pos = hsi_sub_neg")
    print(f"  Wald test [hsi_sub_pos == hsi_sub_neg]: diff={float(wald.effect[0]):+.4f}, t={float(wald.tvalue[0][0]):+.2f}, p={float(wald.pvalue):.4f}")

    # B. Monthly Hot-Issue Cycles (Lowry & Schwert 2002 vs Pastor & Veronesi 2005, T = 393 Months)
    valve = pd.read_csv(VALVE_CSV)
    ctp_rf = pd.read_csv(CTP_RF_CSV)[["year_month", "rf_monthly_pct"]]
    clean["ym"] = pd.to_datetime(clean["listing_date"]).dt.to_period("M").astype(str)
    clean["ir_c"] = pd.to_numeric(clean["ir_close_pct"], errors="coerce").clip(lower=-90, upper=300)

    mo_ir = clean.groupby("ym").agg(
        n_ipo_clean=("stock_code", "count"),
        mean_ir_mo=("ir_c", "mean"),
        med_ir_mo=("ir_c", "median"),
    ).reset_index().rename(columns={"ym": "year_month"})

    cyc = valve.merge(ctp_rf, on="year_month", how="left").merge(mo_ir, on="year_month", how="left")
    cyc["n_ipo_clean"] = cyc["n_ipo_clean"].fillna(0)
    cyc["hibor_1m_ann"] = cyc["rf_monthly_pct"] * 12.0

    # Rolling 3-month backward predictors [t-2, t] and forward 3-month issuance [t+1, t+3]
    cyc["fwd3m_ipo_count"] = cyc["hk_total_ipos"].shift(-1) + cyc["hk_total_ipos"].shift(-2) + cyc["hk_total_ipos"].shift(-3)
    cyc["log_fwd3m_count"] = np.log1p(cyc["fwd3m_ipo_count"])
    cyc["lag3m_count"] = np.log1p(cyc["hk_total_ipos"].rolling(3).sum())
    cyc["lag3m_hsi_ret"] = cyc["hsi_monthly_return_pct"].rolling(3).sum()
    cyc["lag3m_mean_ir"] = cyc["mean_ir_mo"].rolling(3, min_periods=1).mean()

    est_c = cyc.dropna(subset=["log_fwd3m_count", "lag3m_count", "lag3m_hsi_ret", "lag3m_mean_ir", "hibor_1m_ann"]).copy()
    m_cyc1 = smf.ols("log_fwd3m_count ~ lag3m_hsi_ret + lag3m_mean_ir + hibor_1m_ann", data=est_c).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
    m_cyc2 = smf.ols("log_fwd3m_count ~ lag3m_count + lag3m_hsi_ret + lag3m_mean_ir + hibor_1m_ann", data=est_c).fit(cov_type="HAC", cov_kwds={"maxlags": 6})

    print(f"\n--- E8B: Monthly Hot-Issue Cycle Regressions Predicting Future 3M IPO Volume (T = {int(m_cyc2.nobs)}) ---")
    for name, mod in [("Without AR Lag", m_cyc1), ("With AR Persistence Control", m_cyc2)]:
        print(f"[{name}] R2 = {mod.rsquared:.4f}")
        for k in mod.params.index:
            print(f"  {k:24s}: coef={mod.params[k]:+.4f} (t_NW={mod.tvalues[k]:+.2f}, p={mod.pvalues[k]:.4f})")

    # Autocorrelations of monthly volume and monthly mean IR
    ac_vol1 = cyc["hk_total_ipos"].autocorr(lag=1)
    ac_vol3 = cyc["hk_total_ipos"].autocorr(lag=3)
    ac_ir1 = cyc["mean_ir_mo"].dropna().autocorr(lag=1)
    print(f"  Monthly Autocorrelations: Volume rho(1)={ac_vol1:.3f}, rho(3)={ac_vol3:.3f} | Mean IR rho(1)={ac_ir1:.3f}")

    # Save summary CSV for E8
    e8_rows = [
        {"Model": "Post-Prospectus HSI Rally Slope (R_m > 0)", "Sample_N": int(m_asym.nobs), "Estimate": round(float(m_asym.params["hsi_sub_pos"]), 4), "t_stat": round(float(m_asym.tvalues["hsi_sub_pos"]), 2), "p_val": round(float(m_asym.pvalues["hsi_sub_pos"]), 4)},
        {"Model": "Post-Prospectus HSI Drop Slope (R_m < 0)", "Sample_N": int(m_asym.nobs), "Estimate": round(float(m_asym.params["hsi_sub_neg"]), 4), "t_stat": round(float(m_asym.tvalues["hsi_sub_neg"]), 2), "p_val": round(float(m_asym.pvalues["hsi_sub_neg"]), 4)},
        {"Model": "Pre-Prospectus 30d HSI Rally Slope", "Sample_N": int(m_asym.nobs), "Estimate": round(float(m_asym.params["hsi_pre30_pos"]), 4), "t_stat": round(float(m_asym.tvalues["hsi_pre30_pos"]), 2), "p_val": round(float(m_asym.pvalues["hsi_pre30_pos"]), 4)},
        {"Model": "Hot-Cycle: Lag 3M HSI -> Fwd 3M Log Volume", "Sample_N": int(m_cyc2.nobs), "Estimate": round(float(m_cyc2.params["lag3m_hsi_ret"]), 4), "t_stat": round(float(m_cyc2.tvalues["lag3m_hsi_ret"]), 2), "p_val": round(float(m_cyc2.pvalues["lag3m_hsi_ret"]), 4)},
        {"Model": "Hot-Cycle: Lag 3M Mean IR -> Fwd 3M Log Volume", "Sample_N": int(m_cyc2.nobs), "Estimate": round(float(m_cyc2.params["lag3m_mean_ir"]), 4), "t_stat": round(float(m_cyc2.tvalues["lag3m_mean_ir"]), 2), "p_val": round(float(m_cyc2.pvalues["lag3m_mean_ir"]), 4)},
        {"Model": "Hot-Cycle: HKMA 1M HIBOR -> Fwd 3M Log Volume", "Sample_N": int(m_cyc2.nobs), "Estimate": round(float(m_cyc2.params["hibor_1m_ann"]), 4), "t_stat": round(float(m_cyc2.tvalues["hibor_1m_ann"]), 2), "p_val": round(float(m_cyc2.pvalues["hibor_1m_ann"]), 4)},
    ]
    pd.DataFrame(e8_rows).to_csv(EXT_DIR / "ext_table12_public_info_and_hot_cycles.csv", index=False)


def run_module_e9_144a_secondary_and_bessembinder(df: pd.DataFrame) -> None:
    print("\n" + "=" * 78)
    print("4. MODULE E9: GLOBAL 144A DECOUPLING, SECONDARY SHARES & BESSEMBINDER WEALTH")
    print("=" * 78)

    mb = df[(df["board"] == "Main Board") & df["has_rule_144a"].notna()].copy()

    def get_win(yr):
        if yr <= 1999: return "1. 1994-1999 (Asian / Local Era)"
        elif yr <= 2007: return "2. 2000-2007 (WTO & SOE Privatization)"
        elif yr <= 2017: return "3. 2008-2017 (Global Institutional Peak)"
        elif yr <= 2020: return "4. 2018-2020 (Ch. 18A/19C Reform)"
        elif yr <= 2022: return "5. 2021-2022 (Pandemic Tech/Biotech Peak)"
        else: return "6. 2023-2026Q3 (U.S.-China Decoupling & CSRC Filing)"

    mb["period_6"] = mb["cohort_year"].apply(get_win)
    rows_144a = []
    for per, g in mb.groupby("period_6"):
        big1b = g[g["funds_raised_total_hkd"] >= 1e9]
        rows_144a.append({
            "Historical_Window": per,
            "N_MB_Matched": len(g),
            "Rule_144A_All_Pct": round(float(g["has_rule_144a"].mean() * 100), 2),
            "Reg_S_All_Pct": round(float(g["has_reg_s"].mean() * 100), 2),
            "N_Deals_Over_HKD1Bn": len(big1b),
            "Rule_144A_Over_HKD1Bn_Pct": round(float(big1b["has_rule_144a"].mean() * 100), 2) if len(big1b) else np.nan,
            "Secondary_Sale_Share_Pct": round(float(g["has_secondary_sale"].mean() * 100), 2),
            "Bulge_Bracket_Bookrunner_Pct": round(float(g["has_bb_bookrunner"].mean() * 100), 2),
        })

    df_144a = pd.DataFrame(rows_144a)
    df_144a.to_csv(EXT_DIR / "ext_table13_rule144a_decoupling_and_secondary.csv", index=False)
    print("--- E9A: Global Distribution Regimes (Rule 144A vs. Reg S) & Secondary Sales ---")
    print(df_144a.to_string(index=False))

    # Multivariate test of 2023-2026 Rule 144A Decoupling (2018-2026 modern Reg S tagged era)
    mod_era = mb[mb["cohort_year"] >= 2018].copy()
    mod_era["post_2023"] = (mod_era["cohort_year"] >= 2023).astype(int)
    mod_era["log_proceeds"] = np.log(pd.to_numeric(mod_era["funds_raised_total_hkd"], errors="coerce") / 1e6)
    mod_era["is_h"] = (mod_era["is_prc_joint_stock"] == 1).astype(int)
    mod_era["is_ah_clean"] = pd.to_numeric(mod_era["is_ah"], errors="coerce").fillna(0)
    mod_era["bb_br"] = pd.to_numeric(mod_era["has_bb_bookrunner"], errors="coerce").fillna(0)

    m144_1 = smf.ols("has_rule_144a ~ post_2023 + log_proceeds + is_h + is_ah_clean", data=mod_era).fit(cov_type="HC3")
    m144_2 = smf.ols("has_rule_144a ~ post_2023 + log_proceeds + is_h + is_ah_clean + bb_br", data=mod_era).fit(cov_type="HC3")
    print(f"\n[2018-2026 Rule 144A Probability Regressions, N = {int(m144_1.nobs)}]")
    for nm, md in [("Size & Legal Origin Controls", m144_1), ("Adding Wall St Bulge-Bracket Bookrunner", m144_2)]:
        print(f"  {nm} (R2={md.rsquared:.4f}): post_2023={md.params['post_2023']:+.4f} (t={md.tvalues['post_2023']:+.2f}), log_proceeds={md.params['log_proceeds']:+.4f} (t={md.tvalues['log_proceeds']:+.2f})" + (f", bb_br={md.params['bb_br']:+.4f} (t={md.tvalues['bb_br']:+.2f})" if "bb_br" in md.params else ""))

    # Secondary share sale signaling across 33Y Main Board
    mb_sec = mb.copy()
    mb_sec["log_proceeds"] = np.log(pd.to_numeric(mb_sec["funds_raised_total_hkd"], errors="coerce") / 1e6)
    mb_sec["log_ir"] = np.log1p(pd.to_numeric(mb_sec["ir_close_pct"], errors="coerce").clip(lower=-95) / 100.0)
    mb_sec["bhar_1y"] = pd.to_numeric(mb_sec["after_bhar_1y_pct"], errors="coerce")
    m_sec_ir = smf.ols("log_ir ~ has_secondary_sale + log_proceeds + C(epoch)", data=mb_sec).fit(cov_type="HC3")
    m_sec_1y = smf.ols("bhar_1y ~ has_secondary_sale + log_proceeds + C(epoch)", data=mb_sec).fit(cov_type="HC3")
    print("\n[Secondary Share Sales Signaling (33Y MB)]:")
    print(f"  Log(1+IR): coef={m_sec_ir.params['has_secondary_sale']:+.4f} (t={m_sec_ir.tvalues['has_secondary_sale']:+.2f}, N={int(m_sec_ir.nobs)})")
    print(f"  1Y BHAR %: coef={m_sec_1y.params['has_secondary_sale']:+.2f}% (t={m_sec_1y.tvalues['has_secondary_sale']:+.2f}, N={int(m_sec_1y.nobs)})")

    # C. Bessembinder (2018, JFE) Lifetime Return Skewness & Wealth Concentration (1994-2026)
    # Explicit 2,866 -> Verified Sample Attrition Audit (addressing survivorship & delisting accounting)
    n_tot = len(df)
    m_recycled = df["flag_recycled_or_transferred_ticker"].fillna(0) != 0
    m_revsplit = (~m_recycled) & df["flag_reverse_split_distortion"].fillna(False).astype(bool)
    m_split_unv = (~m_recycled) & (~m_revsplit) & df["flag_lifetime_split_unverified"].fillna(False).astype(bool)
    m_no_life_quote = (~m_recycled) & (~m_revsplit) & (~m_split_unv) & df["lifetime_offer_to_date_pct"].isna()
    m_verified = (~m_recycled) & (~m_revsplit) & (~m_split_unv) & df["lifetime_offer_to_date_pct"].notna()

    # Check delisted / near-total-loss status among missing quote rows using last 1Y/3Y market_cache price
    attrition_rows = [
        {"Step": "1. Gross HKEX Ordinary Equity IPO Universe (1994-2026Q3)", "Main_Board": int((df["board"] == "Main Board").sum()), "GEM": int((df["board"] == "GEM").sum()), "Total": int(n_tot)},
        {"Step": "2. Less: Recycled Ticker Codes / Ch. 9A GEM-to-MB Transfers", "Main_Board": int((m_recycled & (df["board"] == "Main Board")).sum()), "GEM": int((m_recycled & (df["board"] == "GEM")).sum()), "Total": int(m_recycled.sum())},
        {"Step": "3. Less: Unadjusted Reverse-Split / Consolidation Distortions", "Main_Board": int((m_revsplit & (df["board"] == "Main Board")).sum()), "GEM": int((m_revsplit & (df["board"] == "GEM")).sum()), "Total": int(m_revsplit.sum())},
        {"Step": "4. Less: Lifetime Split Factor Unverified Across Corporate Actions", "Main_Board": int((m_split_unv & (df["board"] == "Main Board")).sum()), "GEM": int((m_split_unv & (df["board"] == "GEM")).sum()), "Total": int(m_split_unv.sum())},
        {"Step": "5. Less: Delisted (Rule 6.01A / Privatized) Without Terminal Quote", "Main_Board": int((m_no_life_quote & (df["board"] == "Main Board")).sum()), "GEM": int((m_no_life_quote & (df["board"] == "GEM")).sum()), "Total": int(m_no_life_quote.sum())},
        {"Step": "6. Verified Split-Clean Terminal Wealth Sample", "Main_Board": int((m_verified & (df["board"] == "Main Board")).sum()), "GEM": int((m_verified & (df["board"] == "GEM")).sum()), "Total": int(m_verified.sum())},
    ]
    attr_df = pd.DataFrame(attrition_rows)
    attr_df.to_csv(EXT_DIR / "ext_table14b_bessembinder_attrition_audit.csv", index=False)
    print("\n--- E9C-Audit: Explicit Terminal Wealth Sample Attrition Accounting (2,866 -> Verified) ---")
    print(attr_df.to_string(index=False))

    # Also compute conservative lower-bound sensitivity imputing -100% (Rule 6.01A wipeout) vs last 3Y observed return for Step 5 delistings
    clean_nonrec_df = df[(~m_recycled) & (~m_revsplit) & (~m_split_unv)].copy()
    last_obs_ret = pd.to_numeric(clean_nonrec_df["lifetime_offer_to_date_pct"], errors="coerce")
    # Fallback to 1Y or 6M offer-to-horizon return for delisted firms missing terminal quote, else -95% distressed delisting bound
    fb_1y = pd.to_numeric(clean_nonrec_df["offer_to_1y_pct"], errors="coerce") if "offer_to_1y_pct" in clean_nonrec_df.columns else pd.Series(np.nan, index=clean_nonrec_df.index)
    fb_6m = pd.to_numeric(clean_nonrec_df["offer_to_6m_pct"], errors="coerce") if "offer_to_6m_pct" in clean_nonrec_df.columns else pd.Series(np.nan, index=clean_nonrec_df.index)
    fallback_ret = fb_1y.fillna(fb_6m).fillna(-95.0)
    clean_nonrec_df["lifetime_delist_imputed_pct"] = last_obs_ret.fillna(fallback_ret)
    print(
        f"  [Delisting-Imputed Sensitivity, N={len(clean_nonrec_df)}]: "
        f"Below Offer={float((clean_nonrec_df['lifetime_delist_imputed_pct'] < 0).mean()*100):.2f}%, "
        f"Median={float(clean_nonrec_df['lifetime_delist_imputed_pct'].median()):.2f}%"
    )

    bess = df[m_verified].copy()

    bess["proceeds_hkd_bn"] = pd.to_numeric(bess["funds_raised_total_hkd"], errors="coerce") / 1e9
    bess["gross_wealth_gain_bn"] = bess["proceeds_hkd_bn"] * (bess["lifetime_offer_to_date_pct"] / 100.0)

    bess_rows = []
    for grp_label, sub_b in [
        ("All HKEX Verified IPOs (1994-2026)", bess),
        ("HKEX Main Board", bess[bess["board"] == "Main Board"]),
        ("HKEX GEM", bess[bess["board"] == "GEM"]),
        ("Seasoned Cohorts >= 5 Years (1994-2021)", bess[bess["cohort_year"] <= 2021]),
    ]:
        n_b = len(sub_b)
        below_p0 = (sub_b["lifetime_offer_to_date_pct"] < 0).mean() * 100
        loss_50 = (sub_b["lifetime_offer_to_date_pct"] <= -50).mean() * 100
        loss_80 = (sub_b["lifetime_offer_to_date_pct"] <= -80).mean() * 100
        multibag_2x = (sub_b["lifetime_offer_to_date_pct"] >= 100).mean() * 100
        multibag_10x = (sub_b["lifetime_offer_to_date_pct"] >= 900).mean() * 100

        # Positive wealth concentration among IPOs with positive gross gain
        w_sorted = sub_b.dropna(subset=["gross_wealth_gain_bn"]).sort_values("gross_wealth_gain_bn", ascending=False)
        pos_gain_sum = w_sorted[w_sorted["gross_wealth_gain_bn"] > 0]["gross_wealth_gain_bn"].sum()
        net_gain_sum = w_sorted["gross_wealth_gain_bn"].sum()
        k_top1pct = max(1, int(round(0.01 * len(w_sorted))))
        k_top5pct = max(1, int(round(0.05 * len(w_sorted))))
        top1_share_gross_pos = w_sorted.head(k_top1pct)["gross_wealth_gain_bn"].sum() / pos_gain_sum * 100 if pos_gain_sum > 0 else np.nan
        top5_share_gross_pos = w_sorted.head(k_top5pct)["gross_wealth_gain_bn"].sum() / pos_gain_sum * 100 if pos_gain_sum > 0 else np.nan

        bess_rows.append({
            "Universe": grp_label,
            "N_Verified": n_b,
            "Mean_Lifetime_Ret_Pct": round(float(sub_b["lifetime_offer_to_date_pct"].mean()), 2),
            "Median_Lifetime_Ret_Pct": round(float(sub_b["lifetime_offer_to_date_pct"].median()), 2),
            "Below_Offer_Price_Pct": round(float(below_p0), 2),
            "Lost_50Pct_Plus_Pct": round(float(loss_50), 2),
            "Lost_80Pct_Plus_Pct": round(float(loss_80), 2),
            "Doubled_100Pct_Plus_Pct": round(float(multibag_2x), 2),
            "TenBagger_900Pct_Plus_Pct": round(float(multibag_10x), 2),
            "Net_Offered_Tranche_Wealth_HKD_Bn": round(float(net_gain_sum), 1),
            "Top_1Pct_Share_of_Gross_Creation_Pct": round(float(top1_share_gross_pos), 2),
            "Top_5Pct_Share_of_Gross_Creation_Pct": round(float(top5_share_gross_pos), 2),
        })

    df_bess = pd.DataFrame(bess_rows)
    df_bess.to_csv(EXT_DIR / "ext_table14_bessembinder_lifetime_wealth.csv", index=False)
    print("\n--- E9C: Bessembinder (2018) Lifetime Return Distribution & Wealth Concentration ---")
    print(df_bess.to_string(index=False))

    print("\nTop 10 Lifetime Compounders (Verified Split-Clean Universe):")
    top10 = bess.sort_values("lifetime_offer_to_date_pct", ascending=False).head(10)
    print(top10[["cohort_year", "stock_code", "company_name", "board", "lifetime_offer_to_date_pct", "gross_wealth_gain_bn"]].to_string(index=False))


def main() -> None:
    df = pd.read_csv(PANEL_CSV, low_memory=False)
    ctp = pd.read_csv(CTP_RF_CSV, low_memory=False)
    run_upgraded_ctp_with_hkma_rf(ctp)
    run_module_e7_hibor_and_fini(df)
    run_module_e8_public_info_and_cycles(df)
    run_module_e9_144a_secondary_and_bessembinder(df)
    print("\nALL FRONTIER ECONOMETRIC MODULES (E6.3 UPGRADE, E7, E8, E9) COMPLETED!")


if __name__ == "__main__":
    main()
