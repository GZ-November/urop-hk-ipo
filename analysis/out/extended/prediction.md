# Predictability of first-day returns, 2026 (N = 91, deals with a prior-IR value)

Out-of-sample R-squared is measured against predicting each held-out deal with the training-sample mean; 0 is no
better than the mean, negative is worse. In leave-one-month-out the held-out month's Apr-Jun label is treated as known,
which flatters the window dummy: a forecaster would not know in real time that April had started a hot regime.

| Model | Regressors | In-sample R-squared | Out-of-sample R-squared, leave one month out | Out-of-sample R-squared, leave one deal out |
|---|---|---|---|---|
| Mean only (null) | 0 | 0.000 | 0.000 | 0.000 |
| April-June dummy only | 1 | 0.157 | 0.164 | 0.138 |
| Prior-30-day IR only | 1 | 0.020 | -0.005 | -0.002 |
| Ex-ante issuer + market (no window) | 8 | 0.248 | 0.129 | 0.068 |
| Ex-ante + prior IR | 9 | 0.249 | 0.104 | 0.038 |
| M1: age, size, A+H + window | 4 | 0.243 | 0.171 | 0.142 |
| M3 baseline + window | 9 | 0.288 | 0.160 | 0.071 |

- The M3 baseline (leave-one-month-out 0.160) does no better than the window dummy alone (0.164); in-sample R-squared
  overstates it. Issuer and market variables without the window reach 0.129; prior-IPO returns add nothing (-0.005 alone).
- Most of the predictable variation in 2026 IR is the level shift between windows, and none of the variables tested forecasts that
  shift in real time. Any claim about issuer characteristics should be read against this ceiling.
