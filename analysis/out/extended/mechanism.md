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

Mean IR 69.5% (A, n = 23) vs 48.4% (B, n = 80); median
44.7% vs 14.1%. Welch p = 0.311, Mann-Whitney p = 0.230,
permutation p stratified by the Apr-Jun window = 0.369.

## Adjusted contrast, outcome log(1 + IR)

| Specification | Mechanism A coefficient (HC3 s.e.) | HC3 p | Wild cluster p | N | Min. detectable effect (log pts, 80% power) |
|---|---|---|---|---|---|
| Mechanism A only | 0.156 (0.108) | 0.148 | 0.312 | 103 | 0.30 |
| + Apr-Jun dummy | 0.082 (0.115) | 0.477 | 0.598 | 103 | 0.32 |
| + route (18A, 18C; A+H in controls) | -0.162 (0.176) | 0.358 | 0.668 | 103 | 0.49 |
| + route + size + fixed price | -0.168 (0.173) | 0.330 | 0.629 | 103 | 0.48 |

- Once route is held fixed the Mechanism A coefficient is identified from 6 non-18C issuers only, so its standard
  error is large. The sample cannot separate a mechanism effect from an 18C effect at any economically plausible size.
- Recommendation: fold Mechanism A vs B into the route/18C analysis as a descriptive note, or move it to a multi-year
  study. Do not present it as an independent 2026 hypothesis.
