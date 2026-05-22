"""Pre-flight memory / nnz estimators for Thread 2b skip decisions.

The full sweep stresses ``n`` up to 20 and ``T`` up to 10000, where building
``Kbar`` explicitly can require 5--30 GB depending on lag length. Before
spending memory we want a cheap closed-form estimate of:

* ``H_B`` nnz (the matrix-free storage bottleneck);
* explicit ``Kbar`` nnz (the per-iter assembly cost on the direct path);
* CSR bytes for the explicit ``Kbar`` (a proxy for peak intermediate RSS).

CHOLMOD ``L`` factor nnz cannot be predicted without a symbolic analysis
(fill-in is reordering-dependent), so we only estimate the inputs.

The estimates count nonzero entries *as if* every banded position is
filled, ignoring the truncation at ``t < p`` (which removes O(p^2 n^2)
entries -- negligible vs O(T n^2)). The aggregation term ``lambda M' M``
adds at most 25 nz per low-frequency row per quarter, which is also
negligible at this scale.

Skip rules:
* ``estimated_Kbar_csr_bytes > MAX_BYTES``  -> skip direct paths
* ``estimated_Kbar_nnz       > MAX_NNZ``    -> skip direct paths
"""

from __future__ import annotations

from dataclasses import dataclass


# CSR storage: nnz * (8 bytes data + 4 bytes col index) + (n_rows+1) * 4
# Plus typically 2x overhead for SciPy intermediate transposes / products.
# Use 16 bytes per nnz as a conservative per-entry cost (data + indices +
# transient copies during ``A' D A`` builds).
_CSR_BYTES_PER_NNZ = 16.0
_DEFAULT_MAX_BYTES = 6.0 * 1024**3  # 6 GB
_DEFAULT_MAX_NNZ = 1e8


@dataclass(frozen=True)
class MemoryEstimate:
    n: int
    T: int
    p: int
    Tn: int
    H_B_nnz: int
    Kbar_nnz: int
    Kbar_csr_bytes: float
    skip_direct: bool
    skip_reason: str


def estimate_H_B_nnz(n: int, T: int, p: int) -> int:
    """``H_B`` has ``I_n`` on the diagonal and ``-B_k`` at the k-th sub-diag.

    For each of ``T`` block-rows: ``n`` identity nz on the diagonal block
    + ``n * n`` nz for each of up to ``p`` previous lags. The first ``p``
    rows have truncated lag sets, but the upper bound is good enough.
    """
    return T * n + T * p * n * n


def estimate_Kbar_nnz(n: int, T: int, p: int) -> int:
    """``Kbar = H_B' D H_B + lambda M_m' M_m``.

    ``H_B' H_B`` is banded with bandwidth ``p * n`` on each side, so each
    block-row has up to ``2 p + 1`` nonzero ``n x n`` blocks. The diagonal
    ``D`` does not change the sparsity pattern. The aggregation term is
    negligible (``M_m`` has at most 5 nz per row, ``M_m' M_m`` adds at
    most ~25 nz per low-frequency monthly cell).
    """
    return T * (2 * p + 1) * n * n


def estimate(
    n: int,
    T: int,
    p: int,
    *,
    max_bytes: float = _DEFAULT_MAX_BYTES,
    max_nnz: float = _DEFAULT_MAX_NNZ,
) -> MemoryEstimate:
    Tn = T * n
    h_nnz = estimate_H_B_nnz(n, T, p)
    k_nnz = estimate_Kbar_nnz(n, T, p)
    k_bytes = k_nnz * _CSR_BYTES_PER_NNZ

    skip = False
    reason = ""
    if k_bytes > max_bytes:
        skip = True
        reason = f"estimated_Kbar_csr_bytes={k_bytes / 1024**3:.2f} GB > {max_bytes / 1024**3:.2f} GB"
    elif k_nnz > max_nnz:
        skip = True
        reason = f"estimated_Kbar_nnz={k_nnz:.2e} > {max_nnz:.2e}"

    return MemoryEstimate(
        n=n, T=T, p=p, Tn=Tn,
        H_B_nnz=h_nnz, Kbar_nnz=k_nnz, Kbar_csr_bytes=k_bytes,
        skip_direct=skip, skip_reason=reason,
    )


if __name__ == "__main__":
    grid = [
        (5, 480, 2), (5, 1920, 2), (5, 1920, 12),
        (10, 1920, 2), (10, 5000, 12), (10, 10000, 12),
        (20, 1920, 12), (20, 5000, 24), (20, 10000, 24),
    ]
    print(f"{'n':>3} {'T':>6} {'p':>3} {'Tn':>8} {'H_B nnz':>12} {'Kbar nnz':>12} {'Kbar GB':>8}  skip?")
    for (n, T, p) in grid:
        est = estimate(n, T, p)
        flag = f"SKIP ({est.skip_reason})" if est.skip_direct else "ok"
        print(f"{n:3d} {T:6d} {p:3d} {est.Tn:8d} {est.H_B_nnz:12d} {est.Kbar_nnz:12d} "
              f"{est.Kbar_csr_bytes / 1024**3:8.3f}  {flag}")
