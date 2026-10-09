"""26L part 2: sharp ambiguity verdict, support closure, value ranges, DTQ gate."""
import sys, copy, json
from pathlib import Path
from collections import Counter, defaultdict
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

AMB = {('LL', 5, 'LL', 'LL', 'even'), ('RR', 5, 'LL', 'LL', 'even')}

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def foldword(B, y):
    P = path_nodes(B, y)
    d = len(P) - 1
    pats = []
    for i in range(d, 1, -2):
        gnd, pnd, xnd = P[i - 2], P[i - 1], P[i]
        sp = 0 if gnd[1] is pnd else 1
        sx = 0 if pnd[1] is xnd else 1
        pats.append({(0, 0): "LL", (1, 1): "RR", (0, 1): "LR", (1, 0): "RL"}[(sp, sx)])
    return pats

def full_P_row_q(B, y):
    """Quotient-mapped P-row: UG twins identified, NONE->K_d (with multiplicity)."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        s_ = j4.slot_of(B, y, z)
        if s_ == ('NONE',):
            ms[('K', dB[y])] += 1
        else:
            ms[('t', (s_, lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
    return ms

def main():
    modes = sys.argv[1:] or ["amb2"]
    if "amb2" in modes:
        # sharp: do the 2 canonical shift forms contain old-F atoms whose
        # table key is ambiguous? Table keys need (pad,j0,w1,w2,term) of the
        # PRE-shift row. j0>=4 necessary (ambiguous keys have j0=5... but j0 is
        # the atom's fringe index; table key j0 == atom j0). Check j0>=4 atoms.
        forms = json.load(open(OUT / "j4_shiftforms_full.json"))
        n579 = 0
        for f in forms:
            for ks, vv in f["terms"]:
                k = eval(ks)
                if k[0] == 't' and k[1][0][0] == 'F' and k[1][0][1] >= 4:
                    n579 += 1
                    print(f"   deep-F term {ks} x{vv} in meta {f['meta']}", flush=True)
        print(f"[SL] deep-j0 F terms in canonical shift forms: {n579}", flush=True)
        # Also: can j0=5 even occur given n<=7 rows? F_5 needs depth>=5 row + fringe.
        # Check realizability of (F_5,*,*,*) in SH567 at all:
        import numpy as np
        Z = np.load(OUT / "j4_rednorm_mat.npz")
        keys = [eval(k) for k in Z["keys"]]
        f5 = [k for k in keys if k[0] == 't' and k[1][0] == ('F', 5)]
        print(f"[SL] (F_5,...) vars in reduced system: {len(f5)}", flush=True)
        for k in f5[:10]:
            print("   ", k, flush=True)
        json.dump({"deepF_terms": n579, "f5_vars": [str(k) for k in f5]},
                  open(OUT / "j4_ambsens2.json", "w"), indent=1, default=str)
    print("[SL] done")
    if "gate" in modes:
        import numpy as np
        from scipy.optimize import linprog
        import scipy.sparse as sp
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
        forms = json.load(open(OUT / "j4_shiftforms_full.json"))
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
                    # K_d in reduced system? keys have ('K',d)
                    if k in rv:
                        c[rv[k]] += vv
                    else:
                        miss += 1
                else:
                    t = k[1]
                    if t in UGMAP:
                        t = UGMAP[t]
                    if t[0] == ('NONE',):
                        # quotient: NONE atoms aggregated; need depth: from atom key t[3]
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
            print(f"[SL] form{i} e.g.{meta}: missing={miss} sup={int((c != 0).sum())}", flush=True)
        # ranges for closed forms (miss==0)
        closed = [(c, meta) for (c, miss, meta) in objs if miss == 0]
        print(f"[SL] closed forms: {len(closed)}/{len(objs)}", flush=True)
        ranges = []
        for c, meta in closed:
            r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0,
                         bounds=[(None, None)] * V, method="highs")
            r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0,
                         bounds=[(None, None)] * V, method="highs")
            mn = float(r1.fun) if r1.status == 0 else None
            mx = float(-r2.fun) if r2.status == 0 else None
            ranges.append({"meta": meta, "min": mn, "max": mx})
            print(f"[SL] range e.g.{meta}: [{mn},{mx}]", flush=True)
        # joint DTQ gate over closed forms
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
            print(f"[SL] DTQ joint: status={res.status} margin={margin}", flush=True)
            json.dump({"ranges": ranges, "dtq_status": res.status, "dtq_margin": margin},
                      open(OUT / "j4_dtqgate.json", "w"), indent=1, default=str)
    print("[SL] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
