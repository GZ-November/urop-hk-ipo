# Retail Profit Distributions — 2026

Read [the English study report](research.md) or [the consolidated report](../../../docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md).

| Artifact | Contents |
|---|---|
| portfolio_distributions.csv | Conditional profit distributions by strategy and handling-fee scenario |
| applicant_outcomes.csv | Guaranteed/additional outcomes, expected net profits and separate loss probabilities |
| profit_concentration_sensitivity.csv | Removal of the largest observed profit contributors |
| allocation_return_decomposition.csv | Allocation-return covariance identity and subgroup descriptions |
| fee_frontier.csv | Handling fees from HK$0 to HK$200 |
| application_size_schedule_fee88.csv | All disclosed tiers at an assumed HK$88 fee |
| financing_sensitivity.csv | Borrowing-rate and funded-day assumptions |
| month_bootstrap_mean_net.csv | Descriptive listing-month sampling intervals |
| a_influence_regressions.csv / a_subgroup_stability.csv | Supporting demand robustness |
| a_matched_aftermarket.csv / a_matched_sample.csv | Jointly observed five/twenty-day stock and HSI windows |
| 3355_original_and_derived.json | Original text versus inferred guarantee quantities |
| fee_sources.json | Current channel sources, hypothetical fees and excluded costs |
| run_manifest.json | Source/code/output hashes, versions and simulation assumptions |

Prices are observed first-day closes, not forecasts. Simulations assume independent ballots; partial costs and principal-only budgets are stated in the report. CSV returns use decimals unless their column explicitly says otherwise.
