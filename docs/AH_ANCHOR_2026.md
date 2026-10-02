# A+H reference prices and source review · 2026-10-02

Documentation updated on 2026-10-02; the observation cutoff remains **2026-09-30**. The current analysis covers **38 A+H issuers listed in 2026**, within the 113-issuer IPO sample. The earlier 34-issuer analysis and 41-issuer cross-year collection described in the [September 30 integration review](AGY_INTEGRATION_2026-09-30.md) are historical snapshots. Cross-year collection does not expand the study's 2026 scope.

`pipeline/exports/HKIPO-MASTER-AH-reference.csv` stores cross-year anchors; `HKIPO-2026-AH-reference.csv` is the study input. Anchors record A price date, FX date and observation cutoff. Failed or empty refreshes preserve existing caches. The refresh target rebuilds the master before collecting reference prices.

## Price and date definitions

The offer-price anchor is the raw A-share close on the last A trading day on or before the H subscription closing date, converted with that day's HKD-per-CNY exchange rate. The day-1 gap uses the A-share close on the H listing date; differences also reflect A-share and FX movements between dates.

The raw H-share first-day price correction was merged in PR #20. PR #23 rechecked A+H date anchors, FX direction and raw day-1 closes. The daily H/A premium divides raw H prices by raw A prices × FX. Price returns exclude dividend reinvestment and may be affected by corporate actions; they are not total returns.

## Current results and remaining research

Read the [generated report](../analysis/out/ah_anchor/ah_anchor.md) for current estimates and sample sizes. It reports 38 A+H issuers, with horizon-specific matched samples, a balanced day-60 path, and A-share event reactions using both index subtraction and a pre-event alpha/beta market model. Numerical results are maintained in generated outputs rather than copied into this document.

Remaining priorities are to separate A-market movements, H offer discounts and H listing repricing; collect the first H issuance announcement date; and add peer/industry benchmarks. Overlapping announcements, selected listing timing, raw-price corporate actions and few time clusters limit causal interpretation. A market model alone does not solve these issues.

## Margin financing and lockups

Current margin coverage is **25 of 113 issuers / 93 source-reported observations**. The closing-day specification has N=15 and G=4; the demonstrably public-before-subscription-deadline specification has N=25 and G=6. Publication metadata and coverage-selection diagnostics are available in the [margin report](../analysis/out/margin/margin.md); availability before the subscription deadline does not establish availability before pricing. Sparse surveys and inconsistent broker coverage remain limitations.

Contract-based lockup evidence now covers 113 issuers following PR #23 and #25; missing contractual evidence remains explicit. Q2 event windows still require actual post-event observations. Refresh them as full windows mature, keeping the cutoff explicit. See the [current readiness report](../pipeline/reports/research_readiness/README.md).
