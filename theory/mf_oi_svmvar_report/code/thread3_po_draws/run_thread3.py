"""Driver for Thread 3 perturbation-optimisation validation.

Produces three CSVs and a console summary:

    * ``po_moments.csv``     -- sample-mean / variance summaries per
                                (scale, sv_sigma, sampler).
    * ``po_functionals.csv`` -- per-functional comparison of direct vs PCG.
    * ``pcg_tolerance.csv``  -- iter counts / residuals across
                                rtol in {1e-6, 1e-8, 1e-10}.

The small-scale block exercises dense diag(K^{-1}) since Tn is small. The
Taiwan-scale block uses only the CHOLMOD factor's back-solve and selected
functionals so it stays tractable.
"""

from __future__ import annotations

import csv
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Optional

import numpy as np

_THIS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(_THIS_DIR))
sys.path.insert(0, str(_THIS_DIR.parent / "thread1_matvec"))
sys.path.insert(0, str(_THIS_DIR.parent / "thread2_pcg"))

from dgp import sample_dgp  # type: ignore
from po_draws import build_direct_context, build_pcg_context
from validation import (
    draw_direct_batch, draw_pcg_batch,
    exact_dense_covariance, exact_functional_cov,
    summarise_mean_marginals, two_sample_functional_tests,
)


# ---------------------------------------------------------------------------
# Scale configurations
# ---------------------------------------------------------------------------


@dataclass
class ScaleSpec:
    label: str
    n: int
    T: int
    p: int
    M: int                # Monte Carlo draws
    use_dense_inverse: bool
    n_functionals: int


SMALL = ScaleSpec(
    label="small", n=3, T=40, p=2,
    M=2000, use_dense_inverse=True, n_functionals=4,
)
TAIWAN = ScaleSpec(
    label="taiwan", n=5, T=480, p=2,
    M=400, use_dense_inverse=False, n_functionals=6,
)

SV_SIGMAS = (0.1, 0.3)
TOLERANCES = (1e-6, 1e-8, 1e-10)
DGP_SEED = 42
NOISE_SEED0_DIRECT = 100_000
NOISE_SEED0_PCG = 200_000


def _make_functionals(Tn: int, n: int, n_func: int, rng: np.random.Generator) -> np.ndarray:
    """Build a small bank of test functionals c'y.

    Mix of structured functionals (sum across time for a chosen variable,
    average across all coordinates) and random unit-norm directions, so the
    KS comparison sees both smooth/global and stochastic directions.
    """
    rows = []
    T = Tn // n
    # functional 0: time-sum of variable 0  --  c[t*n + 0] = 1
    c0 = np.zeros(Tn); c0[0::n] = 1.0; rows.append(c0)
    # functional 1: all-ones / sqrt(Tn) (global mean direction)
    c1 = np.ones(Tn) / np.sqrt(Tn); rows.append(c1)
    # functional 2: difference of last and first variable-0 entry
    c2 = np.zeros(Tn); c2[0] = 1.0; c2[(T - 1) * n] = -1.0; rows.append(c2)
    # remaining: random Gaussian directions, normalised
    while len(rows) < n_func:
        v = rng.standard_normal(Tn)
        v /= np.linalg.norm(v)
        rows.append(v)
    return np.vstack(rows[:n_func])


# ---------------------------------------------------------------------------
# Per-cell runner
# ---------------------------------------------------------------------------


def run_cell(
    scale: ScaleSpec, sv_sigma: float, *, rtol: float = 1e-8,
    verbose: bool = True,
) -> dict:
    """Run direct + PCG draws and assemble all summaries for one cell."""
    t_cell0 = time.perf_counter()
    dgp = sample_dgp(
        n=scale.n, T=scale.T, p=scale.p, seed=DGP_SEED,
        sv_sigma=sv_sigma, sv_rho=0.95, lam=1e4, target_radius=0.9,
        lf_indices=[0],
    )
    Tn = dgp.Tn
    rng_h = np.random.default_rng(7)
    n_L = dgp.M_m.shape[0]
    y_L = rng_h.standard_normal(n_L)
    h = dgp.lam * (dgp.M_m.T @ y_L)

    # Functionals.
    rng_C = np.random.default_rng(11)
    C = _make_functionals(Tn, scale.n, scale.n_functionals, rng_C)

    if verbose:
        print(f"\n=== cell scale={scale.label}  sv_sigma={sv_sigma}  rtol={rtol:.0e} ===")
        print(f"  Tn={Tn}, n_L={n_L}, M={scale.M}, q_func={C.shape[0]}")

    # Direct CHOLMOD context (production reference).
    t0 = time.perf_counter()
    dctx = build_direct_context(dgp)
    t_direct_setup = time.perf_counter() - t0
    mu = dctx.solve_mean(h)

    # Exact variances if feasible.
    exact_var = None
    if scale.use_dense_inverse:
        Kinv = exact_dense_covariance(dctx.Kbar)
        exact_var = np.diag(Kinv).copy()

    # Functional covariance: use back-solves (cheap if q small).
    func_cov = exact_functional_cov(dctx.Kbar, C)
    func_mean = C @ mu
    func_var = np.diag(func_cov)

    # Direct draw batch.
    Yd = draw_direct_batch(dctx, h, scale.M, NOISE_SEED0_DIRECT, C=C)
    Yd_full = None
    if scale.use_dense_inverse:
        Yd_full = draw_direct_batch(dctx, h, scale.M, NOISE_SEED0_DIRECT, C=None)

    # PCG context for this rtol.
    pctx = build_pcg_context(dgp, rtol=rtol)
    Yp = draw_pcg_batch(pctx, h, scale.M, NOISE_SEED0_PCG, C=C)
    Yp_full = None
    if scale.use_dense_inverse:
        Yp_full = draw_pcg_batch(pctx, h, scale.M, NOISE_SEED0_PCG, C=None)

    summaries: list[dict] = []
    if Yd_full is not None:
        sd = summarise_mean_marginals(Yd_full.Y, mu, exact_var, label="direct")
        sp_ = summarise_mean_marginals(Yp_full.Y, mu, exact_var, label="pcg")
        for s in (sd, sp_):
            row = asdict(s)
            row.update(dict(scale=scale.label, sv_sigma=sv_sigma, rtol=rtol))
            summaries.append(row)

    func_tests = two_sample_functional_tests(Yd.Y, Yp.Y, func_mean, func_var)
    # Annotate.
    n_q = len(func_tests["func_idx"])
    func_tests["scale"] = [scale.label] * n_q
    func_tests["sv_sigma"] = [sv_sigma] * n_q
    func_tests["rtol"] = [rtol] * n_q

    pcg_stats = dict(
        scale=scale.label, sv_sigma=sv_sigma, rtol=rtol,
        iters_mean=float(np.mean(Yp.iters)),
        iters_median=float(np.median(Yp.iters)),
        iters_max=int(np.max(Yp.iters)),
        rel_residual_mean=float(np.mean(Yp.rel_residuals)),
        rel_residual_max=float(np.max(Yp.rel_residuals)),
        direct_solve_ms_mean=float(np.mean(Yd.solve_times) * 1000),
        pcg_solve_ms_mean=float(np.mean(Yp.solve_times) * 1000),
        direct_setup_s=float(t_direct_setup),
        pcg_setup_precond_s=float(pctx.setup_time_precond),
        Tn=Tn,
    )
    if verbose:
        print(
            f"  direct setup={t_direct_setup*1e3:.1f} ms (assembly={dctx.setup_time_assembly*1e3:.1f}, "
            f"factor={dctx.setup_time_factor*1e3:.1f})"
        )
        print(
            f"  pcg precond setup={pctx.setup_time_precond*1e3:.1f} ms, "
            f"iters mean={pcg_stats['iters_mean']:.1f} (max={pcg_stats['iters_max']}), "
            f"rel_res_max={pcg_stats['rel_residual_max']:.2e}"
        )
        if summaries:
            for row in summaries:
                print(
                    f"  {row['name']:6s}  ||mean_err||_2/||mu||={row['sample_mean_l2_err']:.2e}  "
                    f"z_max={row['z_max_abs']:.2f}  var_rmse={row['var_relative_rmse']:.2e}"
                )
        print(
            f"  functional KS p-values: {[f'{p:.2f}' for p in func_tests['ks_pvalue']]}"
        )
        print(f"  cell wallclock: {time.perf_counter() - t_cell0:.1f} s")

    return dict(
        moments=summaries,
        functionals=func_tests,
        pcg_stats=pcg_stats,
    )


# ---------------------------------------------------------------------------
# Drivers
# ---------------------------------------------------------------------------


def _write_csv(path: Path, rows: list[dict], fieldnames: Optional[list[str]] = None) -> None:
    if not rows:
        return
    if fieldnames is None:
        fieldnames = list(rows[0].keys())
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)


def main(quick: bool = False) -> None:
    out_dir = _THIS_DIR
    moments_rows: list[dict] = []
    functional_rows: list[dict] = []
    pcg_rows: list[dict] = []

    scales = [SMALL]
    if not quick:
        scales.append(TAIWAN)

    # Block 1: direct vs PCG validation at the canonical rtol=1e-8 across scales/sv.
    for scale in scales:
        for sv in SV_SIGMAS:
            res = run_cell(scale, sv, rtol=1e-8)
            moments_rows.extend(res["moments"])
            ft = res["functionals"]
            n = len(ft["func_idx"])
            for i in range(n):
                functional_rows.append(
                    {k: (ft[k][i] if isinstance(ft[k], list) else ft[k]) for k in ft}
                )
            pcg_rows.append(res["pcg_stats"])

    # Block 2: tolerance sensitivity at small scale, sv=0.3 (where iter count is highest).
    for rtol in TOLERANCES:
        if rtol == 1e-8:
            continue  # already covered above
        res = run_cell(SMALL, 0.3, rtol=rtol)
        moments_rows.extend(res["moments"])
        ft = res["functionals"]
        n = len(ft["func_idx"])
        for i in range(n):
            functional_rows.append(
                {k: (ft[k][i] if isinstance(ft[k], list) else ft[k]) for k in ft}
            )
        pcg_rows.append(res["pcg_stats"])

    # Block 3: Taiwan-scale tolerance sweep (only feasible cells).
    if not quick:
        for rtol in TOLERANCES:
            if rtol == 1e-8:
                continue
            res = run_cell(TAIWAN, 0.3, rtol=rtol)
            ft = res["functionals"]
            n = len(ft["func_idx"])
            for i in range(n):
                functional_rows.append(
                    {k: (ft[k][i] if isinstance(ft[k], list) else ft[k]) for k in ft}
                )
            pcg_rows.append(res["pcg_stats"])

    _write_csv(out_dir / "po_moments.csv", moments_rows)
    _write_csv(out_dir / "po_functionals.csv", functional_rows)
    _write_csv(out_dir / "pcg_tolerance.csv", pcg_rows)
    print(f"\nwrote: {out_dir / 'po_moments.csv'}")
    print(f"wrote: {out_dir / 'po_functionals.csv'}")
    print(f"wrote: {out_dir / 'pcg_tolerance.csv'}")


if __name__ == "__main__":
    quick = "--quick" in sys.argv
    main(quick=quick)
