# Regime tests, 2026 (N = 106)

The Apr-Jun "hot window" was found by inspecting these data, so its ordinary p-value overstates the evidence.
These tests price in the search and ask what a listing-date regime does and does not explain.

## 1. Search-corrected test for a contiguous window

Statistic: the largest |Welch t| of log(1 + IR) inside vs outside any contiguous run of listings
(1410 candidate windows, edges on listing-date changes, at least 10 deals on each side).
Null: IR is exchangeable across listing order (5000 permutations).

| Item | Value |
|---|---|
| Largest |t| over all windows | 4.48 (95th percentile under null: 4.57) |
| **Search-corrected permutation p** | **0.056** |
| Best "hot" window (positive) | 2026-03-30 to 2026-06-30, 51 deals, t = 4.16 |
| Best "cold" window (negative) | 2026-07-02 to 2026-09-08, 22 deals, t = -4.48 |
| Calendar Apr-Jun vs rest (a data-informed window) | Welch t = 3.97, ordinary permutation p = 0.0004 |

- The data-optimal hot window (2026-03-30 to 2026-06-30, 51 deals) is close to the calendar Apr-Jun dummy, so the dummy is
  not far from the best possible block. The single strongest contrast is the cold spell that follows it (2026-07-02 to 2026-09-08, 22 deals).
- After correcting for the search, the evidence for a level shift is **marginal (p < 0.10)** (p = 0.056) while the
  uncorrected Apr-Jun p-value (0.0004) is far smaller. Report the corrected number; the regime is a feature of 2026,
  not a precisely dated event.

## 2. How much of IR is a month effect?

| Item | Value |
|---|---|
| ANOVA intraclass correlation across 9 listing months | 0.147 |
| F (month effect) / permutation p | 2.96 / 0.0052 |

About 15% of the variance of log(1 + IR) sits between months; most dispersion is within a month.

## 3. Serial dependence across listing order

| Series | Spearman lag-1 (p) | Ljung-Box p, 5 lags | Ljung-Box p, 10 lags |
|---|---|---|---|
| log(1+IR) | 0.091 (0.36) | 0.203 | 0.129 |

Consecutive listings are not significantly correlated, which is why the permutation null above is reasonable.
The regime is a level shift in the mean with large idiosyncratic noise, not a smooth momentum process.

## 4. Real-time predictability and crowding

`prior_ir` is the mean IR of 2026 IPOs listed in the 30 days before the deal's subscription opened (at least 3 deals,
so January listings are dropped). It uses only information available at the offer date. Crowding counts other deals
whose subscription window overlaps this one; the last row asks whether crowding lowers retail oversubscription.

| Specification | Coefficient (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| Prior-30-day mean IR (per +100 pp) | 0.178 (0.148) | 0.227 | 0.391 | 91 |
|   + issuer controls | 0.155 (0.153) | 0.310 | 0.375 | 87 |
|   + issuer controls + April-June dummy | -0.244 (0.178) | 0.169 | 0.145 | 87 |
| Overlapping subscriptions (per deal), controls + hot | -0.011 (0.010) | 0.262 | 0.359 | 102 |
| Same-day listings (per deal), controls + hot | -0.023 (0.026) | 0.378 | 0.160 | 102 |
| Overlapping subscriptions -> ln subscription ratio | -0.051* (0.028) | 0.068 | 0.125 | 102 |

- Unconditional Spearman correlation of prior-IPO mean IR with IR: 0.12 (p = 0.28).
- Prior-IPO returns are not a significant predictor with or without the window dummy (the sign flips once the dummy is
  added, because the dummy carries the level). Prior IR is a weak real-time signal of the regime; prediction.md checks this out of sample.
- Retail oversubscription falls by about 5% per additional overlapping offering
  (HC3 p = 0.068, wild cluster p = 0.125): marginal (p < 0.10). Crowding does not significantly change IR itself.
- Wild cluster p uses listing-month clusters (exact enumeration); HC3 p ignores clustering. Read both.
