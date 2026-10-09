"""Clean expansion: UG-only base + chain rows (proven green path), then impose
quotient/UG/AR as explicit EQUALITIES. Single assembly, no edit drift.
Usage: python scripts/wp6_xclean.py [base|ug|ar|all]
 modes add equality sets cumulatively; reports margin each stage.
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

def build_base():
    import scipy.sparse as sp
    spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs0, metas0, vmap = j4b.assemble(raw)
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
    keep = [i for i in range(A.shape[1]) if i not in elim]
    inv = {i: kk for kk, i in vmap.items()}
    keys = [inv[i] for i in keep]
    return A[:, keep].tocsr(), np.array(r), keys

def build_chain_rows():
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
    return newrows

def main():
    modes = sys.argv[1:] or ["base"]
    import scipy.sparse as sp
    from scipy.optimize import linprog
    Abase, rbase, basekeys = build_base()
    E0, V0 = Abase.shape
    print(f"[XC] base E={E0} V={V0}", flush=True)
    newrows = build_chain_rows()
    print(f"[XC] chain rows: {len(newrows)}", flush=True)
    # assemble extended with raw keys (no mapping)
    allk = list(basekeys)
    for (terms, _) in newrows:
        for kk in terms:
            if kk not in allk:
                allk.append(kk)
    # optional new twin pairs (proven manifold only)
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    proven = set()
    for (k, dl, d) in dom["overlap"]:
        proven.add((('F', k), 2, dl, d))
    for dl in (-5, -4):
        proven.add((('F', 5), 2, dl, 6))
    xug = {}
    for kk in list(allk):
        if kk[0] == 't' and kk[1][1] == 2 and kk[1][0][0] == 'F' and kk[1][0][1] % 2 == 1 and kk[1] in proven:
            twin = ('t', (kk[1][0], 1, kk[1][2], kk[1][3]))
            if twin in allk:
                xug[kk] = twin
    print(f"[XC] proven new twin pairs: {len(xug)}", flush=True)
    # equalities per mode
    EQ = []  # (dict key->coef, rhs)
    if "ug" in modes or "all" in modes:
        for kk, tw2 in xug.items():
            EQ.append(({kk: 1.0, tw2: -1.0}, 1.0))
    if "ar" in modes or "all" in modes:
        # AR as equalities: rho(c)-a*c-b=0 for each realized c + b=0 gauge... need a,b vars.
        # Instead: pairwise Delta2=0? NO -- AR means affine; impose via (a,b) vars:
        pass
    xvmap = {k: i for i, k in enumerate(allk)}
    V2 = len(allk)
    rd, cd, vd, rext = [], [], [], list(rbase)
    Ao = Abase.tocoo()
    invb = {i: k for i, k in enumerate(basekeys)}
    for i, j, v in zip(Ao.row, Ao.col, Ao.data):
        rd.append(int(i)); cd.append(xvmap[invb[int(j)]]); vd.append(float(v))
    for i, (terms, rh) in enumerate(newrows):
        row = {}
        off = 0.0
        for kk, cc in terms.items():
            if kk in xug and ("ug" in modes or "all" in modes):
                row[xug[kk]] = row.get(xug[kk], 0) + cc
                off += cc
            else:
                row[kk] = row.get(kk, 0) + cc
        for kk, cc in row.items():
            rd.append(E0 + i); cd.append(xvmap[kk]); vd.append(float(cc))
        rext.append(rh - off)
    E1 = E0 + len(newrows)
    Aext = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E1, V2))
    rext = np.array(rext)
    print(f"[XC] modes={modes} E={E1} V={V2}", flush=True)
    t0 = [i for i, k in enumerate(allk) if k[0] == 't'][0]
    keep = [i for i in range(V2) if i != t0]
    Aub = sp.hstack([-Aext[:, keep], np.ones((E1, 1))]).tocsr()
    cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
    kw = {}
    if "ar" in modes or "all" in modes:
        # AR equalities: rho(c) - a*c = 0 for each realized c (b=0 gauge).
        # Implement by SUBSTITUTION (cleaner than A_eq with extra var):
        # add ('a',) column with entries c per root-token occurrence is wrong
        # (tokens have coef +-1 per row). Correct: replace each root var column
        # col_c by c * [new a-column]? That forces rho(c)=a*c exactly. Do:
        # Anew = A with all root cols REMOVED and single a-col = sum_c c*col_c.
        rcols = [i for i, k in enumerate(allk) if k[0] == 'r']
        acol = np.zeros(E1)
        for i in rcols:
            acol += np.asarray(Aext[:, i].toarray()).ravel() * allk[i][1]
        tcols = [i for i in range(V2) if i not in set(rcols)]
        Aext = sp.hstack([Aext[:, tcols], sp.csr_matrix(acol).T]).tocsr()
        allk = [allk[i] for i in tcols] + [('a',)]
        V2 = len(allk)
        keep = [i for i in range(V2) if allk[i] != [k for k in allk if k[0] == 't'][0]]
        Aub = sp.hstack([-Aext[:, keep], np.ones((E1, 1))]).tocsr()
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        print(f"[XC] AR-substituted V={V2}", flush=True)
    res = linprog(cobj, A_ub=Aub, b_ub=-rext, bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[XC] feas: status={res.status} margin={margin}", flush=True)
    if res.status == 0:
        g = np.zeros(V2); g[keep] = res.x[:len(keep)]
        drops = (Aext @ g) - rext
        print(f"[XC] viol={int((drops < -1e-7).sum())} newrows-viol={int((drops[E0:] < -1e-7).sum())}", flush=True)
        np.savez_compressed(OUT / "j4_xclean_mat.npz", A=Aext.toarray(), rhs=rext,
                            keys=np.array([str(k) for k in allk]),
                            E0=np.array([E0]), wit=res.x[:len(keep)] if False else np.zeros(0))
        print("[XC] matrix saved", flush=True)
    json.dump({"E1": E1, "V2": V2, "status": res.status, "margin": margin},
              open(OUT / "j4_xclean.json", "w"), indent=1, default=str)
    print("[XC] done", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
