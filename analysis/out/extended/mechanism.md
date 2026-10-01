# Offer Mechanism A vs B, 2026 (N = 110 with a recorded mechanism)

Research plan line A proposes A vs B as a main hypothesis. The cross-tab shows why it cannot be identified as such.

## Who uses Mechanism A

| Mechanism | 18C | Not 18C |
|---|---|---|
| Mechanism A | 19 | 6 |
| Mechanism B | 0 | 85 |

| Mechanism | Apr-Jun | Other months |
|---|---|---|
| Mechanism A | 13 | 12 |
| Mechanism B | 29 | 56 |

- 19 of 19 18C issuers use Mechanism A. Only 6 of the 91 non-18C issuers with a mechanism are on A.
  "A vs B" is therefore almost the same variable as "18C vs the rest", and it is a choice made by the issuer.

## Raw contrast

Mean IR 63.8% (A, n = 25) vs 48.7% (B, n = 85); median
44.2% vs 13.4%. Welch p = 0.442, Mann-Whitney p = 0.346,
permutation p stratified by the Apr-Jun window = 0.494.

## Adjusted contrast, outcome log(1 + IR)

| Specification | Mechanism A coefficient (HC3 s.e.) | HC3 p | Wild cluster p | N | Min. detectable effect (log pts, 80% power) |
|---|---|---|---|---|---|
| Mechanism A only | 0.122 (0.104) | 0.240 | 0.359 | 110 | 0.29 |
| + Apr-Jun dummy | 0.056 (0.107) | 0.602 | 0.684 | 110 | 0.30 |
| + route (18A, 18C; A+H in controls) | -0.170 (0.177) | 0.336 | 0.582 | 110 | 0.49 |
| + route + size + fixed price | -0.177 (0.175) | 0.313 | 0.637 | 110 | 0.49 |

- Once route is held fixed the Mechanism A coefficient is identified from 6 non-18C issuers only, so its standard
  error is large. The sample cannot separate a mechanism effect from an 18C effect at any economically plausible size.
- Recommendation: fold Mechanism A vs B into the route/18C analysis as a descriptive note, or move it to a multi-year
  study. Do not present it as an independent 2026 hypothesis.
