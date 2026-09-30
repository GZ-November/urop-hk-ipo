# A+H issuers: offer discount to the A-share price (N = 34 issuers listed in 2026)

Data: `tools/external/ah_reference.py` (raw A-share closes from Tencent, CNY/HKD from Yahoo, CSI 300). A-share reference = close on the last A-share trading day
on or before the H-share subscription closing date; the price is converted to HKD with that day's exchange rate. Anchors are matched to issuers by A/H short name
(one manual override, 2768.HK); 1 issuer(s) fall outside a plausible +/-60% band and are flagged (`plausible = 0`); robustness drops them.
The day-1 gap uses the A-share close on the H listing day, so it also reflects A-share moves between the two dates.

## 1. The discount

| Sample | N | Offer vs A (mean) | Offer vs A (median) | Day-1 close vs A (mean) | Mean IR | Median IR |
|---|---|---|---|---|---|---|
| All A+H | 34 | -38.2% | -39.2% | -32.8% | 7.7% | 0.9% |
| April-June | 9 | -41.3% | -39.7% | -30.1% | 21.8% | 0.6% |
| Other months | 25 | -37.1% | -38.7% | -33.8% | 2.6% | 1.1% |

- Offer vs A is negative for 34 of 34 issuers: H shares are priced below the A-share close on average, and the discount is
  smaller at the day-1 close (paired t p = 0.029), i.e. part of the offer discount closes on the first day.
- April-June listings vs others: difference in the offer discount = -4.2 pp (HC3 p = 0.387).

## 2. Does the offer discount go with the first-day return?

Rank correlation of offer premium with IR: rho = -0.33 (p = 0.059). Outcome log(1 + IR):

| Specification | Coefficient per +10 pp of offer premium (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| Offer discount only | -0.059* (0.030) | 0.053 | 0.199 | 34 |
| + April-June window | -0.051* (0.028) | 0.068 | 0.211 | 34 |
| + window + ln size | -0.105*** (0.040) | 0.009 | 0.012 | 34 |
| + window, drop implausible anchors | -0.055 (0.034) | 0.104 | 0.246 | 33 |

- A negative coefficient means a deeper discount (a more negative offer premium) goes with a higher first-day return: the H share catches up toward the A share.
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
| 5 | 32 | -33.7% | -33.1% | 0.6 pp | 0.650 | 0.692 | 1.5% | 0.5% |
| 20 | 33 | -32.5% | -30.5% | 2.0 pp | 0.205 | 0.257 | 3.1% | 2.2% |
| 40 | 32 | -32.4% | -28.6% | 3.7 pp | 0.117 | 0.239 | 5.5% | 2.2% |
| 60 | 25 | -31.7% | -30.0% | 1.6 pp | 0.711 | 0.220 | 4.2% | -10.3% |

## 5. The A-share reaction to the H-share issue (A-share return minus CSI 300)

Same placebo calibration as the lockup study (placebo days within 30 bars of the event, cross-sectional t against the placebo t-distribution).
The CSI 300 benchmark does not match each stock's beta or sector (the issuers are mostly technology manufacturers), which is why placebo days from the same stock
are the relevant comparison rather than zero.

Around the subscription closing date:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -1.4% | 0.5% | -1.49 | 0.343 | 0.062 | 47% |
| [0,+5] | 34 | -3.8% | -4.1% | -2.29 | 0.046 | 0.004 | 68% |
| [-5,+5] | 34 | -3.2% | -2.6% | -1.38 | 0.105 | 0.041 | 68% |
| [-5,-1] | 34 | 0.5% | 0.1% | 0.45 | 0.919 | 0.800 | 50% |

Around the H listing day:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 34 | -2.7% | -2.8% | -2.56 | 0.021 | 0.005 | 68% |
| [0,+5] | 34 | -4.0% | -3.3% | -2.98 | 0.005 | 0.000 | 68% |
| [-5,+5] | 34 | -6.0% | -5.2% | -2.67 | 0.009 | 0.000 | 65% |
| [-5,-1] | 34 | -2.0% | -0.8% | -1.25 | 0.352 | 0.088 | 56% |

## 6. Multiplicity

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Discount | A-share momentum -> offer discount (HC3) | 0.0000 | 0.0000 |
| 2 | A-share reaction | A-share CAR [-1,+1] around H listing day (placebo) | 0.0050 | 0.0225 |
| 3 | Discount | Day-1 close discount is smaller than offer discount (paired t) | 0.0287 | 0.0861 |
| 4 | Discount | Offer discount vs IR, Spearman | 0.0587 | 0.1019 |
| 5 | A-share reaction | A-share CAR [-1,+1] around subscription close (placebo) | 0.0616 | 0.1019 |
| 6 | Discount | Offer discount -> log(1 + IR), window-adjusted (HC3) | 0.0679 | 0.1019 |
| 7 | Convergence | H/A gap changes from day 0 to day 60 (Wilcoxon) | 0.2200 | 0.2828 |
| 8 | Convergence | H/A gap changes from day 0 to day 20 (Wilcoxon) | 0.2565 | 0.2886 |
| 9 | Discount | Offer discount differs between April-June and other listings (HC3) | 0.3874 | 0.3874 |

Limits: 34 issuers; the offer anchor uses the closing-date A-share price (pricing dates are missing for several issuers; the pre-pricing anchor is in the CSV where available);
CNY/HKD is a daily close rather than the rate at the pricing time; raw A-share prices are not adjusted for dividends inside the window.
