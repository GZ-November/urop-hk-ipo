# Aftermarket returns of 2026 IPOs from daily bars (106 of 106 issuers, last bar 2026-09-29)

Bars are the cached Tencent series in `data/market/aftermarket`; benchmark returns are aligned to each issuer's own bar dates.
Issuers have between 12 and 180 trading days after listing, so long horizons cover
earlier listings only (N shown per row). "Hot" = listed April-June (calendar dummy used throughout the analysis).

## Reading

- Event time, treating each IPO as independent, shows a large hot-vs-other gap that grows with the horizon. With listing-month clustering
  it is weaker (day-60 wild cluster p = 0.031); the ordinary Mann-Whitney and HC3 p-values overstate it.
- Calendar time, which counts each date once, gives the April-June portfolio an excess return not distinguishable from zero (p = 0.50), the other
  listings a positive excess return (p = 0.039), and no significant difference between them (p = 0.27).
- So the evidence supports "January-March listings did well after day 1" more than "April-June listings collapsed"; the two are not the same claim,
  and a 9-month sample cannot separate them from the market path of each window.

## 1. Event time: BHAR from the day-1 close, benchmark HSI

| Trading days after day 1 | N (hot / other) | Mean BHAR | Median BHAR | Mean difference | HC3 p | Wild cluster p (9 months) | Mann-Whitney p |
|---|---|---|---|---|---|---|---|
| 5 | 45 / 61 | -4.0% / 5.1% | -5.5% / 0.7% | -9.1 pp | 0.051 | 0.113 | 0.022 |
| 20 | 45 / 55 | -6.9% / 13.2% | -15.3% / 1.3% | -20.1 pp | 0.020 | 0.109 | 0.004 |
| 40 | 45 / 53 | -12.7% / 24.4% | -27.9% / 0.1% | -37.0 pp | 0.009 | 0.062 | 0.002 |
| 60 | 45 / 38 | -19.1% / 40.0% | -33.1% / 0.5% | -59.1 pp | 0.006 | 0.031 | 0.000 |
| 90 | 16 / 37 | -29.8% / 45.8% | -38.1% / -7.7% | -75.6 pp | 0.009 | 0.250 | 0.006 |

- Inference: HC3 ignores clustering; the wild cluster p uses exact enumeration over listing months (the hot dummy is constant within a month,
  so only 9 clusters, 3 treated, identify the difference; it is the appropriate but low-power test). Mann-Whitney ignores clustering.
- Horizons mix calendar windows: the 90-day "other" group is mostly January-March listings, whose window overlaps the April-June rally.

Same table, benchmark HSTECH:

| Trading days after day 1 | N (hot / other) | Mean BHAR | Median BHAR | Mean difference | HC3 p | Wild cluster p (9 months) | Mann-Whitney p |
|---|---|---|---|---|---|---|---|
| 5 | 45 / 61 | -4.6% / 6.2% | -7.2% / 1.8% | -10.8 pp | 0.023 | 0.090 | 0.005 |
| 20 | 45 / 55 | -6.2% / 17.0% | -18.4% / 4.0% | -23.2 pp | 0.007 | 0.016 | 0.001 |
| 40 | 45 / 53 | -9.7% / 30.3% | -21.8% / 6.6% | -40.0 pp | 0.005 | 0.031 | 0.000 |
| 60 | 45 / 38 | -13.7% / 45.4% | -26.6% / 7.2% | -59.2 pp | 0.006 | 0.031 | 0.000 |
| 90 | 16 / 37 | -23.0% / 51.1% | -31.8% / -3.1% | -74.1 pp | 0.011 | 0.250 | 0.009 |

![BHAR paths](fig7_bhar_paths.png)

## 2. Calendar time: equal-weighted portfolios in days 1-60 after listing

Each date's portfolio averages the excess return of all issuers in their first 60 trading days after day 1, requires at least
5 issuers, and uses Newey-West standard errors (10 lags). This treats overlapping same-window IPOs as one observation per date.

Benchmark HSI:

| Portfolio | Days | Mean issuers/day | Excess return, bp/day | NW t (p) | CAPM alpha, bp/day | CAPM beta | CAPM alpha NW t (p) |
|---|---|---|---|---|---|---|---|
| April-June listings | 104 | 26 | -18.6 | -0.67 (0.502) | -19.7 | 0.59 | -0.76 (0.446) |
| Other listings | 170 | 19 | 36.5 | 2.06 (0.039) | 36.9 | 1.06 | 2.12 (0.034) |
| Hot minus other (dates with both) | 99 | — | -32.1 | -1.11 (0.268) | — | — | — |

Benchmark HSTECH:

| Portfolio | Days | Mean issuers/day | Excess return, bp/day | NW t (p) | CAPM alpha, bp/day | CAPM beta | CAPM alpha NW t (p) |
|---|---|---|---|---|---|---|---|
| April-June listings | 104 | 26 | -13.8 | -0.49 (0.626) | -16.3 | 0.66 | -0.62 (0.534) |
| Other listings | 170 | 19 | 48.0 | 2.76 (0.006) | 44.3 | 0.80 | 2.52 (0.012) |
| Hot minus other (dates with both) | 99 | — | -32.1 | -1.11 (0.268) | — | — | — |

- Alpha is per trading day in basis points (100 bp = 1%). The "Other" portfolio is largely January-March listings, so it and the hot portfolio face different market paths;
  the CAPM columns control the common market move but not a different sentiment regime.
- Calendar-time p-values are typically much larger than event-time ones because they count each date once.

## 3. Multiplicity

| Test | p | q (BH) |
|---|---|---|
| BHAR vs HSI, day 20: hot minus other (wild cluster) | 0.1094 | 0.1823 |
| BHAR vs HSI, day 60: hot minus other (wild cluster) | 0.0312 | 0.0981 |
| Calendar-time alpha vs HSI, April-June listings | 0.5023 | 0.5023 |
| Calendar-time alpha vs HSI, Other listings | 0.0392 | 0.0981 |
| Calendar-time spread, hot minus other, vs HSI | 0.2682 | 0.3353 |

The comparisons above are the headline aftermarket claims; the earlier Mann-Whitney p-values in `analysis/out/extended/` correspond to the event-time design without clustering.
