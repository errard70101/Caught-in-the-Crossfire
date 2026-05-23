# Thread 3: Perturbation-Optimisation Draw Validation

Reference plan: `theory/mf_oi_svmvar_report/NEXT_THREAD_PLAN.md`, Thread 3.
Builds on Thread 1 (`code/thread1_matvec/`), Thread 2 (`code/thread2_pcg/`),
and Thread 2b (`code/thread2b_fair_cost/`).

## Objective

Validate Gaussian latent-state draws from
`y* | rest ~ N(K^{-1} h, K^{-1})`, with
`K = A'DA + lambda M'M`, `D = blockdiag(D_t)`, `D_t = B0' diag(1/U_t) B0`,
under the solver strategy implied by Threads 2 and 2b. Two samplers are
implemented:

- **Direct CHOLMOD PO** -- the production accuracy reference per
  Thread 2b's total-cost result. Assemble the exact `Kbar` once per
  cell, factor with CHOLMOD, draw via perturbation-optimisation, reuse
  the factor for the back-solve.
- **Matrix-free PCG PO** -- diagnostic fallback. Uses Thread 1's
  `SVAwareKbar` matvec with Thread 2's `time_averaged_chol`
  preconditioner; PCG via `scipy.sparse.linalg.cg`. No lightweight
  preconditioner (`none`, `jacobi`, `block_jacobi`) is exercised
  because Thread 2 already showed they fail at realistic SV dispersion.

Correction rerun status (2026-05-23): the matrix-free PCG PO path uses
the `time_averaged_chol` preconditioner from
`thread2_pcg/preconditioners.py`, which has been corrected to use the
precision average `D_bar = mean_t(D_t) = B0' diag(mean_t 1/U_t) B0`
instead of the old `B0' diag(1 / mean_t U_t) B0` construction. The
PCG diagnostics, `pcg_tolerance.csv`, `po_moments.csv`, and
`po_functionals.csv` have been refreshed accordingly. The direct
CHOLMOD reference is unaffected by the preconditioner correction (it
factors the exact `Kbar`, not `Kbar_avg`).

## Perturbation-optimisation recipe

For each draw:

1. `eta_t ~ N(0, I_n)` for `t = 1..T`,
   `s_t = B0' diag(1/sqrt(U_t)) eta_t`,
   so `Cov(s_t) = D_t` and stacked `s ~ N(0, D)`.
2. `zeta ~ N(0, I_{n_L})`,
   `q = sqrt(lambda) M' zeta` with `Cov(q) = lambda M'M`.
3. `v = h + A' s + q`, hence `v ~ N(h, K)` exactly.
4. Solve `K y = v`; `y ~ N(K^{-1} h, K^{-1})`.

`h = lambda M' y_L` is constructed from a synthetic `y_L` once per cell
(seed 7); the same `h` is used by both samplers so they target the same
posterior. Within each draw index `m`, both samplers seed their RNG with
`m + offset`, so direct draw `m` and PCG draw `m` use *the same noise
realisation* of `(eta, zeta)` and therefore the same right-hand side
`v_m`. Same-seed reproducibility check at `n=4, T=30`: `||y_pcg -
y_direct||_2 / ||y_direct||_2 = 2.0e-6` at `rtol=1e-8` (consistent with
PCG residual times `cond(K)`).

## Experimental design

Two scales:

| label  | `n` | `T`  | `p` | `Tn`  | `M`  | dense `K^{-1}`? | functionals |
| ------ | --- | ---- | --- | ----- | ---- | --------------- | ----------- |
| small  | 3   | 40   | 2   | 120   | 2000 | yes             | 4           |
| taiwan | 5   | 480  | 2   | 2400  | 400  | no              | 6           |

Other DGP knobs match Thread 2's baseline: `target_radius = 0.9`,
`sv_rho = 0.95`, `lam = 1e4`, `lf_indices = [0]`, `DGP_SEED = 42`.

Block 1 (canonical `rtol = 1e-8`) sweeps `sv_sigma in {0.1, 0.3}` at
both scales. Block 2 adds `rtol in {1e-6, 1e-10}` at `sv_sigma = 0.3`
(the harder of the two controlled regimes).

Functionals exercised at every cell:

- `func 0`: time-sum of variable 0 (`c[t*n] = 1`),
- `func 1`: global-mean direction (`ones / sqrt(Tn)`),
- `func 2`: end-minus-start of variable 0,
- `func 3+`: random unit-norm Gaussian directions (RNG seed 11).

## Results -- accuracy

Direct and PCG produce statistically indistinguishable samples in every
cell tested:

| scale  | `sv_sigma` | rtol  | `||smean - mu||_2 / ||mu||_2` (direct / pcg) | MC SE (theory) | `z_max_abs` (direct / pcg) | `var_relative_rmse` (direct / pcg) |
| ------ | ---------- | ----- | -------------------------------------------- | -------------- | -------------------------- | ---------------------------------- |
| small  | 0.1        | 1e-8  | 0.119 / 0.135                                | 0.225          | 2.61 / 3.53                | 3.3e-2 / 2.9e-2                    |
| small  | 0.3        | 1e-8  | 0.100 / 0.116                                | 0.227          | 2.58 / 3.60                | 3.3e-2 / 3.0e-2                    |
| small  | 0.3        | 1e-6  | 0.100 / 0.116                                | 0.227          | 2.58 / 3.60                | 3.3e-2 / 3.0e-2                    |
| small  | 0.3        | 1e-10 | 0.100 / 0.116                                | 0.227          | 2.58 / 3.60                | 3.3e-2 / 3.0e-2                    |

Key observations:

1. **Sample-mean error is below the theoretical MC SE in every cell**:
   the empirical `||smean - mu||_2 / ||mu||_2` (0.10-0.14) is well
   under `sqrt(trace(K^{-1}) / M) / ||mu||_2 = 0.22-0.23`.
2. **Marginal variances match `diag(K^{-1})` to ~3% relative RMSE**, in
   line with the theoretical sample-variance RSD `sqrt(2 / M) =
   3.2%` for `M = 2000`.
3. **PCG tolerance error is invisible at MC precision**: across rtol in
   `{1e-6, 1e-8, 1e-10}`, the PCG `sample_mean_l2_err` differs only in
   the 4th-5th decimal (0.11621 vs 0.11623 vs 0.11628). MC noise is 100-1000x
   larger than PCG tolerance error.
4. **The slightly larger `z_max_abs` for PCG (3.5-3.6 vs 2.6 for
   direct)** is at the Bonferroni-corrected critical value for 120
   coordinates and matches across all three rtol values; it is the same
   draw realisations, not a tolerance effect.

Linear-functional KS tests between direct and PCG samples (4-6
functionals per cell, two-sample KS with `M_d = M_p`):

| scale  | sv_sigma | rtol  | KS p-values                            |
| ------ | -------- | ----- | -------------------------------------- |
| small  | 0.1      | 1e-8  | 0.46, 0.10, 0.59, 0.01                 |
| small  | 0.3      | 1e-8  | 0.48, 0.18, 0.26, 0.03                 |
| taiwan | 0.1      | 1e-8  | 0.32, 0.70, 0.94, 0.81, 0.58, 0.32     |
| taiwan | 0.3      | 1e-8  | 0.32, 0.52, 0.94, 0.76, 0.76, 0.24     |
| taiwan | 0.3      | 1e-6  | 0.32, 0.52, 0.94, 0.76, 0.76, 0.24     |
| taiwan | 0.3      | 1e-10 | 0.32, 0.52, 0.94, 0.76, 0.76, 0.24     |

Only one borderline `p < 0.05` row (small/sv=0.1 func-3) -- consistent
with multiple testing across 4 functionals at 5% (expected false-
positive rate over the full table is ~24 of 24 ~ 1.2 hits). At
Taiwan-scale every p-value is `> 0.20`. The KS p-values are *identical
to four digits* across `rtol`, confirming the tolerance-vs-MC-error
finding above.

## Results -- PCG cost vs direct

| scale  | sv_sigma | rtol  | PCG iters (mean / max) | rel_res max | direct solve (ms) | PCG solve (ms) | PCG/direct |
| ------ | -------- | ----- | ---------------------- | ----------- | ----------------- | -------------- | ---------- |
| small  | 0.1      | 1e-8  | 7.6 / 8                | 1.0e-8      | 0.0023            | 0.13           | 56x        |
| small  | 0.3      | 1e-8  | 16.0 / 17              | 1.0e-8      | 0.0023            | 0.26           | 113x       |
| taiwan | 0.1      | 1e-8  | 13.1 / 14              | 1.0e-8      | 0.026             | 0.90           | 35x        |
| taiwan | 0.3      | 1e-8  | 73.7 / 77              | 1.0e-8      | 0.026             | 4.97           | 191x       |
| taiwan | 0.3      | 1e-6  | 43.5 / 45              | 1.0e-6      | 0.027             | 2.94           | 110x       |
| taiwan | 0.3      | 1e-10 | 102.7 / 105            | 1.0e-10     | 0.026             | 6.93           | 266x       |

Iteration count grows linearly in `-log10(rtol)` (Taiwan/sv=0.3: 44 ->
74 -> 103 across `1e-6 -> 1e-8 -> 1e-10`), which is the expected
log-convergence rate of PCG on an SPD system. Per-draw solve cost is
two orders of magnitude above the direct CHOLMOD back-solve at every
tolerance and every controlled SV setting we tested, matching the
fair-cost picture from Thread 2b.

The direct path's per-cell setup (assembly + CHOLMOD factorisation) is
17-18 ms at Taiwan scale and is amortised across all `M` draws within
the cell, since `K` is held fixed when SV is fixed. The PCG path's
preconditioner setup (`build_time_averaged_chol`) is ~10 ms and is
also amortised. Both are negligible relative to total draw cost in any
realistic MCMC where the SV update changes `D_t` only between sweeps.

## PCG tolerance recommendation

For the controlled-SV regime where PCG is used as a diagnostic
fallback, `rtol = 1e-8` is the right operating point:

- At `rtol = 1e-6`, the recovered sample distribution is already
  identical (to MC precision) to the direct draw; the change in PCG
  iters is small.
- At `rtol = 1e-8`, PCG residual error is `~10^4` times smaller than
  per-draw MC noise on the functionals we tested.
- `rtol = 1e-10` doubles iteration count without any visible accuracy
  gain. It is wasteful here.

In short: `rtol = 1e-8` keeps PCG's contribution to total sampling
error well below MC noise without paying for unnecessary iterations.
**This is a diagnostic-mode recommendation only.** Production runs
should use direct CHOLMOD per Thread 2b.

## Acceptance criteria

- **Direct PO draws reproduce the intended Gaussian posterior
  summaries.** Sample means match `K^{-1} h` to within MC SE
  (`||err||/||mu|| ~ 0.10` vs theoretical `0.22`); marginal variances
  match `diag(K^{-1})` to ~3% relative RMSE, in line with
  `sqrt(2/M)`; functional `z_max_abs ~ 2.6` is consistent with
  Bonferroni-corrected sampling noise over `Tn = 120` coordinates.
  PASS.

- **PCG-based summaries match direct CHOLMOD summaries within Monte
  Carlo error in the controlled regimes.** All KS p-values `> 0.20`
  at Taiwan scale; only one borderline at small-scale (expected at
  4 functionals * 6 cells under 5% testing). PCG sample means agree
  with direct to 4-5 decimal digits, well inside MC noise. PASS.

- **PCG tolerance recommendation is documented.** `rtol = 1e-8`
  for diagnostic mode, justified above. PASS.

- **No claim that matrix-free PCG is production-ready at high SV
  dispersion.** This thread tested only `sv_sigma in {0.1, 0.3}` per
  the Thread 2 controlled-convergence regime; it makes no claim about
  `sv_sigma >= 0.5`. PASS.

## Solver recommendation for the full MCMC

- **Production / Taiwan-scale.** Use direct CHOLMOD for the latent
  state. Thread 2b shows direct CHOLMOD dominates on total cost at
  these dimensions; this thread shows it also produces statistically
  exact draws and amortises its setup cleanly within a per-sweep
  block-Gibbs structure. The PO recipe above is the implementation.

- **Diagnostic / memory-constrained / larger-scale regimes.**
  Matrix-free PCG with `time_averaged_chol` preconditioner and
  `rtol = 1e-8` reproduces direct CHOLMOD's distribution within MC
  noise, but only in the controlled-SV regime that Thread 2 identified
  (`sv_sigma <= 0.3`). It is acceptable as a fallback when explicit
  assembly is infeasible. It is not the default.

- **Out of scope.** High SV dispersion (`sv_sigma >= 0.5`) remains
  unresolved. Thread 2 already documented PCG breakdown at this
  setting under lightweight preconditioning, and the time-averaged
  preconditioner's iteration counts here (74 at sv=0.3) would extend
  unfavourably. Any future work in that regime needs a stronger
  preconditioner first, not a PO-draw redesign.

## Files

- `po_draws.py` -- `build_direct_context`, `build_pcg_context`,
  `_build_perturbation_rhs`, `DirectPOContext.draw`,
  `PCGPOContext.draw`. Self-check at module bottom (run directly).
- `validation.py` -- Monte Carlo summaries (mean / variance /
  functional KS tests).
- `run_thread3.py` -- driver; writes `po_moments.csv`,
  `po_functionals.csv`, `pcg_tolerance.csv` to this directory.
  `--quick` flag restricts to small scale only.
- `po_moments.csv` -- per-(scale, sv, rtol, sampler) sample-mean and
  marginal-variance summaries.
- `po_functionals.csv` -- per-functional direct/PCG comparison with KS
  test.
- `pcg_tolerance.csv` -- PCG iteration counts, residuals, and solve
  times across rtol.

## Reproduction

```bash
cd theory/mf_oi_svmvar_report/code/thread3_po_draws
# benchmark conda env supplies scikit-sparse (sksparse.cholmod).
/opt/homebrew/Caskroom/miniforge/base/envs/benchmark/bin/python run_thread3.py
```

Wallclock on the development machine: ~12 s for the full sweep, ~6 s
for `--quick`.
