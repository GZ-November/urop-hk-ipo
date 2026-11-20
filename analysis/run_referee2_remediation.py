#!/usr/bin/env python3
"""
run_referee2_remediation.py
===========================
Empirical remediation suite addressing Referee #2's methodological critiques:
  1. Asset Pricing (Identical 303-month sample 3F vs 4F vs 5F+LIQ, WLS Newey-West HAC,
     exact paired delta-alpha test, forward-cast listing-cap HML sensitivity, LIQ_ZeroRet).
  2. PN18 15x Clawback RD & Mechanism B (balance in |z|<=0.45 headline bandwidth,
     P0 vs P1 decomposition, non-waiver strict-compliance subsample, Mechanism B
     demand-shift / selection / Day-1 share turnover diagnostics).
  3. Lifetime Wealth & US-HK Comparison (equal-horizon 1Y/3Y/5Y cross-era wealth ratios,
     475 no-quote delisted sensitivity bounds, pure Main Board first-time IPO US-HK table).
  4. Event Studies (formal A+H vs non-A+H T_stab+1 panel DiD with issuer FE & clustered SEs;
     lockup Day +180 exposure-scaled CAR & turnover-shock cross-section + Day 240 placebo).
"""
from __future__ import annotations

import bisect
import json
import pathlib
import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
from scipy import stats

warnings.filterwarnings("ignore", category=FutureWarning)

REPO = pathlib.Path(__file__).resolve().parent.parent
OV_DIR = REPO / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO / "analysis" / "out" / "overview_extensions"
SEAS_DIR = OV_DIR / "seasoned_monthly_hfq_cache"
MC_DIR = OV_DIR / "market_cache"
MB_MASTER_CSV = REPO / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv"


def ym_diff(ym1: str, ym2: str) -> int:
    y1, m1 = int(ym1[:4]), int(ym1[5:7])
    y2, m2 = int(ym2[:4]), int(ym2[5:7])
    return (y2 - y1) * 12 + (m2 - m1)


def to_sym(sc: object) -> str | None:
    dig = "".join(ch for ch in str(sc) if ch.isdigit())
    return f"hk{int(dig):05d}" if dig else None


def nw_hac_se(X: np.ndarray, resid: np.ndarray, lags: int = 6) -> np.ndarray:
    """Compute Newey-West HAC covariance for weighted or unweighted least squares (X @ b = y)."""
    n, k = X.shape
    XtX_inv = np.linalg.inv(X.T @ X)
    S = X * resid[:, None]
    G = S.T @ S
    for lag in range(1, min(lags, n - 1) + 1):
        w = 1.0 - lag / (lags + 1.0)
        Gl = S[lag:].T @ S[:-lag]
        G = G + w * (Gl + Gl.T)
    return XtX_inv @ G @ XtX_inv


def paired_delta_alpha_hac(
    y: np.ndarray, X_small: np.ndarray, X_full: np.ndarray, w: np.ndarray, lags: int = 6
) -> tuple[float, float, float, float]:
    """
    Exact paired test of delta_alpha = alpha_full - alpha_small on identical sample y,
    using stacked GMM moment conditions on sqrt(w)-weighted regressions and NW HAC(lags).
    Returns (delta_alpha, se_hac, t_hac, p_hac).
    """
    sw = np.sqrt(w)
    yw = y * sw
    Xs = X_small * sw[:, None]
    Xf = X_full * sw[:, None]

    bs = np.linalg.lstsq(Xs, yw, rcond=None)[0]
    bf = np.linalg.lstsq(Xf, yw, rcond=None)[0]
    us = yw - Xs @ bs
    uf = yw - Xf @ bf

    # Influence scores for intercept (column 0) in each model: (X'X)^-1 x_t u_t
    inv_s = np.linalg.inv(Xs.T @ Xs)
    inv_f = np.linalg.inv(Xf.T @ Xf)
    psi_s = (Xs @ inv_s[0, :]) * us
    psi_f = (Xf @ inv_f[0, :]) * uf
    d_psi = psi_f - psi_s

    n = len(yw)
    var = float(np.sum(d_psi ** 2))
    for lag in range(1, min(lags, n - 1) + 1):
        wt = 1.0 - lag / (lags + 1.0)
        cov_l = float(np.sum(d_psi[lag:] * d_psi[:-lag]))
        var += 2.0 * wt * cov_l
    se = float(np.sqrt(max(var, 1e-18)))
    delta = float(bf[0] - bs[0])
    t_val = delta / se if se > 0 else np.nan
    p_val = float(2.0 * stats.norm.sf(abs(t_val))) if np.isfinite(t_val) else np.nan
    return delta, se, t_val, p_val


# =============================================================================
# MODULE 1: ASSET PRICING (IDENTICAL 303M SAMPLE + LIQ_ZeroRet + CAP SENSITIVITY)
# =============================================================================
def build_fwd_hml_and_liq() -> pd.DataFrame:
    """Build strictly forward-cast listing-cap HML (post-1994 IPOs) & seasoned LIQ_ZeroRet."""
    print("\n--- Module 1A: Building Forward-Cast HML & Seasoned LIQ_ZeroRet ---")
    fin = pd.read_csv(
        EXT_DIR / "hkex_eastmoney_annual_equity_1999_2026.csv",
        dtype={"SECURITY_CODE": str},
        low_memory=False,
    )
    master = pd.read_csv(OV_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
    fin["sym"] = fin["SECURITY_CODE"].apply(to_sym)
    fin["be"] = pd.to_numeric(fin["TOTAL_PARENT_EQUITY"], errors="coerce")
    fin["is_cny"] = pd.to_numeric(fin["IS_CNY_CODE"], errors="coerce").fillna(0)
    fin.loc[fin["is_cny"] == 1, "be"] = fin.loc[fin["is_cny"] == 1, "be"] * 1.08
    fin = fin.dropna(subset=["sym", "be", "report_ym"]).copy()
    fin = fin[fin["be"] > 0].copy()
    fin["rep_dt"] = pd.to_datetime(fin["report_ym"] + "-28", errors="coerce")
    fin = fin.dropna(subset=["rep_dt"])
    fin["avail_ym"] = (fin["rep_dt"] + pd.DateOffset(months=6)).dt.strftime("%Y-%m")
    fin = fin.sort_values(["sym", "avail_ym", "report_ym"]).drop_duplicates(["sym", "avail_ym"], keep="last")

    be_lookup: dict[str, list[tuple[str, float]]] = {}
    for sym, grp in fin.groupby("sym"):
        be_lookup[sym] = list(zip(grp["avail_ym"].tolist(), grp["be"].tolist()))

    ipo_meta: dict[str, tuple[str, float]] = {}
    all_ipo_nums: set[int] = set()
    for _, row in master.sort_values("listing_date").iterrows():
        sym = to_sym(row.get("stock_code"))
        if not sym:
            continue
        dig = int(sym[2:])
        all_ipo_nums.add(dig)
        if sym not in ipo_meta:
            sh = pd.to_numeric(row.get("ext_total_shares_listed"), errors="coerce")
            p0 = pd.to_numeric(row.get("offer_price_hkd"), errors="coerce")
            pr = pd.to_numeric(row.get("funds_raised_total_hkd"), errors="coerce")
            m0 = float(sh * p0) if (pd.notna(sh) and sh > 0 and pd.notna(p0) and p0 > 0) else (float(pr * 4.0) if pd.notna(pr) and pr > 0 else np.nan)
            if pd.notna(m0) and m0 > 0:
                ipo_meta[sym] = (str(row["listing_date"])[:7], m0)

    def _get_lagged_be(sym: str, ym: str) -> float | None:
        pts = be_lookup.get(sym)
        if not pts:
            return None
        idx = bisect.bisect_right([p[0] for p in pts], ym) - 1
        if idx < 0:
            return None
        av_ym, be_val = pts[idx]
        if ym_diff(av_ym, ym) > 24:
            return None
        return be_val

    pre94_syms = [f"hk{k:05d}" for k in range(1, 601) if k not in all_ipo_nums]
    all_targets = [(s, "1990-01", np.nan, True) for s in pre94_syms] + [
        (s, v[0], v[1], False) for s, v in ipo_meta.items()
    ]

    fwd_rows = []
    liq_rows = []
    for sym, anchor_ym, m0, is_pre94 in all_targets:
        sf = SEAS_DIR / f"{sym}.json"
        if not sf.exists():
            continue
        item = json.loads(sf.read_text(encoding="utf-8"))
        bars = item.get("bars", [])
        if len(bars) < 15:
            continue
        m_closes = {str(b[0]): float(b[1]) for b in bars}
        yms = sorted(m_closes.keys())
        first_ym = yms[0]
        if not is_pre94 and ym_diff(anchor_ym, first_ym) < -2:
            continue
        if is_pre94 and first_ym > "1990-12":
            continue
        cur_mcap = item.get("cur_mcap_hkd")
        last_close = m_closes[yms[-1]]
        first_close = m_closes[first_ym]
        eff_list_ym = first_ym if is_pre94 else anchor_ym

        # Precompute monthly returns for trailing 12M zero-return count
        rets_by_idx: list[tuple[str, str, float, float]] = []
        for i in range(len(yms) - 1):
            py, cy = yms[i], yms[i + 1]
            if ym_diff(py, cy) != 1 or m_closes[py] <= 0:
                continue
            r = (m_closes[cy] - m_closes[py]) / m_closes[py]
            rets_by_idx.append((py, cy, r, m_closes[py]))

        for j in range(len(rets_by_idx)):
            py, cy, r, p_prev = rets_by_idx[j]
            if cy < "1994-01" or cy > "2026-09":
                continue
            if ym_diff(eff_list_ym, cy) < 37:
                continue

            # Backcast mcap (only for LIQ size sort when pre94; forward-cast m0 for post94)
            mcap_back = (float(cur_mcap) * (p_prev / last_close)) if (cur_mcap and cur_mcap > 0 and last_close > 0) else np.nan
            mcap_fwd = (float(m0) * (p_prev / first_close)) if (not is_pre94 and pd.notna(m0) and first_close > 0) else np.nan

            # Trailing 12M exact zero-return fraction (t-12 .. t-1, strictly lagged)
            if j >= 12:
                win_r = [rets_by_idx[k][2] for k in range(j - 12, j)]
                z_frac = sum(1 for x in win_r if abs(x) < 1e-6) / 12.0
                liq_mcap = mcap_fwd if pd.notna(mcap_fwd) else mcap_back
                if pd.notna(liq_mcap) and liq_mcap > 0:
                    liq_rows.append({"year_month": cy, "ret": r, "mcap": liq_mcap, "z_frac": z_frac})

            # Strictly forward-cast HML (no cur_mcap at all)
            if cy >= "2000-01" and pd.notna(mcap_fwd) and mcap_fwd > 0:
                be_lag = _get_lagged_be(sym, py)
                if be_lag is not None:
                    bm = be_lag / mcap_fwd
                    if 0.01 <= bm <= 20.0:
                        fwd_rows.append({"year_month": cy, "ret": r, "mcap": mcap_fwd, "bm": bm})

    fdf = pd.DataFrame(fwd_rows)
    q01, q99 = fdf["ret"].quantile([0.01, 0.99])
    fdf["clean_ret"] = fdf["ret"].clip(q01, q99)

    ldf = pd.DataFrame(liq_rows)
    lq01, lq99 = ldf["ret"].quantile([0.01, 0.99])
    ldf["clean_ret"] = ldf["ret"].clip(lq01, lq99)

    out_rows = []
    all_yms = sorted(set(fdf["year_month"]).union(set(ldf["year_month"])))
    for ym in all_yms:
        rec = {"year_month": ym}
        gf = fdf[fdf["year_month"] == ym]
        if len(gf) >= 30:
            med = gf["mcap"].median()
            q30, q70 = gf["bm"].quantile([0.30, 0.70])
            cv, ce = {}, {}
            for sz, smask in [("S", gf["mcap"] <= med), ("B", gf["mcap"] > med)]:
                for bm_l, bmask in [("G", gf["bm"] <= q30), ("V", gf["bm"] >= q70)]:
                    sub = gf[smask & bmask]
                    if len(sub) >= 3:
                        cv[f"{sz}{bm_l}"] = float(np.average(sub["clean_ret"], weights=sub["mcap"]) * 100.0)
                        ce[f"{sz}{bm_l}"] = float(sub["clean_ret"].mean() * 100.0)
            if len(cv) == 4:
                rec["hml_fwd_vw_pct"] = round(0.5 * (cv["SV"] + cv["BV"]) - 0.5 * (cv["SG"] + cv["BG"]), 4)
                rec["hml_fwd_ew_pct"] = round(0.5 * (ce["SV"] + ce["BV"]) - 0.5 * (ce["SG"] + ce["BG"]), 4)
                rec["n_fwd_hml_stocks"] = len(gf)

        gl = ldf[ldf["year_month"] == ym]
        if len(gl) >= 30:
            med_l = gl["mcap"].median()
            # Zero-return illiquidity: Top 30% illiquid vs 0-zero-return liquid
            ill_mask = gl["z_frac"] >= max(gl["z_frac"].quantile(0.70), 1.0 / 12.0)
            liq_mask = gl["z_frac"] <= gl["z_frac"].quantile(0.30)
            cv_l, ce_l = {}, {}
            for sz, smask in [("S", gl["mcap"] <= med_l), ("B", gl["mcap"] > med_l)]:
                for l_l, lmask in [("L", liq_mask), ("I", ill_mask)]:
                    sub = gl[smask & lmask]
                    if len(sub) >= 3:
                        cv_l[f"{sz}{l_l}"] = float(np.average(sub["clean_ret"], weights=sub["mcap"]) * 100.0)
                        ce_l[f"{sz}{l_l}"] = float(sub["clean_ret"].mean() * 100.0)
            if len(cv_l) == 4:
                rec["liq_zeroret_vw_pct"] = round(0.5 * (cv_l["SI"] + cv_l["BI"]) - 0.5 * (cv_l["SL"] + cv_l["BL"]), 4)
                rec["liq_zeroret_ew_pct"] = round(0.5 * (ce_l["SI"] + ce_l["BI"]) - 0.5 * (ce_l["SL"] + ce_l["BL"]), 4)
                rec["n_liq_stocks"] = len(gl)
        out_rows.append(rec)

    res = pd.DataFrame(out_rows).sort_values("year_month")
    print(f"    Built fwd-cap HML ({res['hml_fwd_vw_pct'].notna().sum()} mos) & LIQ_ZeroRet ({res['liq_zeroret_vw_pct'].notna().sum()} mos)")
    return res


def run_module1_asset_pricing() -> None:
    fac = pd.read_csv(EXT_DIR / "clean_monthly_ctp_seasoned_4factors_1994_2026.csv")
    extra = build_fwd_hml_and_liq()
    df = fac.merge(extra, on="year_month", how="left")
    df.to_csv(EXT_DIR / "remed_monthly_ctp_5factors_1994_2026.csv", index=False)

    portfolios = [
        ("ctp_12m_mb_ew_ret", "n_ctp_12m_mb", "Main Board 12M Equal-Weighted"),
        ("ctp_12m_mb_vw_ret", "n_ctp_12m_mb", "Main Board 12M Value-Weighted"),
        ("ctp_36m_mb_ew_ret", "n_ctp_36m_mb", "Main Board 36M Equal-Weighted"),
        ("ctp_36m_mb_vw_ret", "n_ctp_36m_mb", "Main Board 36M Value-Weighted"),
        ("ctp_12m_gem_ew_ret", "n_ctp_12m_gem", "GEM 12M Equal-Weighted"),
        ("ctp_12m_gem_vw_ret", "n_ctp_12m_gem", "GEM 12M Value-Weighted"),
        ("ctp_36m_gem_ew_ret", "n_ctp_36m_gem", "GEM 36M Equal-Weighted"),
        ("ctp_36m_gem_vw_ret", "n_ctp_36m_gem", "GEM 36M Value-Weighted"),
    ]

    rows = []
    for win_lbl, ym_lo in [("Identical_2001_2026Q3_303m", "2001-07"), ("Identical_2008_2026Q3_225m", "2008-01")]:
        w_df = df[(df["year_month"] >= ym_lo) & (df["year_month"] <= "2026-09")].copy()
        for r_col, n_col, p_lbl in portfolios:
            # Restrict to IDENTICAL months where ALL 5 factors & portfolio return are valid
            req = [r_col, n_col, "rf_monthly_pct", "mkt_tr_excess_pct", "smb_seasoned_pct", "mom_seasoned_pct", "hml_hkex_vw_pct", "liq_zeroret_vw_pct"]
            sub = w_df.dropna(subset=req).copy()
            sub = sub[sub[n_col] > 0].reset_index(drop=True)
            if len(sub) < 36:
                continue
            y = (sub[r_col] - sub["rf_monthly_pct"]).values
            w = np.sqrt(sub[n_col].values.astype(float))
            sw = np.sqrt(w)
            X3 = np.column_stack([np.ones(len(sub)), sub["mkt_tr_excess_pct"].values, sub["smb_seasoned_pct"].values, sub["mom_seasoned_pct"].values])
            X4 = np.column_stack([X3, sub["hml_hkex_vw_pct"].values])
            X5 = np.column_stack([X4, sub["liq_zeroret_vw_pct"].values])

            models = [("1_HKEX_3F", X3), ("2_HKEX_4F_HML", X4), ("3_HKEX_5F_HML_LIQ", X5)]
            for m_lbl, X in models:
                ols_fit = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
                yw = y * sw
                Xw = X * sw[:, None]
                wls_hc3 = sm.OLS(yw, Xw).fit(cov_type="HC3")
                wls_hac_cov = nw_hac_se(Xw, wls_hc3.resid, lags=6)
                wls_a = float(wls_hc3.params[0])
                wls_t_hac = wls_a / float(np.sqrt(wls_hac_cov[0, 0]))
                wls_p_hac = float(2.0 * stats.norm.sf(abs(wls_t_hac)))

                d_4_3, se_4_3, t_4_3, p_4_3 = paired_delta_alpha_hac(y, X3, X4, w, lags=6)
                d_5_4, se_5_4, t_5_4, p_5_4 = paired_delta_alpha_hac(y, X4, X5, w, lags=6)

                b_hml = float(wls_hc3.params[4]) if X.shape[1] >= 5 else np.nan
                t_hml_hac = (b_hml / float(np.sqrt(wls_hac_cov[4, 4]))) if X.shape[1] >= 5 else np.nan
                b_liq = float(wls_hc3.params[5]) if X.shape[1] >= 6 else np.nan
                t_liq_hac = (b_liq / float(np.sqrt(wls_hac_cov[5, 5]))) if X.shape[1] >= 6 else np.nan

                rows.append({
                    "Window": win_lbl,
                    "Model": m_lbl,
                    "Portfolio": p_lbl,
                    "Months_T": len(sub),
                    "OLS_Alpha_Mo": round(float(ols_fit.params[0]), 3),
                    "OLS_t_HAC6": round(float(ols_fit.tvalues[0]), 2),
                    "OLS_p_HAC6": round(float(ols_fit.pvalues[0]), 4),
                    "WLS_Alpha_Mo": round(wls_a, 3),
                    "WLS_t_HC3": round(float(wls_hc3.tvalues[0]), 2),
                    "WLS_t_HAC6": round(wls_t_hac, 2),
                    "WLS_p_HAC6": round(wls_p_hac, 4),
                    "Delta_Alpha_4F_minus_3F": round(d_4_3, 3) if m_lbl == "2_HKEX_4F_HML" else np.nan,
                    "Delta_Alpha_4F_t_HAC6": round(t_4_3, 2) if m_lbl == "2_HKEX_4F_HML" else np.nan,
                    "Delta_Alpha_4F_p_HAC6": round(p_4_3, 4) if m_lbl == "2_HKEX_4F_HML" else np.nan,
                    "Delta_Alpha_5F_minus_4F": round(d_5_4, 3) if m_lbl == "3_HKEX_5F_HML_LIQ" else np.nan,
                    "Delta_Alpha_5F_t_HAC6": round(t_5_4, 2) if m_lbl == "3_HKEX_5F_HML_LIQ" else np.nan,
                    "Delta_Alpha_5F_p_HAC6": round(p_5_4, 4) if m_lbl == "3_HKEX_5F_HML_LIQ" else np.nan,
                    "Beta_HML": round(b_hml, 3) if pd.notna(b_hml) else np.nan,
                    "t_HML_HAC6": round(t_hml_hac, 2) if pd.notna(t_hml_hac) else np.nan,
                    "Beta_LIQ": round(b_liq, 3) if pd.notna(b_liq) else np.nan,
                    "t_LIQ_HAC6": round(t_liq_hac, 2) if pd.notna(t_liq_hac) else np.nan,
                    "R2_WLS": round(float(wls_hc3.rsquared), 3),
                })

    t1 = pd.DataFrame(rows)
    t1.to_csv(EXT_DIR / "remed_table1_asset_pricing_identical_sample.csv", index=False)

    # Sensitivity check across HML definitions on identical overlapping sample
    sens_rows = []
    req_all = [
        "rf_monthly_pct", "mkt_tr_excess_pct", "smb_seasoned_pct", "mom_seasoned_pct",
        "hml_hkex_vw_pct", "hml_hkex_ew_pct", "hml_fwd_vw_pct", "kf_hml", "liq_zeroret_vw_pct",
    ]
    w_ov = df[(df["year_month"] >= "2001-07") & (df["year_month"] <= "2026-09")].dropna(subset=req_all).copy()
    for r_col, n_col, p_lbl in portfolios[:6]:
        sub = w_ov.dropna(subset=[r_col, n_col]).copy()
        sub = sub[sub[n_col] > 0].reset_index(drop=True)
        if len(sub) < 36:
            continue
        y = (sub[r_col] - sub["rf_monthly_pct"]).values
        w_s = np.sqrt(sub[n_col].values.astype(float))
        sw = np.sqrt(w_s)
        X3 = np.column_stack([np.ones(len(sub)), sub["mkt_tr_excess_pct"].values, sub["smb_seasoned_pct"].values, sub["mom_seasoned_pct"].values])
        for h_col, h_lbl in [
            ("hml_hkex_vw_pct", "1_Backcast_VW_HML"),
            ("hml_hkex_ew_pct", "2_Backcast_EW_HML"),
            ("hml_fwd_vw_pct", "3_ForwardCast_ListingCap_VW_HML"),
            ("kf_hml", "4_KenFrench_APxJP_HML"),
        ]:
            X4 = np.column_stack([X3, sub[h_col].values])
            yw = y * sw
            Xw = X4 * sw[:, None]
            fit = sm.OLS(yw, Xw).fit()
            cov = nw_hac_se(Xw, fit.resid, lags=6)
            a = float(fit.params[0])
            t_hac = a / float(np.sqrt(cov[0, 0]))
            bh = float(fit.params[4])
            th = bh / float(np.sqrt(cov[4, 4]))
            da, _, td, pd_v = paired_delta_alpha_hac(y, X3, X4, w_s, lags=6)
            sens_rows.append({
                "Portfolio": p_lbl,
                "HML_Variant": h_lbl,
                "Months_T": len(sub),
                "WLS_Alpha_Mo": round(a, 3),
                "WLS_t_HAC6": round(t_hac, 2),
                "WLS_p_HAC6": round(float(2.0 * stats.norm.sf(abs(t_hac))), 4),
                "Delta_Alpha_vs_3F": round(da, 3),
                "Delta_Alpha_t_HAC6": round(td, 2),
                "Beta_HML": round(bh, 3),
                "t_HML_HAC6": round(th, 2),
            })
    t1b = pd.DataFrame(sens_rows)
    t1b.to_csv(EXT_DIR / "remed_table1b_hml_and_liq_sensitivity.csv", index=False)
    print("Saved remed_table1 & remed_table1b.")


# =============================================================================
# MODULE 2: PN18 15x RD BALANCE / P0-vs-P1 / NON-WAIVER + MECHANISM B TURNOVER
# =============================================================================
def _rd_row(df: pd.DataFrame, dep: str, bw: float, panel: str, spec_lbl: str, controls: list[str] | None = None) -> dict:
    cols = [dep, "z", "above"] + (controls or [])
    sub = df[np.abs(df["z"]) <= bw].dropna(subset=cols).copy()
    rhs = "above * z" + ((" + " + " + ".join(controls)) if controls else "")
    fit = smf.ols(f"{dep} ~ {rhs}", data=sub).fit(cov_type="HC3")
    return {
        "Panel": panel,
        "Specification": spec_lbl,
        "Bandwidth": f"|z|<={bw:.2f}",
        "Outcome_or_Var": dep,
        "N": int(fit.nobs),
        "N_Below": int((sub["above"] == 0).sum()),
        "N_Above": int((sub["above"] == 1).sum()),
        "Estimate": round(float(fit.params["above"]), 4),
        "SE_HC3": round(float(fit.bse["above"]), 4),
        "t_HC3": round(float(fit.tvalues["above"]), 2),
        "p_val": round(float(fit.pvalues["above"]), 4),
    }


def run_module2_pn18_and_mechb() -> None:
    print("\n--- Module 2: PN18 15x RD Diagnostics & Mechanism B Turnover ---")
    d33 = pd.read_csv(EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv", low_memory=False)
    d33["listing_dt"] = pd.to_datetime(d33["listing_date"])
    # The August 2025 allocation rules apply by listing-document publication date, not listing date.
    # Use the prospectus date where it is recorded and fall back to the listing date otherwise.
    d33["regime_dt"] = pd.to_datetime(d33["prospectus_date"], errors="coerce").fillna(d33["listing_dt"])
    pn18 = d33[
        (d33["board"] == "Main Board")
        & (d33["listing_dt"] >= "1998-06-22")
        & (d33["regime_dt"] < "2025-08-04")
        & (d33["retail_sub_ratio_clean"].notna())
        & (d33["pn18_allocation_sample"] == 1)
    ].copy()

    col_s = pd.to_numeric(pn18["col_S"], errors="coerce")
    col_ct = pd.to_numeric(pn18["col_CT"], errors="coerce")
    col_m = pd.to_numeric(pn18["col_M"], errors="coerce")
    pn18["init_pub_pct"] = np.clip(col_s / col_m * 100.0, 0.0, 100.0)
    pn18["final_pub_pct"] = np.clip(col_ct / col_m * 100.0, 0.0, 100.0)
    pn18["log_ir"] = np.log1p(np.maximum(pd.to_numeric(pn18["ir_close_pct"], errors="coerce") / 100.0, -0.99))
    pn18["offer_p0"] = pd.to_numeric(pn18["offer_price_hkd"], errors="coerce")
    pn18["debut_p1"] = pn18["offer_p0"] * (1.0 + pd.to_numeric(pn18["ir_close_pct"], errors="coerce") / 100.0)
    pn18["log_p0"] = np.where(pn18["offer_p0"] > 0, np.log(pn18["offer_p0"]), np.nan)
    pn18["log_p1"] = np.where(pn18["debut_p1"] > 0, np.log(pn18["debut_p1"]), np.nan)
    pn18["range_pos"] = pd.to_numeric(pn18["ext_range_pos"], errors="coerce")
    pn18["log_proceeds"] = np.log(np.maximum(pd.to_numeric(pn18["funds_raised_total_hkd"], errors="coerce") / 1e6, 1e-3))
    pn18["has_cornerstone"] = pd.to_numeric(pn18["ext_has_cornerstone"], errors="coerce").fillna(0.0)
    pn18["hsi_ret_pre30td_pct"] = pd.to_numeric(pn18["hsi_ret_pre30td_pct"], errors="coerce")
    pn18["z"] = np.log(np.maximum(pn18["retail_sub_ratio_clean"], 0.01)) - np.log(15.0)
    pn18["above"] = (pn18["retail_sub_ratio_clean"] >= 15.0).astype(int)

    # Identify waiver / discretionary reallocation vs strict PN18 statutory compliance
    sub_r = pn18["retail_sub_ratio_clean"]
    fp = pn18["final_pub_pct"]
    ip = pn18["init_pub_pct"]
    strict_mask = (
        ((sub_r < 15.0) & (np.abs(fp - ip) <= 2.5))
        | ((sub_r >= 15.0) & (sub_r < 50.0) & (fp >= 27.5) & (fp <= 32.5))
        | ((sub_r >= 50.0) & (sub_r < 100.0) & (fp >= 37.5) & (fp <= 42.5))
        | ((sub_r >= 100.0) & (fp >= 47.5) & (fp <= 52.5))
    )
    pn18["strict_pn18"] = strict_mask.astype(int)
    pn18_strict = pn18[pn18["strict_pn18"] == 1].copy()

    rows = []
    # Panel A: Balance across headline bandwidth |z|<=0.45 and |z|<=0.65
    for bw in [0.45, 0.65]:
        for cov in ["log_proceeds", "has_cornerstone", "is_prc_joint_stock", "init_pub_pct", "hsi_ret_pre30td_pct"]:
            rows.append(_rd_row(pn18, cov, bw, "A_Covariate_Balance_Full", "Full PN18"))
            rows.append(_rd_row(pn18_strict, cov, bw, "A2_Covariate_Balance_StrictNoWaiver", "Strict Non-Waiver PN18"))

    # Panel B: P0 vs P1 Decomposition (Raw & Covariate-Adjusted)
    ctrls = ["log_proceeds", "is_prc_joint_stock", "has_cornerstone", "init_pub_pct"]
    for bw in [0.45, 0.65]:
        for dep in ["final_pub_pct", "log_ir", "log_p0", "log_p1", "range_pos"]:
            rows.append(_rd_row(pn18, dep, bw, "B_Price_Decomp_Full_Raw", "Local Linear (No Controls)"))
            rows.append(_rd_row(pn18, dep, bw, "B_Price_Decomp_Full_Adj", "Local Linear (+Controls)", controls=ctrls))
            rows.append(_rd_row(pn18_strict, dep, bw, "C_Strict_NonWaiver_Raw", "Strict Non-Waiver (No Controls)"))
            rows.append(_rd_row(pn18_strict, dep, bw, "C_Strict_NonWaiver_Adj", "Strict Non-Waiver (+Controls)", controls=ctrls))

    # Panel D: Mechanism B Demand Shift & Endogenous Conditioning (N=226)
    n226 = pd.read_csv(OV_DIR / "clean_micro_panel_2025_2026_N226.csv")
    mb_raw = pd.read_csv(MB_MASTER_CSV, low_memory=False)
    mb_raw["stock_code"] = mb_raw["Stock Code"].astype(str).str.strip()
    n226 = n226.merge(
        mb_raw[["stock_code", "First-day flipping ratio (%)", "Industry classification code"]],
        on="stock_code",
        how="left",
    )
    n226["day1_turnover_pct"] = pd.to_numeric(n226["First-day flipping ratio (%)"], errors="coerce") * 100.0
    n226["sub_x"] = pd.to_numeric(n226["subscription_ratio_times"], errors="coerce").clip(lower=0.0)
    n226["log1p_sub"] = np.log1p(n226["sub_x"])
    n226["is_ge100x"] = (n226["sub_x"] >= 100.0).astype(int)
    n226["log_proc"] = np.log(pd.to_numeric(n226["gross_proceeds_hkd_m"], errors="coerce"))
    n226["log_ir"] = np.log1p(pd.to_numeric(n226["initial_return_pct"], errors="coerce") / 100.0)
    n226["is_mech_b"] = (n226["offer_mechanism"] == "Mechanism B").astype(int)
    n226["post_reg"] = n226["post_aug2025_prospectus"].astype(int)
    n226["non_ah"] = 1 - n226["is_ah_dual_listed"].astype(int)
    n226["small_deal"] = (n226["gross_proceeds_hkd_m"] < n226["gross_proceeds_hkd_m"].median()).astype(int)
    n226["hsics"] = n226["Industry classification code"].fillna("UNK")
    n226["list_ym"] = pd.to_datetime(n226["listing_date"]).dt.strftime("%Y-%m")

    for grp_lbl, mask in [
        ("Pre_Aug2025_All", n226["post_aug2025_prospectus"] == 0),
        ("Post_Aug2025_All", n226["post_aug2025_prospectus"] == 1),
        # Keep Chapter 18C (Rule 18C.09 schedule) apart from statutory Mechanism A / bespoke waivers.
        ("Post_Aug2025_MechA_or_Bespoke", (n226["post_aug2025_prospectus"] == 1) & (n226["is_mech_b"] == 0) & (n226["alloc_regime_actual"] != "Ch18C_Special")),
        ("Post_Aug2025_Ch18C", (n226["post_aug2025_prospectus"] == 1) & (n226["alloc_regime_actual"] == "Ch18C_Special")),
        ("Post_Aug2025_MechB", (n226["post_aug2025_prospectus"] == 1) & (n226["is_mech_b"] == 1)),
    ]:
        g = n226[mask]
        for col_m, lbl_m in [
            ("is_ge100x", "Share_Sub_GE_100x"),
            ("log1p_sub", "Mean_Log1p_Sub"),
            ("public_offer_fraction_pct", "Mean_Final_Retail_Pct"),
            ("day1_turnover_pct", "Mean_Day1_Share_Turnover_Pct"),
            ("log_ir", "Mean_Log1p_IR"),
            ("log_proc", "Mean_Log_Proceeds"),
            ("cornerstone_pct_of_offering", "Mean_Cornerstone_Pct"),
            ("is_ah_dual_listed", "Share_AH_Dual_Listed"),
        ]:
            s = pd.to_numeric(g[col_m], errors="coerce").dropna()
            rows.append({
                "Panel": "D_MechB_Selection_And_Conditioning",
                "Specification": grp_lbl,
                "Bandwidth": "N=226",
                "Outcome_or_Var": lbl_m,
                "N": int(len(s)),
                "N_Below": np.nan,
                "N_Above": np.nan,
                "Estimate": round(float(s.mean()), 4),
                "SE_HC3": round(float(s.sem()), 4) if len(s) > 1 else np.nan,
                "t_HC3": np.nan,
                "p_val": np.nan,
            })

    # Panel E: Unconditional & predetermined-characteristic ITT Mechanism B regressions (+HSICS FE, Month cluster)
    for dep in ["public_offer_fraction_pct", "day1_turnover_pct", "log_ir"]:
        sub_m = n226.dropna(subset=[dep, "log_proc"]).copy()
        specs_e = [
            ("Uncond_PostAug2025", f"{dep} ~ post_reg + log_proc + cornerstone_pct_of_offering + is_ah_dual_listed + C(hsics)", "post_reg"),
            ("Predet_Post_x_NonAH", f"{dep} ~ post_reg * non_ah + log_proc + cornerstone_pct_of_offering + C(hsics)", "post_reg:non_ah"),
            ("Predet_Post_x_SmallDeal", f"{dep} ~ post_reg * small_deal + log_proc + cornerstone_pct_of_offering + is_ah_dual_listed + C(hsics)", "post_reg:small_deal"),
        ]
        for s_lbl, fml, key_var in specs_e:
            fit_e = smf.ols(fml, data=sub_m).fit(cov_type="cluster", cov_kwds={"groups": sub_m["list_ym"]})
            rows.append({
                "Panel": "E_MechB_ExAnte_ITT_Regressions",
                "Specification": s_lbl,
                "Bandwidth": f"MonthCluster(G={sub_m['list_ym'].nunique()})",
                "Outcome_or_Var": dep,
                "N": int(fit_e.nobs),
                "N_Below": np.nan,
                "N_Above": np.nan,
                "Estimate": round(float(fit_e.params[key_var]), 4),
                "SE_HC3": round(float(fit_e.bse[key_var]), 4),
                "t_HC3": round(float(fit_e.tvalues[key_var]), 2),
                "p_val": round(float(fit_e.pvalues[key_var]), 4),
            })

    t2 = pd.DataFrame(rows)
    t2.to_csv(EXT_DIR / "remed_table2_pn18_rd_and_mechb.csv", index=False)
    print(f"Saved remed_table2_pn18_rd_and_mechb.csv ({len(t2)} rows; strict PN18 N={len(pn18_strict)}/{len(pn18)}).")


# =============================================================================
# MODULE 3: EQUAL-HORIZON WEALTH RATIOS, DELISTING BOUNDS, & PURE MB US-HK
# =============================================================================
def _load_hsi_monthly() -> pd.DataFrame:
    fac = pd.read_csv(EXT_DIR / "clean_monthly_ctp_seasoned_factors_1994_2026.csv")
    hsi_px_raw = json.loads((OV_DIR / "market_cache" / "hkHSI_1994_2026.json").read_text())
    px_s = pd.Series({pd.Timestamp(k): float(v) for k, v in hsi_px_raw.items()}).sort_index()
    px_m = px_s.resample("ME").last()
    px_m.index = px_m.index.strftime("%Y-%m")
    div = fac.set_index("year_month")["hsi_div_monthly_pct"].astype(float) / 100.0
    months = pd.period_range("1994-01", "2026-11", freq="M").strftime("%Y-%m")
    div = div.reindex(months).fillna(0.0)
    div_idx = (1.0 + div).cumprod()
    px_m = px_m.reindex(months).ffill()
    tr_idx = px_m * div_idx
    return pd.DataFrame({"px": px_m, "tr": tr_idx})


def run_module3_wealth_and_ushk() -> None:
    print("\n--- Module 3: Equal-Horizon Wealth Ratios, Delisting Bounds & Pure MB US-HK ---")
    d33 = pd.read_csv(EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv", low_memory=False)
    hsi_m = _load_hsi_monthly()

    d33["sym"] = d33["stock_code"].apply(to_sym)
    d33["list_ym"] = pd.to_datetime(d33["listing_date"], format="mixed").dt.strftime("%Y-%m")
    d33["list_year"] = pd.to_datetime(d33["listing_date"], format="mixed").dt.year
    d33["proceeds_bn"] = pd.to_numeric(d33["funds_raised_total_hkd"], errors="coerce") / 1e9

    def era_of(yr: int) -> str:
        if yr <= 1999:
            return "Era I (1994-1999)"
        if yr <= 2007:
            return "Era II (2000-2007)"
        if yr <= 2017:
            return "Era III (2008-2017)"
        if yr <= 2022:
            return "Era IV (2018-2022)"
        return "Era V (2023-2026Q3)"

    d33["era"] = d33["list_year"].apply(era_of)

    # Panel A: Equal-horizon (12M, 36M, 60M) proceeds-weighted wealth ratios from offer/first-month
    # Using after_bhr_1y_pct (verified 1Y from listing/first-close) & SEAS_DIR monthly hfq series
    seas_cache: dict[str, dict[str, float]] = {}
    for sym in d33["sym"].dropna().unique():
        sf = SEAS_DIR / f"{sym}.json"
        if sf.exists():
            bars = json.loads(sf.read_text(encoding="utf-8")).get("bars", [])
            seas_cache[sym] = {str(b[0]): float(b[1]) for b in bars}

    eq_rows = []
    for h_mos, h_lbl in [(12, "1Y (12M)"), (36, "3Y (36M)"), (60, "5Y (60M)")]:
        rec_list = []
        for _, r in d33.iterrows():
            P = r["proceeds_bn"]
            sym = r["sym"]
            ym0 = r["list_ym"]
            if pd.isna(P) or P <= 0 or not sym or ym0 not in hsi_m.index:
                continue
            ym_h = (pd.to_datetime(ym0 + "-01") + pd.DateOffset(months=h_mos)).strftime("%Y-%m")
            if ym_h not in hsi_m.index:
                continue
            mc = seas_cache.get(sym, {})
            # Use listing month or +1 month anchor if listing happened at month end
            ym_start = ym0 if ym0 in mc else (pd.to_datetime(ym0 + "-01") + pd.DateOffset(months=1)).strftime("%Y-%m")
            if ym_start not in mc or ym_h not in mc or mc[ym_start] <= 0:
                continue
            ipo_r = mc[ym_h] / mc[ym_start] - 1.0
            hsi_px_r = hsi_m.loc[ym_h, "px"] / hsi_m.loc[ym0, "px"] - 1.0
            hsi_tr_r = hsi_m.loc[ym_h, "tr"] / hsi_m.loc[ym0, "tr"] - 1.0
            if not (np.isfinite(ipo_r) and np.isfinite(hsi_px_r) and np.isfinite(hsi_tr_r)):
                continue
            rec_list.append({
                "era": r["era"], "board": r["board"], "name": str(r["company_name"]),
                "P": P, "ipo_r": ipo_r, "hsi_px_r": hsi_px_r, "hsi_tr_r": hsi_tr_r
            })
        hdf = pd.DataFrame(rec_list)
        for grp_lbl, mask in [
            ("All Matched", pd.Series(True, index=hdf.index)),
            ("All excl. Tencent", ~hdf["name"].str.contains("Tencent", na=False)),
            ("Era I (1994-1999)", hdf["era"] == "Era I (1994-1999)"),
            ("Era II (2000-2007)", hdf["era"] == "Era II (2000-2007)"),
            ("Era II excl. Tencent", (hdf["era"] == "Era II (2000-2007)") & (~hdf["name"].str.contains("Tencent", na=False))),
            ("Era III (2008-2017)", hdf["era"] == "Era III (2008-2017)"),
            ("Era IV (2018-2022)", hdf["era"] == "Era IV (2018-2022)"),
            ("Era V (2023-2026Q3)", hdf["era"] == "Era V (2023-2026Q3)"),
        ]:
            sub = hdf[mask]
            if len(sub) == 0:
                continue
            p_sum = sub["P"].sum()
            wr_px = (sub["P"] * (1.0 + sub["ipo_r"])).sum() / (sub["P"] * (1.0 + sub["hsi_px_r"])).sum()
            wr_tr = (sub["P"] * (1.0 + sub["ipo_r"])).sum() / (sub["P"] * (1.0 + sub["hsi_tr_r"])).sum()
            eq_rows.append({
                "Panel": "A_Equal_Horizon_Wealth_Ratios",
                "Horizon_or_Scenario": h_lbl,
                "Group": grp_lbl,
                "N": len(sub),
                "Proceeds_HKD_Bn": round(float(p_sum), 2),
                "IPO_Gain_HKD_Bn": round(float((sub["P"] * sub["ipo_r"]).sum()), 2),
                "HSI_Px_Gain_HKD_Bn": round(float((sub["P"] * sub["hsi_px_r"]).sum()), 2),
                "HSI_TR_Gain_HKD_Bn": round(float((sub["P"] * sub["hsi_tr_r"]).sum()), 2),
                "WR_vs_HSI_Price": round(float(wr_px), 3),
                "WR_vs_HSI_TR": round(float(wr_tr), 3),
                "EW_Mean_Excess_vs_HSI_TR_Pct": round(float((sub["ipo_r"] - sub["hsi_tr_r"]).mean() * 100.0), 2),
            })

    # Panel B: Aggregate Terminal Bounds including 475 No-Quote Delisted IPOs (0%, 50%, 100% recovery)
    hsi_px_raw = json.loads((OV_DIR / "market_cache" / "hkHSI_1994_2026.json").read_text())
    px_d = pd.Series({pd.Timestamp(k): float(v) for k, v in hsi_px_raw.items()}).sort_index()
    px_d = px_d[px_d.index <= pd.Timestamp("2026-11-12")]
    fac = pd.read_csv(EXT_DIR / "clean_monthly_ctp_seasoned_factors_1994_2026.csv")
    div_m = fac.set_index("year_month")["hsi_div_monthly_pct"].astype(float) / 100.0
    months = pd.period_range("1994-01", "2026-11", freq="M").strftime("%Y-%m")
    div_idx = (1.0 + div_m.reindex(months).ffill()).cumprod()

    recycled = d33["flag_recycled_or_transferred_ticker"].fillna(0) != 0
    rev = ~recycled & d33["flag_reverse_split_distortion"].fillna(False).astype(bool)
    unv = ~recycled & ~rev & d33["flag_lifetime_split_unverified"].fillna(False).astype(bool)
    ret_lt = pd.to_numeric(d33["lifetime_offer_to_date_pct"], errors="coerce") / 100.0
    ok = ~recycled & ~rev & ~unv & ret_lt.notna()
    noq = ~recycled & ~rev & ~unv & ret_lt.isna()

    d33["ld_dt"] = pd.to_datetime(d33["listing_date"], format="mixed")
    start_px = px_d.reindex(d33["ld_dt"], method="ffill").to_numpy()
    b_px = px_d.iloc[-1] / start_px - 1.0
    ym_s = d33["ld_dt"].dt.strftime("%Y-%m")
    b_tr = (1.0 + b_px) * (div_idx.iloc[-1] / ym_s.map(div_idx)) - 1.0
    d33["b_px"] = b_px
    d33["b_tr"] = b_tr

    base_g = d33[ok & d33["proceeds_bn"].notna()].copy()
    del_g = d33[noq & d33["proceeds_bn"].notna()].copy()

    for scen_lbl, recov_rate in [("Verified_Only_N2116", None), ("Incl_475_NoQuote_0pct_Recovery", 0.0), ("Incl_475_NoQuote_50pct_Recovery", 0.5), ("Incl_475_NoQuote_100pct_Par", 1.0)]:
        for ex_lbl, ex_mask_fn in [
            ("All", lambda df_: pd.Series(True, index=df_.index)),
            ("Excl_Tencent", lambda df_: ~df_["company_name"].str.contains("Tencent", na=False)),
            ("Excl_Tencent_and_AIA", lambda df_: ~df_["company_name"].str.contains("Tencent|AIA Group", na=False)),
        ]:
            bg = base_g[ex_mask_fn(base_g)]
            p_tot = bg["proceeds_bn"].sum()
            g_ipo = (bg["proceeds_bn"] * ret_lt.loc[bg.index]).sum()
            g_hpx = (bg["proceeds_bn"] * bg["b_px"]).sum()
            g_htr = (bg["proceeds_bn"] * bg["b_tr"]).sum()
            n_tot = len(bg)
            if recov_rate is not None:
                dg = del_g[ex_mask_fn(del_g)]
                n_tot += len(dg)
                p_tot += dg["proceeds_bn"].sum()
                g_ipo += (dg["proceeds_bn"] * (recov_rate - 1.0)).sum()
                g_hpx += (dg["proceeds_bn"] * dg["b_px"]).sum()
                g_htr += (dg["proceeds_bn"] * dg["b_tr"]).sum()
            wr_px = (p_tot + g_ipo) / (p_tot + g_hpx)
            wr_tr = (p_tot + g_ipo) / (p_tot + g_htr)
            eq_rows.append({
                "Panel": "B_Aggregate_Terminal_Bounds",
                "Horizon_or_Scenario": scen_lbl,
                "Group": ex_lbl,
                "N": n_tot,
                "Proceeds_HKD_Bn": round(float(p_tot), 2),
                "IPO_Gain_HKD_Bn": round(float(g_ipo), 2),
                "HSI_Px_Gain_HKD_Bn": round(float(g_hpx), 2),
                "HSI_TR_Gain_HKD_Bn": round(float(g_htr), 2),
                "WR_vs_HSI_Price": round(float(wr_px), 3),
                "WR_vs_HSI_TR": round(float(wr_tr), 3),
                "EW_Mean_Excess_vs_HSI_TR_Pct": np.nan,
            })

    # Panel C: Like-for-like dividend-reinvested IPO Total Return (via chained gtimg hfq) vs HSI-TR
    # plus observed pre-delisting hfq recovery for 363/475 unquoted issuers and 0-100% bounds on residual 112
    def _chain_hfq_tr(row: pd.Series) -> float:
        sym = row["sym"]
        smap = seas_cache.get(sym)
        if not smap:
            return np.nan
        ld = str(row["listing_date"])[:10]
        ir = pd.to_numeric(row.get("ir_close_pct"), errors="coerce")
        if pd.isna(ir):
            return np.nan
        bdf = _load_exact_bars(row["stock_code"], ld)
        if bdf is None or len(bdf) == 0:
            return np.nan
        bdf_pos = bdf[pd.to_numeric(bdf["close"], errors="coerce") > 0].copy()
        if len(bdf_pos) == 0:
            return np.nan
        p_d1 = float(bdf_pos.iloc[0]["close"])
        bdf_pos["ym"] = bdf_pos["date"].dt.strftime("%Y-%m")
        mc_by_ym = bdf_pos.groupby("ym")["close"].last().to_dict()
        ym0 = next((ym for ym in sorted(mc_by_ym) if ym in smap and smap[ym] > 0), None)
        if ym0 is None:
            return np.nan
        end_ym = max(smap.keys())
        if end_ym < ym0:
            return np.nan
        return float((1.0 + float(ir) / 100.0) * (float(mc_by_ym[ym0]) / p_d1) * (smap[end_ym] / smap[ym0]) - 1.0)

    d33["hfq_tr"] = [_chain_hfq_tr(r) for _, r in d33.iterrows()]
    bg_tr = d33[ok & d33["proceeds_bn"].notna() & d33["hfq_tr"].notna()].copy()
    dg_all = d33[noq & d33["proceeds_bn"].notna()].copy()
    dg_obs = dg_all[dg_all["hfq_tr"].notna()].copy()
    dg_rem = dg_all[dg_all["hfq_tr"].isna()].copy()

    # obs_recov=None keeps the last observed pre-delisting quote as the recovery proxy for the 363 issuers;
    # a number replaces that proxy with a flat recovery of offer value (0.0 = total loss), so readers can see
    # how much the result depends on treating the last quote as the exit value.
    for scen_lbl, res_recov, obs_recov in [
        ("LikeForLike_HFQ_TR_Verified_N2115", None, None),
        ("LikeForLike_HFQ_TR_Plus_ObsPreDelist363_0pctRem112", 0.0, None),
        ("LikeForLike_HFQ_TR_Plus_ObsPreDelist363_50pctRem112", 0.5, None),
        ("LikeForLike_HFQ_TR_Plus_ObsPreDelist363_100pctRem112", 1.0, None),
        ("LikeForLike_HFQ_TR_Plus_All475_at_0pct_Recovery", 0.0, 0.0),
        ("LikeForLike_HFQ_TR_Plus_All475_at_50pct_Recovery", 0.5, 0.5),
    ]:
        for ex_lbl, ex_mask_fn in [
            ("All", lambda df_: pd.Series(True, index=df_.index)),
            ("Excl_Tencent", lambda df_: ~df_["company_name"].str.contains("Tencent", na=False)),
            ("Excl_Tencent_and_AIA", lambda df_: ~df_["company_name"].str.contains("Tencent|AIA Group", na=False)),
        ]:
            bg = bg_tr[ex_mask_fn(bg_tr)]
            p_tot = bg["proceeds_bn"].sum()
            g_ipo = (bg["proceeds_bn"] * bg["hfq_tr"]).sum()
            g_hpx = (bg["proceeds_bn"] * bg["b_px"]).sum()
            g_htr = (bg["proceeds_bn"] * bg["b_tr"]).sum()
            n_tot = len(bg)
            if res_recov is not None:
                d1 = dg_obs[ex_mask_fn(dg_obs)]
                d2 = dg_rem[ex_mask_fn(dg_rem)]
                n_tot += len(d1) + len(d2)
                p_tot += d1["proceeds_bn"].sum() + d2["proceeds_bn"].sum()
                d1_ret = d1["hfq_tr"] if obs_recov is None else pd.Series(obs_recov - 1.0, index=d1.index)
                g_ipo += (d1["proceeds_bn"] * d1_ret).sum() + (d2["proceeds_bn"] * (res_recov - 1.0)).sum()
                g_hpx += (d1["proceeds_bn"] * d1["b_px"]).sum() + (d2["proceeds_bn"] * d2["b_px"]).sum()
                g_htr += (d1["proceeds_bn"] * d1["b_tr"]).sum() + (d2["proceeds_bn"] * d2["b_tr"]).sum()
            wr_tr = (p_tot + g_ipo) / (p_tot + g_htr)
            eq_rows.append({
                "Panel": "C_LikeForLike_HFQ_TotalReturn_Bounds",
                "Horizon_or_Scenario": scen_lbl,
                "Group": ex_lbl,
                "N": n_tot,
                "Proceeds_HKD_Bn": round(float(p_tot), 2),
                "IPO_Gain_HKD_Bn": round(float(g_ipo), 2),
                "HSI_Px_Gain_HKD_Bn": round(float(g_hpx), 2),
                "HSI_TR_Gain_HKD_Bn": round(float(g_htr), 2),
                "WR_vs_HSI_Price": np.nan,
                "WR_vs_HSI_TR": round(float(wr_tr), 3),
                "EW_Mean_Excess_vs_HSI_TR_Pct": np.nan,
            })

    t3 = pd.DataFrame(eq_rows)
    t3.to_csv(EXT_DIR / "remed_table3_wealth_horizons_and_bounds.csv", index=False)

    # Panel 3B: Pure Main Board First-Time IPOs (excluding GEM & A+H) vs US Ritter
    us_hk = pd.read_csv(OV_DIR / "table5_us_hk_parallel_clean_1994_2026.csv")
    d33["is_ah_bool"] = d33["is_ah"].fillna(False).astype(bool)
    pure_mb = d33[(d33["board"] == "Main Board") & (~d33["is_ah_bool"])].copy()
    ah_mb = d33[(d33["board"] == "Main Board") & (d33["is_ah_bool"])].copy()

    yr_pure = pure_mb.groupby("list_year").agg(
        HK_PureMB_FirstTime_N=("stock_code", "count"),
        HK_PureMB_Proceeds_HKD_Bn=("proceeds_bn", "sum"),
    ).reset_index().rename(columns={"list_year": "Year"})
    yr_ah = ah_mb.groupby("list_year").agg(
        HK_AH_AlreadyListed_N=("stock_code", "count"),
        HK_AH_Proceeds_HKD_Bn=("proceeds_bn", "sum"),
    ).reset_index().rename(columns={"list_year": "Year"})

    merged = us_hk.merge(yr_pure, on="Year", how="left").merge(yr_ah, on="Year", how="left")
    merged["HK_PureMB_FirstTime_N"] = merged["HK_PureMB_FirstTime_N"].fillna(0).astype(int)
    merged["HK_AH_AlreadyListed_N"] = merged["HK_AH_AlreadyListed_N"].fillna(0).astype(int)
    merged["HK_PureMB_Proceeds_USD_Bn"] = (merged["HK_PureMB_Proceeds_HKD_Bn"].fillna(0.0) / 7.8).round(2)
    merged["HK_All_N"] = merged["HK_MB_N"] + merged["HK_GEM_N"]

    sum_rows = []
    for per_lbl, ylo, yhi in [("1994-1999 (Pre-2000)", 1994, 1999), ("2000-2025 (Post-2000)", 2000, 2025), ("2000-2026Q3", 2000, 2026)]:
        s = merged[(merged["Year"] >= ylo) & (merged["Year"] <= yhi)]
        sum_rows.append({
            "Period": per_lbl,
            "Years": len(s),
            "US_Ritter_Ann_N": round(float(s["US_Ritter_N"].mean()), 1),
            "HK_All_Ann_N": round(float(s["HK_All_N"].mean()), 1),
            "HK_MB_All_Ann_N": round(float(s["HK_MB_N"].mean()), 1),
            "HK_PureMB_FirstTime_Ann_N": round(float(s["HK_PureMB_FirstTime_N"].mean()), 1),
            "HK_AH_Ann_N": round(float(s["HK_AH_AlreadyListed_N"].mean()), 1),
            "US_Ritter_Ann_USD_Bn": round(float(s["US_Proceeds_USD_Bn"].mean()), 2),
            "HK_MB_All_Ann_USD_Bn": round(float(s["HK_MB_Proceeds_USD_Bn"].mean()), 2),
            "HK_PureMB_Ann_USD_Bn": round(float(s["HK_PureMB_Proceeds_USD_Bn"].mean()), 2),
        })
    pd.DataFrame(sum_rows).to_csv(EXT_DIR / "remed_table3b_us_hk_pure_mb.csv", index=False)
    print("Saved remed_table3 & remed_table3b.")


# =============================================================================
# MODULE 4: SOUTHBOUND CONNECT T_STAB+1 PANEL DiD & LOCKUP EXPOSURE CROSS-SEC
# =============================================================================
def _load_exact_bars(sc: str | int, ld_str: str) -> pd.DataFrame | None:
    num = int(str(sc).split(".")[0].strip())
    exact = MC_DIR / f"{num:04d}.HK_{ld_str}.json"
    if exact.exists():
        b = pd.DataFrame(json.loads(exact.read_text()), columns=["date", "open", "close", "high", "low", "vol", "turn"])
        b["date"] = pd.to_datetime(b["date"])
        return b[b["date"] >= pd.to_datetime(ld_str)].reset_index(drop=True)
    for h in sorted(MC_DIR.glob(f"{num:04d}.HK_*.json")):
        if ld_str[:4] in h.name:
            b = pd.DataFrame(json.loads(h.read_text()), columns=["date", "open", "close", "high", "low", "vol", "turn"])
            b["date"] = pd.to_datetime(b["date"])
            return b[b["date"] >= pd.to_datetime(ld_str)].reset_index(drop=True)
    return None


def run_module4_events() -> None:
    print("\n--- Module 4: Southbound T_stab+1 Panel DiD & Lockup Exposure Cross-Section ---")
    n226 = pd.read_csv(OV_DIR / "clean_micro_panel_2025_2026_N226.csv")
    mb = pd.read_csv(MB_MASTER_CSV, low_memory=False)
    mb["stock_code"] = mb["Stock Code"].astype(str).str.strip()
    sc_df = n226.merge(
        mb[["stock_code", "Stabilization period end date", "Over-allotment Option (%)", "Greenshoe exercise rate (%)"]].drop_duplicates("stock_code"),
        on="stock_code",
        how="left",
    )

    panel_rows = []
    for _, r in sc_df.iterrows():
        ld_str = str(r["listing_date"])[:10]
        ld = pd.to_datetime(ld_str)
        bdf = _load_exact_bars(r["stock_code"], ld_str)
        if bdf is None or len(bdf) < 32:
            continue
        stab_dt = pd.to_datetime(r["Stabilization period end date"], errors="coerce")
        has_exact_stab = int(pd.notna(stab_dt))
        if pd.isna(stab_dt):
            stab_dt = ld + pd.Timedelta(days=30)
        post_idx = bdf.index[bdf["date"] > stab_dt]
        if len(post_idx) == 0:
            continue
        idx0 = int(post_idx[0])
        if idx0 < 8 or idx0 + 15 >= len(bdf):
            continue
        pre_t = float(bdf.loc[idx0 - 8 : idx0 - 1, "turn"].mean())
        if pre_t <= 0:
            continue
        gs_rate = pd.to_numeric(r["Greenshoe exercise rate (%)"], errors="coerce")
        gs_rate = 0.0 if pd.isna(gs_rate) else float(gs_rate)
        for rel_k in range(-8, 16):
            t_val = float(bdf.loc[idx0 + rel_k, "turn"])
            panel_rows.append({
                "stock_code": r["stock_code"],
                "is_ah": int(r["is_ah_dual_listed"]),
                "has_exact_stab": has_exact_stab,
                "gs_rate": gs_rate,
                "rel_day": rel_k,
                "post_stab": int(rel_k >= 0),
                "log_turn_norm": float(np.log((t_val + 1.0) / (pre_t + 1.0))),
                "norm_turn": float(t_val / pre_t),
            })

    pdf = pd.DataFrame(panel_rows)
    out_rows = []
    for sub_lbl, sub_df in [
        ("All_Valid_Stab_Window_[-8,+15]", pdf),
        ("All_Valid_Stab_Window_[-8,+9]", pdf[pdf["rel_day"] <= 9]),
        ("Exact_Stab_Date_Only_[-8,+15]", pdf[pdf["has_exact_stab"] == 1]),
    ]:
        for dep in ["log_turn_norm", "norm_turn"]:
            s = sub_df.copy()
            s["ah_x_post"] = s["is_ah"] * s["post_stab"]
            fit = smf.ols(f"{dep} ~ ah_x_post + C(stock_code) + C(rel_day)", data=s).fit(
                cov_type="cluster", cov_kwds={"groups": s["stock_code"]}
            )
            n_ah = int(s.loc[s["is_ah"] == 1, "stock_code"].nunique())
            n_non = int(s.loc[s["is_ah"] == 0, "stock_code"].nunique())
            out_rows.append({
                "Panel": "A_Southbound_Tstab_Panel_DiD",
                "Sample_or_Spec": sub_lbl,
                "Outcome": dep,
                "Regressor": "is_ah * post_stab (Issuer FE + RelDay FE)",
                "N_Obs": int(fit.nobs),
                "N_Issuers": n_ah + n_non,
                "Aux_Info": f"AH={n_ah}, NonAH={n_non}",
                "Estimate": round(float(fit.params["ah_x_post"]), 4),
                "SE_Clustered": round(float(fit.bse["ah_x_post"]), 4),
                "t_stat": round(float(fit.tvalues["ah_x_post"]), 2),
                "p_val": round(float(fit.pvalues["ah_x_post"]), 4),
            })

    # Stabilization-controlled panel DiD & pre-event trend check [-8, -1]
    s_ctrl = pdf.copy()
    s_ctrl["ah_x_post"] = s_ctrl["is_ah"] * s_ctrl["post_stab"]
    s_ctrl["gs_x_post"] = s_ctrl["gs_rate"] * s_ctrl["post_stab"]
    fit_sc = smf.ols("log_turn_norm ~ ah_x_post + gs_x_post + C(stock_code) + C(rel_day)", data=s_ctrl).fit(
        cov_type="cluster", cov_kwds={"groups": s_ctrl["stock_code"]}
    )
    out_rows.append({
        "Panel": "A_Southbound_Tstab_Panel_DiD",
        "Sample_or_Spec": "All_Valid_Stab_Window_[-8,+15]_Plus_GreenshoeCtrl",
        "Outcome": "log_turn_norm",
        "Regressor": "is_ah * post_stab (+ gs_rate*post + FEs)",
        "N_Obs": int(fit_sc.nobs),
        "N_Issuers": int(s_ctrl["stock_code"].nunique()),
        "Aux_Info": f"gs_x_post={fit_sc.params['gs_x_post']:.4f} (t={fit_sc.tvalues['gs_x_post']:.2f})",
        "Estimate": round(float(fit_sc.params["ah_x_post"]), 4),
        "SE_Clustered": round(float(fit_sc.bse["ah_x_post"]), 4),
        "t_stat": round(float(fit_sc.tvalues["ah_x_post"]), 2),
        "p_val": round(float(fit_sc.pvalues["ah_x_post"]), 4),
    })
    pre_df = pdf[pdf["rel_day"] < 0].copy()
    pre_df["ah_x_relday"] = pre_df["is_ah"] * pre_df["rel_day"]
    fit_pre = smf.ols("log_turn_norm ~ ah_x_relday + C(stock_code) + C(rel_day)", data=pre_df).fit(
        cov_type="cluster", cov_kwds={"groups": pre_df["stock_code"]}
    )
    out_rows.append({
        "Panel": "A_Southbound_Tstab_Panel_DiD",
        "Sample_or_Spec": "PreTrend_Diagnostic_[-8,-1]",
        "Outcome": "log_turn_norm",
        "Regressor": "is_ah * rel_day (Issuer FE + RelDay FE)",
        "N_Obs": int(fit_pre.nobs),
        "N_Issuers": int(pre_df["stock_code"].nunique()),
        "Aux_Info": "Pre-event slope differential per day",
        "Estimate": round(float(fit_pre.params["ah_x_relday"]), 4),
        "SE_Clustered": round(float(fit_pre.bse["ah_x_relday"]), 4),
        "t_stat": round(float(fit_pre.tvalues["ah_x_relday"]), 2),
        "p_val": round(float(fit_pre.pvalues["ah_x_relday"]), 4),
    })

    # Panel B: Lockup Expiry Exposure-Scaled Cross-Section (Day +180 CAR & Vol Shock)
    lk_obs = pd.read_csv(EXT_DIR / "lockup_n226_matched_firm_cars_obs.csv")
    lk_pair = pd.read_csv(EXT_DIR / "clean_2025_2026_paired_6m_12m_lockup_panel.csv")
    lk = lk_obs.merge(
        lk_pair[["stock_code", "vol_shock_6m_bars", "vol_shock_12m_bars", "pre_unlock_runup_6m"]],
        on="stock_code",
        how="left",
    ).merge(
        n226[["stock_code", "unrestricted_free_float_pct", "public_offer_fraction_pct"]],
        on="stock_code",
        how="left",
    )
    lk["cs_pct_10pp"] = pd.to_numeric(lk["cs_pct"], errors="coerce") / 10.0
    lk["vol_shock_6m"] = pd.to_numeric(lk["vol_shock_6m_bars"], errors="coerce")
    lk["mcar20_6m"] = pd.to_numeric(lk["mcar20_6m_bars"], errors="coerce")
    lk["mcar5_6m"] = pd.to_numeric(lk["mcar5_6m_bars"], errors="coerce")
    lk["mcar20_8m_placebo"] = pd.to_numeric(lk["mcar20_8m"], errors="coerce")

    for dep in ["mcar20_6m", "mcar5_6m", "vol_shock_6m", "mcar20_8m_placebo"]:
        sub = lk.dropna(subset=[dep, "cs_pct_10pp", "is_cayman", "is_ah_dual_listed", "log_proc"]).copy()
        fit = smf.ols(f"{dep} ~ cs_pct_10pp + is_cayman + is_ah_dual_listed + log_proc", data=sub).fit(cov_type="HC3")
        for var in ["cs_pct_10pp", "is_cayman"]:
            out_rows.append({
                "Panel": "B_Lockup_Exposure_CrossSection",
                "Sample_or_Spec": "HC3 OLS (+AH, +LogProc)",
                "Outcome": dep,
                "Regressor": var,
                "N_Obs": int(fit.nobs),
                "N_Issuers": int(fit.nobs),
                "Aux_Info": f"R2={fit.rsquared:.3f}",
                "Estimate": round(float(fit.params[var]), 4),
                "SE_Clustered": round(float(fit.bse[var]), 4),
                "t_stat": round(float(fit.tvalues[var]), 2),
                "p_val": round(float(fit.pvalues[var]), 4),
            })

    t4 = pd.DataFrame(out_rows)
    t4.to_csv(EXT_DIR / "remed_table4_event_study_did_and_lockup.csv", index=False)
    print(f"Saved remed_table4_event_study_did_and_lockup.csv ({len(t4)} rows).")


def main() -> None:
    run_module1_asset_pricing()
    run_module2_pn18_and_mechb()
    run_module3_wealth_and_ushk()
    run_module4_events()
    print("\nALL 4 REFEREE #2 REMEDIATION MODULES COMPLETED.")


if __name__ == "__main__":
    main()
