# Subscription demand: exploratory associations

Final demand is observed after pricing; these groups are retrospective. HC3 and exact Rademacher bootstrap use nine listing-month clusters.

## demand_summary.csv

|  | Group | N | Mean IR (%) | Median IR (%) | P25 IR (%) | P75 IR (%) | Break Rate (%) | Median Sub (x) | Median Applicants | Median Proceeds (HK$M) | Mean Public Offer (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Full Sample (2026) | 113 | 53.15% | 14.82% | 0.00% | 91.73% | 23.0% | 1073.4x | 153,878 | 1233.1 | 11.5% |
| 1 | Low demand (Sub: 3.4x - 356.9x) | 38 | 13.91% | 0.00% | -4.87% | 10.19% | 42.1% | 95.2x | 51,928 | 2977.9 | 10.4% |
| 2 | Mid demand (Sub: 399.1x - 2003.2x) | 37 | 52.14% | 33.56% | 2.94% | 102.75% | 10.8% | 1073.4x | 177,196 | 1620.0 | 10.5% |
| 3 | High demand (Sub: 2007.6x - 14855.4x) | 38 | 93.38% | 82.01% | 9.07% | 127.49% | 15.8% | 4581.7x | 222,377 | 854.8 | 13.5% |

## demand_subgroups.csv

|  | Category | Subgroup | Demand Group | N | Mean IR (%) | Median IR (%) | Break Rate (%) | Median Sub (x) | Median Proceeds (HK$M) | Mean Public Offer (%) | Median Public Offer (%) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Quarter | 2026Q1 | Low demand | 13 | 2.15% | 1.53% | 23.1% | 68.9x | 1639.0 | 10.1% | 10.0% |
| 1 | Quarter | 2026Q1 | Mid demand | 14 | 36.74% | 22.86% | 0.0% | 1082.7x | 3488.2 | 11.2% | 10.0% |
| 2 | Quarter | 2026Q1 | High demand | 11 | 67.67% | 75.82% | 9.1% | 3118.4x | 499.2 | 13.2% | 10.0% |
| 3 | Quarter | 2026Q2 | Low demand | 5 | 80.77% | 0.00% | 40.0% | 134.4x | 4600.9 | 9.7% | 10.0% |
| 4 | Quarter | 2026Q2 | Mid demand | 18 | 71.87% | 62.81% | 16.7% | 1120.1x | 1253.3 | 10.2% | 10.0% |
| 5 | Quarter | 2026Q2 | High demand | 22 | 112.46% | 100.00% | 13.6% | 5632.5x | 940.5 | 13.2% | 10.0% |
| 6 | Quarter | 2026Q3 | Low demand | 20 | 4.84% | -0.57% | 55.0% | 117.1x | 4715.9 | 10.7% | 10.0% |
| 7 | Quarter | 2026Q3 | Mid demand | 5 | 24.26% | 0.00% | 20.0% | 927.4x | 600.0 | 10.0% | 10.0% |
| 8 | Quarter | 2026Q3 | High demand | 5 | 65.99% | 5.06% | 40.0% | 3646.1x | 682.0 | 16.0% | 20.0% |
| 9 | Listing Route | A+H Issuers | Low demand | 23 | -0.06% | 0.00% | 47.8% | 79.5x | 4930.8 | 10.2% | 10.0% |
| 10 | Listing Route | A+H Issuers | Mid demand | 14 | 24.83% | 14.04% | 7.1% | 638.4x | 3186.7 | 9.9% | 10.0% |
| 11 | Listing Route | A+H Issuers | High demand | 1 | 11.56% | 11.56% | 0.0% | 2251.8x | 1080.0 | 10.0% | 10.0% |
| 12 | Listing Route | Non-A+H Issuers | Low demand | 15 | 35.32% | 7.41% | 33.3% | 104.8x | 1103.0 | 10.7% | 10.0% |
| 13 | Listing Route | Non-A+H Issuers | Mid demand | 23 | 68.77% | 69.06% | 13.0% | 1159.5x | 1198.7 | 10.9% | 10.0% |
| 14 | Listing Route | Non-A+H Issuers | High demand | 37 | 95.59% | 84.02% | 16.2% | 4591.4x | 843.7 | 13.6% | 10.0% |
| 15 | Offer Size | Small deal | Low demand | 7 | 57.52% | -9.18% | 57.1% | 140.0x | 650.2 | 11.6% | 10.0% |
| 16 | Offer Size | Small deal | Mid demand | 9 | 58.04% | 44.25% | 33.3% | 1073.4x | 584.0 | 10.6% | 10.0% |
| 17 | Offer Size | Small deal | High demand | 22 | 114.51% | 105.27% | 13.6% | 4702.0x | 610.7 | 12.7% | 10.0% |
| 18 | Offer Size | Mid deal | Low demand | 11 | 4.29% | 4.17% | 36.4% | 143.5x | 1225.4 | 10.7% | 10.0% |
| 19 | Offer Size | Mid deal | Mid demand | 12 | 59.04% | 26.70% | 8.3% | 1239.2x | 1292.7 | 10.0% | 10.0% |
| 20 | Offer Size | Mid deal | High demand | 14 | 40.70% | 29.24% | 21.4% | 4203.7x | 1191.2 | 14.1% | 10.0% |
| 21 | Offer Size | Large deal | Low demand | 20 | 3.94% | 0.00% | 40.0% | 48.9x | 6155.2 | 9.8% | 10.0% |
| 22 | Offer Size | Large deal | Mid demand | 16 | 43.65% | 35.54% | 0.0% | 817.3x | 4374.4 | 10.9% | 10.0% |
| 23 | Offer Size | Large deal | High demand | 2 | 229.72% | 229.72% | 0.0% | 4066.1x | 4055.1 | 18.7% | 18.7% |

## demand_regressions.csv

|  | Specification | Focus Regressor | Coefficient (HC3 SE) | HC3 p-value | Wild Cluster p | R-squared | N | G | coefficient | hc3_se | ci_lower | ci_upper |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0 | M1: Raw Subscription Multiple | lsub | 0.1124*** (0.0181) | 0.0 | 0.0078 | 0.209 | 113 | 9 | 0.1124435186191109 | 0.0181285559787836 | 0.0769122018089766 | 0.1479748354292452 |
| 1 | M2: + Offer Proceeds (Deal Size) | lsub | 0.1185*** (0.0246) | 0.0 | 0.0078 | 0.211 | 113 | 9 | 0.118495638094455 | 0.0245618570155324 | 0.0703552829505889 | 0.1666359932383211 |
| 2 | M3: + A+H Anchor, Firm Age, Cornerstone | lsub | 0.1149*** (0.0252) | 0.0 | 0.0078 | 0.266 | 113 | 9 | 0.114928749243375 | 0.0251651425685211 | 0.0656059761432577 | 0.1642515223434923 |
| 3 | M4: + Hot Window (April-June / Q2) | lsub | 0.0934*** (0.0272) | 0.0006 | 0.0039 | 0.308 | 113 | 9 | 0.0934439945037488 | 0.0272454070592691 | 0.0400439779234479 | 0.1468440110840497 |
| 4 | M5: Raw Applicant Count | lapp | 0.2405*** (0.0484) | 0.0 | 0.0078 | 0.159 | 113 | 9 | 0.240454580790998 | 0.048395480862416 | 0.145601181286165 | 0.335307980295831 |
| 5 | M6: Applicant Count + Full Controls | lapp | 0.1682*** (0.0605) | 0.0054 | 0.0352 | 0.284 | 113 | 9 | 0.1681774629491053 | 0.0604744857511215 | 0.0496496488933264 | 0.2867052770048842 |

## aftermarket_performance.csv

|  | Group | N | Mean Day-1 IR (%) | Median Day-1 IR (%) | Mean Day-5 BHR (%) | Median Day-5 BHR (%) | Positive Day-5 (%) | Mean Day-20 BHR (%) | Median Day-20 BHR (%) | Positive Day-20 (%) |
|---|---|---|---|---|---|---|---|---|---|---|
| 0 | Full Balanced Sample | 102 | 55.64% | 18.75% | 2.60% | -0.80% | 46.1% | 5.49% | -0.97% | 47.1% |
| 1 | Low demand | 30 | 12.56% | 0.00% | 0.74% | -1.17% | 43.3% | 2.09% | -6.35% | 33.3% |
| 2 | Mid demand | 36 | 54.78% | 35.54% | 5.12% | 1.53% | 52.8% | 16.71% | 6.87% | 63.9% |
| 3 | High demand | 36 | 92.40% | 82.01% | 1.63% | -4.06% | 41.7% | -2.90% | -7.66% | 41.7% |
