# Underwriting commission rates, 2026 (N = 101)

Outcome: disclosed underwriting commission on the HK offer, as a share of proceeds. The derived columns `Underwriting base commission rate`
and `Total underwriting fee rate` in the master are not used: the total equals 3.5% for 68 issuers and 1.00x% for the other 38 regardless of the disclosed
commission, so it does not follow from it (see docs/ACADEMIC_EXTENSIONS_2026.md).

## Distribution

| Commission rate | Deals | Share |
|---|---|---|
| 3.00% | 32 | 32% |
| 2.50% | 13 | 13% |
| 2.00% | 8 | 8% |
| 3.50% | 5 | 5% |
| 4.00% | 5 | 5% |
| 1.50% | 4 | 4% |
| 1.00% | 4 | 4% |
| 0.60% | 3 | 3% |

The most common single rate covers 32% of deals; unlike the U.S. 7% gross spread, no rate dominates.

## Determinants (OLS, one regression, 101 deals, R-squared 0.58)

| Regressor | Coefficient, pp of proceeds (HC3 s.e.) | HC3 p | Wild cluster p |
|---|---|---|---|
| ln offer size | -0.463*** (0.093) | 0.000 | 0.004 |
| April-June window | 0.031 (0.146) | 0.832 | 0.609 |
| A+H issuer | -0.675*** (0.232) | 0.004 | 0.023 |
| VC/PE-backed | 0.078 (0.209) | 0.709 | 0.793 |
| Top-tier sponsor | 0.189 (0.157) | 0.230 | 0.457 |
| Cornerstone allocation | -0.138 (0.478) | 0.772 | 0.758 |
| Fixed-price offer | -0.070 (0.159) | 0.659 | 0.629 |

- A negative size coefficient is the usual scale economy: a doubling of the offer (ln 2 = 0.69) changes the commission rate by -0.32 percentage points.
- Wild cluster p uses listing months (exact enumeration); with few clusters treat both p-values as indicative.
