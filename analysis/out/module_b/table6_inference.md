# Table 6 — Inference with time clustering, baseline model (M3)

| Variable | Coefficient | HC3 p | Cluster-robust p, t(8) | Wild cluster bootstrap p (512 draws) |
|---|---|---|---|---|
| ln firm age | 0.098 | 0.614 | 0.326 | 0.652 |
| ln offer size | 0.010 | 0.871 | 0.827 | 0.848 |
| A+H issuer | -0.304 | 0.046 | 0.031 | 0.020 |
| VC/PE-backed | 0.096 | 0.519 | 0.521 | 0.578 |
| Top-tier sponsor | 0.049 | 0.620 | 0.555 | 0.559 |
| Cornerstone allocation | -0.294 | 0.448 | 0.240 | 0.266 |
| HSI return, prior 20 days | 1.736 | 0.073 | 0.000 | 0.020 |
| IPO count, prior 90 days | -0.000 | 0.996 | 0.994 | 0.992 |
| April-June hot window | 0.335 | 0.067 | 0.004 | 0.027 |

- Clusters: 9 listing months (01: 12, 02: 11, 03: 15, 04: 8, 05: 13, 06: 24, 07: 16, 08: 2, 09: 5 IPOs). With so few clusters, conventional cluster-robust p-values are unreliable; the wild cluster bootstrap is the recommended small-G test (Cameron, Gelbach & Miller 2008).
- Wild cluster bootstrap: restricted residuals, Rademacher weights per cluster, all 2^G sign patterns enumerated (exact, no simulation noise); a p-value cannot go below 2 / 2^G = 0.004.
- Cluster-robust and HC3 coefficients are identical (same OLS fit); only the standard errors differ.
