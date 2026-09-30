# Lockup expiry and stabilization end, 2026 (HSI-adjusted, from cached daily bars)

Event day 0 is the first trading day on or after the event date; CAR is the sum of daily stock returns minus HSI returns over the window.
The **placebo p** re-draws one non-event day per issuer from the same issuer's own history, between 11 and 30 trading days from the true
event (so the volatility regime is similar), 5000 times. It calibrates drift and cross-issuer dependence that a plain t-test ignores.
The placebo compares the cross-sectional t-statistic of each draw with the observed one, so a window whose returns are unusually dispersed (event-induced variance) is not mistaken for a shifted mean.
Turnover rows compare mean turnover on days [0,+5] to days [-25,-6] (log ratio; 0 = no change).

## 1. Six-month lockup expiry (cornerstone unlock date, else controlling-shareholder date)

Only issuers listed early enough to have reached the expiry with a full window are included (31 at most, all listed January-March; 88 issuers share the same
cornerstone and controlling-shareholder date, so they are one event, not two).

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.5% | -2.9% | -1.37 | 0.076 | 0.215 | 61% |
| [0,+5] | 26 | -2.6% | -0.3% | -1.06 | 0.764 | 0.295 | 54% |
| [-5,+5] | 26 | -5.9% | -5.1% | -1.55 | 0.123 | 0.147 | 69% |
| [-5,-1] | 31 | -3.9% | -2.9% | -1.65 | 0.090 | 0.116 | 65% |
| Turnover [0,+5] vs [-25,-6], median log ratio | 26 | 0.20 | 0.14 | 1.27 | 0.227 | 0.004 | 38% |

Robustness, HSTECH-adjusted:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 31 | -2.6% | -2.3% | -1.45 | 0.120 | 0.117 | 61% |
| [0,+5] | 26 | -1.7% | 0.4% | -0.73 | 0.861 | 0.322 | 50% |
| [-5,+5] | 26 | -5.4% | -4.3% | -1.45 | 0.150 | 0.088 | 73% |
| [-5,-1] | 31 | -4.4% | -3.3% | -1.90 | 0.069 | 0.032 | 61% |
| Turnover [0,+5] vs [-25,-6], median log ratio | 26 | 0.20 | 0.14 | 1.27 | 0.227 | 0.004 | 38% |

## 2. End of the stabilization period

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 100 | 0.4% | -0.9% | 0.46 | 0.888 | 0.359 | 55% |
| [0,+5] | 99 | 1.3% | -0.0% | 0.77 | 0.772 | 0.186 | 51% |
| [-5,+5] | 99 | 4.1% | 2.9% | 1.87 | 0.059 | 0.004 | 43% |
| [-5,-1] | 100 | 2.8% | 0.4% | 1.67 | 0.217 | 0.029 | 48% |

Split by whether stabilizing purchases occurred (their number is small):

Purchases occurred:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 13 | -2.7% | -3.5% | -1.51 | 0.127 | 0.177 | 77% |
| [0,+5] | 13 | -3.2% | -4.7% | -0.70 | 0.497 | 0.595 | 62% |
| [-5,+5] | 13 | 0.6% | 1.0% | 0.11 | 0.893 | 0.866 | 46% |
| [-5,-1] | 13 | 3.7% | 0.8% | 1.43 | 0.305 | 0.166 | 31% |

No purchases:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 87 | 0.9% | -0.3% | 0.88 | 0.501 | 0.190 | 52% |
| [0,+5] | 86 | 1.9% | 0.2% | 1.09 | 0.551 | 0.103 | 49% |
| [-5,+5] | 86 | 4.6% | 3.1% | 1.92 | 0.045 | 0.005 | 43% |
| [-5,-1] | 87 | 2.7% | -0.0% | 1.41 | 0.337 | 0.037 | 51% |

- A negative pre-window on the lockup event ([-5,-1]) is the usual anticipation of selling pressure; the sign and size of [-5,+5] against the placebo distribution
  is the test. With about 31 events from one listing quarter the power is limited.
- The placebo statistics are centred below zero: returns drift down and turnover decays as a new listing ages, so an ordinary window in the same weeks would
  show a negative average. That is why the placebo p can be much smaller than the plain t-test or Wilcoxon p (for example the stabilization-end [-5,+5] window has
  t about 1.9 but placebo p about 0.004): the window is unusual relative to the issuer's own neighbouring days, though a plain test against zero is only marginal.
- Stabilization end falls about 20 trading days after listing, exactly the Day-20 observation used elsewhere in this project, so this window also overlaps
  the post-listing decline that the hot-window comparison shows; the pre-window [-5,-1] is positive as well, which fits price support that lasts until the end.
- Lockup events include only January-March listings (N = 26 to 31), so they say nothing about April-June or later issuers.
