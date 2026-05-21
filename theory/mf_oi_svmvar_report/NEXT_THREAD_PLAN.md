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

Thread 2 update:

- The lightweight PCG route did not pass the go/no-go checkpoint. `none`, diagonal Jacobi, and date block-Jacobi all show explosive `iter_PCG` as SV dispersion rises.
- The time-averaged CHOLMOD preconditioner works at baseline and moderate SV dispersion, but it remains slower than direct CHOLMOD at Taiwan-scale monthly dimensions.
- For `n ~= 5`, `T <= 1920`, and monthly lags, direct CHOLMOD is the production baseline. Matrix-free PCG should be treated as a fallback for memory pressure, larger systems, or extreme-frequency settings, not as the default per-sweep speed advantage.
- The computational story is now: direct sparse Cholesky is best at Taiwan scale; matrix-free remains relevant for avoiding assembly/memory pressure and for larger regimes, but only with strong global preconditioning.

Thread 2b update:

- Thread 2b is complete. The fair-cost benchmark is documented in `code/thread2b_fair_cost/THREAD2B_NOTE.md`, with raw results in `code/thread2b_fair_cost/results.csv` and plots `fig_total_time_vs_T`, `fig_memory_vs_Tn`, and `fig_phase_breakdown`.
- Once assembly, factorisation, solve time, and memory proxies are all counted, `direct_cholmod` wins on total time at every completed grid cell. The current matrix-free PCG path with an explicit `Kbar_avg` preconditioner is uniformly slower because it still pays global sparse assembly and factor storage costs.
- At Taiwan-scale dimensions (`n ~= 5`, `T <= 1920`, `p in 2..12`), the production latent-state Gaussian solver should be direct CHOLMOD. Matrix-free PCG should not be advertised as a per-iteration speed advantage.
- The only unresolved matrix-free opportunity is a genuinely no-explicit-`Kbar_avg` preconditioner for larger stress regimes such as `(n=20, T=10000, p=24)`, where explicit sparse assembly was skipped by the memory rule.
- The next executable thread is Thread 3: validate perturbation-optimisation draws using direct CHOLMOD as the production accuracy reference. PCG comparisons should be limited to controlled diagnostic regimes, not presented as production candidates.

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

Validate Gaussian latent-state draws from the same conditional posterior under the solver strategy implied by Threads 2 and 2b. Direct CHOLMOD is the production reference at Taiwan scale; matrix-free PCG is a fallback that should be checked only as a diagnostic in regimes where Thread 2 shows controlled convergence.

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
  - direct CHOLMOD for Taiwan-scale production, since Thread 2b confirms total-cost dominance;
  - matrix-free PCG only in larger-scale or memory-constrained regimes.

Acceptance criteria:

- Posterior means and variances match direct sampler within Monte Carlo error.
- PCG tolerance recommendation documented for the controlled regime.
- No claim that matrix-free PCG is production-ready at high SV dispersion.

Suggested thread prompt:

```text
Validate perturbation-optimisation Gaussian draws for the SV-aware MF latent-state sampler. Thread 2b has confirmed that direct CHOLMOD is the Taiwan-scale production solver on total cost. Treat direct CHOLMOD as the production accuracy reference. Compare matrix-free PCG with time_averaged_chol only as a diagnostic in controlled regimes where Thread 2 showed convergence, initially sv_sigma in {0.1, 0.3}. Report posterior means, selected variances, linear-functional diagnostics, and PCG tolerance sensitivity. Do not present none/jacobi/block_jacobi PCG as production candidates.
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
- Compare basis choices:
  - normalized Legendre;
  - normalized Almon;
  - exponential decay;
  - B-spline if convenient.
- Implement stationarity screening through the companion spectral radius.
- Track rejection rates under plausible priors for `Gamma_k`.

Deliverables:

- A small module that maps `Gamma_k` to `B_1, ..., B_p`.
- Stability diagnostics by basis and prior scale.
- Recommended prior scaling.

Acceptance criteria:

- Stationarity check is automated.
- Prior scale recommendation keeps rejection rates manageable.

Suggested thread prompt:

```text
Build and test the parametric lag expansion for the MF-OI-SVMVAR report. Implement basis-to-VAR coefficient reconstruction and companion-matrix stationarity screening. Compare normalized Legendre, Almon, and exponential bases, and recommend prior scaling for Gamma_k.
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

Deliverables:

- A theory note, not necessarily code-first.
- A proposed rank diagnostic.
- A Monte Carlo design for `B0` recovery.
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

Only after Threads 1-6 are credible, assemble the full sampler.

Scope:

- Latent path draw from Threads 1-4.
- Parametric lag update from Thread 5.
- `B0` update from DHK conditional on `y*`.
- Volatility and classification update from DHK/CHKP.

Deliverables:

- Full block-Gibbs algorithm in pseudocode.
- Minimal implementation on a small synthetic DGP.
- Convergence diagnostics and timing profile.

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
4. [next] Thread 3: perturbation-optimisation draw validation.
5. Thread 4: lambda sensitivity.
6. Thread 5: parametric lag stability.
7. Thread 6: identification diagnostics.
8. Thread 7: full MCMC architecture.

The Thread 2b go/no-go checkpoint has been reached: after counting assembly, factorisation, solve time, and memory proxies, direct CHOLMOD remains dominant at Taiwan-scale monthly dimensions. The production implementation should use direct CHOLMOD for Taiwan-scale latent Gaussian solves and keep matrix-free PCG as a larger-scale fallback or preconditioner-design research item. Move next to Thread 3 to validate perturbation-optimisation draws under this solver strategy.
