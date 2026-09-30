# Table 4 — Determinants of underpricing, 2026 HK IPOs (N = 106)

|  | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| Intercept | 0.043 (0.427) | 0.021 (0.656) | 0.020 (0.891) | -0.664 (0.921) |
| ln firm age | 0.091 (0.172) | 0.076 (0.204) | 0.098 (0.195) | 0.127 (0.178) |
| ln offer size | -0.006 (0.052) | 0.018 (0.065) | 0.010 (0.063) | 0.101* (0.060) |
| A+H issuer | -0.347** (0.151) | -0.285* (0.152) | -0.304** (0.152) | -0.306** (0.127) |
| VC/PE-backed |  | 0.109 (0.149) | 0.096 (0.149) | 0.016 (0.142) |
| Top-tier sponsor |  | 0.045 (0.099) | 0.049 (0.099) | 0.075 (0.097) |
| Cornerstone allocation |  | -0.261 (0.390) | -0.294 (0.388) | -0.480 (0.346) |
| HSI return, prior 20 days |  |  | 1.736* (0.969) | 1.257 (0.935) |
| IPO count, prior 90 days |  |  | -0.000 (0.014) | 0.002 (0.014) |
| April-June hot window | 0.318*** (0.097) | 0.326*** (0.101) | 0.335* (0.183) | 0.274 (0.187) |
| ln subscription ratio |  |  |  | 0.090** (0.037) |
| N | 106 | 106 | 106 | 106 |
| R-squared | 0.226 | 0.238 | 0.268 | 0.322 |
| Adj. R-squared | 0.195 | 0.183 | 0.199 | 0.250 |
| Joint F-test, uncertainty (p) | 0.002 | 0.137 | 0.117 | 0.024 |
| Joint F-test, certification (p) |  | 0.653 | 0.682 | 0.406 |
| Joint F-test, market conditions (p) |  |  | 0.068 | 0.154 |
| Breusch-Pagan (p) | 0.002 | 0.006 | 0.010 | 0.020 |

- Dependent variable: ln(1 + first-day return). HC3 standard errors in parentheses; * p<0.10, ** p<0.05, *** p<0.01.
- Read a dummy coefficient b as a proportional change in the day-1 price ratio: exp(b) - 1.
- Adjusted R-squared across M1-M4: 0.195 -> 0.183 -> 0.199 -> 0.250.
- Most influential observations in M3 (Cook's distance): 2290.HK (0.53), 2720.HK (0.10), 2797.HK (0.08).
- M4 adds a demand variable measured at pricing; treat it as a channel check, not a causal estimate.
- All four models use the same finite complete-case sample, including the demand variable and listing month; see sample_selection.md for overlapping missing/invalid counts.
- With roughly 100 observations and up to 10 regressors, non-significance is weak evidence of no effect; the model has little power against moderate effects.
