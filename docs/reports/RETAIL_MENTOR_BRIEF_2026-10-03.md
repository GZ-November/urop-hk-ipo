# From headline IPO returns to retail application returns

Mentor discussion draft | 3 October 2026 | Price observation cutoff: 30 September 2026

## Research question and sample

How much of a new listing's first-day return reaches a retail investor who applies for one lot? We study 113 ordinary Hong Kong Main Board IPOs listed from 2 January to 30 September 2026 (Q1: 38; Q2: 45; Q3: 30). Each IPO receives equal weight. Allocation expectations come from the disclosed application tier, including guarantees and additional ballots; they describe a hypothetical applicant in that tier, rather than the average actual retail account.

Source follow-up resolves two earlier qualifications. ALSCO (2649) officially corrected its board lot to 500 shares; its minimum application is also 500 shares, so the one-lot sample now includes all 113 IPOs. FS.COM (3355) subsequently disclosed the ten Pool B guarantees previously inferred in our data; all ten match. The 19 corrected application totals match 763 quantity/count pairs read afresh from the original PDFs. All 19 formal extraction totals have now been repaired and independently reviewed for col_CO; the old values are preserved in before snapshots. This is a scoped field review, not whole-payload writeback approval. This draft uses a separately documented lot-size overlay and does not rewrite pipeline approvals. See the [evidence assessment](RETAIL_EVIDENCE_ASSESSMENT_2026-10-03.md).

## 1. How far are headline returns from application returns?

| Measure | IPO mean | IPO median |
| --- | --- | --- |
| First-day return on allocated securities | 53.15% | 14.82% |
| Expected gross return on one-lot application principal | 2.08% | 0.59% |
| Expected gross profit per application (HK$) | 91.77 | 27.00 |

The mean difference is **51.07 percentage points**. This is a difference between return denominators: the headline return is earned on allocated securities, while the application return spreads the expected profit across all requested principal. The application principal here equals requested quantity times the final offer price; it excludes application levies and does not measure peak cash blocked at the maximum offer price. The median is the median across IPO-specific expectations, not a median investor outcome. The single HDR issuer is calculated in its own disclosed security units.

## 2. What does the allocation-return relationship contribute?

For IPO i, define a_i as expected allotted quantity divided by requested quantity, and r_i as first-day close divided by offer price minus one. Expected application return is a_i r_i. The exact equal-IPO decomposition is:

`mean(a*r) = mean(a)*mean(r) + Cov_N(a,r)`

The product of means is **5.73%**, and the covariance contributes **-3.65 percentage points**, leaving **2.08%**. The negative covariance offsets **63.6%** of the product-of-means component. Covariance uses denominator N, so the identity is exact.

This describes a combination of smaller allocations in high-return IPOs and larger allocations in weaker IPOs. The product of means is an algebraic comparison; it does not identify the return from changing an allocation rule. Demand, offer size and issuer characteristics can jointly affect allocations and returns, so the decomposition does not establish causation or investor information types.

## 3. How sensitive are the conclusions?

**Across quarters:** the covariance is negative in every quarter, while the expected monetary gain varies considerably.

| Quarter | N | Mean first-day return | Mean application return | Covariance (pp) | Mean gross profit (HK$) |
| --- | --- | --- | --- | --- | --- |
| 2026Q1 | 38 | 33.86% | 1.71% | -2.17 | 121.14 |
| 2026Q2 | 45 | 92.70% | 2.98% | -2.00 | 123.32 |
| 2026Q3 | 30 | 18.27% | 1.21% | -2.08 | 7.24 |

**Fees:** gross profit is the baseline. All nonzero fees below are hypothetical per-application scenarios paid regardless of allocation.

| Assumed fee (HK$) | Mean expected profit (HK$) | Median IPO expected profit (HK$) | Mean return after fee |
| --- | --- | --- | --- |
| 0 | 91.77 | 27.00 | 2.08% |
| 28 | 63.77 | -1.00 | 1.43% |
| 88 | 3.77 | -61.00 | 0.02% |
| 100 | -8.23 | -73.00 | -0.26% |

The average gross profit implies a handling-fee-only break-even level of HK$91.77 per application in this observed sample. It is not a complete-cost threshold: allotted-security subscription brokerage and levies, selling costs, financing and opportunity cost are excluded. HK$88 is a sensitivity parameter, not evidence of historical account fees. An average after-fee application return is the mean of profit/principal across IPOs, so it need not equal mean HK$ profit divided by mean principal.

**Large winners:** removing the IPOs with the largest expected one-lot gross profits leaves positive mean gross profit, but changes the sign under the HK$88 scenario.

| Largest-profit IPOs excluded | N | Mean gross profit (HK$) | Mean profit with HK$88 fee | Excluded codes |
| --- | --- | --- | --- | --- |
| 0 | 113 | 91.77 | 3.77 | None |
| 1 | 112 | 77.41 | -10.59 | 0501.HK |
| 3 | 110 | 58.48 | -29.52 | 0501.HK;2672.HK;3231.HK |

These exclusions are retrospective influence checks, not subscription selection rules. The ranking uses expected one-lot HK$ profit, rather than headline percentage returns.

**Source exclusions:** the main allocation-return pattern also remains after removing the flagged issuers.

| Sample | N | Mean application return | Covariance (pp) | Mean gross profit (HK$) |
| --- | --- | --- | --- | --- |
| Corrected one-lot baseline | 113 | 2.08% | -3.65 | 91.77 |
| Exclude 2649 (previous strict sample) | 112 | 2.10% | -3.77 | 92.59 |
| Exclude 3355 | 112 | 2.10% | -3.71 | 92.54 |
| Exclude 19 total corrections | 94 | 2.48% | -4.06 | 109.62 |
| Exclude all 21 flagged issuers | 92 | 2.53% | -4.32 | 111.95 |

Exclusions change issuer and quarter composition; their differences cannot be attributed solely to data quality. One-lot expected profits depend on the selected tier, not on an issuer's aggregate application total. Consequently, the 19 total corrections do not mechanically change this draft's one-lot results; they matter for aggregate allocation rates and data consistency.

## Interpretation and next discussion

The contribution is to quantify the distance between IPO returns on allotted securities and returns on requested retail capital using actual tier rules. The negative allocation-return covariance is stable in the reported source exclusions and quarters; the profitability conclusion depends on fees, period and large winners. These are exploratory, sample-specific expectations conditional on observed first-day closing prices, not realized account returns, annualized performance or forecasts. This draft uses no simulation, bootstrap, or new hypothesis tests and makes no population significance claim.

For discussion with the supervisor: is this allocation-adjusted descriptive question a sufficient research focus, and which institutional comparison would add an economic explanation without overstating identification?

## Reproduction

From the repository root, with the cited official PDFs cached locally:

```bash
.venv/bin/python tools/audit_retail_sources_2026.py
.venv/bin/python analysis/retail_evidence_brief_2026.py
```

Tables and issuer-level results: [deterministic outputs](../../analysis/out/retail_evidence_brief/). [Run manifest](../../analysis/out/retail_evidence_brief/run_manifest.json) records hashes; the [source manifest](../../pipeline/reports/data_gap_collection/source_followup_2026-10-03/source_manifest.json) records official URLs and local PDF hashes. Earlier portfolio simulations are not used in this draft.
