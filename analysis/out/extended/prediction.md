# Predictability of first-day returns, 2026 (N = 87, deals with a prior-IR value)

Out-of-sample R-squared is measured against predicting each held-out deal with the training-sample mean; 0 is no
better than the mean, negative is worse. In leave-one-month-out the held-out month's Apr-Jun label is treated as known,
which flatters the window dummy: a forecaster would not know in real time that April had started a hot regime.

| Model | Regressors | In-sample R-squared | Out-of-sample R-squared, leave one month out | Out-of-sample R-squared, leave one deal out |
|---|---|---|---|---|
| Mean only (null) | 0 | 0.000 | 0.000 | 0.000 |
| April-June dummy only | 1 | 0.143 | 0.133 | 0.123 |
| Prior-30-day IR only | 1 | 0.023 | 0.003 | -0.001 |
| Ex-ante issuer + market (no window) | 8 | 0.229 | 0.079 | 0.041 |
| Ex-ante + prior IR | 9 | 0.229 | 0.046 | 0.012 |
| M1: age, size, A+H + window | 4 | 0.218 | 0.122 | 0.112 |
| M3 baseline + window | 9 | 0.278 | 0.133 | 0.053 |

- The M3 baseline (leave-one-month-out 0.133) does no better than the window dummy alone (0.133); in-sample R-squared
  overstates it. Issuer and market variables without the window reach 0.079; prior-IPO returns add nothing (0.003 alone).
- Most of the predictable variation in 2026 IR is the level shift between windows, and none of the variables tested forecasts that
  shift in real time. Any claim about issuer characteristics should be read against this ceiling.
