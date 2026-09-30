# Tails of the first-day return distribution, 2026 (N = 102, M3 specification)

log(1 + IR) is bimodal: 21% of deals break issue while 25% more than double.
A mean regression averages over both, so this section asks where in the distribution each variable acts.

## 1. Quantile regressions of log(1 + IR)

Cells: coefficient [95% pairs-bootstrap interval]; * = interval excludes zero. 1000 draws, seed 20260930,
0 rank-deficient draws rejected in total. The OLS column repeats the M3 mean coefficients (HC3).

| Variable | OLS mean | q10 | q25 | q50 | q75 | q90 |
|---|---|---|---|---|---|---|
| ln firm age | 0.11 | 0.11 [-0.22, 0.48] | 0.25 [-0.25, 0.36] | -0.09 [-0.22, 0.34] | -0.08 [-0.34, 0.23] | -0.34 [-0.46, 0.30] |
| ln offer size | -0.00 | -0.04 [-0.11, 0.17] | 0.02 [-0.10, 0.17] | -0.05 [-0.17, 0.12] | -0.04 [-0.19, 0.20] | -0.17 [-0.27, 0.24] |
| A+H issuer | -0.30* | -0.01 [-0.50, 0.16] | -0.30 [-0.53, 0.14] | -0.07 [-0.56, 0.10] | -0.19 [-0.65, 0.17] | 0.05 [-0.88, 0.20] |
| VC/PE-backed | 0.09 | -0.02 [-0.25, 0.45] | 0.12 [-0.17, 0.38] | 0.06 [-0.13, 0.36] | 0.04 [-0.19, 0.40] | 0.19 [-0.26, 0.44] |
| Top-tier sponsor | 0.06 | 0.04 [-0.38, 0.25] | -0.01 [-0.24, 0.29] | 0.13 [-0.03, 0.34] | 0.15 [-0.11, 0.33] | 0.00 [-0.32, 0.33] |
| Cornerstone allocation | -0.29 | 0.77 [-0.56, 1.33] | 0.18 [-0.77, 1.16] | -0.16 [-1.30, 0.30] | -0.98 [-1.78, 0.12] | -0.64 [-2.12, 0.69] |
| HSI return, prior 20 days | 2.09** | 2.64 [-0.06, 6.14] | 1.38 [-0.37, 4.75] | 1.96 [-0.45, 3.50] | 1.35 [-0.72, 3.55] | 2.69 [-1.27, 5.16] |
| April-June hot window | 0.38* | 0.40 [-0.59, 0.77] | 0.20 [-0.31, 0.87] | 0.37 [0.05, 0.81]* | 0.41 [0.10, 0.81]* | 0.57 [-0.02, 0.89] |

- Bootstrap intervals that exclude zero: April-June hot window: q50, q75. Everything else is compatible with no effect at that quantile.
- The cornerstone point estimates drift from +0.77 at q10 to -0.64 at q90 (fewer extreme pops with
  larger anchor share), but the q90 bootstrap interval includes zero (p = 0.27). Asymptotic quantile standard errors would
  suggest significance; the bootstrap does not support it. Treat as a hypothesis for a larger sample, not a finding.
- The April-June coefficient is positive at every quantile and A+H is negative at every quantile, matching the OLS signs; with
  106 observations the per-quantile intervals are wide, so treat this as a distributional description.

## 2. PPML on 1 + IR (mean multiplier, no log re-transformation bias)

| Variable | Multiplier on 1 + IR, exp(b) | HC3 p |
|---|---|---|
| ln firm age | 1.07 | 0.524 |
| ln offer size | 0.98 | 0.684 |
| A+H issuer | 0.72 | 0.008 |
| VC/PE-backed | 1.10 | 0.491 |
| Top-tier sponsor | 1.06 | 0.513 |
| Cornerstone allocation | 0.64 | 0.191 |
| HSI return, prior 20 days | 5.13 | 0.049 |
| April-June hot window | 1.56 | 0.011 |

## 3. Break and pop events (logit, reduced regressors, HC3)

- **IR < 0 (break)**: 21 of 102 deals (21%).
- **IR > 50%**: 40 of 102 deals (39%).
- **IR > 100%**: 26 of 102 deals (25%).

Odds ratios (* p<0.10, ** p<0.05, *** p<0.01); cornerstone allocation is a 0-1 share so its odds ratio is per 100 percentage points,
ln offer size per ln HK$bn. Events are few (about 5 per regressor), so read these as descriptive.

| Variable | IR < 0 (break) | IR > 50% | IR > 100% |
|---|---|---|---|
| A+H issuer | 0.93 | 0.15** | 0.10** |
| VC/PE-backed | 0.76 | 2.02 | 0.46 |
| Cornerstone allocation | 0.05 | 0.09 | 1.51 |
| April-June hot window | 0.83 | 5.43*** | 5.21*** |
| ln offer size | 1.56 | 1.22 | 0.53 |

- Fisher exact: VC/PE backing vs break issue p = 0.5336 (odds ratio 0.67); April-June vs IR > 100% p = 0.0011 (odds ratio 5.22).
- VC/PE-backed deals are much less likely to break; the non-VC/PE group is mostly A+H and large state-linked issuers,
  so this is partly the A+H story; the A+H control is in the model.
