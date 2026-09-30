# Underwriting commission rates, 2026 (N = 105)

Outcome: disclosed underwriting commission on the HK offer, as a share of proceeds. The derived columns `Underwriting base commission rate`
and `Total underwriting fee rate` in the master are not used: the total equals 3.5% for 68 issuers and 1.00x% for the other 38 regardless of the disclosed
commission, so it does not follow from it (see docs/ACADEMIC_EXTENSIONS_2026.md).

## Distribution

| Commission rate | Deals | Share |
|---|---|---|
| 3.00% | 32 | 30% |
| 2.50% | 13 | 12% |
| 2.00% | 8 | 8% |
| 3.50% | 5 | 5% |
| 4.00% | 5 | 5% |
| 1.50% | 4 | 4% |
| 1.00% | 4 | 4% |
| 0.60% | 3 | 3% |

The most common single rate covers 30% of deals; unlike the U.S. 7% gross spread, no rate dominates.

## Determinants (OLS, one regression, 105 deals, R-squared 0.61)

| Regressor | Coefficient, pp of proceeds (HC3 s.e.) | HC3 p | Wild cluster p |
|---|---|---|---|
| ln offer size | -0.465*** (0.092) | 0.000 | 0.004 |
| April-June window | 0.043 (0.143) | 0.761 | 0.555 |
| A+H issuer | -0.684*** (0.228) | 0.003 | 0.020 |
| VC/PE-backed | 0.125 (0.195) | 0.520 | 0.648 |
| Top-tier sponsor | 0.189 (0.152) | 0.215 | 0.445 |
| Cornerstone allocation | -0.155 (0.470) | 0.742 | 0.707 |
| Fixed-price offer | -0.073 (0.156) | 0.637 | 0.598 |

- A negative size coefficient is the usual scale economy: a doubling of the offer (ln 2 = 0.69) changes the commission rate by -0.32 percentage points.
- Wild cluster p uses listing months (exact enumeration); with few clusters treat both p-values as indicative.
