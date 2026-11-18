#!/usr/bin/env python3
"""
33-Year Deal Characteristics & Modern Complete-Case Financial Fundamentals Regressions.

Repairs two peer-review audit issues in the legacy fundamentals script:
1. Replaces `cov_type="HC1"` (previously mislabeled as `SE_HC3`) with genuine
   MacKinnon-White `cov_type="HC3"` AND listing-year-month clustered inference (`G` clusters).
2. Separates the Full 33-Year Deal-Characteristics Cross-Section (1994-2026Q3, consistent N)
   from the Modern Audited Financial-Fundamentals Cross-Section (2018-2026Q3, where balance-sheet
   and income-statement coverage exceeds 95%, fixed on one complete-case estimation sample).
"""

from __future__ import annotations

from pathlib import Path
import numpy as np
import pandas as pd
import statsmodels.api as sm

REPO_ROOT = Path(__file__).resolve().parent.parent
MASTER_CSV = REPO_ROOT / "analysis" / "out" / "overview_1994_2026" / "hkipo_33y_master_panel_1994_2026_tier1_complete.csv"
OUT_CSV = REPO_ROOT / "analysis" / "out" / "overview_1994_2026" / "table_33y_financial_fundamentals_regressions.csv"


def winsorize_nan_safe(s: pd.Series, lo: float = 0.01, hi: float = 0.99) -> pd.Series:
    valid = s.dropna()
    if len(valid) < 20:
        return s
    q_lo, q_hi = valid.quantile([lo, hi])
    return s.clip(lower=q_lo, upper=q_hi)


def run_fe_ols_hc3_and_clustered(
    df: pd.DataFrame,
    dep_var: str,
    x_vars: list[str],
    fe_col: str = "cohort_year",
    cluster_col: str = "listing_ym",
    model_name: str = "",
    sample_label: str = "",
) -> pd.DataFrame:
    cols = list(dict.fromkeys([dep_var] + x_vars + [fe_col, cluster_col]))
    sub = df[cols].replace([np.inf, -np.inf], np.nan).dropna().copy()

    fe_dummies = pd.get_dummies(sub[fe_col].astype(int), prefix="yr", drop_first=True, dtype=float)
    X = pd.concat([sub[x_vars].astype(float), fe_dummies], axis=1)
    X = sm.add_constant(X, has_constant="add")
    y = sub[dep_var].astype(float)

    res_hc3 = sm.OLS(y, X).fit(cov_type="HC3")
    res_cl = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": sub[cluster_col]})
    n_clusters = int(sub[cluster_col].nunique())

    rows = []
    for var in x_vars:
        coef = float(res_hc3.params[var])
        se_hc3 = float(res_hc3.bse[var])
        t_hc3 = float(res_hc3.tvalues[var])
        p_hc3 = float(res_hc3.pvalues[var])
        se_cl = float(res_cl.bse[var])
        t_cl = float(res_cl.tvalues[var])
        p_cl = float(res_cl.pvalues[var])
        stars_hc3 = "***" if p_hc3 < 0.01 else ("**" if p_hc3 < 0.05 else ("*" if p_hc3 < 0.10 else ""))
        stars_cl = "***" if p_cl < 0.01 else ("**" if p_cl < 0.05 else ("*" if p_cl < 0.10 else ""))
        rows.append({
            "Model": model_name,
            "Sample": sample_label,
            "Dep_Var": dep_var,
            "Variable": var,
            "Coef": round(coef, 4),
            "SE_HC3": round(se_hc3, 4),
            "t_HC3": round(t_hc3, 2),
            "p_HC3": round(p_hc3, 4),
            "Sig_HC3": stars_hc3,
            "SE_MonthCluster": round(se_cl, 4),
            "t_MonthCluster": round(t_cl, 2),
            "p_MonthCluster": round(p_cl, 4),
            "Sig_MonthCluster": stars_cl,
            "N": int(res_hc3.nobs),
            "Clusters_YM": n_clusters,
            "R2": round(float(res_hc3.rsquared), 4),
            "Adj_R2": round(float(res_hc3.rsquared_adj), 4),
            "Year_FE": "Yes",
        })
    return pd.DataFrame(rows)


def main() -> None:
    df = pd.read_csv(MASTER_CSV, low_memory=False)
    # Clean analytical universe: exclude recycled tickers and unverified reverse-split distortions
    clean_mask = (df["flag_recycled_or_transferred_ticker"].fillna(0) == 0) & (~df["flag_reverse_split_distortion"].fillna(False))
    df = df[clean_mask].copy()

    df["listing_ym"] = pd.to_datetime(df["listing_date"], errors="coerce").dt.to_period("M").astype(str)

    # Outcomes: log(1 + IR) (preferred for right-skewed IPO returns) and winsorized raw IR / 1Y BHAR
    ir_raw = pd.to_numeric(df["ir_close_pct"], errors="coerce")
    df["log_1p_ir"] = np.log1p((ir_raw / 100.0).clip(lower=-0.95)) * 100.0
    df["ir_close_w"] = winsorize_nan_safe(ir_raw)
    bhar_col = "after_bhar_1y_hsi_tr_pct" if "after_bhar_1y_hsi_tr_pct" in df.columns else "after_bhar_1y_pct"
    df["bhar_1y_w"] = winsorize_nan_safe(pd.to_numeric(df[bhar_col], errors="coerce"))

    # Deal & institutional characteristics (strictly preserving NaN — ZERO fillna(0) on missing disclosures)
    df["log_proceeds_hkdm"] = np.log(pd.to_numeric(df["funds_raised_total_hkd"], errors="coerce").where(lambda s: s > 0) / 1e6)
    df["log1p_retail_sub"] = np.log1p(pd.to_numeric(df["ext_retail_sub_ratio"], errors="coerce").clip(lower=0))
    df["is_gem"] = (df["board"] == "GEM").astype(float)
    df["is_prc_domicile"] = (df["ext_domicile"] == "PRC").astype(float)
    df["secondary_flag"] = pd.to_numeric(df["ext_secondary_sale_flag"], errors="coerce")
    df["has_cornerstone"] = pd.to_numeric(df["ext_has_cornerstone"], errors="coerce")

    # HKD-harmonized audited year-1 financials
    assets_hkd = pd.to_numeric(df["ext_total_assets_hkd"], errors="coerce")
    rev_hkd = pd.to_numeric(df["ext_revenue_yr1_hkd"], errors="coerce")
    np_hkd = pd.to_numeric(df["ext_net_profit_yr1_hkd"], errors="coerce")
    liab_hkd = pd.to_numeric(df["ext_total_liabilities_hkd"], errors="coerce")

    df["log_assets_hkdm"] = np.log(assets_hkd.where(assets_hkd > 0) / 1e6)
    df["log_revenue_hkdm"] = np.log(rev_hkd.where(rev_hkd > 0) / 1e6)
    df["profitable_yr1"] = np.where(np_hkd.notna(), (np_hkd > 0).astype(float), np.nan)
    df["roa_pct"] = winsorize_nan_safe(pd.Series(np.where(assets_hkd > 0, (np_hkd / assets_hkd) * 100.0, np.nan), index=df.index))
    df["leverage_pct"] = winsorize_nan_safe(
        pd.Series(np.where((assets_hkd > 0) & (liab_hkd >= 0), (liab_hkd / assets_hkd) * 100.0, np.nan), index=df.index)
    )

    all_res: list[pd.DataFrame] = []

    # Panel A: Full 33-Year Deal & Demand Cross-Section (1994-2026Q3, fixed complete-case sample)
    vars_33y_base = ["log_proceeds_hkdm", "is_gem", "is_prc_domicile"]
    all_res.append(
        run_fe_ols_hc3_and_clustered(
            df, "log_1p_ir", vars_33y_base, model_name="M1_33y_PrePricing_Deal", sample_label="1994-2026Q3 Full Clean Universe"
        )
    )
    all_res.append(
        run_fe_ols_hc3_and_clustered(
            df,
            "log_1p_ir",
            vars_33y_base + ["log1p_retail_sub"],
            model_name="M2_33y_With_Retail_Demand",
            sample_label="1994-2026Q3 Public-Tranche Verified",
        )
    )

    # Panel B: Modern Complete-Case Audited Financials Sample (2018-2026Q3, fixed consistent sample across M3-M4)
    mod_fin_cols = [
        "log_1p_ir",
        "log_assets_hkdm",
        "log_revenue_hkdm",
        "profitable_yr1",
        "roa_pct",
        "leverage_pct",
        "log_proceeds_hkdm",
        "has_cornerstone",
        "is_gem",
        "is_prc_domicile",
        "cohort_year",
        "listing_ym",
    ]
    df_mod_fixed = df[df["cohort_year"] >= 2018].dropna(subset=mod_fin_cols).copy()

    all_res.append(
        run_fe_ols_hc3_and_clustered(
            df_mod_fixed,
            "log_1p_ir",
            ["log_assets_hkdm", "profitable_yr1", "roa_pct", "leverage_pct", "log_proceeds_hkdm", "has_cornerstone", "is_gem", "is_prc_domicile"],
            model_name="M3_2018_2026_PrePricing_Fundamentals",
            sample_label="2018-2026Q3 Complete-Case Audited Financials",
        )
    )
    df_mod_sub = df_mod_fixed.dropna(subset=["log1p_retail_sub"]).copy()
    all_res.append(
        run_fe_ols_hc3_and_clustered(
            df_mod_sub,
            "log_1p_ir",
            ["log_assets_hkdm", "profitable_yr1", "roa_pct", "leverage_pct", "log_proceeds_hkdm", "has_cornerstone", "log1p_retail_sub", "is_gem", "is_prc_domicile"],
            model_name="M4_2018_2026_Fundamentals_Plus_Demand",
            sample_label="2018-2026Q3 Complete-Case + Demand",
        )
    )
    df_mod_bhar = df[df["cohort_year"] >= 2018].dropna(
        subset=["bhar_1y_w", "ir_close_w", "log_assets_hkdm", "profitable_yr1", "roa_pct", "leverage_pct", "log_proceeds_hkdm", "has_cornerstone", "is_gem", "cohort_year", "listing_ym"]
    ).copy()
    all_res.append(
        run_fe_ols_hc3_and_clustered(
            df_mod_bhar,
            "bhar_1y_w",
            ["ir_close_w", "log_assets_hkdm", "profitable_yr1", "roa_pct", "leverage_pct", "log_proceeds_hkdm", "has_cornerstone", "is_gem"],
            model_name="M5_2018_2026_1Y_BHAR_Reversal",
            sample_label="2018-2026Q3 Matured 1Y Complete-Case",
        )
    )

    out_df = pd.concat(all_res, ignore_index=True)
    out_df.to_csv(OUT_CSV, index=False)
    print(f"Saved true-HC3 & month-clustered regressions to: {OUT_CSV}")
    for mname, g in out_df.groupby("Model", sort=False):
        print(f"\n=== {mname} [{g['Sample'].iloc[0]}] (N={g['N'].iloc[0]}, Clusters={g['Clusters_YM'].iloc[0]}, R2={g['R2'].iloc[0]:.4f}) ===")
        print(g[["Variable", "Coef", "SE_HC3", "t_HC3", "Sig_HC3", "t_MonthCluster", "Sig_MonthCluster"]].to_string(index=False))


if __name__ == "__main__":
    main()
