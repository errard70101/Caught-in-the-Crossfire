"""Monte Carlo validation utilities for Thread 3 PO draws.

Compares posterior summaries from

    * exact closed-form K^{-1} h  (mean) and dense K^{-1}  (variances),
    * direct CHOLMOD PO draws,
    * matrix-free PCG PO draws with the ``time_averaged_chol`` preconditioner.

Diagnostics implemented:

    * Sample posterior mean vs exact mean (||.||_inf, ||.||_2, and per-coord
      Monte Carlo standard error).
    * Selected marginal variances vs diag(K^{-1}) (only at small scale where
      a dense inverse is tractable).
    * Distribution of linear functionals c' y for chosen test vectors c
      (mean, variance, KS test between direct and PCG samples).
    * PCG iteration counts and relative residuals across draws.

The module is consumed by ``run_thread3.py`` which writes CSVs.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy import stats

from po_draws import (
    DirectPOContext, PCGPOContext, PCGPODrawResult,
    build_direct_context, build_pcg_context,
)
from dgp import DGP  # type: ignore


# ---------------------------------------------------------------------------
# Exact reference summaries
# ---------------------------------------------------------------------------


def exact_mean(ctx: DirectPOContext, h: np.ndarray) -> np.ndarray:
    """Return mu = K^{-1} h via the existing CHOLMOD factor."""
    return ctx.solve_mean(h)


def exact_dense_covariance(Kbar: sp.csc_matrix) -> np.ndarray:
    """Return dense K^{-1} (only call at small scale -- O(Tn^2) memory)."""
    Tn = Kbar.shape[0]
    return spla.spsolve(Kbar, sp.eye(Tn, format="csc")).toarray()


def exact_functional_var(Kbar: sp.csc_matrix, C: np.ndarray) -> np.ndarray:
    """Return Var(C y) = C K^{-1} C' computed *without* materialising K^{-1}.

    Each row c_i contributes Var(c_i y) = c_i^T K^{-1} c_i. We solve
    K x = c_i once per functional via CHOLMOD's factor on the CSC Kbar.
    Returns a (q,) vector of marginal functional variances.
    """
    from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore

    factor = cholmod_cholesky(Kbar)
    q = C.shape[0]
    out = np.empty(q)
    for i in range(q):
        x = factor(C[i])
        out[i] = float(C[i] @ x)
    return out


def exact_functional_cov(Kbar: sp.csc_matrix, C: np.ndarray) -> np.ndarray:
    """Return the full functional covariance Cov(C y) = C K^{-1} C'.

    For q functionals this is q CHOLMOD back-solves. Only call when q is small.
    """
    from sksparse.cholmod import cholesky as cholmod_cholesky  # type: ignore

    factor = cholmod_cholesky(Kbar)
    q, Tn = C.shape
    KinvCT = np.empty((Tn, q))
    for j in range(q):
        KinvCT[:, j] = factor(C[j])
    return C @ KinvCT


# ---------------------------------------------------------------------------
# Draw batches
# ---------------------------------------------------------------------------


@dataclass
class DrawBatchResult:
    """Stacked draws + per-draw diagnostics."""

    Y: np.ndarray  # (M, Tn) -- consider returning C @ y instead for large Tn
    solve_times: np.ndarray  # (M,)
    iters: Optional[np.ndarray] = None  # (M,)  only for PCG
    rel_residuals: Optional[np.ndarray] = None  # (M,)  only for PCG


def draw_direct_batch(
    ctx: DirectPOContext, h: np.ndarray, M: int, seed0: int,
    C: Optional[np.ndarray] = None,
) -> DrawBatchResult:
    """Generate M direct PO draws. If C is given, store C @ y instead of y."""
    Tn = ctx.dgp.Tn
    q = C.shape[0] if C is not None else Tn
    Y = np.empty((M, q))
    solve_times = np.empty(M)
    for m in range(M):
        rng = np.random.default_rng(seed0 + m)
        y, t = ctx.draw(h, rng)
        Y[m] = (C @ y) if C is not None else y
        solve_times[m] = t
    return DrawBatchResult(Y=Y, solve_times=solve_times)


def draw_pcg_batch(
    pctx: PCGPOContext, h: np.ndarray, M: int, seed0: int,
    C: Optional[np.ndarray] = None,
) -> DrawBatchResult:
    """Generate M matrix-free PCG PO draws."""
    Tn = pctx.dgp.Tn
    q = C.shape[0] if C is not None else Tn
    Y = np.empty((M, q))
    solve_times = np.empty(M)
    iters = np.empty(M, dtype=np.int64)
    rels = np.empty(M)
    for m in range(M):
        rng = np.random.default_rng(seed0 + m)
        res = pctx.draw(h, rng)
        Y[m] = (C @ res.y) if C is not None else res.y
        solve_times[m] = res.solve_time
        iters[m] = res.iters
        rels[m] = res.relative_residual
    return DrawBatchResult(Y=Y, solve_times=solve_times, iters=iters, rel_residuals=rels)


# ---------------------------------------------------------------------------
# Summary statistics
# ---------------------------------------------------------------------------


@dataclass
class MomentSummary:
    name: str
    M: int
    sample_mean_l2_err: float       # ||sample_mean - exact_mean||_2 / ||exact_mean||_2 (or ||exact||_2 if 0 use abs)
    sample_mean_linf_err: float
    sample_mean_mc_se: float        # expected ||error||_2 from MC theory: sqrt(sum diag(Sigma))/M)
    z_max_abs: float                # max_i |sample_mean_i - exact_i| / SE_i
    var_relative_rmse: Optional[float]  # for marginal variances
    extras: dict = field(default_factory=dict)


def summarise_mean_marginals(
    samples: np.ndarray, exact_mean: np.ndarray, exact_var: np.ndarray,
    label: str,
) -> MomentSummary:
    """Compare sample mean to ``exact_mean`` and sample variance to ``exact_var``.

    ``samples`` is (M, q); ``exact_mean`` and ``exact_var`` are (q,).
    """
    M = samples.shape[0]
    smean = samples.mean(axis=0)
    err = smean - exact_mean
    norm_exact = max(np.linalg.norm(exact_mean), 1e-300)
    l2_rel = float(np.linalg.norm(err) / norm_exact)
    linf = float(np.abs(err).max())
    # MC SE (theoretical): each coordinate has SE sqrt(var_i / M).
    se_coord = np.sqrt(np.maximum(exact_var, 0.0) / M)
    # Expected ||error||_2 = sqrt(sum se_coord^2) under exact Gaussianity.
    mc_se_total = float(np.sqrt(np.sum(se_coord ** 2)))
    z = np.abs(err) / np.maximum(se_coord, 1e-300)
    z_max = float(z.max())
    svar = samples.var(axis=0, ddof=1)
    var_rmse = float(np.sqrt(np.mean(((svar - exact_var) / np.maximum(exact_var, 1e-300)) ** 2)))
    return MomentSummary(
        name=label, M=M,
        sample_mean_l2_err=l2_rel,
        sample_mean_linf_err=linf,
        sample_mean_mc_se=mc_se_total,
        z_max_abs=z_max,
        var_relative_rmse=var_rmse,
    )


def two_sample_functional_tests(
    Yd: np.ndarray, Yp: np.ndarray, exact_mean_C: np.ndarray, exact_var_C: np.ndarray,
) -> dict:
    """Compare direct and PCG functional samples against each other and against exact.

    Inputs are (M, q). Returns per-functional t-test, KS, and ratio diagnostics.
    """
    q = Yd.shape[1]
    out: dict[str, list] = {
        "func_idx": list(range(q)),
        "exact_mean": exact_mean_C.tolist(),
        "exact_var": exact_var_C.tolist(),
        "direct_mean": [], "pcg_mean": [],
        "direct_var": [], "pcg_var": [],
        "direct_z": [], "pcg_z": [],
        "ks_stat": [], "ks_pvalue": [],
    }
    Md, Mp = Yd.shape[0], Yp.shape[0]
    for i in range(q):
        d, p = Yd[:, i], Yp[:, i]
        md, mp = d.mean(), p.mean()
        vd, vp = d.var(ddof=1), p.var(ddof=1)
        se_d = np.sqrt(max(exact_var_C[i], 0.0) / Md)
        se_p = np.sqrt(max(exact_var_C[i], 0.0) / Mp)
        out["direct_mean"].append(float(md))
        out["pcg_mean"].append(float(mp))
        out["direct_var"].append(float(vd))
        out["pcg_var"].append(float(vp))
        out["direct_z"].append(float((md - exact_mean_C[i]) / max(se_d, 1e-300)))
        out["pcg_z"].append(float((mp - exact_mean_C[i]) / max(se_p, 1e-300)))
        ks = stats.ks_2samp(d, p)
        out["ks_stat"].append(float(ks.statistic))
        out["ks_pvalue"].append(float(ks.pvalue))
    return out
