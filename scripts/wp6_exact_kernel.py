"""Exact integer rank + kernel of SH567 J4 matrix.
- Builds shared J4 [5,6,7] integer matrix via wp6_j4shared.
- Modular rank over 3 large primes (vectorized numpy elimination).
- Floating SVD nullspace -> integer rounding -> EXACT verification A@v==0.
- Saves kernel basis (exact ints) + diagnostics JSON.
Usage: python scripts/wp6_exact_kernel.py
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import importlib.util
spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)

OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def mod_rank(A, p):
    M = (A % p).astype(np.int64).copy()
    E, V = M.shape
    r = 0
    for c in range(V):
        sub = M[r:, c] % p
        nz = np.flatnonzero(sub)
        if nz.size == 0:
            continue
        piv = r + int(nz[0])
        M[[r, piv]] = M[[piv, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r, c:] = (M[r, c:] * inv) % p
        if r + 1 < E:
            col = M[r + 1:, c]
            m = col != 0
            if m.any():
                blk = M[r + 1:, c:]
                blk[m] = (blk[m] - (col[m].reshape(-1, 1) * M[r, c:].reshape(1, -1)) % p) % p
        r += 1
        if r == E:
            break
    return r

def main():
    raw, info = j4.build_shared([5, 6, 7])
    Amat, rhs, metas, vmap = j4.assemble(raw)
    E, V = Amat.shape
    print(f"[XK] E={E} V={V}", flush=True)
    A = Amat.toarray().astype(np.int64)
    print(f"[XK] entry range [{A.min()},{A.max()}] nnz={np.count_nonzero(A)}", flush=True)
    ranks = {}
    for p in (1000000007, 1000000009, 998244353):
        r = mod_rank(A, p)
        ranks[str(p)] = r
        print(f"[XK] rank mod {p} = {r}", flush=True)
    # floating nullspace
    U, S, Vt = np.linalg.svd(A.astype(float), full_matrices=True)
    tol = max(E, V) * np.finfo(float).eps * (S[0] if len(S) else 0.0)
    frank = int((S > tol).sum())
    print(f"[XK] float rank={frank} (tol={tol:.2e}, smin_nz~{S[frank-1] if frank else None}, smax={S[0] if len(S) else None})", flush=True)
    N = Vt[frank:].T  # V x (V-frank)
    print(f"[XK] null cand dim={N.shape[1]}", flush=True)
    inv = {i: k for k, i in vmap.items()}
    basis = []
    for j in range(N.shape[1]):
        v = N[:, j]
        # scale to small integers: try denominators from max element
        sc = v / (np.abs(v).max() + 1e-300)
        # round continued: find integer vector via scaling by 1..200 LLL-lite
        best = None
        for q in range(1, 501):
            w = np.rint(sc * q).astype(np.int64)
            if np.abs(w).max() == 0:
                continue
            if np.linalg.norm(sc * q - w) < 1e-6:
                best = w; break
        if best is None:
            w = np.rint(sc * 60).astype(np.int64)
            best = w
        r = A.astype(np.int64) @ best
        ok = bool((r == 0).all())
        basis.append({"vec": [int(x) for x in best], "verified": ok,
                      "maxabs": int(np.abs(best).max())})
        print(f"[XK] nullvec {j}: maxabs={np.abs(best).max()} exact_null={ok}", flush=True)
    out = {"E": E, "V": V, "mod_ranks": ranks, "float_rank": frank,
           "float_tol": tol, "keys": [str(inv[i]) for i in range(V)],
           "basis": basis}
    (OUT / "j4_sh567_exact_kernel.json").write_text(json.dumps(out, indent=1))
    print("[XK] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
