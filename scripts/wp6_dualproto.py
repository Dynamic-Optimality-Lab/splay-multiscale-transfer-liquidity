"""Correct-sign dual prototype for forced m=1 gap + L1 vertex gap diagnostic."""
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
    Z = np.load(OUT / "j4_sh567_A.npz")
    Amat = sp.csr_matrix(Z["A"].astype(float))
    import importlib.util
    spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
    raw, info = j4.build_shared([5, 6, 7])
    A2, rhs, metas, vmap = j4.assemble(raw)
    E, V = Amat.shape
    from collections import defaultdict
    fams = defaultdict(list)
    for k, i in vmap.items():
        t = k
        if t[0] == 't' and t[1][0] == ('NONE',):
            fams[t[1][3]].append((t[1][2], i))
    er, ec, ev, beq = [], [], [], []
    for dy, lst in sorted(fams.items()):
        base = [i for (dl, i) in lst if dl == -1][0]
        for (dl, i) in lst:
            if dl != -1:
                er += [len(beq), len(beq)]; ec += [i, base]; ev += [1.0, -1.0]
                beq.append(0.0)
    tk = [k for k in vmap if k[0] == 't'][0]; rk = [k for k in vmap if k[0] == 'r'][0]
    er += [len(beq), len(beq) + 1]; ec += [vmap[tk], vmap[rk]]; ev += [1.0, 1.0]
    beq += [0.0, 0.0]
    beq = np.array(beq); nEQ = len(beq)
    Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
    # correct dual of min c^Tx s.t. -Ax<=-rhs, Aeq x=beq:
    # max rhs^T y + beq^T w s.t. A^T y + Aeq^T w = c, y>=0  -> min -(rhs^T y+beq^T w)
    key1 = ('t', (('F', 3), 1, -3, 4)); key2 = ('t', (('F', 3), 2, -3, 4))
    c = np.zeros(V); c[vmap[key2]] = 1.0; c[vmap[key1]] = -1.0
    M = sp.hstack([Amat.T, Aeq.T]).tocsr()
    c2 = np.concatenate([rhs, beq])
    res = linprog(-c2, A_eq=M, b_eq=c, bounds=[(0, None)] * E + [(None, None)] * nEQ, method="highs")
    print(f"[DP] dual max status={res.status} obj={float(-res.fun) if res.status==0 else None} (expect 1.0)", flush=True)
    if res.status == 0:
        y = res.x[:E]
        sup = np.where(y > 1e-7)[0]
        print(f"[DP] support={len(sup)}", flush=True)
        rows = []
        for i in sup[np.argsort(-y[sup])][:16]:
            print(f"    y={float(y[i]):.4f} {metas[i][:7]} rhs={float(rhs[i]):.2f}", flush=True)
            rows.append([float(y[i]), [str(x) for x in metas[i][:7]], float(rhs[i])])
        json.dump({"obj": float(-res.fun), "support": rows}, open(OUT / "j4_gapdual_fix.json", "w"), indent=1, default=str)
    # L1 vertex gaps
    J = dict(json.load(open(OUT / "j4shared_567_l1.json"))["vals"])
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    print("[DP] L1 vertex pointwise gaps:", flush=True)
    for (k, dl, d) in dom["overlap"]:
        v1 = J.get(str(('t', (('F', k), 1, dl, d))), None)
        v2 = J.get(str(('t', (('F', k), 2, dl, d))), None)
        print(f"    k={k} dl={dl} d={d}: {v2}-{v1}={None if v1 is None or v2 is None else round(v2-v1,4)}", flush=True)
    print("[DP] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
