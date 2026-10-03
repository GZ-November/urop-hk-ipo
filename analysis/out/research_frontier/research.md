# 2026 Research Frontier: Exploratory Evidence

Design: docs/RESEARCH_DESIGN_2026.md. No causal or preregistration claim.

## Retail application capital and allocated capital

Common valid sample N=113, listing-month clusters G=9. The intervals use 2,000 listing-month resamples, seed=20260930; few-cluster intervals are descriptive and do not eliminate market shocks or information-type selection.

| Measure | Estimate | Cluster-bootstrap lower | Cluster-bootstrap upper |
|---|---|---|---|
| mean_ir | 53.153% | 28.904% | 77.053% |
| allocation_weighted_ir | 1.181% | -2.232% | 8.579% |
| application_return | 0.020% | -0.051% | 0.098% |

Returns above are percentages; CSVs retain decimals. A HK$10,000 proportional application has mean expected gross profit of HK$1.99. This legacy issuer-average scenario is not a one-lot win probability or actual account result. The tier-based retail study separately uses disclosed application tiers and excludes employee reserved allotments from its macro comparison. In retail_cost_scenarios.csv, fees, borrowing fractions and two funded days are assumptions, not measured account loans. Subscription/trading costs and opportunity cost are excluded; these are not complete net investment returns.
## Cornerstone share: association, few-cluster inference and omitted variables

| Specification | n | g | b | hc3_se | hc3_p | restricted_wild_p | rv_to_zero_equal_strength |
|---|---|---|---|---|---|---|---|
| Ex-ante controls | 106 | 9 | -0.309 | 0.410 | 0.451 | 0.191 | 0.096 |
| + final demand (endogenous) | 106 | 9 | -0.455 | 0.365 | 0.213 | 0.082 | 0.144 |

Both specifications use the same issuer sample. A 0.10 change in the focus regressor changes log(1+IR) by 0.10*b; exp(0.10*b)-1 is the proportional change in (1+IR), not an IR percentage-point change. The restricted wild bootstrap-t enumerates all Rademacher patterns across listing months. The two HC3 focus tests form a Holm family; cluster p-values are not mixed into HC3 stars.

RV and partial R-squared diagnose point-estimate sensitivity using the ordinary OLS residual scale, not cluster significance or causal confidence intervals. Final demand and cornerstone share are endogenous; conditioning on demand may condition on a mediator or collider. Significance cannot repair identification.

Event and six-calendar-month coverage: event_readiness.csv. Mechanism overlap: mechanism_support.csv. Missing evidence and immature windows remain distinct; neither is imputed.
