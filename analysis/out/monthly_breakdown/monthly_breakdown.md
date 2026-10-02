# 2026 first-day returns by listing month (N = 113)

## 1. By listing month

| Month | N | Mean IR | Median IR | IR < 0 | IR > 100% | Fixed price | Median public subscription (x) | HSI 20d before prospectus | IPOs in prior 90 days |
|---|---|---|---|---|---|---|---|---|---|
| 2026-01 | 12 | 36% | 28% | 0% | 8% | 67% | 1,121 | 0.6% | 46 |
| 2026-02 | 11 | 41% | 12% | 0% | 18% | 64% | 570 | 5.7% | 47 |
| 2026-03 | 15 | 27% | 8% | 27% | 13% | 47% | 1,073 | -3.8% | 43 |
| 2026-04 | 8 | 126% | 89% | 0% | 50% | 62% | 1,120 | 0.5% | 32 |
| 2026-05 | 13 | 98% | 92% | 15% | 46% | 77% | 5,480 | 2.1% | 30 |
| 2026-06 | 24 | 79% | 46% | 25% | 38% | 67% | 1,492 | -5.3% | 36 |
| 2026-07 | 16 | 7% | 0% | 44% | 6% | 56% | 336 | -7.8% | 41 |
| 2026-08 | 2 | 32% | 32% | 0% | 0% | 50% | 1,720 | 7.5% | 50 |
| 2026-09 | 12 | 31% | -1% | 58% | 17% | 58% | 84 | -1.6% | 42 |

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
| Quarter dummies | 3 | 0.151 | 0.135 | 144.2 |
| Quarter dummies + route + sector | 15 | 0.301 | 0.201 | 146.2 |
| Hot window (Apr-Jun) dummy | 2 | 0.139 | 0.131 | 143.8 |
| Hot window (Apr-Jun) dummy + route + sector | 14 | 0.298 | 0.206 | 144.6 |
| Month dummies | 9 | 0.187 | 0.125 | 151.3 |
| Month dummies + route + sector | 21 | 0.351 | 0.210 | 149.8 |

- Hot-window coefficient (with route + sector): 0.36; s.e. 0.09 clustered by month, 0.11 heteroskedasticity-robust (HC3).

## 4. Tests

- Restricting month dummies to the hot-window dummy: F = 1.07, p = 0.388.
- Restricting month dummies to the quarter dummies: F = 1.18, p = 0.322.
- IR equal across Apr, May, Jun: Kruskal-Wallis p = 0.366.
- IR equal across Jan, Feb, Mar: Kruskal-Wallis p = 0.468.
- Mar vs Apr: Mann-Whitney p = 0.047; Jun vs Jul: Mann-Whitney p = 0.023.
- Hot window vs rest: mean IR 93% (n = 45) vs 27% (n = 68); Mann-Whitney p = 0.00017.

- Months with fewer than 6 deals: 2026-08 (N = 2). Their estimates are too thin to read individually.
