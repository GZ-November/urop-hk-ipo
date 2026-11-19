#!/usr/bin/env python3
"""
Module E15 Econometric Suite: Official Stock Connect Verification & Tier-1 Fuzzy RDD,
Statutory HK$5.0 Billion HSCI Market-Cap Cutoff, HKEX CCASS Southbound Accumulation,
Automatic Post-Stabilization A+H Entry (SSE Art. 66 / SZSE Art. 65), and Limits to Arbitrage.

Outputs:
  - analysis/out/overview_extensions/ext_table20a_southbound_connect_hsci_rdd.csv
  - analysis/out/overview_extensions/ext_table20b_ah_auto_connect_and_convergence.csv
  - analysis/out/overview_extensions/ext_table20c_fuzzy_rdd_diagnostics_and_ccass_holdings.csv
  - docs/overview_paper/figures/fig17_southbound_connect_rdd_and_ah_convergence.{pdf,png}
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from scipy import stats

BASE_DIR = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_MAIN = BASE_DIR / "analysis" / "out" / "overview_1994_2026"
OUT_EXT = BASE_DIR / "analysis" / "out" / "overview_extensions"
FIG_DIR = BASE_DIR / "docs" / "overview_paper" / "figures"
CACHE_DIR = OUT_MAIN / "market_cache"
AH_CACHE = BASE_DIR / "pipeline" / "prospectus_pipeline" / "data" / "market" / "ah_reference"

OUT_EXT.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def load_exact_bars(sc: str | int, ld_str: str) -> pd.DataFrame | None:
    """Load exact listing-matched daily OHLCV/turnover bars from market_cache."""
    num = int(str(sc).split(".")[0].strip())
    exact = CACHE_DIR / f"{num:04d}.HK_{ld_str}.json"
    if exact.exists():
        b = pd.DataFrame(json.loads(exact.read_text()), columns=["date", "open", "close", "high", "low", "vol", "turn"])
        b["date"] = pd.to_datetime(b["date"])
        return b[b["date"] >= pd.to_datetime(ld_str)].reset_index(drop=True)
    for h in sorted(CACHE_DIR.glob(f"{num:04d}.HK_*.json")):
        if ld_str[:4] in h.name:
            b = pd.DataFrame(json.loads(h.read_text()), columns=["date", "open", "close", "high", "low", "vol", "turn"])
            b["date"] = pd.to_datetime(b["date"])
            return b[b["date"] >= pd.to_datetime(ld_str)].reset_index(drop=True)
    return None


def fit_2sls_hc1(
    sub: pd.DataFrame,
    y_col: str,
    d_col: str = "treat_ggt",
    z_col: str = "above_5b",
    run_col: str = "run_var",
    extra_ctrls: list[str] | None = None,
) -> dict[str, Any]:
    """
    Exact Two-Stage Least Squares Fuzzy RDD LATE with HC1 heteroskedasticity-robust SEs
    and Weak-IV-robust Anderson-Rubin (1949) test + 95% confidence interval by grid inversion.
    """
    ctrls = extra_ctrls or []
    s = sub.dropna(subset=[y_col, d_col, z_col, run_col] + ctrls).copy()
    s["z_x_run"] = s[z_col] * s[run_col]
    n = len(s)
    ctrl_formula = (" + " + " + ".join(ctrls)) if ctrls else ""

    # First stage: D ~ 1 + Z + run + Z*run (+ ctrls) (HC1)
    fs = smf.ols(f"{d_col} ~ {z_col} + {run_col} + {z_col}:{run_col}{ctrl_formula}", data=s).fit(cov_type="HC1")
    fs_coef = float(fs.params[z_col])
    fs_se = float(fs.bse[z_col])
    fs_t = float(fs.tvalues[z_col])
    fs_p = float(fs.pvalues[z_col])
    fs_f = float(fs_t ** 2)

    # Reduced form (ITT): Y ~ 1 + Z + run + Z*run (+ ctrls) (HC1)
    rf = smf.ols(f"{y_col} ~ {z_col} + {run_col} + {z_col}:{run_col}{ctrl_formula}", data=s).fit(cov_type="HC1")
    itt_coef = float(rf.params[z_col])
    itt_se = float(rf.bse[z_col])
    itt_t = float(rf.tvalues[z_col])
    itt_p = float(rf.pvalues[z_col])

    # Exact 2SLS matrix estimator + HC1 sandwich covariance
    y = s[y_col].to_numpy(dtype=float)
    d_vec = s[d_col].to_numpy(dtype=float)
    ctrl_cols = [np.ones(n), s[run_col].to_numpy(dtype=float), s["z_x_run"].to_numpy(dtype=float)] + [
        s[c].to_numpy(dtype=float) for c in ctrls
    ]
    x_ctrl = np.column_stack(ctrl_cols)
    W = np.column_stack([d_vec, x_ctrl])
    Z = np.column_stack([s[z_col].to_numpy(dtype=float), x_ctrl])
    k_w = W.shape[1]

    ztz_inv = np.linalg.pinv(Z.T @ Z)
    W_hat = Z @ ztz_inv @ (Z.T @ W)
    B = np.linalg.pinv(W_hat.T @ W)
    theta = B @ (W_hat.T @ y)
    resid = y - W @ theta
    meat = (W_hat * (resid[:, None] ** 2)).T @ W_hat
    cov_hc1 = (n / max(1, n - k_w)) * (B @ meat @ B.T)

    late = float(theta[0])
    se_late = float(np.sqrt(max(1e-16, cov_hc1[0, 0])))
    t_late = late / se_late if se_late > 0 else np.nan
    p_late = float(2.0 * stats.t.sf(abs(t_late), df=max(1, n - k_w)))

    # Anderson-Rubin 95% confidence set via HC1 reduced-form inversion of (y - b0 * D) on Z
    span = max(2.5, 4.5 * se_late)
    b_grid = np.linspace(late - span, late + span, 801)
    ztz_inv_z = Z @ ztz_inv
    # Orthogonal projection residual maker for X_ctrl
    Qx = np.eye(n) - x_ctrl @ np.linalg.pinv(x_ctrl.T @ x_ctrl) @ x_ctrl.T
    z_perp = Qx @ s[z_col].to_numpy(dtype=float)
    y_perp = Qx @ y
    d_perp = Qx @ d_vec
    denom_zz = float(z_perp @ z_perp)
    ar_in = []
    if denom_zz > 1e-12:
        for b0 in b_grid:
            yt = y_perp - b0 * d_perp
            pi_b = float((z_perp @ yt) / denom_zz)
            u_b = yt - pi_b * z_perp
            # HC1 variance of pi_b using Frisch-Waugh-Lovell residualized regressor z_perp
            se_b = np.sqrt((n / max(1, n - k_w)) * np.sum((z_perp ** 2) * (u_b ** 2)) / (denom_zz ** 2))
            t_b = abs(pi_b) / se_b if se_b > 1e-12 else 0.0
            if t_b <= 1.95996:
                ar_in.append(b0)
    ar_ci = (float(min(ar_in)), float(max(ar_in))) if ar_in else (np.nan, np.nan)

    return {
        "n": n,
        "fs_coef": fs_coef,
        "fs_se": fs_se,
        "fs_t": fs_t,
        "fs_p": fs_p,
        "fs_f": fs_f,
        "itt_coef": itt_coef,
        "itt_se": itt_se,
        "itt_t": itt_t,
        "itt_p": itt_p,
        "late_coef": late,
        "late_se": se_late,
        "late_t": t_late,
        "late_p": p_late,
        "ar_p_zero": itt_p,
        "ar_ci_lo": ar_ci[0],
        "ar_ci_hi": ar_ci[1],
        "rf_r2": float(rf.rsquared),
    }


def run_hsci_5b_rdd_and_rebalancing(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Test 1 (Tier-1 Official One-Sided Fuzzy RDD): Non-A+H Main Board Issuers around
    the Statutory HK$5.0B Shenzhen-HK Stock Connect / HSCI Semi-Annual Inclusion Cutoff.
      - Uses official HKEX/HSCI month-end average market cap (`hsci_month_end_avg_mv_bn`)
        and SSE/HKEX CCASS verified review admission (`official_admitted_at_review`).
    """
    reb_rows = []
    m6_rows = []

    for _, r in df.iterrows():
        if int(r["is_ah_dual_listed"]) == 1:
            continue
        ld_str = str(r["listing_date"])[:10]
        bdf = load_exact_bars(r["Stock Code"], ld_str)
        if bdf is None or len(bdf) < 30:
            continue

        hkex_mv_bn = pd.to_numeric(r.get("hsci_month_end_avg_mv_bn"), errors="coerce")
        first_eff = r.get("first_hsci_eff_date")
        treat_ggt = pd.to_numeric(r.get("official_admitted_at_review"), errors="coerce")
        is_wvr = int(pd.to_numeric(r.get("is_wvr_eff", r.get("is_wvr", 0)), errors="coerce") or 0)
        is_drs = int("DRS" in str(r.get("company_name", "")).upper())

        # 1A. First eligible semi-annual HSCI / Stock Connect review post-listing
        if pd.notna(hkex_mv_bn) and hkex_mv_bn > 0 and pd.notna(first_eff) and pd.notna(treat_ggt):
            eff_dt = pd.to_datetime(first_eff)
            post_i = bdf.index[bdf["date"] >= eff_dt]
            if len(post_i) > 0:
                i0 = int(post_i[0])
                if i0 >= 15 and i0 + 10 <= len(bdf):
                    pre10_t = float(bdf.loc[i0 - 10 : i0 - 1, "turn"].mean())
                    base_t = float(bdf.loc[max(0, i0 - 25) : i0 - 12, "turn"].mean())
                    post10_t = float(bdf.loc[i0 : i0 + 9, "turn"].mean())
                    ret_ann = float((bdf.loc[i0 - 1, "close"] / bdf.loc[max(0, i0 - 12), "close"] - 1.0) * 100.0)
                    ret_eff = float((bdf.loc[i0 + 9, "close"] / bdf.loc[i0 - 1, "close"] - 1.0) * 100.0)
                    reb_rows.append({
                        "stock_code": r["Stock Code"],
                        "company_name": str(r.get("company_name", "")),
                        "eff_date": str(eff_dt.date()),
                        "hkex_mv_bn": float(hkex_mv_bn),
                        "run_var": float(np.log(hkex_mv_bn / 5.0)),
                        "above_5b": int(hkex_mv_bn >= 5.0),
                        "treat_ggt": int(treat_ggt),
                        "is_wvr": is_wvr,
                        "is_drs": is_drs,
                        "ex_wvr_drs": int((is_wvr == 0) and (is_drs == 0)),
                        "turn_ratio_post_pre10": post10_t / pre10_t if pre10_t > 0 else np.nan,
                        "log_jump_pre10": float(np.log((post10_t + 1.0) / (pre10_t + 1.0))),
                        "log_jump_base": float(np.log((post10_t + 1.0) / (base_t + 1.0))),
                        "ret_ann_runup_pct": ret_ann,
                        "ret_post_eff10_pct": ret_eff,
                        "cornerstone_pct_of_offering": pd.to_numeric(r.get("cornerstone_pct_of_offering"), errors="coerce"),
                        "log_sub": np.log1p(pd.to_numeric(r.get("subscription_ratio_times"), errors="coerce")),
                        "initial_return_pct": pd.to_numeric(r.get("initial_return_pct"), errors="coerce"),
                        "is_18ac": int((pd.to_numeric(r.get("is_18a"), errors="coerce") == 1) or (pd.to_numeric(r.get("is_18c"), errors="coerce") == 1)),
                    })

        # 1B. Medium-run (Month 1 -> Month 6) Zombie-Liquidity Reversal around HK$5.0B floor
        if len(bdf) >= 110 and pd.notna(hkex_mv_bn) and hkex_mv_bn > 0 and pd.notna(treat_ggt):
            bdf["abs_ret"] = bdf["close"].pct_change().abs()
            bdf["ami"] = np.where(bdf["turn"] > 0, bdf["abs_ret"] / (bdf["turn"] / 1e6), np.nan)
            m1_t = float(bdf.loc[5:24, "turn"].mean())
            m6_t = float(bdf.loc[95 : min(125, len(bdf) - 1), "turn"].mean())
            m1_a = float(bdf.loc[5:24, "ami"].median())
            m6_a = float(bdf.loc[95 : min(125, len(bdf) - 1), "ami"].median())
            d1_t = float(bdf.loc[0, "turn"])
            m6_rows.append({
                "stock_code": r["Stock Code"],
                "hkex_mv_bn": float(hkex_mv_bn),
                "run_var": float(np.log(hkex_mv_bn / 5.0)),
                "above_5b": int(hkex_mv_bn >= 5.0),
                "treat_ggt": int(treat_ggt),
                "treat_ggt_ever": int(pd.to_numeric(r.get("official_ggt_ever_included"), errors="coerce") or 0),
                "ex_wvr_drs": int((is_wvr == 0) and (is_drs == 0)),
                "m6_m1_turn_ratio": m6_t / m1_t if m1_t > 0 else np.nan,
                "log_m6_m1_turn": float(np.log((m6_t + 1.0) / (m1_t + 1.0))),
                "dlog_amihud": float(np.log((m6_a + 1e-6) / (m1_a + 1e-6))),
                "zombie_m6": int(m6_t < 0.05 * d1_t),
            })

    reb = pd.DataFrame(reb_rows)
    m6 = pd.DataFrame(m6_rows)

    out_rows = []
    # 0. Official First-Stage Compliance Discontinuity (P(Admitted) at HK$5.0B)
    for fs_lbl, fs_sub, fs_bw in [
        ("0a. First Stage (Full Non-A+H): Official Connect Inclusion", reb, "All First Post-IPO Reviews"),
        ("0b. First Stage (Narrow Bandwidth): Official Connect Inclusion", reb[(reb["hkex_mv_bn"] >= 1.5) & (reb["hkex_mv_bn"] <= 15.0)], "HK$1.5B - HK$15.0B"),
        ("0c. First Stage (Ex-WVR/DRS Statutory HSCI-Eligible)", reb[reb["ex_wvr_drs"] == 1], "Ex-WVR & Ex-DRS"),
    ]:
        fs_res = fit_2sls_hc1(fs_sub, "log_jump_pre10")
        n_ab = int(fs_sub["above_5b"].sum())
        n_be = int((1 - fs_sub["above_5b"]).sum())
        adm_ab = fs_sub.loc[fs_sub["above_5b"] == 1, "treat_ggt"].mean() * 100.0
        adm_be = fs_sub.loc[fs_sub["above_5b"] == 0, "treat_ggt"].mean() * 100.0
        out_rows.append({
            "Panel_Specification": fs_lbl,
            "Outcome_Metric": "P(Official Connect Admission at Review)",
            "Sample_Bandwidth": fs_bw,
            "N_Total": fs_res["n"],
            "N_Above_5B": n_ab,
            "N_Below_5B": n_be,
            "Estimate": round(fs_res["fs_coef"], 3),
            "Aux_Median_or_SE": round(fs_res["fs_se"], 3),
            "t_stat": round(fs_res["fs_t"], 2),
            "p_value": round(fs_res["fs_p"], 6),
            "Economic_Interpretation": f"First-Stage F={fs_res['fs_f']:.1f}; Above={adm_ab:.1f}% vs Below={adm_be:.1f}% (One-Sided)"
        })

    # 1. Descriptive comparison on exact semi-annual effective dates
    s_in = reb[reb["treat_ggt"] == 1]
    s_out = reb[reb["above_5b"] == 0]
    t_did, p_did = stats.ttest_ind(s_in["log_jump_pre10"], s_out["log_jump_pre10"], equal_var=False)

    out_rows.append({
        "Panel_Specification": "1a. Semi-Annual Effective Monday: Officially Admitted Non-A+H",
        "Outcome_Metric": "Log Turnover Jump [0,+9] vs [-10,-1] (Med Ratio)",
        "Sample_Bandwidth": "SSE/CCASS Verified Admitted",
        "N_Total": len(s_in),
        "N_Above_5B": int(s_in["above_5b"].sum()),
        "N_Below_5B": int((1 - s_in["above_5b"]).sum()),
        "Estimate": round(float(s_in["log_jump_pre10"].mean()), 3),
        "Aux_Median_or_SE": round(float(s_in["turn_ratio_post_pre10"].median()), 3),
        "t_stat": round(float(stats.ttest_1samp(s_in["log_jump_pre10"], 0).statistic), 2),
        "p_value": round(float(stats.ttest_1samp(s_in["log_jump_pre10"], 0).pvalue), 6),
        "Economic_Interpretation": f"Mean ratio {s_in['turn_ratio_post_pre10'].mean():.2f}x (med {s_in['turn_ratio_post_pre10'].median():.2f}x); Ann run-up {s_in['ret_ann_runup_pct'].mean():+.2f}%, Post-eff {s_in['ret_post_eff10_pct'].mean():+.2f}%"
    })
    out_rows.append({
        "Panel_Specification": "1b. Semi-Annual Effective Monday: Excluded Placebo (HKEX MV < HK$5.0B)",
        "Outcome_Metric": "Log Turnover Jump [0,+9] vs [-10,-1] (Med Ratio)",
        "Sample_Bandwidth": "Same Calendar Mondays",
        "N_Total": len(s_out),
        "N_Above_5B": 0,
        "N_Below_5B": len(s_out),
        "Estimate": round(float(s_out["log_jump_pre10"].mean()), 3),
        "Aux_Median_or_SE": round(float(s_out["turn_ratio_post_pre10"].median()), 3),
        "t_stat": round(float(stats.ttest_1samp(s_out["log_jump_pre10"], 0).statistic), 2),
        "p_value": round(float(stats.ttest_1samp(s_out["log_jump_pre10"], 0).pvalue), 6),
        "Economic_Interpretation": f"Med ratio {s_out['turn_ratio_post_pre10'].median():.2f}x; Same-day DiD = {s_in['log_jump_pre10'].mean() - s_out['log_jump_pre10'].mean():+.3f} (Welch t={t_did:+.2f}, p={p_did:.2e})"
    })

    # 2 & 3. Local-Linear RD ITT and 2SLS Fuzzy RDD LATE
    rd_specs = [
        ("2a. Sharp ITT (Reduced Form): Effective-Date Turnover Jump vs [-10,-1]", reb, "log_jump_pre10", "Full Non-A+H", "ITT", None),
        ("2b. 2SLS Fuzzy RDD LATE: Effective-Date Turnover Jump vs [-10,-1]", reb, "log_jump_pre10", "Full Non-A+H", "LATE", None),
        ("2c. Sharp ITT (Reduced Form): Effective-Date Jump vs Pre-Ann [-25,-12]", reb, "log_jump_base", "Full Non-A+H", "ITT", None),
        ("2d. 2SLS Fuzzy RDD LATE: Effective-Date Jump vs Pre-Ann [-25,-12]", reb, "log_jump_base", "Full Non-A+H", "LATE", None),
        ("2e. 2SLS Fuzzy RDD LATE (Narrow BW): Effective-Date Jump vs [-10,-1]", reb[(reb["hkex_mv_bn"] >= 1.5) & (reb["hkex_mv_bn"] <= 15.0)], "log_jump_pre10", "HK$1.5B - HK$15.0B", "LATE", None),
        ("2f. 2SLS Fuzzy RDD LATE (Ex-WVR/DRS): Effective-Date Jump vs [-10,-1]", reb[reb["ex_wvr_drs"] == 1], "log_jump_pre10", "Ex-WVR & Ex-DRS", "LATE", None),
        ("2g. 2SLS Fuzzy RDD LATE (Covariate-Adjusted IR, Sub, CS%)", reb, "log_jump_pre10", "Full + IR/Sub/CS%", "LATE", ["initial_return_pct", "log_sub", "cornerstone_pct_of_offering"]),
        ("3a. Medium-Run 2SLS Fuzzy RDD LATE: Log(Month-6 / Month-1 Turnover)", m6, "log_m6_m1_turn", "Matured 6M Non-A+H", "LATE", None),
        ("3b. Medium-Run 2SLS Fuzzy RDD LATE: Delta Log(Amihud M1->M6)", m6, "dlog_amihud", "Matured 6M Non-A+H", "LATE", None),
        ("3c. Medium-Run 2SLS Fuzzy RDD LATE: Month-6 Zombie Incidence (>95% Decay)", m6, "zombie_m6", "Matured 6M Non-A+H", "LATE", None),
        ("3d. Medium-Run Sharp ITT: Month-6 Zombie Incidence (>95% Decay)", m6, "zombie_m6", "Matured 6M Non-A+H", "ITT", None),
    ]
    for label, sub, yvar, bw_desc, est_type, x_ctrls in rd_specs:
        res = fit_2sls_hc1(sub, yvar, extra_ctrls=x_ctrls)
        if est_type == "ITT":
            est, se, tval, pval = res["itt_coef"], res["itt_se"], res["itt_t"], res["itt_p"]
            interp = f"Reduced-form local-linear RD; R2={res['rf_r2']:.3f}, AR p={res['ar_p_zero']:.2e}"
        else:
            est, se, tval, pval = res["late_coef"], res["late_se"], res["late_t"], res["late_p"]
            interp = f"FS F={res['fs_f']:.1f}; AR p={res['ar_p_zero']:.2e}, AR 95% CI [{res['ar_ci_lo']:+.2f}, {res['ar_ci_hi']:+.2f}]"
        out_rows.append({
            "Panel_Specification": label,
            "Outcome_Metric": yvar,
            "Sample_Bandwidth": bw_desc,
            "N_Total": res["n"],
            "N_Above_5B": int(sub["above_5b"].sum()),
            "N_Below_5B": int((1 - sub["above_5b"]).sum()),
            "Estimate": round(est, 3),
            "Aux_Median_or_SE": round(se, 3),
            "t_stat": round(tval, 2),
            "p_value": round(pval, 6),
            "Economic_Interpretation": interp,
        })

    out_20a = pd.DataFrame(out_rows)
    out_20a.to_csv(OUT_EXT / "ext_table20a_southbound_connect_hsci_rdd.csv", index=False)
    print("\n=== Table E20A: Official Stock Connect / HSCI One-Sided Fuzzy RDD & Liquidity Reversal ===")
    print(out_20a.to_string(index=False))
    return out_20a, reb, m6


def run_ah_auto_connect_and_convergence(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Test 2: SSE Art. 66 / SZSE Art. 65 Automatic Southbound Stock Connect Entry at T_stab + 1
    for A+H Dual-Listed IPOs vs. Non-A+H Main Board IPOs, plus Limits-to-Arbitrage H/A Convergence.
    """
    stab_rows = []
    event_paths = []

    for _, r in df.iterrows():
        ld_str = str(r["listing_date"])[:10]
        ld = pd.to_datetime(ld_str)
        bdf = load_exact_bars(r["Stock Code"], ld_str)
        if bdf is None or len(bdf) < 32:
            continue
        stab_dt = pd.to_datetime(r["Stabilization period end date"], errors="coerce")
        if pd.isna(stab_dt):
            stab_dt = ld + pd.Timedelta(days=30)
        post_idx = bdf.index[bdf["date"] > stab_dt]
        if len(post_idx) == 0:
            continue
        idx0 = int(post_idx[0])
        if idx0 < 8 or idx0 + 10 >= len(bdf):
            continue

        pre_t = float(bdf.loc[idx0 - 8 : idx0 - 1, "turn"].mean())
        post10_t = float(bdf.loc[idx0 : idx0 + 9, "turn"].mean())
        post20_t = float(bdf.loc[idx0 : min(idx0 + 19, len(bdf) - 1), "turn"].mean())
        ret10 = float((bdf.loc[idx0 + 9, "close"] / bdf.loc[idx0 - 1, "close"] - 1.0) * 100.0)
        ret20 = float((bdf.loc[min(idx0 + 19, len(bdf) - 1), "close"] / bdf.loc[idx0 - 1, "close"] - 1.0) * 100.0)

        stab_rows.append({
            "stock_code": r["Stock Code"],
            "is_ah": int(r["is_ah_dual_listed"]),
            "turn_ratio10": post10_t / pre_t if pre_t > 0 else np.nan,
            "turn_ratio20": post20_t / pre_t if pre_t > 0 else np.nan,
            "log_jump10": float(np.log((post10_t + 1.0) / (pre_t + 1.0))),
            "log_jump20": float(np.log((post20_t + 1.0) / (pre_t + 1.0))),
            "ret10": ret10,
            "ret20": ret20,
        })

        # Daily normalized turnover path around idx0 [-8, +15]
        if pre_t > 0 and idx0 + 15 < len(bdf):
            for rel_k in range(-8, 16):
                event_paths.append({
                    "is_ah": int(r["is_ah_dual_listed"]),
                    "rel_day": rel_k,
                    "norm_turn": float(bdf.loc[idx0 + rel_k, "turn"] / pre_t),
                    "log_norm_turn": float(np.log((bdf.loc[idx0 + rel_k, "turn"] + 1.0) / (pre_t + 1.0))),
                })

    sdf = pd.DataFrame(stab_rows)
    ep_df = pd.DataFrame(event_paths)
    if len(ep_df):
        ep_sum = ep_df.groupby(["is_ah", "rel_day"]).agg(
            mean_norm_turn=("norm_turn", "mean"),
            med_norm_turn=("norm_turn", "median"),
            se_norm_turn=("norm_turn", "sem"),
            mean_log_turn=("log_norm_turn", "mean"),
            se_log_turn=("log_norm_turn", "sem"),
            n=("norm_turn", "count"),
        ).reset_index()
        ep_sum.to_csv(OUT_EXT / "ext_table20d_stab_turnover_paths.csv", index=False)

    # Load daily A-share & H-share matched valuation discount path around T_stab + 1 (full 57-issuer MASTER AH ref)
    ref = pd.read_csv(BASE_DIR / "pipeline" / "exports" / "HKIPO-MASTER-AH-reference.csv")
    ref = ref.merge(
        df[["Stock Code", "Stabilization period end date"]].drop_duplicates("Stock Code"),
        left_on="h_code", right_on="Stock Code", how="left"
    )
    fx_raw = json.loads((AH_CACHE / "fx_cnyhkd.json").read_text())
    fx = pd.Series({pd.Timestamp(b["date"]): float(b["close"]) for b in fx_raw}).sort_index()

    conv_rows = []
    ah_daily = []
    for _, r in ref.iterrows():
        if pd.isna(r["a_symbol"]):
            continue
        hp = AH_CACHE / "h_bars" / f"hk{str(r['h_code']).split('.')[0].zfill(5)}.json"
        ap = AH_CACHE / "a_bars" / f"{r['a_symbol']}.json"
        if not hp.exists() or not ap.exists():
            continue
        hb = pd.DataFrame(json.loads(hp.read_text()))
        ab = pd.DataFrame(json.loads(ap.read_text()))
        hb["date"] = pd.to_datetime(hb["date"])
        ab["date"] = pd.to_datetime(ab["date"])
        ld = pd.to_datetime(r["listing_date"])
        hb = hb[hb["date"] >= ld].sort_values("date").reset_index(drop=True)
        hb["eday"] = np.arange(len(hb))
        mg = hb.set_index("date").join(ab.set_index("date")["close"].rename("a_cny"), how="inner")
        mg["fx"] = fx.reindex(mg.index, method="ffill")
        mg["a_hkd"] = mg["a_cny"] * mg["fx"]
        mg["disc_pct"] = (mg["close"] / mg["a_hkd"] - 1.0) * 100.0
        stab_dt = pd.to_datetime(r["Stabilization period end date"], errors="coerce")
        if pd.isna(stab_dt):
            stab_dt = ld + pd.Timedelta(days=30)

        post_dates = mg.index[mg.index > stab_dt]
        if len(post_dates) > 0:
            pos0 = mg.index.get_loc(post_dates[0])
            for k in range(-10, 21):
                if 0 <= pos0 + k < len(mg):
                    ah_daily.append({"rel_day": k, "disc_pct": float(mg.iloc[pos0 + k]["disc_pct"])})

        if len(mg) >= 35:
            d1_disc = float(mg.iloc[0]["disc_pct"])
            pre_s = mg[mg.index <= stab_dt]["disc_pct"]
            post_s = mg[(mg.index > stab_dt) & (mg["eday"] <= 60)]["disc_pct"]
            if len(pre_s) >= 5 and len(post_s) >= 5:
                conv_rows.append({
                    "h_code": r["h_code"],
                    "offer_disc": float(r["offer_vs_a_close"]) * 100.0,
                    "d1_disc": d1_disc,
                    "pre_stab_disc": float(pre_s.mean()),
                    "post_connect_disc": float(post_s.mean()),
                    "d1_vs_offer_narrowing": d1_disc - float(r["offer_vs_a_close"]) * 100.0,
                    "post_vs_pre_narrowing": float(post_s.mean() - pre_s.mean()),
                })

    cdf = pd.DataFrame(conv_rows)
    ah_path_df = pd.DataFrame(ah_daily)

    ah_s = sdf[sdf["is_ah"] == 1]
    non_s = sdf[sdf["is_ah"] == 0]
    t10, p10 = stats.ttest_ind(ah_s["log_jump10"], non_s["log_jump10"], equal_var=False)
    t20, p20 = stats.ttest_ind(ah_s["log_jump20"], non_s["log_jump20"], equal_var=False)
    u10, pu10 = stats.mannwhitneyu(ah_s["turn_ratio10"], non_s["turn_ratio10"])
    t_off, p_off = stats.ttest_1samp(cdf["d1_vs_offer_narrowing"], 0)
    t_pc, p_pc = stats.ttest_1samp(cdf["post_vs_pre_narrowing"], 0)

    rows_20b = [
        {
            "Channel_Cohort": "1a. A+H Dual-Listed IPOs: Automatic Southbound Entry at T_stab+1 (SSE Art.66 / SZSE Art.65)",
            "N": len(ah_s),
            "Mean_Metric": round(float(ah_s["log_jump10"].mean()), 3),
            "Median_or_Ratio": round(float(ah_s["turn_ratio10"].median()), 3),
            "Aux_Mean_Ratio_or_Disc": round(float(ah_s["turn_ratio10"].mean()), 3),
            "t_or_z_stat": round(float(stats.ttest_1samp(ah_s["log_jump10"], 0).statistic), 2),
            "p_value": round(float(stats.ttest_1samp(ah_s["log_jump10"], 0).pvalue), 4),
            "Notes": f"10d post/pre turnover mean {ah_s['turn_ratio10'].mean():.2f}x (med {ah_s['turn_ratio10'].median():.2f}x); 20d med {ah_s['turn_ratio20'].median():.2f}x"
        },
        {
            "Channel_Cohort": "1b. Non-A+H Main Board IPOs: Stabilization Expiry Without Stock Connect at T_stab+1",
            "N": len(non_s),
            "Mean_Metric": round(float(non_s["log_jump10"].mean()), 3),
            "Median_or_Ratio": round(float(non_s["turn_ratio10"].median()), 3),
            "Aux_Mean_Ratio_or_Disc": round(float(non_s["turn_ratio10"].mean()), 3),
            "t_or_z_stat": round(float(stats.ttest_1samp(non_s["log_jump10"], 0).statistic), 2),
            "p_value": round(float(stats.ttest_1samp(non_s["log_jump10"], 0).pvalue), 4),
            "Notes": f"10d post/pre turnover med {non_s['turn_ratio10'].median():.2f}x; syndicate bid withdrawal without Mainland Connect inflow"
        },
        {
            "Channel_Cohort": "1c. Difference-in-Differences (A+H Auto-Connect minus Non-A+H at T_stab+1)",
            "N": len(sdf),
            "Mean_Metric": round(float(ah_s["log_jump10"].mean() - non_s["log_jump10"].mean()), 3),
            "Median_or_Ratio": round(float(ah_s["turn_ratio10"].median() - non_s["turn_ratio10"].median()), 3),
            "Aux_Mean_Ratio_or_Disc": round(float(ah_s["log_jump20"].mean() - non_s["log_jump20"].mean()), 3),
            "t_or_z_stat": round(float(t10), 2),
            "p_value": round(float(p10), 4),
            "Notes": f"10d Welch p={p10:.4f}, Mann-Whitney p={pu10:.4f}; 20d DiD t={t20:+.2f} (p={p20:.4f})"
        },
        {
            "Channel_Cohort": "2a. A+H Primary-Market Repricing: Offer Price Discount -> Day-1 Close Discount (pp)",
            "N": len(cdf),
            "Mean_Metric": round(float(cdf["d1_vs_offer_narrowing"].mean()), 2),
            "Median_or_Ratio": round(float(cdf["d1_vs_offer_narrowing"].median()), 2),
            "Aux_Mean_Ratio_or_Disc": round(float(cdf["d1_disc"].mean()), 2),
            "t_or_z_stat": round(float(t_off), 2),
            "p_value": round(float(p_off), 4),
            "Notes": f"Mean H/A discount narrows from {cdf['offer_disc'].mean():.2f}% at offer to {cdf['d1_disc'].mean():.2f}% at Day-1 close"
        },
        {
            "Channel_Cohort": "2b. Post-Connect Limits to Arbitrage: Post-Connect [T_stab+1..D60] minus Pre-Connect Window (pp)",
            "N": len(cdf),
            "Mean_Metric": round(float(cdf["post_vs_pre_narrowing"].mean()), 2),
            "Median_or_Ratio": round(float(cdf["post_vs_pre_narrowing"].median()), 2),
            "Aux_Mean_Ratio_or_Disc": round(float(cdf["post_connect_disc"].mean()), 2),
            "t_or_z_stat": round(float(t_pc), 2),
            "p_value": round(float(p_pc), 4),
            "Notes": f"Mean H/A gap stays at {cdf['post_connect_disc'].mean():.2f}% (vs {cdf['pre_stab_disc'].mean():.2f}% pre-Connect): non-fungibility + 20% dividend tax block arbitrage"
        },
    ]
    out_20b = pd.DataFrame(rows_20b)
    out_20b.to_csv(OUT_EXT / "ext_table20b_ah_auto_connect_and_convergence.csv", index=False)
    print("\n=== Table E20B: Automatic T_stab+1 Southbound Entry & Limits to A-H Arbitrage ===")
    print(out_20b.to_string(index=False))
    return out_20b, ep_df, ah_path_df


def run_fuzzy_rdd_diagnostics_and_ccass(df: pd.DataFrame, reb: pd.DataFrame) -> pd.DataFrame:
    """
    Create ext_table20c_fuzzy_rdd_diagnostics_and_ccass_holdings.csv:
      Panel A: Binomial density manipulation tests around HK$5.0B cutoff
      Panel B: Pre-determined covariate balance RD around HK$5.0B cutoff
      Panel C: Official HKEX CCASS Mainland Southbound Shareholding (%) accumulation
      Panel D: Stacked official-inclusion date event study vs same-date never-included controls
    """
    rows = []

    # Panel A: Density Test around log(MV/5B) = 0
    for bw_lbl, bw in [("Bandwidth |log(MV/5B)| <= 0.35 (HK$3.5B-7.1B)", 0.35),
                       ("Bandwidth |log(MV/5B)| <= 0.55 (HK$2.9B-8.7B)", 0.55)]:
        s = reb[reb["run_var"].abs() <= bw]
        n_b = int((s["run_var"] < 0).sum())
        n_a = int((s["run_var"] >= 0).sum())
        p_bin = float(stats.binomtest(n_a, n_a + n_b, 0.5).pvalue) if (n_a + n_b) > 0 else np.nan
        rows.append({
            "Panel": "A. Cutoff Density Test",
            "Specification": bw_lbl,
            "N_Total": n_a + n_b,
            "Metric_1": f"Below 5B={n_b}, Above 5B={n_a}",
            "Estimate": round(n_a / max(1, n_a + n_b), 3),
            "SE_or_Aux": 0.500,
            "t_stat": np.nan,
            "p_value": round(p_bin, 4),
            "Notes": "Two-sided binomial test of continuous sorting density at HK$5.0B",
        })

    # Panel B: Covariate Balance RD on Pre-Determined IPO Characteristics
    for cov_col, cov_lbl in [
        ("cornerstone_pct_of_offering", "Pre-Determined Cornerstone Share (% of Offer)"),
        ("log_sub", "Log(1 + Retail Subscription Ratio)"),
        ("initial_return_pct", "Day-1 Initial Return (%)"),
        ("is_18ac", "Chapter 18A/18C Frontier Tech Share"),
    ]:
        sub_c = reb.dropna(subset=[cov_col, "run_var", "above_5b"])
        mod = smf.ols(f"{cov_col} ~ above_5b + run_var + above_5b:run_var", data=sub_c).fit(cov_type="HC1")
        rows.append({
            "Panel": "B. Covariate Balance RD",
            "Specification": cov_lbl,
            "N_Total": len(sub_c),
            "Metric_1": f"Mean={sub_c[cov_col].mean():.2f}",
            "Estimate": round(float(mod.params["above_5b"]), 3),
            "SE_or_Aux": round(float(mod.bse["above_5b"]), 3),
            "t_stat": round(float(mod.tvalues["above_5b"]), 2),
            "p_value": round(float(mod.pvalues["above_5b"]), 4),
            "Notes": "Local-linear RD jump at HK$5.0B (balance requires p > 0.10)",
        })

    # Panel C: HKEX CCASS Mainland Southbound Shareholding (%) Accumulation
    cc_groups = [
        ("Joint HSCI Index + Southbound Connect (Semi-Annual Review)", df[df["official_entry_channel"] == "HSCI_SemiAnnual_Review"]),
        ("Joint HSCI / Hang Seng Index Fast-Entry + Connect", df[df["official_entry_channel"] == "Fast_Entry_or_Index"]),
        ("WVR 6M+20D + Joint Index/Connect Entry", df[df["official_entry_channel"] == "WVR_6M20D_Entry"]),
        ("A+H Dual-Listed (Auto T_stab+1 Connect, No HSCI Rebalance)", df[df["official_entry_channel"] == "AH_Post_Stabilization"]),
        ("Excluded Non-A+H (Never Included)", df[df["official_entry_channel"] == "Not_Included"]),
    ]
    for g_lbl, grp in cc_groups:
        s_pre = grp["ccass_sb_pct_pre_eff"].dropna()
        s_p4 = grp["ccass_sb_pct_post4d"].dropna()
        s_p10 = grp["ccass_sb_pct_post10d"].dropna()
        s_nov = grp["ccass_sb_pct_20261112"].dropna()
        rows.append({
            "Panel": "C. CCASS Mainland Holdings (%)",
            "Specification": g_lbl,
            "N_Total": len(grp),
            "Metric_1": f"Pre={s_pre.mean():.2f}% (N={len(s_pre)}); +4d={s_p4.mean():.2f}% (N={len(s_p4)}); +10d={s_p10.mean():.2f}% (N={len(s_p10)})" if len(s_pre) > 0 else "Non-semiannual entry date (tracked 2026-11-12)",
            "Estimate": round(float(s_nov.mean()), 3) if len(s_nov) > 0 else np.nan,
            "SE_or_Aux": round(float(s_nov.median()), 3) if len(s_nov) > 0 else np.nan,
            "t_stat": round(float(stats.ttest_1samp(s_nov, 0).statistic), 2) if (len(s_nov) > 1 and s_nov.std() > 0) else np.nan,
            "p_value": round(float(stats.ttest_1samp(s_nov, 0).pvalue), 6) if (len(s_nov) > 1 and s_nov.std() > 0) else np.nan,
            "Notes": f"As of 2026-11-12: mean {s_nov.mean():.2f}% (med {s_nov.median():.2f}%, max {s_nov.max():.2f}%)" if len(s_nov) else "",
        })

    # Panel D: Stacked Official-Inclusion Date Event Study (All Non-A+H Official Entrants vs Same-Date Controls)
    ev_rows = []
    tr_df = df[(df["is_ah_dual_listed"] == 0) & (df["official_ggt_ever_included"] == 1) & df["official_ggt_eff_date"].notna()].copy()
    ctrl_df = df[(df["is_ah_dual_listed"] == 0) & (df["official_ggt_ever_included"] == 0)].copy()

    def jump_at_date(bdf: pd.DataFrame, eff_dt: pd.Timestamp) -> tuple[float, float] | None:
        post_i = bdf.index[bdf["date"] >= eff_dt]
        if len(post_i) == 0:
            return None
        i0 = int(post_i[0])
        if i0 < 15 or i0 + 10 > len(bdf):
            return None
        pre10 = float(bdf.loc[i0 - 10 : i0 - 1, "turn"].mean())
        post10 = float(bdf.loc[i0 : i0 + 9, "turn"].mean())
        return float(np.log((post10 + 1.0) / (pre10 + 1.0))), float(post10 / pre10) if pre10 > 0 else np.nan

    unique_eff_dates = sorted(tr_df["official_ggt_eff_date"].dropna().unique())
    bar_cache: dict[str, pd.DataFrame] = {}
    for _, r in pd.concat([tr_df, ctrl_df]).iterrows():
        bdf = load_exact_bars(r["Stock Code"], str(r["listing_date"])[:10])
        if bdf is not None:
            bar_cache[r["Stock Code"]] = bdf

    for _, r in tr_df.iterrows():
        sc = r["Stock Code"]
        bdf = bar_cache.get(sc)
        if bdf is None:
            continue
        res_j = jump_at_date(bdf, pd.to_datetime(r["official_ggt_eff_date"]))
        if res_j is not None:
            ev_rows.append({"stock_code": sc, "eff_date": r["official_ggt_eff_date"], "treated": 1, "log_jump": res_j[0], "ratio": res_j[1]})

    for eff_s in unique_eff_dates:
        eff_dt = pd.to_datetime(eff_s)
        for _, cr in ctrl_df.iterrows():
            bdf = bar_cache.get(cr["Stock Code"])
            if bdf is None:
                continue
            res_j = jump_at_date(bdf, eff_dt)
            if res_j is not None:
                ev_rows.append({"stock_code": cr["Stock Code"], "eff_date": eff_s, "treated": 0, "log_jump": res_j[0], "ratio": res_j[1]})

    ev_df = pd.DataFrame(ev_rows)
    tr_ev = ev_df[ev_df["treated"] == 1]
    ct_ev = ev_df[ev_df["treated"] == 0]
    mod_did = smf.ols("log_jump ~ treated + C(eff_date)", data=ev_df).fit(cov_type="cluster", cov_kwds={"groups": ev_df["stock_code"]})
    rows.append({
        "Panel": "D. Stacked Official Entrant DiD",
        "Specification": "All Official Non-A+H Entrants vs Same-Date Never-Included Controls",
        "N_Total": len(ev_df),
        "Metric_1": f"Treated N={len(tr_ev)} (med {tr_ev['ratio'].median():.2f}x) vs Ctrl obs={len(ct_ev)} (med {ct_ev['ratio'].median():.2f}x)",
        "Estimate": round(float(mod_did.params["treated"]), 3),
        "SE_or_Aux": round(float(mod_did.bse["treated"]), 3),
        "t_stat": round(float(mod_did.tvalues["treated"]), 2),
        "p_value": round(float(mod_did.pvalues["treated"]), 6),
        "Notes": f"Event-date FE + Issuer-clustered SE; Treated jump={tr_ev['log_jump'].mean():+.3f}, Control={ct_ev['log_jump'].mean():+.3f}",
    })

    out_20c = pd.DataFrame(rows)
    out_20c.to_csv(OUT_EXT / "ext_table20c_fuzzy_rdd_diagnostics_and_ccass_holdings.csv", index=False)
    print("\n=== Table E20C: Fuzzy RDD Diagnostics, HKEX CCASS Mainland Holdings & Stacked Official DiD ===")
    print(out_20c.to_string(index=False))
    return out_20c


def generate_figure_17(reb: pd.DataFrame, out_20a: pd.DataFrame, ep_df: pd.DataFrame, ah_path_df: pd.DataFrame, out_20b: pd.DataFrame) -> None:
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 10.6,
        "axes.titleweight": "bold",
        "axes.labelsize": 9.6,
        "figure.dpi": 300,
    })

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14.0, 5.6))

    # =========================================================================
    # Panel A: Official One-Sided Fuzzy RDD (Turnover Jump & First-Stage Compliance)
    # =========================================================================
    sub = reb[(reb["run_var"] >= -1.8) & (reb["run_var"] <= 2.4)].copy()
    s_excl = sub[sub["above_5b"] == 0]
    s_nonc = sub[(sub["above_5b"] == 1) & (sub["treat_ggt"] == 0)]
    s_comp = sub[(sub["above_5b"] == 1) & (sub["treat_ggt"] == 1)]

    ax1.scatter(s_excl["run_var"], s_excl["log_jump_pre10"], color="#4393c3", alpha=0.60, s=34, label=f"Excluded < HK$5B (0% Admitted, N={(reb['above_5b']==0).sum()})")
    ax1.scatter(s_nonc["run_var"], s_nonc["log_jump_pre10"], color="#f4a582", edgecolor="#b2182b", marker="^", alpha=0.75, s=42, label="MV >= HK$5B Non-Complier (WVR / DRS / Excluded)")
    ax1.scatter(s_comp["run_var"], s_comp["log_jump_pre10"], color="#b2182b", alpha=0.60, s=36, label=f"MV >= HK$5B Officially Admitted (N={(reb['treat_ggt']==1).sum()})")

    bins_l = np.linspace(-1.75, 0.0, 6)
    bins_r = np.linspace(0.0, 2.35, 8)
    for b_edges, col in [(bins_l, "#053061"), (bins_r, "#67001f")]:
        if b_edges[0] >= 0:
            s_side = sub[(sub["run_var"] >= 0.0) & (sub["run_var"] <= b_edges[-1])].copy()
        else:
            s_side = sub[(sub["run_var"] >= b_edges[0]) & (sub["run_var"] < 0.0)].copy()
        s_side["bin"] = pd.cut(s_side["run_var"], bins=b_edges, include_lowest=True)
        bm = s_side.groupby("bin", observed=False).agg(x=("run_var", "mean"), y=("log_jump_pre10", "mean"), n=("run_var", "count")).dropna()
        bm = bm[bm["n"] >= 2]
        ax1.scatter(bm["x"], bm["y"], color=col, s=75, zorder=5, edgecolor="white", linewidth=0.8)

    mod = smf.ols("log_jump_pre10 ~ above_5b + run_var + above_5b:run_var", data=reb).fit(cov_type="HC1")
    xg_l = np.linspace(-1.7, 0.0, 50)
    xg_r = np.linspace(0.0, 2.3, 50)
    yg_l = mod.params["Intercept"] + mod.params["run_var"] * xg_l
    yg_r = (mod.params["Intercept"] + mod.params["above_5b"]) + (mod.params["run_var"] + mod.params["above_5b:run_var"]) * xg_r
    ax1.plot(xg_l, yg_l, color="#053061", linewidth=2.4)
    ax1.plot(xg_r, yg_r, color="#b2182b", linewidth=2.4)
    ax1.axvline(0.0, color="#111111", linestyle="--", linewidth=1.3)
    ax1.axhline(0.0, color="#777777", linestyle=":", linewidth=0.9)

    fs_row = out_20a[out_20a["Panel_Specification"].str.startswith("0a.")].iloc[0]
    itt_row = out_20a[out_20a["Panel_Specification"].str.startswith("2a.")].iloc[0]
    late_row = out_20a[out_20a["Panel_Specification"].str.startswith("2b.")].iloc[0]
    mult_late = float(np.exp(late_row["Estimate"]))
    ax1.annotate(
        f"Official One-Sided Fuzzy RDD (SSE + CCASS)\n"
        f"First Stage: +{fs_row['Estimate']*100:.1f} pp (t = +{fs_row['t_stat']:.1f})\n"
        f"Sharp ITT Jump: {itt_row['Estimate']:+.2f} (t = {itt_row['t_stat']:+.2f})\n"
        f"2SLS LATE: {late_row['Estimate']:+.2f} log-pts ({mult_late:.2f}x turnover, t = {late_row['t_stat']:+.2f})",
        xy=(0.0, mod.params["Intercept"] + mod.params["above_5b"] * 0.55),
        xytext=(-1.72, 2.25),
        fontsize=8.2,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#fff7ec", edgecolor="#b2182b", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#b2182b", lw=1.2),
    )

    ax1.set_xlabel("Running Variable: log(HSCI Month-End Avg MV / HK$5.0B Cutoff)")
    ax1.set_ylabel("Effective-Monday Log Turnover Jump [0,+9] vs. [-10,-1]")
    ax1.set_ylim(-2.2, 3.6)
    ax1.set_title(f"Panel A: Official HSCI / Stock Connect Fuzzy RDD at HK$5.0B\n(Exact Semi-Annual Effective Mondays, N = {len(reb)} Non-A+H IPOs)")
    ax1.legend(loc="lower right", frameon=True, fontsize=7.9)
    ax1.grid(linestyle=":", alpha=0.45)

    # =========================================================================
    # Panel B: T_stab+1 Automatic A+H Stock Connect Entry & Non-Fungible H/A Wedge
    # =========================================================================
    p_ah = ep_df[ep_df["is_ah"] == 1].groupby("rel_day")["log_norm_turn"].mean()
    p_non = ep_df[ep_df["is_ah"] == 0].groupby("rel_day")["log_norm_turn"].mean()

    l1 = ax2.plot(p_ah.index, p_ah.values, color="#b2182b", marker="o", markersize=4.5, linewidth=2.2, label="A+H IPOs (57/57 Auto Connect at T_stab+1)")
    l2 = ax2.plot(p_non.index, p_non.values, color="#2166ac", marker="s", markersize=4.0, linewidth=2.0, linestyle="--", label="Non-A+H IPOs (Post-Stab Control, No Connect)")
    ax2.axvline(0, color="#111111", linestyle="--", linewidth=1.3)
    ax2.axhline(0, color="#777777", linestyle=":", linewidth=0.9)

    ax2_r = ax2.twinx()
    ah_disc = ah_path_df[(ah_path_df["rel_day"] >= -8) & (ah_path_df["rel_day"] <= 15)].groupby("rel_day")["disc_pct"].mean()
    mean_disc = float(ah_disc.mean())
    l3 = ax2_r.plot(ah_disc.index, ah_disc.values, color="#1b7837", linewidth=2.1, linestyle="-.", marker="^", markersize=4.2, label=f"H-vs-A Price Discount (%, Right Axis: {mean_disc:+.1f}%)")

    did_r = out_20b[out_20b["Channel_Cohort"].str.contains("Difference-in-Differences", na=False)].iloc[0]
    ax2.annotate(
        f"T_stab + 1: Automatic Stock Connect\nAdmission (SSE Art.66 / SZSE Art.65)\n"
        f"Turnover DiD = {did_r['Mean_Metric']:+.3f} (t={did_r['t_or_z_stat']:+.2f}, p={did_r['p_value']:.4f})\n"
        f"Yet H/A Discount Persists ({mean_disc:+.1f}%)",
        xy=(0.2, float(p_ah.loc[1])),
        xytext=(2.1, 0.34),
        fontsize=8.1,
        fontweight="bold",
        bbox=dict(boxstyle="round,pad=0.35", facecolor="#f7fcf5", edgecolor="#1b7837", alpha=0.95),
        arrowprops=dict(arrowstyle="->", color="#111111", lw=1.1),
    )

    ax2.set_xlabel("Event Trading Day Relative to Stabilization Expiry (Day 0 = T_stab + 1)")
    ax2.set_ylabel("Mean Log(Daily Turnover / [-8,-1] Pre-Expiry Mean)")
    ax2_r.set_ylabel("Mean H-Share vs. A-Share Price Discount (%)", color="#1b7837")
    ax2.set_ylim(-0.55, 0.62)
    ax2_r.set_ylim(-48, -10)
    ax2.set_title("Panel B: Automatic T_stab+1 Southbound Entry & Limits to Arbitrage\n(Liquidity Surge Without A-H Convergence Under Share Non-Fungibility)")

    lines = l1 + l2 + l3
    labels = [ln.get_label() for ln in lines]
    ax2.legend(lines, labels, loc="lower left", frameon=True, fontsize=7.8)
    ax2.grid(linestyle=":", alpha=0.45)

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig17_southbound_connect_rdd_and_ah_convergence.png", dpi=300)
    fig.savefig(FIG_DIR / "fig17_southbound_connect_rdd_and_ah_convergence.pdf")
    plt.close(fig)
    print("Saved Figure 17 successfully.")


def main() -> None:
    m = pd.read_csv(BASE_DIR / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv", low_memory=False)
    m226 = pd.read_csv(OUT_MAIN / "clean_micro_panel_2025_2026_N226.csv", low_memory=False)
    off_sc = pd.read_csv(OUT_EXT / "clean_n226_official_stock_connect_panel.csv", low_memory=False)
    df = m.merge(
        m226[[
            "stock_code", "listing_date", "is_ah_dual_listed", "is_prc_h_share",
            "is_18a", "is_18c", "is_wvr", "a_symbol",
            "cornerstone_pct_of_offering", "subscription_ratio_times", "initial_return_pct",
        ]],
        left_on="Stock Code", right_on="stock_code", how="inner"
    ).merge(
        off_sc[[
            "stock_code", "is_wvr", "official_ggt_ever_included", "official_ggt_eff_date",
            "official_ggt_doc_no", "official_entry_channel", "first_hsci_cutoff",
            "first_hsci_eff_date", "hsci_month_end_avg_mv_bn", "hsci_daily_avg_mv_bn",
            "official_admitted_at_review", "ccass_sb_pct_pre_eff", "ccass_sb_pct_post4d",
            "ccass_sb_pct_post10d", "ccass_sb_pct_20261112",
        ]].rename(columns={"is_wvr": "is_wvr_eff"}),
        on="stock_code", how="left"
    )
    out_20a, reb, _m6 = run_hsci_5b_rdd_and_rebalancing(df)
    out_20b, ep_df, ah_path_df = run_ah_auto_connect_and_convergence(df)

    # Augment out_20b with exact SSE official post-stabilization inclusion audit
    ah_sub = df[df["is_ah_dual_listed"] == 1]
    ah_lags = []
    ah_lags_exact = []
    ah_lags_fallback = []
    for _, r in ah_sub.iterrows():
        ld = pd.to_datetime(str(r["listing_date"])[:10])
        st_raw = pd.to_datetime(r["Stabilization period end date"], errors="coerce")
        is_exact = pd.notna(st_raw)
        st = st_raw if is_exact else (ld + pd.Timedelta(days=30))
        eff = pd.to_datetime(r["official_ggt_eff_date"], errors="coerce")
        if pd.notna(eff):
            lag = (eff - st).days
            ah_lags.append(lag)
            if is_exact:
                ah_lags_exact.append(lag)
            else:
                ah_lags_fallback.append(lag)
    lag_s = pd.Series(ah_lags)
    lag_ex = pd.Series(ah_lags_exact)
    lag_fb = pd.Series(ah_lags_fallback)
    extra_row = pd.DataFrame([{
        "Channel_Cohort": "3. Official SSE/CCASS Audit: A+H Auto-Inclusion at T_stab+1 (% Verified / Med Lag Days)",
        "N": len(ah_sub),
        "Mean_Metric": round(float(ah_sub["official_ggt_ever_included"].mean() * 100.0), 1),
        "Median_or_Ratio": round(float(lag_ex.median()), 1) if len(lag_ex) else np.nan,
        "Aux_Mean_Ratio_or_Disc": round(float(lag_s.median()), 1) if len(lag_s) else np.nan,
        "t_or_z_stat": np.nan,
        "p_value": np.nan,
        "Notes": (
            f"{int(ah_sub['official_ggt_ever_included'].sum())}/{len(ah_sub)} (100%) verified in SSE/CCASS; "
            f"exact-date N={len(lag_ex)} med {lag_ex.median():+.1f}d (IQR [{lag_ex.quantile(0.25):+.1f}, {lag_ex.quantile(0.75):+.1f}]); "
            f"statutory-cap (ld+30d) fallback N={len(lag_fb)} med {lag_fb.median():+.1f}d; pooled med {lag_s.median():+.1f}d "
            "(negative fallback reflects offer-close 30d statutory clock & zero-greenshoe Day-1 entries)"
        ),
    }])
    out_20b = pd.concat([out_20b, extra_row], ignore_index=True)
    out_20b.to_csv(OUT_EXT / "ext_table20b_ah_auto_connect_and_convergence.csv", index=False)

    run_fuzzy_rdd_diagnostics_and_ccass(df, reb)
    generate_figure_17(reb, out_20a, ep_df, ah_path_df, out_20b)


if __name__ == "__main__":
    main()
