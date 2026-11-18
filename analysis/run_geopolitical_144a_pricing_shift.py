#!/usr/bin/env python3
"""
run_geopolitical_144a_pricing_shift.py
======================================
Produces the unified empirical tables for Main Table 4 of the Overview Paper:
"Intermediary Handover, Global Rule 144A Retreat, and the Re-Anchoring of
Offer-Price Discovery (1994-2026Q3)".

Integrates:
- Repaired 33-year master panel (`hkipo_33y_master_panel_1994_2026_tier1_complete.csv`,
  including verified cornerstone prevalence, secondary vendor sales, bookbuilding
  range positions, and dividend-adjusted HSI-TR / size-matched 1Y BHARs)
- Intermediary & Rule 144A / greenshoe panel (`clean_33y_macro_144a_hibor_panel.csv`)

Outputs:
1. `analysis/out/overview_1994_2026/table4_panelA_5epoch_syndicate_and_144a.csv`
2. `analysis/out/overview_1994_2026/table4_panelB_geopolitical_pricing_regressions.csv`
"""

from __future__ import annotations

from pathlib import Path
from typing import Any
import numpy as np
import pandas as pd
import statsmodels.api as sm

REPO_ROOT = Path(__file__).resolve().parent.parent
OVERVIEW_DIR = REPO_ROOT / "analysis" / "out" / "overview_1994_2026"
EXT_DIR = REPO_ROOT / "analysis" / "out" / "overview_extensions"

MASTER_CSV = OVERVIEW_DIR / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
MACRO_144A_CSV = EXT_DIR / "clean_33y_macro_144a_hibor_panel.csv"

OUT_PANEL_A = OVERVIEW_DIR / "table4_panelA_5epoch_syndicate_and_144a.csv"
OUT_PANEL_B = OVERVIEW_DIR / "table4_panelB_geopolitical_pricing_regressions.csv"

EPOCH_ORDER = [
    "Epoch I (1994-1999)",
    "Epoch II (2000-2007)",
    "Epoch III (2008-2017)",
    "Epoch IV (2018-2022)",
    "Epoch V (2023-2026Q3)",
]


def winsorize_s(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    v = s.dropna()
    if len(v) < 20:
        return s
    q_lo, q_hi = v.quantile([lo, hi])
    return s.clip(lower=q_lo, upper=q_hi)


def fit_ols_hc3_cl(
    df: pd.DataFrame,
    dep: str,
    x_vars: list[str],
    fe_col: str | None,
    model_id: str,
    dep_label: str,
    sample_desc: str,
) -> list[dict[str, Any]]:
    need = list(dict.fromkeys([dep] + x_vars + (["listing_ym"] if "listing_ym" in df.columns else []) + ([fe_col] if fe_col else [])))
    sub = df[need].replace([np.inf, -np.inf], np.nan).dropna().copy()
    X_parts = [sub[x_vars].astype(float)]
    if fe_col:
        fe_d = pd.get_dummies(sub[fe_col].astype(str), prefix="fe", drop_first=True, dtype=float)
        X_parts.append(fe_d)
    X = sm.add_constant(pd.concat(X_parts, axis=1), has_constant="add")
    y = sub[dep].astype(float)

    m_hc3 = sm.OLS(y, X).fit(cov_type="HC3")
    m_cl = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": sub["listing_ym"]})
    g_cnt = int(sub["listing_ym"].nunique())

    rows = []
    for v in x_vars:
        p_h = float(m_hc3.pvalues[v])
        p_c = float(m_cl.pvalues[v])
        st_h = "***" if p_h < 0.01 else ("**" if p_h < 0.05 else ("*" if p_h < 0.10 else ""))
        st_c = "***" if p_c < 0.01 else ("**" if p_c < 0.05 else ("*" if p_c < 0.10 else ""))
        rows.append({
            "Model": model_id,
            "Sample": sample_desc,
            "Dep_Var": dep_label,
            "Variable": v,
            "Coef": round(float(m_hc3.params[v]), 4),
            "SE_HC3": round(float(m_hc3.bse[v]), 4),
            "t_HC3": round(float(m_hc3.tvalues[v]), 2),
            "Sig_HC3": st_h,
            "SE_MonthCluster": round(float(m_cl.bse[v]), 4),
            "t_MonthCluster": round(float(m_cl.tvalues[v]), 2),
            "Sig_MonthCluster": st_c,
            "N": int(m_hc3.nobs),
            "Clusters_YM": g_cnt,
            "R2": round(float(m_hc3.rsquared), 4),
            "Fixed_Effects": fe_col if fe_col else "None",
        })
    return rows


def main() -> None:
    print("=" * 80)
    print("Geopolitical Syndicate Handover, Rule 144A Retreat & Offer-Price Discovery")
    print("=" * 80)

    m_df = pd.read_csv(MASTER_CSV, low_memory=False)
    e_df = pd.read_csv(MACRO_144A_CSV, low_memory=False)

    keep_ext_cols = [
        "stock_code",
        "listing_date",
        "board",
        "has_bb_sponsor",
        "has_prc_sponsor",
        "bb_sponsor_share",
        "prc_sponsor_share",
        "has_bb_bookrunner",
        "has_prc_bookrunner",
        "bb_bookrunner_share",
        "prc_bookrunner_share",
        "is_big4_auditor",
        "gross_spread_clean_pct",
        "greenshoe_exercised_ratio",
        "greenshoe_regime",
        "has_rule_144a",
        "has_reg_s",
        "hsi_ret_sub_window_pct",
        "hsi_ret_pre30td_pct",
    ]
    merge_keys = ["stock_code", "listing_date", "board"]
    new_ext_cols = merge_keys + [c for c in keep_ext_cols if c not in m_df.columns and c not in merge_keys]
    e_sub = e_df[new_ext_cols].drop_duplicates(subset=merge_keys)
    df = m_df.merge(e_sub, on=merge_keys, how="left").copy()
    df["listing_ym"] = pd.to_datetime(df["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    # Main Board universe (gross for primary syndicate/deal structure; clean non-recycled for secondary returns)
    mb_all = df[df["board"] == "Main Board"].copy()
    clean_mask = (mb_all["flag_recycled_or_transferred_ticker"].fillna(0) == 0) & (~mb_all["flag_reverse_split_distortion"].fillna(False))

    # Panel A: 5-Epoch Syndicate, Rule 144A, Cornerstone & Bookbuilding Architecture on Main Board
    pa_rows: list[dict[str, Any]] = []
    slices = [(ep, mb_all[mb_all["epoch_5"] == ep]) for ep in EPOCH_ORDER]
    slices.append(("All Main Board (1994-2026Q3)", mb_all))

    for label, g in slices:
        sp_valid = g[g["lead_sponsor"].notna() | g["sponsors"].notna()]
        br_valid = g[g["has_bb_bookrunner"].notna()]
        r144_valid = g[g["has_rule_144a"].notna()]
        r144_big = r144_valid[pd.to_numeric(r144_valid["funds_raised_total_hkd"], errors="coerce") >= 1e9]
        cs_valid = g[g["ext_has_cornerstone"].notna()]
        cs_pos = g[pd.to_numeric(g["ext_cornerstone_pct"], errors="coerce") > 0]
        if len(cs_valid) < 0.5 * len(g):  # too few checked filings to state a market-wide rate
            cs_valid, cs_pos = g.iloc[0:0], g.iloc[0:0]
        sec_valid = g[g["ext_secondary_sale_flag"].notna()]
        rng_valid = g[g["ext_is_bookbuilding_range"].notna()]
        spr_valid = pd.to_numeric(g["gross_spread_clean_pct"], errors="coerce").dropna()
        gs_valid = pd.to_numeric(g["greenshoe_exercised_ratio"], errors="coerce").dropna()

        pa_rows.append({
            "Epoch": label,
            "N_MB_Deals": len(g),
            "US_EU_BulgeBracket_Sponsor_Pct": round(float(sp_valid["has_bb_sponsor"].mean() * 100.0), 1) if len(sp_valid) else np.nan,
            "PRC_Mainland_Sponsor_Pct": round(float(sp_valid["has_prc_sponsor"].mean() * 100.0), 1) if len(sp_valid) else np.nan,
            "US_EU_BulgeBracket_Bookrunner_Pct": round(float(br_valid["has_bb_bookrunner"].mean() * 100.0), 1) if len(br_valid) else np.nan,
            "Rule_144A_All_Pct": round(float(r144_valid["has_rule_144a"].mean() * 100.0), 1) if len(r144_valid) else np.nan,
            "Rule_144A_Deals_GE_HKD1B_Pct": round(float(r144_big["has_rule_144a"].mean() * 100.0), 1) if len(r144_big) else np.nan,
            "Cornerstone_Prevalence_Pct": round(float(cs_valid["ext_has_cornerstone"].mean() * 100.0), 1) if len(cs_valid) else np.nan,
            "Cornerstone_Cond_Median_Pct": round(float(pd.to_numeric(cs_pos["ext_cornerstone_pct"], errors="coerce").median()), 1) if len(cs_pos) else np.nan,
            "Secondary_Vendor_Sale_Pct": round(float(sec_valid["ext_secondary_sale_flag"].mean() * 100.0), 1) if len(sec_valid) else np.nan,
            "Bookbuilding_Range_Share_Pct": round(float(rng_valid["ext_is_bookbuilding_range"].mean() * 100.0), 1) if len(rng_valid) else np.nan,
            "Median_Gross_Spread_Pct": round(float(spr_valid.median()), 2) if len(spr_valid) else np.nan,
            "Greenshoe_Full_Exercise_Pct": round(float((gs_valid >= 0.95).mean() * 100.0), 1) if len(gs_valid) else np.nan,
        })

    pa_df = pd.DataFrame(pa_rows)
    pa_df.to_csv(OUT_PANEL_A, index=False)
    print("\n--- Main Table 4 Panel A: 5-Epoch Syndicate, Rule 144A & Bookbuilding Architecture ---")
    print(pa_df.to_string(index=False))

    # Panel B: Multivariate Synthesis Regressions
    mb = mb_all[clean_mask].copy()
    mb["log_proceeds_hkdm"] = np.log(pd.to_numeric(mb["funds_raised_total_hkd"], errors="coerce").where(lambda s: s > 0) / 1e6)
    mb["post_2023"] = (mb["cohort_year"] >= 2023).astype(float)
    mb["is_h_share"] = (mb["is_prc_joint_stock"] == 1).astype(float)
    mb["is_ah_dual"] = pd.to_numeric(mb["is_ah"], errors="coerce").fillna(0.0)
    mb["bb_sponsor"] = pd.to_numeric(mb["has_bb_sponsor"], errors="coerce")
    mb["prc_sponsor"] = pd.to_numeric(mb["has_prc_sponsor"], errors="coerce")
    mb["bb_bookrunner"] = pd.to_numeric(mb["has_bb_bookrunner"], errors="coerce")
    mb["rule_144a"] = pd.to_numeric(mb["has_rule_144a"], errors="coerce")
    mb["has_cs"] = pd.to_numeric(mb["ext_has_cornerstone"], errors="coerce")
    mb["big4_auditor"] = pd.to_numeric(mb["is_big4_auditor"], errors="coerce")
    mb["hsi_sub_ret"] = pd.to_numeric(mb["hsi_ret_sub_window_pct"], errors="coerce")
    mb["range_pos"] = pd.to_numeric(mb["ext_range_pos"], errors="coerce")

    ir_c = pd.to_numeric(mb["ir_close_pct"], errors="coerce")
    mb["log_1p_ir"] = np.log1p((ir_c / 100.0).clip(lower=-0.95)) * 100.0
    mb["abs_ir_w"] = winsorize_s(ir_c.abs())
    mb["day1_break"] = np.where(ir_c.notna(), (ir_c < 0).astype(float) * 100.0, np.nan)
    mb["bhar_1y_tr_w"] = winsorize_s(pd.to_numeric(mb["after_bhar_1y_hsi_tr_pct"], errors="coerce"))
    mb["bhar_1y_sm_w"] = winsorize_s(pd.to_numeric(mb["after_bhar_1y_size_matched_pct"], errors="coerce"))

    pb_rows: list[dict[str, Any]] = []

    # Model 1 & 2: Post-2023 Geopolitical Rule 144A Retreat & Wall St Syndicate Mediation (2018-2026Q3 Main Board)
    mod18 = mb[mb["cohort_year"] >= 2018].copy()
    mod18["rule_144a_pct"] = mod18["rule_144a"] * 100.0
    pb_rows.extend(
        fit_ols_hc3_cl(
            mod18,
            "rule_144a_pct",
            ["post_2023", "log_proceeds_hkdm", "is_h_share", "is_ah_dual"],
            None,
            "M1_Rule144A_Decoupling_Base",
            "Rule_144A_Tranche_Pct",
            "2018-2026Q3 Main Board",
        )
    )
    pb_rows.extend(
        fit_ols_hc3_cl(
            mod18,
            "rule_144a_pct",
            ["post_2023", "bb_bookrunner", "prc_sponsor", "log_proceeds_hkdm", "is_h_share", "is_ah_dual"],
            None,
            "M2_Rule144A_With_Syndicate",
            "Rule_144A_Tranche_Pct",
            "2018-2026Q3 Main Board",
        )
    )

    # Model 3: Offer-Price Position Within Filing Range (`ext_range_pos` in [0,1], Bookbuilt Main Board 2000-2026Q3)
    mb_rng = mb[(mb["cohort_year"] >= 2000) & (mb["ext_is_bookbuilding_range"] == 1)].copy()
    mb_rng["range_pos_pct"] = mb_rng["range_pos"] * 100.0
    pb_rows.extend(
        fit_ols_hc3_cl(
            mb_rng,
            "range_pos_pct",
            ["bb_sponsor", "prc_sponsor", "rule_144a", "has_cs", "hsi_sub_ret", "log_proceeds_hkdm"],
            "cohort_year",
            "M3_Offer_Range_Position",
            "Range_Position_0_to_100_Pct",
            "2000-2026Q3 Bookbuilt Main Board",
        )
    )

    # Model 4: Primary-Market Pricing Error / Day-1 Return Dispersion (`|IR_close|`, 2000-2026Q3 Main Board)
    mb_2000 = mb[mb["cohort_year"] >= 2000].copy()
    pb_rows.extend(
        fit_ols_hc3_cl(
            mb_2000,
            "abs_ir_w",
            ["bb_sponsor", "prc_sponsor", "rule_144a", "has_cs", "big4_auditor", "log_proceeds_hkdm"],
            "cohort_year",
            "M4_Day1_Abs_Pricing_Error",
            "Abs_Day1_IR_Pct_Winsor",
            "2000-2026Q3 Main Board",
        )
    )

    # Model 5: Post-IPO 1-Year Dividend-Adjusted HSI-TR BHAR (`bhar_1y_tr_w`, 2000-2026Q3 Matured Main Board)
    pb_rows.extend(
        fit_ols_hc3_cl(
            mb_2000,
            "bhar_1y_tr_w",
            ["bb_sponsor", "prc_sponsor", "rule_144a", "has_cs", "big4_auditor", "log_proceeds_hkdm"],
            "cohort_year",
            "M5_1Y_BHAR_HSI_TR",
            "Aftermarket_1Y_BHAR_HSI_TR_Pct",
            "2000-2026Q3 Matured Main Board",
        )
    )

    pb_df = pd.DataFrame(pb_rows)
    pb_df.to_csv(OUT_PANEL_B, index=False)
    print("\n--- Main Table 4 Panel B: Syndicate, Rule 144A & Price Discovery Regressions ---")
    for mid, g in pb_df.groupby("Model", sort=False):
        print(f"\n[{mid}] Dep={g['Dep_Var'].iloc[0]} | N={g['N'].iloc[0]} | Clusters={g['Clusters_YM'].iloc[0]} | R2={g['R2'].iloc[0]:.4f}")
        print(g[["Variable", "Coef", "SE_HC3", "t_HC3", "Sig_HC3", "t_MonthCluster", "Sig_MonthCluster"]].to_string(index=False))


if __name__ == "__main__":
    main()
