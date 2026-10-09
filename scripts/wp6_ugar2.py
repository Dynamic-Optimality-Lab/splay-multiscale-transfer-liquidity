"""AR follow-ups: dual supports fixing a=1; width probe under UG+AR;
expanded twin rows under UG+AR.
Usage: python scripts/wp6_ugar2.py [acert|width|expand]
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
def build_ugmap():
    dom = json.load(open(OUT / "j4_gapdomain.json"))
    for (k, dl, d) in dom["overlap"]:
        UGMAP[(('F', k), 2, dl, d)] = ((('F', k), 1, dl, d), 1.0)
    for dl in (-5, -4):
        UGMAP[(('F', 5), 2, dl, 6)] = ((('F', 5), 1, dl, 6), 1.0)

def Jrow_form_AR(B, y):
    """J row linear form in UG+AR coords: returns (coefdict, acoef, const).
    coef over t-keys, acoef multiplies 'a', const = UG +1 per substituted twin."""
    _, lam = R_coeffs(B, y)
    dB = depths_list(B)
    coef = {}
    const = 0.0
    for z in dB:
        if z == y:
            continue
        t = (j4.slot_of(B, y, z), lam.get(z, 0), dB[z] - dB[y], dB[y])
        if t in UGMAP:
            t2, c = UGMAP[t]
            coef[('t', t2)] = coef.get(('t', t2), 0) + 1.0
            const += c
        else:
            coef[('t', t)] = coef.get(('t', t), 0) + 1.0
    c, _ = R_coeffs(B, y)
    return coef, c, const  # root contributes a*c

def load_ugar():
    Z = np.load(OUT / "j4_ugar_mat.npz")
    import scipy.sparse as sp
    A = sp.csr_matrix(Z["A"])
    r = Z["rhs"]
    keys = [eval(k) for k in Z["keys"]]
    return A, r, keys

def mode_acert():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    A, r, keys = load_ugar()
    E, V = A.shape
    rvmap = {k: i for i, k in enumerate(keys)}
    aidx = rvmap[('a',)]
    t0 = [i for i, k in enumerate(keys) if k[0] == 't'][0]
    Aeq = sp.csr_matrix(([1.0], ([0], [t0])), shape=(1, V))
    beq = np.zeros(1)
    # max a: min -a; get dual certificate via dual variables? use res.ineqlin marginals
    for sense, tag in ((1.0, "min_a"), (-1.0, "max_a")):
        c = np.zeros(V); c[aidx] = sense
        res = linprog(c, A_ub=-A, b_ub=-r, A_eq=Aeq, b_eq=beq, bounds=[(None, None)] * V,
                      method="highs", options={"disp": False})
        print(f"[UA] {tag}: obj={float(res.fun) if res.status==0 else None} st={res.status}", flush=True)
        if res.status == 0:
            # dual: marg = res.ineqlin.marginals (one per A_ub row): support of certificate
            try:
                marg = np.asarray(res.ineqlin.marginals).ravel()
                sup = np.where(np.abs(marg) > 1e-7)[0]
                print(f"[UA] {tag} support={len(sup)}", flush=True)
                # need metas: rebuild quickly? metas order = SH567 build order
                spec = importlib.util.spec_from_file_location('j4b', str(ROOT / 'scripts' / 'wp6_j4shared.py'))
                j4b = importlib.util.module_from_spec(spec); spec.loader.exec_module(j4b)
                raw, info = j4b.build_shared([5, 6, 7])
                A2, rhs2, metas, vmap = j4b.assemble(raw)
                for i in sup[np.argsort(-np.abs(marg[sup]))][:10]:
                    print(f"    m={float(marg[i]):+.3f} {metas[i][:7]} rhs={float(rhs2[i]):.1f}", flush=True)
            except Exception as e:
                print(f"[UA] marginals unavailable: {e}", flush=True)
    print("[UA] done acert", flush=True)

def mode_width():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    A, r, keys = load_ugar()
    E, V = A.shape
    rvmap = {k: i for i, k in enumerate(keys)}
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
                            def vec(BB, yy):
                                f, cc, kk0 = Jrow_form_AR(BB, yy)
                                w = np.zeros(V)
                                for kkk, c2 in f.items():
                                    if kkk in rvmap:
                                        w[rvmap[kkk]] += c2
                                w[rvmap[('a',)]] += cc
                                return w, kk0
                            wT, kT = vec(T, u); wTv, kTv = vec(T, v)
                            wB, kB = vec(B, u); wBv, kBv = vec(B, v)
                            wT = wT - wTv
                            wB = wB - wBv
                            hT = (H0(T, u, t) + kT) - (H0(T, v, t) + kTv)
                            hB = (H0(B, u, nB) + kB) - (H0(B, v, nB) + kBv)
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
    print(f"[UA] width under AR: {npres}/{ntest}", flush=True)
    for o in viols[:12]:
        print(f"    VIOL {o}", flush=True)
    json.dump({"pres": npres, "tot": ntest, "viols": viols}, open(OUT / "j4_uarwidth.json", "w"), indent=1, default=str)

def mode_expand():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    A, r, keys = load_ugar()
    E, V = A.shape
    rvmap = {k: i for i, k in enumerate(keys)}
    newrows = []; newrhs = []
    for (k, q) in ((5, 0), (5, 1)):
        for tag, fn in (("K2", tw.Twin2), ("K3", tw.Twin1)):
            B, T, S, y0, z0 = fn(k, q)
            n = len(depths_list(B))
            for x in depths_list(B):
                Bp = j4.V.replay(copy.deepcopy(B), copy.deepcopy(B), [("K", x)])["endB"]
                R = R_static(B, x); Rp = R_static(Bp, x)
                G = n - subsize(B, x); Gp = n - subsize(Bp, x)
                b = 1 if B[0] == x else 0
                D0 = R - 2 * (1 - b)
                s0 = ((-R + j4.KAPPA * G) - (-Rp + j4.KAPPA * Gp)) - D0
                fB, cB, kB = Jrow_form_AR(B, x)
                fP, cP, kP = Jrow_form_AR(Bp, x)
                terms = dict(fB)
                for kk, cc in fP.items():
                    terms[kk] = terms.get(kk, 0) - cc
                # root a-coef difference; UG const offsets:
                # (recompute const: Jrow_form_AR drops +1 consts! need them)
                newrows.append((terms, cB - cP)); newrhs.append(-s0 - (kB - kP))
            bB = B[0]
            for rr in depths_list(B):
                for x in depths_list(B):
                    if x == rr:
                        continue
                    Hr = H0(B, rr, n); Hx = H0(B, x, n)
                    br = 1 if bB == rr else 0; bx = 1 if bB == x else 0
                    Psi1 = -2 + 2 * (br - bx) - (Hr - Hx)
                    fr, cr, kr = Jrow_form_AR(B, rr)
                    fx, cx, kx = Jrow_form_AR(B, x)
                    terms = dict(fr)
                    for kk, cc in fx.items():
                        terms[kk] = terms.get(kk, 0) - cc
                    newrows.append((terms, cr - cx)); newrhs.append(Psi1 - (kr - kx))
    # NOTE: Jrow_form_AR dropped UG +1 consts and new-var handling; rows with
    # keys outside rvmap (new k=5 vars) need extension. Check coverage first:
    from scipy.optimize import linprog
    import scipy.sparse as sp
    # extend variable space: new t-vars + map ('r',c) already folded as acoef.
    # Build full extended matrix over xvmap = rvmap keys + new t-keys.
    allk = list(rvmap.keys())
    for (terms, _) in newrows:
        for kk in terms:
            if kk not in rvmap and kk not in allk and kk[0] == 't':
                allk.append(kk)
    # new UG twin pairs among extended vars
    xug = {}
    for kk in list(allk):
        if kk[0] == 't' and kk[1][1] == 2 and kk[1][0][0] == 'F' and kk[1][0][1] % 2 == 1:
            twin = ('t', (kk[1][0], 1, kk[1][2], kk[1][3]))
            if twin in allk:
                xug[kk] = twin
    xvmap = {k: i for i, k in enumerate(allk)}
    V2 = len(allk)
    E0 = A.shape[0]
    rd, cd, vd, rext = [], [], [], list(r)
    # old rows
    Ao = A.tocoo()
    for i, j, v in zip(Ao.row, Ao.col, Ao.data):
        rd.append(int(i)); cd.append(xvmap[[k for k, ii in rvmap.items() if ii == j][0]]); vd.append(float(v))
    for i, ((terms, ac), rh) in enumerate(zip(newrows, newrhs)):
        row = {}
        off = 0.0
        for kk, cc in terms.items():
            if kk in xug:
                row[xug[kk]] = row.get(xug[kk], 0) + cc
                off += cc
            elif kk in xvmap:
                row[kk] = row.get(kk, 0) + cc
            else:
                print(f"[UA] expand: UNMAPPED {kk}", flush=True)
        for kk, cc in row.items():
            rd.append(E0 + i); cd.append(xvmap[kk]); vd.append(float(cc))
        # a-coef + const: ac multiplies a; const already in rh? rh includes -(kB-kP);
        # a-term: append to a-column
        rd.append(E0 + i); cd.append(xvmap[('a',)]); vd.append(float(ac))
        rext.append(rh - off)
    E1 = E0 + len(newrows)
    Aext = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E1, V2))
    rext = np.array(rext)
    t0 = [i for i, k in enumerate(allk) if k[0] == 't'][0]
    keep2 = [i for i in range(V2) if i != t0]
    Aub = sp.hstack([-Aext[:, keep2], np.ones((E1, 1))]).tocsr()
    cobj = np.zeros(len(keep2) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rext, bounds=[(None, None)] * len(keep2) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[UA] expand UG+AR: E={E1} V={V2} status={res.status} margin={margin}", flush=True)
    nv = None
    if res.status == 0:
        g = np.zeros(V2); g[keep2] = res.x[:len(keep2)]
        drops = (Aext @ g) - rext
        nv = int((drops[E0:] < -1e-7).sum())
        print(f"[UA] newrows-viol={nv} minslack={float(drops.min()):.3e}", flush=True)
    json.dump({"E1": E1, "V2": V2, "newrows": len(newrows), "status": res.status,
               "margin": margin, "newviol": nv},
              open(OUT / "j4_uarexpand.json", "w"), indent=1, default=str)

def main():
    modes = sys.argv[1:] or ["acert"]
    build_ugmap()
    if "acert" in modes:
        mode_acert()
    if "width" in modes:
        mode_width()
    if "expand" in modes:
        mode_expand()
    return 0

if __name__ == "__main__":
    sys.exit(main())
