"""LRF_obs gate: canonical 20 single-transition formulas (representative per
(parity,sx,sx2,slot,lam) Lift2 class), joint feasibility, rank, incompat analysis.
 representative: first corpus occurrence; equation jbar(tau')-jbar(tau)=0.
Usage: python scripts/wp6_lrf.py [formulas|gate]
"""
import sys, copy, json
from pathlib import Path
from collections import defaultdict
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
from wp6_staticR import depths_list, path_nodes
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def build_formulas():
    """Return list of dicts: class key + representative (tau, tau2)."""
    reps = {}
    for T in O.shapes_of(list(range(1, 6)))[:60]:
        for y in range(1, 6):
            Py = path_nodes(T, y)
            if Py is None:
                continue
            d = len(Py) - 1
            if d < 2 or d > 3:
                continue
            sx = 0 if Py[0][1] is Py[1] else 1
            sx2 = 0 if Py[1][1] is Py[2] else 1
            T2 = [0, None, [-1, None, copy.deepcopy(T)]]
            _, lam = R_coeffs(T, y)
            _, lam2 = R_coeffs(T2, y)
            dT = depths_list(T)
            for z in range(1, 6):
                if z == y:
                    continue
                s0 = j4.slot_of(T, y, z)
                if s0[0] not in ('L', 'R'):
                    continue
                key = (d % 2, sx, sx2, s0[0], lam.get(z, 0))
                if key not in reps:
                    s1 = j4.slot_of(T2, y, z)
                    dT2 = depths_list(T2)
                    tau = (s0, lam.get(z, 0), dT[z] - dT[y], dT[y])
                    tau2 = (s1, lam2.get(z, 0), dT2[z] - dT2[y], dT2[y])
                    reps[key] = {"tau": tau, "tau2": tau2}
    return reps

def main():
    modes = sys.argv[1:] or ["formulas"]
    reps = build_formulas()
    print(f"[LRF] classes: {len(reps)}", flush=True)
    for k in sorted(reps, key=str):
        r = reps[k]
        print(f"    class par={k[0]} sx={k[1]} sx2={k[2]} slot={k[3]} lam={k[4]}:", flush=True)
        print(f"      {r['tau']} -> {r['tau2']}", flush=True)
    json.dump([{"class": list(k), "tau": [str(r["tau"][0]), r["tau"][1], r["tau"][2], r["tau"][3]],
                "tau2": [str(r["tau2"][0]), r["tau2"][1], r["tau2"][2], r["tau2"][3]]}
               for k, r in sorted(reps.items(), key=str)],
              open(OUT / "j4_lrflist.json", "w"), indent=1, default=str)
    if "gate" in modes:
        import scipy.sparse as sp
        from scipy.optimize import linprog
        Z = np.load(OUT / "j4_rednorm_mat.npz")
        A = sp.csr_matrix(Z["A"]); r = Z["rhs"].copy()
        keys = [eval(k) for k in Z["keys"]]
        E, V = A.shape
        rv = {k: i for i, k in enumerate(keys)}
        # equations jbar(t2)-jbar(t1)=0 for reps whose BOTH vars exist
        eqs = []
        missing = 0
        for k, rp in sorted(reps.items(), key=str):
            a = ('t', rp["tau"]); b = ('t', rp["tau2"])
            if a in rv and b in rv:
                eqs.append((rv[b], rv[a]))
            else:
                missing += 1
        print(f"[LRF] equations usable: {len(eqs)}/{len(reps)} (missing vars: {missing})", flush=True)
        nEQ = len(eqs)
        er, ec, ev = [], [], []
        for i, (jb, ja) in enumerate(eqs):
            er += [i, i]; ec += [jb, ja]; ev += [1.0, -1.0]
        Aeq = sp.csr_matrix((np.array(ev), (np.array(er), np.array(ec))), shape=(nEQ, V))
        beq = np.zeros(nEQ)
        # rank of equations (mod prime)
        M = (Aeq.toarray().astype(np.int64) % 1000000007)
        rr = 0
        for c in range(V):
            sub = M[rr:, c]
            nz = np.flatnonzero(sub)
            if nz.size == 0:
                continue
            i = rr + int(nz[0])
            M[[rr, i]] = M[[i, rr]]
            inv = pow(int(M[rr, c]), 1000000007 - 2, 1000000007)
            M[rr, c:] = (M[rr, c:] * inv) % 1000000007
            if rr + 1 < nEQ:
                col = M[rr + 1:, c]
                m = col != 0
                if m.any():
                    blk = M[rr + 1:, c:]
                    blk[m] = (blk[m] - (col[m].reshape(-1, 1) * M[rr, c:].reshape(1, -1)) % 1000000007) % 1000000007
            rr += 1
            if rr == nEQ:
                break
        print(f"[LRF] raw eqs={nEQ} independent={rr}", flush=True)
        # feasibility with gauge pin (gauge var fixed 0: drop its equality entries)
        t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
        keep = [i for i in range(V) if i != t0]
        kmap = {old: new for new, old in enumerate(keep)}
        er2, ec2, ev2 = [], [], []
        for i in range(nEQ):
            row = Aeq.getrow(i)
            for j, v in zip(row.indices, row.data):
                if j in kmap:
                    er2.append(i); ec2.append(kmap[j]); ev2.append(v)
                # dropped gauge var == 0: contributes nothing
        import scipy.sparse as _sp
        AeqK = _sp.hstack([_sp.csr_matrix((np.array(ev2), (np.array(er2), np.array(ec2))), shape=(nEQ, len(keep))),
                             _sp.csr_matrix((nEQ, 1))]).tocsr()
        Aub = sp.hstack([-A[:, keep], np.ones((E, 1))]).tocsr()
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=Aub, b_ub=-r, A_eq=AeqK, b_eq=beq,
                      bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
        margin = float(-res.fun) if res.status == 0 else None
        print(f"[LRF] joint feas status={res.status} margin={margin}", flush=True)
        out = {"classes": len(reps), "usable": len(eqs), "independent": rr,
               "status": res.status, "margin": margin}
        if res.status == 0:
            g = np.zeros(V); g[keep] = res.x[:len(keep)]
            drops = (A @ g) - r
            out["minslack"] = float(drops.min())
            out["verdict"] = "LRF_obs-COMPATIBLE"
            print(f"[LRF] minslack={out['minslack']:.3e}", flush=True)
        else:
            out["verdict"] = "LRF_obs-INCOMPATIBLE"
        json.dump(out, open(OUT / "j4_lrfgate.json", "w"), indent=1, default=str)
    print("[LRF] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
