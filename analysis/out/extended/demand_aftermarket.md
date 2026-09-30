# Demand and aftermarket, 2026

## 1. What drives retail demand (OLS, HC3, M3 regressors; * p<0.10, ** p<0.05, *** p<0.01)

| Variable | ln subscription ratio | ln public applicants | ln average application value |
|---|---|---|---|
| ln firm age | -0.32 | -0.16 | -0.07 |
| ln offer size | -1.01*** | -0.11 | -0.04 |
| A+H issuer | 0.02 | 0.03 | 0.29 |
| VC/PE-backed | 0.89** | 0.40* | 0.57* |
| Top-tier sponsor | -0.28 | -0.21* | -0.08 |
| Cornerstone allocation | 2.07** | 1.19*** | 1.01* |
| HSI return, prior 20 days | 5.34* | 2.14* | 3.41** |
| IPO count, prior 90 days | -0.03 | -0.02 | 0.00 |
| April-June hot window | 0.68 | 0.27 | 0.51* |
| R-squared | 0.53 | 0.34 | 0.24 |
| N | 106 | 106 | 106 |

- The hot-window coefficient implies retail oversubscription about 2.0x higher (HC3 p = 0.17: not significant);
  its size depends on the controls, because the HSI return carries part of the regime. Larger offers see lower multiples, partly by
  construction because the retail tranche scales with size.
- The final retail share after clawback is deliberately excluded as a regressor: it is a mechanical function of the multiple.

## 2. First-day return and demand

| Sample | N | d log(1+IR) / d ln subscription (HC3 s.e.) | R-squared |
|---|---|---|---|
| All | 106 | 0.114 (0.021) | 0.19 |
| April-June | 45 | 0.134 (0.046) | 0.14 |
| Other months | 61 | 0.069 (0.025) | 0.11 |

Interaction test (ln subscription x April-June), HC3 p = 0.219. Demand and IR are jointly determined; this is the Rock/Welch
association, not a causal effect.

## 3. Aftermarket returns, hot window vs other listings

BHR is measured from the day-1 close; WR is the wealth relative vs the HSI over the same horizon. Only matured windows appear.
The 3-month "other" group is January-March listings; the 3-month hot group is April to early June listings.

| Horizon | N (Apr-Jun / other) | Median BHR | Mean BHR | Mann-Whitney p (BHR) | Median WR vs HSI | Mann-Whitney p (WR) |
|---|---|---|---|---|---|---|
| Day 5 | 45 / 61 | -4.2% / 1.1% | -1.4% / 4.8% | 0.027 | 0.956 / 1.013 | 0.057 |
| Day 20 | 45 / 55 | -15.1% / 4.6% | -5.4% / 15.5% | 0.002 | 0.859 / 1.025 | 0.006 |
| 3 months | 41 / 37 | -28.6% / -3.3% | -14.8% / 34.5% | 0.008 | 0.686 / 0.973 | 0.001 |

- Deals listed in the hot window fall further after day 1: medians turn clearly negative by day 20, and
  the 3-month gap is the largest. Each horizon mixes different calendar windows, and these Mann-Whitney p-values treat every IPO as independent.
  `analysis/out/event_time/` redoes this with listing-month clustering and calendar-time portfolios, where the gap is weaker: read that first.

## 4. Does a high day-1 return predict a later reversal?

| Horizon | N | Spearman IR vs BHR (p) | OLS slope on IR, controlling Apr-Jun (HC3 p) |
|---|---|---|---|
| Day 5 | 106 | -0.07 (0.473) | 0.020 (0.543) |
| Day 20 | 100 | -0.11 (0.295) | 0.027 (0.699) |
| 3 months | 78 | -0.21 (0.067) | -0.022 (0.844) |

Unconditionally, higher first-day returns go with weaker 3-month BHR (rank correlation above), but the association disappears once the
Apr-Jun dummy is included. This is consistent with reversal being a feature of the listing window rather than of individual deals.

## 5. Stabilization and greenshoe by IR bin

| IR bin | N | Stabilization purchases | Mean greenshoe exercise rate | Median day-20 BHR |
|---|---|---|---|---|
| IR <= 0 | 33 | 21% | 12% | -0.9% |
| 0 to 25% | 24 | 25% | 45% | 4.0% |
| 25% to 100% | 23 | 0% | 59% | 2.1% |
| > 100% | 26 | 0% | 32% | -9.6% |

Stabilization purchases cluster in weak deals and greenshoe exercise in strong ones, as the mechanism implies; both are consequences of
the first-day price, not explanatory variables for it.
