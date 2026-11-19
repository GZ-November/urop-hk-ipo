#!/usr/bin/env python3
"""
build_longrun_benchmarks_and_factors.py
=======================================
Upgrades 33-year HKEX post-IPO long-run performance evaluation to top-journal
standards (Lyon, Barber & Tsai 1999; Mitchell & Stafford 2000):

1. Dividend-Adjusted Hang Seng Total Return Index (`HSI-TR`) 1-Year BHAR:
   Replaces price-only HSI with historical Hang Seng Index dividend-reinvested
   total returns (1994-2026 annual dividend yields compounded over each IPO's
   exact [Day-1, Day+365] aftermarket window), quantifying the ~3.5 pp upward
   bias induced by omitting Hong Kong blue-chip dividends.
2. Lyon, Barber & Tsai (1999) Seasoned HKEX Size-Matched Control 1-Year BHAR:
   Uses full 1988-2026 dividend-and-split-adjusted (`hfq`) monthly histories of
   pre-1991 seasoned HKEX stocks plus post-1994 HKEX firms once they pass
   month +37 (>36 months post-IPO, zero overlap with recent IPOs), matching each
   IPO at listing month tau_i to its dynamic market-cap tercile and reporting
   skewness-adjusted t-statistics (Johnson 1978; Sutton 1993), listing-month
   clustered t-statistics, and Wealth Relatives (WR).
3. Strictly Out-of-Sample Seasoned HKEX Monthly Factors (`MKT_TR_rf`, `SMB_seasoned`,
   `MOM_seasoned`) for Calendar-Time Portfolios (CTP) across the full 1994-2026
   sample, replacing the endogenous IPO-internal `hk_smb_proxy_pct` with factors
   built exclusively from seasoned HKEX stocks (>36 months post-IPO), net of
   official HKMA 1-month HIBOR (`rf_monthly_pct`), estimated via Newey-West HAC
   OLS and Mitchell-Stafford sqrt(N_t) WLS.
"""

from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from typing import Any
import urllib.request

import numpy as np
import pandas as pd
from scipy import stats
import statsmodels.api as sm

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERVIEW_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"
SEASONED_CACHE_DIR = OVERVIEW_DIR / "seasoned_monthly_hfq_cache"
SEASONED_CACHE_DIR.mkdir(parents=True, exist_ok=True)

MASTER_CSV = OVERVIEW_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
CTP_RF_CSV = EXT_DIR / "clean_monthly_ctp_with_hibor_rf_1994_2026.csv"

OUT_BHAR_CSV = OVERVIEW_DIR / "table_longrun_bhar_upgraded_5epochs.csv"
OUT_FACTORS_CSV = EXT_DIR / "clean_monthly_ctp_seasoned_factors_1994_2026.csv"
OUT_CTP_ALPHAS_CSV = EXT_DIR / "ext_table10_calendar_time_portfolio_alphas.csv"

AS_OF_STR = "2026-11-12"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Historical Hang Seng Index annual dividend yield (% p.a., Hang Seng Indexes Co. / HKMA Statistical Digest)
HSI_DIV_YIELD_PA: dict[int, float] = {
    1994: 3.40, 1995: 3.65, 1996: 3.10, 1997: 3.55, 1998: 4.15, 1999: 2.75,
    2000: 2.35, 2001: 3.15, 2002: 3.65, 2003: 3.45, 2004: 3.30, 2005: 3.50,
    2006: 2.95, 2007: 2.45, 2008: 4.35, 2009: 3.25, 2010: 3.05, 2011: 3.75,
    2012: 3.55, 2013: 3.45, 2014: 3.65, 2015: 3.70, 2016: 3.65, 2017: 3.15,
    2018: 3.65, 2019: 3.55, 2020: 3.10, 2021: 2.85, 2022: 4.10, 2023: 4.20,
    2024: 4.05, 2025: 3.75, 2026: 3.60,
}


def ym_diff(ym_start: str, ym_end: str) -> int:
    y1, m1 = int(ym_start[:4]), int(ym_start[5:7])
    y2, m2 = int(ym_end[:4]), int(ym_end[5:7])
    return (y2 - y1) * 12 + (m2 - m1)


def ym_add(ym: str, delta: int) -> str:
    y, m = int(ym[:4]), int(ym[5:7])
    tot = y * 12 + (m - 1) + delta
    return f"{tot // 12:04d}-{(tot % 12) + 1:02d}"


def skew_adjusted_t(arr: np.ndarray) -> tuple[float, float]:
    """Lyon, Barber & Tsai (1999) / Johnson (1978) skewness-adjusted t-stat and 2-sided normal approx p-val."""
    x = np.asarray(arr, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 5:
        return np.nan, np.nan
    mu = float(np.mean(x))
    sd = float(np.std(x, ddof=1))
    if sd <= 1e-12:
        return np.nan, np.nan
    s = mu / sd
    gamma = float(stats.skew(x, bias=False))
    t_sa = float(np.sqrt(n) * (s + (gamma / 3.0) * (s**2) + gamma / (6.0 * n)))
    p_sa = float(2.0 * (1.0 - stats.norm.cdf(abs(t_sa))))
    return t_sa, p_sa


def clustered_mean_t(df_sub: pd.DataFrame, col: str, cluster_col: str = "listing_ym") -> tuple[float, float]:
    sub = df_sub[[col, cluster_col]].dropna()
    if len(sub) < 10 or sub[cluster_col].nunique() < 3:
        return np.nan, np.nan
    X = pd.DataFrame({"const": np.ones(len(sub))}, index=sub.index)
    fit = sm.OLS(sub[col].astype(float), X).fit(cov_type="cluster", cov_kwds={"groups": sub[cluster_col]})
    return float(fit.tvalues["const"]), float(fit.pvalues["const"])


def fetch_or_load_monthly_hfq(sym: str) -> dict[str, Any]:
    cfile = SEASONED_CACHE_DIR / f"{sym}.json"
    if cfile.exists():
        try:
            return json.loads(cfile.read_text(encoding="utf-8"))
        except Exception:
            pass
    url = f"https://web.ifzq.gtimg.cn/appstock/app/hkfqkline/get?param={sym},month,1988-01-01,{AS_OF_STR},500,hfq"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        raw = json.loads(urllib.request.urlopen(req, timeout=10).read().decode("utf-8"))
        sub = (raw.get("data") or {}).get(sym) or {}
        rows = sub.get("hfqmonth") or sub.get("month") or []
        qt = (sub.get("qt") or {}).get(sym) or []
        cur_mcap_hkd = None
        if len(qt) > 45 and qt[45] not in (None, "", "0", "0.0"):
            try:
                cur_mcap_hkd = float(qt[45]) * 1e8
            except Exception:
                cur_mcap_hkd = None
        compact_rows = []
        for r in rows:
            d_s = str(r[0])[:10]
            if d_s <= AS_OF_STR:
                try:
                    c_val = float(r[2])
                    if c_val > 0.0001:
                        compact_rows.append([d_s[:7], c_val])
                except Exception:
                    continue
        payload = {"sym": sym, "cur_mcap_hkd": cur_mcap_hkd, "bars": compact_rows}
        cfile.write_text(json.dumps(payload), encoding="utf-8")
        return payload
    except Exception:
        return {"sym": sym, "cur_mcap_hkd": None, "bars": []}


def main() -> None:
    print("=" * 80)
    print("Upgrading 33-Year Long-Run Benchmarks (HSI-TR, Seasoned Size-Matched, Out-of-Sample CTP)")
    print("=" * 80)

    df = pd.read_csv(MASTER_CSV, low_memory=False)
    ctp_rf = pd.read_csv(CTP_RF_CSV)

    clean_mask = (df["flag_recycled_or_transferred_ticker"].fillna(0) == 0) & (~df["flag_reverse_split_distortion"].fillna(False))
    clean_df = df[clean_mask].copy()
    clean_df["listing_ym"] = pd.to_datetime(clean_df["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    # Identify all 5-digit ticker codes that EVER appeared in the 1994-2026 IPO universe
    all_ipo_nums: set[int] = set()
    for sc in df["stock_code"].dropna().astype(str):
        digits = "".join(ch for ch in sc if ch.isdigit())
        if digits:
            all_ipo_nums.add(int(digits))

    # Candidate pre-1994 seasoned HKEX equities: codes 1..600 never used for a 1994-2026 IPO
    pre94_candidates = [f"hk{k:05d}" for k in range(1, 601) if k not in all_ipo_nums]

    # Post-1994 clean IPO tickers (for months strictly >= 37 after their IPO listing month)
    ipo_tasks: list[tuple[str, str, float]] = []
    seen_syms: set[str] = set()
    for _, row in clean_df.iterrows():
        digits = "".join(ch for ch in str(row["stock_code"]) if ch.isdigit())
        if not digits:
            continue
        sym = f"hk{int(digits):05d}"
        if sym in seen_syms:
            continue
        seen_syms.add(sym)
        p_ipo = pd.to_numeric(row.get("offer_price_hkd"), errors="coerce")
        sh_list = pd.to_numeric(row.get("ext_total_shares_listed"), errors="coerce")
        proc = pd.to_numeric(row.get("funds_raised_total_hkd"), errors="coerce")
        if pd.notna(sh_list) and sh_list > 0 and pd.notna(p_ipo) and p_ipo > 0:
            ipo_mcap = float(sh_list * p_ipo)
        elif pd.notna(proc) and proc > 0:
            ipo_mcap = float(proc * 4.0)
        else:
            ipo_mcap = 5e8
        ipo_tasks.append((sym, str(row["listing_date"])[:7], ipo_mcap))

    all_syms_to_fetch = pre94_candidates + [t[0] for t in ipo_tasks]
    print(f"Fetching/loading full monthly hfq histories for {len(pre94_candidates)} pre-1994 candidates + {len(ipo_tasks)} clean post-1994 equities...")
    with ThreadPoolExecutor(max_workers=24) as ex:
        fetched_list = list(ex.map(fetch_or_load_monthly_hfq, all_syms_to_fetch))
    fetched_map = {item["sym"]: item for item in fetched_list}

    # Build strictly seasoned (>36 months post-IPO) monthly panel across 1993-2026
    seasoned_rows: list[dict[str, Any]] = []
    n_pre91_used = 0

    def append_seasoned_series(sym: str, anchor_list_ym: str, fallback_ipo_mcap: float) -> bool:
        item = fetched_map.get(sym)
        if not item or len(item.get("bars", [])) < 15:
            return False
        m_closes: dict[str, float] = {}
        for b in item["bars"]:
            m_closes[str(b[0])] = float(b[1])
        yms = sorted(m_closes.keys())
        first_ym = yms[0]
        # Guard against ticker recycling: first bar must not predate anchor_list_ym by >2 months for post-1994 IPOs
        if anchor_list_ym >= "1994-01" and ym_diff(anchor_list_ym, first_ym) < -2:
            return False
        # For pre-1994 candidates, require listing on or before 1990-12 so they are >36M seasoned by 1994-01
        if anchor_list_ym < "1994-01" and first_ym > "1990-12":
            return False

        cur_mcap = item.get("cur_mcap_hkd")
        last_close = m_closes[yms[-1]]
        first_close = m_closes[first_ym]

        added_any = False
        for i in range(len(yms) - 1):
            prev_ym, curr_ym = yms[i], yms[i + 1]
            if curr_ym < "1993-12" or curr_ym > "2026-10":
                continue
            if ym_diff(prev_ym, curr_ym) != 1:
                continue
            eff_list_ym = first_ym if anchor_list_ym < "1994-01" else anchor_list_ym
            offset = ym_diff(eff_list_ym, curr_ym)
            if offset < 37:
                continue  # STRICTLY >36 months post-IPO!

            p_prev = m_closes[prev_ym]
            p_curr = m_closes[curr_ym]
            if p_prev <= 0:
                continue
            ret = (p_curr - p_prev) / p_prev

            if cur_mcap and cur_mcap > 0 and last_close > 0:
                dyn_mcap = float(cur_mcap) * (p_prev / last_close)
            else:
                dyn_mcap = float(fallback_ipo_mcap) * (p_prev / max(first_close, 1e-4))

            ym_t12 = ym_add(curr_ym, -12)
            ym_t2 = ym_add(curr_ym, -2)
            mom_11m = ((m_closes[ym_t2] / m_closes[ym_t12]) - 1.0) if (ym_t12 in m_closes and ym_t2 in m_closes and m_closes[ym_t12] > 0) else np.nan

            ym_fwd12 = ym_add(prev_ym, 12)
            bhr_fwd12 = ((m_closes[ym_fwd12] / p_prev) - 1.0) if (ym_fwd12 in m_closes and p_prev > 0) else np.nan

            seasoned_rows.append({
                "sym": sym,
                "year_month": curr_ym,
                "prev_ym": prev_ym,
                "offset": offset,
                "ret": ret,
                "dyn_mcap": dyn_mcap,
                "mom_11m": mom_11m,
                "bhr_fwd12": bhr_fwd12,
            })
            added_any = True
        return added_any

    for sym in pre94_candidates:
        if append_seasoned_series(sym, "1990-01", 2e9):
            n_pre91_used += 1

    n_post94_used = 0
    for sym, l_ym, ipo_mcap in ipo_tasks:
        if append_seasoned_series(sym, l_ym, ipo_mcap):
            n_post94_used += 1

    seasoned_df = pd.DataFrame(seasoned_rows)
    # Winsorize monthly returns and forward-12M returns at 1/99% across the seasoned universe
    q01, q99 = seasoned_df["ret"].quantile([0.01, 0.99])
    seasoned_df["clean_ret"] = seasoned_df["ret"].clip(lower=q01, upper=q99)
    fq01, fq99 = seasoned_df["bhr_fwd12"].dropna().quantile([0.01, 0.99])
    seasoned_df["clean_bhr_fwd12"] = seasoned_df["bhr_fwd12"].clip(lower=fq01, upper=fq99)

    print(
        f"Seasoned universe built: {n_pre91_used} pre-1991 HKEX equities + {n_post94_used} matured post-1994 equities "
        f"= {len(seasoned_df):,} strictly seasoned (>36M post-IPO) stock-months!"
    )

    # 2. Construct Out-of-Sample Monthly Factors (MKT_TR_rf, SMB_seasoned, MOM_seasoned) across all 393 months
    factor_rows: list[dict[str, Any]] = []
    seasoned_by_ym = {ym: g for ym, g in seasoned_df.groupby("year_month")}

    for _, rf_row in ctp_rf.iterrows():
        ym = str(rf_row["year_month"])
        yr = int(ym[:4])
        div_mo_pct = HSI_DIV_YIELD_PA.get(yr, 3.50) / 12.0
        hsi_px_pct = float(rf_row["hsi_monthly_return_pct"]) if pd.notna(rf_row["hsi_monthly_return_pct"]) else np.nan
        rf_mo_pct = float(rf_row["rf_monthly_pct"]) if pd.notna(rf_row["rf_monthly_pct"]) else 0.0
        hsi_tr_pct = hsi_px_pct + div_mo_pct if pd.notna(hsi_px_pct) else np.nan
        mkt_tr_rf = hsi_tr_pct - rf_mo_pct if pd.notna(hsi_tr_pct) else np.nan

        g_seas = seasoned_by_ym.get(ym)
        n_seas = len(g_seas) if g_seas is not None else 0
        smb_seas = np.nan
        mom_seas = np.nan
        mkt_ew_seas = np.nan

        if g_seas is not None and n_seas >= 15:
            mkt_ew_seas = float(g_seas["clean_ret"].mean() * 100.0)
            med_cap = g_seas["dyn_mcap"].median()
            s_ret = g_seas[g_seas["dyn_mcap"] <= med_cap]["clean_ret"].mean() * 100.0
            b_ret = g_seas[g_seas["dyn_mcap"] > med_cap]["clean_ret"].mean() * 100.0
            smb_seas = float(s_ret - b_ret)

            g_mom = g_seas.dropna(subset=["mom_11m"])
            if len(g_mom) >= 15:
                q_lo, q_hi = g_mom["mom_11m"].quantile([1.0 / 3.0, 2.0 / 3.0])
                win_ret = g_mom[g_mom["mom_11m"] >= q_hi]["clean_ret"].mean() * 100.0
                los_ret = g_mom[g_mom["mom_11m"] <= q_lo]["clean_ret"].mean() * 100.0
                mom_seas = float(win_ret - los_ret)

        rec = rf_row.to_dict()
        rec["hsi_div_monthly_pct"] = round(div_mo_pct, 4)
        rec["hsi_tr_monthly_pct"] = round(hsi_tr_pct, 4) if pd.notna(hsi_tr_pct) else np.nan
        rec["mkt_tr_excess_pct"] = round(mkt_tr_rf, 4) if pd.notna(mkt_tr_rf) else np.nan
        rec["n_seasoned_hkex"] = n_seas
        rec["seasoned_ew_ret_pct"] = round(mkt_ew_seas, 4) if pd.notna(mkt_ew_seas) else np.nan
        rec["smb_seasoned_pct"] = round(smb_seas, 4) if pd.notna(smb_seas) else np.nan
        rec["mom_seasoned_pct"] = round(mom_seas, 4) if pd.notna(mom_seas) else np.nan
        factor_rows.append(rec)

    fac_df = pd.DataFrame(factor_rows)
    fac_df.to_csv(OUT_FACTORS_CSV, index=False)
    print(f"Saved out-of-sample seasoned factor panel ({len(fac_df)} months; min n_seasoned={fac_df['n_seasoned_hkex'].min()}, max={fac_df['n_seasoned_hkex'].max()}) to: {OUT_FACTORS_CSV}")

    # 3. Estimate Upgraded Calendar-Time Portfolio Alphas (OLS Newey-West HAC & WLS sqrt(N_t))
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
    ctp_alpha_rows: list[dict[str, Any]] = []
    for p_col, n_col, p_name in portfolios:
        s1 = fac_df.dropna(subset=[p_col, "mkt_tr_excess_pct", "rf_monthly_pct"]).copy()
        y1 = s1[p_col].astype(float) - s1["rf_monthly_pct"].astype(float)
        X1 = sm.add_constant(s1[["mkt_tr_excess_pct"]].astype(float))
        m1_ols = sm.OLS(y1, X1).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        w1 = np.sqrt(s1[n_col].astype(float).clip(lower=1.0))
        m1_wls = sm.WLS(y1, X1, weights=w1).fit(cov_type="HC3")

        s3 = fac_df.dropna(subset=[p_col, "mkt_tr_excess_pct", "smb_seasoned_pct", "mom_seasoned_pct", "rf_monthly_pct"]).copy()
        y3 = s3[p_col].astype(float) - s3["rf_monthly_pct"].astype(float)
        X3 = sm.add_constant(s3[["mkt_tr_excess_pct", "smb_seasoned_pct", "mom_seasoned_pct"]].astype(float))
        m3_ols = sm.OLS(y3, X3).fit(cov_type="HAC", cov_kwds={"maxlags": 6})
        w3 = np.sqrt(s3[n_col].astype(float).clip(lower=1.0))
        m3_wls = sm.WLS(y3, X3, weights=w3).fit(cov_type="HC3")

        ctp_alpha_rows.append({
            "Portfolio": p_name,
            "Months_CAPM_TR": len(s1),
            "Mean_Excess_Ret_Mo_Pct": round(float(y1.mean()), 3),
            "CAPM_TR_Alpha_OLS_Mo": round(float(m1_ols.params["const"]), 3),
            "CAPM_TR_t_HAC": round(float(m1_ols.tvalues["const"]), 2),
            "CAPM_TR_Alpha_WLS_Mo": round(float(m1_wls.params["const"]), 3),
            "CAPM_TR_t_WLS": round(float(m1_wls.tvalues["const"]), 2),
            "Months_Seasoned_3F": len(s3),
            "Seasoned3F_Alpha_OLS_Mo": round(float(m3_ols.params["const"]), 3),
            "Seasoned3F_t_HAC": round(float(m3_ols.tvalues["const"]), 2),
            "Seasoned3F_Alpha_Ann_Pct": round(float(m3_ols.params["const"] * 12.0), 2),
            "Seasoned3F_Alpha_WLS_Mo": round(float(m3_wls.params["const"]), 3),
            "Seasoned3F_t_WLS": round(float(m3_wls.tvalues["const"]), 2),
            "Beta_MKT_TR": round(float(m3_ols.params["mkt_tr_excess_pct"]), 3),
            "Beta_SMB_Seasoned": round(float(m3_ols.params["smb_seasoned_pct"]), 3),
            "Beta_MOM_Seasoned": round(float(m3_ols.params["mom_seasoned_pct"]), 3),
            "R2_3F": round(float(m3_ols.rsquared), 3),
        })

    ctp_res_df = pd.DataFrame(ctp_alpha_rows)
    ctp_res_df.to_csv(OUT_CTP_ALPHAS_CSV, index=False)
    print(f"\nSaved out-of-sample CTP Alpha table to: {OUT_CTP_ALPHAS_CSV}")
    print(ctp_res_df.to_string(index=False))

    # 4. Upgrade 1-Year Aftermarket BHAR (HSI-TR & Seasoned Size-Matched Control)
    seas_fwd = seasoned_df.dropna(subset=["clean_bhr_fwd12"]).copy()
    seas_ctrl_lookup: dict[tuple[str, int], float] = {}
    seas_all_lookup: dict[str, float] = {}
    seas_q_bounds: dict[str, tuple[float, float]] = {}
    for pym, g in seas_fwd.groupby("prev_ym"):
        if len(g) >= 5:
            seas_all_lookup[pym] = float(g["clean_bhr_fwd12"].mean() * 100.0)
        if len(g) >= 9:
            q1, q2 = g["dyn_mcap"].quantile([1.0 / 3.0, 2.0 / 3.0])
            seas_q_bounds[pym] = (float(q1), float(q2))
            seas_ctrl_lookup[(pym, 1)] = float(g[g["dyn_mcap"] <= q1]["clean_bhr_fwd12"].mean() * 100.0)
            seas_ctrl_lookup[(pym, 2)] = float(g[(g["dyn_mcap"] > q1) & (g["dyn_mcap"] <= q2)]["clean_bhr_fwd12"].mean() * 100.0)
            seas_ctrl_lookup[(pym, 3)] = float(g[g["dyn_mcap"] > q2]["clean_bhr_fwd12"].mean() * 100.0)

    df = df.copy()
    sh_all = pd.to_numeric(df["ext_total_shares_listed"], errors="coerce")
    p_all = pd.to_numeric(df["offer_price_hkd"], errors="coerce")
    pr_all = pd.to_numeric(df["funds_raised_total_hkd"], errors="coerce")
    ipo_mcap_arr = np.where(sh_all.notna() & (sh_all > 0) & p_all.notna(), sh_all * p_all, pr_all * 4.0)

    raw_bhr_1y = pd.to_numeric(df["after_bhr_1y_pct"], errors="coerce")
    hsi_px_1y_pct = pd.to_numeric(df["hsi_ret_1y"], errors="coerce") * 100.0
    div_1y_pct = pd.Series([HSI_DIV_YIELD_PA.get(int(y), 3.50) if pd.notna(y) else 3.50 for y in df["cohort_year"]], index=df.index)
    hsi_tr_1y_pct = ((1.0 + hsi_px_1y_pct / 100.0) * (1.0 + div_1y_pct / 100.0) - 1.0) * 100.0

    bhar_hsi_tr = raw_bhr_1y - hsi_tr_1y_pct

    lym_series = pd.to_datetime(df["listing_date"], errors="coerce").dt.to_period("M").astype(str)
    ctrl_1y_pct = []
    for lym, mcap_i, htr in zip(lym_series, ipo_mcap_arr, hsi_tr_1y_pct):
        bounds = seas_q_bounds.get(lym)
        if bounds is not None and pd.notna(mcap_i):
            terc = 1 if mcap_i <= bounds[0] else (2 if mcap_i <= bounds[1] else 3)
            val = seas_ctrl_lookup.get((lym, terc), seas_all_lookup.get(lym, np.nan))
        else:
            val = seas_all_lookup.get(lym, np.nan)
        if pd.isna(val):
            val = htr
        ctrl_1y_pct.append(val)
    ctrl_1y_s = pd.Series(ctrl_1y_pct, index=df.index, dtype=float)
    bhar_size_matched = raw_bhr_1y - ctrl_1y_s

    df = pd.concat(
        [
            df.drop(columns=[c for c in ["after_bhar_1y_hsi_tr_pct", "after_bhar_1y_size_matched_pct"] if c in df.columns]),
            pd.DataFrame(
                {
                    "after_bhar_1y_hsi_tr_pct": bhar_hsi_tr,
                    "after_bhar_1y_size_matched_pct": bhar_size_matched,
                },
                index=df.index,
            ),
        ],
        axis=1,
    )
    df.to_csv(MASTER_CSV, index=False)
    print(f"\nUpdated {MASTER_CSV} with `after_bhar_1y_hsi_tr_pct` and `after_bhar_1y_size_matched_pct`.")

    # 5. Tabulate 5-Epoch Upgraded 1Y BHAR Summary for Main Board & GEM
    clean_upd = df[clean_mask].copy()
    clean_upd["listing_ym"] = pd.to_datetime(clean_upd["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    bhar_rows: list[dict[str, Any]] = []
    epoch_order = [
        "Epoch I (1994-1999)",
        "Epoch II (2000-2007)",
        "Epoch III (2008-2017)",
        "Epoch IV (2018-2022)",
        "Epoch V (2023-2026Q3)",
    ]

    for brd in ["Main Board", "GEM"]:
        sub_b = clean_upd[(clean_upd["board"] == brd) & clean_upd["after_bhr_1y_pct"].notna()].copy()
        for col in ["after_bhr_1y_pct", "after_bhar_1y_pct", "after_bhar_1y_hsi_tr_pct", "after_bhar_1y_size_matched_pct"]:
            lo, hi = sub_b[col].quantile([0.01, 0.99])
            sub_b[col + "_w"] = sub_b[col].clip(lower=lo, upper=hi)

        slices = [(ep, sub_b[sub_b["epoch_5"] == ep]) for ep in epoch_order if (sub_b["epoch_5"] == ep).sum() > 0]
        slices.append((f"All {brd} Matured 1Y (1994-2026Q3)", sub_b))

        for label, g in slices:
            n = len(g)
            raw_m = float(g["after_bhr_1y_pct_w"].mean())
            raw_med = float(g["after_bhr_1y_pct"].median())
            pos_pct = float((g["after_bhr_1y_pct"] > 0).mean() * 100.0)

            px_m = float(g["after_bhar_1y_pct_w"].mean())
            tr_m = float(g["after_bhar_1y_hsi_tr_pct_w"].mean())
            tr_med = float(g["after_bhar_1y_hsi_tr_pct"].median())
            t_sa_tr, _ = skew_adjusted_t(g["after_bhar_1y_hsi_tr_pct_w"].values)
            t_cl_tr, _ = clustered_mean_t(g, "after_bhar_1y_hsi_tr_pct_w")

            sm_m = float(g["after_bhar_1y_size_matched_pct_w"].mean())
            sm_med = float(g["after_bhar_1y_size_matched_pct"].median())
            t_sa_sm, _ = skew_adjusted_t(g["after_bhar_1y_size_matched_pct_w"].values)
            t_cl_sm, _ = clustered_mean_t(g, "after_bhar_1y_size_matched_pct_w")

            bench_tr_m = raw_m - tr_m
            bench_sm_m = raw_m - sm_m
            wr_tr = (1.0 + raw_m / 100.0) / max(1.0 + bench_tr_m / 100.0, 0.05)
            wr_sm = (1.0 + raw_m / 100.0) / max(1.0 + bench_sm_m / 100.0, 0.05)

            bhar_rows.append({
                "Board": brd,
                "Epoch": label,
                "N_Matured_1Y": n,
                "Raw_1Y_Mean_Pct": round(raw_m, 2),
                "Raw_1Y_Med_Pct": round(raw_med, 2),
                "Pct_Positive_Raw": round(pos_pct, 1),
                "Legacy_BHAR_HSI_Price_Mean": round(px_m, 2),
                "BHAR_HSI_TR_Mean": round(tr_m, 2),
                "BHAR_HSI_TR_Med": round(tr_med, 2),
                "t_SkewAdj_HSI_TR": round(t_sa_tr, 2) if pd.notna(t_sa_tr) else np.nan,
                "t_MonthClust_HSI_TR": round(t_cl_tr, 2) if pd.notna(t_cl_tr) else np.nan,
                "WR_HSI_TR": round(wr_tr, 3),
                "BHAR_SizeMatched_Mean": round(sm_m, 2),
                "BHAR_SizeMatched_Med": round(sm_med, 2),
                "t_SkewAdj_SizeMatched": round(t_sa_sm, 2) if pd.notna(t_sa_sm) else np.nan,
                "t_MonthClust_SizeMatched": round(t_cl_sm, 2) if pd.notna(t_cl_sm) else np.nan,
                "WR_SizeMatched": round(wr_sm, 3),
            })

    bhar_df = pd.DataFrame(bhar_rows)
    bhar_df.to_csv(OUT_BHAR_CSV, index=False)
    print(f"\nSaved upgraded 5-Epoch Long-Run BHAR table to: {OUT_BHAR_CSV}")
    print(bhar_df.to_string(index=False))


if __name__ == "__main__":
    main()
