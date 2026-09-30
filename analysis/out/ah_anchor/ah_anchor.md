# A+H issuers: offer discount to the A-share price (N = 34 issuers listed in 2026)

Data: `tools/external/ah_reference.py` (raw A-share closes from Tencent, CNY/HKD from Yahoo, CSI 300). A-share reference = close on the last A-share trading day
on or before the H-share subscription closing date; the price is converted to HKD with that day's exchange rate. Anchors are matched to issuers by A/H short name
(one manual override, 2768.HK); 1 issuer(s) fall outside a plausible +/-60% band and are flagged (`plausible = 0`); robustness drops them.
The day-1 gap uses the A-share close on the H listing day, so it also reflects A-share moves between the two dates.

## 1. The discount

| Sample | N | Offer vs A (mean) | Offer vs A (median) | Day-1 close vs A (mean) | Mean IR | Median IR |
|---|---|---|---|---|---|---|
| All A+H | 34 | -38.2% | -39.2% | -30.7% | 10.9% | 2.7% |
| April-June | 9 | -41.3% | -39.7% | -27.5% | 25.7% | 13.3% |
| Other months | 25 | -37.1% | -38.7% | -31.8% | 5.6% | 2.4% |

- Offer vs A is negative for 34 of 34 issuers: H shares are priced below the A-share close on average, and the discount is
  smaller at the day-1 close (paired t p = 0.001). This comparison also includes A-share and FX moves between anchor dates.
- April-June listings vs others: difference in the offer discount = -4.2 pp (HC3 p = 0.387).

## 2. Does the offer discount go with the first-day return?

Rank correlation of offer premium with IR: rho = -0.30 (p = 0.084). Outcome log(1 + IR):

| Specification | Coefficient per +10 pp of offer premium (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| Offer discount only | -0.048* (0.026) | 0.069 | 0.254 | 34 |
| + April-June window | -0.039 (0.024) | 0.103 | 0.242 | 34 |
| + window + ln size | -0.084** (0.038) | 0.026 | 0.016 | 34 |
| + window, drop implausible anchors | -0.043 (0.029) | 0.137 | 0.262 | 33 |

- A negative coefficient means a deeper discount goes with a higher first-day return; this association alone does not identify convergence.
- N = 34 and 9 listing months; treat as directional.

## 3. What explains the size of the discount

| Regressor | Coefficient, pp of discount per unit (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| A-share 20-day return before the offer | -36.57*** (6.10) | 0.000 | 0.027 | 34 |
| April-June window | -2.06 (4.17) | 0.622 | 0.723 | 34 |
| ln offer size | 5.80*** (1.68) | 0.001 | 0.066 | 34 |

A-share momentum is the 20-trading-day A-share return up to the anchor date. The coefficient is in percentage points of offer premium per unit (100 pp) of A-share return.

## 4. Convergence with the A share after listing

H/A gap = H close / (A close x CNY/HKD) - 1 on days when both markets traded; day 0 is the H listing day. "H minus own A return" is the H-share buy-and-hold return
from the day-0 close minus the A-share's return (in HKD) over the same dates: an abnormal return against the issuer's own A share.

| Trading days after listing | N | Mean gap, day 0 | Mean gap, day k | Mean change | t p | Wilcoxon p | H minus own A return, mean | H minus own A return, median |
|---|---|---|---|---|---|---|---|---|
| 5 | 32 | -31.4% | -30.7% | 0.7 pp | 0.597 | 0.678 | 1.5% | 0.5% |
| 20 | 33 | -30.3% | -28.8% | 1.4 pp | 0.362 | 0.469 | 1.9% | 1.9% |
| 40 | 32 | -30.1% | -26.7% | 3.3 pp | 0.155 | 0.295 | 4.5% | 2.2% |
| 60 | 25 | -28.7% | -28.7% | 0.0 pp | 0.996 | 0.075 | 1.8% | -10.4% |

`horizon_coverage.csv` records matched issuers at every reported horizon. `balanced_path_60.csv` and the figure hold the cohort fixed to issuers
with valid day-0 and day-60 pairs. On cross-market holidays the daily count can still fall; prices are not carried forward.
The daily premium panel uses raw H and A prices from Tencent. Adjusted H caches cannot be divided by raw A prices after a share split.
Nonsignificant gap changes are inconclusive, rather than evidence that convergence is absent.

## 5. The A-share reaction to the H-share issue (A-share return minus CSI 300)

Same placebo calibration as the lockup study (placebo days within 30 bars of the event, cross-sectional t against the placebo t-distribution).
The CSI 300 benchmark does not match each stock's beta or sector (the issuers are mostly technology manufacturers), which is why placebo days from the same stock
are the relevant comparison rather than zero.

Around the subscription closing date:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -1.4% | 0.5% | -1.49 | 0.343 | 0.057 | 47% |
| [0,+5] | 34 | -3.8% | -4.1% | -2.29 | 0.046 | 0.004 | 68% |
| [-5,+5] | 34 | -3.2% | -2.6% | -1.38 | 0.105 | 0.041 | 68% |
| [-5,-1] | 34 | 0.5% | 0.1% | 0.45 | 0.919 | 0.799 | 50% |

Around the H listing day:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -2.7% | -2.8% | -2.56 | 0.021 | 0.005 | 68% |
| [0,+5] | 34 | -4.0% | -3.3% | -2.98 | 0.005 | 0.000 | 68% |
| [-5,+5] | 34 | -6.0% | -5.2% | -2.67 | 0.009 | 0.000 | 65% |
| [-5,-1] | 34 | -2.0% | -0.8% | -1.25 | 0.352 | 0.085 | 56% |

Sensitivity to pre-event alpha/beta: OLS on A trading bars [-120,-21], minimum 60 matched returns. Parameters are estimated separately
for subscription-close and listing events and held fixed in the event/placebo windows. This does not provide sector matching or causal identification.

Around subscription close (market model):

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -1.7% | 0.1% | -1.73 | 0.309 | 0.145 | 50% |
| [0,+5] | 34 | -4.9% | -4.5% | -2.84 | 0.017 | 0.009 | 62% |
| [-5,+5] | 34 | -5.9% | -3.9% | -2.49 | 0.031 | 0.031 | 65% |
| [-5,-1] | 34 | -1.0% | -1.3% | -0.88 | 0.427 | 0.655 | 53% |

Around H listing (market model):

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -3.6% | -3.2% | -3.22 | 0.004 | 0.004 | 68% |
| [0,+5] | 34 | -4.9% | -4.2% | -3.56 | 0.001 | 0.001 | 79% |
| [-5,+5] | 34 | -7.6% | -5.0% | -3.12 | 0.001 | 0.004 | 76% |
| [-5,-1] | 34 | -2.8% | -0.9% | -1.81 | 0.209 | 0.150 | 56% |

## 6. Multiplicity

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Discount | A-share momentum -> offer discount (HC3) | 0.0000 | 0.0000 |
| 2 | Discount | Day-1 close discount is smaller than offer discount (paired t) | 0.0009 | 0.0052 |
| 3 | A-share reaction | Market-model CAR [-1,+1] around H listing day (placebo) | 0.0040 | 0.0143 |
| 4 | A-share reaction | A-share CAR [-1,+1] around H listing day (placebo) | 0.0052 | 0.0143 |
| 5 | A-share reaction | A-share CAR [-1,+1] around subscription close (placebo) | 0.0570 | 0.1254 |
| 6 | Convergence | H/A gap changes from day 0 to day 60 (Wilcoxon) | 0.0755 | 0.1319 |
| 7 | Discount | Offer discount vs IR, Spearman | 0.0839 | 0.1319 |
| 8 | Discount | Offer discount -> log(1 + IR), window-adjusted (HC3) | 0.1029 | 0.1415 |
| 9 | A-share reaction | Market-model CAR [-1,+1] around subscription close (placebo) | 0.1448 | 0.1769 |
| 10 | Discount | Offer discount differs between April-June and other listings (HC3) | 0.3874 | 0.4262 |
| 11 | Convergence | H/A gap changes from day 0 to day 20 (Wilcoxon) | 0.4688 | 0.4688 |

Limits: 34 issuers; the offer anchor uses the closing-date A-share price (pricing dates are missing for several issuers; the pre-pricing anchor is in the CSV where available);
CNY/HKD is a daily close rather than the rate at the pricing time; raw A-share prices are not adjusted for dividends inside the window.
