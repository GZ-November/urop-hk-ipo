# Nested OLS, outcome = log(1 + first-day return), 2026

Coefficients with month-clustered standard errors in parentheses. Omitted groups: Conventional route, listed 2026Q1, not VC/PE-backed. Market variables are standardized (mean 0, s.d. 1) and measured before the prospectus date. * p<0.10, ** p<0.05, *** p<0.01.

## A. Route, quarter and backing

|  | (1) Route | (2) Quarter | (3) VC/PE backing | (4) Route + quarter | (5) Route + quarter + backing | (6) + controls |
|---|---|---|---|---|---|---|
| 18A biotech | 0.08 (0.16) |  |  | -0.01 (0.16) | -0.02 (0.17) | -0.00 (0.17) |
| 18C specialist tech | 0.05 (0.16) |  |  | 0.08 (0.17) | 0.06 (0.18) | 0.07 (0.18) |
| A+H (19A) | -0.34*** (0.11) |  |  | -0.26*** (0.10) | -0.20* (0.10) | -0.19* (0.12) |
| Listed 2026Q2 |  | 0.32*** (0.08) |  | 0.26*** (0.08) | 0.26*** (0.08) | 0.28*** (0.08) |
| Listed 2026Q3 |  | -0.15*** (0.05) |  | -0.14** (0.06) | -0.15** (0.06) | -0.19*** (0.07) |
| VC/PE-backed |  |  | 0.31*** (0.11) |  | 0.13 (0.19) | 0.14 (0.19) |
| ln(gross proceeds, HK$) |  |  |  |  |  | 0.07** (0.03) |
| Fixed price |  |  |  |  |  | -0.09 (0.10) |
| Cornerstone (share of base offer) |  |  |  |  |  | -0.43* (0.24) |
| N | 106 | 106 | 106 | 106 | 106 | 106 |
| R-squared | 0.12 | 0.15 | 0.07 | 0.22 | 0.23 | 0.25 |
| Adj. R-squared | 0.09 | 0.14 | 0.06 | 0.18 | 0.18 | 0.18 |

| Factor (model 5) | R-squared lost when dropped |
|---|---|
| Route | 0.030 |
| Quarter | 0.103 |
| VC/PE backing | 0.008 |

## B. Can market conditions replace the quarter?

|  | (5) Route + quarter + backing | (7) Market only | (8) Route + backing + market | (9) Route + backing + market + quarter |
|---|---|---|---|---|
| 18A biotech | -0.02 (0.17) |  | 0.04 (0.17) | -0.00 (0.18) |
| 18C specialist tech | 0.06 (0.18) |  | 0.03 (0.17) | 0.07 (0.18) |
| A+H (19A) | -0.20* (0.10) |  | -0.23** (0.11) | -0.21* (0.11) |
| Listed 2026Q2 | 0.26*** (0.08) |  |  | 0.26*** (0.08) |
| Listed 2026Q3 | -0.15** (0.06) |  |  | -0.11 (0.07) |
| VC/PE-backed | 0.13 (0.19) |  | 0.09 (0.18) | 0.11 (0.20) |
| HSI 20-day return before prospectus (z) |  | 0.11*** (0.04) | 0.10*** (0.03) | 0.06*** (0.02) |
| IPO count, prior 90 days (z) |  | -0.18*** (0.02) | -0.13*** (0.02) | -0.01 (0.04) |
| 1-month HIBOR (z) |  | 0.00 (0.03) | -0.00 (0.04) | 0.00 (0.03) |
| Banking aggregate balance (z) |  | 0.01 (0.02) | 0.01 (0.02) | 0.02 (0.02) |
| N | 106 | 106 | 106 | 106 |
| R-squared | 0.23 | 0.14 | 0.21 | 0.24 |
| Adj. R-squared | 0.18 | 0.11 | 0.14 | 0.17 |

| Factor (model 9) | R-squared lost when dropped |
|---|---|
| Route | 0.030 |
| VC/PE backing | 0.006 |
| Market variables (4) | 0.015 |
| Quarter | 0.039 |

- Nine listing months give few clusters, so the p-values are indicative only. Backing is identified only within Conventional and A+H issuers, because all 18A/18C issuers are backed.

- A coefficient b on log(1 + IR) is roughly a 100*b percent difference in (1 + IR).
