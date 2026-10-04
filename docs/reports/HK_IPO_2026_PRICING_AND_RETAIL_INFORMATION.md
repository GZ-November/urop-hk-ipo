# Topic 1: Pricing Adjustment and First-Day Returns

## 1. Question, answer and evidence boundary

Topic 1: Pricing adjustment and first-day returns. Hong Kong Main Board ordinary IPOs listed from 2 January to 30 September 2026. Prepared on 4 October 2026. This report completes the empirical assessment of the current sample. It does not claim to identify the cause of each price change. Research topics on retail prediction and allocation rules are separate.

Question: If the final offer price is high relative to the filed price range, why can a large gain still occur when trading starts? The data show that a price above the filed midpoint and a first-day gain can coexist. They also show large gains after pricing below the midpoint. A filed midpoint is a reference price, not an earlier agreed transaction price. Thus, the premise that the price was already increased during subscription is not established for these offers.

Main answer: The revision-return association is positive on the 43 range offers, but its size is uncertain. It survives changes in estimator and month deletion in sign. It does not pass the maintained multiple-test inference. Market-date sensitivity is much smaller than the effect of selecting firms with available pricing proxies. The data do not distinguish compensation for investor information from demand pressure, issuer selection, supply limits or other pricing choices.

### Table 1. Audited classification and close returns

| Price evidence | N | A+H | Mean % | Median % |
| --- | --- | --- | --- | --- |
| Two-sided range | 43 | 9 | 68.29 | 37.53 |
| Recorded equal endpoints | 39 | 0 | 73.39 | 44.74 |
| Single quoted price: 2041 | 1 | 0 | -42.93 | -42.93 |
| Confirmed maximum only | 30 | 29 | 8.36 | 2.67 |

Total N=113. The 31 previously missing-lower-bound cases were reviewed against complete official prospectuses: 30 maximum-only and one single-price offer. The other 39 equal-endpoint cases were not re-audited. All means are unweighted across IPOs; they are not account returns.

The main outcome is the offer-to-first-day-close return. Opening and intraday returns locate the trading stages. HSI adjustment is a sensitivity check. All primary price-stage equations use the same 43 firms and the same controls. A missing lower endpoint receives no invented midpoint and no zero revision.

$$
P_M=(P_L+P_H)/2,\quad v=P_0/P_M-1,\quad R_C=P_C/P_0-1,\\ R_O=P_O/P_0-1,\quad R_D=P_C/P_O-1.
$$

PL and PH are the filed lower and upper prices. PM is their midpoint. P0 is the final offer price. PO and PC are the first trading-day opening and closing prices. Revision v compares final price with midpoint; it does not prove a dated price change. The 43 firms comprise 16 Q1, 14 Q2 and 13 Q3 listings; nine are A+H offers.

## 2. Main estimates and the strength of inference

$$
\ln(P_{Ci}/P_{0i})=\alpha+\beta v_i+\delta_2 Q2_i+\delta_3 Q3_i+\varepsilon_i.
$$

The main model includes an intercept and Q2/Q3 indicators. Log returns limit the influence of very large gains, while raw returns remain in the descriptions. The slope is an association across companies. Both the final offer price and the first-day price reflect issuer characteristics, demand and the chosen offer structure.

### Table 2. Quarter-controlled slopes and month-jackknife intervals

| Outcome | Slope | CV3 SE | 95% low | 95% high | WCR p | Holm p |
| --- | --- | --- | --- | --- | --- | --- |
| Offer to close | 1.598 | 1.058 | -0.841 | 4.037 | 0.207 | 1.000 |
| Offer to opening | 0.874 | 0.958 | -1.334 | 3.083 | 0.375 | 1.000 |
| Opening to close | 0.723 | 0.226 | 0.203 | 1.244 | 0.051 | 0.355 |
| HSI-adjusted close | 1.554 | 1.064 | -0.900 | 4.008 | 0.242 | 1.000 |

N=43, nine listing-month clusters, four parameters. CV3 is the full-estimate-centered cluster jackknife; intervals use t(8). WCR is restricted wild cluster-t with all 512 Rademacher signs. Holm p retains the original seven-outcome family, including raw close, allocation and application return. No stars are used. Slope units are log-return units per one unit of fractional revision.

A 10 percentage point difference in revision corresponds to a fitted 17.33% multiplicative difference in the close/offer price ratio. Its CV3 interval is -8.07% to 49.73%. This is not a change of the same number of percentage points in raw return. The revision standard deviation is 7.91 percentage points; the corresponding fitted ratio difference is 13.47%.

### Table 3. Inference changes with the covariance method

| Outcome | HC3 p | CV3 p | CV3 Holm | WCR p | WCR Holm |
| --- | --- | --- | --- | --- | --- |
| Offer to close | 0.251 | 0.169 | 1.000 | 0.207 | 1.000 |
| Offer to opening | 0.431 | 0.388 | 1.000 | 0.375 | 1.000 |
| Opening to close | 0.050 | 0.013 | 0.088 | 0.051 | 0.355 |
| HSI-adjusted close | 0.267 | 0.182 | 1.000 | 0.242 | 1.000 |

HC3 uses a t reference. Both Holm columns retain seven tests. The same estimates receive different uncertainty measures; this is not new independent evidence.

The intraday CV3 p-value is 0.013 before adjustment, but 0.088 after Holm adjustment. Its exact WCR p-value is 0.051 and its Holm WCR p-value is 0.355. This conflict is a material limitation with only nine clusters. The report therefore treats the intraday result as suggestive, and does not choose CV3 because it gives a smaller p-value. Failure to reject is also not proof of zero association.

### Table 4. All previously declared control designs

| Controls | Close | Opening | Intraday | HSI close |
| --- | --- | --- | --- | --- |
| Revision only | 1.396 | 0.669 | 0.727 | 1.341 |
| Quarter | 1.598 | 0.874 | 0.723 | 1.554 |
| Launch size and A+H | 1.502 | 0.734 | 0.768 | 1.448 |
| Subscription HSI and launch size | 1.679 | 0.893 | 0.786 | 1.631 |

All cells retain the same 43 firms. These are alternative small models, not a nested sequence. Full estimates, uncertainty and adjusted R-squared values are in stage_inference.csv.

## 3. Where the price difference occurs

$$
\ln(P_C/P_0)=\ln(P_O/P_0)+\ln(P_C/P_O).
$$

The stage identity is exact for each firm. With the same OLS design, the close slope equals the opening slope plus the intraday slope: 1.598 = 0.874 + 0.723 after rounding. About 45.3% of the fitted slope is in the intraday component. This is accounting of an association, not a fraction of gains caused by late information.

### Table 5. Prices above and below the filed midpoint

| Final price | N | Revision % | Mean close % | Mean open % | Log day points |
| --- | --- | --- | --- | --- | --- |
| Below midpoint | 22 | -7.15 | 57.69 | 58.94 | -7.96 |
| Above midpoint | 21 | 5.70 | 79.39 | 69.50 | 3.78 |

Log day points are 100 times mean log(PC/PO), not mean simple intraday return. No final price equals the midpoint. The raw return mean need not describe a typical firm.

The below-midpoint firms have large mean opening gains but negative mean log intraday returns. The above-midpoint firms have positive mean log intraday returns. This locates a difference in subsequent trading. It does not show which traders caused it, or whether opening or closing prices were closer to fundamental value. Price discovery needs information or later valuation evidence, not only price changes.

### Table 6. Robust estimators on the full sample

| Outcome | OLS | Median | Huber |
| --- | --- | --- | --- |
| Offer to close | 1.598 | 0.870 | 1.890 |
| Offer to opening | 0.874 | 0.489 | 1.053 |
| Opening to close | 0.723 | 0.699 | 0.528 |
| HSI-adjusted close | 1.554 | 1.076 | 1.866 |

N=43 throughout. Median and Huber regressions estimate different functionals from the conditional mean. Their asymptotic SEs are not month-cluster robust. Their slopes cannot be added across stages as an exact decomposition.

### Table 7. Delete one listing month at a time

| Deleted month | N kept | Close | Opening | Intraday | Info % |
| --- | --- | --- | --- | --- | --- |
| 2026-01 | 39 | 1.453 | 0.823 | 0.630 | 9.62 |
| 2026-02 | 39 | 1.405 | 0.723 | 0.682 | 2.21 |
| 2026-03 | 35 | 1.342 | 0.583 | 0.759 | 15.94 |
| 2026-04 | 40 | 1.245 | 0.439 | 0.806 | 4.27 |
| 2026-05 | 40 | 1.334 | 0.691 | 0.643 | 7.15 |
| 2026-06 | 35 | 1.846 | 1.190 | 0.656 | 13.63 |
| 2026-07 | 36 | 1.254 | 0.618 | 0.636 | 31.18 |
| 2026-08 | 42 | 1.667 | 0.935 | 0.731 | 0.56 |
| 2026-09 | 38 | 2.468 | 1.602 | 0.865 | 15.44 |

All deleted-month designs remain full rank. Information share is the month share of squared revision residuals after quarter controls, measured in the full sample. No diagnostic exclusion replaces the main result.

All month-deletion slopes remain positive. Close slopes range from 1.245 to 2.468. July holds 31.2% of the revision information. The inverse sum of squared information shares is 5.50; this is a concentration diagnostic, not a replacement degrees of freedom. Sign stability is useful, but it does not establish a precise or causal effect.

## 4. Pricing dates, missing firms and market adjustment

No actual price-agreement date is newly certified in the current evidence record. The 36 recorded pricing anchors are expected-date proxies. Final-price publication timestamps are available for all 43 firms, but publication is not the time of agreement. The prior date search covered 29 complete local prospectuses and all 43 allotment texts. It did not establish that actual dates are absent from all public disclosures.

### Table 8. Matched companies distinguish date effects from selection

| Sample / anchor | N | Mean return % | Slope |
| --- | --- | --- | --- |
| All / raw close | 43 | 68.29 | 1.598 |
| All / subscription close | 43 | 68.85 | 1.554 |

The full seven-row anchor comparison is retained in Step 2. Publication-day and expected-date windows are sensitivity benchmarks, not verified holding periods.

On the same 36 proxy-available firms, the raw close slope is 3.419. Adjusted slopes range from 3.386 to 3.412, with adjusted mean returns from 66.05% to 66.18%. Thus, the apparent stronger relation comes mainly from excluding seven firms. It does not result from locating the market window more accurately. Keep all 43 firms in the headline analysis.

### Table 9. Two economically relevant counterexamples

| Code | Filed range HK$ | Final HK$ | Revision % | Open % | Close % |
| --- | --- | --- | --- | --- | --- |
| 2672.HK | 15.60-20.28 | 15.60 | -13.04 | 291.67 | 367.95 |
| 3231.HK | 14.45-19.55 | 14.45 | -15.00 | 142.21 | 153.84 |

The offer-price clauses in both complete official prospectuses were checked for this report. Final prices and raw opening/close inputs were also checked in the stored allotment evidence and market caches. Key source URLs and PDF hashes are retained in key_counterexample_evidence.csv.

These two firms account for 85.2% of the slope increase from 1.598 to 3.419 in exact deletion-order accounting across the seven missing-proxy firms. About 82.1% of that slope change occurs at opening. This diagnoses selection sensitivity. It is not evidence that these firms are errors, nor a reason to delete observations that contradict a preferred story.

### Table 10. Date uncertainty without deleting any company

| Candidate anchor set | N | Slope low | Slope high | Mean low % | Mean high % |
| --- | --- | --- | --- | --- | --- |
| Subscription to publication | 43 | 1.474 | 1.678 | 67.17 | 70.03 |
| Prospectus to publication | 43 | 1.351 | 1.744 | 65.93 | 71.99 |

Each issuer may use any observed HSI daily close in the named set, including the latest close on or before its start date. All 43 firms remain; controls remain identical. These are sharp point-slope sensitivity bounds conditional on the assumed sets, not confidence intervals or certified actual pricing intervals.

Even the wider prospectus-to-publication set leaves the point slope between 1.351 and 1.744. That date effect is far smaller than the increase caused by selecting the 36 firms. It does not repair the wide statistical interval, and it cannot prove what the correct actual-date-adjusted coefficient is. HSI is a broad index; it does not remove sector shocks or issuer-specific news.

## 5. Range geometry, asymmetry and public information

$$
z=(P_0-P_L)/(P_H-P_L),\quad w=(P_H-P_L)/P_M,\quad v=w(z-1/2).
$$

Revision combines location within the range with the width of that range. The mean width is 15.67% of midpoint, its median is 13.97%, and its range is 3.00%-46.15%. The final price is at the lower endpoint for 13 firms, inside for 13 and at the upper endpoint for 17. No recorded final price is outside its filed range. A result from these offers is therefore not a direct replication of evidence about pricing above a preliminary upper limit.

### Table 11. Conditioning on range width

| Design / outcome | Slope | CV3 SE | WCR p | Holm p |
| --- | --- | --- | --- | --- |
| Revision / Offer to close | 1.648 | 1.007 | 0.191 | 0.766 |
| Position / Offer to close | 0.359 | 0.186 | 0.109 | 0.656 |
| Revision / Offer to opening | 0.897 | 0.979 | 0.359 | 0.766 |
| Position / Offer to opening | 0.213 | 0.190 | 0.293 | 0.766 |
| Revision / Opening to close | 0.751 | 0.193 | 0.023 | 0.188 |
| Position / Opening to close | 0.146 | 0.044 | 0.027 | 0.191 |
| Revision / HSI-adjusted close | 1.604 | 1.013 | 0.195 | 0.766 |
| Position / HSI-adjusted close | 0.351 | 0.187 | 0.125 | 0.656 |

Both designs include width and Q2/Q3. N=43, five parameters. Position is centered at 0.5 and measured on a 0-1 scale. Position and revision slopes have different units. Holm covers all eight geometry tests; these extensions are exploratory.

The width-controlled close slope is 1.648, near the main 1.598. The centered-position close slope is 0.359. These signs suggest that width alone does not remove the association. They do not establish a structural price-adjustment parameter. The exploratory intraday geometry p-values are smaller before adjustment, but none passes the eight-test Holm family.

### Table 12. Exploratory positive versus negative revision slopes

| Outcome | Positive | Negative | Difference | Diff WCR p | Holm p |
| --- | --- | --- | --- | --- | --- |
| Offer to close | 4.174 | -0.849 | 5.023 | 0.172 | 1.000 |
| Offer to opening | 3.217 | -1.350 | 4.567 | 0.203 | 1.000 |
| Opening to close | 0.957 | 0.501 | 0.456 | 0.723 | 1.000 |
| HSI-adjusted close | 4.125 | -0.888 | 5.013 | 0.172 | 1.000 |

Continuous hinge model with intercept and Q2/Q3; 21 positive and 22 negative revisions. The negative regressor retains its negative sign. Difference is positive slope minus negative slope. Holm covers both slopes and their difference for four outcomes: 12 tests.

The positive-revision close slope is 4.174; the negative-revision slope is -0.849. The difference has WCR p=0.172. None of the 12 asymmetry tests passes Holm adjustment; the smallest adjusted p-value is 0.797. The data are compatible with asymmetry, but cannot establish it. Different ranges of positive and negative revision and the small sample limit this test.

The prospectus-close to subscription-close HSI movement has a revision slope of 0.730, CV3 SE 0.658 and WCR p=0.293, with quarter controls. Its close-return slope conditional on revision and quarter is 1.236 (WCR p=0.637). This does not show that public information is ignored or fully incorporated. The calendar window is not verified to precede actual agreement for every firm, and HSI movement is an incomplete information measure.

$$
\ln(P_C/P_M)=\ln(P_0/P_M)+\ln(P_C/P_0).
$$

A shared-price problem also remains: with log(P0/PM) as regressor, the midpoint-close slope is exactly one plus the offer-close slope on the same design. That arithmetic is not an independent mechanism test. A final price is an endogenous choice, and the filed range can already contain expected demand information.

## 6. What the maximum-only offers add

The audit adds a separate disclosure regime, not 30 new midpoint revisions. These firms have an observed ceiling and a final price, so we can measure final price relative to ceiling. That measure is not revision relative to a two-sided midpoint.

$$
v_H=P_0/P_H-1.\qquad v_H=0\text{ means pricing at the ceiling.}
$$

### Table 13. Maximum-only offers: ceiling comparison

| Pricing position | N | Mean discount % | Mean close % | Median close % | Mean open % |
| --- | --- | --- | --- | --- | --- |
| Below ceiling | 4 | -2.72 | -0.16 | -0.51 | 2.13 |
| At ceiling | 26 | 0.00 | 9.68 | 3.72 | 9.48 |

Discount is negative below the ceiling. Twenty-six of 30 offers price at the ceiling. Only four offer ceiling-discount variation; all four are A+H. This comparison is descriptive.

### Table 14. Every below-ceiling case

| Code | Ceiling HK$ | Final HK$ | Discount % | Opening % | Close % |
| --- | --- | --- | --- | --- | --- |
| 2692.HK | 73.68 | 71.28 | -3.26 | 9.43 | 2.41 |
| 3223.HK | 102.80 | 100.00 | -2.72 | 0.00 | 0.00 |
| 3308.HK | 1010.00 | 980.00 | -2.97 | -0.92 | -2.04 |
| 9976.HK | 240.60 | 236.00 | -1.91 | 0.00 | -1.02 |

These four observations cannot support a rich ceiling-revision regression or a general trading rule. Their mean close return is -0.16%, versus 9.68% for the at-ceiling group; this is not a causal discount effect.

### Table 15. Listing-route overlap changes the comparison

| Route and disclosure | N | Mean close % | Median close % | Mean open % |
| --- | --- | --- | --- | --- |
| Non-A+H / range | 34 | 83.41 | 72.44 | 77.32 |
| A+H / range | 9 | 11.16 | 0.00 | 14.14 |
| A+H / maximum only | 29 | 8.88 | 2.94 | 8.79 |
| Other / maximum only | 1 | -6.54 | -6.54 | 0.00 |

The single non-A+H maximum-only case is Merdeka Gold depositary receipts, not a large comparable control group. Route categories are retained from the existing panel.

The all-firm mean close-return gap between range and maximum-only offers is 59.92 percentage points. Within A+H, it is only 2.28 percentage points: 11.16% versus 8.88%. This does not estimate a percentage of the gap caused by listing route; conditioning changes the population and leaves only nine range offers. It does show why a headline disclosure-format comparison is misleading. There is almost no non-A+H overlap in the maximum-only group.

For A+H issuers, the prospectus waiver often refers to the existing A-share market price as a pricing benchmark. Merdeka instead has an existing Indonesian share market. These source statements motivate benchmark and selection differences, but do not show equal A- and H-share valuations. Share classes, currency, investor access and market segmentation can differ. A rigorous cross-market valuation design would need dated reference-share prices and comparable conversion terms.

2041 is a separate caution. Its prospectus states a single price of HK$15.42, and its recorded close return is -42.93%. It belongs with single-price descriptions, not with maximum-only offers. The 30-firm maximum-only mean is now 8.36%, rather than the 6.71% mean for the old mixed 31-firm category. No source JSON or workbook was changed for this research overlay.

## 7. Findings, unresolved questions and supervisor brief

### Table 16. Which claims the current evidence supports

| Question | Assessment |
| --- | --- |
| Does midpoint revision predict later price gains? | Positive association; uncertain magnitude and adjusted inference. |
| Were prices already raised during bookbuilding? | Not established by a final price above the filed midpoint. |
| Are gains concentrated only at opening? | No. Opening and intraday components both enter the fitted relation. |
| Does market-date adjustment reverse the point sign? | No within the stated candidate sets; actual dates remain unverified. |
| Do contrary high-gain firms matter? | Yes. Two firms dominate the missing-proxy deletion effect. |
| Does maximum-only disclosure cause lower returns? | Not identified; severe route imbalance and little ceiling variation. |
| Has the current empirical topic been completed? | Yes as an association and sensitivity study; no causal mechanism claim. |

The conclusions use the full main sample. Selected deletions, new covariance methods and additional tests do not replace the maintained inference.

The central economic puzzle remains: an offer price can be below the first-day trading price even after investors have expressed interest. Investor information rewards, constrained offer-price setting, issuer and intermediary objectives, scarce tradable supply, demand pressure and market segmentation can each generate this pattern. The present variables do not discriminate among them. Neither a positive slope nor a high opening price certifies market inefficiency or deliberate underpricing.

The first-day close is a market outcome, not an observed fundamental value. Opening auctions and thin tradable supply may change the measured stage pattern. Underwriter support can affect downside returns. Sector news and company quality can affect both revision and trading returns. Quarter controls are coarse; small models reduce parameter count but cannot remove these channels. No valid instrument, natural experiment or dated sequence of indicative price proposals is available here.

The next evidence with the highest value is a dated sequence of indicative prices and price-agreement statements for the range offers, plus a verified inventory of any range amendments. That would distinguish an actual change during marketing from a comparison with a filed midpoint. Order-flow or later valuation evidence would be needed to call the stage results price discovery. These are requirements for stronger causal research, not missing calculations that a larger regression can supply.

## Supervisor discussion draft

We assess whether final offer-price revision is followed by further price gains in 113 Hong Kong Main Board IPOs listed in the first three quarters of 2026. Forty-three offers have usable two-sided ranges. A fresh source review separates 30 maximum-only offers from one single-price case. In the range sample, the quarter-controlled revision-close slope is positive, but its month-jackknife interval includes zero and the maintained multiple-test inference does not support a strong partial-adjustment claim. Opening and intraday components both contribute. Robust estimators and month deletions preserve the positive sign, while missing-date selection materially strengthens the estimate. Two below-midpoint, high-gain IPOs explain most of that selection effect. HSI anchor sensitivity is smaller when the companies are held fixed. Maximum-only offers provide limited ceiling-discount variation and differ sharply in listing route. We therefore report a robust sign pattern with uncertain magnitude, and a set of identification limits. We do not claim that prices were raised during subscription, that public information was ignored, or that the observed relation identifies investor-information compensation.

## 8. Technical appendix, provenance and replication

Month inference follows the cluster-jackknife approach in MacKinnon, Nielsen and Webb [2]. For each of nine listing months, re-estimate the complete design after deleting that month. Quarter indicators are re-estimated; they are not held at full-sample residual values. All retained designs are full rank.

$$
\widehat V_{CV3}=\frac{G-1}{G}\sum_{g=1}^{G}(\hat b_{(-g)}-\hat b)(\hat b_{(-g)}-\hat b)^{\prime},\qquad G=9.
$$

The covariance centers the deletion coefficients on the full-sample estimate, not their mean. An independent block-residual sandwich check agrees to numerical tolerance. Tests also verify the known variance of an intercept-only mean with equal-size clusters, row-duplication invariance, and rejection of singular deleted-cluster designs. Exact Rademacher enumeration remains coarse with nine clusters; CV3 and WCR need not agree in this finite sample.

The anchor calculation fixes the companies and regression design. For each company, adjusted log return equals log close return minus log listing-day HSI close plus log candidate anchor close. The coefficient is a weighted sum of outcomes. Choose each allowed lower or upper outcome according to the sign of its coefficient weight to obtain sharp bounds within the sensitivity box.

$$
a^{\prime}=e_v^{\prime}(X^{\prime}X)^{-1}X^{\prime},\qquad \hat\beta=a^{\prime}y,\\ \beta_{\min}=\sum_{a_i\geq0}a_i y_i^-+\sum_{a_i<0}a_i y_i^+,\quad \beta_{\max}=\sum_{a_i\geq0}a_i y_i^++\sum_{a_i<0}a_i y_i^-.
$$

Independent linear programming reproduces both bounds. The sets allow each company to select its own observed daily index anchor; the resulting worst cases are deliberately broad. They assume the chosen interval is relevant. They exclude unobserved intraday index levels and do not verify price agreement. No probability is attached to the bound endpoints.

Data provenance: The frozen 113-issuer panel is issuer_sample.csv in analysis/out/pricing_adjustment. The 31-issuer ledger in lower_bound_audit supplies official URLs, PDF pages and hashes. It is an analyst evidence record, not a formal source-writeback approval. The key two-company prospectus check is separate. Raw price and index series come from the documented Tencent market caches; official filings supply offer-price and disclosure evidence. Not every one of the 113 source fields was freshly certified in this topic.

Replication: Run analysis/pricing_topic1_completion_2026.py and then analysis/pricing_topic1_report.py with the project Python environment. The completion script needs the frozen panel, lower-bound ledger, earlier date ledger, baseline regression table and HSI cache. All are included or source-linked in the research package. It creates deterministic tables, manifests and checks. No investment simulation or random resampling is used. Earlier step scripts remain available for their separate source searches and estimator checks.

The report uses the existing editor filename to keep the open source stable. Its title and contents cover Topic 1 only. The former joint-report generator no longer overwrites this completed report automatically. Topic 2 and Topic 3 require separate reports after their own research is complete. Source-field corrections, expanded cohorts and later revisions can change these estimates; the cutoff and input hashes delimit the present result.

## References and source records

1. Hanley, K. W. (1993). The underpricing of initial public offerings and the partial adjustment phenomenon. Journal of Financial Economics 34, 231-250. [Source](https://business.lehigh.edu/sites/default/files/2019-08/7%20hanley_1993_jfe_0.pdf)

2. MacKinnon, J. G., Nielsen, M. O., and Webb, M. D. (2023). Fast and reliable jackknife and bootstrap methods for cluster-robust inference. [Source](https://arxiv.org/abs/2301.04527)

3. Official Medcaptain prospectus: single quoted price, PDF pages 2 and 293. [Source](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0828/2026082800009.pdf)

4. Official Baige prospectus: two-sided offer-price terms, PDF page 2. [Source](https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0618/2026061800045.pdf)

The Topic 1 result folder contains the issuer panel, all model estimates, cluster diagnostics, date sensitivity bounds, disclosure comparisons and source checks. Its README maps each result file to its research purpose. The run manifest records input hashes, package versions, checks and study limits.
