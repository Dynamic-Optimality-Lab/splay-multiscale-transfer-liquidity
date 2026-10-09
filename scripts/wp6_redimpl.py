"""Reduced-coordinate implication tests: Tbar class collapse, old-F uniformity,
B_K ranges, width recheck, reduced SELF formula.
Usage: python scripts/wp6_redimpl.py [tbar|foldF|bk|width]
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
    A = sp.csr_matrix(Z["A"])
    r = Z["rhs"]
    keys = [eval(k) for k in Z["keys"]]
    return A, r, keys

def feas_wrap(A, r, c, pin):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    V = A.shape[1]
    nEQ = 1
    Aeq = sp.csr_matrix(([1.0], ([0], [pin])), shape=(nEQ, V))
    beq = np.zeros(nEQ)
    out = []
    for sgn in (1.0, -1.0):
        res = linprog(sgn * c, A_ub=-A, b_ub=-r, A_eq=Aeq, b_eq=beq,
                      bounds=[(None, None)] * V, method="highs")
        out.append(float(sgn * res.fun) if res.status == 0 else None)
    return out  # [min, max]

def mode_tbar():
    A, r, keys = load_red()
    rv = {k: i for i, k in enumerate(keys)}
    pin = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    # Tbar for Lift2 L/R transition classes: jbar(tau')-jbar(tau).
    # Reuse banked type transitions: for each (parity,sx,sx2,slot,lam)->(slot',lam',ddelta)
    # from oldcore data; here test VALUE ranges of Tbar grouped with/without lambda.
    # We need the type maps: rebuild quickly from wp6_lift2 oldcore? Use class_table rule:
    # single-pad rule verified; Lift2 = two pads. Approximate Lift2 Tbar by composing
    # single-pad Tbar ranges? Instead directly optimize a few concrete Tbar instances:
    tests = {}
    # concrete: (L,-1,d=1,dy=1) -> under LL pad? Use realized vars only.
    cand = []
    for k in keys:
        if k[0] == 't' and k[1][0] in (('L',), ('R',)):
            cand.append(k)
    print(f"[RI] L/R reduced vars: {len(cand)}", flush=True)
    # group Tbar = jbar(B)-jbar(A) for same (slot, dlam-class)? Simplify: report
    # value ranges of a sample of jbar vars themselves (spread), then Tbar for
    # the 20 banked L/R transition pairs is future work; here test Tbar=0 hypothesis
    # on the simplest: persistent (L,lam) with dlam=0 class (even-depth stays).
    # Find var pairs ((L,lam,dl,d),(L,lam,dl,d+1)) both realized:
    pairs = []
    S = {(k[1][0], k[1][1], k[1][2], k[1][3]) for k in cand}
    for (s, lam, dl, d) in sorted(S, key=str):
        a = ('t', (s, lam, dl, d)); b = ('t', (s, lam, dl, d + 1))
        if a in rv and b in rv:
            pairs.append((a, b))
    print(f"[RI] Tbar candidate persistence pairs: {len(pairs)}", flush=True)
    out = []
    for (a, b) in pairs[:14]:
        c = np.zeros(A.shape[1]); c[rv[b]] = 1.0; c[rv[a]] = -1.0
        mn, mx = feas_wrap(A, r, c, pin)
        out.append({"pair": [str(a), str(b)], "min": mn, "max": mx})
        print(f"    Tbar {a[1][0]}{a[1][1:]} -> d+1: [{mn},{mx}]", flush=True)
    json.dump(out, open(OUT / "j4_ritbar.json", "w"), indent=1, default=str)

def mode_foldF():
    A, r, keys = load_red()
    rv = {k: i for i, k in enumerate(keys)}
    pin = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    # old-F reduced transition uniformity: group realized (F_j,lam) vars'
    # Tbar analog: persistence (F_j,lam,dl,d)->(F_j,lam,dl,d+1)? F index may shift;
    # test same-index persistence ranges grouped by j, then merged over j.
    from collections import defaultdict
    fams = defaultdict(list)
    S = {(k[1][0], k[1][1], k[1][2], k[1][3]) for k in keys if k[0] == 't' and k[1][0][0] == 'F'}
    for (s, lam, dl, d) in S:
        a = ('t', (s, lam, dl, d)); b = ('t', (s, lam, dl, d + 1))
        if a in rv and b in rv:
            fams[s[1]].append((a, b))
    print("[RI] F persistence pairs by j:", {k: len(v) for k, v in fams.items()}, flush=True)
    out = {}
    for j, pairs in sorted(fams.items()):
        rngs = []
        for (a, b) in pairs[:10]:
            c = np.zeros(A.shape[1]); c[rv[b]] = 1.0; c[rv[a]] = -1.0
            mn, mx = feas_wrap(A, r, c, pin)
            rngs.append([mn, mx])
        out[str(j)] = rngs
        print(f"    j={j}: {rngs}", flush=True)
    json.dump(out, open(OUT / "j4_rifoldF.json", "w"), indent=1, default=str)

def mode_bk():
    A, r, keys = load_red()
    rv = {k: i for i, k in enumerate(keys)}
    pin = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    out = []
    for d in range(0, 6):
        a = ('K', d); b = ('K', d + 2)
        if a not in rv or b not in rv:
            print(f"[RI] B_K({d}): K var missing", flush=True)
            out.append({"d": d, "status": "missing"})
            continue
        c = np.zeros(A.shape[1]); c[rv[b]] = 1.0; c[rv[a]] = -1.0
        mn, mx = feas_wrap(A, r, c, pin)
        print(f"[RI] B_K({d})=K_{d+2}-K_{d}: [{mn},{mx}]", flush=True)
        out.append({"d": d, "min": mn, "max": mx})
    json.dump(out, open(OUT / "j4_ribk.json", "w"), indent=1, default=str)

def mode_width():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import copy
    A, r, keys = load_red()
    E, V = A.shape
    rvmap = {k: i for i, k in enumerate(keys)}
    import importlib.util
    spec = importlib.util.spec_from_file_location('j4', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4 = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4)
    from wp6_staticR import depths_list, R_static
    from wp6_lambda import R_coeffs
    import wp6_cycle_ratio as O
    def shift(T, s):
        if T is None:
            return None
        return [T[0] + s, shift(T[1], s), shift(T[2], s)]
    def subsize(T, x):
        nd = T
        while nd is not None and nd[0] != x:
            nd = nd[1] if x < nd[0] else nd[2]
        c = [0]
        def go(m):
            if m is None:
                return
            c[0] += 1; go(m[1]); go(m[2])
        go(nd); return c[0]
    def H0(T, y, n, ka=4.0):
        return -R_static(T, y) + ka * (n - subsize(T, y))
    UGMAP = {}
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)
    for dl in (-5, -4):
        UGMAP[(('F', 5), 2, dl, 6)] = ((('F', 5), 1, dl, 6), 1.0)
    def Pform(B, y):
        """P_y linear form in reduced coords (NO extra consts: jbar twins equal
        structurally; UG/λ consts already live in system RHS)."""
        _, lam = R_coeffs(B, y)
        dB = depths_list(B)
        w = np.zeros(V)
        for z in dB:
            if z == y:
                continue
            t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
            if t in UGMAP:
                t = UGMAP[t][0]
            tt = ('t', t)
            if tt in rvmap:
                w[rvmap[tt]] += 1.0
        if dB[y] != 0:
            w[rvmap[('K', dB[y])]] += float(dB[y])
        return w, 0.0
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    ntest = npres = 0
    viols = []
    for t in (2, 3, 4):
        for T in O.shapes_of(list(range(1, t + 1))):
            for s in (0, 1, 2):
                Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                for S in Slist:
                    B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)] if S is not None else [0, None, copy.deepcopy(T)]
                    nB = t + 1 + s
                    for u in range(1, t + 1):
                        for v in range(u + 1, t + 1):
                            wTu, kTu = Pform(T, u); wTv, kTv = Pform(T, v)
                            wBu, kBu = Pform(B, u); wBv, kBv = Pform(B, v)
                            wT = wTu - wTv
                            wB = wBu - wBv
                            # H = 4G + P; G shifts row-common => Gamma via P only + verify
                            hT = (4 * (t - subsize(T, u)) + kTu) - (4 * (t - subsize(T, v)) + kTv)
                            hB = (4 * (nB - subsize(B, u)) + kBu) - (4 * (nB - subsize(B, v)) + kBv)
                            Aub = sp.vstack([-A, wT.reshape(1, -1), -wT.reshape(1, -1)]).tocsr()
                            bub = np.concatenate([-r, [2 - hT], [2 + hT]])
                            Aeq = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
                            beq = np.zeros(1)
                            r1 = linprog(-wB, A_ub=Aub, b_ub=bub, A_eq=Aeq, b_eq=beq,
                                         bounds=[(None, None)] * V, method="highs")
                            ntest += 1
                            if r1.status == 0:
                                mx = hB - float(r1.fun)
                                if mx <= 2 + 1e-6:
                                    npres += 1
                                elif len(viols) < 30:
                                    viols.append({"t": t, "s": s, "u": u, "v": v, "max": mx})
    print(f"[RI] reduced-coords width: {npres}/{ntest}", flush=True)
    json.dump({"pres": npres, "tot": ntest, "viols": viols}, open(OUT / "j4_riwidth.json", "w"), indent=1, default=str)

def main():
    modes = sys.argv[1:] or ["tbar"]
    if "tbar" in modes:
        mode_tbar()
    if "foldF" in modes:
        mode_foldF()
    if "bk" in modes:
        mode_bk()
    if "width" in modes:
        mode_width()
    print("[RI] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
