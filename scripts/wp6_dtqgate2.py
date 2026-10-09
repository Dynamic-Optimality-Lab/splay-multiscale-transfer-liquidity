"""Valid-lift DTQ gate redo: support closure, ranges, joint feasibility."""
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
    A = sp.csr_matrix(Z["A"])
    r = Z["rhs"].copy()
    keys = [eval(k) for k in Z["keys"]]
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    UGMAP = {}
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d))
    forms = json.load(open(OUT / "j4_shiftforms_v2.json"))
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    Aeq0 = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
    beq0 = np.zeros(1)
    objs = []
    for f in forms:
        c = np.zeros(V)
        miss = 0
        for ks, vv in f["terms"]:
            k = eval(ks)
            if k[0] == 'K':
                if k in rv:
                    c[rv[k]] += vv
                else:
                    miss += 1
            else:
                t = k[1]
                if t in UGMAP:
                    t = UGMAP[t]
                if t[0] == ('NONE',):
                    kk = ('K', t[3])
                    if kk in rv:
                        c[rv[kk]] += vv
                    else:
                        miss += 1
                elif ('t', t) in rv:
                    c[rv[('t', t)]] += vv
                else:
                    miss += 1
        objs.append((c, miss, f["meta"]))
    for i, (c, miss, meta) in enumerate(objs):
        print(f"[G2] form{i} e.g.{meta}: missing={miss} sup={int((c != 0).sum())}", flush=True)
    closed = [(c, meta) for (c, miss, meta) in objs if miss == 0]
    print(f"[G2] closed: {len(closed)}/{len(objs)}", flush=True)
    ranges = []
    for c, meta in closed:
        r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
        r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
        mn = float(r1.fun) if r1.status == 0 else None
        mx = float(-r2.fun) if r2.status == 0 else None
        ranges.append({"meta": meta, "min": mn, "max": mx})
        print(f"[G2] range e.g.{meta}: [{mn},{mx}]", flush=True)
    if closed:
        nEQ = len(closed)
        er, ec, ev = [], [], []
        for i, (c, meta) in enumerate(closed):
            nz = np.flatnonzero(c)
            for j in nz:
                er.append(i); ec.append(j); ev.append(float(c[j]))
        Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
        beq = np.zeros(nEQ)
        keep = [i for i in range(V) if i != t0]
        import scipy.sparse as _sp
        AeqK = _sp.hstack([Aeq[:, keep], _sp.csr_matrix((nEQ, 1))]).tocsr()
        Aub = _sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=Aub, b_ub=-r, A_eq=AeqK, b_eq=beq,
                      bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
        margin = float(-res.fun) if res.status == 0 else None
        print(f"[G2] DTQ-v2 joint: status={res.status} margin={margin}", flush=True)
        json.dump({"ranges": ranges, "dtq_status": res.status, "dtq_margin": margin},
                  open(OUT / "j4_dtqgate_v2.json", "w"), indent=1, default=str)
    print("[G2] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
