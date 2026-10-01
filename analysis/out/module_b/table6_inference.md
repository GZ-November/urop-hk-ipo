# Table 6 — Inference with time clustering, baseline model (M3)

| Variable | Coefficient | HC3 p | Cluster-robust p, t(8) | Wild cluster bootstrap p (512 draws) |
|---|---|---|---|---|
| ln firm age | 0.110 | 0.563 | 0.245 | 0.637 |
| ln offer size | 0.017 | 0.797 | 0.743 | 0.746 |
| A+H issuer | -0.313 | 0.018 | 0.014 | 0.004 |
| VC/PE-backed | 0.088 | 0.577 | 0.548 | 0.770 |
| Top-tier sponsor | 0.051 | 0.612 | 0.552 | 0.555 |
| Cornerstone allocation | -0.353 | 0.368 | 0.222 | 0.270 |
| HSI return, prior 20 days | 2.055 | 0.033 | 0.001 | 0.020 |
| IPO count, prior 90 days | 0.004 | 0.806 | 0.726 | 0.734 |
| April-June hot window | 0.394 | 0.039 | 0.003 | 0.039 |

- Clusters: 9 listing months (01: 12, 02: 11, 03: 15, 04: 8, 05: 13, 06: 24, 07: 12, 08: 2, 09: 8 IPOs). With so few clusters, conventional cluster-robust p-values are unreliable; the wild cluster bootstrap is the recommended small-G test (Cameron, Gelbach & Miller 2008).
- Wild cluster bootstrap: restricted residuals, Rademacher weights per cluster, all 2^G sign patterns enumerated (exact, no simulation noise); a p-value cannot go below 2 / 2^G = 0.004.
- Cluster-robust and HC3 coefficients are identical (same OLS fit); only the standard errors differ.
