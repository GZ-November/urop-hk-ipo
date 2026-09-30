# Empirical analysis of HK IPO data

## Choose the study sample explicitly

This skill supports any requested year, cohort or multi-year interval. Collection
and the master storage layer remain broader than an individual study. Select by
observed listing dates, check cohort/date agreement and issuer uniqueness, and
report requested versus actual coverage and exclusions. Official report coverage
and extraction evidence must also be checked; a populated workbook does not
establish either. Do not import a previous study's date filter as a global rule.

Read the root `analysis/README.md` and the applicable research plan before using
existing scripts. The current Module A/B and breakdown scripts implement a
2026-only study with `select_2026`; `make analysis` runs those scripts. For an
all-years or other-period analysis, implement and validate the requested selector
and applicable specifications instead of presenting those outputs as all-data
results. Changing the skill's scope does not itself change an existing study.

## Inputs and variable construction

Use the master clean export (`pipeline/exports/HKIPO-MB-MASTER_clean.csv`) and
registry types. Resolve semantic headers/slugs; legacy `col_*` keys are extraction
identifiers and cannot be used as assumed physical columns or CSV names.

- Initial return: day-one close / final offer price minus one.
- Base proceeds: final offer price times final global-offering shares before
  over-allotment. Distinguish gross base proceeds from issuer net proceeds.
- Aftermarket BHR from day-one close excludes the initial return. Keep it distinct
  from total return from offer price and CAR versus a benchmark.
- Preserve missing/unknown classifications. No blanket `fillna(0)` for backing,
  sponsor tier, listing route or A+H flags. An exclusive route group and an
  independent A+H flag can overlap differently; report their definitions.
- Confirm percentage units from the registry and producer before dividing by 100;
  do not infer scale from the label alone.
- Positive log inputs and finite values are required. `ln(subscription multiple)`
  and `ln(1 + subscription multiple)` are different specifications; use the study's
  definition. Fixed-price offers have no observed within-range price position;
  do not substitute 0.5 for every missing price position.
- Keep original financial-period values distinct from annualized values and
  stocks distinct from flows. Do not mix unconverted currencies in regressors.

Missing counts need source interpretation: unavailable disclosure, absent
extraction, unknown classification, immature horizon and missing market/benchmark
observations are different causes. Consult `data_quality_and_events.md` before
using regenerated or previously written event fields.

## Descriptive statistics and estimation

Report availability and denominators for each input. Weighted returns use matched
money-left-on-table and positive base proceeds; aggregate wealth relatives use
matched stock/benchmark observations. Do not count missing flags as negative
classifications. Unequal horizon maturity changes the sample behind each table.

Use a consistent finite complete-case sample for nested model comparisons, or
explicitly report why samples differ. Log sample-selection reasons (which can
overlap), unique exclusions and final N. Require residual degrees of freedom,
full-rank design matrices and at least two clusters for clustered covariance.
Reject and count singular pairs-bootstrap draws. State cluster definitions,
small-cluster limitations, and any resampling method's supported bounds.

Use the chosen research plan rather than a generic regression template. Avoid
adding every available regressor or fixed effect to a small sample. Describe
retail demand, cornerstone allocation and data-informed timing controls as
potentially endogenous; passing diagnostics does not establish causality.

## Current repository study (conditional reference)

For requests about the current 2026 study, authoritative specifications are in
`docs/RESEARCH_PLAN_2026.md`, `analysis/README.md` and
`analysis/module_b_underpricing_regression.py`:

- Module A describes quarters, routes, pricing, VC/PE backing and aftermarket
  performance within 2026; it reports input availability and matched denominators.
- Module B uses log(1 + initial return) and one common finite sample for M1–M4,
  including the demand variable and listing month. Each main model includes the
  April–June 2026 control. M3/M4 have nine/ten explanatory variables.
- 18A/18C are descriptive groups; the state-owned cornerstone study is separate.
- Robustness includes raw returns, 1/99 winsorization, drop-top-three, median
  regression, quarter effects and pairs bootstrap. Quarter effects replace both
  market variables and the hot-window control.
- Inference reports HC3, listing-month CR1 and restricted wild cluster bootstrap;
  exact Rademacher enumeration supports at most 16 clusters in this implementation.

These are study-specific choices, not universal requirements for other years or
research questions. Re-export updated cohort workbooks, rebuild the master, then
run the appropriate analysis. Record whether outputs were only rerun or whether
their input evidence and derived values were also reconciled.
