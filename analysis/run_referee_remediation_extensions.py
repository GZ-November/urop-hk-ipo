#!/usr/bin/env python3
"""
run_referee_remediation_extensions.py
=====================================
Computes all 4 empirical extensions & referee robustness suites:
1. Carhart 4-Factor (+HML) Calendar-Time Robustness (`2000-2026Q3`, `2008-2026Q3`, `1994-2026Q3`):
   - Strictly out-of-sample HKEX-seasoned (>36M) 2x3 Size x Book-to-Market `HML_HKEX`
     using lagged historical annual TOTAL_PARENT_EQUITY (6-month FF reporting lag)
     over dynamic monthly market cap `dyn_mcap` (no look-ahead bias).
   - Cross-checked against Kenneth French Asia-Pacific ex-Japan `HML` and full 4F (`Mkt-RF, SMB, HML, WML`).
2. Industry x Size Matched-Firm CAR for Lockup Natural Experiment (`Table 12` / `IA.14`):
   - Matches each 2025-2026Q3 IPO to k=5 strictly-seasoned (>36M) HKEX Main Board peers
     in the exact same industry & closest market cap (`matched_peer_daily_cache/`).
   - Computes daily matched-firm CAR[-20,+20] and CAR[-5,+5] across Day +180 (N=123),
     Day +120 / Day +240 placebos, Paired Day +365 (N=64), and HC3 OLS Models 1-3 & 5.
3. Mechanism B Statistical Power (MDE), 6-point Webb WCB p-values, & HSICS-2 Sector FEs (`N=226, G=21`).
4. FINI Settlement Narrow-Window (`2021-2026` & `2022-2026`), Short-Rate Regime & Hot-Tier DiD Diagnostics.
"""
from __future__ import annotations

import bisect
import calendar
import datetime as dt
import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

REPO_ROOT = Path(__file__).resolve().parent.parent
OV_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"
SEAS_DIR = OV_DIR / "seasoned_monthly_hfq_cache"
MC_DIR = OV_DIR / "market_cache"
PEER_DAILY_DIR = OV_DIR / "matched_peer_daily_cache"

AS_OF_STR = "2026-11-12"
AS_OF_DATE = dt.date(2026, 11, 12)


def ym_diff(ym_start: str, ym_end: str) -> int:
    y1, m1 = int(ym_start[:4]), int(ym_start[5:7])
    y2, m2 = int(ym_end[:4]), int(ym_end[5:7])
    return (y2 - y1) * 12 + (m2 - m1)


def ym_add(ym: str, delta: int) -> str:
    y, m = int(ym[:4]), int(ym[5:7])
    tot = y * 12 + (m - 1) + delta
    return f"{tot // 12:04d}-{(tot % 12) + 1:02d}"


def add_calendar_months(value: dt.date, months: int) -> dt.date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return dt.date(year, month, day)


def wild_cluster_bootstrap_p_vec(
    df_est: pd.DataFrame,
    dep_col: str,
    exog_cols: list[str],
    target_var: str,
    cluster_col: str,
    B: int = 4999,
    seed: int = 42,
) -> float:
    """Cameron, Gelbach & Miller (2008) / Webb (2023) 6-point Wild Cluster Restricted (WCR) bootstrap."""
    rng = np.random.default_rng(seed)
    webb_weights = np.array([-np.sqrt(1.5), -1.0, -np.sqrt(0.5), np.sqrt(0.5), 1.0, np.sqrt(1.5)])

    X_full = sm.add_constant(df_est[exog_cols].astype(float))
    y_vec = df_est[dep_col].astype(float).values
    full_fit = sm.OLS(y_vec, X_full).fit(cov_type="cluster", cov_kwds={"groups": df_est[cluster_col]})
    t_obs = float(full_fit.tvalues[target_var])

    rest_cols = [c for c in exog_cols if c != target_var]
    X_rest = sm.add_constant(df_est[rest_cols].astype(float))
    rest_fit = sm.OLS(y_vec, X_rest).fit()
    yhat_r = rest_fit.fittedvalues.values
    u_r = rest_fit.resid.values

    X_mat = X_full.values
    var_idx = list(X_full.columns).index(target_var)
    clusters = df_est[cluster_col].values
    uniq_cl, inv_idx = np.unique(clusters, return_inverse=True)
    G = len(uniq_cl)
    n, k = X_mat.shape
    XtX_inv = np.linalg.inv(X_mat.T @ X_mat)
    dof_scale = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    cl_masks = [np.where(inv_idx == g)[0] for g in range(G)]

    t_boot = np.empty(B)
    for b in range(B):
        w = rng.choice(webb_weights, size=G)
        y_star = yhat_r + u_r * w[inv_idx]
        beta_star = XtX_inv @ (X_mat.T @ y_star)
        e_star = y_star - X_mat @ beta_star
        scores = X_mat * e_star[:, None]
        meat_jj = 0.0
        for idx_g in cl_masks:
            sg = scores[idx_g].sum(axis=0)
            v_j = XtX_inv[var_idx] @ sg
            meat_jj += v_j * v_j
        se_star = np.sqrt(dof_scale * meat_jj)
        t_boot[b] = beta_star[var_idx] / se_star
    return float((np.sum(np.abs(t_boot) >= np.abs(t_obs)) + 1.0) / (B + 1.0))


# =============================================================================
# 1. CARHART 4-FACTOR (+HML) LONG-RUN ROBUSTNESS
# =============================================================================
def run_module1_carhart_4f() -> pd.DataFrame:
    print("\n" + "=" * 80)
    print("1. CARHART 4-FACTOR (+HML) CALENDAR-TIME ROBUSTNESS (2000-2026 & 2008-2026)")
    print("=" * 80)

    fac = pd.read_csv(EXT_DIR / "clean_monthly_ctp_seasoned_factors_1994_2026.csv")
    kf = pd.read_csv(EXT_DIR / "kenfrench_apxj_factors_1994_2026.csv")
    fin = pd.read_csv(EXT_DIR / "hkex_eastmoney_annual_equity_1999_2026.csv", dtype={"SECURITY_CODE": str}, low_memory=False)
    master = pd.read_csv(OV_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)

    # Clean annual book equity: keep positive TOTAL_PARENT_EQUITY, exclude RMB dual counters (8xxxx)
    fin = fin[(fin["SECURITY_CODE"] < "80000") & fin["TOTAL_PARENT_EQUITY"].notna() & (fin["TOTAL_PARENT_EQUITY"] > 0)].copy()
    fin["rep_dt"] = pd.to_datetime(fin["REPORT_DATE"], errors="coerce")
    fin = fin.dropna(subset=["rep_dt"]).copy()
    # Keep fiscal year-end filings (prefer Dec-31 / Mar-31 / Jun-30; deduplicate by taking latest REPORT_DATE per stock-year)
    fin["rep_yr"] = fin["rep_dt"].dt.year
    fin["rep_mo"] = fin["rep_dt"].dt.month
    # Keep only standard fiscal year-ends if available, or latest report per stock-year
    fin = fin.sort_values(["SECURITY_CODE", "rep_dt"]).drop_duplicates(["SECURITY_CODE", "rep_yr"], keep="last").copy()
    fin["sym"] = "hk" + fin["SECURITY_CODE"]
    # 6-month Fama-French availability lag: available starting ym_avail = rep_ym + 6
    fin["rep_ym"] = fin["rep_dt"].dt.to_period("M").astype(str)
    fin["avail_ym"] = fin["rep_ym"].apply(lambda x: ym_add(x, 6))

    # Build lookup: sym -> sorted list of (avail_ym, book_equity_hkd)
    be_lookup: dict[str, list[tuple[str, float]]] = {}
    for sym, g in fin.groupby("sym"):
        pts = sorted((str(r["avail_ym"]), float(r["TOTAL_PARENT_EQUITY"])) for _, r in g.iterrows())
        be_lookup[sym] = pts

    # Build seasoned monthly universe (>36M post-IPO) from seasoned_monthly_hfq_cache
    clean_mask = (master["flag_recycled_or_transferred_ticker"].fillna(0) == 0) & (~master["flag_reverse_split_distortion"].fillna(False))
    clean_df = master[clean_mask].copy()
    all_ipo_nums: set[int] = set()
    ipo_meta: dict[str, tuple[str, float]] = {}
    for _, row in clean_df.iterrows():
        dig = "".join(ch for ch in str(row["stock_code"]) if ch.isdigit())
        if not dig:
            continue
        all_ipo_nums.add(int(dig))
        sym = f"hk{int(dig):05d}"
        if sym not in ipo_meta:
            sh = pd.to_numeric(row.get("ext_total_shares_listed"), errors="coerce")
            p0 = pd.to_numeric(row.get("offer_price_hkd"), errors="coerce")
            pr = pd.to_numeric(row.get("funds_raised_total_hkd"), errors="coerce")
            m0 = float(sh * p0) if (pd.notna(sh) and sh > 0 and pd.notna(p0) and p0 > 0) else (float(pr * 4.0) if pd.notna(pr) and pr > 0 else 5e8)
            ipo_meta[sym] = (str(row["listing_date"])[:7], m0)
    for sc in master["stock_code"].dropna().astype(str):
        dig = "".join(ch for ch in sc if ch.isdigit())
        if dig:
            all_ipo_nums.add(int(dig))

    pre94_syms = [f"hk{k:05d}" for k in range(1, 601) if k not in all_ipo_nums]
    seas_rows: list[dict[str, Any]] = []

    def _get_lagged_be(sym: str, ym: str) -> float | None:
        pts = be_lookup.get(sym)
        if not pts:
            return None
        idx = bisect.bisect_right([p[0] for p in pts], ym) - 1
        if idx < 0:
            return None
        av_ym, be_val = pts[idx]
        if ym_diff(av_ym, ym) > 24:  # stale > 2.5 years since fiscal close
            return None
        return be_val

    all_targets = [(s, "1990-01", 2e9) for s in pre94_syms] + [(s, v[0], v[1]) for s, v in ipo_meta.items()]
    for sym, anchor_ym, fb_mcap in all_targets:
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
        if anchor_ym >= "1994-01" and ym_diff(anchor_ym, first_ym) < -2:
            continue
        if anchor_ym < "1994-01" and first_ym > "1990-12":
            continue
        cur_mcap = item.get("cur_mcap_hkd")
        last_close = m_closes[yms[-1]]
        first_close = m_closes[first_ym]
        eff_list_ym = first_ym if anchor_ym < "1994-01" else anchor_ym

        for i in range(len(yms) - 1):
            prev_ym, curr_ym = yms[i], yms[i + 1]
            if curr_ym < "2000-01" or curr_ym > "2026-09" or ym_diff(prev_ym, curr_ym) != 1:
                continue
            if ym_diff(eff_list_ym, curr_ym) < 37:
                continue
            p_prev, p_curr = m_closes[prev_ym], m_closes[curr_ym]
            if p_prev <= 0:
                continue
            ret = (p_curr - p_prev) / p_prev
            dyn_mcap = (float(cur_mcap) * (p_prev / last_close)) if (cur_mcap and cur_mcap > 0 and last_close > 0) else (float(fb_mcap) * (p_prev / max(first_close, 1e-4)))
            be_lag = _get_lagged_be(sym, prev_ym)
            if be_lag is None or dyn_mcap <= 0:
                continue
            bm = be_lag / dyn_mcap
            if not (0.01 <= bm <= 20.0):  # exclude extreme data artifacts
                continue
            seas_rows.append({
                "sym": sym,
                "year_month": curr_ym,
                "ret": ret,
                "dyn_mcap": dyn_mcap,
                "bm": bm,
            })

    sdf = pd.DataFrame(seas_rows)
    q01, q99 = sdf["ret"].quantile([0.01, 0.99])
    sdf["clean_ret"] = sdf["ret"].clip(lower=q01, upper=q99)

    hml_rows = []
    for ym, g in sdf.groupby("year_month"):
        if len(g) < 30:
            hml_rows.append({"year_month": ym, "n_hml_stocks": len(g), "hml_hkex_vw_pct": np.nan, "hml_hkex_ew_pct": np.nan})
            continue
        med_mv = g["dyn_mcap"].median()
        q30, q70 = g["bm"].quantile([0.30, 0.70])
        cells_vw = {}
        cells_ew = {}
        for sz_lbl, sz_mask in [("S", g["dyn_mcap"] <= med_mv), ("B", g["dyn_mcap"] > med_mv)]:
            for bm_lbl, bm_mask in [("G", g["bm"] <= q30), ("V", g["bm"] >= q70)]:
                sub = g[sz_mask & bm_mask]
                if len(sub) >= 3:
                    w = sub["dyn_mcap"].values
                    cells_vw[f"{sz_lbl}{bm_lbl}"] = float(np.average(sub["clean_ret"].values, weights=w) * 100.0)
                    cells_ew[f"{sz_lbl}{bm_lbl}"] = float(sub["clean_ret"].mean() * 100.0)
        if len(cells_vw) == 4:
            hml_vw = 0.5 * (cells_vw["SV"] + cells_vw["BV"]) - 0.5 * (cells_vw["SG"] + cells_vw["BG"])
            hml_ew = 0.5 * (cells_ew["SV"] + cells_ew["BV"]) - 0.5 * (cells_ew["SG"] + cells_ew["BG"])
        else:
            hml_vw = np.nan
            hml_ew = np.nan
        hml_rows.append({"year_month": ym, "n_hml_stocks": len(g), "hml_hkex_vw_pct": round(hml_vw, 4), "hml_hkex_ew_pct": round(hml_ew, 4)})

    hml_df = pd.DataFrame(hml_rows).sort_values("year_month")
    print(f"    Built strictly-seasoned HKEX HML (2x3 Size x Lagged Book-to-Market): {len(hml_df)} months "
          f"(min firms/mo={hml_df['n_hml_stocks'].min()}, 2002+ min={hml_df[hml_df['year_month']>='2002-01']['n_hml_stocks'].min()}, "
          f"2008+ min={hml_df[hml_df['year_month']>='2008-01']['n_hml_stocks'].min()}, max={hml_df['n_hml_stocks'].max()})")

    m_all = fac.merge(kf, on="year_month", how="left").merge(hml_df, on="year_month", how="left")
    m_all.to_csv(EXT_DIR / "clean_monthly_ctp_seasoned_4factors_1994_2026.csv", index=False)

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
    windows = [
        ("1994-2026Q3", "1994-01", "2026-09"),
        ("2000-2026Q3", "2000-01", "2026-09"),
        ("2008-2026Q3", "2008-01", "2026-09"),
    ]
    specs = [
        ("HKEX_Seasoned_3F", ["mkt_tr_excess_pct", "smb_seasoned_pct", "mom_seasoned_pct"], "rf_monthly_pct"),
        ("HKEX_Seasoned_4F_HML_HKEX", ["mkt_tr_excess_pct", "smb_seasoned_pct", "hml_hkex_vw_pct", "mom_seasoned_pct"], "rf_monthly_pct"),
        ("HKEX_Seasoned_4F_HML_APxJP", ["mkt_tr_excess_pct", "smb_seasoned_pct", "kf_hml", "mom_seasoned_pct"], "rf_monthly_pct"),
        ("KenFrench_APxJP_4F", ["kf_mkt_rf", "kf_smb", "kf_hml", "kf_wml"], "kf_rf"),
    ]

    out_rows = []
    for win_lbl, ym_lo, ym_hi in windows:
        wdf = m_all[(m_all["year_month"] >= ym_lo) & (m_all["year_month"] <= ym_hi)].copy()
        for spec_lbl, f_cols, rf_col in specs:
            if win_lbl == "1994-2026Q3" and spec_lbl == "HKEX_Seasoned_4F_HML_HKEX":
                continue  # HKEX annual book equity starts 2000-2001
            for p_col, n_col, p_name in portfolios:
                sub = wdf.dropna(subset=[p_col, rf_col] + f_cols).copy()
                if len(sub) < 24:
                    continue
                y = sub[p_col].astype(float) - sub[rf_col].astype(float)
                X = sm.add_constant(sub[f_cols].astype(float))
                m_ols = sm.OLS(y, X).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
                w_wls = np.sqrt(sub[n_col].astype(float).clip(lower=1.0))
                m_wls = sm.WLS(y, X, weights=w_wls).fit(cov_type="HC3")
                hml_key = [c for c in f_cols if "hml" in c]
                beta_hml = float(m_wls.params[hml_key[0]]) if hml_key else np.nan
                t_hml = float(m_wls.tvalues[hml_key[0]]) if hml_key else np.nan
                out_rows.append({
                    "Sample_Window": win_lbl,
                    "Factor_Model": spec_lbl,
                    "Portfolio": p_name,
                    "Months_T": len(sub),
                    "OLS_Alpha_Mo": round(float(m_ols.params["const"]), 3),
                    "OLS_t_HAC": round(float(m_ols.tvalues["const"]), 2),
                    "OLS_p_HAC": round(float(m_ols.pvalues["const"]), 4),
                    "WLS_Alpha_Mo": round(float(m_wls.params["const"]), 3),
                    "WLS_t_HC3": round(float(m_wls.tvalues["const"]), 2),
                    "WLS_p_HC3": round(float(m_wls.pvalues["const"]), 4),
                    "Beta_HML_WLS": round(beta_hml, 3) if pd.notna(beta_hml) else np.nan,
                    "t_HML_WLS": round(t_hml, 2) if pd.notna(t_hml) else np.nan,
                    "R2_WLS": round(float(m_wls.rsquared), 3),
                })

    res_df = pd.DataFrame(out_rows)
    res_df.to_csv(EXT_DIR / "ext_table10c_carhart4f_hml_robustness.csv", index=False)
    print("\n--- Summary: Main Board Portfolios Across 3F vs. 4F (+HML) ---")
    mb_show = res_df[res_df["Portfolio"].str.startswith("Main Board")]
    print(mb_show.to_string(index=False))
    return res_df


# =============================================================================
# 2. INDUSTRY x SIZE MATCHED-FIRM LOCKUP CAR (Table 12 & Table IA.14)
# =============================================================================
def _load_daily_close_map(cache_path: Path) -> dict[str, float]:
    if not cache_path.exists():
        return {}
    rows = json.loads(cache_path.read_text(encoding="utf-8"))
    return {str(b[0])[:10]: float(b[2]) for b in rows if b[2] and float(b[2]) > 0}


def _load_ipo_bars(stock_code: str, ld_str: str) -> list[list[Any]]:
    cands = sorted(MC_DIR.glob(f"{stock_code}_*.json"))
    if not cands:
        num = stock_code.split(".")[0].lstrip("0")
        for z in [4, 5]:
            cands = sorted(MC_DIR.glob(f"{num.zfill(z)}.HK_*.json"))
            if cands:
                break
    if not cands:
        return []
    bars = json.loads(cands[0].read_text(encoding="utf-8"))
    return [b for b in bars if b[0] >= ld_str and b[0] <= AS_OF_STR]


def run_module2_matched_firm_lockup() -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 80)
    print("2. INDUSTRY x SIZE MATCHED-FIRM LOCKUP CAR (Day +120, +180, +240, +365)")
    print("=" * 80)

    paired = pd.read_csv(EXT_DIR / "clean_2025_2026_paired_6m_12m_lockup_panel.csv")
    peers_df = pd.read_csv(EXT_DIR / "lockup_n226_industry_size_matched_peers.csv")
    m226 = pd.read_csv(OV_DIR / "clean_micro_panel_2025_2026_N226.csv")
    hsi_map = json.loads((MC_DIR / "hkHSI_1994_2026.json").read_text(encoding="utf-8"))
    hsi_dates = sorted(hsi_map.keys())

    meta = m226[[
        "stock_code", "is_prc_h_share", "is_ah_dual_listed", "is_18a", "is_18c",
        "cornerstone_pct_of_offering", "gross_proceeds_hkd_m",
    ]].drop_duplicates("stock_code")
    p = paired.merge(meta, on="stock_code", how="left").merge(peers_df[["stock_code", "peer_codes_json"]], on="stock_code", how="left")
    p["is_cayman"] = (p["is_prc_h_share"] == 0).astype(int)

    # Preload daily peer close maps
    peer_close_maps: dict[str, dict[str, float]] = {}
    for pjson in p["peer_codes_json"].dropna().unique():
        for pc in json.loads(pjson):
            if pc not in peer_close_maps:
                peer_close_maps[pc] = _load_daily_close_map(PEER_DAILY_DIR / f"hk{pc}.json")

    def _compute_matched_car(bars: list[list[Any]], peer_codes: list[str], event_date: dt.date) -> tuple[float | None, float | None, float | None]:
        if not bars or event_date > AS_OF_DATE:
            return None, None, None
        ev_str = event_date.isoformat()
        u_idx = next((i for i, b in enumerate(bars) if b[0] >= ev_str), None)
        if u_idx is None:
            return None, None, None
        if bisect.bisect_left(hsi_dates, bars[u_idx][0]) - bisect.bisect_left(hsi_dates, ev_str) > 2:
            return None, None, None

        def _car(lo: int, hi: int) -> float | None:
            if lo < 1 or hi >= len(bars):
                return None
            tot = 0.0
            for i in range(lo, hi + 1):
                d_curr, d_prev = bars[i][0], bars[i - 1][0]
                p_curr, p_prev = bars[i][2], bars[i - 1][2]
                if not (p_curr and p_prev and p_curr > 0 and p_prev > 0):
                    return None
                r_s = p_curr / p_prev - 1.0
                # Equal-weighted industry x size matched peer return on (d_prev -> d_curr)
                peer_rets = []
                for pc in peer_codes:
                    pmap = peer_close_maps.get(pc, {})
                    pc_c = pmap.get(d_curr)
                    pc_p = pmap.get(d_prev)
                    if pc_c and pc_p and pc_c > 0 and pc_p > 0:
                        peer_rets.append(pc_c / pc_p - 1.0)
                if not peer_rets:
                    return None
                tot += (r_s - float(np.mean(peer_rets)))
            return tot * 100.0

        c20 = _car(u_idx - 20, u_idx + 20)
        c5 = _car(u_idx - 5, u_idx + 5)
        pre_runup = ((bars[u_idx - 21][2] / bars[0][2] - 1.0) * 100.0) if (u_idx >= 22 and bars[0][2] > 0) else None
        return c20, c5, pre_runup

    # Compute matched-firm CARs at D+120 (4M), D+180 (6M), D+240 (8M), D+365 (12M)
    obs_rows = []
    for _, row in p.iterrows():
        ld_str = str(row["listing_date"])[:10]
        ld_d = dt.date.fromisoformat(ld_str)
        bars = _load_ipo_bars(row["stock_code"], ld_str)
        pcodes = json.loads(row["peer_codes_json"]) if pd.notna(row["peer_codes_json"]) else []
        if not bars or not pcodes:
            continue

        # Use exact unlock_6m_date when cornerstone exists (for N=123 consistency) AND calendar 6M for full matured bars
        u6_master_d = dt.date.fromisoformat(str(row["unlock_6m_date"])[:10]) if (row["has_cornerstone_unlock_date"] == 1 and pd.notna(row["unlock_6m_date"])) else None
        u6_cal_d = add_calendar_months(ld_d, 6)
        u12_d = dt.date.fromisoformat(str(row["unlock_12m_date"])[:10]) if pd.notna(row["unlock_12m_date"]) else add_calendar_months(ld_d, 12)

        c20_4m, c5_4m, _ = _compute_matched_car(bars, pcodes, add_calendar_months(ld_d, 4))
        c20_6m_cal, c5_6m_cal, run6_cal = _compute_matched_car(bars, pcodes, u6_cal_d)
        c20_6m_m, c5_6m_m, run6_m = _compute_matched_car(bars, pcodes, u6_master_d) if u6_master_d else (None, None, None)
        c20_8m, c5_8m, _ = _compute_matched_car(bars, pcodes, add_calendar_months(ld_d, 8))
        c20_12m, c5_12m, run12 = _compute_matched_car(bars, pcodes, u12_d)

        obs_rows.append({
            "stock_code": row["stock_code"],
            "is_prc_h_share": row["is_prc_h_share"],
            "is_ah_dual_listed": row["is_ah_dual_listed"],
            "is_cayman": row["is_cayman"],
            "is_tech_18ac": int((row["is_18a"] == 1) or (row["is_18c"] == 1)),
            "cs_pct": row["cornerstone_pct_of_offering"],
            "log_proc": np.log(row["gross_proceeds_hkd_m"]) if pd.notna(row["gross_proceeds_hkd_m"]) else np.nan,
            "mcar20_4m": c20_4m,
            "mcar20_6m_master": c20_6m_m,
            "mcar5_6m_master": c5_6m_m,
            "runup_6m_master": run6_m,
            "mcar20_6m_bars": c20_6m_cal,
            "mcar5_6m_bars": c5_6m_cal,
            "mcar20_8m": c20_8m,
            "mcar20_12m": c20_12m,
            "mcar5_12m": c5_12m,
            # Keep original HSI-adjusted for paired N=64 alignment check
            "hsi_car20_6m": row["car20_6m_bars"] * 100.0 if pd.notna(row["car20_6m_bars"]) else np.nan,
            "hsi_car20_12m": row["car20_12m_bars"] * 100.0 if pd.notna(row["car20_12m_bars"]) else np.nan,
        })

    odf = pd.DataFrame(obs_rows)
    odf.to_csv(EXT_DIR / "lockup_n226_matched_firm_cars_obs.csv", index=False)

    sum_rows = []
    def _add_group_stats(sub_df: pd.DataFrame, col: str, lbl: str, hor: str) -> None:
        h = sub_df[sub_df["is_prc_h_share"] == 1][col].dropna()
        c = sub_df[sub_df["is_prc_h_share"] == 0][col].dropna()
        p19 = sub_df[(sub_df["is_prc_h_share"] == 1) & (sub_df["is_ah_dual_listed"] == 0)][col].dropna()
        ah = sub_df[sub_df["is_ah_dual_listed"] == 1][col].dropna()
        for g_lbl, s in [
            (f"{lbl} — PRC H-Shares", h),
            (f"{lbl} — Pure Ch.19A H-Shares", p19),
            (f"{lbl} — A+H Dual-Listed", ah),
            (f"{lbl} — Cayman Red-Chips", c),
        ]:
            if len(s) >= 3:
                t1, p1 = stats.ttest_1samp(s, 0)
                w1 = stats.wilcoxon(s).pvalue if len(s) >= 5 else np.nan
                sum_rows.append({
                    "Window_Group": g_lbl, "Benchmark_Window": hor, "N": len(s),
                    "Mean_Matched_CAR_Pct": round(float(s.mean()), 2),
                    "Med_Matched_CAR_Pct": round(float(s.median()), 2),
                    "t_stat": round(float(t1), 2), "p_value": round(float(p1), 4),
                    "Wilcoxon_MW_p": round(float(w1), 4) if pd.notna(w1) else np.nan,
                })
        if len(c) >= 3 and len(h) >= 3:
            tw, pw = stats.ttest_ind(c, h, equal_var=False)
            _, pmw = stats.mannwhitneyu(c, h, alternative="two-sided")
            sum_rows.append({
                "Window_Group": f"{lbl} — DiD (Cayman minus H-Share)", "Benchmark_Window": hor, "N": len(c) + len(h),
                "Mean_Matched_CAR_Pct": round(float(c.mean() - h.mean()), 2),
                "Med_Matched_CAR_Pct": round(float(c.median() - h.median()), 2),
                "t_stat": round(float(tw), 2), "p_value": round(float(pw), 4),
                "Wilcoxon_MW_p": round(float(pmw), 4),
            })

    _add_group_stats(odf, "mcar20_6m_master", "Day +180 (Cornerstone Cohort)", "Ind×Size CAR[-20,+20]")
    _add_group_stats(odf, "mcar5_6m_master", "Day +180 Narrow (CS Cohort)", "Ind×Size CAR[-5,+5]")
    _add_group_stats(odf, "mcar20_6m_bars", "Day +180 (All Matured Bars)", "Ind×Size CAR[-20,+20]")
    _add_group_stats(odf, "mcar20_4m", "Placebo Day +120 (4M)", "Ind×Size CAR[-20,+20]")
    _add_group_stats(odf, "mcar20_8m", "Placebo Day +240 (8M)", "Ind×Size CAR[-20,+20]")

    # Paired 6M vs 12M
    pr = odf.dropna(subset=["mcar20_6m_bars", "mcar20_12m", "is_prc_h_share"]).copy()
    pr["m_diff_12_6"] = pr["mcar20_12m"] - pr["mcar20_6m_bars"]
    for col_p, h_lbl in [("mcar20_6m_bars", "Paired Day +180"), ("mcar20_12m", "Paired Day +365"), ("m_diff_12_6", "Within-Firm (12M - 6M)")]:
        _add_group_stats(pr, col_p, f"Paired (N={len(pr)})", h_lbl)

    sum_df = pd.DataFrame(sum_rows)
    sum_df.to_csv(EXT_DIR / "ext_table15c_matched_firm_lockup_car.csv", index=False)
    print(sum_df.to_string(index=False))

    # Multivariate HC3 OLS on Industry x Size Matched-Firm CAR[-20,+20]
    ols_rows = []
    d180 = odf.dropna(subset=["mcar20_6m_master", "is_cayman", "cs_pct", "log_proc"]).copy()
    for m_name, fml, df_m in [
        ("Matched_M1_Univariate_D180", "mcar20_6m_master ~ is_cayman", d180),
        ("Matched_M2_Deal_Route_Ctrls_D180", "mcar20_6m_master ~ is_cayman + cs_pct + log_proc + is_ah_dual_listed + is_tech_18ac", d180),
        ("Matched_M3_Add_PreRunup_D180", "mcar20_6m_master ~ is_cayman + cs_pct + log_proc + is_ah_dual_listed + is_tech_18ac + runup_6m_master", d180.dropna(subset=["runup_6m_master"])),
        ("Matched_M5_Paired_12M_minus_6M", "m_diff_12_6 ~ is_cayman + cs_pct + log_proc + is_ah_dual_listed + is_tech_18ac", pr),
    ]:
        fit = smf.ols(fml, data=df_m).fit(cov_type="HC3")
        for v in fit.params.index:
            ols_rows.append({
                "Model": m_name, "Variable": v,
                "Coef_pp": round(float(fit.params[v]), 2),
                "SE_HC3": round(float(fit.bse[v]), 2),
                "t_HC3": round(float(fit.tvalues[v]), 2),
                "p_HC3": round(float(fit.pvalues[v]), 4),
                "N": int(fit.nobs), "R2": round(float(fit.rsquared), 3),
            })
    ols_df = pd.DataFrame(ols_rows)
    ols_df.to_csv(EXT_DIR / "ext_table15d_matched_firm_lockup_ols.csv", index=False)
    print("\n--- Matched-Firm Lockup Multivariate HC3 OLS ---")
    print(ols_df[ols_df["Variable"].isin(["is_cayman", "cs_pct", "is_tech_18ac"])].to_string(index=False))
    return sum_df, ols_df


# =============================================================================
# 3. MECHANISM B POWER / WCB / HSICS-2 FE + FINI NARROW-WINDOW RATE-REGIME DiD
# =============================================================================
def run_module3_mechb_and_fini() -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 80)
    print("3A. MECHANISM B STATISTICAL POWER (MDE), WEBB WCB & HSICS-2 SECTOR ROBUSTNESS")
    print("=" * 80)

    d = pd.read_csv(OV_DIR / "clean_micro_panel_2025_2026_N226.csv")
    mb_raw = pd.read_csv(REPO_ROOT / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv", low_memory=False)
    mb_raw["stock_code"] = mb_raw["Stock Code"].astype(str).str.strip()
    mb_raw["hsic2"] = mb_raw["Industry classification code"].astype(str).str.extract(r"(\d+)")[0].fillna("00").str.zfill(6).str.slice(0, 2)
    # Merge flipping & hsic2
    d = d.merge(mb_raw[["stock_code", "First-day flipping ratio (%)", "hsic2"]], on="stock_code", how="left")
    # Also map broad HSICS sector (collapse rare 2-digit codes into 5 clean macro sectors for G=21 degrees of freedom)
    def _hsic_macro(h2: str) -> str:
        if h2 in ("28",):
            return "Healthcare"
        if h2 in ("70", "35"):
            return "InfoTech_Telecom"
        if h2 in ("23", "25"):
            return "Consumer"
        if h2 in ("10", "00", "05", "40"):
            return "Industrials_Mat_Energy"
        return "Financials_Prop_Other"

    d["hsic_macro"] = d["hsic2"].apply(_hsic_macro)
    d["actual_final_public_pct"] = pd.to_numeric(d["public_offer_fraction_pct"], errors="coerce")
    d["flip_pct"] = pd.to_numeric(d["First-day flipping ratio (%)"], errors="coerce") * 100.0
    d["log_ir"] = np.log1p(pd.to_numeric(d["initial_return_pct"], errors="coerce") / 100.0)
    sub_x = pd.to_numeric(d["subscription_ratio_times"], errors="coerce").clip(lower=0.0)
    d["log_sub"] = np.log1p(sub_x)
    d["log_proc"] = np.log(pd.to_numeric(d["gross_proceeds_hkd_m"], errors="coerce"))
    d["high_sub_100x"] = (sub_x >= 100.0).astype(int)
    d["post_x_high100"] = d["post_aug2025_prospectus"] * d["high_sub_100x"]
    d["listing_ym"] = pd.to_datetime(d["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    is_18c = d["is_18c"].fillna(0).astype(int)
    p_init = np.where(is_18c == 1, 5.0, 10.0)
    pn18_cf = np.where(
        is_18c == 1,
        np.where(sub_x >= 50.0, 20.0, np.where(sub_x >= 10.0, 10.0, p_init)),
        np.where(sub_x >= 100.0, 50.0, np.where(sub_x >= 50.0, 40.0, np.where(sub_x >= 15.0, 30.0, p_init))),
    )
    d["avoided_clawback_pp"] = np.maximum(0.0, pn18_cf - d["actual_final_public_pct"])

    # Sector dummies (4 dummies, baseline Consumer)
    sec_dummies = pd.get_dummies(d["hsic_macro"], prefix="sec", drop_first=True, dtype=int)
    d = pd.concat([d, sec_dummies], axis=1)
    sec_cols = list(sec_dummies.columns)

    mb_specs = [
        ("PreDetermined_PostAug2025", "post_aug2025_prospectus", ["post_aug2025_prospectus", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]),
        ("DiD_PostAug2025_x_High100x", "post_x_high100", ["post_aug2025_prospectus", "high_sub_100x", "post_x_high100", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]),
        ("DiD_Plus_HSICS_Sector_FE", "post_x_high100", ["post_aug2025_prospectus", "high_sub_100x", "post_x_high100", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"] + sec_cols),
        ("DoseResponse_Avoided_Clawback", "avoided_clawback_pp", ["avoided_clawback_pp", "log_sub", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"]),
        ("DoseResponse_Plus_HSICS_FE", "avoided_clawback_pp", ["avoided_clawback_pp", "log_sub", "log_proc", "is_ah_dual_listed", "is_18a", "is_18c"] + sec_cols),
    ]

    mb_rows = []
    for sp_lbl, tgt, exogs in mb_specs:
        for dep_col, dep_lbl in [
            ("actual_final_public_pct", "Final_Retail_Share_pp"),
            ("flip_pct", "Day1_Flipping_Pct"),
            ("log_ir", "Log_1_plus_Day1_IR"),
        ]:
            if "DoseResponse" in sp_lbl and dep_col == "actual_final_public_pct":
                continue
            sub = d.dropna(subset=[dep_col, "listing_ym"] + exogs).copy()
            X = sm.add_constant(sub[exogs].astype(float))
            fit_cl = sm.OLS(sub[dep_col].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": sub["listing_ym"]})
            p_wcb = wild_cluster_bootstrap_p_vec(sub, dep_col, exogs, tgt, "listing_ym", B=4999, seed=42)
            se_cl = float(fit_cl.bse[tgt])
            mde_80 = 2.8016 * se_cl  # (z_{0.975} + z_{0.80}) * SE
            mb_rows.append({
                "Specification": sp_lbl,
                "Dep_Var": dep_lbl,
                "Target_Var": tgt,
                "Coef": round(float(fit_cl.params[tgt]), 4),
                "SE_Cluster": round(se_cl, 4),
                "t_Cluster": round(float(fit_cl.tvalues[tgt]), 2),
                "p_Cluster": round(float(fit_cl.pvalues[tgt]), 4),
                "p_Webb_WCB": round(p_wcb, 4),
                "MDE_80Pct_Power": round(mde_80, 4),
                "N": len(sub),
                "G_Clusters": int(sub["listing_ym"].nunique()),
                "R2": round(float(fit_cl.rsquared), 3),
            })

    mb_df = pd.DataFrame(mb_rows)
    mb_df.to_csv(EXT_DIR / "ext_table9g_mechanism_b_wcb_power_hsic.csv", index=False)
    print(mb_df.to_string(index=False))

    print("\n" + "=" * 80)
    print("3B. FINI NARROW-WINDOW (2021-2026 & 2022-2026) & RATE-REGIME DiD DIAGNOSTICS")
    print("=" * 80)

    hm = pd.read_csv(EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv", low_memory=False)
    post99 = hm[(hm["board"] == "Main Board") & (hm["cohort_year"] >= 1999) & hm["locked_retail_hkd_bn"].notna()].copy()
    post99["listing_dt"] = pd.to_datetime(post99["listing_date"])
    post99["post_fini"] = (post99["listing_dt"] >= pd.Timestamp("2023-11-22")).astype(int)
    post99["log_locked_bn"] = np.log1p(pd.to_numeric(post99["locked_retail_hkd_bn"], errors="coerce").clip(lower=0))
    post99["delta_1w_bps"] = post99["delta_hibor_1w_freeze_pp"] * 100.0
    post99["spread_1w_3m_bps"] = post99["hibor_1w_3m_spread_peak_pp"] * 100.0
    post99["open_spread_bps"] = (post99["hibor_1w_open"] - post99["hibor_3m_open"]) * 100.0
    post99["hot_100b"] = (post99["locked_retail_hkd_bn"] >= 100.0).astype(int)
    post99["post_x_hot100"] = post99["post_fini"] * post99["hot_100b"]
    post99["high_rate_3m"] = (post99["hibor_3m_open"] >= 3.0).astype(int)
    post99["ym"] = post99["listing_dt"].dt.to_period("M").astype(str)

    fini_specs = [
        ("1. Full 1999-2026: Hot >=HK$100B DiD (No YFE)", post99, "spread_1w_3m_bps ~ hot_100b * post_fini + hibor_3m_open + open_spread_bps"),
        ("2. Full 1999-2026: Hot >=HK$100B DiD (+ Year FE)", post99, "spread_1w_3m_bps ~ hot_100b * post_fini + hibor_3m_open + open_spread_bps + C(cohort_year)"),
        ("3. Narrow Window 2021-2026: Log(Sub) x Post-FINI", post99[post99["cohort_year"] >= 2021], "spread_1w_3m_bps ~ log_locked_bn * post_fini + hibor_3m_open + open_spread_bps"),
        ("4. Narrow Window 2021-2026: Hot >=HK$100B DiD", post99[post99["cohort_year"] >= 2021], "spread_1w_3m_bps ~ hot_100b * post_fini + hibor_3m_open + open_spread_bps"),
        ("5. Narrow Window 2022-2026: Log(Sub) x Post-FINI", post99[post99["cohort_year"] >= 2022], "spread_1w_3m_bps ~ log_locked_bn * post_fini + hibor_3m_open + open_spread_bps"),
        ("6. Narrow Window 2021-2026: High-Rate (>=3%) x Log(Sub)", post99[post99["cohort_year"] >= 2021], "spread_1w_3m_bps ~ log_locked_bn * post_fini + high_rate_3m + hibor_3m_open + open_spread_bps"),
        ("7. Narrow 2021-2026 Delta 1W HIBOR: Log(Sub) x Post-FINI", post99[post99["cohort_year"] >= 2021], "delta_1w_bps ~ log_locked_bn * post_fini + hibor_3m_open"),
        ("8. Narrow 2021-2026 Delta 1W HIBOR: Hot >=HK$100B DiD", post99[post99["cohort_year"] >= 2021], "delta_1w_bps ~ hot_100b * post_fini + hibor_3m_open"),
    ]
    fini_rows = []
    for sp_lbl, sub_f, fml in fini_specs:
        req = ["ym", "hibor_3m_open", "open_spread_bps", "spread_1w_3m_bps", "delta_1w_bps", "log_locked_bn", "post_fini", "hot_100b"]
        sf = sub_f.dropna(subset=req).copy()
        fit = smf.ols(fml, data=sf).fit(cov_type="cluster", cov_kwds={"groups": sf["ym"]})
        for vk in ["post_fini", "log_locked_bn", "log_locked_bn:post_fini", "hot_100b", "hot_100b:post_fini", "hibor_3m_open", "open_spread_bps"]:
            if vk not in fit.params.index:
                continue
            fini_rows.append({
                "Specification": sp_lbl,
                "Variable": vk,
                "Coef_bps": round(float(fit.params[vk]), 2),
                "SE_MonthClust": round(float(fit.bse[vk]), 2),
                "t_MonthClust": round(float(fit.tvalues[vk]), 2),
                "p_MonthClust": round(float(fit.pvalues[vk]), 4),
                "N": int(fit.nobs),
                "Pre_N": int((sf["post_fini"] == 0).sum()),
                "Post_N": int((sf["post_fini"] == 1).sum()),
                "R2": round(float(fit.rsquared), 3),
            })
    fini_df = pd.DataFrame(fini_rows)
    fini_df.to_csv(EXT_DIR / "ext_table11c_fini_narrow_rate_regime.csv", index=False)
    print(fini_df[fini_df["Variable"].isin(["post_fini", "log_locked_bn", "log_locked_bn:post_fini", "hot_100b", "hot_100b:post_fini"])].to_string(index=False))
    return mb_df, fini_df


def main() -> None:
    run_module1_carhart_4f()
    run_module2_matched_firm_lockup()
    run_module3_mechb_and_fini()
    print("\nALL REFEREE REMEDIATION EXTENSIONS COMPUTED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
