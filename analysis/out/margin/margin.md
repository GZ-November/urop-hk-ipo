# Margin Snapshots & Retail Demand, 2026 (Idea 13)

Closing-day snapshot sensitivity: N = 15, coefficient = 0.150, HC3 p = 0.473. G = 4; maximum leverage = 0.586; status = estimated. HC3 estimability does not ensure reliable inference with few/unbalanced listing-month clusters. A closing-day snapshot is not necessarily available before the subscription/pricing decision. Non-closing observations are censored and differ in time to deadline.

## 1. Broker Margin Financing Panel (N = 25 issuers)

Source-reported broker-survey snapshots cover 25 of 106 issuers (93 observations). Only 15 have a snapshot on the subscription closing date. No missing dates are interpolated. These are media-reported survey amounts, not audited market-wide totals.
- **Rank correlation** of latest observed margin multiple with first-day return (IR): $\rho = 0.46$ ($p = 0.020$).
- **Observed growth** in 20 issuers with multiple dates and a constant named survey scope: mean **41.59x**, median **16.80x**. Endpoint growth does not establish acceleration, exponential growth or herding. Broker membership within a news survey remains unspecified.

### Latest Observed Margin Multiple vs First-Day Return (IR)

| Specification | Coefficient (HC3 s.e.) | HC3 p | Wild cluster p | N |
|---|---|---|---|---|
| ln latest observed margin multiple | 0.161* (0.083) | 0.051 | 0.250 | 25 |
| + April-June window | 0.091 (0.060) | 0.129 | 0.156 | 25 |
| + window + ln size | 0.082 (0.073) | 0.265 | 0.219 | 25 |

### Growth Between Observed Endpoints

| Stock Code | Latest Observed Multiple | Earliest Observed Multiple | days | first_date | last_date | Earliest Margin (B HKD) | Latest Margin (B HKD) | on_close | comparable_scope | Observed Growth Ratio |
|---|---|---|---|---|---|---|---|---|---|---|
| 0537.HK | 94.0x | 3.3x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 0.4 | 10.7 | True | True | 28.47x |
| 1377.HK | 188.6x | 4.5x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 2.2 | 90.5 | True | True | 41.76x |
| 1770.HK | 127.0x | 12.1x | 4 | 2026-06-29 00:00:00 | 2026-07-02 00:00:00 | 0.6 | 6.6 | False | True | 10.52x |
| 1879.HK | 4653.3x | 363.1x | 4 | 2026-04-20 00:00:00 | 2026-04-23 00:00:00 | 45.9 | 588.0 | True | True | 12.82x |
| 2249.HK | 235.6x | 1.2x | 6 | 2026-06-30 00:00:00 | 2026-07-07 00:00:00 | 0.8 | 164.5 | True | True | 200.91x |
| 2475.HK | 2.5x | 0.7x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 1.7 | 5.9 | True | True | 3.51x |
| 2493.HK | 298.8x | 18.1x | 4 | 2026-04-20 00:00:00 | 2026-04-23 00:00:00 | 2.6 | 43.2 | True | True | 16.49x |
| 2667.HK | 81.3x | 41.8x | 3 | 2026-06-29 00:00:00 | 2026-07-01 00:00:00 | 2.8 | 5.5 | False | True | 1.95x |
| 2797.HK | 790.3x | 3.5x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 0.1 | 15.8 | True | True | 225.79x |
| 3296.HK | 421.4x | 64.7x | 2 | 2026-04-17 00:00:00 | 2026-04-20 00:00:00 | 29.4 | 191.7 | True | True | 6.52x |
| 3752.HK | 98.4x | 3.4x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 0.3 | 8.6 | True | True | 29.26x |
| 6658.HK | 4311.2x | 122.5x | 3 | 2026-06-05 00:00:00 | 2026-06-10 00:00:00 | 6.1 | 215.4 | True | True | 35.20x |
| 6745.HK | 120.9x | 1.8x | 6 | 2026-06-30 00:00:00 | 2026-07-07 00:00:00 | 0.2 | 15.3 | True | True | 65.35x |
| 6810.HK | 1205.5x | 23.8x | 4 | 2026-04-21 00:00:00 | 2026-04-24 00:00:00 | 2.5 | 127.7 | True | True | 50.69x |
| 6880.HK | 100.4x | 10.7x | 4 | 2026-06-29 00:00:00 | 2026-07-02 00:00:00 | 6.3 | 59.2 | False | True | 9.41x |
| 6951.HK | 196.2x | 3.5x | 5 | 2026-06-30 00:00:00 | 2026-07-06 00:00:00 | 2.5 | 140.4 | True | True | 55.57x |
| 7656.HK | 744.0x | 43.5x | 4 | 2026-06-29 00:00:00 | 2026-07-02 00:00:00 | 1.3 | 22.6 | False | True | 17.12x |
| 7687.HK | 41.9x | 5.3x | 4 | 2026-06-29 00:00:00 | 2026-07-02 00:00:00 | 1.2 | 9.6 | False | True | 7.96x |
| 9971.HK | 1539.5x | 149.1x | 4 | 2026-06-29 00:00:00 | 2026-07-02 00:00:00 | 6.5 | 66.7 | False | True | 10.33x |
| 9976.HK | 27.2x | 12.1x | 3 | 2026-09-01 00:00:00 | 2026-09-03 00:00:00 | 7.6 | 17.0 | True | True | 2.25x |

![Idea 13 Margin Cascades](fig10_margin_cascades.png)

## 2. Model 13.1: Full-Sample Retail Frenzy & Intraday Price Discovery (N = 106)

Following **Idea 13 (Model 13.1)** in `docs/RESEARCH_IDEAS.md`:
$$\text{IntradayRange}_i = \alpha_0 + \beta_1 \ln(\text{SubscriptionRatio}_i) + \beta_2 \ln(\text{PublicApplicants}_i) + \beta_3 \text{HIBOR1m}_i + \gamma \mathbf{X}_i + \varepsilon_i$$
$$\text{FirstDayFlipping}_i = \alpha_0 + \beta_1 \ln(\text{SubscriptionRatio}_i) + \beta_2 \ln(\text{PublicApplicants}_i) + \beta_3 \text{HIBOR1m}_i + \gamma \mathbf{X}_i + \varepsilon_i$$

### Econometric Results

| Specification | Focus Coeff (HC3 s.e.) | HC3 p | Wild cluster p | R² | N |
|---|---|---|---|---|---|
| Intraday Range ~ ln Subscription Ratio | 0.078*** (0.012) | 0.000 | 0.008 | 0.254 | 106 |
| + ln Applicants + HIBOR + ln Size | 0.035 (0.044) | 0.426 | 0.301 | 0.304 | 106 |
| + Window (Hot) | 0.040 (0.044) | 0.362 | 0.150 | 0.352 | 106 |
| Flipping Ratio ~ ln Subscription Ratio | 0.047*** (0.006) | 0.000 | 0.004 | 0.231 | 106 |
| + ln Applicants + HIBOR + ln Size | 0.012 (0.035) | 0.722 | 0.609 | 0.246 | 106 |
| + Window (Hot) | 0.013 (0.035) | 0.715 | 0.604 | 0.247 | 106 |

### Interpretation

Nested models use the same finite complete-case sample within each outcome. Intraday range / offer is a price amplitude, not realized volatility.
Subscription intensity, applicants and HIBOR are proxies. These regressions do not observe individual borrowing, loan repayment or investor herding;
they cannot establish that leverage causes flipping. Read the controlled estimates and cluster p-values alongside the simple correlations.


## Multiplicity (all reported HC3 tests)

| Rank | Section | Test | p | q (BH) |
|---|---|---|---|---|
| 1 | Retail proxies | Flipping Ratio ~ ln Subscription Ratio | 1.0154520793514926e-13 | 1.0154520793514925e-12 |
| 2 | Retail proxies | Intraday Range ~ ln Subscription Ratio | 7.99975394934113e-11 | 3.9998769746705646e-10 |
| 3 | Observed margin | ln latest observed margin multiple | 0.051095295972895804 | 0.17031765324298603 |
| 4 | Observed margin | + April-June window | 0.12894291646379072 | 0.32235729115947676 |
| 5 | Observed margin | + window + ln size | 0.2647204004279633 | 0.5294408008559266 |
| 6 | Retail proxies | + Window (Hot) | 0.36156607234892546 | 0.5914750082953468 |
| 7 | Retail proxies | + ln Applicants + HIBOR + ln Size | 0.42634352399131725 | 0.5914750082953468 |
| 8 | Observed margin | Closing-day snapshots, window + size | 0.47318000663627746 | 0.5914750082953468 |
| 9 | Retail proxies | + Window (Hot) | 0.7147906534849415 | 0.7220753279509531 |
| 10 | Retail proxies | + ln Applicants + HIBOR + ln Size | 0.7220753279509531 | 0.7220753279509531 |