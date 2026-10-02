# Sponsor effects, 2026

The first-named sponsor in the `Sponsor(s)` column is used as a proxy. Earlier source review found unreliable entries in `Lead sponsor name`
(see docs/archive/pre-raw-price-correction/ACADEMIC_EXTENSIONS_2026.md), so that field is not used. First-named order does not establish actual lead responsibility.
Sponsors with at least 3 complete-case deals are compared (9 sponsors, 85 deals).

| First-named sponsor | Deals | Mean IR | Median IR | Share listed Apr-Jun |
|---|---|---|---|---|
| China International Capital Corporation Hong Kong Securities Limited | 29 | 62% | 35% | 41% |
| CITIC Securities (Hong Kong) Limited | 20 | 41% | 6% | 45% |
| Huatai Financial Holdings (Hong Kong) Limited | 11 | 14% | 0% | 27% |
| Haitong International Capital Limited | 6 | 33% | 12% | 17% |
| China Securities (International) Corporate Finance Company Limited | 5 | 13% | 3% | 40% |
| Guotai Junan Capital Limited | 5 | 52% | 80% | 40% |
| CMB International Capital Limited | 3 | 59% | -15% | 33% |
| Goldman Sachs (Asia) L.L.C. | 3 | 35% | -0% | 33% |
| Morgan Stanley Asia Limited | 3 | -3% | 4% | 0% |

| Statistic | Raw log(1 + IR) | After window, A+H and size |
|---|---|---|
| Intraclass correlation across sponsors | -0.015 | -0.046 |
| ANOVA F (permutation p) | 0.88 (0.535) | 0.63 (0.731) |

- The residual test asks whether sponsor differences remain after controlling for the listing window, A+H and size. With few deals per sponsor and sponsors that often co-sponsor, a null result is weak evidence of no sponsor effect.
