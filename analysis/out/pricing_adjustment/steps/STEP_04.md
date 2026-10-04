# Topic 1 — Step 4: robust estimation of the price stages

Prepared 4 October 2026. Cutoff: 30 September 2026. Working research note,
not a final report. All estimates retain the same 43 range-priced IPOs.
No dates, prices or source fields are changed.

## Question

Does the positive revision–return association persist when we change the
estimator rather than delete the firms with missing pricing-date proxies?
Does estimator sensitivity occur mainly at opening or during first-day trading?

## Design and interpretation

The four existing control designs are retained: revision alone; quarter
controls; launch size and A+H status; subscription-period market movement and
launch size. Every design uses all 43 firms for every outcome and estimator.
No specification is selected for its sign or significance.

Three estimators are compared:

- OLS with HC3 standard errors and a t reference: the existing conditional-mean
  model, reproduced as the benchmark.
- Median regression, quantile 0.5: a conditional-median model that uses absolute
  loss. It does not estimate the same quantity as conditional-mean OLS.
- Huber regression, tuning constant 1.345 and MAD scale: residual-based robust
  estimation that reduces the contribution of large residuals while retaining
  every firm. Its fitted weights are not application weights or probabilities.

The outcomes are log offer-to-close, log offer-to-open, log open-to-close and
log HSI-adjusted close return. The market adjustment retains the complete
subscription-close window. No actual pricing date is assumed.

## Main comparison: quarter controls

| Outcome | OLS coefficient | OLS HC3 SE | Median coefficient | Median SE | Huber coefficient | Huber SE |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Offer to close | 1.598 | 1.372 | 0.870 | 1.528 | 1.890 | 1.154 |
| Offer to opening | 0.874 | 1.098 | 0.489 | 1.126 | 1.053 | 0.904 |
| Opening to close | 0.723 | 0.358 | 0.699 | 0.354 | 0.528 | 0.287 |
| HSI-adjusted close | 1.554 | 1.380 | 1.076 | 1.546 | 1.866 | 1.168 |

N=43 in every cell. Coefficients are log-return units per one unit of fractional
revision. A +10 pp revision implies a fitted log-return change of 0.1 times the
coefficient; the corresponding simple-return change is not the same number of
percentage points.

Median SE uses the QuantReg robust asymptotic sparsity estimate, Epanechnikov
kernel and Hall–Sheather bandwidth. Huber SE uses RLM H1 asymptotic covariance.
Neither is HC3 or month-cluster-robust inference. Their small-sample validity is
limited, so no new significance stars or robust-estimator p-value claims are made.
The main OLS close p-value remains 0.251. Previous wild-cluster and multiple-test
results are not replaced by these sensitivity estimates.

The positive sign persists in this comparison, but the effect size is uncertain.
The quarter-controlled median close estimate is smaller than the OLS estimate.
The Huber close estimate is moderately larger. Neither reproduces the 3.419
close coefficient obtained by excluding all seven missing-proxy firms.

## All four declared designs

| Controls | Close: OLS / median / Huber | Opening: OLS / median / Huber | Intraday: OLS / median / Huber |
| --- | --- | --- | --- |
| Revision only | 1.396 / 2.664 / 1.569 | 0.669 / 1.364 / 0.720 | 0.727 / 0.429 / 0.663 |
| Quarter controls | 1.598 / 0.870 / 1.890 | 0.874 / 0.489 / 1.053 | 0.723 / 0.699 / 0.528 |
| Launch size and A+H | 1.502 / 1.429 / 1.587 | 0.734 / 0.425 / 0.794 | 0.768 / 0.827 / 0.700 |
| Subscription market and launch size | 1.679 / 2.617 / 1.812 | 0.893 / 1.529 / 0.917 | 0.786 / 0.795 / 0.732 |

All signs in this table are positive. Median close coefficients nevertheless
range from 0.870 to 2.664 across controls; their size is sensitive to conditioning.
The unadjusted median is not evidence that the adjusted median must be large.
These are post-exploration sensitivity checks, not independently preregistered
confirmations or a set of interchangeable estimates.

The output retains all 48 models, including all market-adjusted close models,
full coefficients, warnings and iteration counts. No fit produces a convergence
warning. This is computational convergence, not assurance of precise inference.

## What Huber estimation does to the two influential firms

| Issuer | Close weight | Opening weight | Intraday weight |
| --- | ---: | ---: | ---: |
| 2672.HK | 0.624 | 0.595 | 0.983 |
| 3231.HK | 0.615 | 0.551 | 1.000 |

Quarter-controlled Huber estimation moderately reduces their close/opening
weights. It retains nearly full intraday weights. This is consistent with the
Step 3 diagnosis: these firms' unusual revision–return pattern is concentrated
at opening. The weights do not establish that the observations are erroneous,
and they do not assign an economic cause to the opening gains.

## Stage arithmetic: an important limit

Log close return equals log opening return plus log intraday return. With a
common linear OLS design, the fitted coefficients obey the same identity.

Separately fitted median and Huber models need not obey coefficient addition.
The median of a sum is not generally the sum of medians. Huber models also use
outcome-specific residual weights. Their stage slopes cannot be added to form
an exact contribution decomposition. The Step 3 exact opening-stage share is
an OLS deletion-accounting result; it is not transferred to these estimators.

## Verification

All 16 median fits are checked against independent linear-programming solutions
of the median absolute-loss problem. The largest objective discrepancy is
approximately 0.00000041, within the declared numerical tolerance. The check
validates the loss minimum, not coefficient uniqueness or confidence intervals.

All OLS coefficients match the earlier study. Their stage identities hold.
All fits retain 43 distinct firms, with no missing required model inputs.
Convergence and maintained-source lint checks pass. Huber weights for every
issuer and every model are retained for inspection.

## Research conclusion and next step

The positive sign is not removed by changing from OLS to median or Huber
estimation on the full sample. However, its size and uncertainty remain
substantial. This step does not justify a strong partial-adjustment claim or
exclusion of the seven firms with missing dates.

Next, assess inference with only nine listing-month clusters, using a
deterministic leave-one-month-out analysis and cluster-jackknife uncertainty.
This addresses common monthly shocks and checks whether apparent stage evidence
is concentrated in particular months. Actual pricing dates remain a separate
evidence gap. The topic is not yet presented as a completed final report.

## Reproduction

Run `python analysis/pricing_robust_stages_2026.py` from the repository root.

- `step04_estimates.csv`: all 48 models and estimator-specific uncertainty labels.
- `step04_coefficients.csv`: every fitted coefficient.
- `step04_huber_weights.csv`: weights and residuals for every issuer.
- `step04_weight_groups.csv`: weights by proxy availability.
- `step04_median_objective_checks.csv`: independent optimisation checks.
- `step04_manifest.json`: specification, versions, source hashes and limits.
