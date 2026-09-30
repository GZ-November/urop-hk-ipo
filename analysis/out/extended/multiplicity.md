# Multiplicity across the headline tests in this module

Benjamini-Hochberg step-up at FDR 10% over the tests listed. Other tables in this repository are outside this family.

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Tails | April-June window -> P(IR > 100%), logit | 0.0035 | 0.0231 |
| 2 | Regime | Month effect on IR (ANOVA permutation) | 0.0052 | 0.0231 |
| 3 | Aftermarket | Wealth relative vs HSI, Day 20: Apr-Jun vs other listings (Mann-Whitney) | 0.0056 | 0.0231 |
| 4 | Aftermarket | Wealth relative vs HSI, 3 months: Apr-Jun vs other listings (Mann-Whitney) | 0.0070 | 0.0231 |
| 5 | Tails | A+H issuer, PPML on 1 + IR | 0.0077 | 0.0231 |
| 6 | Tails | April-June window, PPML on 1 + IR | 0.0113 | 0.0283 |
| 7 | Aftermarket | Day-1 return vs 3-month BHR (Spearman) | 0.0536 | 0.1042 |
| 8 | Regime | Best contiguous window, search-corrected (permutation) | 0.0556 | 0.1042 |
| 9 | Regime | Subscription crowding -> IR | 0.2616 | 0.3806 |
| 10 | Tails | Cornerstone allocation, 90th-percentile quantile regression (bootstrap) | 0.2680 | 0.3806 |
| 11 | Demand | April-June window -> ln subscription ratio | 0.2791 | 0.3806 |
| 12 | Mechanism | Mechanism A vs B, route- and time-adjusted | 0.3581 | 0.4252 |
| 13 | Mechanism | Mechanism A vs B, raw (stratified permutation) | 0.3685 | 0.4252 |
| 14 | Tails | Cornerstone allocation, mean OLS (HC3) | 0.4550 | 0.4875 |
| 15 | Tails | VC/PE backing -> P(IR < 0), logit | 0.6862 | 0.6862 |

- 6 of 15 tests have q < 0.10. Most p-values ignore listing-month clustering; those that rely on it carry few (9) clusters, so q-values are indicative only. The family counts only tests reported here, not the exploration that chose them, so q-values understate the true multiplicity.
