"""Farkas certificate for joint LRF incompatibility (UG+AR reduced + 20 eqs)."""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def main():
    import scipy.sparse as sp
    from scipy.optimize import linprog
    Z = np.load(OUT / "j4_rednorm_mat.npz")
    A = sp.csr_matrix(Z["A"]); r = Z["rhs"].copy()
    keys = [eval(k) for k in Z["keys"]]
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    reps = json.load(open(OUT / "j4_lrflist.json"))
    er, ec, ev = [], [], []
    for i, e in enumerate(reps):
        a = ('t', (eval(e["tau"][0]), e["tau"][1], e["tau"][2], e["tau"][3]))
        b = ('t', (eval(e["tau2"][0]), e["tau2"][1], e["tau2"][2], e["tau2"][3]))
        er += [i, i]; ec += [rv[b], rv[a]]; ev += [1.0, -1.0]
    nEQ = len(reps)
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    # gauge pin as equality
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    Aeq2 = sp.vstack([Aeq, sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))]).tocsr()
    beq = np.zeros(nEQ + 1)
    # Farkas: max r^T y + beq^T w s.t. A^T y + Aeq2^T w = 0, y>=0, sum(y)+|w|_1<=1
    # linearize |w|: w = w+ - w-, bounds: y in [0,1], w+,w- in [0,1], sum<=1 via extra constraint
    nW = nEQ + 1
    # vars [y(E), wp(nW), wm(nW)]; eqs: A^T y + G^T(wp-wm) = 0 (V eqs); ineq: sum <= 1
    G = Aeq2
    Meq = sp.hstack([A.T, G.T, -G.T]).tocsr()
    cobj = -np.concatenate([r, beq, -beq])  # min -(r^T y + beq^T(wp-wm))
    Aub = sp.csr_matrix(np.ones((1, E + 2 * nW)))
    res = linprog(cobj, A_ub=Aub, b_ub=np.ones(1), A_eq=Meq, b_eq=np.zeros(V),
                  bounds=[(0, 1)] * (E + 2 * nW), method="highs")
    print(f"[LF] Farkas status={res.status} max_viol={float(-res.fun) if res.status==0 else None}", flush=True)
    if res.status == 0:
        y = res.x[:E]
        wp = res.x[E:E + nW]; wm = res.x[E + nW:]
        w = wp - wm
        sup = np.where(y > 1e-7)[0]
        print(f"[LF] row support={len(sup)} eq-support={int((np.abs(w) > 1e-7).sum())}", flush=True)
        # decode: need metas
        import importlib.util
        spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
        j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
        raw, info = j4b.build_shared([5, 6, 7])
        A2, rhs2, metas, vmap = j4b.assemble(raw)
        rows = []
        for i in sup[np.argsort(-y[sup])][:16]:
            print(f"    y={float(y[i]):.4f} {metas[i][:7]} rhs={float(rhs2[i]):.1f}", flush=True)
            rows.append([float(y[i]), [str(x) for x in metas[i][:7]], float(rhs2[i])])
        eqs_used = [[int(i), float(w[i])] for i in range(nW) if abs(w[i]) > 1e-7]
        print(f"[LF] LRF-eq weights used: {eqs_used}", flush=True)
        json.dump({"value": float(-res.fun), "rows": rows, "eqw": eqs_used},
                  open(OUT / "j4_lrffarkas.json", "w"), indent=1, default=str)
    print("[LF] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
