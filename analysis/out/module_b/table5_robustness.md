# Table 5 — Robustness of the baseline model (M3)

|  | Baseline (M3) | Raw return | Winsorized 1/99 | Drop top-3 returns | Median regression | Quarter FE | Bootstrap 95% CI (2000) |
|---|---|---|---|---|---|---|---|
| Intercept | -0.147 (0.926) | -0.202 (1.439) | -0.180 (0.916) | 0.072 (0.849) | 0.402 (0.606) | 0.115 (0.648) | [-1.526, 1.478] |
| ln firm age | 0.110 (0.189) | 0.121 (0.266) | 0.109 (0.189) | 0.116 (0.174) | -0.037 (0.081) | 0.092 (0.200) | [-0.191, 0.289] |
| ln offer size | 0.017 (0.064) | -0.005 (0.093) | 0.015 (0.064) | 0.005 (0.061) | -0.042 (0.060) | 0.059 (0.064) | [-0.081, 0.158] |
| A+H issuer | -0.313** (0.133) | -0.477** (0.206) | -0.313** (0.132) | -0.287** (0.125) | -0.125 (0.131) | -0.308** (0.128) | [-0.524, -0.043] |
| VC/PE-backed | 0.088 (0.157) | 0.159 (0.236) | 0.090 (0.157) | 0.053 (0.147) | 0.043 (0.120) | 0.106 (0.171) | [-0.176, 0.334] |
| Top-tier sponsor | 0.051 (0.100) | 0.102 (0.157) | 0.053 (0.099) | 0.077 (0.099) | 0.127 (0.092) | 0.039 (0.098) | [-0.144, 0.238] |
| Cornerstone allocation | -0.353 (0.393) | -0.828 (0.666) | -0.348 (0.389) | -0.291 (0.373) | -0.213 (0.287) | -0.437 (0.383) | [-1.084, 0.243] |
| HSI return, prior 20 days | 2.055** (0.965) | 2.549 (1.625) | 1.996** (0.938) | 2.340** (0.923) | 1.980** (0.878) |  | [0.231, 3.958] |
| IPO count, prior 90 days | 0.004 (0.014) | 0.010 (0.026) | 0.004 (0.014) | -0.002 (0.013) | -0.003 (0.012) |  | [-0.026, 0.031] |
| April-June hot window | 0.394** (0.191) | 0.732** (0.323) | 0.402** (0.187) | 0.275 (0.184) | 0.363** (0.146) |  | [0.026, 0.764] |
| 2026Q2 dummy |  |  |  |  |  | 0.257** (0.109) |  |
| 2026Q3 dummy |  |  |  |  |  | -0.243** (0.123) |  |
| N | 105 | 105 | 105 | 102 | 105 | 105 | 105 |
| R-squared | 0.264 | 0.277 | 0.270 | 0.248 | 0.229 (pseudo) | 0.250 |  |
| Specifications significant at 5% | A+H issuer 6/7; HSI return, prior 20 days 5/6; April-June hot window 5/6 |  |  |  |  |  |  |

- Dependent variable is ln(1 + first-day return) except 'Raw return' (return in decimal units; coefficients are not comparable in size).
- Median regression reports asymptotic standard errors; it estimates the effect on the typical IPO, not the mean.
- Quarter FE replaces the market variables and hot-window control with quarter dummies; other robustness checks use the baseline complete-case sample.
- Bootstrap: 2000 full-rank pairs resamples of the baseline sample, seed 20260929; 0 rank-deficient draws rejected.
- Significant at 5% in every specification that includes them (incl. the bootstrap interval): none. These p-values ignore clustering by listing month; see Table 6 for the wild cluster bootstrap.
