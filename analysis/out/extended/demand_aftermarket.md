# Demand and aftermarket, 2026

## 1. What drives retail demand (OLS, HC3, M3 regressors; * p<0.10, ** p<0.05, *** p<0.01)

| Variable | ln subscription ratio | ln public applicants | ln average application value |
|---|---|---|---|
| ln firm age | -0.33 | -0.15 | -0.03 |
| ln offer size | -0.87*** | -0.02 | 0.12 |
| A+H issuer | -0.04 | -0.08 | 0.05 |
| VC/PE-backed | 0.90 | 0.34 | 0.50 |
| Top-tier sponsor | -0.23 | -0.17 | -0.05 |
| Cornerstone allocation | 1.53 | 0.93** | 0.59 |
| HSI return, prior 20 days | 5.75** | 2.33* | 3.31** |
| IPO count, prior 90 days | -0.03 | -0.02 | 0.01 |
| April-June hot window | 0.70 | 0.34 | 0.61** |
| R-squared | 0.44 | 0.31 | 0.24 |
| N | 105 | 105 | 105 |

- The hot-window coefficient implies retail oversubscription about 2.0x higher (HC3 p = 0.19: not significant);
  its size depends on the controls, because the HSI return carries part of the regime. Larger offers see lower multiples, partly by
  construction because the retail tranche scales with size.
- The final retail share after clawback is deliberately excluded as a regressor: it is a mechanical function of the multiple.

## 2. First-day return and demand

| Sample | N | d log(1+IR) / d ln subscription (HC3 s.e.) | R-squared |
|---|---|---|---|
| All | 113 | 0.112 (0.018) | 0.21 |
| April-June | 45 | 0.129 (0.044) | 0.13 |
| Other months | 68 | 0.076 (0.023) | 0.15 |

Interaction test (ln subscription x April-June), HC3 p = 0.285. Demand and IR are jointly determined; this is the Rock/Welch
association, not a causal effect.

## 3. Aftermarket returns, hot window vs other listings

BHR is measured from the day-1 close; WR is the wealth relative vs the HSI over the same horizon. Only matured windows appear.
The 3-month "other" group is January-March listings; the 3-month hot group is April to early June listings.

| Horizon | N (Apr-Jun / other) | Median BHR | Mean BHR | Mann-Whitney p (BHR) | Median WR vs HSI | Mann-Whitney p (WR) |
|---|---|---|---|---|---|---|
| Day 5 | 45 / 61 | -4.2% / 1.1% | -1.4% / 4.8% | 0.027 | 0.956 / 1.013 | 0.057 |
| Day 20 | 45 / 57 | -15.1% / 2.2% | -5.4% / 14.1% | 0.003 | 0.859 / 1.025 | 0.006 |
| 3 months | 45 / 37 | -29.7% / 0.3% | -16.8% / 35.2% | 0.001 | 0.767 / 1.034 | 0.007 |

- Deals listed in the hot window fall further after day 1: medians turn clearly negative by day 20, and
  the 3-month gap is the largest. Each horizon mixes different calendar windows, and these Mann-Whitney p-values treat every IPO as independent.
  `analysis/out/event_time/` redoes this with listing-month clustering and calendar-time portfolios, where the gap is weaker: read that first.

## 4. Does a high day-1 return predict a later reversal?

| Horizon | N | Spearman IR vs BHR (p) | OLS slope on IR, controlling Apr-Jun (HC3 p) |
|---|---|---|---|
| Day 5 | 106 | -0.06 (0.525) | 0.021 (0.539) |
| Day 20 | 102 | -0.07 (0.468) | 0.031 (0.665) |
| 3 months | 82 | -0.21 (0.054) | -0.012 (0.921) |

Unconditionally, higher first-day returns go with weaker 3-month BHR (rank correlation above), but the association disappears once the
Apr-Jun dummy is included. This is consistent with reversal being a feature of the listing window rather than of individual deals.

## 5. Stabilization and greenshoe by IR bin

| IR bin | N | Stabilization purchases | Mean greenshoe exercise rate | Median day-20 BHR |
|---|---|---|---|---|
| IR <= 0 | 32 | 100% | 7% | -1.7% |
| 0 to 25% | 30 | 20% | 38% | 2.4% |
| 25% to 100% | 24 | 0% | 61% | 2.2% |
| > 100% | 27 | 0% | 31% | -9.6% |

Stabilization purchases cluster in weak deals and greenshoe exercise in strong ones, as the mechanism implies; both are consequences of
the first-day price, not explanatory variables for it.
