# Multiplicity across the headline tests in this module

Benjamini-Hochberg step-up at FDR 10% over the tests listed. Other tables in this repository are outside this family.

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Tails | April-June window -> P(IR > 100%), logit | 0.0023 | 0.0172 |
| 2 | Tails | A+H issuer, PPML on 1 + IR | 0.0023 | 0.0172 |
| 3 | Aftermarket | Wealth relative vs HSI, Day 20: Apr-Jun vs other listings (Mann-Whitney) | 0.0056 | 0.0180 |
| 4 | Regime | Month effect on IR (ANOVA permutation) | 0.0064 | 0.0180 |
| 5 | Aftermarket | Wealth relative vs HSI, 3 months: Apr-Jun vs other listings (Mann-Whitney) | 0.0070 | 0.0180 |
| 6 | Tails | April-June window, PPML on 1 + IR | 0.0072 | 0.0180 |
| 7 | Aftermarket | Day-1 return vs 3-month BHR (Spearman) | 0.0536 | 0.1149 |
| 8 | Regime | Best contiguous window, search-corrected (permutation) | 0.0832 | 0.1560 |
| 9 | Demand | April-June window -> ln subscription ratio | 0.1924 | 0.3207 |
| 10 | Tails | Cornerstone allocation, 90th-percentile quantile regression (bootstrap) | 0.2360 | 0.3522 |
| 11 | Regime | Subscription crowding -> IR | 0.2583 | 0.3522 |
| 12 | Mechanism | Mechanism A vs B, route- and time-adjusted | 0.3361 | 0.4202 |
| 13 | Tails | Cornerstone allocation, mean OLS (HC3) | 0.3682 | 0.4248 |
| 14 | Mechanism | Mechanism A vs B, raw (stratified permutation) | 0.4943 | 0.5296 |
| 15 | Tails | VC/PE backing -> P(IR < 0), logit | 0.8083 | 0.8083 |

- 6 of 15 tests have q < 0.10. Most p-values ignore listing-month clustering; those that rely on it carry few (9) clusters, so q-values are indicative only. The family counts only tests reported here, not the exploration that chose them, so q-values understate the true multiplicity.
