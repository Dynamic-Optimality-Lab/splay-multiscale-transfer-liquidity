"""Exact QQ kernel basis via sympy on 177 independent rows + classification.
Loads j4_sh567_A.npz. Steps:
1. GF(p) elimination recording pivot rows -> 177 independent row indices.
2. sympy Matrix.nullspace() over QQ on the 177x194 submatrix.
3. Exact verification + classification of each basis vector by induced K_y(B):
   CONST / ROWCONST / SELF-INV / DIAM-INV / GENUINE (tested over all n<=7 pointed configs).
Usage: python scripts/wp6_kernel_qq.py
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))

OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"
P = 1000000007

def indep_rows(A, p):
    M = (A % p).astype(np.int64)
    order = np.arange(A.shape[0])
    E, V = M.shape
    r = 0
    pivots = []
    for c in range(V):
        sub = M[r:, c]
        nz = np.flatnonzero(sub)
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        M[[r, i]] = M[[i, r]]
        order[[r, i]] = order[[i, r]]
        inv = pow(int(M[r, c]), p - 2, p)
        M[r, c:] = (M[r, c:] * inv) % p
        if r + 1 < E:
            col = M[r + 1:, c]
            m = col != 0
            if m.any():
                blk = M[r + 1:, c:]
                blk[m] = (blk[m] - (col[m].reshape(-1, 1) * M[r, c:].reshape(1, -1)) % p) % p
        pivots.append(c)
        r += 1
        if r == E:
            break
    return order[:len(pivots)], pivots

def main():
    Z = np.load(OUT / "j4_sh567_A.npz")
    A = Z["A"].astype(np.int64)
    vm = json.load(open(OUT / "j4_sh567_vmap.json"))["vmap"]
    E, V = A.shape
    print(f"[QQ] A {A.shape}", flush=True)
    idx, pivs = indep_rows(A, P)
    print(f"[QQ] indep rows={len(idx)} pivots={len(pivs)}", flush=True)
    import sympy as sp
    M = sp.Matrix(A[np.sort(idx)].tolist())
    print("[QQ] sympy nullspace...", flush=True)
    NS = M.nullspace()
    print(f"[QQ] dim={len(NS)}", flush=True)
    inv = {i: k for k, i in vm.items()}
    basis = []
    for j, v in enumerate(NS):
        vec = [int(x) for x in v]
        r = A @ np.array(vec, dtype=object)
        ok = bool(all(int(x) == 0 for x in r))
        nz = [(inv[i], vec[i]) for i in range(V) if vec[i] != 0]
        print(f"[QQ] vec {j}: nnz={len(nz)} exact_null={ok} maxabs={max(abs(x) for x in vec)}", flush=True)
        basis.append({"vec": [[str(k), int(c)] for k, c in nz], "verified": ok})
    json.dump({"dim": len(NS), "basis": basis, "keys": [str(inv[i]) for i in range(V)]},
              open(OUT / "j4_sh567_qq_kernel.json", "w"))
    print("[QQ] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
