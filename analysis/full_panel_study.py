"""Full Multi-Year Panel Study (2025–2026, N = all stored Main Board IPOs).

Unlocks the complete stored Main Board panel across 2025–2026 (including pre-reform
2025Q1–Q2 and post-August 4, 2025 HKEX Allocation & Pricing Reform cohorts) and
the newly derived accounting, R&D, cash-flow and governance variables.

Outputs (analysis/out/full_panel/):
    table1_cohort_summary.md       Sample breakdown & core metrics across all stored quarters
    table2_reform_comparison.md    Pre- vs Post-Aug 2025 HKEX Reform comparison
    table3_panel_regressions.md    Multi-cohort OLS & Quarter-FE underpricing regressions
                                   with governance wedge, R&D intensity, and gross margin
"""
from __future__ import annotations

import numpy as np
import pandas as pd
import statsmodels.api as sm

from research_inputs import C, ROOT, load_panel, prepare_regression, select_period
from shared.reporting import to_markdown

OUT = ROOT / "analysis" / "out" / "full_panel"


def build_panel_frame(df: pd.DataFrame) -> pd.DataFrame:
    d = prepare_regression(df)
    d["post_reform"] = df["post_aug2025_reform"]
    d["gross_margin_y1"] = df.get("gross_margin_y1", np.nan)
    d["rd_intensity_y1"] = df.get("rd_intensity_y1", np.nan)
    d["cfo_to_assets_y1"] = df.get("cfo_to_assets_y1", np.nan)
    d["wedge"] = df.get("voting_cashflow_wedge", np.nan)
    d["leverage_y1"] = (
        df["total liability in year-1"] / df["total assets in year-1"].where(df["total assets in year-1"] > 0)
    )
    d["roa_y1"] = (
        df["Profit for the year in year-1"] / df["total assets in year-1"].where(df["total assets in year-1"] > 0)
    )
    return d


def summarize_by_cohort(df: pd.DataFrame, d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for cohort, part in df.groupby("cohort", observed=True):
        sub_d = d.loc[part.index]
        ir = part["ir"].dropna() * 100.0
        rows.append({
            "Cohort": str(cohort),
            "N": len(part),
            "Mean IR (%)": ir.mean(),
            "Median IR (%)": ir.median(),
            "Break Rate (%)": (ir < 0).mean() * 100.0,
            "Median Sub (x)": part[C["sub"]].median(),
            "Mean Cornerstone (%)": part[C["corner"]].mean() * 100.0,
            "VC/PE Backed (%)": part[C["vc"]].where(part[C["vc"]].isin([0, 1])).mean() * 100.0,
            "Mean Gross Margin (%)": sub_d["gross_margin_y1"].dropna().mean() * 100.0,
            "Mean Gov Wedge (pp)": sub_d["wedge"].dropna().mean() * 100.0,
        })
    return pd.DataFrame(rows)


def summarize_reform(df: pd.DataFrame, d: pd.DataFrame) -> pd.DataFrame:
    rows = []
    labels = {0.0: "Pre-Reform (Before 2025-08-04)", 1.0: "Post-Reform (On/After 2025-08-04)"}
    for flag in (0.0, 1.0):
        mask = df["post_aug2025_reform"] == flag
        part = df.loc[mask]
        sub_d = d.loc[mask]
        if part.empty:
            continue
        ir = part["ir"].dropna() * 100.0
        rows.append({
            "Regime": labels[flag],
            "N": len(part),
            "Mean IR (%)": ir.mean(),
            "Median IR (%)": ir.median(),
            "Std IR (%)": ir.std(),
            "Median Sub (x)": part[C["sub"]].median(),
            "Mean Cornerstone (%)": part[C["corner"]].mean() * 100.0,
            "Mean Free Float (%)": part[C["float"]].mean() * 100.0,
            "Mean R&D Intensity (%)": sub_d["rd_intensity_y1"].clip(upper=5.0).dropna().mean() * 100.0,
        })
    return pd.DataFrame(rows)


def run_panel_regressions(d: pd.DataFrame) -> pd.DataFrame:
    specs = [
        ("P1: Baseline (2025-2026)", ["lage", "lproc", "ah", "vc", "tier1", "corner", "hsi", "n90"], False),
        ("P2: + Post-Aug2025 Reform", ["lage", "lproc", "ah", "vc", "tier1", "corner", "hsi", "n90", "post_reform"], False),
        ("P3: + Accounting & Gov Wedge", ["lage", "lproc", "ah", "vc", "tier1", "corner", "hsi", "n90", "roa_y1", "leverage_y1", "wedge"], False),
        ("P4: + Quarter Fixed Effects", ["lage", "lproc", "ah", "vc", "tier1", "corner", "roa_y1", "leverage_y1", "wedge"], True),
    ]
    records = []
    for label, cols, use_qfe in specs:
        needed = ["y", "cohort"] + cols
        sub = d[needed].replace([np.inf, -np.inf], np.nan).dropna().copy()
        X_parts = [sub[cols].astype(float)]
        if use_qfe:
            q_dummies = pd.get_dummies(sub["cohort"], prefix="Q", drop_first=True, dtype=float)
            X_parts.append(q_dummies)
        X = sm.add_constant(pd.concat(X_parts, axis=1), has_constant="add")
        fit = sm.OLS(sub["y"].astype(float), X).fit(cov_type="HC3")
        row = {
            "Specification": label,
            "N": int(fit.nobs),
            "R2": float(fit.rsquared),
            "Adj_R2": float(fit.rsquared_adj),
        }
        for c in ("lproc", "ah", "vc", "tier1", "corner", "hsi", "post_reform", "roa_y1", "leverage_y1", "wedge"):
            if c in fit.params:
                b = fit.params[c]
                p = fit.pvalues[c]
                stars = "***" if p < 0.01 else ("**" if p < 0.05 else ("*" if p < 0.10 else ""))
                row[c] = f"{b:+.3f}{stars} (p={p:.3f})"
            else:
                row[c] = "—"
        records.append(row)
    return pd.DataFrame(records)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    panel = select_period(load_panel(), start_year=2020, end_year=2026)
    d = build_panel_frame(panel)

    t1 = summarize_by_cohort(panel, d)
    t2 = summarize_reform(panel, d)
    t3 = run_panel_regressions(d)

    t1.to_csv(OUT / "table1_cohort_summary.csv", index=False)
    t2.to_csv(OUT / "table2_reform_comparison.csv", index=False)
    t3.to_csv(OUT / "table3_panel_regressions.csv", index=False)

    (OUT / "table1_cohort_summary.md").write_text(
        "# Table 1: Multi-Quarter Main Board IPO Summary (2025–2026)\n\n"
        + to_markdown(t1.round(2).set_index("Cohort"), "Cohort") + "\n",
        encoding="utf-8",
    )
    (OUT / "table2_reform_comparison.md").write_text(
        "# Table 2: Pre- vs Post-August 2025 HKEX Allocation & Pricing Reform\n\n"
        + to_markdown(t2.round(2).set_index("Regime"), "Regime") + "\n",
        encoding="utf-8",
    )
    (OUT / "table3_panel_regressions.md").write_text(
        "# Table 3: Multi-Year Panel Underpricing Regressions (Dep. Var: ln(1 + IR), HC3 SE)\n\n"
        + to_markdown(t3.round(3).set_index("Specification"), "Specification") + "\n",
        encoding="utf-8",
    )
    print(f"Full panel study written to {OUT} (N={len(panel)} issuers across {panel['cohort'].nunique()} cohorts)")


if __name__ == "__main__":
    main()
