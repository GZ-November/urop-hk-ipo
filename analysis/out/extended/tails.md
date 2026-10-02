# Tails of the first-day return distribution, 2026 (N = 105, M3 specification)

The first-day-return distribution has losses and large gains: 21% of deals break issue while 25% more than double.
A mean regression averages over both, so this section asks where in the distribution each variable acts.

## 1. Quantile regressions of log(1 + IR)

Cells: coefficient [95% pairs-bootstrap interval]; * = interval excludes zero. 1000 draws, seed 20260930,
0 rank-deficient draws rejected in total. The OLS column repeats the M3 mean coefficients (HC3).

| Variable | OLS mean | q10 | q25 | q50 | q75 | q90 |
|---|---|---|---|---|---|---|
| ln firm age | 0.11 | 0.11 [-0.23, 0.40] | 0.27 [-0.22, 0.34] | -0.04 [-0.21, 0.31] | -0.07 [-0.30, 0.25] | 0.05 [-0.47, 0.32] |
| ln offer size | 0.02 | 0.04 [-0.08, 0.20] | 0.03 [-0.09, 0.17] | -0.04 [-0.13, 0.15] | -0.01 [-0.17, 0.24] | 0.06 [-0.27, 0.26] |
| A+H issuer | -0.31** | -0.11 [-0.47, 0.18] | -0.26 [-0.49, 0.09] | -0.12 [-0.57, 0.07] | -0.21 [-0.69, 0.13] | -0.40 [-0.94, 0.18] |
| VC/PE-backed | 0.09 | -0.00 [-0.28, 0.47] | 0.13 [-0.18, 0.39] | 0.04 [-0.16, 0.35] | 0.04 [-0.23, 0.40] | -0.14 [-0.28, 0.43] |
| Top-tier sponsor | 0.05 | -0.03 [-0.39, 0.24] | -0.02 [-0.25, 0.25] | 0.13 [-0.07, 0.32] | 0.14 [-0.10, 0.33] | 0.16 [-0.35, 0.33] |
| Cornerstone allocation | -0.35 | 0.54 [-0.65, 1.16] | 0.02 [-0.83, 1.00] | -0.21 [-1.35, 0.36] | -1.03 [-1.84, 0.05] | -1.30 [-2.12, 0.69] |
| HSI return, prior 20 days | 2.05** | 2.18 [-0.16, 6.07] | 1.43 [-0.45, 4.64] | 1.98 [-0.42, 3.66] | 1.45 [-0.60, 3.66] | 1.52 [-0.95, 6.08] |
| April-June hot window | 0.39** | 0.16 [-0.63, 0.78] | 0.28 [-0.28, 0.79] | 0.36 [0.01, 0.84]* | 0.40 [0.11, 0.85]* | 0.51 [-0.03, 0.89] |

- Bootstrap intervals that exclude zero: April-June hot window: q50, q75. Everything else is compatible with no effect at that quantile.
- The cornerstone point estimates drift from +0.54 at q10 to -1.30 at q90 (fewer extreme pops with
  larger anchor share), but the q90 bootstrap interval includes zero (p = 0.24). Asymptotic quantile standard errors would
  suggest significance; the bootstrap does not support it. Treat as a hypothesis for a larger sample, not a finding.
- The quantile estimates use 105 observations. Read their signs and bootstrap intervals in the table;
  wide intervals limit inference about differences across the return distribution.

## 2. PPML on 1 + IR (mean multiplier, no log re-transformation bias)

| Variable | Multiplier on 1 + IR, exp(b) | HC3 p |
|---|---|---|
| ln firm age | 1.07 | 0.512 |
| ln offer size | 1.00 | 0.976 |
| A+H issuer | 0.71 | 0.002 |
| VC/PE-backed | 1.10 | 0.502 |
| Top-tier sponsor | 1.05 | 0.548 |
| Cornerstone allocation | 0.60 | 0.128 |
| HSI return, prior 20 days | 5.10 | 0.052 |
| April-June hot window | 1.59 | 0.007 |

## 3. Break and pop events (logit, reduced regressors, HC3)

- **IR < 0 (break)**: 22 of 105 deals (21%).
- **IR > 50%**: 40 of 105 deals (38%).
- **IR > 100%**: 26 of 105 deals (25%).

Odds ratios (* p<0.10, ** p<0.05, *** p<0.01); cornerstone allocation is a 0-1 share so its odds ratio is per 100 percentage points,
ln offer size per ln HK$bn. Events are few (about 5 per regressor), so read these as descriptive.

| Variable | IR < 0 (break) | IR > 50% | IR > 100% |
|---|---|---|---|
| A+H issuer | 1.52 | 0.12*** | 0.11** |
| VC/PE-backed | 0.84 | 1.78 | 0.56 |
| Cornerstone allocation | 0.07 | 0.05* | 0.99 |
| April-June hot window | 0.82 | 6.24*** | 5.24*** |
| ln offer size | 1.20 | 1.46 | 0.58 |

- Fisher exact: VC/PE backing vs break issue p = 0.5405 (odds ratio 0.69); April-June vs IR > 100% p = 0.0005 (odds ratio 5.53).
- The VC/PE break-issue association must be assessed from the logit and Fisher tests above, rather than inferred from backing alone.
  Backing and listing route are selected characteristics; the A+H control does not establish a causal certification effect.
