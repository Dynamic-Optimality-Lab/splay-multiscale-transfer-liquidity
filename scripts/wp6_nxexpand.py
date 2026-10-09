"""26N expansion: level-2 chain rows + joint shift-DTQ gate + frozen-witness test."""
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
    """J-row terms in SH567 reduced-var naming + UG-twin pre-map flag.
    Returns (terms, off) with terms over RAW J4 keys; caller maps."""
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
    import numpy as np
    from scipy.optimize import linprog
    import scipy.sparse as sp
    Z = np.load(OUT / "j4_rednorm_mat.npz")
    A0 = sp.csr_matrix(Z["A"])
    r0 = Z["rhs"].copy()
    keys0 = [eval(k) for k in Z["keys"]]
    E0, V0 = A0.shape
    rv0 = {k: i for i, k in enumerate(keys0)}
    # collect distinct level-2 trees across shift instances
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
    print(f"[NX] distinct level-2 trees: {len(trees)}", flush=True)
    # build rows: SELF (replay splay) + DIAMETER (all ordered pairs), in reduced coords
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    UGMAP = {}
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)
    newrows = []
    newrhs = []
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
    print(f"[NX] new rows: {len(newrows)}", flush=True)
    # map to reduced coords: UG twins->twin+const; NONE->K_d (counted); root->a*c.
    # First collect ALL raw keys (old + new rows) so twin detection is complete.
    allk = list(rv0.keys())
    for (terms, _) in newrows:
        for kk in terms:
            if kk not in rv0 and kk not in allk:
                allk.append(kk)
    # new UG twin pairs among extended vars (sibling-manifold coords)
    # STRICT=1: only manifold-proven pairs (gapdomain overlap + k=5 sib pairs)
    import os as _os  # noqa
    _strict = _os.environ.get("NXSTRICT", "0") == "1"
    _proven = set()
    for (k, dl, d) in dom["overlap"]:
        _proven.add((('F', k), 2, dl, d))
    for dl in (-5, -4):
        _proven.add((('F', 5), 2, dl, 6))
    xug = {}
    for kk in list(allk):
        if kk[0] == 't' and kk[1][1] == 2 and kk[1][0][0] == 'F' and kk[1][0][1] % 2 == 1:
            if _strict and kk[1] not in _proven:
                continue
            twin = ('t', (kk[1][0], 1, kk[1][2], kk[1][3]))
            if twin in allk:
                xug[kk] = twin
    _arf = _os.environ.get("NXARFREE", "0") == "1"
    _nomerge = _os.environ.get("NXNOMERGE", "0") == "1"
    print(f"[NX] strict={_strict} arfree={_arf} new UG twin pairs: {len(xug)}", flush=True)
    # single reduction pass
    redrows = []
    for (terms, rh) in newrows:
        row = {}
        off = 0.0
        for kk, cc in terms.items():
            if kk in xug:
                row[xug[kk]] = row.get(xug[kk], 0) + cc
                off += cc
            else:
                row[kk] = row.get(kk, 0) + cc
        row2 = {}
        rh2 = rh - off
        for kk, cc in row.items():
            if kk[0] == 'r':
                if _arf:
                    row2[kk] = row2.get(kk, 0) + cc
                else:
                    rh2 -= cc * kk[1]
            elif kk[0] == 't' and kk[1][0] == ('NONE',) and not _nomerge:
                kk2 = ('K', kk[1][3])
                row2[kk2] = row2.get(kk2, 0) + cc
            else:
                row2[kk] = row2.get(kk, 0) + cc
        redrows.append((row2, rh2))
        for kk in row2:
            if kk not in allk:
                allk.append(kk)
    xvmap = {k: i for i, k in enumerate(allk)}
    V2 = len(allk)
    rd, cd, vd, rext = [], [], [], list(r0)
    Ao = A0.tocoo()
    for i, j, v in zip(Ao.row, Ao.col, Ao.data):
        rd.append(int(i)); cd.append(xvmap[[k for k, ii in rv0.items() if ii == j][0]]); vd.append(float(v))
    for i, (row2, rh2) in enumerate(redrows):
        for kk, cc in row2.items():
            rd.append(E0 + i); cd.append(xvmap[kk]); vd.append(float(cc))
        rext.append(rh2)
    E1 = E0 + len(newrows)
    Aext = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E1, V2))
    rext = np.array(rext)
    print(f"[NX] extended E={E1} V={V2} (+{V2-V0} vars)", flush=True)
    t0 = [i for i, k in enumerate(allk) if k[0] == 't'][0]
    keep = [i for i in range(V2) if i != t0]
    Aub = sp.hstack([-Aext[:, keep], np.ones((E1, 1))]).tocsr()
    cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rext, bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[NX] expanded base feas: status={res.status} margin={margin}", flush=True)
    json.dump({"E1": E1, "V2": V2, "newrows": len(newrows), "status": res.status, "margin": margin},
              open(OUT / "j4_nxexpand.json", "w"), indent=1, default=str)
    if res.status == 0:
        g = np.zeros(V2); g[keep] = res.x[:len(keep)]
        drops = (Aext @ g) - rext
        print(f"[NX] viol={int((drops < -1e-7).sum())} newrows-viol={int((drops[E0:] < -1e-7).sum())}", flush=True)
    print("[NX] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
