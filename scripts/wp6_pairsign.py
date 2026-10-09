"""Pair-level L/R sign audit: exact pair Cbar_LR sup over reduced LP on Lift2
instances (base n<=5 so lifted rows stay in SH567); falsification search;
C_rem joint sup on same instances.
Usage: python scripts/wp6_pairsign.py [pairs|crem]
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

def shift(T, s):
    if T is None:
        return None
    return [T[0] + s, shift(T[1], s), shift(T[2], s)]

def row_jbar_atoms(B, y):
    """Non-NONE jbar atom multiset of row y (reduced keys)."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    ms = defaultdict(int)
    for z in dB:
        if z == y:
            continue
        s_ = j4.slot_of(B, y, z)
        if s_[0] == 'NONE':
            continue
        ms[('t', (s_, lam.get(z, 0), dB[z] - dB[y], dB[y]))] += 1
    return ms

def lift2_pair_instance(T, S, u, v):
    """Build (B,T) and (B2,T2) rows; return L/R-atom pair-Cbar form + full info.
    Lift2 = double-pad above T-root: T2=[0,None,[-1,None,T]] (keys preserved).
    B=Ext(T,S) with T left child; B2=Ext(T2,S)."""
    t = len(depths_list(T))
    s = 0 if S is None else len(depths_list(S))
    if S is None:
        B = [0, None, copy.deepcopy(T)]
    else:
        B = [t + 1, copy.deepcopy(T), shift(copy.deepcopy(S), t + 1)]
    T2 = [0, None, [-1, None, copy.deepcopy(T)]]
    if S is None:
        B2 = [0, None, copy.deepcopy(T2)]
    else:
        # shift S above new keys: T2 uses keys of T plus {0,-1}; S shifted accordingly
        B2 = [t + 1, copy.deepcopy(T2), shift(copy.deepcopy(S), t + 1)]
    return (B, T, B2, T2)

def pair_cbar_form(B, T, B2, T2, u, v):
    """L/R-only part of Dbar-relevant pair combination, split by slot class.
    Returns (form_dict, info). Form = [u(B2)-v(B2)] - [u(T2)-v(T2)] - [u(B)-v(B)] + [u(T)-v(T)]
    restricted to L/R atoms (jbar keys)."""
    states = [(B2, u, 1), (B2, v, -1), (T2, u, -1), (T2, v, 1),
              (B, u, -1), (B, v, 1), (T, u, 1), (T, v, -1)]
    form = defaultdict(float)
    detail = []
    for (BB, yy, sgn) in states:
        ms = row_jbar_atoms(BB, yy)
        for kk, cc in ms.items():
            if kk[1][0] in (('L',), ('R',)):
                form[kk] += sgn * cc
                detail.append((str(kk), sgn * cc))
    form = {k: v for k, v in form.items() if abs(v) > 1e-12}
    return form

def main():
    modes = sys.argv[1:] or ["pairs"]
    import scipy.sparse as sp
    from scipy.optimize import linprog
    Z = np.load(OUT / "j4_rednorm_mat.npz")
    A = sp.csr_matrix(Z["A"]); r = Z["rhs"].copy()
    keys = [eval(k) for k in Z["keys"]]
    E, V = A.shape
    rv = {k: i for i, k in enumerate(keys)}
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    Aeq0 = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
    beq0 = np.zeros(1)
    def sup_of(form):
        c = np.zeros(V)
        miss = 0
        for kk, cc in form.items():
            if kk in rv:
                c[rv[kk]] += cc
            else:
                miss += 1
        if miss:
            return None, f"missing-{miss}"
        res = linprog(-c, A_ub=-A, b_ub=-r, A_eq=Aeq0, b_eq=beq0,
                      bounds=[(None, None)] * V, method="highs")
        if res.status != 0:
            return None, f"st{res.status}"
        return float(-res.fun), "ok"
    if "pairs" in modes:
        results = []
        npos = ntot = 0
        worst = None
        for t in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1))):
                for s in (0, 1, 2):
                    if t + 1 + s > 5:
                        continue
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                    for S in Slist:
                        for u in range(1, t + 1):
                            for v in range(u + 1, t + 1):
                                B, T_, B2, T2 = lift2_pair_instance(T, S, u, v)
                                # sanity: lifted sizes fit SH567 (n<=7)
                                if len(depths_list(B2)) > 7:
                                    continue
                                form = pair_cbar_form(B, T_, B2, T2, u, v)
                                if not form:
                                    continue
                                ntot += 1
                                val, st = sup_of(form)
                                if val is not None and val > 1e-6:
                                    npos += 1
                                    if worst is None or val > worst[0]:
                                        worst = (val, t, s, u, v)
                                results.append({"t": t, "s": s, "u": u, "v": v, "sup": val, "st": st,
                                                "nterms": len(form)})
        print(f"[PS] pair-level Cbar_LR sup>0: {npos}/{ntot} worst={worst}", flush=True)
        # distribution of sups
        import collections as _c
        hist = _c.Counter(round(x["sup"], 1) if x["sup"] is not None else None for x in results)
        print("[PS] sup histogram:", dict(sorted((str(k), v) for k, v in hist.items())), flush=True)
        json.dump({"npos": npos, "ntot": ntot, "worst": worst,
                   "detail": [x for x in results if x["sup"] is not None and x["sup"] > 1e-6][:15]},
                  open(OUT / "j4_pairsign.json", "w"), indent=1, default=str)
    if "crem" in modes:
        # C_rem joint sup on same instances: full Dbar L/R+F+sib/K parts as ONE form.
        # Full Dbar form = 8-state signed FULL P-rows (jbar+K). K_d needs multiplicity.
        results = []
        npos = ntot = 0
        worst = None
        for t in (2, 3):
            for T in O.shapes_of(list(range(1, t + 1)))[:10]:
                for s in (0, 1):
                    if t + 1 + s > 5:
                        continue
                    Slist = [None] if s == 0 else O.shapes_of(list(range(1, s + 1)))
                    for S in Slist:
                        for u in range(1, t + 1):
                            for v in range(u + 1, t + 1):
                                B, T_, B2, T2 = lift2_pair_instance(T, S, u, v)
                                if len(depths_list(B2)) > 7:
                                    continue
                                states = [(B2, u, 1), (B2, v, -1), (T2, u, -1), (T2, v, 1),
                                          (B, u, -1), (B, v, 1), (T, u, 1), (T, v, -1)]
                                form = defaultdict(float)
                                for (BB, yy, sgn) in states:
                                    _, lam = R_coeffs(BB, yy)
                                    dB = depths_list(BB)
                                    for z in dB:
                                        if z == yy:
                                            continue
                                        tt = (j4.slot_of(BB, yy, z), lam.get(z, 0), dB[z] - dB[yy], dB[yy])
                                        if tt[0] == ('NONE',):
                                            continue
                                        form[('t', tt)] += sgn
                                    if dB[yy] != 0:
                                        form[('K', dB[yy])] += sgn * float(dB[yy])
                                form = {k: v for k, v in form.items() if abs(v) > 1e-12}
                                ntot += 1
                                val, st = sup_of(form)
                                if val is not None and abs(val) > 1e-6:
                                    npos += 1
                                    if worst is None or abs(val) > abs(worst[0]):
                                        worst = (val, t, s, u, v, len(form))
                                results.append({"t": t, "s": s, "u": u, "v": v, "sup": val, "nt": len(form)})
        print(f"[PS] full-Dbar-form nonzero sup: {npos}/{ntot} worst={worst}", flush=True)
        json.dump({"npos": npos, "ntot": ntot, "worst": worst},
                  open(OUT / "j4_crem.json", "w"), indent=1, default=str)
    print("[PS] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
