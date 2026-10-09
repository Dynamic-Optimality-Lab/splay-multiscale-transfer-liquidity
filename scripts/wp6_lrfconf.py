"""LRF incompatibility analysis: per-equation Tbar ranges, leave-one-out,
Farkas certificate on minimal conflict set.
Usage: python scripts/wp6_lrfconf.py [ranges|loo|farkas]
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
OUT = ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine"

def load_red():
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_rednorm_mat.npz")
    A = sp.csr_matrix(Z["A"]); r = Z["rhs"].copy()
    keys = [eval(k) for k in Z["keys"]]
    return A, r, keys

def lrf_eqs(keys):
    rv = {k: i for i, k in enumerate(keys)}
    reps = json.load(open(OUT / "j4_lrflist.json"))
    eqs = []
    for e in reps:
        cls = tuple(e["class"])
        s1 = eval(e["tau"][0]); l1, dl1, d1 = e["tau"][1], e["tau"][2], e["tau"][3]
        s2 = eval(e["tau2"][0]); l2, dl2, d2 = e["tau2"][1], e["tau2"][2], e["tau2"][3]
        a = ('t', (s1, l1, dl1, d1))
        b = ('t', (s2, l2, dl2, d2))
        if a in rv and b in rv:
            eqs.append({"class": cls, "a": a, "b": b, "ia": rv[a], "ib": rv[b]})
    return eqs

def main():
    modes = sys.argv[1:] or ["ranges"]
    import scipy.sparse as sp
    from scipy.optimize import linprog
    A, r, keys = load_red()
    E, V = A.shape
    eqs = lrf_eqs(keys)
    print(f"[LC] equations: {len(eqs)}", flush=True)
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    def solve_eq_subset(sub, get_margin=True):
        # max-min margin with equalities sub (list of eq indices)
        nEQ = len(sub)
        er, ec, ev = [], [], []
        for i, j in enumerate(sub):
            er += [i, i]; ec += [eqs[j]["ib"], eqs[j]["ia"]]; ev += [1.0, -1.0]
        Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V)) if nEQ else None
        keep = [i for i in range(V) if i != t0]
        # map equality cols to kept (gauge var fixed 0)
        if nEQ:
            er2, ec2, ev2 = [], [], []
            kmap = {old: new for new, old in enumerate(keep)}
            for i in range(nEQ):
                row = Aeq.getrow(i)
                for jj, vv in zip(row.indices, row.data):
                    if jj in kmap:
                        er2.append(i); ec2.append(kmap[jj]); ev2.append(vv)
            AeqK = sp.hstack([sp.csr_matrix((np.array(ev2), (np.array(er2), np.array(ec2))), shape=(nEQ, len(keep))),
                              sp.csr_matrix((nEQ, 1))]).tocsr()
        else:
            AeqK = None
        Aub = sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        kw = {} if AeqK is None else {"A_eq": AeqK, "b_eq": np.zeros(nEQ)}
        res = linprog(cobj, A_ub=Aub, b_ub=-r, bounds=[(None, None)] * len(keep) + [(None, 1e6)],
                      method="highs", **kw)
        return float(-res.fun) if res.status == 0 else None, res.status
    if "ranges" in modes:
        out = []
        for j, e in enumerate(eqs):
            c = np.zeros(V); c[e["ib"]] = 1.0; c[e["ia"]] = -1.0
            # min/max over reduced feasible set with gauge pin
            Aeq0 = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
            beq0 = np.zeros(1)
            r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            mn = float(r1.fun) if r1.status == 0 else None
            mx = float(-r2.fun) if r2.status == 0 else None
            forced = "NONZERO-FORCED" if (mn is not None and (mn > 1e-7 or (mx is not None and mx < -1e-7))) else ("contains-0" if mn is not None else "unbounded?")
            print(f"[LC] eq{j} class={e['class']}: Tbar range=[{mn},{mx}] {forced}", flush=True)
            out.append({"j": j, "class": [str(x) for x in e["class"]], "min": mn, "max": mx, "forced": forced})
        json.dump(out, open(OUT / "j4_lcfranges.json", "w"), indent=1, default=str)
    if "loo" in modes:
        base, st = solve_eq_subset(list(range(len(eqs))))
        print(f"[LC] all-eq margin={base} st={st}", flush=True)
        out = []
        for j in range(len(eqs)):
            sub = [i for i in range(len(eqs)) if i != j]
            m, s = solve_eq_subset(sub)
            print(f"[LC] drop eq{j}: margin={m} st={s}", flush=True)
            out.append({"drop": j, "margin": m, "status": s})
        json.dump(out, open(OUT / "j4_lcfloo.json", "w"), indent=1, default=str)
    print("[LC] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
