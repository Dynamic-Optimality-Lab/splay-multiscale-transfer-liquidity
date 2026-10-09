"""UG+AR reduced system: rho(c)=a*c (b=0 gauge), rank/feas/a-range, width probe,
expanded twin rows. b is exact gauge (every row has +1/-1 root pair).
Usage: python scripts/wp6_ugar.py [build|arange|width|expand]
"""
import sys, copy, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"
import importlib.util
def load(name):
    spec = importlib.util.spec_from_file_location(name, str(ROOT / 'scripts' / (name + '.py')))
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
j4 = load('wp6_j4shared')
from wp6_staticR import depths_list, R_static
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

UGMAP = {}
def build_ugmap():
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)
    for dl in (-5, -4):
        UGMAP[(('F', 5), 2, dl, 6)] = ((('F', 5), 1, dl, 6), 1.0)

def build_base():
    """SH567 UG-reduced (t-vars only + root vars), then AR. Returns dict."""
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_sh567_A.npz")
    A0 = sp.csr_matrix(Z["A"].astype(float))
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs0, metas0, vmap = j4b.assemble(raw)
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    pairs = []
    for (k, dl, d) in dom["overlap"]:
        pairs.append((vmap[('t', (('F', k), 2, dl, d))], vmap[('t', (('F', k), 1, dl, d))]))
    A = A0.tolil(); r = rhs0.copy()
    for (e, k) in pairs:
        col = A[:, e].toarray().ravel()
        A[:, k] = A[:, k].toarray().ravel() + col
        r = r - col
    elim = {e for (e, k) in pairs}
    keep = [i for i in range(A.shape[1]) if i not in elim]
    inv = {i: kk for kk, i in vmap.items()}
    keys = [inv[i] for i in keep]
    # AR: root vars -> a*c; b exact gauge (row root-coef sums are 0)
    rcols = [i for i, k in enumerate(keys) if k[0] == 'r']
    # verify gauge: every row's root-coef sum == 0
    Acsr = A[:, keep].tocsr()
    rs = np.asarray(Acsr[:, rcols].sum(axis=1)).ravel()
    print(f"[UAR] root-coef row sums: max abs={np.abs(rs).max()} (0 => b exact gauge)", flush=True)
    acol = np.zeros(Acsr.shape[0])
    for i in rcols:
        acol += np.asarray(Acsr[:, i].toarray()).ravel() * keys[i][1]
    tcols = [i for i in range(len(keys)) if i not in set(rcols)]
    Anew = sp.hstack([Acsr[:, tcols], sp.csr_matrix(acol).T]).tocsr()
    newkeys = [keys[i] for i in tcols] + [('a',)]
    return {"A": Anew, "rhs": r, "keys": newkeys, "metas": metas0,
            "nroot": len(rcols)}

def mod_rank(A, p=1000000007):
    M = (A.toarray().astype(np.int64) % p)
    E, V = M.shape
    r = 0
    for c in range(V):
        sub = M[r:, c]
        nz = np.flatnonzero(sub)
        if nz.size == 0:
            continue
        i = r + int(nz[0])
        M[[r, i]] = M[[i, r]]
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

def feas(A, r, pin_idx):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    E, V = A.shape
    keep = [i for i in range(V) if i not in set(pin_idx)]
    Aub = sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
    cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-r, bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
    return res, keep

def main():
    modes = sys.argv[1:] or ["build"]
    build_ugmap()
    S = build_base()
    A, r, keys = S["A"], S["rhs"], S["keys"]
    E, V = A.shape
    print(f"[UAR] UG+AR E={E} V={V} (root vars removed: {S['nroot']})", flush=True)
    rnk = mod_rank(A)
    print(f"[UAR] rank={rnk} nullity={V-rnk}", flush=True)
    # gauge pin: first t-var (=0). NOTE 'a' observability tested via arange.
    tkeys = [i for i, k in enumerate(keys) if isinstance(k, tuple) and k[0] == 't']
    aidx = keys.index(('a',))
    res, keep = feas(A, r, [tkeys[0]])
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[UAR] feas status={res.status} margin={margin}", flush=True)
    out = {"E": E, "V": V, "rank": rnk, "nullity": V - rnk, "status": res.status, "margin": margin}
    json.dump(out, open(OUT / "j4_ugar.json", "w"), indent=1, default=str)
    if "arange" in modes:
        from scipy.optimize import linprog
        import scipy.sparse as sp
        # min/max a s.t. Ax>=rhs, gauge pin; a = keys.index(('a',))
        # pin gauge t-var to 0 via equality
        Aeq = sp.csr_matrix(([1.0], ([0], [tkeys[0]])), shape=(1, V))
        beq = np.zeros(1)
        c = np.zeros(V); c[aidx] = 1.0
        r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * V, method="highs")
        r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * V, method="highs")
        mn = float(r1.fun) if r1.status == 0 else None
        mx = float(-r2.fun) if r2.status == 0 else None
        print(f"[UAR] a-range: [{mn},{mx}] (st {r1.status}/{r2.status})", flush=True)
        # observability: does a affect row-differences? check column of a in a DIAM row sample
        col = np.asarray(A[:, aidx].toarray()).ravel()
        print(f"[UAR] a-column nnz={int((col != 0).sum())}/{E} range=[{col.min()},{col.max()}]", flush=True)
        json.dump({"a_min": mn, "a_max": mx, "a_nnz": int((col != 0).sum())},
                  open(OUT / "j4_ugar_a.json", "w"), indent=1, default=str)
    if "width" in modes or "expand" in modes:
        np.savez_compressed(OUT / "j4_ugar_mat.npz", A=A.toarray(), rhs=r,
                            keys=np.array([str(k) for k in keys]))
        print("[UAR] saved matrix for width/expand", flush=True)
    print("[UAR] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
