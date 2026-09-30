# Multiplicity across the tests in this module

Benjamini-Hochberg step-up at FDR 10%.

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Fees | Scale economies: commission rate vs ln offer size (HC3) | 0.0000 | 0.0000 |
| 2 | Events | Stabilization end: CAR [-5,+5] vs HSI (placebo) | 0.0040 | 0.0103 |
| 3 | Events | Six-month lockup expiry: turnover shock vs placebo days | 0.0044 | 0.0103 |
| 4 | Events | Six-month lockup expiry: CAR [-5,+5] vs HSI (placebo) | 0.1470 | 0.2572 |
| 5 | Partial adjustment | Offer-price revision -> IR, window-adjusted (HC3) | 0.2219 | 0.3107 |
| 6 | Money left | Commission rate vs log(1 + IR), controlling size, window, A+H (HC3) | 0.4549 | 0.5307 |
| 7 | Sponsor | First-named sponsor effect on IR, after window, A+H and size (ANOVA permutation) | 0.7618 | 0.7618 |

The family counts only tests reported here, not the exploration that chose them.
