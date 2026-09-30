# Codebase review and improvements · 2026-09-30

Scope: recent committed changes (`05d0408...de88f41`), the new untracked Module B analysis, collection/runtime helpers, core event/validation/writeback modules, packaging, checks and internal documentation. Standards and research-spec reviews ran independently. There was no originating issue specification; the local research plan, contracts and user instruction define the requirements. The user's current instruction restricts every statistical and regression analysis, including Module A, to 2026 listings.

## Standards

Ten findings, all addressed in code or repository policy:

1. **P1 — incomplete stabilization windows were reported as complete.** `stabilization_panel.py` clamped unavailable endpoints, producing a [-5,+5] return and +20 return from eight bars. Full endpoints are now required; unmatured windows remain missing. Zero-turnover observations stay in turnover averages.
2. **P1 — unsupported stabilization fields.** Generic “stabilizing actions” text could mark market purchases even when describing stock borrowing. Explicit purchase evidence is now required. Announcement date no longer copies stabilization-end date; it stays missing until independently parsed.
3. **P1 — package discovery failed.** Root setuptools discovery found both `pipeline` and `analysis` and raised `PackageDiscoveryError`. Both metadata projects now explicitly describe dependency-only installs for a source-checkout CLI. Wheels contain metadata only, excluding datasets and scratch trees.
4. **P2 — immature six-month daily statistics.** The expansion mapper previously used `bars[:126]` even for newly listed issuers. It now requires a mature, observed Month_6 horizon, sorts daily dates and uses its inclusive actual-date cutoff. Missing dates yield missing statistics; malformed dates fail closed.
5. **P2 — stale cornerstone absence could override a positive allocation.** Positive final allocation now clears stale absence; zero still confirms no allocation. Tests cover both precedence directions.
6. **P2 — unsafe scratch utilities and run logs.** One-issuer helpers mutate CWD-relative candidate JSON on import. They and extraction run logs are excluded from distribution. Existing tracked run logs are removed from the index while retained on disk.
7. **Policy conflict.** README, SECURITY and CONTRIBUTING disagreed about tracked research data. They now document the actual public-disclosure artifact policy and explain that ignore rules do not remove already tracked files or provide security guarantees.
8. **P2 — incomplete refresh/check coverage.** `aftermarket-refresh` omitted 2025Q2; cohort config discovery now covers all configured cohorts. `make check-code`, CI and the hook share lint, pipeline/analysis tests and registry checks. Missing flake8 is an error. An unused import in the monthly analysis was removed.

9. **P1 — truncated lockup CARs and missing benchmarks.** The lockup engine clamped [-5,+5]/[-20,+20] and had a +60 endpoint off-by-one. Each CAR includes both endpoint daily returns (11/41/61 observations) and requires its full independent window plus the prior benchmark close and observed finite stock and benchmark returns. Missing benchmark returns are never recoded as zero. Complete turnover windows retain true zeros; undisclosed locked percentages remain missing.
10. **P1 — month horizons used trading-day approximations and could admit future bars.** Month_1/3/6/12/24/36 now use a shared calendar-month helper and the first observed trading date at or after the calendar endpoint. Window averages stop at that endpoint, and bars after the explicit as-of date are excluded. Day_5/20 retain their trading-observation definitions.

## Spec

Five findings, addressed against `docs/RESEARCH_PLAN_2026.md`:

1. **P1 — missing hot-window control.** The plan requires a 4–6 month control in every main regression; old Module B omitted it. M1–M4 now include the April-June indicator, derived from the actual listing date.
2. **P2 — specification drift.** Old models used 11/12 regressors, 5/95 winsorization and 18A/18C hypothesis coefficients despite the plan's 8–10 limit, 1/99 robustness and descriptive-only route groups. M3/M4 now have 9/10 explanatory variables; 18A/18C remain descriptive, and state-owned cornerstones are reserved for their own study. Quarter effects replace both market controls and the hot-window indicator to avoid collinearity.
3. **P2 — unknown classifications became observed zero.** Numeric CSV columns containing textual missing markers could remain strings, causing comparisons against integer flags to fail; entirely missing route text also broke `.str`. Inputs now use registry numeric types. Unknown route evidence remains `Unknown`, and unknown A+H/backing/tier inputs remain missing. This correction changes the exclusive A+H route group to 33; the independent A+H flag identifies 34, including one overlapping 18C issuer. Total N remains 106.
4. **P2 — invalid transforms/unidentified models.** Zero or negative log inputs and infinities could reach fitting; singular OLS could reach covariance inversion. Transform domains, finite complete cases, residual degrees of freedom, full rank and cluster counts are now checked. Singular pairs-bootstrap resamples are rejected and counted; exact wild enumeration is bounded to 16 clusters.
5. **P2 — missing sample-selection reporting.** All nested models now use one complete-case sample including the demand input and listing month. Module A reports input availability and matched denominators; Module B reports overlapping invalid/missing reasons and total unique exclusions. Weighted returns and aggregate wealth relatives use matched observations.

The 2026-only scope is enforced by observed listing year, cohort/date agreement and issuer uniqueness. Module A's 2025H1/US comparison tables and historical distribution benchmark were removed. All six scripts now use the same selector. Literature and prior sponsor rankings inform definitions, rather than adding historical observations.

## Verification

- `make check-code`: 275 pipeline + 14 analysis tests passed (289 total), with maintained-source syntax/static checks and registry consistency passed. The clean staged checkout runs the same 289 tests successfully, skipping two production acceptance checks requiring omitted local evidence.
- `make analysis`: all six scripts completed; Module A/B and decomposition reports use 106 listings (2026Q1 38, Q2 45, Q3 23).
- CR1 covariance matches statsmodels' cluster covariance numerically on synthetic data. Tests cover singular bootstrap draws, invalid transforms, missing flags and analysis-year boundaries.
- A clean copy containing only staged files passes `make check-code` with the project interpreter (including an absolute path containing spaces).
- Both root and engine wheels build without automatic package discovery; archive inspection finds metadata only.
- Generated coefficient chart visually inspected; legend moved away from plotted intervals.
- Root/policy/navigation links checked; active architecture and research-plan paths/counts reconciled.

## Data audit and remaining limits

Read-only cell comparisons against available authorized extractions:

| Cohort | Prospectus cells matched / total | Prospectus JSON missing | Allotment cells matched / total | Allotment JSON missing | Numeric mismatches |
|---|---:|---:|---:|---:|---:|
| 2026Q1 | 2660 / 2660 | 0 | 684 / 684 | 0 | 0 |
| 2026Q2 | 3087 / 3150 | 63 | 810 / 810 | 0 | 0 |
| 2026Q3 | 1004 / 1610 | 606 | 282 / 414 | 132 | 0 |

Zero mismatches among comparable cells do not establish complete evidence coverage. Q2/Q3 missing extraction evidence requires source collection and independent review; it was not fabricated in this code review. Original cohort workbooks and reviewed extraction payloads were not rewritten. Market, stabilization and lockup producers now enforce the corrected rules on regeneration; previously generated event tables/workbook cells should be re-audited before another expansion writeback. New missing values must not overwrite curated workbook cells without reconciling their sources.

The sample ends on 2026-09-09 and is not the complete 2026 year. Results are exploratory; few monthly clusters, sparse subgroups and endogenous retail/cornerstone choices limit causal interpretation. The observed hot window is a data-informed control. The architecture manual describes operational checks, not a guarantee of semantic or econometric correctness.

Review totals: Standards 10 findings (worst: nominal event windows built from incomplete observations); Spec 5 findings (worst: missing mandated hot-window control).
