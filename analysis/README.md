# 2026 IPO analysis

Every statistical and regression output uses Hong Kong Main Board ordinary IPOs **listed in 2026**. `select_2026` checks actual listing dates, cohort consistency and issuer uniqueness. Module A contains no 2025H1 or historical US comparison observations. Literature and prior sponsor rankings inform definitions only.

From the repository root:

```bash
python -m pip install -e '.[analysis,dev]'
python run.py master --derive
make analysis
make test-analysis
```

The input is `pipeline/exports/HKIPO-MB-MASTER_clean.csv`; the CLI merges existing cohort exports. Export updated workbooks per config before rebuilding the master. Historical cohorts can remain in the storage layer and are excluded at the analysis selector.

| Script | Output |
|---|---|
| `module_a_stylized_facts.py` | `out/module_a/`: quarter/route/pricing/backing tables, aftermarket table, three charts, input availability |
| `module_b_underpricing_regression.py` | `out/module_b/`: hypotheses, nested regressions, robustness, time-cluster inference, coefficient chart, sample selection |
| `ir_decomposition_2026.py` | `out/ir_decomposition/`: descriptive route/quarter/backing decomposition |
| `q2_breakdown_2026.py` | `out/q2_breakdown/`: sector mix and return concentration |
| `monthly_breakdown_2026.py` | `out/monthly_breakdown/`: monthly cycle and exploratory time-structure comparisons |
| `testability_screen_2026.py` | Console: variable coverage and variation |
| `aftermarket_event_time_2026.py` | `out/event_time/`: BHAR paths and horizons from cached daily bars, wild-cluster inference, calendar-time portfolio alphas (Newey-West) |
| `academic_extensions_2026.py` | `out/academic/`: who captures money left on the table and retail application returns, underwriting-fee determinants, lockup-expiry and stabilization-end event studies with placebo calibration, partial adjustment in the filing range, sponsor effects |
| `ah_anchor_2026.py` | `out/ah_anchor/`: A+H issuers' offer discount to the A-share price (from `tools/external/ah_reference.py`), its determinants, link to IR, convergence, A-share reaction |
| `margin_financing_2026.py` | `out/margin/`: margin-financing demand when `HKIPO-2026-margin-daily.csv` is supplied (validated; no data shipped) |
| `extended_analysis_2026.py` | `out/extended/`: search-corrected hot-window test, serial dependence, crowding, Mechanism A/B identification, quantile/PPML/logit tails, demand, aftermarket, out-of-sample R-squared, BH multiplicity (about 1 minute) |

Module B uses log(1 + first-day return), one common finite complete-case sample for M1–M4, and an April-June control in every model. M3 has nine explanatory variables; M4 adds log retail subscription for ten. 18A/18C groups remain descriptive in Module A, and state-owned cornerstones are reserved for the separate cornerstone study. Raw-return, 1/99 winsorized, drop-top-three, median-regression, quarter-effect and pairs-bootstrap checks use the baseline sample (except the deliberate top-three exclusion).

HC3 and listing-month CR1 inference are shown together. The restricted wild cluster bootstrap enumerates all Rademacher sign patterns for up to 16 clusters. Pairs-bootstrap draws without full rank are rejected and counted. These are exploratory associations with a small sample and few time clusters; the hot window was identified from these data. Descriptive decomposition models compare time controls and are not confirmatory hypothesis tests.

Unknown classification flags remain missing; invalid log inputs are excluded. Module A reports availability per input and matches MLOT/proceeds and IPO/benchmark observations for weighted statistics. Missing counts cannot by themselves distinguish uncollected from unmatured data; inspect the source cohort and horizon records.

[Extended analysis and data review](../docs/EXTENDED_ANALYSIS_2026.md) · [Academic extensions](../docs/ACADEMIC_EXTENSIONS_2026.md) · [A+H anchor](../docs/AH_ANCHOR_2026.md) · [Research plan](../docs/RESEARCH_PLAN_2026.md) · [Review and fixes](../docs/CODE_REVIEW_2026-09-30.md)
