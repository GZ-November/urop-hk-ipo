# A+H issuers: offer discount to the A-share price (N = 38 issuers listed in 2026)

Data: `tools/external/ah_reference.py` (raw A-share closes from Tencent, CNY/HKD from Yahoo, CSI 300). A-share reference = close on the last A-share trading day
on or before the H-share subscription closing date; the price is converted to HKD with that day's exchange rate. Anchors are matched to issuers by A/H short name
(one manual override, 2768.HK); 2 issuer(s) fall outside a plausible +/-60% band and are flagged (`plausible = 0`); robustness drops them.
The day-1 gap uses the A-share close on the H listing day, so it also reflects A-share moves between the two dates.

## 0. A+H vs Non-A+H Comparison (Full 2026 Population)

| Group | N | Mean Proceeds (HK$M) | Median Proceeds (HK$M) | Mean Sub (x) | Median Sub (x) | Median Applicants | Mean IR (%) | Median IR (%) | Break Rate (%) |
|---|---|---|---|---|---|---|---|---|---|
| Full Sample (2026) | 113 | 3,178.7 | 1,233.1 | 1985.2x | 1073.4x | 153,878 | 53.15% | 14.82% | 23.0% |
| A+H Issuers (ah_true = 1) | 38 | 6,326.8 | 4,616.2 | 433.0x | 289.6x | 120,809 | 9.42% | 1.97% | 31.6% |
| Non-A+H Issuers (ah_true = 0) | 75 | 1,583.7 | 900.5 | 2771.6x | 2003.2x | 177,196 | 75.31% | 50.99% | 18.7% |

- **Size and Liquidity Divergence**: A+H issuers are large-cap enterprises (median base proceeds of HK$ 4,616.2M vs HK$ 900.5M for non-A+H, a ~5.1x difference).
- **Demand and Underpricing Gap**: A+H offerings attract substantially lower retail oversubscription (median 289.6x vs 2,003.2x) and deliver much lower first-day initial returns (median +1.97% vs +50.99%), with a higher offer break rate (31.6% vs 18.7%). The existing secondary market A-share quote acts as a visible valuation anchor, anchoring pricing expectations and curbing first-day speculative run-ups.

## 1. The discount

Issuer N counts A+H membership; the anchor columns count observed reference pairs. Means use available values, while IR uses all issuers in each row.
Paired offer/day-1 gap comparison N = 38.

| Sample | Issuer N | Offer-anchor N | Day-1-anchor N | Offer vs A (mean) | Offer vs A (median) | Day-1 close vs A (mean) | Mean IR | Median IR |
|---|---|---|---|---|---|---|---|---|
| All A+H | 38 | 38 | 38 | -39.0% | -40.5% | -32.2% | 9.4% | 2.0% |
| April-June | 9 | 9 | 9 | -41.3% | -39.7% | -27.5% | 25.7% | 13.3% |
| Other months | 29 | 29 | 29 | -38.2% | -41.3% | -33.6% | 4.4% | 1.5% |

- Offer vs A is negative for 38 of 38 issuers with an observed offer anchor: H shares are priced below the A-share close on average, and the discount is
  smaller at the day-1 close (paired t p = 0.001). This comparison also includes A-share and FX moves between anchor dates.
- April-June listings vs others: difference in the offer discount = -3.1 pp (HC3 p = 0.522).

## 2. Does the offer discount go with the first-day return?

Rank correlation of offer premium with IR: rho = -0.18 (p = 0.268, N = 38 finite pairs). Outcome log(1 + IR):

| Specification | Coefficient per +10 pp of offer premium (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| Offer discount only | -0.035 (0.025) | 0.163 | 0.262 | 38 |
| + April-June window | -0.028 (0.022) | 0.210 | 0.309 | 38 |
| + window + ln size | -0.077** (0.035) | 0.030 | 0.020 | 38 |
| + window, drop implausible anchors | -0.041 (0.028) | 0.147 | 0.270 | 36 |

- A negative coefficient means a deeper discount goes with a higher first-day return; this association alone does not identify convergence.
- The issuer population is 38 across 9 listing months; each regression reports its own valid-anchor N.
  Issuers missing an anchor remain in the population but do not enter anchor statistics or regressions. Treat these estimates as directional.

## 3. What explains the size of the discount

| Regressor | Coefficient, pp of discount per unit (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| A-share 20-day return before the offer | -35.45*** (6.32) | 0.000 | 0.035 | 38 |
| April-June window | -1.17 (4.25) | 0.783 | 0.828 | 38 |
| ln offer size | 6.56*** (1.75) | 0.000 | 0.035 | 38 |

A-share momentum is the 20-trading-day A-share return up to the anchor date. The coefficient is in percentage points of offer premium per unit (100 pp) of A-share return.

## 4. Convergence with the A share after listing

H/A gap = H close / (A close x CNY/HKD) - 1 on days when both markets traded; day 0 is the H listing day. "H minus own A return" is the H-share buy-and-hold return
from the day-0 close minus the A-share's return (in HKD) over the same dates: an abnormal return against the issuer's own A share.

| Trading days after listing | N | Mean gap, day 0 | Mean gap, day k | Mean change | t p | Wilcoxon p | H minus own A return, mean | H minus own A return, median |
|---|---|---|---|---|---|---|---|---|
| 5 | 33 | -32.5% | -31.8% | 0.6 pp | 0.629 | 0.751 | 1.3% | 0.5% |
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
| [-1,+1] | 38 | -1.5% | -0.0% | -1.70 | 0.232 | 0.022 | 50% |
| [0,+5] | 35 | -3.5% | -3.9% | -2.16 | 0.065 | 0.006 | 66% |
| [-5,+5] | 35 | -3.1% | -2.6% | -1.35 | 0.119 | 0.039 | 66% |
| [-5,-1] | 38 | 0.3% | -0.1% | 0.27 | 0.875 | 0.824 | 53% |

Around the H listing day:

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 38 | -2.6% | -2.8% | -2.59 | 0.016 | 0.002 | 66% |
| [0,+5] | 35 | -4.3% | -3.8% | -3.23 | 0.003 | 0.000 | 69% |
| [-5,+5] | 35 | -5.9% | -4.4% | -2.73 | 0.007 | 0.000 | 66% |
| [-5,-1] | 38 | -2.1% | -1.3% | -1.40 | 0.243 | 0.034 | 58% |

Sensitivity to pre-event alpha/beta: OLS on A trading bars [-120,-21], minimum 60 matched returns. Parameters are estimated separately
for subscription-close and listing events and held fixed in the event/placebo windows. This does not provide sector matching or causal identification.

Around subscription close (market model):

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 38 | -1.6% | -0.3% | -1.72 | 0.274 | 0.093 | 53% |
| [0,+5] | 35 | -4.6% | -4.4% | -2.69 | 0.024 | 0.013 | 60% |
| [-5,+5] | 35 | -5.6% | -3.8% | -2.41 | 0.046 | 0.029 | 63% |
| [-5,-1] | 38 | -1.2% | -1.4% | -1.21 | 0.237 | 0.300 | 58% |

Around H listing (market model):

| Window | N | Mean CAR | Median CAR | t | Wilcoxon p | Placebo p | share < 0 |
|---|---|---|---|---|---|---|---|
| [-1,+1] | 38 | -3.3% | -2.8% | -3.21 | 0.003 | 0.002 | 68% |
| [0,+5] | 35 | -5.1% | -4.4% | -3.78 | 0.000 | 0.001 | 80% |
| [-5,+5] | 35 | -7.4% | -4.6% | -3.10 | 0.001 | 0.002 | 74% |
| [-5,-1] | 38 | -2.7% | -1.6% | -1.85 | 0.140 | 0.084 | 58% |

## 6. Multiplicity

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Discount | A-share momentum -> offer discount (HC3) | 0.0000 | 0.0000 |
| 2 | Discount | Day-1 close discount is smaller than offer discount (paired t) | 0.0010 | 0.0055 |
| 3 | A-share reaction | A-share CAR [-1,+1] around H listing day (placebo) | 0.0020 | 0.0060 |
| 4 | A-share reaction | Market-model CAR [-1,+1] around H listing day (placebo) | 0.0022 | 0.0060 |
| 5 | A-share reaction | A-share CAR [-1,+1] around subscription close (placebo) | 0.0220 | 0.0484 |
| 6 | Convergence | H/A gap changes from day 0 to day 60 (Wilcoxon) | 0.0755 | 0.1384 |
| 7 | A-share reaction | Market-model CAR [-1,+1] around subscription close (placebo) | 0.0928 | 0.1458 |
| 8 | Discount | Offer discount -> log(1 + IR), window-adjusted (HC3) | 0.2103 | 0.2891 |
| 9 | Discount | Offer discount vs IR, Spearman | 0.2675 | 0.3270 |
| 10 | Convergence | H/A gap changes from day 0 to day 20 (Wilcoxon) | 0.4688 | 0.5157 |
| 11 | Discount | Offer discount differs between April-June and other listings (HC3) | 0.5225 | 0.5225 |

Limits: 38 A+H issuers, 38 observed offer anchors; the offer anchor uses the closing-date A-share price (pricing dates are missing for several issuers; the pre-pricing anchor is in the CSV where available);
CNY/HKD is a daily close rather than the rate at the pricing time; raw A-share prices are not adjusted for dividends inside the window.
