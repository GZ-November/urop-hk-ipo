# Multiplicity across the headline tests in this module

Benjamini-Hochberg step-up at FDR 10% over the tests listed. Other tables in this repository are outside this family.

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Aftermarket | Wealth relative vs HSI, 3 months: Apr-Jun vs other listings (Mann-Whitney) | 0.0011 | 0.0172 |
| 2 | Tails | April-June window -> P(IR > 100%), logit | 0.0035 | 0.0260 |
| 3 | Aftermarket | Wealth relative vs HSI, Day 20: Apr-Jun vs other listings (Mann-Whitney) | 0.0056 | 0.0265 |
| 4 | Tails | A+H issuer, PPML on 1 + IR | 0.0071 | 0.0265 |
| 5 | Regime | Month effect on IR (ANOVA permutation) | 0.0106 | 0.0267 |
| 6 | Tails | VC/PE backing -> P(IR < 0), logit | 0.0107 | 0.0267 |
| 7 | Tails | April-June window, PPML on 1 + IR | 0.0137 | 0.0293 |
| 8 | Aftermarket | Day-1 return vs 3-month BHR (Spearman) | 0.0673 | 0.1262 |
| 9 | Regime | Best contiguous window, search-corrected (permutation) | 0.0812 | 0.1353 |
| 10 | Demand | April-June window -> ln subscription ratio | 0.1679 | 0.2518 |
| 11 | Tails | Cornerstone allocation, 90th-percentile quantile regression (bootstrap) | 0.2940 | 0.4009 |
| 12 | Mechanism | Mechanism A vs B, raw (stratified permutation) | 0.3399 | 0.4137 |
| 13 | Regime | Subscription crowding -> IR | 0.3844 | 0.4137 |
| 14 | Mechanism | Mechanism A vs B, route- and time-adjusted | 0.3862 | 0.4137 |
| 15 | Tails | Cornerstone allocation, mean OLS (HC3) | 0.4480 | 0.4480 |

- 7 of 15 tests have q < 0.10. Most p-values ignore listing-month clustering; those that rely on it carry few (9) clusters, so q-values are indicative only. The family counts only tests reported here, not the exploration that chose them, so q-values understate the true multiplicity.
