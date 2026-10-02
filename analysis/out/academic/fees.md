# Underwriting commission rates, 2026 (N = 104)

Outcome: disclosed underwriting commission on the HK offer, as a share of proceeds. The derived columns `Underwriting base commission rate`
and `Total underwriting fee rate` in the master are not used. Earlier source review found that these derived fields did not reliably follow
the disclosed commissions (see docs/archive/pre-raw-price-correction/ACADEMIC_EXTENSIONS_2026.md). The regression uses the disclosed HK commission.

## Distribution

| Commission rate | Deals | Share |
|---|---|---|
| 3.00% | 33 | 32% |
| 2.50% | 13 | 12% |
| 2.00% | 8 | 8% |
| 3.50% | 5 | 5% |
| 4.00% | 5 | 5% |
| 1.50% | 4 | 4% |
| 1.00% | 4 | 4% |
| 0.60% | 3 | 3% |

The most common single rate covers 32% of deals; unlike the U.S. 7% gross spread, no rate dominates.

## Determinants (OLS, one regression, 104 deals, R-squared 0.55)

| Regressor | Coefficient, pp of proceeds (HC3 s.e.) | HC3 p | Wild cluster p |
|---|---|---|---|
| ln offer size | -0.493*** (0.105) | 0.000 | 0.020 |
| April-June window | -0.029 (0.146) | 0.844 | 0.742 |
| A+H issuer | -0.524** (0.261) | 0.044 | 0.047 |
| VC/PE-backed | 0.238 (0.220) | 0.278 | 0.457 |
| Top-tier sponsor | 0.166 (0.162) | 0.307 | 0.484 |
| Cornerstone allocation | -0.155 (0.491) | 0.753 | 0.715 |
| Fixed-price offer | -0.102 (0.161) | 0.526 | 0.465 |

- A negative size coefficient is the usual scale economy: a doubling of the offer (ln 2 = 0.69) changes the commission rate by -0.34 percentage points.
- Wild cluster p uses listing months (exact enumeration); with few clusters treat both p-values as indicative.
