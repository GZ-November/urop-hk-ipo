# 2026 IPO analysis

Current baseline (documentation synced 2026-10-02): 113 ordinary IPOs (Q1 38, Q2 45, Q3 30), observation cutoff 2026-09-30. A+H analysis covers 38 issuers. PR #23 repairs and PR #25 sample expansion are reflected in current outputs; model-specific complete-case N differs from the full sample. See [repair status and remaining limits](../pipeline/reports/research_readiness/README.md).

Every statistical and regression output uses Hong Kong Main Board ordinary IPOs **listed in 2026**. `select_2026` checks actual listing dates, cohort consistency and issuer uniqueness. Module A contains no 2025H1 or historical US comparison observations. Literature and prior sponsor rankings inform definitions only.

List or run studies through the unified runner (existing direct script commands remain valid):

```bash
python run.py analysis --list
python run.py analysis --study underpricing
python run.py analysis --study ah --study margin
```

`analysis/run.py` owns the study registry and execution order. Shared table/chart functions live in `shared/reporting.py`; clustered inference lives in `shared/inference.py`; focused regressions and multiple-test adjustment live in `shared/estimation.py`. Underpricing hypotheses and the common-sample policy live in `specifications/underpricing.py`. Legacy Module A/B exports point to these same implementations. See [architecture](../docs/ARCHITECTURE.md).

From the repository root:

```bash
python -m pip install -e '.[analysis,dev]'
python run.py master --derive
make basic-analysis   # start with coverage, descriptive statistics, groups and correlations
make analysis         # reproduce all existing exploratory modules when needed
make test-analysis
```

The input is `pipeline/exports/HKIPO-MB-MASTER_clean.csv`; the CLI merges existing cohort exports. Export updated workbooks per config before rebuilding the master. Historical cohorts can remain in the storage layer and are excluded at the analysis selector.

Shared research inputs live in `research_inputs.py`, which imports no report,
plotting or estimation scripts. New studies can start with:

```python
from research_inputs import load_panel, select_2026, prepare_regression

issuers = select_2026(load_panel())
frame = prepare_regression(issuers)
```

`load_panel` interprets the registry and missing values; `select_2026` verifies
listing dates, cohort consistency and issuer uniqueness. `prepare_regression`,
`prepare_extended` and `prepare_academic` supply the existing shared variables,
without dropping observations for a particular model. Estimation samples,
models, market observations and figures remain study-specific. The older
Module A input names, Module B/extended `prepare`, and academic `build_frame`
remain compatible aliases. The pipeline's slug-based `src/panel.py` remains
available for browsing registered variables; this migration preserves the
existing research column names and definitions.

| Script | Output |
|---|---|
| `retail_2026_report.py` | `out/retail_2026_report/`: descriptive tables, direct workbook coverage for all 202 fields, data meanings and research uses; generates the English [LaTeX report](../docs/reports/HK_IPO_2026_COMPREHENSIVE_REPORT.tex) and mentor draft without simulation |
| `basic_statistics_2026.py` | `out/basic_statistics/`: 202-field coverage, core descriptive statistics, quarter/month/route/demand groups and pairwise Spearman correlations; no regressions or hypothesis tests |
| `module_a_stylized_facts.py` | `out/module_a/`: quarter/route/pricing/backing tables, aftermarket table, three charts, input availability |
| `module_b_underpricing_regression.py` | `out/module_b/`: hypotheses, nested regressions, robustness, time-cluster inference, coefficient chart, sample selection |
| `ir_decomposition_2026.py` | `out/ir_decomposition/`: descriptive route/quarter/backing decomposition |
| `q2_breakdown_2026.py` | `out/q2_breakdown/`: sector mix and return concentration |
| `monthly_breakdown_2026.py` | `out/monthly_breakdown/`: monthly cycle and exploratory time-structure comparisons |
| `research_frontier_2026.py` | `out/research_frontier/`: allocation/application returns, cost scenarios, cornerstone OVB sensitivity, common-sample inference and explicit as-of event coverage; uses versioned helpers from the installed 2026-09-30 skill |
| `testability_screen_2026.py` | Console: variable coverage and variation |
| `aftermarket_event_time_2026.py` | `out/event_time/`: BHAR paths and horizons from cached daily bars, wild-cluster inference, calendar-time portfolio alphas (Newey-West) |
| `academic_extensions_2026.py` | `out/academic/`: who captures money left on the table and retail application returns, underwriting-fee determinants, lockup-expiry and stabilization-end event studies with placebo calibration, partial adjustment in the filing range, sponsor effects |
| `ah_anchor_2026.py` | `out/ah_anchor/`: A+H issuers' offer discount to the A-share price (from `tools/external/ah_reference.py`), its determinants, link to IR, convergence, A-share reaction |
| `margin_financing_2026.py` | `out/margin/`: source-reported margin snapshots, coverage and censoring, endpoint growth, and separate full-sample retail-demand proxies |
| `extended_analysis_2026.py` | `out/extended/`: search-corrected hot-window test, serial dependence, crowding, Mechanism A/B identification, quantile/PPML/logit tails, demand, aftermarket, out-of-sample R-squared, BH multiplicity (about 1 minute) |

Module B uses log(1 + first-day return), one common finite complete-case sample for M1–M4, and an April-June control in every model. M3 has nine explanatory variables; M4 adds log retail subscription for ten. 18A/18C groups remain descriptive in Module A, and state-owned cornerstones are reserved for the separate cornerstone study. Raw-return, 1/99 winsorized, drop-top-three, median-regression, quarter-effect and pairs-bootstrap checks use the baseline sample (except the deliberate top-three exclusion).

HC3 and listing-month CR1 inference are shown together. The restricted wild cluster bootstrap enumerates all Rademacher sign patterns for up to 16 clusters. Pairs-bootstrap draws without full rank are rejected and counted. These are exploratory associations with a small sample and few time clusters; the hot window was identified from these data. Descriptive decomposition models compare time controls and are not confirmatory hypothesis tests.

Unknown classification flags remain missing; invalid log inputs are excluded. Module A reports availability per input and matches MLOT/proceeds and IPO/benchmark observations for weighted statistics. Missing counts cannot by themselves distinguish uncollected from unmatured data; inspect the source cohort and horizon records.

[Research start](../docs/RESEARCH_START.md) · [Current research plan](../docs/RESEARCH_PLAN_2026.md) · [A+H anchor](../docs/AH_ANCHOR_2026.md) · [Historical source review](../docs/archive/reviews-2026-09-30/AGY_INTEGRATION_2026-09-30.md) · [Historical write-ups](../docs/archive/README.md)

A+H market collection also supports `--all --as-of YYYY-MM-DD`; the cross-year reference is stored separately from the 2026 analysis. `make margin-reference` regenerates margin observations from the curated source ledger with initial public-offer shares × maximum offer price as a fixed denominator. See [integration and source review](../docs/archive/reviews-2026-09-30/AGY_INTEGRATION_2026-09-30.md).

Current research design and brainstorm: [RESEARCH_DESIGN_2026.md](../docs/RESEARCH_DESIGN_2026.md). Evidence-gap disposition: [readiness review](../pipeline/reports/research_readiness/README.md).

The active plan starts with basic statistics and selects a few topics; the advanced modules above remain exploratory references. Data availability and collection feasibility: [DATA_GAPS_2026.md](../docs/DATA_GAPS_2026.md).


## Focused retail research — 3 October 2026

The latest [mentor brief](../docs/reports/RETAIL_MENTOR_BRIEF_2026-10-03.md) and [source reassessment](../docs/reports/RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md) resolve 2649's lot size to 500 and confirm 3355's Pool B rules using official clarifications. They use a source-bound overlay, exact expectations and no simulation. The earlier frozen inputs and distribution outputs remain historical snapshots. This opt-in follow-up is separate from the study registry:

```bash
.venv/bin/python tools/audit_retail_sources_2026.py
.venv/bin/python analysis/retail_evidence_brief_2026.py
```

Raw PDFs are needed at the paths in the follow-up source manifest. Tables are in `out/retail_evidence_brief/`; this source/analysis follow-up changes no workbooks or whole-payload pipeline approvals. The separate 19-issuer JSON repair has its own scoped source review. The pipeline skill handles collection/evidence only; this module handles empirical analysis.

The English [consolidated report](../docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md) and [implementation notes](../docs/reports/RETAIL_RESEARCH_IMPLEMENTATION_2026-10-03.md) describe the current study.

| Study | Output | Scope |
|---|---|---|
| `demand` | `out/subscription_heat/` | Retrospective demand groups, first-day return associations and aftermarket descriptions |
| `allocation_profit` | `out/retail_profit/` | Tier-based application expectations and separate applicant outcome probabilities |
| `retail_distribution` | `out/retail_distribution/` | Strict/minimum-tier portfolio distributions, covariance decomposition, cost frontiers and supporting robustness |

```bash
python run.py analysis --study demand --study allocation_profit --study retail_distribution
```

`retail_distribution` is opt-in. It conditions on observed prices and does not annualize simulated profits. Its English narrative is rendered by `shared/retail_report.py`; machine-readable values remain in CSVs. The allocation reader checks the pre-existing independent review against candidate/coverage/source hashes. Running `allocation_tiers_2026.py` only generates pending candidates, requiring a new review if their bytes change.
