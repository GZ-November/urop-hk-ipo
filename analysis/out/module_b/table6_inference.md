# Table 6 — Inference with time clustering, baseline model (M3)

| Variable | Coefficient | HC3 p | Cluster-robust p, t(8) | Wild cluster bootstrap p (512 draws) |
|---|---|---|---|---|
| ln firm age | 0.096 | 0.624 | 0.320 | 0.633 |
| ln offer size | 0.002 | 0.980 | 0.972 | 1.000 |
| A+H issuer | -0.309 | 0.046 | 0.030 | 0.020 |
| VC/PE-backed | 0.145 | 0.383 | 0.273 | 0.414 |
| Top-tier sponsor | 0.058 | 0.568 | 0.491 | 0.520 |
| Cornerstone allocation | -0.323 | 0.406 | 0.202 | 0.258 |
| HSI return, prior 20 days | 1.894 | 0.054 | 0.001 | 0.016 |
| IPO count, prior 90 days | 0.005 | 0.722 | 0.580 | 0.559 |
| April-June hot window | 0.403 | 0.041 | 0.003 | 0.047 |

- Clusters: 9 listing months (01: 12, 02: 11, 03: 15, 04: 8, 05: 13, 06: 24, 07: 12, 08: 2, 09: 5 IPOs). With so few clusters, conventional cluster-robust p-values are unreliable; the wild cluster bootstrap is the recommended small-G test (Cameron, Gelbach & Miller 2008).
- Wild cluster bootstrap: restricted residuals, Rademacher weights per cluster, all 2^G sign patterns enumerated (exact, no simulation noise); a p-value cannot go below 2 / 2^G = 0.004.
- Cluster-robust and HC3 coefficients are identical (same OLS fit); only the standard errors differ.
