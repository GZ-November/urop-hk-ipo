# Tails of the first-day return distribution, 2026 (N = 106, M3 specification)

log(1 + IR) is bimodal: 27% of deals break issue while 25% more than double.
A mean regression averages over both, so this section asks where in the distribution each variable acts.

## 1. Quantile regressions of log(1 + IR)

Cells: coefficient [95% pairs-bootstrap interval]; * = interval excludes zero. 1000 draws, seed 20260930,
0 rank-deficient draws rejected in total. The OLS column repeats the M3 mean coefficients (HC3).

| Variable | OLS mean | q10 | q25 | q50 | q75 | q90 |
|---|---|---|---|---|---|---|
| ln firm age | 0.10 | 0.02 [-0.29, 0.41] | 0.23 [-0.29, 0.34] | -0.13 [-0.24, 0.35] | -0.04 [-0.28, 0.28] | -0.00 [-0.39, 0.32] |
| ln offer size | 0.01 | 0.12 [-0.08, 0.24] | 0.03 [-0.09, 0.19] | -0.04 [-0.16, 0.15] | -0.03 [-0.17, 0.23] | 0.03 [-0.22, 0.24] |
| A+H issuer | -0.30** | -0.09 [-0.53, 0.17] | -0.32 [-0.53, 0.11] | -0.09 [-0.55, 0.09] | -0.28 [-0.67, 0.13] | -0.34 [-0.93, 0.19] |
| VC/PE-backed | 0.10 | 0.27 [-0.16, 0.49] | 0.20 [-0.16, 0.41] | 0.04 [-0.16, 0.36] | -0.05 [-0.24, 0.35] | -0.10 [-0.29, 0.35] |
| Top-tier sponsor | 0.05 | -0.14 [-0.44, 0.22] | -0.06 [-0.30, 0.27] | 0.10 [-0.06, 0.33] | 0.06 [-0.11, 0.33] | 0.16 [-0.35, 0.29] |
| Cornerstone allocation | -0.29 | 0.50 [-0.77, 1.19] | 0.08 [-0.79, 0.98] | -0.17 [-1.30, 0.43] | -0.82 [-1.78, 0.15] | -1.25 [-2.09, 0.70] |
| HSI return, prior 20 days | 1.74* | 1.57 [-0.43, 5.87] | 0.67 [-0.99, 4.53] | 1.94 [-0.94, 3.29] | 1.06 [-1.14, 3.25] | 1.68 [-1.46, 4.64] |
| April-June hot window | 0.33* | 0.11 [-0.61, 0.77] | 0.27 [-0.28, 0.83] | 0.34 [-0.03, 0.79] | 0.30 [0.05, 0.73]* | 0.52 [-0.06, 0.80] |

- Bootstrap intervals that exclude zero: April-June hot window: q75. Everything else is compatible with no effect at that quantile.
- The cornerstone point estimates drift from +0.50 at q10 to -1.25 at q90 (fewer extreme pops with
  larger anchor share), but the q90 bootstrap interval includes zero (p = 0.29). Asymptotic quantile standard errors would
  suggest significance; the bootstrap does not support it. Treat as a hypothesis for a larger sample, not a finding.
- The April-June coefficient is positive at every quantile and A+H is negative at every quantile, matching the OLS signs; with
  106 observations the per-quantile intervals are wide, so treat this as a distributional description.

## 2. PPML on 1 + IR (mean multiplier, no log re-transformation bias)

| Variable | Multiplier on 1 + IR, exp(b) | HC3 p |
|---|---|---|
| ln firm age | 1.06 | 0.583 |
| ln offer size | 0.99 | 0.828 |
| A+H issuer | 0.72 | 0.007 |
| VC/PE-backed | 1.10 | 0.455 |
| Top-tier sponsor | 1.06 | 0.537 |
| Cornerstone allocation | 0.64 | 0.184 |
| HSI return, prior 20 days | 4.05 | 0.093 |
| April-June hot window | 1.51 | 0.014 |

## 3. Break and pop events (logit, reduced regressors, HC3)

- **IR < 0 (break)**: 29 of 106 deals (27%).
- **IR > 50%**: 40 of 106 deals (38%).
- **IR > 100%**: 26 of 106 deals (25%).

Odds ratios (* p<0.10, ** p<0.05, *** p<0.01); cornerstone allocation is a 0-1 share so its odds ratio is per 100 percentage points,
ln offer size per ln HK$bn. Events are few (about 5 per regressor), so read these as descriptive.

| Variable | IR < 0 (break) | IR > 50% | IR > 100% |
|---|---|---|---|
| A+H issuer | 1.22 | 0.15** | 0.10** |
| VC/PE-backed | 0.22** | 2.13 | 0.47 |
| Cornerstone allocation | 0.05 | 0.08 | 1.51 |
| April-June hot window | 0.83 | 5.54*** | 5.27*** |
| ln offer size | 1.42 | 1.22 | 0.53 |

- Fisher exact: VC/PE backing vs break issue p = 0.0010 (odds ratio 0.18); April-June vs IR > 100% p = 0.0005 (odds ratio 5.64).
- VC/PE-backed deals are much less likely to break; the non-VC/PE group is mostly A+H and large state-linked issuers,
  so this is partly the A+H story; the A+H control is in the model.
