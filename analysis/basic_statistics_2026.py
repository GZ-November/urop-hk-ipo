"""Describe the observed 2026 IPO sample before selecting a research question.

Run: python3 analysis/basic_statistics_2026.py
Outputs: analysis/out/basic_statistics/ (coverage, summaries, groups, correlations).
No regressions or hypothesis tests; coverage means stored values, not verified evidence.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import yaml

from research_inputs import C, MASTER, ROOT, load_panel, select_2026
from shared.reporting import to_markdown

OUT = ROOT / "analysis/out/basic_statistics"
AS_OF = pd.Timestamp("2026-09-30")


def markdown(frame: pd.DataFrame) -> str:
    return to_markdown(frame.round(3).set_index(frame.columns[0]), str(frame.columns[0]))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    sample = select_2026(load_panel())
    sample = sample[sample.listing_date <= AS_OF].copy()
    registry_path = ROOT / "pipeline/registry/HKIPO_Variable_Registry.yaml"
    registry = yaml.safe_load(registry_path.read_text())
    coverage = []
    for variable in registry["variables"]:
        field = variable["header"]
        values = sample[field]
        row = {"field": field, "dtype": variable["dtype"], "n_population": len(sample),
               "n_present": int(values.notna().sum()), "n_missing": int(values.isna().sum()),
               "n_distinct": int(values.nunique())}
        for cohort, part in sample.groupby("cohort"):
            row[f"{cohort}_present"] = int(part[field].notna().sum())
        coverage.append(row)
    coverage = pd.DataFrame(coverage)
    coverage.to_csv(OUT / "field_coverage.csv", index=False)

    ratio = sample["Final public offer shares"] / sample["Public valid applied shares"].where(sample["Public valid applied shares"] > 0)
    allocation = ratio.where(ratio.gt(0) & ratio.le(1))
    frame = pd.DataFrame({
        "code": sample["Stock Code"], "quarter": sample["cohort"], "month": sample["month"].astype(str),
        "route": sample["route"], "ir_pct": 100 * sample["ir"], "base_proceeds_hkd_mn": sample["base_proceeds"] / 1e6,
        "subscription_x": sample[C["sub"]], "applicants": sample["Public applicants"],
        "age_years": sample[C["age"]], "cornerstone_pct": 100 * sample[C["corner"]],
        "allocation_pct": 100 * allocation, "application_gross_return_pct": 100 * allocation * sample["ir"],
    })
    frame["demand_group"] = pd.qcut(frame["subscription_x"], 3, labels=["Low demand", "Middle demand", "High demand"])
    frame.to_csv(OUT / "sample.csv", index=False)
    units = {"ir_pct": "First-day return (%)", "base_proceeds_hkd_mn": "Base offer proceeds (HK$ million)",
             "subscription_x": "Public subscription multiple (times)", "applicants": "Public applicants (persons)", "age_years": "Firm age (years)",
             "cornerstone_pct": "Cornerstone allocation (%)", "allocation_pct": "Issuer-average allocation rate (%)",
             "application_gross_return_pct": "Application gross return (%, proportional allocation scenario)"}
    summary = frame[list(units)].describe(percentiles=[.25, .5, .75]).T.reset_index(names="variable")
    summary["variable"] = summary["variable"].map(units)
    summary.to_csv(OUT / "summary.csv", index=False)

    tables = []
    for group in ["quarter", "month", "route", "demand_group"]:
        rows = []
        for name, part in frame.groupby(group, observed=True):
            ir = part["ir_pct"].dropna()
            rows.append({"grouping": group, "group": str(name), "issuer_n": len(part), "ir_n": len(ir),
                         "mean_ir_pct": ir.mean(), "median_ir_pct": ir.median(),
                         "break_share_pct": 100 * ir.lt(0).mean(), "median_subscription_x": part["subscription_x"].median(),
                         "median_base_proceeds_hkd_mn": part["base_proceeds_hkd_mn"].median(),
                         "application_return_n": int(part["application_gross_return_pct"].notna().sum()),
                         "mean_application_gross_return_pct": part["application_gross_return_pct"].mean()})
        tables.append(pd.DataFrame(rows))
    groups = pd.concat(tables, ignore_index=True)
    groups.to_csv(OUT / "group_comparisons.csv", index=False)

    correlations = []
    for variable in ["subscription_x", "applicants", "base_proceeds_hkd_mn", "age_years", "cornerstone_pct"]:
        pair = frame[["ir_pct", variable]].replace([np.inf, -np.inf], np.nan).dropna()
        correlations.append({"variable": units[variable], "pair_n": len(pair),
                             "spearman_with_ir": pair["ir_pct"].corr(pair[variable], method="spearman")})
    correlations = pd.DataFrame(correlations)
    correlations.to_csv(OUT / "correlations.csv", index=False)

    core_fields = [C[k] for k in ("ir", "offer", "sub", "age", "corner", "vc", "float", "profit_y1")]
    core_fields += ["Industry classification code", "Public applicants", "Public valid applied shares", "Final public offer shares",
                    "Pricing date", "First trading day turnover (HK$)", "Day-5 BHR from Day-1 close (%)",
                    "Day-20 BHR from Day-1 close (%)", "3-month BHR from Day-1 close (%)", "6-month BHR from Day-1 close (%)"]
    selected = coverage[coverage.field.isin(core_fields)][["field", "n_present", "n_missing"]]
    missing_rows = [{"field": field, "code": row["Stock Code"], "cohort": row["cohort"]}
                    for field in core_fields for _, row in sample.loc[sample[field].isna()].iterrows()]
    pd.DataFrame(missing_rows, columns=["field", "code", "cohort"]).to_csv(OUT / "core_missing_records.csv", index=False)
    report = f"""# 2026 IPO Basic Statistics and Data Coverage

Sample: {len(sample)} ordinary Main Board IPOs listed from {sample.listing_date.min().date()} to {sample.listing_date.max().date()}; observation cutoff {AS_OF.date()}. Only actual 2026 listing dates are selected.
This report contains descriptive statistics and rank correlations, without regressions or significance tests. It retains the current raw-price and security-unit corrections.

## 1. Core-field coverage

{markdown(selected)}

Coverage means a value is stored in the master, not that the original disclosure has been independently verified. See field_coverage.csv for all registered fields and core_missing_records.csv for issuers with missing core inputs. Unmatured, undisclosed, uncollected and inapplicable values must be distinguished; missing values are not automatically zero. Fixed-price offers have no within-range revision.

Base offer proceeds equal offer price times base offered security units. Share and HDR units follow the current repairs; this measure is not proceeds including greenshoe exercise or issuer net proceeds.

## 2. Descriptive statistics

{markdown(summary)}

Application gross return equals issuer-average allocation rate times first-day return. This is a proportional-allocation scenario, not a one-lot ballot probability, actual account outcome or fee-adjusted profit. Here the aggregate rate retains the legacy final-public/applications denominator; the tier-based retail study separately excludes employee reserved allotments. Ratios above one or nonpositive ratios remain missing rather than being capped. Means and medians are reported together to show tail sensitivity.

## 3. Quarters and listing routes

{markdown(groups.loc[groups.grouping.isin(['quarter', 'route']), ['group', 'ir_n', 'mean_ir_pct', 'median_ir_pct', 'break_share_pct']])}

Routes are mutually exclusive in the order 18A, 18C, A+H and conventional. The separate A+H flag can overlap 18C. Each return cell has its own valid N. Small groups are descriptive; the complete monthly table is in group_comparisons.csv.

## 4. Subscription-demand terciles

{markdown(groups.loc[groups.grouping.eq('demand_group'), ['group', 'ir_n', 'mean_ir_pct', 'median_ir_pct', 'break_share_pct', 'mean_application_gross_return_pct']])}

Groups use subscription quantiles in the observed sample, not external regulatory thresholds. Differences may also reflect offer size, listing month and route composition.

## 5. Rank correlations with first-day returns

{markdown(correlations)}

Spearman correlations describe rankings and do not identify causal effects. Each pair uses its own finite sample, separately from regression complete-case samples.

## 6. Current research

See the [English empirical report](../../../docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md) for tier-based retail profits and demand robustness; see [the research plan](../../../docs/RESEARCH_PLAN_2026.md) and [data gaps](../../../docs/DATA_GAPS_2026.md) for scope and collection priorities.
"""
    (OUT / "basic_statistics.md").write_text(report, encoding="utf-8")
    manifest = {"as_of": str(AS_OF.date()), "sample_n": len(sample), "registered_fields": len(coverage),
                "inputs": {str(MASTER.relative_to(ROOT)): hashlib.sha256(MASTER.read_bytes()).hexdigest(),
                           "analysis/basic_statistics_2026.py": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           str(registry_path.relative_to(ROOT)): hashlib.sha256(registry_path.read_bytes()).hexdigest()},
                "pandas_version": pd.__version__}
    (OUT / "run_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2)+"\n")
    print(f"Basic statistics written: {len(sample)} issuers, {len(coverage)} registered fields")


if __name__ == "__main__":
    main()
