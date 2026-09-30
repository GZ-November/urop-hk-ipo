# Table 4 — Determinants of underpricing, 2026 HK IPOs (N = 102)

|  | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| Intercept | 0.013 (0.431) | 0.014 (0.659) | -0.150 (0.939) | -0.982 (0.937) |
| ln firm age | 0.104 (0.173) | 0.090 (0.205) | 0.112 (0.194) | 0.149 (0.173) |
| ln offer size | -0.011 (0.055) | 0.010 (0.069) | -0.004 (0.065) | 0.097 (0.060) |
| A+H issuer | -0.313** (0.150) | -0.274* (0.156) | -0.298* (0.154) | -0.305** (0.123) |
| VC/PE-backed |  | 0.073 (0.153) | 0.090 (0.157) | 0.007 (0.146) |
| Top-tier sponsor |  | 0.043 (0.101) | 0.056 (0.101) | 0.076 (0.098) |
| Cornerstone allocation |  | -0.235 (0.394) | -0.291 (0.390) | -0.488 (0.343) |
| HSI return, prior 20 days |  |  | 2.092** (0.966) | 1.548* (0.928) |
| IPO count, prior 90 days |  |  | 0.003 (0.015) | 0.007 (0.014) |
| April-June hot window | 0.320*** (0.097) | 0.329*** (0.102) | 0.381* (0.196) | 0.324* (0.196) |
| ln subscription ratio |  |  |  | 0.101*** (0.038) |
| N | 102 | 102 | 102 | 102 |
| R-squared | 0.203 | 0.211 | 0.257 | 0.326 |
| Adj. R-squared | 0.171 | 0.152 | 0.184 | 0.252 |
| Joint F-test, uncertainty (p) | 0.006 | 0.177 | 0.123 | 0.021 |
| Joint F-test, certification (p) |  | 0.802 | 0.728 | 0.425 |
| Joint F-test, market conditions (p) |  |  | 0.025 | 0.050 |
| Breusch-Pagan (p) | 0.002 | 0.010 | 0.012 | 0.018 |

- Dependent variable: ln(1 + first-day return). HC3 standard errors in parentheses; * p<0.10, ** p<0.05, *** p<0.01.
- Read a dummy coefficient b as a proportional change in the day-1 price ratio: exp(b) - 1.
- Adjusted R-squared across M1-M4: 0.171 -> 0.152 -> 0.184 -> 0.252.
- Most influential observations in M3 (Cook's distance): 2290.HK (0.51), 2797.HK (0.09), 2720.HK (0.09).
- M4 adds a demand variable measured at pricing; treat it as a channel check, not a causal estimate.
- All four models use the same finite complete-case sample, including the demand variable and listing month; see sample_selection.md for overlapping missing/invalid counts.
- With roughly 100 observations and up to 10 regressors, non-significance is weak evidence of no effect; the model has little power against moderate effects.
