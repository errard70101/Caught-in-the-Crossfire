"""Amortised cost benchmark.

    *** SUPERSEDED -- DO NOT USE FOR PRODUCTION COMPARISONS. ***

This benchmark models the per-MCMC-iteration cost as

    cost_explicit  = assemble_Kbar + iter_PCG * ex_matvec
    cost_matfree   =                 iter_PCG * mf_matvec

Both terms are wrong for the comparison that actually matters in Thread
2b / Thread 3:

  * The real explicit baseline is ``assemble + factor + back-solve``
    (direct CHOLMOD), not ``assemble + iter_PCG SpMVs``. A CHOLMOD
    back-solve takes one solve, not ``iter_PCG`` matvecs.
  * The hard-coded ``iter_PCG = 50`` is contradicted by Thread 2: actual
    PCG iteration counts range from ~7 at sv_sigma=0.1 to >1000 under
    high SV dispersion with lightweight preconditioning.

Thread 2b's fair-cost benchmark (see
``code/thread2b_fair_cost/THREAD2B_NOTE.md``) replaces this script with
phase-separated timings for direct_cholmod, direct_splu, and
pcg_time_avg_chol. The conclusion there is the opposite of what this
script suggests: direct CHOLMOD wins on total time at every Taiwan-scale
grid cell.

This file is retained only so older table references in
``THREAD1_NOTE.md`` (now flagged as superseded) continue to resolve.
"""

from __future__ import annotations

import time
from statistics import median

import numpy as np

from dgp import sample_dgp
from kbar_explicit import build_Kbar_explicit
from kbar_matfree import SVAwareKbar


def bench_amortised(n: int, T: int, p: int, *, seed: int = 0, n_reps: int = 7) -> dict:
    dgp = sample_dgp(n=n, T=T, p=p, seed=seed, sv_sigma=0.3, lam=1e4)
    op = SVAwareKbar(dgp)
    Tn = dgp.Tn
    rng = np.random.default_rng(seed + 100)
    x = rng.standard_normal(Tn)

    # warmup
    _ = op.matvec(x)

    # explicit assembly cost (median over reps)
    asm_times = []
    for _ in range(n_reps):
        t0 = time.perf_counter()
        Kbar = build_Kbar_explicit(dgp)
        asm_times.append(time.perf_counter() - t0)
    t_assemble = median(asm_times)

    _ = Kbar @ x  # warmup explicit matvec

    mf_times = []
    ex_times = []
    for _ in range(n_reps):
        t0 = time.perf_counter()
        _ = op.matvec(x)
        mf_times.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        _ = Kbar @ x
        ex_times.append(time.perf_counter() - t0)
    mf = median(mf_times)
    ex = median(ex_times)

    # break-even: t_assemble + k * ex = k * mf => k = t_assemble / (mf - ex) if mf > ex else inf
    if mf > ex:
        break_even = t_assemble / (mf - ex)
    else:
        break_even = float("inf")

    iter_pcg = 50
    cost_ex = t_assemble + iter_pcg * ex
    cost_mf = iter_pcg * mf

    return dict(
        n=n, T=T, p=p, Tn=Tn,
        assemble_s=t_assemble,
        mf_matvec_s=mf,
        ex_matvec_s=ex,
        break_even=break_even,
        cost_ex_50_s=cost_ex,
        cost_mf_50_s=cost_mf,
    )


def main() -> None:
    configs = [
        dict(n=3, T=120, p=2),
        dict(n=3, T=480, p=2),
        dict(n=3, T=1920, p=2),
        dict(n=5, T=120, p=2),
        dict(n=5, T=480, p=2),
        dict(n=5, T=1920, p=2),
        dict(n=5, T=480, p=6),
        dict(n=5, T=1920, p=6),
        dict(n=10, T=480, p=6),
        dict(n=10, T=1920, p=6),
    ]
    header = (
        f"{'n':>2} {'T':>5} {'p':>2} {'Tn':>6} "
        f"{'assemble_ms':>12} {'mf_us':>8} {'ex_us':>8} "
        f"{'break_even_k':>13} {'cost@50_mf_ms':>14} {'cost@50_ex_ms':>14}"
    )
    print(header)
    print("-" * len(header))
    for c in configs:
        r = bench_amortised(**c)
        print(f"{r['n']:>2} {r['T']:>5} {r['p']:>2} {r['Tn']:>6} "
              f"{r['assemble_s']*1e3:>12.2f} "
              f"{r['mf_matvec_s']*1e6:>8.1f} {r['ex_matvec_s']*1e6:>8.1f} "
              f"{r['break_even']:>13.1f} "
              f"{r['cost_mf_50_s']*1e3:>14.2f} {r['cost_ex_50_s']*1e3:>14.2f}")


if __name__ == "__main__":
    main()
