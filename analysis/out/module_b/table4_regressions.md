# Table 4 — Determinants of underpricing, 2026 HK IPOs (N = 102)

|  | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| Intercept | 0.035 (0.437) | 0.009 (0.662) | -0.254 (0.957) | -1.041 (0.963) |
| ln firm age | 0.094 (0.176) | 0.075 (0.207) | 0.096 (0.196) | 0.131 (0.177) |
| ln offer size | -0.010 (0.055) | 0.015 (0.069) | 0.002 (0.065) | 0.097 (0.061) |
| A+H issuer | -0.347** (0.153) | -0.284* (0.155) | -0.309** (0.155) | -0.316** (0.126) |
| VC/PE-backed |  | 0.124 (0.158) | 0.145 (0.166) | 0.065 (0.158) |
| Top-tier sponsor |  | 0.044 (0.101) | 0.058 (0.101) | 0.077 (0.099) |
| Cornerstone allocation |  | -0.268 (0.393) | -0.323 (0.389) | -0.509 (0.343) |
| HSI return, prior 20 days |  |  | 1.894* (0.983) | 1.379 (0.948) |
| IPO count, prior 90 days |  |  | 0.005 (0.015) | 0.009 (0.015) |
| April-June hot window | 0.319*** (0.098) | 0.330*** (0.103) | 0.403** (0.197) | 0.348* (0.197) |
| ln subscription ratio |  |  |  | 0.095** (0.038) |
| N | 102 | 102 | 102 | 102 |
| R-squared | 0.215 | 0.228 | 0.267 | 0.327 |
| Adj. R-squared | 0.183 | 0.170 | 0.196 | 0.253 |
| Joint F-test, uncertainty (p) | 0.002 | 0.138 | 0.097 | 0.016 |
| Joint F-test, certification (p) |  | 0.658 | 0.589 | 0.365 |
| Joint F-test, market conditions (p) |  |  | 0.041 | 0.074 |
| Breusch-Pagan (p) | 0.004 | 0.011 | 0.019 | 0.033 |

- Dependent variable: ln(1 + first-day return). HC3 standard errors in parentheses; * p<0.10, ** p<0.05, *** p<0.01.
- Read a dummy coefficient b as a proportional change in the day-1 price ratio: exp(b) - 1.
- Adjusted R-squared across M1-M4: 0.183 -> 0.170 -> 0.196 -> 0.253.
- Most influential observations in M3 (Cook's distance): 2290.HK (0.50), 2720.HK (0.10), 2797.HK (0.10).
- M4 adds a demand variable measured at pricing; treat it as a channel check, not a causal estimate.
- All four models use the same finite complete-case sample, including the demand variable and listing month; see sample_selection.md for overlapping missing/invalid counts.
- With roughly 100 observations and up to 10 regressors, non-significance is weak evidence of no effect; the model has little power against moderate effects.
