"""Month-cluster covariance and restricted wild bootstrap inference.

The array interface enforces rank, residual degrees of freedom and group limits.
It neither selects study samples nor imports reporting or estimation scripts.
"""
from __future__ import annotations

import itertools
import numpy as np

def cr1_cov(X: np.ndarray, u: np.ndarray, g: np.ndarray) -> np.ndarray:
    """Cluster-robust covariance with the CR1 small-sample correction (as in Stata / statsmodels)."""
    n, k = X.shape
    ids = np.unique(g)
    if len(ids) < 2 or n <= k or np.linalg.matrix_rank(X) < k:
        raise ValueError("Cluster covariance needs full rank, residual degrees of freedom and at least two clusters")
    bread = np.linalg.inv(X.T @ X)
    meat = np.zeros((k, k))
    for c in ids:
        s = X[g == c].T @ u[g == c]
        meat += np.outer(s, s)
    return (len(ids) / (len(ids) - 1)) * ((n - 1) / (n - k)) * bread @ meat @ bread



def cluster_t(Y: np.ndarray, X: np.ndarray, g: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    beta = np.linalg.solve(X.T @ X, X.T @ Y)
    u = Y - X @ beta
    return beta, beta / np.sqrt(np.diag(cr1_cov(X, u, g)))



def wild_cluster_p(Y: np.ndarray, X: np.ndarray, g: np.ndarray, j: int) -> float:
    """Restricted wild cluster bootstrap-t p-value for H0: beta_j = 0.

    Rademacher weights, one per cluster, enumerated exactly (2^G draws)."""
    _, t_obs = cluster_t(Y, X, g)
    keep = [c for c in range(X.shape[1]) if c != j]
    Xr = X[:, keep]
    br = np.linalg.solve(Xr.T @ Xr, Xr.T @ Y)
    fit_r, u_r = Xr @ br, Y - Xr @ br
    ids = np.unique(g)
    if len(ids) > 16:
        raise ValueError("Exact wild bootstrap supports at most 16 clusters; use a simulated method for larger samples")
    idx = np.searchsorted(ids, g)
    t_star = []
    for w in itertools.product((-1.0, 1.0), repeat=len(ids)):
        y_star = fit_r + np.array(w)[idx] * u_r
        t_star.append(cluster_t(y_star, X, g)[1][j])
    return float(np.mean(np.abs(t_star) >= abs(t_obs[j]) - 1e-12))
