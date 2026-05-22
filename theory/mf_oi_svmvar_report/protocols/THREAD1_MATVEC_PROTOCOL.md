# Thread 1 Protocol: SV-Aware Matrix-Free Matvec

Reference implementation: `code/thread1_matvec/`.

## Formal Target

Validate the product

```text
K x = H_B' blockdiag(D_1, ..., D_T) H_B x + lambda M' M x,
D_t = B0' diag(1 / U_t) B0.
```

Thread 1 is a matvec protocol only. It does not establish solver competitiveness.

## Algorithm

Explicit reference:

1. Build `H_B`.
2. Build `D = blockdiag(D_1, ..., D_T)`.
3. Build `K_exp = H_B' D H_B + lambda M' M`.
4. Apply `K_exp @ x`.

Matrix-free product:

1. `w = H_B @ x`.
2. For each date, `u_t = B0' diag(1 / U_t) B0 w_t`.
3. `z = H_B.T @ u`.
4. `z = z + lambda M' (M x)`.

Implementation note: `H_B` may be materialized and reused. The claim is only that `K` and `D` are not materialized in the matrix-free path.

Order-invariant compatibility:

- the default DGP and matvec tests must include a dense unrestricted `B0`;
- lower-triangular `B0` may be retained only as a legacy controlled case;
- production code must not rely on triangular zero restrictions when applying
  `D_t = B0' diag(1 / U_t) B0`.

## Boundary Convention

Rows `0..p-1` of `H_B` truncate unavailable lags. This induces a boundary convention different from interior dates. A production model may instead condition on pre-sample values or fold them into an intercept term. Thread 1 only verifies the truncated-lag convention is implemented consistently in explicit and matrix-free products.

## Validation Invariants

For all tested cases and random vectors:

```text
||K_exp x - K_mf x|| / max(||K_exp x||, 1e-300) < 1e-10.
```

Small-case SPD sanity:

```text
K_exp is symmetric within relative numerical tolerance,
and dense Cholesky succeeds for small Tn.
```

Time-averaged precision regression:

```text
D_bar = mean_t(D_t) = B0' diag(mean_t(1 / U_t)) B0.
```

The corrected preconditioner builder must match an independently constructed `K_pre` to numerical precision.

## Benchmark Accounting

Thread 1 may report:

- `H_B` nnz;
- `K_exp` nnz;
- per-matvec time;
- explicit assembly time as a diagnostic.

Thread 1 may not use `assemble + iter_PCG * SpMV` as evidence against direct CHOLMOD. `bench_amortised.py` is superseded by Thread 2b.

## Required Commands

```bash
cd theory/mf_oi_svmvar_report/code/thread1_matvec
python3 test_equivalence.py
python3 test_time_avg_precision.py
```

Both must pass before Thread 2/2b/3 correction reruns or Thread 2c work proceeds.

## Expected Outputs

- `THREAD1_NOTE.md` states that `H_B` is materialized but `K` is not.
- `test_equivalence.py` reports max relative error below `1e-10` for dense
  `B0` and the legacy lower-triangular case.
- `test_time_avg_precision.py` reports corrected `D_bar` agreement and
  old-vs-new `D_bar` contrast for dense `B0`.

## Forbidden Claims

Do not claim:

- no `Tn x Tn` matrix is materialized;
- Thread 1 establishes solver-level speed;
- matrix-free storage is uniformly 50% lower without counting `H_B`, optional transpose storage, `M`, and `M.T`.
- triangular `B0` optimizations are production-safe for the OI target.
