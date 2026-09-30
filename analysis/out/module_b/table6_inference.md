# Table 6 — Inference with time clustering, baseline model (M3)

| Variable | Coefficient | HC3 p | Cluster-robust p, t(8) | Wild cluster bootstrap p (512 draws) |
|---|---|---|---|---|
| ln firm age | 0.112 | 0.563 | 0.222 | 0.562 |
| ln offer size | -0.004 | 0.950 | 0.936 | 0.941 |
| A+H issuer | -0.298 | 0.054 | 0.027 | 0.020 |
| VC/PE-backed | 0.090 | 0.564 | 0.520 | 0.746 |
| Top-tier sponsor | 0.056 | 0.578 | 0.515 | 0.523 |
| Cornerstone allocation | -0.291 | 0.455 | 0.260 | 0.285 |
| HSI return, prior 20 days | 2.092 | 0.030 | 0.001 | 0.016 |
| IPO count, prior 90 days | 0.003 | 0.829 | 0.760 | 0.758 |
| April-June hot window | 0.381 | 0.052 | 0.004 | 0.062 |

- Clusters: 9 listing months (01: 12, 02: 11, 03: 15, 04: 8, 05: 13, 06: 24, 07: 12, 08: 2, 09: 5 IPOs). With so few clusters, conventional cluster-robust p-values are unreliable; the wild cluster bootstrap is the recommended small-G test (Cameron, Gelbach & Miller 2008).
- Wild cluster bootstrap: restricted residuals, Rademacher weights per cluster, all 2^G sign patterns enumerated (exact, no simulation noise); a p-value cannot go below 2 / 2^G = 0.004.
- Cluster-robust and HC3 coefficients are identical (same OLS fit); only the standard errors differ.
