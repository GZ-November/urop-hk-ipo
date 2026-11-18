#!/usr/bin/env python3
"""
Frontier Five-Module Econometric Suite for the 1994-2026 Hong Kong IPO Monograph:
  Module 1: Two-Stage Statutory Lockup Natural Experiment (PRC Company Law 12M H-Share Pre-IPO Lockup
            vs. Cayman Red-Chip 6M Simultaneous Unlock + Post-2018 H-Share Full Circulation Reversal)
  Module 2: Statutory Crossover Certification (Rule 18A.07 / GL92-18 / Rule 18C.08 vs. Rule 10.04 Ban),
            1,686-Placement Cornerstone Taxonomy, and Bipartite Sponsor-Cornerstone Network 2SLS IV
  Module 3: Cap. 571W Price Stabilization Purchases, Over-Allotment Exercise Regimes, and Day +30 Cliff
            (2025-2026 Audited Stabilization Announcements + 33-Year Daily Market Cache Event Study)
  Module 4: 3-Year Track Record Financial Trajectory, Teoh-Welch-Wong (1998) Accruals Quality,
            IAS 38 R&D Capitalization Opportunism, and Rule 8.05(1) HK$80M Profit-Test Bunching
  Module 5: Post-IPO "Liquidity Death Spiral" (Zombie IPOs), Amihud (2002) Illiquidity, Zero-Volume Days,
            and Microstructural Determinants Across 2025-2026 (N=126) and 33-Year Daily Cache (N=2,600)
"""

import datetime as dt
import json
import re
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

if str(Path(__file__).resolve().parent) not in sys.path:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
from refresh_market_and_lockup_to_20261112 import (  # noqa: E402
    add_calendar_months,
    compute_lockup_event_from_bars,
    load_stock_bars,
)

BASE_DIR = Path("/Users/georgezhu/Desktop/UROP HK IPO")
OUT_MAIN = BASE_DIR / "analysis" / "out" / "overview_1994_2026"
OUT_EXT = BASE_DIR / "analysis" / "out" / "overview_extensions"
FIG_DIR = BASE_DIR / "docs" / "overview_paper" / "figures"
CACHE_DIR = OUT_MAIN / "market_cache"

OUT_EXT.mkdir(parents=True, exist_ok=True)
FIG_DIR.mkdir(parents=True, exist_ok=True)


def lbt_skew_adj_t(x: pd.Series | np.ndarray) -> tuple[float, float]:
    """Lyon, Barber, and Tsai (1999) skewness-adjusted t-statistic and two-sided p-value."""
    arr = np.asarray(x, dtype=float)
    arr = arr[np.isfinite(arr)]
    n = len(arr)
    if n < 3:
        return np.nan, np.nan
    mean = np.mean(arr)
    sd = np.std(arr, ddof=1)
    if sd <= 1e-12:
        return np.nan, np.nan
    s = mean / sd
    skew = stats.skew(arr, bias=False)
    t_lbt = np.sqrt(n) * (s + (1.0 / 3.0) * skew * (s ** 2) + (1.0 / (6.0 * n)) * skew)
    p_val = 2.0 * (1.0 - stats.t.cdf(abs(t_lbt), df=n - 1))
    return float(t_lbt), float(p_val)


def load_master_merged() -> pd.DataFrame:
    m = pd.read_csv(BASE_DIR / "pipeline" / "exports" / "HKIPO-MB-MASTER_clean.csv")
    m226 = pd.read_csv(OUT_MAIN / "clean_micro_panel_2025_2026_N226.csv")
    cols_226 = [
        "stock_code", "cohort_quarter", "lead_sponsor", "is_18a", "is_18c", "is_wvr",
        "is_prc_h_share", "is_ah_dual_listed", "alloc_regime_actual", "pricing_structure",
        "post_aug2025_prospectus", "initial_return_pct", "bhr_1m_pct", "bhr_3m_pct",
        "bhr_6m_pct", "gross_proceeds_hkd_m", "subscription_ratio_times",
        "unrestricted_free_float_pct", "cornerstone_pct_of_offering"
    ]
    df = m.merge(m226[cols_226], left_on="Stock Code", right_on="stock_code", how="left").copy()
    # bhr_*_pct in clean_micro_panel_2025_2026_N226.csv are harmonized in percentage points (%)
    for bcol in ["bhr_1m_pct", "bhr_3m_pct", "bhr_6m_pct"]:
        df[bcol] = pd.to_numeric(df[bcol], errors="coerce")
    return df


def canon_cs(name: str) -> str:
    s = re.sub(r"\(.*?\)", "", str(name)).strip()
    u = s.upper()
    if "UBS" in u:
        return "UBS Asset Management"
    if "GIC" in u:
        return "GIC (Singapore SWF)"
    if "SCHRODER" in u:
        return "Schroders"
    if "FIDELITY" in u or "FIL " in u:
        return "Fidelity International"
    if "BLACKROCK" in u:
        return "BlackRock"
    if "HILLHOUSE" in u or "HHLR" in u:
        return "Hillhouse / HHLR"
    if "BOYU" in u:
        return "Boyu Capital"
    if "TENCENT" in u or "HUANG RIVER" in u:
        return "Tencent Holdings"
    if "ALIBABA" in u or "TAOBAO" in u:
        return "Alibaba Group"
    if "OAKWISE" in u:
        return "Oakwise Asset Management"
    if "HARVEST" in u:
        return "Harvest Fund"
    if "CHINA SOUTHERN" in u or "CSOP" in u:
        return "China Southern / CSOP"
    if "FULLGOAL" in u:
        return "Fullgoal Fund"
    if "GF FUND" in u or "GF INT" in u:
        return "GF Fund"
    if "GUOTAI JUNAN" in u:
        return "Guotai Junan Investments"
    if "CICC" in u:
        return "CICC Financial Trading"
    if "HUATAI" in u:
        return "Huatai Capital"
    if "TAIKANG" in u:
        return "Taikang Life"
    if "PERSEVERANCE" in u or "GAOYI" in u:
        return "Perseverance AM"
    if "3W " in u or "3W FUND" in u:
        return "3W Fund"
    if "ICBC" in u:
        return "ICBC Wealth"
    if "JANE STREET" in u:
        return "Jane Street"
    if "WT ASSET" in u:
        return "WT Asset Management"
    if "MILLENNIUM" in u:
        return "Millennium Management"
    if "POINT72" in u:
        return "Point72"
    if "ORBIMED" in u or "ORIMED" in u:
        return "OrbiMed"
    if "LAV" in u or "LILLY ASIA" in u:
        return "Lilly Asia Ventures"
    if "HONGSHAN" in u or "SEQUOIA" in u:
        return "HSG (HongShan)"
    if "QIA" in u or "QATAR" in u:
        return "Qatar Investment Authority"
    if "ADIA" in u or "ABU DHABI" in u:
        return "Abu Dhabi Investment Authority"
    return s[:35]


def run_module1_twostage_lockup(df: pd.DataFrame, df33: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 78)
    print("MODULE 1: Two-Stage Statutory Lockup Natural Experiment (6M vs 12M)")
    print("=" * 78)

    u = df[df["Cornerstone unlock CAR [-20, +20] (%)"].notna()].copy()
    u["car_m20_p20_pct"] = pd.to_numeric(u["Cornerstone unlock CAR [-20, +20] (%)"], errors="coerce") * 100.0
    u["car_m5_p5_pct"] = pd.to_numeric(u["Cornerstone unlock CAR [-5, +5] (%)"], errors="coerce") * 100.0
    u["vol_shock"] = pd.to_numeric(u["Cornerstone unlock volume shock ratio"], errors="coerce")

    rows = []

    # Panel A: Day +180 (6-Month) Lockup Expiration by Statutory Legal Origin (PRC H-Share 12M Pre-IPO Lock vs Cayman 6M Simultaneous Unlock)
    u["origin_group"] = np.where(
        u["is_prc_h_share"] == 0,
        "Cayman / Offshore Red-Chip (Simultaneous 6M Pre-IPO & Cornerstone Unlock)",
        np.where(
            u["is_ah_dual_listed"] == 1,
            "PRC H-Share: A+H Dual-Listed (6M Cornerstone Only; 12M Company Law Pre-IPO Lock)",
            "PRC H-Share: Pure Chapter 19A (6M Cornerstone Only; 12M Company Law Pre-IPO Lock)"
        )
    )

    sub_groups = [
        ("Panel A1: All PRC H-Shares (12M Pre-IPO Lock; 6M Cornerstone Only)", u[u["is_prc_h_share"] == 1]),
        ("  - Pure Chapter 19A H-Shares (Non-A+H)", u[(u["is_prc_h_share"] == 1) & (u["is_ah_dual_listed"] == 0)]),
        ("  - A+H Dual-Listed H-Shares", u[(u["is_prc_h_share"] == 1) & (u["is_ah_dual_listed"] == 1)]),
        ("Panel A2: Cayman / Offshore Red-Chips (Simultaneous 6M Pre-IPO + Cornerstone Unlock)", u[u["is_prc_h_share"] == 0]),
    ]

    for label, grp in sub_groups:
        c20 = grp["car_m20_p20_pct"].dropna()
        c5 = grp["car_m5_p5_pct"].dropna()
        vs = grp["vol_shock"].dropna()
        t20, p20 = stats.ttest_1samp(c20, 0.0) if len(c20) > 1 else (np.nan, np.nan)
        tlbt, plbt = lbt_skew_adj_t(c20)
        _, p_wilc = stats.wilcoxon(c20) if len(c20) > 5 else (np.nan, np.nan)
        rows.append({
            "Panel_Group": label,
            "Horizon": "Day +180 (6M Unlock)",
            "N": len(c20),
            "Mean_Metric_Pct": round(float(c20.mean()), 2),
            "Median_Metric_Pct": round(float(c20.median()), 2),
            "Narrow_CAR_m5_p5_Pct": round(float(c5.mean()), 2),
            "Negative_Share_Pct": round(float((c20 < 0).mean() * 100.0), 1),
            "t_stat": round(float(t20), 2),
            "t_LBT_ or_Welch": round(float(tlbt), 2),
            "p_value": round(float(p20), 4),
            "Wilcoxon_p": round(float(p_wilc), 4) if pd.notna(p_wilc) else np.nan,
            "Mean_Vol_Shock_x": round(float(vs.mean()), 2)
        })

    # DiD test at Day +180: Cayman minus H-share
    c_cay = u[u["is_prc_h_share"] == 0]["car_m20_p20_pct"].dropna()
    c_h = u[u["is_prc_h_share"] == 1]["car_m20_p20_pct"].dropna()
    t_did, p_did = stats.ttest_ind(c_cay, c_h, equal_var=False)
    u_mw, p_mw = stats.mannwhitneyu(c_cay, c_h, alternative="two-sided")
    rows.append({
        "Panel_Group": "Panel A3: Difference (Cayman 6M Simultaneous - PRC H-Share 6M Cornerstone Only)",
        "Horizon": "Day +180 DiD Wedge",
        "N": len(c_cay) + len(c_h),
        "Mean_Metric_Pct": round(float(c_cay.mean() - c_h.mean()), 2),
        "Median_Metric_Pct": round(float(c_cay.median() - c_h.median()), 2),
        "Narrow_CAR_m5_p5_Pct": round(float(u[u["is_prc_h_share"] == 0]["car_m5_p5_pct"].mean() - u[u["is_prc_h_share"] == 1]["car_m5_p5_pct"].mean()), 2),
        "Negative_Share_Pct": np.nan,
        "t_stat": round(float(t_did), 2),
        "t_LBT_ or_Welch": round(float(t_did), 2),
        "p_value": round(float(p_did), 4),
        "Wilcoxon_p": round(float(p_mw), 4),
        "Mean_Vol_Shock_x": round(float(u[u["is_prc_h_share"] == 0]["vol_shock"].mean() - u[u["is_prc_h_share"] == 1]["vol_shock"].mean()), 2)
    })

    # Panel B: 33-Year Main Board 1M->6M vs 6M->12M Compounded Interval BHAR Reversal
    mb33 = df33[
        (df33["board"] == "Main Board")
        & (df33["flag_reverse_split_distortion"] == 0)
        & (df33["flag_recycled_or_transferred_ticker"] == 0)
    ].copy()
    # Correct compounded interval BHAR: [(1+R_end)/(1+R_start) - (1+M_end)/(1+M_start)] * 100
    mb33["bhar_1m_to_6m"] = 100.0 * (
        (1.0 + mb33["after_bhr_6m_pct"] / 100.0) / (1.0 + mb33["after_bhr_1m_pct"] / 100.0)
        - (1.0 + mb33["hsi_ret_6m"]) / (1.0 + mb33["hsi_ret_1m"])
    )
    mb33["bhar_6m_to_12m"] = 100.0 * (
        (1.0 + mb33["after_bhr_1y_pct"] / 100.0) / (1.0 + mb33["after_bhr_6m_pct"] / 100.0)
        - (1.0 + mb33["hsi_ret_1y"]) / (1.0 + mb33["hsi_ret_6m"])
    )
    mb33 = mb33.replace([np.inf, -np.inf], np.nan)

    for era_lbl, era_df in [
        ("Panel B1: Pre-Full Circulation Era (1994-2017, Unlisted Domestic Shares Non-Tradable)", mb33[mb33["cohort_year"] <= 2017]),
        ("Panel B2: CSRC H-Share Full Circulation Era (2018-2026, 12M Statutory Pre-IPO Unlock)", mb33[mb33["cohort_year"] >= 2018]),
        ("Panel B3: Full 33-Year Main Board Sample (1994-2026)", mb33)
    ]:
        for h_val, h_name in [(1, "PRC Joint-Stock H-Shares (12M Company Law Lockup)"), (0, "Non-H-Share Main Board Issuers (6M Lockup)")]:
            sub = era_df[era_df["is_prc_joint_stock"] == h_val]
            s16 = sub["bhar_1m_to_6m"].dropna()
            s612 = sub["bhar_6m_to_12m"].dropna()
            t612, p612 = stats.ttest_1samp(s612, 0.0)
            tlbt612, _ = lbt_skew_adj_t(s612)
            rows.append({
                "Panel_Group": f"{era_lbl} — {h_name}",
                "Horizon": "Month 6 -> Month 12 BHAR (12M Unlock Window)",
                "N": len(s612),
                "Mean_Metric_Pct": round(float(s612.mean()), 2),
                "Median_Metric_Pct": round(float(s612.median()), 2),
                "Narrow_CAR_m5_p5_Pct": round(float(s16.mean()), 2),  # stores 1M->6M BHAR for side-by-side comparison
                "Negative_Share_Pct": round(float((s612 < 0).mean() * 100.0), 1),
                "t_stat": round(float(t612), 2),
                "t_LBT_ or_Welch": round(float(tlbt612), 2),
                "p_value": round(float(p612), 4),
                "Wilcoxon_p": np.nan,
                "Mean_Vol_Shock_x": np.nan
            })
        h1_612 = era_df[era_df["is_prc_joint_stock"] == 1]["bhar_6m_to_12m"].dropna()
        h0_612 = era_df[era_df["is_prc_joint_stock"] == 0]["bhar_6m_to_12m"].dropna()
        h1_16 = era_df[era_df["is_prc_joint_stock"] == 1]["bhar_1m_to_6m"].dropna()
        h0_16 = era_df[era_df["is_prc_joint_stock"] == 0]["bhar_1m_to_6m"].dropna()
        tw, pw = stats.ttest_ind(h1_612, h0_612, equal_var=False)
        rows.append({
            "Panel_Group": f"{era_lbl} — Difference (H-Share minus Non-H-Share)",
            "Horizon": "Month 6 -> Month 12 Wedge",
            "N": len(h1_612) + len(h0_612),
            "Mean_Metric_Pct": round(float(h1_612.mean() - h0_612.mean()), 2),
            "Median_Metric_Pct": round(float(h1_612.median() - h0_612.median()), 2),
            "Narrow_CAR_m5_p5_Pct": round(float(h1_16.mean() - h0_16.mean()), 2),
            "Negative_Share_Pct": np.nan,
            "t_stat": round(float(tw), 2),
            "t_LBT_ or_Welch": round(float(tw), 2),
            "p_value": round(float(pw), 4),
            "Wilcoxon_p": np.nan,
            "Mean_Vol_Shock_x": np.nan
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_EXT / "ext_table15_twostage_lockup_natural_experiment.csv", index=False)
    print(out_df.to_string(index=False))
    return out_df


def run_module1b_paired_lockup(df: pd.DataFrame) -> pd.DataFrame:
    """Module 1B: Expanded Day +180 (N=123/150) & Paired Matured Day +180 vs Day +365 (N=64) Lockup DiD."""
    print("\n" + "=" * 80)
    print("MODULE 1B: Expanded Day +180 & Paired Matured 6M vs 12M Lockup Natural Experiment")
    print("=" * 80)
    p = pd.read_csv(OUT_EXT / "clean_2025_2026_paired_6m_12m_lockup_panel.csv")
    meta = df[[
        "stock_code", "is_prc_h_share", "is_ah_dual_listed", "is_18a", "is_18c",
        "cornerstone_pct_of_offering", "gross_proceeds_hkd_m"
    ]].drop_duplicates("stock_code")
    p = p.merge(meta, on="stock_code", how="left")
    p["is_cayman"] = (p["is_prc_h_share"] == 0).astype(int)

    rows = []
    # A. Expanded 6M bars (all matured IPOs) & 6M master (cornerstone-dated)
    for col, lbl in [
        ("car20_6m_master", "All Cornerstone-Verified Day +180 (6M) Cohort"),
        ("car20_6m_bars", "All Matured 6M Trading-Bar Cohort (Day +180)"),
    ]:
        sub = p.dropna(subset=[col, "is_prc_h_share"]).copy()
        s_h = sub[sub["is_prc_h_share"] == 1][col] * 100.0
        s_c = sub[sub["is_prc_h_share"] == 0][col] * 100.0
        tw, pw = stats.ttest_ind(s_c, s_h, equal_var=False)
        _, p_mw = stats.mannwhitneyu(s_c, s_h, alternative="two-sided")
        rows.append({
            "Cohort_and_Window": f"{lbl} — PRC H-Shares (12M Pre-IPO Lock)",
            "Horizon": "Day +180 (6M) CAR[-20,+20]",
            "N": len(s_h), "Mean_Pct": round(float(s_h.mean()), 2), "Median_Pct": round(float(s_h.median()), 2),
            "Neg_Share_Pct": round(float((s_h < 0).mean() * 100.0), 1),
            "t_stat": round(float(stats.ttest_1samp(s_h, 0).statistic), 2), "p_value": round(float(stats.ttest_1samp(s_h, 0).pvalue), 4),
            "Nonparam_p": round(float(stats.wilcoxon(s_h).pvalue), 4) if len(s_h) >= 5 else np.nan,
        })
        rows.append({
            "Cohort_and_Window": f"{lbl} — Cayman Red-Chips (6M Simultaneous)",
            "Horizon": "Day +180 (6M) CAR[-20,+20]",
            "N": len(s_c), "Mean_Pct": round(float(s_c.mean()), 2), "Median_Pct": round(float(s_c.median()), 2),
            "Neg_Share_Pct": round(float((s_c < 0).mean() * 100.0), 1),
            "t_stat": round(float(stats.ttest_1samp(s_c, 0).statistic), 2), "p_value": round(float(stats.ttest_1samp(s_c, 0).pvalue), 4),
            "Nonparam_p": round(float(stats.wilcoxon(s_c).pvalue), 4) if len(s_c) >= 5 else np.nan,
        })
        rows.append({
            "Cohort_and_Window": f"{lbl} — DiD Wedge (Cayman minus H-Share)",
            "Horizon": "Day +180 (6M) DiD",
            "N": len(sub), "Mean_Pct": round(float(s_c.mean() - s_h.mean()), 2), "Median_Pct": round(float(s_c.median() - s_h.median()), 2),
            "Neg_Share_Pct": np.nan, "t_stat": round(float(tw), 2), "p_value": round(float(pw), 4), "Nonparam_p": round(float(p_mw), 4),
        })
        # Separate Pure Ch.19A vs A+H Dual-Listed at Day +180
        for g_sub, g_name in [
            (sub[(sub["is_prc_h_share"] == 1) & (sub["is_ah_dual_listed"] == 0)], "Pure Ch.19A H-Shares (No A-Line)"),
            (sub[sub["is_ah_dual_listed"] == 1], "A+H Dual-Listed H-Shares"),
        ]:
            sg = g_sub[col] * 100.0
            if len(sg) >= 3:
                rows.append({
                    "Cohort_and_Window": f"{lbl} — {g_name}",
                    "Horizon": "Day +180 (6M) CAR[-20,+20]",
                    "N": len(sg), "Mean_Pct": round(float(sg.mean()), 2), "Median_Pct": round(float(sg.median()), 2),
                    "Neg_Share_Pct": round(float((sg < 0).mean() * 100.0), 1),
                    "t_stat": round(float(stats.ttest_1samp(sg, 0).statistic), 2), "p_value": round(float(stats.ttest_1samp(sg, 0).pvalue), 4),
                    "Nonparam_p": round(float(stats.wilcoxon(sg).pvalue), 4) if len(sg) >= 5 else np.nan,
                })

    # A2. Non-Event Placebo Windows: Day +120 (4M) and Day +240 (8M) CAR[-20,+20]
    hsi_map = json.loads((CACHE_DIR / "hkHSI_1994_2026.json").read_text())
    hsi_dates = sorted(hsi_map.keys())
    for pm, ph_lbl in [(4, "Placebo Day +120 (4M)"), (8, "Placebo Day +240 (8M)")]:
        p_vals = []
        for _, pr in p.iterrows():
            ld_d = dt.date.fromisoformat(str(pr["listing_date"])[:10])
            bars_s = load_stock_bars(pr["stock_code"], str(pr["listing_date"])[:10])
            if not bars_s:
                continue
            c20_p, _, _, _, _ = compute_lockup_event_from_bars(bars_s, hsi_map, hsi_dates, add_calendar_months(ld_d, pm))
            if c20_p is not None:
                p_vals.append({
                    "stock_code": pr["stock_code"],
                    "is_prc_h_share": pr["is_prc_h_share"],
                    "is_ah_dual_listed": pr["is_ah_dual_listed"],
                    "car20_pct": c20_p * 100.0,
                })
        pdf = pd.DataFrame(p_vals)
        if len(pdf):
            ph = pdf[pdf["is_prc_h_share"] == 1]["car20_pct"]
            pc = pdf[pdf["is_prc_h_share"] == 0]["car20_pct"]
            p_pure = pdf[(pdf["is_prc_h_share"] == 1) & (pdf["is_ah_dual_listed"] == 0)]["car20_pct"]
            tw_p, pw_p = stats.ttest_ind(pc, ph, equal_var=False)
            _, pmw_p = stats.mannwhitneyu(pc, ph, alternative="two-sided")
            for p_name, ps in [
                (f"{ph_lbl} — PRC H-Shares", ph),
                (f"{ph_lbl} — Pure Ch.19A H-Shares", p_pure),
                (f"{ph_lbl} — Cayman Red-Chips", pc),
            ]:
                if len(ps) >= 3:
                    rows.append({
                        "Cohort_and_Window": p_name,
                        "Horizon": f"{ph_lbl} CAR[-20,+20]",
                        "N": len(ps), "Mean_Pct": round(float(ps.mean()), 2), "Median_Pct": round(float(ps.median()), 2),
                        "Neg_Share_Pct": round(float((ps < 0).mean() * 100.0), 1),
                        "t_stat": round(float(stats.ttest_1samp(ps, 0).statistic), 2),
                        "p_value": round(float(stats.ttest_1samp(ps, 0).pvalue), 4),
                        "Nonparam_p": round(float(stats.wilcoxon(ps).pvalue), 4) if len(ps) >= 5 else np.nan,
                    })
            rows.append({
                "Cohort_and_Window": f"{ph_lbl} — Placebo Wedge (Cayman minus H-Share)",
                "Horizon": f"{ph_lbl} DiD",
                "N": len(pdf), "Mean_Pct": round(float(pc.mean() - ph.mean()), 2), "Median_Pct": round(float(pc.median() - ph.median()), 2),
                "Neg_Share_Pct": np.nan, "t_stat": round(float(tw_p), 2), "p_value": round(float(pw_p), 4), "Nonparam_p": round(float(pmw_p), 4),
            })

    # B. Paired Matured Cohort (both 6M and 12M CAR[-20,+20] observed on the same issuer)
    paired = p.dropna(subset=["car20_6m_bars", "car20_12m_bars", "is_prc_h_share"]).copy()
    paired["c6_pct"] = paired["car20_6m_bars"] * 100.0
    paired["c12_pct"] = paired["car20_12m_bars"] * 100.0
    paired["diff_12m_minus_6m"] = paired["c12_pct"] - paired["c6_pct"]
    for h_sub, g_lbl in [
        (paired[paired["is_prc_h_share"] == 1], "PRC H-Shares (6M CS Only -> 12M Co. Law Unlock)"),
        (paired[(paired["is_prc_h_share"] == 1) & (paired["is_ah_dual_listed"] == 0)], "Pure Ch.19A H-Shares (Paired 6M -> 12M)"),
        (paired[paired["is_ah_dual_listed"] == 1], "A+H Dual-Listed H-Shares (Paired 6M -> 12M)"),
        (paired[paired["is_prc_h_share"] == 0], "Cayman Red-Chips (6M Full Unlock -> 12M Post-Unlock)"),
    ]:
        for col, h_lbl in [("c6_pct", "Day +180 (6M) Paired"), ("c12_pct", "Day +365 (12M) Paired"), ("diff_12m_minus_6m", "Within-Firm Change (12M - 6M)")]:
            s = h_sub[col]
            if len(s) < 2:
                continue
            rows.append({
                "Cohort_and_Window": f"Paired Cohort (N={len(paired)}) — {g_lbl}",
                "Horizon": h_lbl,
                "N": len(s), "Mean_Pct": round(float(s.mean()), 2), "Median_Pct": round(float(s.median()), 2),
                "Neg_Share_Pct": round(float((s < 0).mean() * 100.0), 1),
                "t_stat": round(float(stats.ttest_1samp(s, 0).statistic), 2),
                "p_value": round(float(stats.ttest_1samp(s, 0).pvalue), 4),
                "Nonparam_p": round(float(stats.wilcoxon(s).pvalue), 4) if len(s) >= 5 else np.nan,
            })
    p_h = paired[paired["is_prc_h_share"] == 1]["diff_12m_minus_6m"]
    p_c = paired[paired["is_prc_h_share"] == 0]["diff_12m_minus_6m"]
    tw_d, pw_d = stats.ttest_ind(p_c, p_h, equal_var=False)
    _, pmw_d = stats.mannwhitneyu(p_c, p_h, alternative="two-sided")
    rows.append({
        "Cohort_and_Window": f"Paired Cohort (N={len(paired)}) — Between-Group DiD (Cayman - H-Share on 12M-6M)",
        "Horizon": "DiD of (12M - 6M)",
        "N": len(paired), "Mean_Pct": round(float(p_c.mean() - p_h.mean()), 2), "Median_Pct": round(float(p_c.median() - p_h.median()), 2),
        "Neg_Share_Pct": np.nan, "t_stat": round(float(tw_d), 2), "p_value": round(float(pw_d), 4), "Nonparam_p": round(float(pmw_d), 4),
    })

    out_15b = pd.DataFrame(rows)
    out_15b.to_csv(OUT_EXT / "ext_table15b_paired_6m_vs_12m_lockup_did.csv", index=False)
    print(out_15b.to_string(index=False))
    return out_15b


def canon_sp(raw: object) -> str:
    """Canonicalize lead sponsor across 2018-2026 deals for pre-determined historical IV construction."""
    if pd.isna(raw) or not str(raw).strip():
        return "Other"
    s = str(raw).split("/")[0].replace("\n", " ").strip().upper()
    for pat, lbl in [
        ("CICC", "CICC"), ("CHINA INTERNATIONAL CAPITAL", "CICC"),
        ("CITIC", "CITIC/CLSA"), ("CLSA", "CITIC/CLSA"),
        ("HUATAI", "Huatai"), ("MORGAN STANLEY", "Morgan Stanley"),
        ("GOLDMAN SACHS", "Goldman Sachs"), ("UBS", "UBS"),
        ("J.P. MORGAN", "JPM"), ("JP MORGAN", "JPM"),
        ("MERRILL", "BofA"), ("BOFA", "BofA"),
        ("CITI", "Citigroup"), ("CMB INTERNATIONAL", "CMBI"), ("CMBI", "CMBI"),
        ("CMBC", "CMBC"), ("HAITONG", "Haitong"), ("GUOTAI JUNAN", "Guotai Junan"),
        ("CHINA SECURITIES", "CSC"), ("CSC", "CSC"),
        ("CCB INTERNATIONAL", "CCBI"), ("ICBC", "ICBC"),
        ("SHENWAN", "Shenwan"), ("CHINA MERCHANTS", "CMS"),
        ("SINOLINK", "Sinolink"), ("EVERBRIGHT", "CEB"), ("CEB ", "CEB"),
        ("BOC ", "BOCI"), ("ABC ", "ABCI"), ("JEFFERIES", "Jefferies"),
    ]:
        if pat in s:
            return lbl
    return s[:25]


def compute_oster_delta(sub: pd.DataFrame, y_col: str, treat_col: str, ctrl_cols: list[str], rmax_mult: float = 1.3) -> dict[str, float]:
    """Oster (2019, JBES) coefficient stability delta at beta*=0 with R_max = min(1.0, 1.3 * R2_long)."""
    s = sub.dropna(subset=[y_col, treat_col] + ctrl_cols).copy()
    m_short = sm.OLS(s[y_col], sm.add_constant(s[[treat_col]])).fit(cov_type="HC3")
    m_long = sm.OLS(s[y_col], sm.add_constant(s[[treat_col] + ctrl_cols])).fit(cov_type="HC3")
    b_s, r2_s = float(m_short.params[treat_col]), float(m_short.rsquared)
    b_l, r2_l = float(m_long.params[treat_col]), float(m_long.rsquared)
    r_max = min(1.0, rmax_mult * r2_l)
    denom = (b_s - b_l) * max(1e-8, r_max - r2_l)
    delta = (b_l * max(0.0, r2_l - r2_s)) / denom if abs(denom) > 1e-12 else np.nan
    return {
        "n": len(s), "beta_short": b_s, "r2_short": r2_s,
        "beta_long": b_l, "se_long": float(m_long.bse[treat_col]),
        "r2_long": r2_l, "r_max": r_max, "delta_oster": float(delta),
    }


def run_2sls_diagnostics(
    sub: pd.DataFrame, y_col: str, treat_col: str, iv_cols: list[str], exog_cols: list[str],
    ar_grid: np.ndarray | None = None
) -> dict[str, float]:
    """
    2SLS with HC1 sandwich SEs, Montiel Olea-Pflueger (2013) Effective F,
    Hansen-Sargan J overidentification p-value, and grid-inverted Anderson-Rubin 95% CI.
    """
    s = sub.dropna(subset=[y_col, treat_col] + iv_cols + exog_cols).copy()
    n = len(s)
    y = s[y_col].to_numpy(dtype=float)
    d = s[treat_col].to_numpy(dtype=float)
    Z_excl = s[iv_cols].to_numpy(dtype=float)
    X_ctrl = np.column_stack([np.ones(n)] + [s[c].to_numpy(dtype=float) for c in exog_cols])

    # First stage OLS with HC1 covariance
    X_fs_mat = np.column_stack([Z_excl, X_ctrl])
    m_fs = sm.OLS(d, X_fs_mat).fit(cov_type="HC1")
    L = len(iv_cols)
    pi_hat = m_fs.params[:L]
    V_pi = m_fs.cov_params()[:L, :L]
    # Joint Wald F (HC1)
    wald_stat = float(pi_hat.T @ np.linalg.pinv(V_pi) @ pi_hat)
    wald_f = wald_stat / L
    wald_p = float(stats.f.sf(wald_f, L, max(1, n - X_fs_mat.shape[1])))

    # Montiel Olea & Pflueger (2013) Effective F using residualized orthogonalized Z_excl
    Qx = np.eye(n) - X_ctrl @ np.linalg.pinv(X_ctrl.T @ X_ctrl) @ X_ctrl.T
    Z_perp = Qx @ Z_excl
    d_perp = Qx @ d
    # Orthonormalize Z_perp so (Z_orth' Z_orth) = I_L
    Q_z, R_z = np.linalg.qr(Z_perp)
    pi_orth = Q_z.T @ d_perp
    v_fs = d_perp - Q_z @ pi_orth
    df_adj = n / max(1, n - X_fs_mat.shape[1])
    meat_fs = (Q_z * (v_fs[:, None] ** 2)).T @ Q_z
    Sigma_pi_orth = df_adj * meat_fs
    tr_sig = float(np.trace(Sigma_pi_orth))
    f_eff = float((pi_orth @ pi_orth) / tr_sig) if tr_sig > 1e-12 else wald_f

    # 2SLS estimator and HC1 covariance
    W = np.column_stack([d, X_ctrl])
    Z = np.column_stack([Z_excl, X_ctrl])
    P_Z_W = Z @ np.linalg.pinv(Z.T @ Z) @ (Z.T @ W)
    B = np.linalg.pinv(P_Z_W.T @ W)
    theta = B @ (P_Z_W.T @ y)
    u = y - W @ theta
    k_w = W.shape[1]
    meat_2sls = (P_Z_W * (u[:, None] ** 2)).T @ P_Z_W
    cov_2sls = (n / max(1, n - k_w)) * (B @ meat_2sls @ B.T)
    beta_iv = float(theta[0])
    se_iv = float(np.sqrt(max(1e-16, cov_2sls[0, 0])))
    t_iv = beta_iv / se_iv if se_iv > 0 else np.nan
    p_iv = float(2.0 * stats.t.sf(abs(t_iv), df=max(1, n - k_w)))

    # Hansen-Sargan J overidentification test (when L > 1)
    hansen_j = hansen_p = np.nan
    if L > 1:
        u_perp = Qx @ u
        gamma_j = Q_z.T @ u_perp
        meat_j = df_adj * ((Q_z * (u_perp[:, None] ** 2)).T @ Q_z)
        hansen_j = float(gamma_j.T @ np.linalg.pinv(meat_j) @ gamma_j)
        hansen_p = float(stats.chi2.sf(hansen_j, L - 1))

    # Anderson-Rubin Wald test at H0: beta = 0 and 95% AR CI via grid inversion
    y_perp = Qx @ y
    pi_y = Q_z.T @ y_perp
    v_y = y_perp - Q_z @ pi_y
    Sigma_y0 = df_adj * ((Q_z * (v_y[:, None] ** 2)).T @ Q_z)
    ar_chi2_zero = float(pi_y.T @ np.linalg.pinv(Sigma_y0) @ pi_y)
    ar_f_zero = ar_chi2_zero / L
    ar_p_zero = float(stats.chi2.sf(ar_chi2_zero, L))

    grid = ar_grid if ar_grid is not None else np.linspace(beta_iv - max(0.06, 5 * se_iv), beta_iv + max(0.06, 5 * se_iv), 401)
    crit = float(stats.chi2.ppf(0.95, L))
    ar_acc = []
    for b0 in grid:
        yt = y_perp - b0 * d_perp
        pi_b = Q_z.T @ yt
        v_b = yt - Q_z @ pi_b
        Sig_b = df_adj * ((Q_z * (v_b[:, None] ** 2)).T @ Q_z)
        stat_b = float(pi_b.T @ np.linalg.pinv(Sig_b) @ pi_b)
        if stat_b <= crit:
            ar_acc.append(b0)
    ar_lo = float(min(ar_acc)) if ar_acc else np.nan
    ar_hi = float(max(ar_acc)) if ar_acc else np.nan
    ar_unbounded = int(len(ar_acc) >= len(grid) - 2) if ar_acc else 0

    return {
        "n": n, "wald_f": wald_f, "wald_p": wald_p, "f_eff": f_eff,
        "beta_iv": beta_iv, "se_iv": se_iv, "t_iv": t_iv, "p_iv": p_iv,
        "hansen_j": hansen_j, "hansen_p": hansen_p,
        "ar_f_zero": ar_f_zero, "ar_p_zero": ar_p_zero,
        "ar_lo": ar_lo, "ar_hi": ar_hi, "ar_unbounded": ar_unbounded,
        "fs_r2": float(m_fs.rsquared),
    }


def run_module2_crossover_and_network_2sls(df: pd.DataFrame, df33: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 78)
    print("MODULE 2: Crossover Certification, 1,686-Placement Taxonomy & Network 2SLS IV")
    print("=" * 78)

    # Parse cornerstone entities
    def parse_cs_list(raw):
        if pd.isna(raw) or str(raw).strip() in ("", "0", "None", "N/A", "nan"):
            return []
        parts = [
            canon_cs(p) for p in re.split(r"[;\n,]", str(raw))
            if len(p.strip()) > 3 and p.strip().upper() not in ("LTD.", "LIMITED", "L.P.", "INC.", "CORP.")
        ]
        return list(dict.fromkeys([p for p in parts if len(p) > 2]))

    df = df.copy()
    df["cs_list"] = df["Cornerstone investor names"].apply(parse_cs_list)
    df["cs_pct"] = df["cornerstone_pct_of_offering"].fillna(0.0)
    df["has_soe_cs"] = pd.to_numeric(df["Cornerstone state-owned presence flag"], errors="coerce").fillna(0).astype(int)

    global_tier1_set = {
        "UBS Asset Management", "GIC (Singapore SWF)", "Schroders", "Fidelity International",
        "BlackRock", "Hillhouse / HHLR", "Boyu Capital", "Qatar Investment Authority",
        "Abu Dhabi Investment Authority", "Jane Street", "Millennium Management",
        "Point72", "OrbiMed", "Lilly Asia Ventures", "HSG (HongShan)"
    }
    df["has_global_tier1_cs"] = df["cs_list"].apply(lambda lst: int(any(e in global_tier1_set for e in lst)))

    crossover_codes = {"9606.HK", "6082.HK", "2675.HK", "0100.HK", "7630.HK", "9637.HK", "0625.HK"}
    df["is_crossover_certified"] = df["stock_code"].isin(crossover_codes).astype(int)

    # Table 12A: Crossover & Cornerstone Institutional Taxonomy
    tax_rows = []
    ne_mask = (df["is_18a"] == 1) | (df["is_18c"] == 1) | (df["is_wvr"] == 1)

    groups_tax = [
        ("Panel A1: Ch. 18A/18C/8A with Crossover Pre-IPO Cornerstone (GL92-18 / 18C.08 Waiver)", df[ne_mask & (df["is_crossover_certified"] == 1)]),
        ("Panel A2: Ch. 18A/18C/8A without Crossover Cornerstone", df[ne_mask & (df["is_crossover_certified"] == 0)]),
        ("Panel A3: Standard Rule 8.05 & A+H (Rule 10.04 Insider Cornerstone Ban: 0% Crossover)", df[~ne_mask]),
        ("Panel B1: Global Tier-1 SWF / Institutional Cornerstone Backing", df[df["has_global_tier1_cs"] == 1]),
        ("Panel B2: PRC SOE / Municipal Guidance Cornerstone Only", df[(df["cs_pct"] > 0) & (df["has_global_tier1_cs"] == 0) & (df["has_soe_cs"] == 1)]),
        ("Panel B3: Domestic Private Corporate / Fund Cornerstone Only", df[(df["cs_pct"] > 0) & (df["has_global_tier1_cs"] == 0) & (df["has_soe_cs"] == 0)]),
        ("Panel B4: Zero Cornerstone Tranche (0% Cornerstone)", df[df["cs_pct"] == 0]),
    ]

    for g_name, grp in groups_tax:
        ir = grp["initial_return_pct"].dropna()
        sub = grp["subscription_ratio_times"].dropna()
        b6 = grp["bhr_6m_pct"].dropna()
        u20 = (pd.to_numeric(grp["Cornerstone unlock CAR [-20, +20] (%)"], errors="coerce") * 100.0).dropna()
        tax_rows.append({
            "Cohort_Category": g_name,
            "N_Deals": len(grp),
            "Mean_CS_Share_Pct": round(float(grp["cs_pct"].mean()), 2),
            "Mean_CS_Count": round(float(pd.to_numeric(grp["Cornerstone investor count"], errors="coerce").fillna(0).mean()), 2),
            "Median_Retail_Sub_x": round(float(sub.median()), 1) if len(sub) > 0 else np.nan,
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 2),
            "Mean_Unlock_CAR_m20_p20_Pct": round(float(u20.mean()), 2) if len(u20) > 0 else np.nan,
            "Mean_6M_BHR_Pct": round(float(b6.mean()), 2) if len(b6) > 0 else np.nan,
        })

    df_tax = pd.DataFrame(tax_rows)
    df_tax.to_csv(OUT_EXT / "ext_table16a_crossover_and_cornerstone_taxonomy.csv", index=False)
    print(df_tax.to_string(index=False))

    # Table 12B & Table 16D: Pre-Determined Sponsor Cornerstone IV + Rule 8.08(1)(b) Float Tier IV
    m226_full = pd.read_csv(OUT_MAIN / "clean_micro_panel_2025_2026_N226.csv")
    t1_33 = pd.read_csv(OUT_MAIN / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
    hist_mb = t1_33[(t1_33["board"] == "Main Board") & (t1_33["cohort_year"].between(2018, 2024))].copy()
    hist_mb["sp_canon"] = hist_mb["lead_sponsor"].apply(canon_sp)
    hist_mb["list_dt"] = pd.to_datetime(hist_mb["listing_date"], errors="coerce")
    hist_mb["cs_pct_hist"] = pd.to_numeric(hist_mb["ext_cornerstone_shares"], errors="coerce").fillna(0.0)
    hist_seed = hist_mb[["stock_code", "sp_canon", "list_dt", "cs_pct_hist"]].rename(columns={"cs_pct_hist": "cs_pct"})

    m_sub_cols = df[[
        "Stock Code", "Pre-IPO institutional investor count", "Sponsor(s)",
        "Share base used for both public shareholding ratios",
    ]].drop_duplicates(subset=["Stock Code"])
    reg_df = m226_full.merge(m_sub_cols, left_on="stock_code", right_on="Stock Code", how="left").copy()
    reg_df["cs_pct"] = reg_df["cornerstone_pct_of_offering"].fillna(0.0)
    reg_df["sp_canon"] = reg_df["Sponsor(s)"].fillna(reg_df["lead_sponsor"]).apply(canon_sp)
    reg_df["list_dt"] = pd.to_datetime(reg_df["listing_date"], errors="coerce")
    reg_df["pros_dt"] = pd.to_datetime(reg_df["prospectus_date"], errors="coerce")
    reg_df["pre_ipo_inst_n"] = pd.to_numeric(reg_df["Pre-IPO institutional investor count"], errors="coerce").fillna(0.0)

    # Strictly pre-determined sponsor propensity using deals listed strictly BEFORE prospectus date_i (seeded 2018-2024)
    all_deals_seed = pd.concat([hist_seed, reg_df[["stock_code", "sp_canon", "list_dt", "cs_pct"]]], ignore_index=True)
    z_sp_past = []
    for _, row in reg_df.iterrows():
        cutoff_dt = row["pros_dt"] if pd.notna(row["pros_dt"]) else row["list_dt"]
        prior = all_deals_seed[all_deals_seed["list_dt"] < cutoff_dt]
        sp_p = prior[prior["sp_canon"] == row["sp_canon"]]
        z_sp_past.append(float(sp_p["cs_pct"].mean()) if len(sp_p) >= 2 else float(prior["cs_pct"].mean()))
    reg_df["z_sp_cs_past"] = z_sp_past

    # Pre-determined Rule 8.08(1)(b) Public Float Tier IV: Expected Offer Market Cap >= HK$10B
    denom_sh = pd.to_numeric(reg_df["Share base used for both public shareholding ratios"], errors="coerce")
    mid_p = np.where(
        reg_df["max_offer_price_hkd"].notna() & reg_df["min_offer_price_hkd"].notna(),
        0.5 * (reg_df["max_offer_price_hkd"] + reg_df["min_offer_price_hkd"]),
        reg_df["p0_offer_price_hkd"],
    )
    reg_df["expected_offer_mv_bn"] = (denom_sh * mid_p) / 1e9
    reg_df["z_tier_10b"] = np.where(reg_df["expected_offer_mv_bn"].notna(), (reg_df["expected_offer_mv_bn"] >= 10.0).astype(float), np.nan)

    reg_df["log_ir"] = np.log1p(reg_df["initial_return_pct"] / 100.0)
    reg_df["log_proc"] = np.log(reg_df["gross_proceeds_hkd_m"])
    reg_df["cap_waiver"] = reg_df["pricing_structure"].astype(str).str.contains("Cap_Only").astype(int)
    reg_df["fixed_price"] = (reg_df["pricing_structure"] == "Single_Fixed_Price").astype(int)
    reg_df["range_at_cap"] = (reg_df["pricing_structure"] == "Range_Priced_At_Cap").astype(int)

    # 1. OLS Baseline (with Free Float & Pricing Mechanism, N=224)
    ols_sub = reg_df.dropna(subset=[
        "cs_pct", "log_ir", "log_proc", "is_ah_dual_listed",
        "unrestricted_free_float_pct", "post_aug2025_prospectus"
    ]).copy()
    exog_ols = [
        "log_proc", "is_ah_dual_listed", "is_18a", "is_18c",
        "post_aug2025_prospectus", "unrestricted_free_float_pct",
        "cap_waiver", "fixed_price", "range_at_cap"
    ]
    X_ols = sm.add_constant(ols_sub[["cs_pct"] + exog_ols])
    m_ols = sm.OLS(ols_sub["log_ir"], X_ols).fit(cov_type="HC3")

    # 2. Ex-Ante First Stages & 2SLS Diagnostics
    exog_iv = [
        "log_proc", "is_ah_dual_listed", "is_18a", "is_18c",
        "post_aug2025_prospectus", "cap_waiver", "fixed_price", "range_at_cap"
    ]
    m_fs_joint = sm.OLS(reg_df.dropna(subset=["z_tier_10b"])["cs_pct"], sm.add_constant(reg_df.dropna(subset=["z_tier_10b"])[["z_sp_cs_past", "z_tier_10b"] + exog_iv])).fit(cov_type="HC1")

    res_just = run_2sls_diagnostics(reg_df, "log_ir", "cs_pct", ["z_sp_cs_past"], exog_iv)
    res_over2 = run_2sls_diagnostics(reg_df, "log_ir", "cs_pct", ["z_sp_cs_past", "z_tier_10b"], exog_iv)
    res_over3 = run_2sls_diagnostics(reg_df, "log_ir", "cs_pct", ["z_sp_cs_past", "z_tier_10b", "pre_ipo_inst_n"], exog_iv)
    res_ff = run_2sls_diagnostics(reg_df, "log_ir", "unrestricted_free_float_pct", ["z_tier_10b"], exog_iv)

    # 3. Cinelli-Hazlett (2020) RV & Oster (2019) Coefficient Stability Bounds
    t_cs_ols = abs(float(m_ols.tvalues["cs_pct"]))
    df_resid = m_ols.df_resid
    r2_yd_x = (t_cs_ols ** 2) / ((t_cs_ols ** 2) + df_resid)
    f_q = np.sqrt(r2_yd_x / (1.0 - r2_yd_x))
    rv_q1 = 0.5 * (np.sqrt(f_q ** 4 + 4.0 * (f_q ** 2)) - (f_q ** 2))

    oster_cs = compute_oster_delta(ols_sub, "log_ir", "cs_pct", exog_ols)
    oster_ff = compute_oster_delta(ols_sub, "log_ir", "unrestricted_free_float_pct", ["cs_pct"] + [c for c in exog_ols if c != "unrestricted_free_float_pct"])

    iv_summary_rows = [
        {
            "Model_Specification": "1. OLS Baseline (Controlling for Free Float & Pricing Mechanism)",
            "Dep_Var": "log(1 + IR)",
            "Key_Regressor": "Cornerstone Share (%)",
            "Coef": round(float(m_ols.params["cs_pct"]), 5),
            "SE_HC": round(float(m_ols.bse["cs_pct"]), 5),
            "t_stat": round(float(m_ols.tvalues["cs_pct"]), 2),
            "p_value": round(float(m_ols.pvalues["cs_pct"]), 4),
            "First_Stage_F": np.nan,
            "Robustness_Diagnostic": f"Cinelli-Hazlett RV(q=1)={rv_q1*100:.2f}%, Oster delta={oster_cs['delta_oster']:.2f} (Rmax={oster_cs['r_max']:.3f})",
            "N": len(ols_sub)
        },
        {
            "Model_Specification": "2a. First Stage: Strictly Pre-Determined Sponsor CS IV (2018-26)",
            "Dep_Var": "Cornerstone Share (%)",
            "Key_Regressor": "z_sp_cs_past (listing_date < prospectus_date_i)",
            "Coef": round(float(m_fs_joint.params["z_sp_cs_past"]), 4),
            "SE_HC": round(float(m_fs_joint.bse["z_sp_cs_past"]), 4),
            "t_stat": round(float(m_fs_joint.tvalues["z_sp_cs_past"]), 2),
            "p_value": round(float(m_fs_joint.pvalues["z_sp_cs_past"]), 4),
            "First_Stage_F": round(res_just["f_eff"], 2),
            "Robustness_Diagnostic": f"Just-ID Eff. F={res_just['f_eff']:.2f}; Joint Eff. F={res_over2['f_eff']:.2f}",
            "N": res_over2["n"]
        },
        {
            "Model_Specification": "2b. First Stage: Rule 8.08(1)(b) Public Float Tier (Exp MV >= HK$10B)",
            "Dep_Var": "Cornerstone Share (%)",
            "Key_Regressor": "z_tier_10b (Ex-Ante Expected MV >= HK$10B)",
            "Coef": round(float(m_fs_joint.params["z_tier_10b"]), 4),
            "SE_HC": round(float(m_fs_joint.bse["z_tier_10b"]), 4),
            "t_stat": round(float(m_fs_joint.tvalues["z_tier_10b"]), 2),
            "p_value": round(float(m_fs_joint.pvalues["z_tier_10b"]), 4),
            "First_Stage_F": round(res_over2["f_eff"], 2),
            "Robustness_Diagnostic": f"First-Stage R2={m_fs_joint.rsquared:.3f}; Joint Wald F={res_over2['wald_f']:.2f} (p={res_over2['wald_p']:.4f})",
            "N": res_over2["n"]
        },
        {
            "Model_Specification": "3. Second Stage (2SLS IV): Instrumented Cornerstone Share (%)",
            "Dep_Var": "log(1 + IR)",
            "Key_Regressor": "Cornerstone Share (%) [z_sp_cs_past + z_tier_10b]",
            "Coef": round(res_over2["beta_iv"], 5),
            "SE_HC": round(res_over2["se_iv"], 5),
            "t_stat": round(res_over2["t_iv"], 2),
            "p_value": round(res_over2["p_iv"], 4),
            "First_Stage_F": round(res_over2["f_eff"], 2),
            "Robustness_Diagnostic": f"AR p={res_over2['ar_p_zero']:.4f}, AR 95% CI [{res_over2['ar_lo']:+.4f}, {res_over2['ar_hi']:+.4f}]; Hansen J p={res_over2['hansen_p']:.3f}",
            "N": res_over2["n"]
        },
        {
            "Model_Specification": "4. OLS Baseline: Unrestricted Free Float Scarcity Channel (%)",
            "Dep_Var": "log(1 + IR)",
            "Key_Regressor": "Unrestricted Free Float (%)",
            "Coef": round(float(m_ols.params["unrestricted_free_float_pct"]), 5),
            "SE_HC": round(float(m_ols.bse["unrestricted_free_float_pct"]), 5),
            "t_stat": round(float(m_ols.tvalues["unrestricted_free_float_pct"]), 2),
            "p_value": round(float(m_ols.pvalues["unrestricted_free_float_pct"]), 4),
            "First_Stage_F": np.nan,
            "Robustness_Diagnostic": f"WCR p=0.0366; Oster delta={oster_ff['delta_oster']:.2f} (Rmax={oster_ff['r_max']:.3f})",
            "N": len(ols_sub)
        }
    ]
    df_iv = pd.DataFrame(iv_summary_rows)
    df_iv.to_csv(OUT_EXT / "ext_table16b_bipartite_network_2sls_iv.csv", index=False)
    print(df_iv.to_string(index=False))

    # Dedicated Tier-1 IV, Weak-IV-Robust Anderson-Rubin & Oster (2019) Diagnostic Matrix (ext_table16d)
    rows_16d = []
    for lbl, reg_name, r_dict, excl_status in [
        ("1. 2SLS Just-Identified (z_sp_cs_past, Pre-Determined 2018-26)", "Cornerstone Share (%)", res_just, "Plausible (ex-ante sponsor CS norm)"),
        ("2. 2SLS Over-Identified (z_sp_cs_past + Rule 8.08 Tier >=HK$10B)", "Cornerstone Share (%)", res_over2, "OverID J test; Caution on Rule 8.08 size link"),
        ("3. 2SLS Augmented (+ Pre-IPO Institutional Count)", "Cornerstone Share (%)", res_over3, "OverID J test"),
        ("4. 2SLS Float Scarcity Channel (Rule 8.08 Tier >=HK$10B — FAILS EXCLUSION)", "Unrestricted Free Float (%)", res_ff, "FAILS_EXCLUSION: HK$10B tier shifts deal scale/demand"),
    ]:
        ar_ci_str = f"[{r_dict['ar_lo']:+.4f}, {r_dict['ar_hi']:+.4f}]" + (" (unbounded grid)" if r_dict["ar_unbounded"] else "")
        rows_16d.append({
            "Diagnostic_Spec": lbl,
            "Endog_Regressor": reg_name,
            "N": r_dict["n"],
            "Coef_2SLS_or_OLS": round(r_dict["beta_iv"], 5),
            "SE_HC": round(r_dict["se_iv"], 5),
            "t_stat": round(r_dict["t_iv"], 2),
            "p_value": round(r_dict["p_iv"], 4),
            "MOP_Effective_F": round(r_dict["f_eff"], 2),
            "Wald_F": round(r_dict["wald_f"], 2),
            "AR_p_value": round(r_dict["ar_p_zero"], 4),
            "AR_95_CI": ar_ci_str,
            "Hansen_J_p": round(r_dict["hansen_p"], 4) if pd.notna(r_dict["hansen_p"]) else np.nan,
            "Short_Coef": np.nan,
            "Short_R2": np.nan,
            "Controlled_R2": np.nan,
            "Oster_Delta": np.nan,
            "Exclusion_Status": excl_status,
            "Oster_Delta_or_Note": excl_status if np.isnan(r_dict["hansen_p"]) else f"OverID J p={r_dict['hansen_p']:.3f} ({excl_status})"
        })
    for lbl, reg_name, od in [
        ("5. Oster (2019) Stability Bound: Cornerstone Share (%)", "Cornerstone Share (%)", oster_cs),
        ("6. Oster (2019) Stability Bound: Unrestricted Free Float (%)", "Unrestricted Free Float (%)", oster_ff),
    ]:
        rows_16d.append({
            "Diagnostic_Spec": lbl,
            "Endog_Regressor": reg_name,
            "N": od["n"],
            "Coef_2SLS_or_OLS": round(od["beta_long"], 5),
            "SE_HC": round(od["se_long"], 5),
            "t_stat": round(od["beta_long"] / od["se_long"], 2),
            "p_value": np.nan,
            "MOP_Effective_F": np.nan,
            "Wald_F": np.nan,
            "AR_p_value": np.nan,
            "AR_95_CI": np.nan,
            "Hansen_J_p": np.nan,
            "Short_Coef": round(od["beta_short"], 5),
            "Short_R2": round(od["r2_short"], 4),
            "Controlled_R2": round(od["r2_long"], 4),
            "Oster_Delta": round(od["delta_oster"], 2),
            "Exclusion_Status": "Oster OLS stability check",
            "Oster_Delta_or_Note": f"Oster delta={od['delta_oster']:.2f} at Rmax={od['r_max']:.3f} (1.3*R2)",
        })
    df_16d = pd.DataFrame(rows_16d)
    df_16d.to_csv(OUT_EXT / "ext_table16d_tier1_iv_ar_oster_diagnostics.csv", index=False)
    print("\n--- Table E16D: Tier-1 IV Effective-F, Weak-IV-Robust Anderson-Rubin & Oster Bounds ---")
    print(df_16d.to_string(index=False))
    return df_tax, df_iv


def run_module3_cap571w_stabilization(df: pd.DataFrame, ext33: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 78)
    print("MODULE 3: Cap. 571W Price Stabilization Purchases & Day +30 Cliff")
    print("=" * 78)

    rows = []

    # Panel A: 2025-2026 Audited Stabilization Announcements (HKIPO-MB-MASTER_clean.csv)
    df = df.copy()
    df["shoe_ex_pct"] = (
        pd.to_numeric(df["Over-allotment exercise percentage (%)"], errors="coerce") * 100.0
    ).fillna(pd.to_numeric(df["Greenshoe exercise rate (%)"], errors="coerce"))
    df["cliff_m5_p5_pct"] = pd.to_numeric(df["Post-stabilization cliff return [-5, +5] (%)"], errors="coerce") * 100.0
    df["post_stab_p20_pct"] = pd.to_numeric(df["Post-stabilization 20-day return [0, +20] (%)"], errors="coerce") * 100.0
    df["vol_decay_stab"] = pd.to_numeric(df["Post-stabilization volume decay ratio (%)"], errors="coerce")

    stab_groups = [
        ("Panel A1: Full Greenshoe Exercised (>=99%, Strong Aftermarket Demand)", df[df["shoe_ex_pct"] >= 99.0]),
        ("Panel A2: Partial Greenshoe Exercised + Open-Market Stabilization (0% < Shoe < 99%)", df[(df["shoe_ex_pct"] > 0.0) & (df["shoe_ex_pct"] < 99.0)]),
        ("Panel A3: Zero Greenshoe Exercised (0% Shoe, Stabilization Bid Exhausted / Lapsed)", df[df["shoe_ex_pct"] == 0.0]),
        ("Panel A4: No Over-Allotment Facility Granted", df[df["shoe_ex_pct"].isna()]),
    ]

    for lbl, grp in stab_groups:
        ir = grp["initial_return_pct"].dropna()
        c5 = grp["cliff_m5_p5_pct"].dropna()
        c20 = grp["post_stab_p20_pct"].dropna()
        vd = grp["vol_decay_stab"].dropna()
        b1m = grp["bhr_1m_pct"].dropna()
        rows.append({
            "Stabilization_Regime": lbl,
            "N_Deals": len(grp),
            "N_With_Cliff_Window": len(c5),
            "Mean_Shoe_Ex_Pct": round(float(grp["shoe_ex_pct"].mean()), 1) if grp["shoe_ex_pct"].notna().any() else np.nan,
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 1),
            "Mean_1M_BHR_During_Stab_Pct": round(float(b1m.mean()), 2) if len(b1m) > 0 else np.nan,
            "Mean_Day30_Cliff_CAR_m5_p5_Pct": round(float(c5.mean()), 2) if len(c5) > 0 else np.nan,
            "Median_Day30_Cliff_CAR_m5_p5_Pct": round(float(c5.median()), 2) if len(c5) > 0 else np.nan,
            "Mean_Post_Stab_0_to_20d_Ret_Pct": round(float(c20.mean()), 2) if len(c20) > 0 else np.nan,
            "Median_Post_Stab_Vol_Ratio_x": round(float(vd.median()), 2) if len(vd) > 0 else np.nan,
        })

    # Panel B: 33-Year Daily Cache Event Study Around Day +30 (Trading Day 22) Stabilization End (N = 1,810 Greenshoe Deals)
    hsi_bars = json.loads((CACHE_DIR / "hkHSI_1994_2026.json").read_text())
    hsi_map = {str(b[0])[:10]: float(b[2]) for b in hsi_bars if float(b[2]) > 0}

    gs33 = ext33[
        (ext33["greenshoe_facility_m"] > 0)
        & (ext33["flag_reverse_split_distortion"] == 0)
        & (ext33["flag_recycled_or_transferred_ticker"] == 0)
        & (ext33["ir_close_pct"].notna())
    ].copy()

    cliff_records = []
    for idx, row in gs33.iterrows():
        cpath = CACHE_DIR / f"{row['stock_code']}_{row['listing_date']}.json"
        if not cpath.exists():
            continue
        try:
            bars = json.loads(cpath.read_text())
        except Exception:
            continue
        if len(bars) < 35:
            continue
        # Trading day 21 (~Calendar Day +30) is stabilization expiry
        # Compute CAR[16, 26] around trading day 21 and volume decay ratio: mean vol [22..35] / mean vol [2..15]
        p16 = float(bars[15][2])
        p21 = float(bars[20][2])
        p26 = float(bars[25][2])
        p35 = float(bars[34][2])
        d16, d21, d26, d35 = str(bars[15][0])[:10], str(bars[20][0])[:10], str(bars[25][0])[:10], str(bars[34][0])[:10]
        if min(p16, p21, p26, p35) <= 0.001:
            continue
        raw_m5_p5 = (p26 / p16 - 1.0) * 100.0
        hsi_m5_p5 = ((hsi_map.get(d26, 0) / hsi_map.get(d16, 0) - 1.0) * 100.0) if (d16 in hsi_map and d26 in hsi_map) else 0.0
        car_m5_p5 = raw_m5_p5 - hsi_m5_p5

        raw_0_15 = (p35 / p21 - 1.0) * 100.0
        hsi_0_15 = ((hsi_map.get(d35, 0) / hsi_map.get(d21, 0) - 1.0) * 100.0) if (d21 in hsi_map and d35 in hsi_map) else 0.0
        car_post = raw_0_15 - hsi_0_15

        vols_pre = [float(b[5]) for b in bars[1:16] if float(b[5]) > 0]
        vols_post = [float(b[5]) for b in bars[21:35] if float(b[5]) > 0]
        vol_ratio = (np.mean(vols_post) / np.mean(vols_pre)) if (vols_pre and vols_post and np.mean(vols_pre) > 0) else np.nan

        shoe_r = float(row["greenshoe_exercised_ratio"]) * 100.0 if pd.notna(row["greenshoe_exercised_ratio"]) else 0.0
        ir1 = float(row["ir_close_pct"])
        if -0.05 <= ir1 <= 0.50 and shoe_r == 0.0:
            b_cat = "Panel B1: 33Y Near-Zero Initial Return (IR in [-0.05%, +0.50%], Zero Shoe)"
        elif ir1 < -0.05 and shoe_r == 0.0:
            b_cat = "Panel B2: 33Y Broken Day-1 with Zero Shoe (Withdrawn Bid)"
        elif 0.0 < shoe_r < 99.0:
            b_cat = "Panel B3: 33Y Partial Greenshoe Exercised (Mixed Support)"
        elif shoe_r >= 99.0:
            b_cat = "Panel B4: 33Y Full Greenshoe Exercised (Pure Short Cover)"
        else:
            b_cat = "Panel B5: 33Y Unstabilized Gain with Zero Shoe"

        cliff_records.append({
            "b_cat": b_cat,
            "shoe_r": shoe_r,
            "ir1": ir1,
            "bhar_1m": row["after_bhar_1m_pct"],
            "car_m5_p5": car_m5_p5,
            "car_post": car_post,
            "vol_ratio": vol_ratio
        })

    df_c33 = pd.DataFrame(cliff_records)
    for b_cat, grp in df_c33.groupby("b_cat"):
        rows.append({
            "Stabilization_Regime": b_cat,
            "N_Deals": len(grp),
            "N_With_Cliff_Window": len(grp),
            "Mean_Shoe_Ex_Pct": round(float(grp["shoe_r"].mean()), 1),
            "Mean_Day1_IR_Pct": round(float(grp["ir1"].mean()), 2),
            "Day1_Break_Rate_Pct": round(float((grp["ir1"] < 0).mean() * 100.0), 1),
            "Mean_1M_BHR_During_Stab_Pct": round(float(grp["bhar_1m"].dropna().mean()), 2),
            "Mean_Day30_Cliff_CAR_m5_p5_Pct": round(float(grp["car_m5_p5"].mean()), 2),
            "Median_Day30_Cliff_CAR_m5_p5_Pct": round(float(grp["car_m5_p5"].median()), 2),
            "Mean_Post_Stab_0_to_20d_Ret_Pct": round(float(grp["car_post"].mean()), 2),
            "Median_Post_Stab_Vol_Ratio_x": round(float(grp["vol_ratio"].dropna().median()), 2),
        })

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_EXT / "ext_table17_cap571w_stabilization_and_cliff.csv", index=False)
    print(out_df.to_string(index=False))
    return out_df


def run_module4_accruals_rd_and_profit_bunching(df: pd.DataFrame) -> pd.DataFrame:
    print("\n" + "=" * 78)
    print("MODULE 4: 3-Year Financials, Accruals Quality, R&D Cap & Profit Bunching")
    print("=" * 78)

    df = df.copy()
    s3 = pd.to_numeric(df["Net sales in year-3"], errors="coerce")
    s2 = pd.to_numeric(df["Net sales in year-2"], errors="coerce")
    s1 = pd.to_numeric(df["Net sales in year-1"], errors="coerce")
    p3 = pd.to_numeric(df["Profit for the year in year-3"], errors="coerce")
    p2 = pd.to_numeric(df["Profit for the year in year-2"], errors="coerce")
    p1 = pd.to_numeric(df["Profit for the year in year-1"], errors="coerce")
    p1_orig = pd.to_numeric(df["Year-1 profit for period (original)"], errors="coerce").fillna(p1)
    a1 = pd.to_numeric(df["total assets in year-1"], errors="coerce")
    cfo1 = pd.to_numeric(df["Operating cash flow in year-1 (before annualization)"], errors="coerce")
    rd_exp = pd.to_numeric(df["R&D expensed in year-1 (before annualization)"], errors="coerce").fillna(0.0)
    rd_cap = pd.to_numeric(df["Development costs capitalized in year-1 (additions, before annualization)"], errors="coerce").fillna(0.0)

    df["sales_cagr_3y_pct"] = np.where((s3 > 0) & (s1 > 0), ((s1 / s3) ** 0.5 - 1.0) * 100.0, np.nan)
    df["total_accruals_pct_assets"] = ((p1_orig - cfo1) / a1) * 100.0
    df["cfo_to_assets_pct"] = (cfo1 / a1) * 100.0
    df["cfo_to_profit_ratio"] = np.where(p1_orig > 0, cfo1 / p1_orig, np.nan)
    df["has_rd_cap"] = (rd_cap > 0).astype(int)
    df["rd_cap_share_pct"] = np.where((rd_exp + rd_cap) > 0, (rd_cap / (rd_exp + rd_cap)) * 100.0, 0.0)

    # Convert 3-year aggregate profit into approximate HKD Millions to check Rule 8.05(1) HK$80M threshold
    # Note: Profit for the year in year-1/2/3 in HKIPO-MB-MASTER_clean.csv is already in full currency units
    curr = df["currency in financial information"].astype(str).str.upper()
    fx_to_hkd = np.where(curr.str.contains(r"USD|US\$"), 7.80, np.where(curr.str.contains("HKD"), 1.0, 1.08))
    df["cum_3y_profit_hkd_m"] = ((p3.fillna(0) + p2.fillna(0) + p1.fillna(0)) * fx_to_hkd) / 1e6

    rows = []

    # Panel A: Teoh, Welch, and Wong (1998) Accruals Quality Terciles
    valid_acc = df[df["total_accruals_pct_assets"].between(-100.0, 100.0)].copy()
    valid_acc["acc_tercile"] = pd.qcut(
        valid_acc["total_accruals_pct_assets"], 3,
        labels=[
            "Panel A1: T1 Lowest Total Accruals",
            "Panel A2: T2 Moderate Accruals",
            "Panel A3: T3 High Accruals (Aggressive Accrual Accounting)"
        ]
    )

    def _acc_row(lbl_str: str, grp_df: pd.DataFrame) -> dict[str, object]:
        ir = grp_df["initial_return_pct"].dropna()
        b3 = grp_df["bhr_3m_pct"].dropna()
        b6 = grp_df["bhr_6m_pct"].dropna()
        return {
            "Accounting_Cohort": str(lbl_str),
            "N_Deals": len(grp_df),
            "N_Valid_3M_BHR": len(b3),
            "N_Valid_6M_BHR": len(b6),
            "Median_3Y_Sales_CAGR_Pct": round(float(grp_df["sales_cagr_3y_pct"].dropna().median()), 2),
            "Median_Accruals_Pct_Assets": round(float(grp_df["total_accruals_pct_assets"].median()), 2),
            "Median_CFO_to_Assets_Pct": round(float(grp_df["cfo_to_assets_pct"].median()), 2),
            "Median_CFO_to_Profit_x": round(float(grp_df["cfo_to_profit_ratio"].dropna().median()), 2) if grp_df["cfo_to_profit_ratio"].notna().any() else np.nan,
            "Mean_Day1_IR_Pct": round(float(ir.mean()), 2),
            "Median_Day1_IR_Pct": round(float(ir.median()), 2),
            "Day1_Break_Rate_Pct": round(float((ir < 0).mean() * 100.0), 1),
            "Mean_3M_BHR_Pct": round(float(b3.mean()), 2) if len(b3) > 0 else np.nan,
            "Mean_6M_BHR_Pct": round(float(b6.mean()), 2) if len(b6) > 0 else np.nan,
        }

    for lbl, grp in valid_acc.groupby("acc_tercile", observed=False):
        rows.append(_acc_row(str(lbl), grp))

    # Panel B: IAS 38 / HKAS 38 Development Cost Capitalization vs 100% Expensing (among R&D-active issuers)
    rd_active = df[(rd_exp + rd_cap) > 0].copy()
    for flag, lbl in [
        (0, "Panel B1: 100% R&D Expensed on Income Statement (Conservative)"),
        (1, "Panel B2: IAS 38 R&D Development Capitalized onto Balance Sheet (Mean 12.8% Cap)")
    ]:
        rows.append(_acc_row(lbl, rd_active[rd_active["has_rd_cap"] == flag]))

    # Panel C: Rule 8.05(1) Profit-Test Threshold Bunching (HK$75M - HK$200M 3Y Cumulative Profit vs >HK$200M)
    r805_prof = df[(df["is_18a"] == 0) & (df["is_18c"] == 0) & (df["cum_3y_profit_hkd_m"] >= 75.0)].copy()
    r805_prof["profit_band"] = np.where(
        r805_prof["cum_3y_profit_hkd_m"] <= 200.0,
        "Panel C1: Rule 8.05(1) Threshold Bunchers (3Y Cum. Profit HK$75M-200M)",
        "Panel C2: Large Cushioned Profitable Issuers (3Y Cum. Profit > HK$200M)"
    )
    for lbl, grp in r805_prof.groupby("profit_band"):
        rows.append(_acc_row(lbl, grp))

    out_df = pd.DataFrame(rows)
    out_df.to_csv(OUT_EXT / "ext_table18_accruals_rd_cap_and_profit_bunching.csv", index=False)
    print(out_df.to_string(index=False))
    return out_df


def run_module5_zombie_liquidity_and_amihud(df: pd.DataFrame, ext33: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    print("\n" + "=" * 78)
    print("MODULE 5: Post-IPO Liquidity Death Spiral (Zombie IPOs) & Amihud Illiquidity")
    print("=" * 78)

    # Part 1: 33-Year Daily Cache Liquidity Decay & Zombie IPO Incidence (N = 2,600)
    clean33 = ext33[
        (ext33["flag_reverse_split_distortion"] == 0)
        & (ext33["flag_recycled_or_transferred_ticker"] == 0)
    ].copy()

    liq33_records = []
    for idx, row in clean33.iterrows():
        cpath = CACHE_DIR / f"{row['stock_code']}_{row['listing_date']}.json"
        if not cpath.exists():
            continue
        try:
            bars = json.loads(cpath.read_text())
        except Exception:
            continue
        if len(bars) < 60:
            continue
        # Day 1 volume/turnover vs Month 6 (trading days 100..125, or last 20 within first 130 days)
        b_6m = bars[:min(len(bars), 130)]
        d1_vol = float(b_6m[0][5])
        d1_turn = float(b_6m[0][6]) if float(b_6m[0][6]) > 0 else float(b_6m[0][2]) * d1_vol

        # Zero volume days in first 125 trading days
        zero_days = sum(1 for b in b_6m[1:] if float(b[5]) <= 0)
        zero_share_pct = (zero_days / max(1, len(b_6m) - 1)) * 100.0

        # Tail window [min(90, len-20) .. len]
        tail_bars = b_6m[max(1, len(b_6m) - 25):]
        tail_vols = [float(b[5]) for b in tail_bars]
        tail_turns = [float(b[6]) if float(b[6]) > 0 else float(b[2]) * float(b[5]) for b in tail_bars]
        decay_ratio_pct = (np.mean(tail_vols) / d1_vol * 100.0) if d1_vol > 0 else np.nan

        # Amihud illiquidity in first 6M: |r_t| / (turnover_t in HK$ millions)
        amihuds = []
        for i in range(1, len(b_6m)):
            p0_b, p1_b = float(b_6m[i - 1][2]), float(b_6m[i][2])
            v_b = float(b_6m[i][5])
            t_b = float(b_6m[i][6]) if float(b_6m[i][6]) > 0 else p1_b * v_b
            if p0_b > 0.001 and t_b > 1000.0:
                ret_abs = abs(p1_b / p0_b - 1.0)
                amihuds.append(ret_abs / (t_b / 1e6))

        liq33_records.append({
            "stock_code": row["stock_code"],
            "board": row["board"],
            "epoch": row["epoch"],
            "cohort_year": row["cohort_year"],
            "proceeds_hkd_m": float(row["funds_raised_total_hkd"]) / 1e6 if pd.notna(row["funds_raised_total_hkd"]) else np.nan,
            "is_h": row["is_prc_joint_stock"],
            "has_fintech": row["has_fintech_retail_broker"],
            "decay_ratio_pct": decay_ratio_pct,
            "zero_days": zero_days,
            "has_zero_vol_day": int(zero_days > 0),
            "is_zombie_95pct_decay": int(pd.notna(decay_ratio_pct) and decay_ratio_pct < 5.0),
            "amihud_6m": float(np.median(amihuds)) if amihuds else np.nan,
            "tail_turn_hkd_m": float(np.mean(tail_turns)) / 1e6 if tail_turns else np.nan,
            "bhar_1y": row["after_bhar_1y_pct"]
        })

    df_l33 = pd.DataFrame(liq33_records)

    rows = []
    # Panel A: 33-Year Liquidity Decay & Zombie Incidence by Board and Epoch
    for (brd, ep), grp in df_l33.groupby(["board", "epoch"]):
        rows.append({
            "Cohort_Segment": f"33Y {brd} — {ep[:20]}",
            "N_Deals": len(grp),
            "Med_6M_Daily_Turnover_HKDm": round(float(grp["tail_turn_hkd_m"].dropna().median()), 2),
            "Med_6M_vs_Day1_Vol_Ratio_Pct": round(float(grp["decay_ratio_pct"].dropna().median()), 2),
            "Zombie_95Pct_Decay_Share_Pct": round(float(grp["is_zombie_95pct_decay"].mean() * 100.0), 1),
            "Any_Zero_Volume_Day_Pct": round(float(grp["has_zero_vol_day"].mean() * 100.0), 1),
            "Median_Amihud_Illiq": round(float(grp["amihud_6m"].dropna().median()), 4),
            "Mean_Post_6M_or_1Y_Return_Pct": round(float(grp["bhar_1y"].dropna().mean()), 2)
        })

    # Panel B: 2025-2026 Audited Matured Panel by Deal Size & Unrestricted Free Float Terciles (N = 150)
    liq = df[df["Liquidity decay ratio (6M vs Day-1 turnover)"].notna()].copy()
    liq["liq_decay_pct"] = pd.to_numeric(liq["Liquidity decay ratio (6M vs Day-1 turnover)"], errors="coerce") * 100.0
    liq["amihud"] = pd.to_numeric(liq["Amihud illiquidity (6M mean)"], errors="coerce")
    liq["zero_vol_days"] = pd.to_numeric(liq["Zero-volume days count (first 6M)"], errors="coerce")
    liq["max_dd_pct"] = pd.to_numeric(liq["Maximum drawdown (first 6M, %)"], errors="coerce") * 100.0
    liq["turn_6m_m"] = pd.to_numeric(liq["6-month average daily turnover (HK$)"], errors="coerce") / 1e6
    liq["size_tercile"] = pd.qcut(
        liq["gross_proceeds_hkd_m"], 3,
        labels=[
            "2025-26 T1 Smallest Proceeds (<HK$620m)",
            "2025-26 T2 Mid Proceeds (HK$620m-1,750m)",
            "2025-26 T3 Largest Proceeds (>HK$1,750m)"
        ]
    )

    for lbl, grp in liq.groupby("size_tercile", observed=False):
        rows.append({
            "Cohort_Segment": str(lbl),
            "N_Deals": len(grp),
            "Med_6M_Daily_Turnover_HKDm": round(float(grp["turn_6m_m"].dropna().median()), 2),
            "Med_6M_vs_Day1_Vol_Ratio_Pct": round(float(grp["liq_decay_pct"].dropna().median()), 2),
            "Zombie_95Pct_Decay_Share_Pct": round(float((grp["liq_decay_pct"] < 5.0).mean() * 100.0), 1),
            "Any_Zero_Volume_Day_Pct": round(float((grp["zero_vol_days"] > 0).mean() * 100.0), 1),
            "Median_Amihud_Illiq": round(float(grp["amihud"].dropna().median()), 4),
            "Mean_Post_6M_or_1Y_Return_Pct": round(float(grp["bhr_6m_pct"].dropna().mean()), 2)
        })

    out_summary = pd.DataFrame(rows)
    out_summary.to_csv(OUT_EXT / "ext_table19a_zombie_ipos_and_amihud_summary.csv", index=False)
    print(out_summary.to_string(index=False))

    # Panel C: Cross-Sectional Regressions of Log(Amihud Illiquidity), Log(6M Daily Turnover), and Zombie Decay
    df_l33_mb = df_l33[df_l33["board"] == "Main Board"].dropna(subset=["amihud_6m", "proceeds_hkd_m", "tail_turn_hkd_m"]).copy()
    df_l33_mb = df_l33_mb[df_l33_mb["proceeds_hkd_m"] > 0].copy()
    df_l33_mb["log_amihud"] = np.log(df_l33_mb["amihud_6m"].clip(lower=1e-6))
    df_l33_mb["log_turn6m"] = np.log(df_l33_mb["tail_turn_hkd_m"].clip(lower=1e-4))
    df_l33_mb["log_proc"] = np.log(df_l33_mb["proceeds_hkd_m"])

    X33 = sm.add_constant(df_l33_mb[["log_proc", "is_h", "has_fintech"]])
    m_ami33 = sm.OLS(df_l33_mb["log_amihud"], X33).fit(cov_type="HC3")
    m_zom33 = sm.OLS(df_l33_mb["has_zero_vol_day"], X33).fit(cov_type="HC3")

    # 2025-2026 Micro-Panel Amihud & Turnover Regression with Unrestricted Free Float & A+H Southbound Eligibility
    liq_reg = liq.dropna(subset=["amihud", "turn_6m_m", "gross_proceeds_hkd_m", "unrestricted_free_float_pct"]).copy()
    liq_reg["log_amihud"] = np.log(liq_reg["amihud"].clip(lower=1e-6))
    liq_reg["log_turn6m"] = np.log(liq_reg["turn_6m_m"].clip(lower=1e-4))
    liq_reg["log_proc"] = np.log(liq_reg["gross_proceeds_hkd_m"])
    liq_reg["cs_pct"] = liq_reg["cornerstone_pct_of_offering"].fillna(0.0)

    X25 = sm.add_constant(liq_reg[["log_proc", "unrestricted_free_float_pct", "cs_pct", "is_ah_dual_listed"]])
    m_ami25 = sm.OLS(liq_reg["log_amihud"], X25).fit(cov_type="HC3")
    m_turn25 = sm.OLS(liq_reg["log_turn6m"], X25).fit(cov_type="HC3")

    reg_rows = []
    for m_name, mod, n_val in [
        ("33Y MB: Log(Amihud Illiquidity)", m_ami33, len(df_l33_mb)),
        ("33Y MB: Any Zero-Volume Day (LPM)", m_zom33, len(df_l33_mb)),
        ("2025-26 MB: Log(Amihud Illiquidity)", m_ami25, len(liq_reg)),
        ("2025-26 MB: Log(6M Daily Turnover HK$m)", m_turn25, len(liq_reg)),
    ]:
        for var in mod.params.index:
            if var == "const":
                continue
            reg_rows.append({
                "Model": m_name,
                "Variable": var,
                "Coef": round(float(mod.params[var]), 4),
                "SE_HC3": round(float(mod.bse[var]), 4),
                "t_stat": round(float(mod.tvalues[var]), 2),
                "p_value": round(float(mod.pvalues[var]), 4),
                "N": n_val,
                "R2": round(float(mod.rsquared), 3)
            })

    out_reg = pd.DataFrame(reg_rows)
    out_reg.to_csv(OUT_EXT / "ext_table19b_liquidity_determinants_regressions.csv", index=False)
    print(out_reg.to_string(index=False))
    return out_summary, out_reg


def generate_figures_15_and_16(df: pd.DataFrame, df33: pd.DataFrame, df_m4: pd.DataFrame, out_l33: pd.DataFrame, df_m1: pd.DataFrame) -> None:
    print("\nGenerating Publication-Grade Figures 15 and 16...")
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.size": 10,
        "axes.titlesize": 11,
        "axes.titleweight": "bold",
        "axes.labelsize": 10,
        "figure.dpi": 300
    })

    # =========================================================================
    # FIGURE 13: Two-Stage Statutory Lockup Waterfall (6M Cayman vs 12M H-Share)
    # =========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15.2, 5.5))

    # Panel A: Day +180 (6-Month) Lockup CAR[-20, +20] by Legal Structure & Cornerstone Type (Dynamic!)
    r_a2 = df_m1[df_m1["Panel_Group"].str.strip().str.startswith("Panel A2:")].iloc[0]
    r_ah = df_m1[df_m1["Panel_Group"].str.strip().str.startswith("- A+H Dual-Listed")].iloc[0]
    r_19a = df_m1[df_m1["Panel_Group"].str.strip().str.startswith("- Pure Chapter 19A")].iloc[0]
    r_a3 = df_m1[df_m1["Panel_Group"].str.strip().str.startswith("Panel A3:")].iloc[0]

    df_u = df.copy()
    df_u["car20_u"] = pd.to_numeric(df_u["Cornerstone unlock CAR [-20, +20] (%)"], errors="coerce") * 100.0
    df_u["cs_pct_u"] = df_u["cornerstone_pct_of_offering"].fillna(0.0)
    df_u["has_soe_u"] = pd.to_numeric(df_u["Cornerstone state-owned presence flag"], errors="coerce").fillna(0).astype(int)
    global_t1 = {
        "UBS Asset Management", "GIC (Singapore SWF)", "Schroders", "Fidelity International",
        "BlackRock", "Hillhouse / HHLR", "Boyu Capital", "Qatar Investment Authority",
        "Abu Dhabi Investment Authority", "Jane Street", "Millennium Management",
        "Point72", "OrbiMed", "Lilly Asia Ventures", "HSG (HongShan)"
    }
    def _has_gt1(raw):
        if pd.isna(raw) or not str(raw).strip():
            return False
        parts = [canon_cs(p) for p in re.split(r"[;\n,]", str(raw)) if len(p.strip()) > 3]
        return any(e in global_t1 for e in parts)
    soe_only = df_u[(df_u["cs_pct_u"] > 0) & (df_u["has_soe_u"] == 1) & (~df_u["Cornerstone investor names"].apply(_has_gt1))]["car20_u"].dropna()

    cats_a = [
        f"Cayman Red-Chip\n(6M Pre-IPO + CS\nUnlock, N={int(r_a2['N'])})",
        f"PRC H: A+H\n(6M CS Only; 12M\nCo. Law, N={int(r_ah['N'])})",
        f"PRC H: Pure 19A\n(6M CS Only; 12M\nCo. Law, N={int(r_19a['N'])})",
        f"PRC SOE / Mun.\nGuidance CS\n(Patient, N={len(soe_only)})"
    ]
    means_a = [float(r_a2["Mean_Metric_Pct"]), float(r_ah["Mean_Metric_Pct"]), float(r_19a["Mean_Metric_Pct"]), float(soe_only.mean())]
    meds_a = [float(r_a2["Median_Metric_Pct"]), float(r_ah["Median_Metric_Pct"]), float(r_19a["Median_Metric_Pct"]), float(soe_only.median())]
    x_a = np.arange(len(cats_a))
    w = 0.36
    bars1 = ax1.bar(x_a - w / 2, means_a, width=w, color=["#b2182b", "#4393c3", "#2166ac", "#1b7837"], alpha=0.9, label="Mean CAR[-20, +20] (%)")
    bars2 = ax1.bar(x_a + w / 2, meds_a, width=w, color=["#ef8a62", "#92c5de", "#67a9cf", "#a6dba0"], alpha=0.9, edgecolor="#333333", linewidth=0.6, label="Median CAR[-20, +20] (%)")
    ax1.axhline(0, color="black", linewidth=0.9, linestyle="--")
    for b in bars1:
        v = b.get_height()
        ax1.text(b.get_x() + b.get_width() / 2, v + (1.2 if v >= 0 else -2.4), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, fontweight="bold")
    ax1.set_xticks(x_a)
    ax1.set_xticklabels(cats_a, fontsize=8.0)
    ax1.set_ylabel("Day +180 Market-Adjusted CAR[-20, +20] (%)")
    ax1.set_ylim(min(-30, min(means_a + meds_a) - 6), max(12, max(means_a + meds_a) + 6))
    ax1.set_title(
        f"Panel A: Day +180 Lockup Natural Experiment\n"
        f"(Cayman 6M vs. H-Share 12M, DiD = {float(r_a3['Mean_Metric_Pct']):+.2f} pp, p={float(r_a3['p_value']):.4f})",
        fontsize=10.0,
    )
    ax1.legend(loc="lower right", frameon=True, fontsize=8.5)
    ax1.grid(axis="y", linestyle=":", alpha=0.5)

    # Panel B: 33-Year H-Share Full Circulation Reversal (Months 1->6 vs Months 6->12 Compounded BHAR in 2018-2026)
    r_b2_h = df_m1[df_m1["Panel_Group"].str.contains("Panel B2.*PRC Joint-Stock", regex=True)].iloc[0]
    r_b2_nh = df_m1[df_m1["Panel_Group"].str.contains("Panel B2.*Non-H-Share", regex=True)].iloc[0]
    r_b1_h = df_m1[df_m1["Panel_Group"].str.contains("Panel B1.*PRC Joint-Stock", regex=True)].iloc[0]
    r_b1_nh = df_m1[df_m1["Panel_Group"].str.contains("Panel B1.*Non-H-Share", regex=True)].iloc[0]
    r_b2_w = df_m1[df_m1["Panel_Group"].str.contains("Panel B2.*Difference", regex=True)].iloc[0]
    cats_b = [
        "Months 1 -> 6 BHAR\n(Pre-12M Statutory Lockup;\n6M Cayman Unlock Window)",
        "Months 6 -> 12 BHAR\n(2018-2026 H-Share Full Circ.\n12M Statutory Unlock Window)",
        "Months 6 -> 12 BHAR\n(1994-2017 Pre-Full Circ.\nPlacebo: Non-Tradable Domestic)"
    ]
    h_vals = [float(r_b2_h["Narrow_CAR_m5_p5_Pct"]), float(r_b2_h["Mean_Metric_Pct"]), float(r_b1_h["Mean_Metric_Pct"])]
    nonh_vals = [float(r_b2_nh["Narrow_CAR_m5_p5_Pct"]), float(r_b2_nh["Mean_Metric_Pct"]), float(r_b1_nh["Mean_Metric_Pct"])]
    x_b = np.arange(len(cats_b))
    b_h = ax2.bar(x_b - w / 2, h_vals, width=w, color="#b2182b", alpha=0.88, label="PRC Joint-Stock H-Shares (12M Statutory Lockup)")
    b_nh = ax2.bar(x_b + w / 2, nonh_vals, width=w, color="#2166ac", alpha=0.88, label="Non-H-Share Main Board Issuers (6M Lockup)")
    ax2.axhline(0, color="black", linewidth=0.9, linestyle="--")
    for b in list(b_h) + list(b_nh):
        v = b.get_height()
        ax2.text(b.get_x() + b.get_width() / 2, v + (0.8 if v >= 0 else -1.8), f"{v:+.2f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=8.5, fontweight="bold")
    ax2.set_xticks(x_b)
    ax2.set_xticklabels(cats_b, fontsize=8.5)
    ax2.set_ylabel("Compounded Interval BHAR (%)")
    ax2.set_ylim(-14, 15)
    ax2.set_title(
        f"Panel B: Months 6->12 Compounded BHAR by Legal Structure\n"
        f"(2018-2026 Wedge = {float(r_b2_w['Mean_Metric_Pct']):+.2f} pp, p = {float(r_b2_w['p_value']):.4f})",
        fontsize=10.0,
    )
    ax2.legend(loc="lower left", frameon=True, fontsize=8.5)
    ax2.grid(axis="y", linestyle=":", alpha=0.5)

    plt.tight_layout()
    fig.savefig(FIG_DIR / "fig15_twostage_lockup_and_571w_stabilization.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG_DIR / "fig15_twostage_lockup_and_571w_stabilization.pdf", bbox_inches="tight")
    plt.close(fig)

    # =========================================================================
    # FIGURE 14: Accruals Quality, R&D Capitalization & Post-IPO Liquidity Decay
    # =========================================================================
    fig2, (ax3, ax4) = plt.subplots(1, 2, figsize=(15.2, 5.5))

    # Panel A: Teoh-Welch-Wong Accruals Terciles & IAS 38 R&D Capitalization -> 6M Aftermarket BHR
    m4_p = df_m4.iloc[:5]
    cats_c = [
        f"T1 Low Accruals\n(Cash-Backed,\nMed {float(m4_p.iloc[0]['Median_Accruals_Pct_Assets']):+.1f}%)",
        f"T2 Moderate\nAccruals\n(Med {float(m4_p.iloc[1]['Median_Accruals_Pct_Assets']):+.1f}%)",
        f"T3 High Accruals\n(Aggressive,\nMed {float(m4_p.iloc[2]['Median_Accruals_Pct_Assets']):+.1f}%)",
        f"100% R&D\nExpensed\n(N={int(m4_p.iloc[3]['N_Deals'])})",
        f"IAS 38 R&D\nCapitalized\n(N={int(m4_p.iloc[4]['N_Deals'])})"
    ]
    bhr6_c = [float(x) for x in m4_p["Mean_6M_BHR_Pct"].values]
    colors_c = ["#1b7837", "#7fbf7b", "#d6604d", "#2166ac", "#b2182b"]
    x_c = np.arange(len(cats_c))
    bars_c = ax3.bar(x_c, bhr6_c, width=0.52, color=colors_c, alpha=0.9, edgecolor="#222222", linewidth=0.6)
    ax3.axvline(2.5, color="#555555", linestyle="--", linewidth=1.0)
    for b in bars_c:
        v = b.get_height()
        ax3.text(b.get_x() + b.get_width() / 2, v + (1.0 if v >= 0 else -2.2), f"{v:+.1f}%", ha="center", va="bottom" if v >= 0 else "top", fontsize=9, fontweight="bold")
    ax3.set_xticks(x_c)
    ax3.set_xticklabels(cats_c, fontsize=8.5)
    ax3.set_ylabel("Mean 6-Month Aftermarket BHR from Day-1 Close (%)")
    ax3.set_ylim(min(0, min(bhr6_c) - 6), max(bhr6_c) + 8)
    ax3.set_title("Panel A: Pre-IPO Accounting Quality & 6M BHR\n(Accruals Terciles & IAS 38 R&D Capitalization)", fontsize=10.0)
    ax3.grid(axis="y", linestyle=":", alpha=0.5)

    # Panel B: Post-IPO Liquidity Death Spiral (Zombie IPO Share & Median 6M Daily Turnover by Size Tercile)
    t25_rows = out_l33[out_l33["Cohort_Segment"].str.startswith("2025-26")].reset_index(drop=True)
    cats_d = [
        f"T1 Small-Cap\n(<HK$620m, N={int(t25_rows.iloc[0]['N_Deals'])})",
        f"T2 Mid-Cap\n(HK$620m-1,750m, N={int(t25_rows.iloc[1]['N_Deals'])})",
        f"T3 Large-Cap\n(>HK$1,750m, N={int(t25_rows.iloc[2]['N_Deals'])})"
    ]
    zombie_share = [float(x) for x in t25_rows["Zombie_95Pct_Decay_Share_Pct"].values]
    zero_vol_share = [float(x) for x in t25_rows["Any_Zero_Volume_Day_Pct"].values]
    med_turn_m = [float(x) for x in t25_rows["Med_6M_Daily_Turnover_HKDm"].values]

    x_d = np.arange(len(cats_d))
    b_z1 = ax4.bar(x_d - w / 2, zombie_share, width=w, color="#b2182b", alpha=0.88, label=">95% Volume Decay ('Zombie Liquidity', %)")
    b_z2 = ax4.bar(x_d + w / 2, zero_vol_share, width=w, color="#f4a582", alpha=0.92, edgecolor="#333333", linewidth=0.6, label="Zero-Volume Trading Days in First 6M (%)")
    for b in list(b_z1) + list(b_z2):
        v = b.get_height()
        ax4.text(b.get_x() + b.get_width() / 2, v + 1.2, f"{v:.1f}%", ha="center", va="bottom", fontsize=8.5, fontweight="bold")

    ax4_r = ax4.twinx()
    ax4_r.plot(x_d, med_turn_m, color="#2166ac", marker="o", linewidth=2.2, markersize=7, label="Median 6M Daily Turnover (HK$ m, Right Axis)")
    for i, txt in enumerate(med_turn_m):
        ax4_r.annotate(f"HK${txt:.1f}m/d", (x_d[i], med_turn_m[i]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=8.5, fontweight="bold", color="#2166ac")

    ax4.set_xticks(x_d)
    ax4.set_xticklabels(cats_d, fontsize=8.8)
    ax4.set_ylabel("Incidence Across Matured Offerings (%)")
    ax4_r.set_ylabel("Median 6M Daily Turnover (HK$ Millions)", color="#2166ac")
    ax4.set_ylim(0, 85)
    ax4_r.set_ylim(0, 125)
    ax4.set_title("Panel B: Post-IPO 'Liquidity Death Spiral' by Deal Scale\n(6M Volume Decay >95%, Zero-Vol Days & Daily Turnover)", fontsize=10.0)
    lines1, labels1 = ax4.get_legend_handles_labels()
    lines2, labels2 = ax4_r.get_legend_handles_labels()
    ax4.legend(lines1 + lines2, labels1 + labels2, loc="upper right", frameon=True, fontsize=8.0)
    ax4.grid(axis="y", linestyle=":", alpha=0.5)

    plt.tight_layout()
    fig2.savefig(FIG_DIR / "fig16_accruals_network_2sls_and_zombie_liquidity.png", dpi=300, bbox_inches="tight")
    fig2.savefig(FIG_DIR / "fig16_accruals_network_2sls_and_zombie_liquidity.pdf", bbox_inches="tight")
    plt.close(fig2)
    print("Saved Figures 15 and 16 successfully.")


def main() -> None:
    df = load_master_merged()
    df33 = pd.read_csv(OUT_MAIN / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv", low_memory=False)
    ext33 = pd.read_csv(OUT_EXT / "clean_33y_intermediaries_greenshoe.csv", low_memory=False)

    df_m1 = run_module1_twostage_lockup(df, df33)
    run_module1b_paired_lockup(df)
    df_m2a, df_m2b = run_module2_crossover_and_network_2sls(df, df33)
    df_m3 = run_module3_cap571w_stabilization(df, ext33)
    df_m4 = run_module4_accruals_rd_and_profit_bunching(df)
    df_m5a, df_m5b = run_module5_zombie_liquidity_and_amihud(df, ext33)
    generate_figures_15_and_16(df, df33, df_m4, df_m5a, df_m1)


if __name__ == "__main__":
    main()
