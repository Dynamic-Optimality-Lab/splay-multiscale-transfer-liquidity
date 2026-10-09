"""Shift-defect forms done right: Delta = hi - lo with middle-level telescoping.
Chain (L0,L1,L2): lo=Dbar(L0->L1), hi=Dbar(L1->L2); middle rows cancel exactly.
Canonicalize Delta, support-close, optimize, joint DTQ gate.
Usage: python scripts/wp6_shiftdelta.py [forms|gate]
"""
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
vl = load('wp6_validlift')
from wp6_staticR import depths_list
from wp6_lambda import R_coeffs
import wp6_cycle_ratio as O

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def full_P_row(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = Counter()
    for z in dB:
        if z == y:
            continue
        ms[('t', (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
    if dB[y] != 0:
        ms[('K', dB[y])] += dB[y]
    return ms

def dbar_of(B, T, B2, T2, u, v):
    net = Counter()
    for (BB, yy, sgn) in ((B2, u, 1), (B2, v, -1), (T2, u, -1), (T2, v, 1),
                          (B, u, -1), (B, v, 1), (T, u, 1), (T, v, -1)):
        for kk, cc in full_P_row(BB, yy).items():
            net[kk] += sgn * cc
    return Counter({k: v for k, v in net.items() if v != 0})

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def chains():
    out = []
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        p = 100
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            T0 = copy.deepcopy(Tr)
            T1 = lift2_spaced(T0)
            T2 = lift2_spaced(T1)
            def ext(TT):
                return [p, copy.deepcopy(TT), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(TT)]
            B0, B1, B2 = ext(T0), ext(T1), ext(T2)
            for BB in (B0, B1, B2, T0, T1, T2):
                vl.assert_valid_bst(BB)
            if len(depths_list(B2)) > 9:
                continue
            for u in sorted(depths_list(Tr).keys()):
                for v in sorted(depths_list(Tr).keys()):
                    if u >= v:
                        continue
                    lo = dbar_of(B0, T0, B1, T1, u, v)
                    hi = dbar_of(B1, T1, B2, T2, u, v)
                    net = Counter()
                    for kk, cc in hi.items():
                        net[kk] += cc
                    for kk, cc in lo.items():
                        net[kk] -= cc
                    net = Counter({k: v for k, v in net.items() if v != 0})
                    out.append(((3, s, u, v), net))
    return out

def main():
    modes = sys.argv[1:] or ["forms"]
    if "forms" in modes:
        recs = chains()
        seen = {}
        for meta, net in recs:
            key = tuple(sorted((str(k), v) for k, v in net.items()))
            seen.setdefault(key, []).append(meta)
        print(f"[SD] raw shift-defect instances={len(recs)} canonical={len(seen)}", flush=True)
        for key, ml in sorted(seen.items(), key=lambda kv: -len(kv[1]))[:8]:
            net = Counter({eval(k): v for k, v in key})
            fams = Counter()
            for kk in net:
                fams[kk[0] if kk[0] == 'K' else kk[1][0][0]] += 1
            print(f"    count={len(ml)} sup={len(net)} fams={dict(fams)} e.g.{ml[0]}", flush=True)
        out = []
        for key, ml in seen.items():
            out.append({"meta": [list(m) for m in ml], "terms": [[k, v] for k, v in key]})
        json.dump(out, open(OUT / "j4_shiftdelta.json", "w"), indent=1, default=str)
        print("[SD] saved", flush=True)
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
        forms = json.load(open(OUT / "j4_shiftdelta.json"))
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
            print(f"[SD] form{i} e.g.{meta}: missing={miss} sup={int((c != 0).sum())}", flush=True)
        closed = [(c, meta) for (c, miss, meta) in objs if miss == 0]
        print(f"[SD] closed: {len(closed)}/{len(objs)}", flush=True)
        ranges = []
        for c, meta in closed:
            r1 = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            r2 = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0, bounds=[(None, None)] * V, method="highs")
            mn = float(r1.fun) if r1.status == 0 else None
            mx = float(-r2.fun) if r2.status == 0 else None
            ranges.append({"meta": meta, "min": mn, "max": mx})
            print(f"[SD] range e.g.{meta}: [{mn},{mx}]", flush=True)
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
            print(f"[SD] DTQ-shift joint: status={res.status} margin={margin}", flush=True)
            json.dump({"ranges": ranges, "dtq_status": res.status, "dtq_margin": margin},
                      open(OUT / "j4_shiftdtq.json", "w"), indent=1, default=str)
    print("[SD] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
