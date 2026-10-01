# Table 4 — Determinants of underpricing, 2026 HK IPOs (N = 105)

|  | M1 | M2 | M3 | M4 |
|---|---|---|---|---|
| Intercept | -0.003 (0.407) | 0.036 (0.658) | -0.147 (0.926) | -0.898 (0.910) |
| ln firm age | 0.106 (0.164) | 0.090 (0.201) | 0.110 (0.189) | 0.141 (0.170) |
| ln offer size | 0.003 (0.049) | 0.036 (0.066) | 0.017 (0.064) | 0.100* (0.056) |
| A+H issuer | -0.326** (0.132) | -0.296** (0.129) | -0.313** (0.133) | -0.309*** (0.107) |
| VC/PE-backed |  | 0.066 (0.153) | 0.088 (0.157) | 0.002 (0.144) |
| Top-tier sponsor |  | 0.036 (0.100) | 0.051 (0.100) | 0.073 (0.096) |
| Cornerstone allocation |  | -0.313 (0.395) | -0.353 (0.393) | -0.499 (0.348) |
| HSI return, prior 20 days |  |  | 2.055** (0.965) | 1.507 (0.929) |
| IPO count, prior 90 days |  |  | 0.004 (0.014) | 0.007 (0.014) |
| April-June hot window | 0.328*** (0.095) | 0.342*** (0.100) | 0.394** (0.191) | 0.327* (0.192) |
| ln subscription ratio |  |  |  | 0.095*** (0.032) |
| N | 105 | 105 | 105 | 105 |
| R-squared | 0.209 | 0.220 | 0.264 | 0.335 |
| Adj. R-squared | 0.178 | 0.163 | 0.194 | 0.264 |
| Joint F-test, uncertainty (p) | 0.003 | 0.060 | 0.058 | 0.008 |
| Joint F-test, certification (p) |  | 0.749 | 0.674 | 0.427 |
| Joint F-test, market conditions (p) |  |  | 0.026 | 0.058 |
| Breusch-Pagan (p) | 0.001 | 0.006 | 0.009 | 0.017 |

- Dependent variable: ln(1 + first-day return). HC3 standard errors in parentheses; * p<0.10, ** p<0.05, *** p<0.01.
- Read a dummy coefficient b as a proportional change in the day-1 price ratio: exp(b) - 1.
- Adjusted R-squared across M1-M4: 0.178 -> 0.163 -> 0.194 -> 0.264.
- Most influential observations in M3 (Cook's distance): 2290.HK (0.53), 2720.HK (0.10), 2797.HK (0.10).
- M4 adds a demand variable measured at pricing; treat it as a channel check, not a causal estimate.
- All four models use the same finite complete-case sample, including the demand variable and listing month; see sample_selection.md for overlapping missing/invalid counts.
- With roughly 100 observations and up to 10 regressors, non-significance is weak evidence of no effect; the model has little power against moderate effects.
