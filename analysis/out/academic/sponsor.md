# Sponsor effects, 2026

The first-named sponsor in the `Sponsor(s)` column is used as the lead-sponsor proxy: the `Lead sponsor name` column reads "CICC" for 92 of 106
issuers even when CICC is not among the sponsors, so it is unusable. Sponsors with at least 3 deals are compared (9 sponsors, 80 deals).

| First-named sponsor | Deals | Mean IR | Median IR | Share listed Apr-Jun |
|---|---|---|---|---|
| China International Capital Corporation Hong Kong Securities Limited | 29 | 60% | 35% | 41% |
| CITIC Securities (Hong Kong) Limited | 18 | 45% | 3% | 50% |
| Huatai Financial Holdings (Hong Kong) Limited | 10 | 12% | -2% | 30% |
| China Securities (International) Corporate Finance Company Limited | 5 | 13% | 2% | 40% |
| Guotai Junan Capital Limited | 5 | 52% | 80% | 40% |
| Haitong International Capital Limited | 4 | 54% | 39% | 25% |
| CMB International Capital Limited | 3 | 59% | -15% | 33% |
| Goldman Sachs (Asia) L.L.C. | 3 | 35% | -0% | 33% |
| Morgan Stanley Asia Limited | 3 | -3% | 3% | 0% |

| Statistic | Raw log(1 + IR) | After window, A+H and size |
|---|---|---|
| Intraclass correlation across sponsors | -0.023 | -0.053 |
| ANOVA F (permutation p) | 0.83 (0.582) | 0.60 (0.762) |

- Sponsor differences in mean IR largely reflect when each sponsor's deals listed; the residual test asks whether anything remains once the listing window, A+H
  and size are removed. With few deals per sponsor and sponsors that often co-sponsor, a null result is weak evidence of no sponsor effect.
