# Multiplicity across the tests in this module

Benjamini-Hochberg step-up at FDR 10%.

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Fees | Scale economies: commission rate vs ln offer size (HC3) | 0.0000 | 0.0000 |
| 2 | Events | Six-month lockup expiry: turnover shock vs placebo days | 0.0040 | 0.0140 |
| 3 | Events | Six-month lockup expiry: CAR [-5,+5] vs HSI (placebo) | 0.1004 | 0.2342 |
| 4 | Partial adjustment | Offer-price revision -> IR, window-adjusted (HC3) | 0.2397 | 0.4195 |
| 5 | Money left | Commission rate vs log(1 + IR), controlling size, window, A+H (HC3) | 0.4751 | 0.6110 |
| 6 | Events | Stabilization end: CAR [-5,+5] vs HSI (placebo) | 0.5237 | 0.6110 |
| 7 | Sponsor | First-named sponsor effect on IR, after window, A+H and size (ANOVA permutation) | 0.7514 | 0.7514 |

The family counts only tests reported here, not the exploration that chose them.
