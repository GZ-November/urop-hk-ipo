# 2026 first-day returns by listing month (N = 106)

## 1. By listing month

| Month | N | Mean IR | Median IR | IR < 0 | IR > 100% | Fixed price | Median public subscription (x) | HSI 20d before prospectus | IPOs in prior 90 days |
|---|---|---|---|---|---|---|---|---|---|
| 2026-01 | 12 | 35% | 28% | 8% | 8% | 67% | 1,121 | 0.6% | 46 |
| 2026-02 | 11 | 35% | 3% | 27% | 18% | 64% | 570 | 5.7% | 47 |
| 2026-03 | 15 | 26% | 8% | 27% | 13% | 47% | 1,073 | -3.8% | 43 |
| 2026-04 | 8 | 122% | 89% | 12% | 50% | 62% | 1,120 | 0.5% | 32 |
| 2026-05 | 13 | 98% | 92% | 15% | 46% | 77% | 5,480 | 2.1% | 30 |
| 2026-06 | 24 | 79% | 46% | 29% | 38% | 67% | 1,492 | -5.3% | 36 |
| 2026-07 | 16 | 7% | 0% | 44% | 6% | 56% | 336 | -7.8% | 41 |
| 2026-08 | 2 | 32% | 32% | 0% | 0% | 50% | 1,720 | 7.5% | 50 |
| 2026-09 | 5 | 22% | -1% | 80% | 20% | 40% | 140 | 1.0% | 43 |

## 2. Longest gaps between consecutive listings

| Last listing before | Next listing | Days |
|---|---|---|
| 2026-02-13 | 2026-03-09 | 24 |
| 2026-03-31 | 2026-04-16 | 16 |
| 2026-07-10 | 2026-07-30 | 20 |
| 2026-08-07 | 2026-08-25 | 18 |

## 3. Time-structure models for log(1 + IR)

| Model | Parameters | R-squared | Adj. R-squared | AIC |
|---|---|---|---|---|
| Quarter dummies | 3 | 0.155 | 0.138 | 139.1 |
| Quarter dummies + route + sector | 15 | 0.333 | 0.230 | 138.1 |
| Hot window (Apr-Jun) dummy | 2 | 0.142 | 0.134 | 138.6 |
| Hot window (Apr-Jun) dummy + route + sector | 14 | 0.328 | 0.234 | 136.7 |
| Month dummies | 9 | 0.184 | 0.117 | 147.4 |
| Month dummies + route + sector | 21 | 0.369 | 0.220 | 144.1 |

- Hot-window coefficient (with route + sector): 0.38; s.e. 0.08 clustered by month, 0.12 heteroskedasticity-robust (HC3).

## 4. Tests

- Restricting month dummies to the hot-window dummy: F = 0.78, p = 0.606.
- Restricting month dummies to the quarter dummies: F = 0.82, p = 0.559.
- IR equal across Apr, May, Jun: Kruskal-Wallis p = 0.443.
- IR equal across Jan, Feb, Mar: Kruskal-Wallis p = 0.452.
- Mar vs Apr: Mann-Whitney p = 0.101; Jun vs Jul: Mann-Whitney p = 0.024.
- Hot window vs rest: mean IR 92% (n = 45) vs 24% (n = 61); Mann-Whitney p = 0.00038.

- Months with 2 or 5 deals (Aug, Sep) are too thin to read individually.
