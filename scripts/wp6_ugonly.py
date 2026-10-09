"""Decisive: chain-row expansion under UG-ONLY (root tokens free, no AR).
Reuses rednorm-equivalent UG system built fresh with roots kept.
Usage: python scripts/wp6_ugonly.py
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
vl = load('wp6_validlift')
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

def lift2_spaced(T):
    mx = max(depths_list(T).keys())
    return [mx + 6, [mx + 3, copy.deepcopy(T), None], None]

def Jrow(B, y):
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    terms = {}
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        terms[('t', t)] = terms.get(('t', t), 0) + 1.0
    c, _ = R_coeffs(B, y)
    terms[('r', c)] = terms.get(('r', c), 0) + 1.0
    return terms

def main():
    import scipy.sparse as sp
    from scipy.optimize import linprog
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs0, metas0, vmap = j4b.assemble(raw)
    E0, V0 = A2.shape
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    pairs = []
    for (k, dl, d) in dom["overlap"]:
        pairs.append((vmap[('t', (('F', k), 2, dl, d))], vmap[('t', (('F', k), 1, dl, d))]))
    A = A2.tolil()
    r = rhs0.copy()
    for (e, k) in pairs:
        col = A[:, e].toarray().ravel()
        A[:, k] = A[:, k].toarray().ravel() + col
        r = r - col
    elim = {e for (e, k) in pairs}
    keep = [i for i in range(V0) if i not in elim]
    inv = {i: kk for kk, i in vmap.items()}
    basekeys = [inv[i] for i in keep]
    Abase = A[:, keep].tocsr()
    print(f"[UO] UG-only base E={E0} V={len(basekeys)} (roots kept)", flush=True)
    # chain trees level-2 only (same 15 trees)
    trees = {}
    for T in O.shapes_of([1, 2, 3]):
        Tr = vl.relabel(copy.deepcopy(T), lambda x: 10 * x)
        p = 100
        for s in (0, 1):
            Sr = None if s == 0 else vl.relabel(O.shapes_of([1])[0], lambda x: 10 * x + 500)
            T1 = lift2_spaced(Tr)
            T2 = lift2_spaced(T1)
            B2 = [p, copy.deepcopy(T2), copy.deepcopy(Sr)] if Sr is not None else [0, None, copy.deepcopy(T2)]
            for BB, tag in ((T2, "T2"), (B2, "B2")):
                vl.assert_valid_bst(BB)
                trees[json.dumps(BB, sort_keys=True)] = BB
    newrows = []
    for key, B in trees.items():
        n = len(depths_list(B))
        for x in depths_list(B):
            Bp = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
            R = R_static(B, x)
            Rp = R_static(Bp, x)
            G = n - subsize(B, x)
            Gp = n - subsize(Bp, x)
            b = 1 if B[0] == x else 0
            D0 = R - 2 * (1 - b)
            s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
            tB = Jrow(B, x)
            tP = Jrow(Bp, x)
            terms = dict(tB)
            for kk, cc in tP.items():
                terms[kk] = terms.get(kk, 0) - cc
            newrows.append((terms, -s0))
        bB = B[0]
        for rr in depths_list(B):
            for x in depths_list(B):
                if x == rr:
                    continue
                Hr = H0(B, rr, n)
                Hx = H0(B, x, n)
                br = 1 if bB == rr else 0
                bx = 1 if bB == x else 0
                Psi1 = -2 + 2 * (br - bx) - (Hr - Hx)
                tr = Jrow(B, rr)
                tx = Jrow(B, x)
                terms = dict(tr)
                for kk, cc in tx.items():
                    terms[kk] = terms.get(kk, 0) - cc
                newrows.append((terms, Psi1))
    print(f"[UO] new rows: {len(newrows)} (roots FREE, strict: no new twin mapping)", flush=True)
    allk = list(basekeys)
    for (terms, _) in newrows:
        for kk in terms:
            if kk not in allk:
                # strict: do NOT map new twins; keep free (except NONE? keep raw too)
                allk.append(kk)
    xvmap = {k: i for i, k in enumerate(allk)}
    V2 = len(allk)
    invbase = {i: k for i, k in enumerate(basekeys)}
    rd, cd, vd, rext = [], [], [], list(r)
    Ao = Abase.tocoo()
    for i, j, v in zip(Ao.row, Ao.col, Ao.data):
        rd.append(int(i)); cd.append(xvmap[invbase[int(j)]]); vd.append(float(v))
    for i, (terms, rh) in enumerate(newrows):
        for kk, cc in terms.items():
            rd.append(E0 + i); cd.append(xvmap[kk]); vd.append(float(cc))
        rext.append(rh)
    E1 = E0 + len(newrows)
    Aext = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E1, V2))
    rext = np.array(rext)
    print(f"[UO] extended E={E1} V={V2}", flush=True)
    t0 = [i for i, k in enumerate(allk) if k[0] == 't'][0]
    r0 = [i for i, k in enumerate(allk) if k[0] == 'r'][0]
    keep2 = [i for i in range(V2) if i not in (t0, r0)]
    Aub = sp.hstack([-Aext[:, keep2], np.ones((E1, 1))]).tocsr()
    cobj = np.zeros(len(keep2) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rext, bounds=[(None, None)] * len(keep2) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[UO] UG-only expanded feas: status={res.status} margin={margin}", flush=True)
    if res.status == 0:
        g = np.zeros(V2); g[keep2] = res.x[:len(keep2)]
        drops = (Aext @ g) - rext
        print(f"[UO] viol={int((drops < -1e-7).sum())} newrows-viol={int((drops[E0:] < -1e-7).sum())}", flush=True)
    json.dump({"E1": E1, "V2": V2, "status": res.status, "margin": margin},
              open(OUT / "j4_ugonly.json", "w"), indent=1, default=str)
    print("[UO] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
