"""Expanded UG gate: twin-context SELF+DIAMETER rows at n=8,9 (k=5 twins)
appended to UG-reduced SH567 system; feasibility = expanded compat.
Usage: python scripts/wp6_ugexpand.py
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
tw = load('wp6_twins')
from wp6_staticR import depths_list, R_static
from wp6_lambda import R_coeffs

UGMAP = {}  # (F_k,2,dl,d) -> ((F_k,1,dl,d), +1)

def build_ugmap():
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)

def Jrow_terms(B, y):
    """Return (terms dict, ) for J_y(B) in REDUCED vars + const offset from UG."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    terms = {}
    off = 0.0
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        if t in UGMAP:
            t2, c = UGMAP[t]
            terms[('t', t2)] = terms.get(('t', t2), 0) + 1.0
            off += c
        else:
            terms[('t', t)] = terms.get(('t', t), 0) + 1.0
    c, _ = R_coeffs(B, y)
    terms[('r', c)] = terms.get(('r', c), 0) + 1.0
    return terms, off

def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    build_ugmap()
    Z = np.load(OUT / "j4_sh567_A.npz")
    A0 = sp.csr_matrix(Z["A"].astype(float))
    import importlib.util as iu
    spec = iu.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
    j4b = iu.module_from_spec(spec); spec.loader.exec_module(j4b)
    raw, info = j4b.build_shared([5, 6, 7])
    A2, rhs0, metas0, vmap = j4b.assemble(raw)
    # UG reduction (same as wp6_ugreduce)
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    pairs = []
    for (k, dl, d) in dom["overlap"]:
        key1 = ('t', (('F', k), 1, dl, d)); key2 = ('t', (('F', k), 2, dl, d))
        pairs.append((vmap[key2], vmap[key1]))
    A = A0.tolil(); r = rhs0.copy()
    elim = [e for (e, k) in pairs]
    for (e, k) in pairs:
        col = A[:, e].toarray().ravel()
        A[:, k] = A[:, k].toarray().ravel() + col
        r = r - col
    keep = [i for i in range(A.shape[1]) if i not in set(elim)]
    Ared = A[:, keep].tocsr()
    inv = {i: kk for kk, i in vmap.items()}
    # vmap for reduced: key->newidx
    rvmap = {}
    for new, old in enumerate(keep):
        rvmap[inv[old]] = new
    newrows = []; newrhs = []
    # twin contexts k=5, q=0 (n=8), q=1 (n=9)
    for (k, q) in ((5, 0), (5, 1)):
        for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
            B, T, S, y0, z0 = fn(k, q)
            n = len(depths_list(B))
            # SELF rows: all x
            for x in depths_list(B):
                Bp = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
                R = R_static(B, x); Rp = R_static(Bp, x)
                G = n - j4.subsize(B, x); Gp = n - j4.subsize(Bp, x)
                b = 1 if B[0] == x else 0
                D0 = R - 2 * (1 - b)
                s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                tB, oB = Jrow_terms(B, x)
                tP, oP = Jrow_terms(Bp, x)
                terms = dict(tB)
                for kk, cc in tP.items():
                    terms[kk] = terms.get(kk, 0) - cc
                newrows.append(terms); newrhs.append(-s0 - (oB - oP))
            # DIAMETER rows: all ordered r!=x
            bB = B[0]
            for rr in depths_list(B):
                for x in depths_list(B):
                    if x == rr:
                        continue
                    Hr = j4.H0(B, rr, n); Hx = j4.H0(B, x, n)
                    br = 1 if bB == rr else 0; bx = 1 if bB == x else 0
                    Psi1 = -2 + 2 * (br - bx) - (Hr - Hx)
                    tr, oor = Jrow_terms(B, rr)
                    tx, oox = Jrow_terms(B, x)
                    terms = dict(tr)
                    for kk, cc in tx.items():
                        terms[kk] = terms.get(kk, 0) - cc
                    newrows.append(terms); newrhs.append(Psi1 - (oor - oox))
            print(f"[UX] twin {tag} k={k} q={q}: n={n} rows={len([rr for rr in depths_list(B)])} "
                  f"self+ diam added (total new={len(newrows)})", flush=True)
    # assemble extended WITH new variables (plus UG twin substitution for new pairs)
    # new UG pairs among new vars: (F_5,2,-5,6)->(F_5,1,-5,6)+1, (F_5,2,-4,6)->(F_5,1,-4,6)+1
    newpairs = [(('t', (('F', 5), 2, -5, 6)), ('t', (('F', 5), 1, -5, 6))),
                (('t', (('F', 5), 2, -4, 6)), ('t', (('F', 5), 1, -4, 6)))]
    npmap = {e: k for (e, k) in newpairs}
    allkeys = list(rvmap.keys())
    for kk, cc in [t for terms in newrows for t in terms.items()]:
        if kk not in rvmap and kk not in npmap and kk not in allkeys:
            allkeys.append(kk)
    for (e, k) in newpairs:
        if k not in allkeys:
            allkeys.append(k)
    xvmap = {k: i for i, k in enumerate(allkeys)}
    V2 = len(allkeys)
    E0 = Ared.shape[0]
    rd, cd, vd = [], [], []
    # old rows in extended columns
    Ao = Ared.tocoo()
    for i, j, v in zip(Ao.row, Ao.col, Ao.data):
        rd.append(int(i)); cd.append(xvmap[[k for k, ii in rvmap.items() if ii == j][0]]); vd.append(float(v))
    rextra = list(r)
    for i, terms in enumerate(newrows):
        row = {}
        off_extra = 0.0
        for kk, cc in terms.items():
            if kk in npmap:
                k2 = npmap[kk]
                row[k2] = row.get(k2, 0) + cc
                off_extra += cc  # x_e = x_k + 1
            else:
                row[kk] = row.get(kk, 0) + cc
        for kk, cc in row.items():
            rd.append(E0 + i); cd.append(xvmap[kk]); vd.append(float(cc))
        rextra.append(newrhs[i] - off_extra)
    E1 = E0 + len(newrows)
    V2 = len(allkeys)
    Aext = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E1, V2))
    rext = np.array(rextra)
    # NOTE: rows referencing vars outside SH567 are dropped above (reported); check count
    print(f"[UX] extended E={E1} V={V2} newrows={len(newrows)} newvars={V2 - len(rvmap)}", flush=True)
    # feasibility with gauge pins (2)
    allk = list(xvmap.keys())
    tk = [k for k in allk if k[0] == 't'][0]; rk = [k for k in allk if k[0] == 'r'][0]
    keep2 = [i for k, i in xvmap.items() if k != tk and k != rk]
    Aub = sp.hstack([-Aext[:, keep2], np.ones((E1, 1))]).tocsr()
    cobj = np.zeros(len(keep2) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rext, bounds=[(None, None)] * len(keep2) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[UX] expanded feas status={res.status} margin={margin}", flush=True)
    if res.status == 0:
        g = np.zeros(V2); g[keep2] = res.x[:len(keep2)]
        drops = (Aext @ g) - rext
        nviol = int((drops < -1e-7).sum())
        print(f"[UX] viol={nviol} minslack={float(drops.min()):.3e} newrows-viol={int((drops[E0:] < -1e-7).sum())}", flush=True)
    json.dump({"E1": E1, "V2": V2, "newrows": len(newrows), "status": res.status, "margin": margin,
               "newviol": int((drops[E0:] < -1e-7).sum()) if res.status == 0 else None},
              open(OUT / "j4_ugexpand.json", "w"), indent=1, default=str)
    print("[UX] saved", flush=True)
    return 0

if __name__ == "__main__":
    sys.exit(main())
