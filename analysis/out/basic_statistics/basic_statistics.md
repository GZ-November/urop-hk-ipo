# 2026 IPO Basic Statistics and Data Coverage

Sample: 113 ordinary Main Board IPOs listed from 2026-01-02 to 2026-09-30; observation cutoff 2026-09-30. Only actual 2026 listing dates are selected.
This report contains descriptive statistics and rank correlations, without regressions or significance tests. It retains the current raw-price and security-unit corrections.

## 1. Core-field coverage

| field | n_present | n_missing |
|---|---|---|
| IPO Subscription Price (HK$) | 113 | 0 |
| Profit for the year in year-1 | 112 | 1 |
| Pre-IPO VC/PE backing (1=yes; 0=no) | 106 | 7 |
| Industry classification code | 113 | 0 |
| Firm age at IPO (years) | 113 | 0 |
| Final cornerstone allocation (% of base offer) | 113 | 0 |
| Subscription Ratio (times) | 113 | 0 |
| Public applicants | 113 | 0 |
| Public valid applied shares | 113 | 0 |
| Pricing date | 59 | 54 |
| Final public offer shares | 113 | 0 |
| Unrestricted public shareholding at listing (%) | 112 | 1 |
| First-day return / Underpricing (%) | 113 | 0 |
| First trading day turnover (HK$) | 106 | 7 |
| 6-month BHR from Day-1 close (%) | 37 | 76 |
| Day-5 BHR from Day-1 close (%) | 106 | 7 |
| Day-20 BHR from Day-1 close (%) | 102 | 11 |
| 3-month BHR from Day-1 close (%) | 82 | 31 |

Coverage means a value is stored in the master, not that the original disclosure has been independently verified. See field_coverage.csv for all registered fields and core_missing_records.csv for issuers with missing core inputs. Unmatured, undisclosed, uncollected and inapplicable values must be distinguished; missing values are not automatically zero. Fixed-price offers have no within-range revision.

Base offer proceeds equal offer price times base offered security units. Share and HDR units follow the current repairs; this measure is not proceeds including greenshoe exercise or issuer net proceeds.

## 2. Descriptive statistics

| variable | count | mean | std | min | 25% | 50% | 75% | max |
|---|---|---|---|---|---|---|---|---|
| First-day return (%) | 113.0 | 53.153 | 85.291 | -56.895 | 0.0 | 14.822 | 91.735 | 383.624 |
| Base offer proceeds (HK$ million) | 113.0 | 3178.722 | 5975.644 | 200.0 | 717.211 | 1233.134 | 3677.438 | 53410.0 |
| Public subscription multiple (times) | 113.0 | 1985.186 | 2482.093 | 3.39 | 174.12 | 1073.37 | 2730.73 | 14855.4 |
| Public applicants (persons) | 113.0 | 154730.204 | 94449.618 | 12645.0 | 66692.0 | 153878.0 | 207986.0 | 471116.0 |
| Firm age (years) | 113.0 | 15.085 | 7.027 | 0.67 | 9.97 | 13.49 | 20.0 | 33.58 |
| Cornerstone allocation (%) | 113.0 | 32.901 | 19.138 | 0.0 | 16.13 | 38.586 | 49.77 | 68.63 |
| Issuer-average allocation rate (%) | 113.0 | 1.687 | 4.968 | 0.011 | 0.056 | 0.108 | 0.634 | 29.532 |
| Application gross return (%, proportional allocation scenario) | 113.0 | 0.02 | 0.442 | -2.698 | 0.0 | 0.025 | 0.09 | 1.748 |

Application gross return equals issuer-average allocation rate times first-day return. This is a proportional-allocation scenario, not a one-lot ballot probability, actual account outcome or fee-adjusted profit. Here the aggregate rate retains the legacy final-public/applications denominator; the tier-based retail study separately excludes employee reserved allotments. Ratios above one or nonpositive ratios remain missing rather than being capped. Means and medians are reported together to show tail sensitivity.

## 3. Quarters and listing routes

| group | ir_n | mean_ir_pct | median_ir_pct | break_share_pct |
|---|---|---|---|---|
| 2026Q1 | 38.0 | 33.861 | 13.409 | 10.526 |
| 2026Q2 | 45.0 | 92.703 | 79.992 | 17.778 |
| 2026Q3 | 30.0 | 18.266 | 0.0 | 46.667 |
| 18A biotech | 11.0 | 79.579 | 102.747 | 9.091 |
| 18C specialist tech | 19.0 | 66.533 | 13.167 | 26.316 |
| A+H (19A) | 36.0 | 10.18 | 2.675 | 30.556 |
| Conventional | 47.0 | 74.476 | 44.737 | 19.149 |

Routes are mutually exclusive in the order 18A, 18C, A+H and conventional. The separate A+H flag can overlap 18C. Each return cell has its own valid N. Small groups are descriptive; the complete monthly table is in group_comparisons.csv.

## 4. Subscription-demand terciles

| group | ir_n | mean_ir_pct | median_ir_pct | break_share_pct | mean_application_gross_return_pct |
|---|---|---|---|---|---|
| Low demand | 38.0 | 13.909 | 0.0 | 42.105 | -0.023 |
| Middle demand | 37.0 | 52.143 | 33.556 | 10.811 | 0.046 |
| High demand | 38.0 | 93.381 | 82.006 | 15.789 | 0.037 |

Groups use subscription quantiles in the observed sample, not external regulatory thresholds. Differences may also reflect offer size, listing month and route composition.

## 5. Rank correlations with first-day returns

| variable | pair_n | spearman_with_ir |
|---|---|---|
| Public subscription multiple (times) | 113.0 | 0.518 |
| Public applicants (persons) | 113.0 | 0.478 |
| Base offer proceeds (HK$ million) | 113.0 | -0.234 |
| Firm age (years) | 113.0 | -0.18 |
| Cornerstone allocation (%) | 113.0 | -0.068 |

Spearman correlations describe rankings and do not identify causal effects. Each pair uses its own finite sample, separately from regression complete-case samples.

## 6. Current research

See the [English empirical report](../../../docs/reports/EMPIRICAL_RESEARCH_REPORT_2026.md) for tier-based retail profits and demand robustness; see [the research plan](../../../docs/RESEARCH_PLAN_2026.md) and [data gaps](../../../docs/DATA_GAPS_2026.md) for scope and collection priorities.
