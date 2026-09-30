# Lockup expiry and stabilization end, 2026 (HSI-adjusted, from cached daily bars)

Event day 0 is the first trading day on or after the event date; CAR is the sum of daily stock returns minus HSI returns over the window.
The **placebo p** re-draws one non-event day per issuer from the same issuer's own history, between 11 and 30 trading days from the true
event (so the volatility regime is similar), 5000 times. It calibrates drift and cross-issuer dependence that a plain t-test ignores.
The placebo compares the cross-sectional t-statistic of each draw with the observed one, so a window whose returns are unusually dispersed (event-induced variance) is not mistaken for a shifted mean.
Turnover rows compare mean turnover on days [0,+5] to days [-25,-6] (log ratio; 0 = no change).

## 1. Six-month lockup expiry (cornerstone unlock date, else controlling-shareholder date)

Only issuers listed early enough to have reached the expiry with a full window are included (37 at most, all listed January-March; 88 issuers share the same
cornerstone and controlling-shareholder date, so they are one event, not two).

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.5% | -2.9% | -1.37 | 0.076 | 0.206 | 61% |
| [0,+5] | 29 | -2.5% | -0.4% | -1.14 | 0.624 | 0.276 | 55% |
| [-5,+5] | 29 | -5.6% | -4.9% | -1.62 | 0.092 | 0.100 | 69% |
| [-5,-1] | 37 | -4.9% | -5.1% | -2.24 | 0.027 | 0.039 | 68% |
| Turnover [0,+5] vs [-25,-6], median log ratio | 29 | 0.18 | 0.12 | 1.19 | 0.275 | 0.004 | 41% |

Robustness, HSTECH-adjusted:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.6% | -2.3% | -1.45 | 0.120 | 0.109 | 61% |
| [0,+5] | 29 | -1.5% | -0.0% | -0.70 | 0.882 | 0.295 | 52% |
| [-5,+5] | 29 | -5.1% | -3.3% | -1.51 | 0.121 | 0.045 | 72% |
| [-5,-1] | 37 | -5.0% | -3.5% | -2.34 | 0.026 | 0.011 | 62% |
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

- A negative pre-window on the lockup event ([-5,-1]) is the usual anticipation of selling pressure; the sign and size of [-5,+5] against the placebo distribution
  is the test. With about 37 events from one listing quarter the power is limited.
- The placebo statistics are centred below zero: returns drift down and turnover decays as a new listing ages, so an ordinary window in the same weeks would
  show a negative average. That is why the placebo p can be much smaller than the plain t-test or Wilcoxon p (for example the stabilization-end [-5,+5] window has
  t about 1.9 but placebo p about 0.004): the window is unusual relative to the issuer's own neighbouring days, though a plain test against zero is only marginal.
- Stabilization end falls about 20 trading days after listing, exactly the Day-20 observation used elsewhere in this project, so this window also overlaps
  the post-listing decline that the hot-window comparison shows; the pre-window [-5,-1] is positive as well, which fits price support that lasts until the end.
- Lockup events include only January-March listings (N = 26 to 31), so they say nothing about April-June or later issuers.
