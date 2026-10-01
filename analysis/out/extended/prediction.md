# Predictability of first-day returns, 2026 (N = 90, deals with a prior-IR value)

Out-of-sample R-squared is measured against predicting each held-out deal with the training-sample mean; 0 is no
better than the mean, negative is worse. In leave-one-month-out the held-out month's Apr-Jun label is treated as known,
which flatters the window dummy: a forecaster would not know in real time that April had started a hot regime.

| Model | Regressors | In-sample R-squared | Out-of-sample R-squared, leave one month out | Out-of-sample R-squared, leave one deal out |
|---|---|---|---|---|
| Mean only (null) | 0 | 0.000 | 0.000 | 0.000 |
| April-June dummy only | 1 | 0.153 | 0.142 | 0.133 |
| Prior-30-day IR only | 1 | 0.029 | 0.010 | 0.006 |
| Ex-ante issuer + market (no window) | 8 | 0.235 | 0.100 | 0.051 |
| Ex-ante + prior IR | 9 | 0.235 | 0.071 | 0.022 |
| M1: age, size, A+H + window | 4 | 0.225 | 0.143 | 0.129 |
| M3 baseline + window | 9 | 0.287 | 0.150 | 0.070 |

- The M3 baseline (leave-one-month-out 0.150) does no better than the window dummy alone (0.142); in-sample R-squared
  overstates it. Issuer and market variables without the window reach 0.100; prior-IPO returns add nothing (0.010 alone).
- Most of the predictable variation in 2026 IR is the level shift between windows, and none of the variables tested forecasts that
  shift in real time. Any claim about issuer characteristics should be read against this ceiling.
