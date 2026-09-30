# Offer Mechanism A vs B, 2026 (N = 103 with a recorded mechanism)

Research plan line A proposes A vs B as a main hypothesis. The cross-tab shows why it cannot be identified as such.

## Who uses Mechanism A

| Mechanism | 18C | Not 18C |
|---|---|---|
| Mechanism A | 17 | 6 |
| Mechanism B | 0 | 80 |

| Mechanism | Apr-Jun | Other months |
|---|---|---|
| Mechanism A | 13 | 10 |
| Mechanism B | 29 | 51 |

- 17 of 17 18C issuers use Mechanism A. Only 6 of the 86 non-18C issuers with a mechanism are on A.
  "A vs B" is therefore almost the same variable as "18C vs the rest", and it is a choice made by the issuer.

## Raw contrast

Mean IR 69.5% (A, n = 23) vs 46.9% (B, n = 80); median
44.7% vs 13.7%. Welch p = 0.281, Mann-Whitney p = 0.157,
permutation p stratified by the Apr-Jun window = 0.340.

## Adjusted contrast, outcome log(1 + IR)

| Specification | Mechanism A coefficient (HC3 s.e.) | HC3 p | Wild cluster p | N | Min. detectable effect (log pts, 80% power) |
|---|---|---|---|---|---|
| Mechanism A only | 0.172 (0.109) | 0.114 | 0.277 | 103 | 0.30 |
| + Apr-Jun dummy | 0.097 (0.116) | 0.405 | 0.555 | 103 | 0.33 |
| + route (18A, 18C; A+H in controls) | -0.153 (0.176) | 0.386 | 0.684 | 103 | 0.49 |
| + route + size + fixed price | -0.159 (0.174) | 0.361 | 0.641 | 103 | 0.49 |

- Once route is held fixed the Mechanism A coefficient is identified from 6 non-18C issuers only, so its standard
  error is large. The sample cannot separate a mechanism effect from an 18C effect at any economically plausible size.
- Recommendation: fold Mechanism A vs B into the route/18C analysis as a descriptive note, or move it to a multi-year
  study. Do not present it as an independent 2026 hypothesis.
