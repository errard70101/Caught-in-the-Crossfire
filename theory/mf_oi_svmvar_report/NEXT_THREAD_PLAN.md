# Next Thread Plan: MF-OI-SVMVAR Technical Work

This plan converts the referee concerns into separate, executable work threads. The immediate goal is not to finish the full MF-OI-SVMVAR, but to de-risk the two hard parts:

1. the SV-aware matrix-free latent-state sampler; and
2. identification of the order-invariant impact matrix in a latent mixed-frequency likelihood.

The computational thread should be handled first because it can produce concrete evidence quickly. The identification thread is deeper and should be treated as a separate theory project.

## Current Position

The original proposal overstated three things:

- It treated Zhu's homoskedastic matrix-free sampler as if it carried over automatically to SV-in-mean.
- It described compute as `O(Tn)`, although Zhu's `O(Tn)` result is memory; compute depends on `iter_PCG`, `K`, and FFT/basis-filter costs.
- It asserted DHK-style point identification at the latent frequency, although DHK's proof is for observed single-frequency data.

The revised position is:

- Matrix-free sampling is still plausible under SV because the operator can be written as a time-invariant VAR shell plus a time-varying sequence of local precision blocks.
- The real computational risk is PCG convergence and preconditioning, not whether the matrix-vector product exists.
- Identification of `B0` is conditional on sampled latent paths unless a separate mixed-frequency identification argument is supplied.

Protocol gate:

- The thread plan is now treated as a high-level roadmap only. Formal mathematical definitions, algorithmic protocols, validation invariants, benchmark accounting rules, and forbidden claims live in `protocols/`.
- Review `protocols/GLOBAL_DEFINITIONS.md` before any further correction rerun or Thread 2c implementation.
- Review the relevant thread protocol before executing that thread. If implementation and protocol conflict, revise the protocol first rather than resolving the ambiguity in code.
- No Thread 2c coding should start until `protocols/THREAD2C_MATRIX_FREE_PROTOCOL.md` is reviewed and accepted.
- No Thread 4, Thread 5, Thread 6, Thread SV, or Thread 7 work should start until the corresponding protocol is reviewed. Thread 7 is gate-level only until Threads 1-6 and the SV/classification protocol pass for any enabled volatility or classification block.

Known protocol risks before execution:

- Thread 5 stationarity rejection can become an MCMC failure mode in high-dimensional VARs. High rejection must trigger a constrained-sampling or prior-bias discussion, not just smaller priors.
- Thread 5 must specify the time-varying-covariance SUR posterior for `Gamma_k`, not only basis reconstruction and companion screening.
- Thread 4 lambda choices must be checked against solver-specific stability. A lambda that CHOLMOD can handle may still break Thread 2c's banded Cholesky route.
- Thread 6 conditional `B0` identification does not guarantee marginal identification or good Thread 7 mixing. Weak-ID and multimodality diagnostics must feed into the full-MCMC gate.
- The Step 4 SV and classification update is governed by `protocols/THREAD_SV_CLASSIFICATION_PROTOCOL.md`; DHK inheritance alone is not a standalone validation.

Thread 2 update:

- The lightweight PCG route did not pass the go/no-go checkpoint. `none`, diagonal Jacobi, and date block-Jacobi all show explosive `iter_PCG` as SV dispersion rises.
- The time-averaged CHOLMOD preconditioner works at baseline and moderate SV dispersion, but it remains slower than direct CHOLMOD at Taiwan-scale monthly dimensions.
- For `n ~= 5`, `T <= 1920`, and monthly lags, direct CHOLMOD is the production baseline. Matrix-free PCG should be treated as a fallback for memory pressure, larger systems, or extreme-frequency settings, not as the default per-sweep speed advantage.
- The computational story is now: direct sparse Cholesky is best at Taiwan scale; matrix-free remains relevant for avoiding assembly/memory pressure and for larger regimes, but only with strong global preconditioning.
- Correction rerun status: the Thread 2 PCG sweep has been rerun with the corrected `D_bar = mean_t(D_t) = B0' diag(mean_t 1/U_t) B0` time-averaged precision preconditioner. Current `results.csv`, `summary_median.csv`, and figures are the operative artifacts; the old `B0' diag(1 / mean_t U_t) B0` numbers are superseded.

Thread 2b update:

- Thread 2b is complete. The fair-cost benchmark is documented in `code/thread2b_fair_cost/THREAD2B_NOTE.md`, with raw results in `code/thread2b_fair_cost/results.csv` and plots `fig_total_time_vs_T`, `fig_memory_vs_Tn`, and `fig_phase_breakdown`.
- Once assembly, factorisation, solve time, and memory proxies are all counted, `direct_cholmod` wins on total time at every completed grid cell. The current matrix-free PCG path with an explicit `Kbar_avg` preconditioner is uniformly slower because it still pays global sparse assembly and factor storage costs.
- At Taiwan-scale dimensions (`n ~= 5`, `T <= 1920`, `p in 2..12`), the production latent-state Gaussian solver should be direct CHOLMOD. Matrix-free PCG should not be advertised as a per-iteration speed advantage.
- The only unresolved matrix-free opportunity is a genuinely no-explicit-`Kbar_avg` preconditioner for larger stress regimes such as `(n=20, T=10000, p=24)`, where explicit sparse assembly was skipped by the memory rule.
- Thread 3 can continue, but its role is validation infrastructure: direct CHOLMOD supplies the reference Gaussian draw against which any future scalable sampler is tested. It is not the endpoint of the general methodological contribution.
- Correction rerun status: Thread 2b has been rerun with the corrected precision-average `D_bar`. The direct CHOLMOD conclusion remains unchanged: at Taiwan-scale dimensions, direct sparse Cholesky is still the production latent-state Gaussian solver, while the current explicit-`Kbar_avg` PCG route remains a diagnostic/scaling baseline rather than a per-sweep speed advantage.

Thread 2c motivation:

- The project is not meant to develop a Taiwan-only method. Direct CHOLMOD is the Taiwan-scale production baseline, but the general MF-OI-SVMVAR contribution still needs a scalable matrix-free route.
- Thread 2b showed that the current `time_avg_chol` PCG route fails to exploit matrix-free structure because it still assembles and factors an explicit global `Kbar_avg`.
- The next matrix-free research task is therefore not another Jacobi-style benchmark. It is to design and test a no-explicit-`Kbar_avg` preconditioner or sampler that avoids global `Tn x Tn` precision assembly.

Thread 3 update:

- Thread 3 is complete. The perturbation-optimisation validation is documented in `code/thread3_po_draws/THREAD3_NOTE.md`, with summary outputs in `po_moments.csv`, `po_functionals.csv`, and `pcg_tolerance.csv`.
- Direct CHOLMOD PO draws reproduce the intended Gaussian posterior: sample means are within theoretical Monte Carlo standard error, marginal variances match `diag(K^{-1})` at the expected sampling error scale, and functional diagnostics are consistent with exact Gaussian draws.
- Matrix-free PCG with `time_averaged_chol` matches direct CHOLMOD within Monte Carlo error in controlled regimes (`sv_sigma in {0.1, 0.3}`), but remains much slower per draw and is diagnostic-only.
- `rtol = 1e-8` is the documented diagnostic-mode PCG tolerance. `rtol = 1e-10` adds cost without visible accuracy gain, while `rtol = 1e-6` is already close at the tested Monte Carlo precision.
- The production/reference latent-state draw is direct CHOLMOD perturbation-optimisation. The next general-method thread is Thread 2c: a scalable no-explicit-`Kbar_avg` matrix-free preconditioner or sampler.
- Correction rerun status: Thread 3 PCG diagnostic iteration counts, solve times, and tolerance comparisons have been refreshed with the corrected time-averaged precision preconditioner. Direct CHOLMOD remains the reference PO draw path; PCG remains diagnostic for controlled regimes and a target for future scalable preconditioning.

Thread 1 rerun and correction update:

- Thread 1 has been rerun after the preconditioner correction. The original explicit-vs-matrix-free `Kbar` equivalence test still passes at roughly `3e-16` to `5e-16` across the tested configurations.
- A new `test_time_avg_precision.py` regression verifies that `D_bar = mean_t(D_t)` equals `B0' diag(mean_t 1/U_t) B0`, and that the corrected `_build_time_averaged_kbar` matches an independent reference to numerical precision.
- The old `1 / mean(U_t)` construction differs from the corrected precision average by about 18-27% at `sv_sigma = 0.3` and 42-52% at `sv_sigma = 0.5`, explaining why the Thread 2/2b/3 PCG correction rerun was required.
- Thread 1 documentation has been reframed: the implementation does not materialise the SV-dependent `Kbar`, but it does materialise and reuse the time-invariant `H_B` shell. `bench_amortised.py` is now explicitly superseded by Thread 2b's fair total-cost benchmark.
- `SVAwareKbar` no longer stores a separate CSR copy of `H_B.T`; it applies `self.H_B.T @ u` directly. Initial-condition truncation and the need to vectorise `build_H_B` before Thread 2c stress dimensions are documented.
- The controlled DGP now defaults to a dense unit-diagonal `B0` to match the order-invariant target. Lower-triangular `B0` remains available only as an explicit legacy test option.

Protocol review update:

- The protocol gate is substantively passable after review of `protocols/README.md` and the 11 protocol files.
- Follow-up edits have been applied before Thread 2c implementation: Thread 2c now pins lower-band SciPy storage, restricts `H_B` boundary corrections to the first `p` dates, requires explicit `M'M` bandwidth-pattern checks, documents the 800MB+ headline-cell feasibility issue, and states that `K_pre` setup cannot be amortized across full MCMC sweeps after `B0` or volatility changes.
- Thread 7 now carries the same Thread 2c cost invariant for full-sampler accounting.
- Thread 5 now records that DHK-style `n=23, K=5` SUR updates remain plausibly dense-Cholesky feasible, so PCG/block SUR is an escape route for materially larger systems rather than a required bottleneck workaround at protocol DGP scales.

## Thread 1: SV-Aware Matrix-Free Matvec

Objective:

Implement and validate the precision product

```text
Kbar x = A' D A x + lambda M' M x,
D = diag(D_1, ..., D_T),
D_t = B0' U_t^{-1} B0.
```

Scope:

- Use a controlled Gaussian latent-path problem, not the full OI-SVMVAR.
- Build `A = H_B S_m` from a stable VAR lag polynomial.
- Implement two products:
  - explicit sparse `Kbar @ x` for small cases;
  - matrix-free forward -> time-varying middle -> adjoint product.
- Verify numerical equivalence.

Deliverables:

- A script under `code/` or `theory/mf_oi_svmvar_report/code/`.
- A short markdown note with:
  - model dimensions;
  - construction of `H_B`, `D_t`, and `M`;
  - relative error between explicit and matrix-free products.

Acceptance criteria:

- Relative matvec error below `1e-10` in small test cases.
- Runtime and memory reported for increasing `T`.

Suggested thread prompt:

```text
Implement a proof-of-concept SV-aware matrix-free matvec for the MF-OI-SVMVAR latent-state precision. Use the current report at theory/mf_oi_svmvar_report/main.tex as context. Focus only on Kbar x = A'DA x + lambda M'M x. Compare against explicit sparse Kbar for small T and report relative errors and runtime.
```

## Thread 2: PCG and Preconditioner Benchmark

Objective:

Determine whether SV destroys the computational advantage through exploding `iter_PCG`.

Scope:

- Reuse Thread 1's matvec.
- Solve `Kbar x = b` with PCG.
- Compare preconditioners:
  - none;
  - scalar diagonal/Jacobi;
  - block-Jacobi by date;
  - optional time-averaged sparse-factor preconditioner.
- Vary:
  - `T`;
  - `n`;
  - SV dispersion;
  - SV persistence;
  - `lambda`;
  - VAR persistence;
  - lag order `p`.

Decisions fixed before implementation:

- The primary preconditioner comparison is `none`, `diagonal_jacobi`, and `block_jacobi_date`.
- Do not treat a vague "smoothed-SV block preconditioner" as a required method. If time permits, implement a stronger optional preconditioner called `time_avg_sparse_factor`:
  - replace the time-varying `D_t` sequence by a time-average precision block `D_bar`;
  - construct `K_pre = A' (I_T kron D_bar) A + lambda M'M`;
  - factorize `K_pre` once and use solves with that factorization as `P^{-1}` inside PCG.
- This optional method is an upper-bound test for whether a stronger approximate direct preconditioner can rescue convergence. It should be reported separately from the three lightweight preconditioners.
- Do not implement EWMA-smoothed `U_t` as a preconditioner unless the thread also defines how `P z = r` is solved cheaply. A smoothed operator alone is not a useful PCG preconditioner.
- Do not add new package dependencies by default. First check whether `scikit-sparse` is already available:
  - if available, use CHOLMOD and label the direct baseline `sparse_cholesky`;
  - if unavailable, use `scipy.sparse.linalg.splu` and label the direct baseline `sparse_direct_lu`, not Cholesky.
- For `block_jacobi_date`, it is acceptable in Thread 2 to construct or reuse explicit sparse `Kbar` and extract the `T` diagonal `n x n` blocks. The benchmark matvec must still use the matrix-free operator. The note must state that explicit `Kbar` is used only for benchmark/preconditioner construction, and that a production implementation can replace this with analytic block construction.
- PCG should use `scipy.sparse.linalg.cg` with `rtol=1e-8`. Use a callback to count iterations. Set `maxiter = min(5*T*n, 20000)` and record whether `maxiter` is hit.
- Include a quick mode for development that uses a reduced grid and one seed.

Baseline design:

```text
n = 5
T = 480
p = 2
sv_sigma = 0.3
sv_rho = 0.95
lambda = 1e4
target_radius = 0.9
seeds = 3
```

One-at-a-time scan grids:

```text
T:             120, 240, 480, 960, 1920
sv_sigma:      0.05, 0.1, 0.3, 0.5, 0.8, 1.2
lambda:        1e2, 1e3, 1e4, 1e5, 1e6
target_radius: 0.5, 0.7, 0.9, 0.97, 0.99
p:             1, 2, 4, 8, 12
```

Use three seeds per cell in the full benchmark and report medians. Do not run a full Cartesian product at this stage.

Deliverables:

- A benchmark table:

```text
T, n, p, sv_sigma, sv_rho, lambda, target_radius,
seed, preconditioner, direct_baseline,
iter_PCG, hit_maxiter, status,
relative_residual, residual_norm,
setup_time, solve_time, matvec_time_mean, wallclock
```

- One plot of `iter_PCG` against SV dispersion.
- One plot of wallclock against `T`.
- A short note explaining whether `iter_PCG` appears stable, logarithmic, or explosive under rising SV dispersion.
- A default preconditioner recommendation.

Acceptance criteria:

- Clear evidence on whether `iter_PCG` is stable, logarithmic, or explosive.
- Direct sparse baseline included for small and medium cases. Use CHOLMOD if available; otherwise use SciPy sparse LU and label it honestly.
- A recommendation for the default preconditioner.
- Go/no-go interpretation after this thread:
  - if `block_jacobi_date` keeps `iter_PCG` bounded or slowly growing across realistic SV dispersion, continue to Thread 3;
  - if `iter_PCG` explodes even with `block_jacobi_date`, pause full sampler work and focus on preconditioner design;
  - if only `time_avg_sparse_factor` works, treat this as evidence that lightweight preconditioning is insufficient and quantify setup costs carefully.

Suggested thread prompt:

```text
Benchmark PCG convergence for the SV-aware matrix-free latent-state precision in theory/mf_oi_svmvar_report. Reuse or implement the matvec Kbar x = A'DA x + lambda M'M x. Compare no preconditioner, diagonal Jacobi, and date block-Jacobi as primary methods. Optionally add a time-averaged sparse-factor preconditioner as a strong upper-bound test. Use one-at-a-time grids around the baseline in NEXT_THREAD_PLAN.md, include a quick mode, and report iter_PCG, residuals, setup/solve time, and direct sparse baseline timings. Do not install new packages unless explicitly requested; use CHOLMOD only if scikit-sparse is already available, otherwise label the baseline sparse_direct_lu.
```

## Thread 3: Perturbation-Optimisation Draw Validation

Objective:

Validate Gaussian latent-state draws from the same conditional posterior under the solver strategy implied by Threads 2 and 2b. Direct CHOLMOD is the production reference at Taiwan scale and the validation reference for future scalable samplers; matrix-free PCG is a fallback that should be checked only as a diagnostic in regimes where Thread 2 shows controlled convergence.

Status:

- Complete. See `code/thread3_po_draws/THREAD3_NOTE.md`.

Scope:

- Use the same Gaussian latent-path model.
- Compute direct sparse Cholesky perturbation-optimisation draws for small and Taiwan-scale cases.
- Compute matrix-free perturbation-optimisation draws using PCG with `time_averaged_chol` only for controlled regimes, initially `sv_sigma in {0.1, 0.3}`.
- Do not use `none`, `jacobi`, or `block_jacobi` as production PCG variants.
- Compare:
  - posterior mean;
  - posterior covariance or selected marginal variances;
  - distribution of linear functionals `c'y`.
- Include a direct sampler based on explicit sparse Cholesky as the accuracy reference.
- Report whether PCG tolerance error is negligible relative to Monte Carlo error.

Deliverables:

- Simulation results comparing direct CHOLMOD posterior summaries with matrix-free PCG posterior summaries in the controlled PCG regime.
- Diagnostics for PCG tolerance effects on sampling accuracy.
- Recommendation for the latent-state draw used in the full MCMC:
  - direct CHOLMOD for Taiwan-scale production and as the gold-standard validation sampler;
  - matrix-free PCG only in larger-scale or memory-constrained regimes after a scalable preconditioner is supplied.

Acceptance criteria:

- Posterior means and variances match direct sampler within Monte Carlo error.
- PCG tolerance recommendation documented for the controlled regime.
- No claim that matrix-free PCG is production-ready at high SV dispersion.

Result:

- PASS. Direct PO draws reproduce the Gaussian posterior summaries, PCG draws match direct CHOLMOD within Monte Carlo error for `sv_sigma in {0.1, 0.3}`, and `rtol = 1e-8` is the recommended diagnostic tolerance.

Suggested thread prompt:

```text
Validate perturbation-optimisation Gaussian draws for the SV-aware MF latent-state sampler. Thread 2b has confirmed that direct CHOLMOD is the Taiwan-scale production solver on total cost. Treat direct CHOLMOD as both the production accuracy reference and the gold-standard validation benchmark for future scalable samplers. Compare matrix-free PCG with time_averaged_chol only as a diagnostic in controlled regimes where Thread 2 showed convergence, initially sv_sigma in {0.1, 0.3}. Report posterior means, selected variances, linear-functional diagnostics, and PCG tolerance sensitivity. Do not present none/jacobi/block_jacobi PCG as production candidates, and do not frame direct CHOLMOD as the endpoint of the general methodological contribution.
```

## Thread 2b: Fair Solver Cost and Memory Benchmark

Objective:

Put Thread 2's solver results on a fair production footing by comparing total direct cost against matrix-free PCG cost, including assembly, factorisation, preconditioner setup, solve time, and memory.

Why this is needed:

- Thread 2 shows direct CHOLMOD dominates the PCG solve at Taiwan-scale dimensions.
- However, the direct path also pays to assemble `Kbar` when SV changes, while the matrix-free path can avoid explicit assembly.
- The proposal should not claim a matrix-free per-solve speed advantage unless total cost and memory support it.

Scope:

- Reuse Thread 1 and Thread 2 code.
- Benchmark at least these paths:
  - `direct_cholmod_total = explicit_Kbar_assembly + CHOLMOD_factor + CHOLMOD_solve`;
  - `direct_splu_total = explicit_Kbar_assembly + sparse_LU_factor + sparse_LU_solve` as fallback/reference;
  - `pcg_time_avg_chol_total = preconditioner_setup + PCG_solve`;
  - `pcg_matrix_free_no_explicit_Kbar = analytic/precomputed preconditioner setup + PCG_solve`, if available.
- Measure peak memory where feasible.
- Expand stress dimensions beyond Thread 2:
  - `n = 5, 10, 20`;
  - `T = 480, 1920, 5000, 10000` where feasible;
  - `p = 2, 12, 24`;
  - `sv_sigma = 0.1, 0.3, 0.5`.

Deliverables:

- A table separating:
  - assembly time;
  - factor/preconditioner setup time;
  - solve time;
  - total time;
  - peak memory or a memory proxy.
- A plot of total time against `T`.
- A plot of memory against `T` or `Tn`.
- A clear recommendation of the solver regime:
  - direct CHOLMOD production regime;
  - matrix-free fallback regime;
  - unresolved/preconditioner-design regime.

Acceptance criteria:

- No comparison mixes direct solve-only cost with matrix-free total cost.
- Direct CHOLMOD is treated as the primary Taiwan-scale production baseline.
- Matrix-free claims are restricted to regimes where it wins on total time, memory, or feasibility.

Suggested thread prompt:

```text
Run a fair total-cost benchmark for the MF-OI-SVMVAR latent-state solver using Thread 1 and Thread 2 code. Compare direct_cholmod_total = explicit Kbar assembly + CHOLMOD factor + solve against matrix-free PCG with time_averaged_chol preconditioning. Separate assembly, setup/factorisation, solve time, total time, and memory proxy. Stress n, T, p, and sv_sigma beyond the Taiwan-scale baseline. The goal is to identify where direct CHOLMOD is production-dominant and where matrix-free becomes useful.
```

## Thread 2c: No-Explicit-Kbar Matrix-Free Preconditioner

Objective:

Develop a genuinely scalable matrix-free preconditioner or sampler path that avoids explicit global `Tn x Tn` precision assembly. This is the computational thread needed for a general MF-OI-SVMVAR method, beyond the Taiwan-scale direct CHOLMOD baseline.

Why this is needed:

- Thread 2b showed that `direct_cholmod` wins at Taiwan-scale dimensions, but the project is not meant to be a Taiwan-only computational method.
- The current `pcg_time_avg_chol_explicit_avgK` path does not deliver a matrix-free advantage because it assembles and factors `Kbar_avg`, which has the same sparsity pattern and factor-storage burden as `Kbar`.
- A general scalable contribution requires avoiding global sparse precision assembly in the preconditioner, not merely using a matrix-free matvec inside PCG.

Candidate routes:

- Analytic block implementation of

```text
K_pre x = H_B' (I_T kron D_bar) H_B x + lambda M' M x
```

  without materialising the global `Kbar_avg` matrix.
- Block-banded or banded Cholesky exploiting the VAR lag bandwidth directly.
- State-space / Kalman simulation-smoother formulation of the same Gaussian latent-path draw.
- FFT or block-Toeplitz approximations only if their approximation error can be diagnosed against Thread 3's direct CHOLMOD reference.

Current implementation note:

- Threads 1-3 validate an `H_B`-materialized sparse-shell path, not Zhu's exact FFT basis-filter path.
- Therefore the `log T` term in the proposal-facing complexity expression is a Zhu best-case reference until Thread 2c, or a later exact FFT/block-Toeplitz thread, validates an exact basis-filter implementation.

Scope:

- Start from the Gaussian latent-path problem used in Threads 1-3.
- Do not revisit `none`, scalar Jacobi, or date block-Jacobi as production candidates.
- Implement at least one no-explicit-`Kbar_avg` route for applying or approximately solving with the time-averaged preconditioner.
- Benchmark against:
  - `direct_cholmod` from Thread 2b;
  - `pcg_time_avg_chol_explicit_avgK` from Thread 2b;
  - Thread 3 direct draw diagnostics when the method is used inside perturbation-optimisation.
- Stress the regimes where direct sparse assembly starts to bind:
  - `n = 10, 20`;
  - `T = 5000, 10000`;
  - `p = 12, 24`;
  - `sv_sigma = 0.1, 0.3, 0.5`.

Deliverables:

- A short design note explaining the chosen no-explicit-`Kbar_avg` route and why it avoids the assembly/factor-storage bottleneck found in Thread 2b.
- Code under `theory/mf_oi_svmvar_report/code/thread2c_matrix_free_preconditioner/`.
- Benchmarks separating setup, apply/solve, total time, iteration count, and memory proxy.
- Accuracy diagnostics against Thread 3's direct CHOLMOD reference if the method is used for posterior draws.
- A revised computational claim for the proposal:
  - direct CHOLMOD for Taiwan-scale production;
  - scalable matrix-free route only where it beats direct CHOLMOD on time, memory, or feasibility.

Acceptance criteria:

- The method does not assemble a global `Tn x Tn` `Kbar` or `Kbar_avg` matrix as part of the matrix-free route.
- The benchmark includes a regime where direct sparse assembly/factorisation is expensive or skipped by memory rules.
- PCG iteration counts remain controlled in at least one large stress regime, or the note clearly explains why the route fails.
- Any approximation error is measured against the direct CHOLMOD reference established in Thread 3.
- No claim of a general scalable sampler is made unless total cost, memory, and accuracy all support it.

Suggested thread prompt:

```text
Design and benchmark a no-explicit-Kbar matrix-free preconditioner or sampler for the SV-aware MF-OI-SVMVAR latent Gaussian problem. Thread 2b showed that the current time_avg_chol PCG path loses because it assembles and factors an explicit global Kbar_avg. Do not revisit Jacobi or date block-Jacobi. Implement a route that avoids global Tn x Tn precision assembly, such as analytic block application of H_B' (I kron D_bar) H_B + lambda M'M, a banded/block-banded solver, or a state-space simulation smoother. Benchmark against direct_cholmod and pcg_time_avg_chol_explicit_avgK in large stress regimes, and use Thread 3 direct CHOLMOD draw diagnostics as the accuracy reference if posterior draws are produced.
```

## Thread 4: Lambda Sensitivity and Exact Aggregation Limit

Objective:

Study whether the soft aggregation penalty approximates exact aggregation without destroying conditioning.

Scope:

- Use the Gaussian latent-path model.
- Vary `lambda` over a grid.
- Track:
  - aggregation residual `||y_L - M y_m||`;
  - posterior mean changes;
  - posterior variance changes;
  - condition number proxy;
  - `iter_PCG` only for the controlled PCG/strong-preconditioner regime;
  - direct CHOLMOD total time and numerical stability.

Deliverables:

- Table and plot showing the tradeoff between aggregation accuracy and conditioning.
- Recommended default `lambda` range for Monte Carlo experiments.

Acceptance criteria:

- A practical finite-`lambda` rule, not just "large lambda".
- Evidence on whether direct CHOLMOD and the strong time-averaged preconditioner absorb the penalty-induced scale problem. Do not use date block-Jacobi as the relevant production preconditioner after Thread 2.

Suggested thread prompt:

```text
Run a lambda sensitivity study for the soft aggregation constraint in the SV-aware mixed-frequency latent-state sampler. Quantify aggregation residuals, posterior changes, direct CHOLMOD total time/stability, PCG iterations under the time_averaged_chol preconditioner, and conditioning proxies as lambda increases. Recommend a finite lambda range. Do not treat date block-Jacobi as a production preconditioner.
```

## Thread 5: Parametric Lag Stability Screening

Objective:

Make the basis-lag restriction operational and stationarity-safe.

Scope:

- Generate `B_j = sum_k Gamma_k phi_k(j/p)`.
- Define and test the time-varying-covariance SUR posterior update for `Gamma_k`.
- Compare basis choices:
  - normalized Legendre;
  - normalized Almon;
  - exponential decay;
  - B-spline if convenient.
- Implement stationarity screening through the companion spectral radius.
- Track rejection rates under plausible priors for `Gamma_k`.

Deliverables:

- A small module that maps `Gamma_k` to `B_1, ..., B_p`.
- A posterior-update note or module implementing the Gaussian conditional precision for `vec(Gamma)`.
- Stability diagnostics by basis and prior scale.
- Recommended prior scaling.

Acceptance criteria:

- Stationarity check is automated.
- The SUR posterior update uses date-specific `D_t = B0' U_t^{-1} B0` weights and documents Minnesota or Horseshoe shrinkage hyperparameter handling.
- Prior scale recommendation keeps rejection rates manageable.

Suggested thread prompt:

```text
Build and test the parametric lag expansion for the MF-OI-SVMVAR report. Implement basis-to-VAR coefficient reconstruction and companion-matrix stationarity screening. Compare normalized Legendre, Almon, and exponential bases, and recommend prior scaling for Gamma_k.
```

## Thread SV: Volatility and Classification Block

Objective:

Validate the Step 4 block from `main.tex`: common volatility paths, idiosyncratic volatility paths, and Markov classification states.

Scope:

- Work conditional on a sampled high-frequency path `y*`.
- Use DHK/CHKP band-sparse ARMH logic for volatility paths, or an explicitly documented equivalent.
- Use FFBS or an equivalent exact finite-state smoother for unclassified-variable state paths.
- Rebuild `U_t` and `D_t` after accepted volatility moves.

Deliverables:

- Standalone synthetic volatility recovery test.
- Standalone classification-path recovery test when classifications are enabled.
- ARMH acceptance rates, volatility ESS, and classification switching frequencies.

Acceptance criteria:

- The block passes `protocols/THREAD_SV_CLASSIFICATION_PROTOCOL.md`.
- Thread 7 cannot enable SV or classification blocks unless this standalone protocol has passed.

Suggested thread prompt:

```text
Implement and validate the standalone SV/classification block for the MF-OI-SVMVAR report. Work conditional on a sampled high-frequency path y*. Follow protocols/THREAD_SV_CLASSIFICATION_PROTOCOL.md: update common and idiosyncratic volatility paths with DHK/CHKP-style band-sparse ARMH or an explicitly documented equivalent, update unclassified-variable Markov state paths with FFBS when classifications are enabled, rebuild U_t and D_t after accepted volatility moves, and report ARMH acceptance rates, volatility ESS, classification switching frequencies, and synthetic recovery diagnostics. Do not compose this into Thread 7 until the standalone tests pass.
```

## Thread 6: Identification Diagnostics for B0

Objective:

Develop diagnostics for the latent mixed-frequency identification problem before attempting a full proof.

Scope:

- Separate two statements:
  - conditional on `y*`, DHK identification applies;
  - after integrating over latent `y*`, identification is not automatic.
- Design numerical diagnostics:
  - rank condition across posterior or simulated latent paths;
  - sensitivity to `lambda`;
  - recovery of known `B0` in controlled DGPs.
- Identify what a formal lemma would need to show.
- Use DHK's simulation study as the template for Monte Carlo comparisons:
  `references/davidson-hou-koop-investigating-economic-uncertainty-using-stochastic-volatility-in-mean-vars-the-importance-of-model-size-order-invariance-and-classification-2025.pdf`
  (Section 3, Table 1, Figures 1-3). Adapt its OI vs triangular, large vs
  small, and time-varying classification comparisons to the mixed-frequency
  latent-path setting.

Deliverables:

- A theory note, not necessarily code-first.
- A proposed rank diagnostic.
- A Monte Carlo design for `B0` recovery.
- A DHK-inspired comparison ladder: `HF-oracle-OI-TVC`, `MF-OI-TVC`,
  `MF-triangular-TVC`, `MF-OI-small`, and `MF-OI-fixed-classification`.
- A list of assumptions needed for a formal result.

Acceptance criteria:

- Clear statement of what is proved, what is only diagnosed, and what remains open.
- No claim that high-frequency latent modelling automatically identifies `B0`.

Suggested thread prompt:

```text
Write a technical note on B0 identification in the latent mixed-frequency MF-OI-SVMVAR. Use DHK and Lütkepohl-Wozniak as the observed-frequency baseline. Separate conditional identification given y* from marginal identification after integrating over latent paths. Propose rank diagnostics and a Monte Carlo recovery design.
```

## Thread 7: Full MCMC Architecture After Components Pass

Objective:

Only after Threads 1-6 and the SV/classification block are credible, assemble the full sampler.

Scope:

- Latent path draw from Threads 1-4.
- Parametric lag update from Thread 5.
- `B0` update from DHK conditional on `y*`.
- Volatility and classification update from the standalone SV/classification protocol.
- Synthetic DGP comparisons should follow the DHK Section 3 logic, with a
  correctly specified large OI/TVC benchmark and misspecified alternatives for
  order dependence, omitted variables, and fixed classification.

Deliverables:

- Full block-Gibbs algorithm in pseudocode.
- Minimal implementation on a small synthetic DGP.
- Convergence diagnostics and timing profile.
- Synthetic recovery tables that separate mixed-frequency loss from
  order-dependence, model-size, and classification misspecification.

Acceptance criteria:

- Each block can be tested independently.
- Full sampler recovers synthetic parameters in a small DGP.
- Runtime bottleneck identified quantitatively.

Suggested thread prompt:

```text
Assemble a minimal full MF-OI-SVMVAR block-Gibbs sampler using the validated latent-path, parametric-lag, and B0 components. Keep the DGP small and synthetic. The goal is architecture validation and timing, not empirical application.
```

## Recommended Order

1. [done] Thread 1: SV-aware matvec.
2. [done] Thread 2: PCG/preconditioner benchmark.
3. [done] Thread 2b: fair solver cost and memory benchmark.
4. [done] Thread 3: perturbation-optimisation draw validation as the direct CHOLMOD reference benchmark.
5. [done] Protocol review: `protocols/GLOBAL_DEFINITIONS.md` and all thread protocols, including `THREAD_SV_CLASSIFICATION_PROTOCOL.md`.
6. [done] Correction rerun: reduced Thread 2 / Thread 2b / Thread 3 PCG diagnostics with corrected `D_bar = mean_t(D_t)`.
7. [done] Thread 2c: no-explicit-Kbar matrix-free preconditioner.
8. [next] Thread 4: lambda sensitivity.
9. Thread 5: parametric lag stability.
10. Thread 6: identification diagnostics.
11. Thread SV: volatility and classification block.
12. Thread 7: full MCMC architecture.

Thread 2c is complete. The banded no-explicit-Kbar_avg preconditioner is
implemented and benchmarked. At the headline stress regime (n=20, T=10000,
p=24, sv=0.3) both direct and explicit PCG paths are memory-skipped; the
banded path converges in 462 iters in 74 s. Banded assembly is 3.5–16×
faster than explicit Kbar_avg assembly across large-cell reference points.
Lambda stress (1e4–1e7) leaves PCG iteration counts unchanged (±3). See
`code/thread2c_matrix_free_preconditioner/THREAD2C_NOTE.md`.

The next execution step is Thread 4: lambda sensitivity.
