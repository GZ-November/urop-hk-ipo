# Contractual lockup expiry and stabilization end, 2026 (HSI-adjusted, from cached daily bars)

Event day 0 is the first trading day on or after the event date; CAR is the sum of daily stock returns minus HSI returns over the window.
The **placebo p** re-draws one non-event day per issuer from the same issuer's own history, between 11 and 30 trading days from the true
event (so the volatility regime is similar), 5000 times. It calibrates drift and cross-issuer dependence that a plain t-test ignores.
The placebo compares the cross-sectional t-statistic of each draw with the observed one, so a window whose returns are unusually dispersed (event-induced variance) is not mistaken for a shifted mean.
Turnover rows compare mean turnover on days [0,+5] to days [-25,-6] (log ratio; 0 = no change).

## 1. Contractual lockup expiry (earliest cornerstone unlock date, else controlling-shareholder date)

Only observed expiry dates with full return or turnover windows are included (35 issuers at most; N varies by window).
The dates follow the stored contractual expiry fields, rather than a uniform listing-date-plus-six-month assumption.
Coincident cornerstone and controlling-shareholder dates are counted as one event, not two.

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.7% | -3.1% | -1.47 | 0.053 | 0.169 | 65% |
| [0,+5] | 29 | -2.5% | -0.4% | -1.14 | 0.624 | 0.276 | 55% |
| [-5,+5] | 29 | -5.6% | -4.9% | -1.62 | 0.092 | 0.100 | 69% |
| [-5,-1] | 35 | -3.3% | -2.9% | -1.64 | 0.075 | 0.139 | 66% |
| Turnover [0,+5] vs [-25,-6], median log ratio | 29 | 0.18 | 0.12 | 1.19 | 0.275 | 0.004 | 41% |

Robustness, HSTECH-adjusted:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.7% | -2.3% | -1.54 | 0.076 | 0.087 | 65% |
| [0,+5] | 29 | -1.5% | -0.0% | -0.70 | 0.882 | 0.295 | 52% |
| [-5,+5] | 29 | -5.1% | -3.3% | -1.51 | 0.121 | 0.045 | 72% |
| [-5,-1] | 35 | -3.6% | -3.3% | -1.78 | 0.075 | 0.042 | 60% |
| Turnover [0,+5] vs [-25,-6], median log ratio | 29 | 0.18 | 0.12 | 1.19 | 0.275 | 0.004 | 41% |

## 2. End of the stabilization period

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -0.7% | -1.5% | -0.54 | 0.468 | 0.844 | 58% |
| [0,+5] | 31 | -1.2% | -2.5% | -0.44 | 0.468 | 0.936 | 55% |
| [-5,+5] | 31 | -2.2% | -0.7% | -0.64 | 0.706 | 0.524 | 52% |
| [-5,-1] | 31 | -1.0% | -0.6% | -0.44 | 0.581 | 0.528 | 58% |

Split by whether stabilizing purchases occurred (their number is small):

Purchases occurred:

Too few issuers with a full window.

No purchases:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 14 | -0.4% | -1.3% | -0.19 | 0.808 | 0.994 | 57% |
| [0,+5] | 14 | -0.7% | -4.0% | -0.16 | 0.426 | 0.855 | 57% |
| [-5,+5] | 14 | -6.3% | -4.4% | -1.12 | 0.358 | 0.302 | 64% |
| [-5,-1] | 14 | -5.7% | -6.4% | -1.50 | 0.068 | 0.126 | 86% |

- Negative pre-event returns alone do not establish anticipated selling pressure. Compare the CAR, window N and placebo p in the tables;
  the available event sample is small and date maturity limits coverage.
- Placebo calibration compares the event with neighbouring non-event dates for the same issuer. A small placebo p and a small test-against-zero p
  answer different questions; neither establishes an exogenous supply shock. Read the current rows rather than an earlier numerical example.
- Stabilization-end windows can overlap the early aftermarket period. Returns there can reflect market movements and the age of a listing as well as
  stabilization; no directional price-support conclusion follows from the event date alone.
- Contract lengths and missing dates differ across issuers. A date present in the workbook is not, by itself, evidence of complete independent review.
