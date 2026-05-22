"""Runtime and memory benchmark for the SV-aware Kbar matvec.

Sweeps T and reports:
    - Tn (problem dimension)
    - explicit Kbar nnz and rough memory footprint
    - matrix-free per-matvec wallclock (median of n_reps)
    - explicit per-matvec wallclock (median of n_reps)
    - assembly time of the explicit Kbar (one-shot)

This is *not* yet a PCG benchmark -- that belongs to Thread 2. The purpose
here is to characterise the matvec primitive itself.
"""

from __future__ import annotations

import time
from statistics import median

import numpy as np

from dgp import sample_dgp
from kbar_explicit import build_Kbar_explicit
from kbar_matfree import SVAwareKbar


def bench_one(n: int, T: int, p: int, *, seed: int = 0, n_reps: int = 11) -> dict:
    dgp = sample_dgp(n=n, T=T, p=p, seed=seed, sv_sigma=0.3, lam=1e4)
    op = SVAwareKbar(dgp)
    Tn = dgp.Tn

    # explicit assembly (one-shot, separate from per-matvec cost)
    t0 = time.perf_counter()
    Kbar = build_Kbar_explicit(dgp)
    t_assemble = time.perf_counter() - t0

    # Validate symmetry and positive-definiteness for all scales
    from kbar_explicit import assert_spd_small
    assert_spd_small(Kbar)

    rng = np.random.default_rng(seed + 100)
    x = rng.standard_normal(Tn)

    # warmup
    _ = op.matvec(x)
    _ = Kbar @ x

    mf_times = []
    ex_times = []
    for _ in range(n_reps):
        t0 = time.perf_counter()
        _ = op.matvec(x)
        mf_times.append(time.perf_counter() - t0)
        t0 = time.perf_counter()
        _ = Kbar @ x
        ex_times.append(time.perf_counter() - t0)

    # Memory accounting (rough): CSR stores nnz floats (8B) + nnz int32 (4B)
    # col + (rows+1) int32 indptr. H_B nnz is O(T n^2 p), Kbar nnz is
    # roughly 2x H_B nnz. The matrix-free op only stores H_B (transpose
    # is a free CSC view), so mf_mem counts H_B once plus M_m + M_m.T.
    H_B_nnz = op.H_B.nnz
    M_m_nnz = op.M_m.nnz
    explicit_nnz = Kbar.nnz
    ex_mem = explicit_nnz * 12 + (Tn + 1) * 4
    mf_mem = H_B_nnz * 12 + (Tn + 1) * 4 + M_m_nnz * 24 + Tn * 8  # M_m + M_m.T cached
    return dict(
        n=n, T=T, p=p, Tn=Tn,
        t_assemble=t_assemble,
        mf_median_s=median(mf_times),
        ex_median_s=median(ex_times),
        H_B_nnz=H_B_nnz,
        explicit_nnz=explicit_nnz,
        mf_mem_bytes=mf_mem,
        ex_mem_bytes=ex_mem,
    )


def main() -> None:
    configs = []
    for n in (3, 5):
        for T in (30, 60, 120, 240, 480, 960):
            configs.append(dict(n=n, T=T, p=2))
    for n in (5,):
        for T in (60, 120, 240):
            configs.append(dict(n=n, T=T, p=6))

    print(f"{'n':>2} {'T':>5} {'p':>2} {'Tn':>6} "
          f"{'mf_ms':>10} {'ex_ms':>10} {'speedup':>8} "
          f"{'H_B_nnz':>10} {'K_nnz':>10} {'mf_MB':>8} {'ex_MB':>8} "
          f"{'assemble_ms':>12}")
    print("-" * 110)
    for c in configs:
        r = bench_one(**c)
        speedup = r["ex_median_s"] / r["mf_median_s"] if r["mf_median_s"] > 0 else float("nan")
        print(f"{r['n']:>2} {r['T']:>5} {r['p']:>2} {r['Tn']:>6} "
              f"{r['mf_median_s']*1e3:>10.3f} {r['ex_median_s']*1e3:>10.3f} {speedup:>8.2f} "
              f"{r['H_B_nnz']:>10} {r['explicit_nnz']:>10} "
              f"{r['mf_mem_bytes']/1e6:>8.2f} {r['ex_mem_bytes']/1e6:>8.2f} "
              f"{r['t_assemble']*1e3:>12.2f}")


if __name__ == "__main__":
    main()
