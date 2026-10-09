"""J3 clean two-phase generator: tau=(slot,lambda,delta), root=c.
Phase 1: symbolic raw.append((terms,rhs,meta)). Phase 2: fixed vmap, A J>=rhs.
Usage: python scripts/wp6_j3clean.py <n> [feas|l1|farkas]
"""
import sys, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs

KAPPA = 4.0

def subkeys_list(t, x):
    nd = t
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    out = []
    def go(m):
        if m is None:
            return
        out.append(m[0])
        go(m[1])
        go(m[2])
    go(nd)
    return frozenset(out)

def slot_of(T, y, z):
    P = path_nodes(T, y)
    d = len(P) - 1
    if z == y:
        return ('SELF',)
    xn = P[d]
    Lset = set(subkeys_list(T, xn[1][0])) if xn[1] else set()
    Rset = set(subkeys_list(T, xn[2][0])) if xn[2] else set()
    if z in Lset:
        return ('L',)
    if z in Rset:
        return ('R',)
    for j in range(d):
        par = P[d - 1 - j]
        ch = P[d - j]
        off = par[2] if par[1] is ch else par[1]
        mset = set()
        if off is not None:
            mset = set(subkeys_list(T, off[0]))
        if z in mset:
            return ('F', j)
    return ('NONE',)

def subsize(T, x):
    nd = T
    while nd is not None and nd[0] != x:
        nd = nd[1] if x < nd[0] else nd[2]
    c = [0]
    def go(m):
        if m is None:
            return
        c[0] += 1
        go(m[1])
        go(m[2])
    go(nd)
    return c[0]

def H0(T, y, n, ka=KAPPA):
    return -R_static(T, y) + ka * (n - subsize(T, y))

def tau_of(T, y, z, lam):
    s = slot_of(T, y, z)
    dd = depths_list(T)
    return (s, lam, dd[z] - dd[y])

def build(n):
    import wp6_cycle_ratio as O
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    rep_cache = {}
    def rep(ia, ib, x, mode="K"):
        k = (ia, ib, x, mode)
        if k not in rep_cache:
            rep_cache[k] = V.replay(Sh[ia], Sh[ib], [(mode, x)])
        return rep_cache[k]
    lam_cache = {}
    def lamrows(ti):
        if ti not in lam_cache:
            lam_cache[ti] = {y: R_coeffs(Sh[ti], y) for y in range(1, n + 1)}
        return lam_cache[ti]
    raw = []
    # J-SELF
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            da0 = depths_list(A)
            for y in range(1, n + 1):
                if da0[y] != 0:
                    continue
                r = rep(ia, ib, y)
                Bp = r["endB"]
                jb = idx[json.dumps(Bp, sort_keys=True)]
                R = R_static(B, y)
                Rp = R_static(Bp, y)
                G = n - subsize(B, y)
                Gp = n - subsize(Bp, y)
                b = 1 if B[0] == y else 0
                D0 = R - 2 * (1 - b)
                s0 = ((-R + KAPPA * G) - (-Rp + KAPPA * Gp)) - D0
                terms = {}
                _, l0 = lamrows(ib)[y]
                _, l1 = lamrows(jb)[y]
                for z in range(1, n + 1):
                    if z == y:
                        continue
                    u = tau_of(B, y, z, l0.get(z, 0))
                    v = tau_of(Bp, y, z, l1.get(z, 0))
                    if u != v:
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                        terms[('t', v)] = terms.get(('t', v), 0) - 1.0
                c0, _ = lamrows(ib)[y]
                c1, _ = lamrows(jb)[y]
                terms[('r', c0)] = terms.get(('r', c0), 0) + 1.0
                terms[('r', c1)] = terms.get(('r', c1), 0) - 1.0
                raw.append((terms, -s0, ('SELF', ia, ib, y, -s0)))
    nself = len(raw)
    # J-SWITCH
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            rA = A[0]
            daA = depths_list(A)
            br = 1 if B[0] == rA else 0
            Hr = H0(B, rA, n)
            for x in range(1, n + 1):
                a = (daA[x] + 1) // 2
                bx = 1 if B[0] == x else 0
                Dd = -2 * a - 2 * (bx - br)
                Hx = H0(B, x, n)
                Psi = Dd - (Hr - Hx)
                terms = {}
                _, lamr = R_coeffs(B, rA)
                _, lamx = R_coeffs(B, x)
                for z in range(1, n + 1):
                    if z != rA:
                        u = tau_of(B, rA, z, lamr.get(z, 0))
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                    if z != x:
                        u = tau_of(B, x, z, lamx.get(z, 0))
                        terms[('t', u)] = terms.get(('t', u), 0) - 1.0
                cr, _ = R_coeffs(B, rA)
                cx, _ = R_coeffs(B, x)
                terms[('r', cr)] = terms.get(('r', cr), 0) + 1.0
                terms[('r', cx)] = terms.get(('r', cx), 0) - 1.0
                raw.append((terms, Psi, ('SWITCH', ia, ib, rA, x, Psi)))
    return raw, Sh

def assemble(raw):
    import scipy.sparse as sp
    vmap = {}
    for (terms, _, _) in raw:
        for k in terms:
            if k not in vmap:
                vmap[k] = len(vmap)
    Vv = len(vmap)
    E = len(raw)
    rd, cd, vd, rhs, metas = [], [], [], [], []
    for i, (terms, rh, meta) in enumerate(raw):
        for k, c in terms.items():
            rd.append(i)
            cd.append(vmap[k])
            vd.append(float(c))
        rhs.append(float(rh))
        metas.append(meta)
    Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E, Vv))
    return Amat, np.array(rhs), metas, vmap

def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    mode = sys.argv[2] if len(sys.argv) > 2 else "feas"
    raw, Sh = build(n)
    Amat, rhs, metas, vmap = assemble(raw)
    Vv = len(vmap); E = len(raw)
    inv = {i: k for k, i in vmap.items()}
    is_t = np.array([1.0 if inv[i][0] == 't' else 0.0 for i in range(Vv)])
    is_r = np.array([1.0 if inv[i][0] == 'r' else 0.0 for i in range(Vv)])
    at = float(np.abs(Amat @ is_t).max()) if E else 0.0
    ar = float(np.abs(Amat @ is_r).max()) if E else 0.0
    print(f"[J3] n={n} E={E} V={Vv} A*1t={at} A*1r={ar}", flush=True)
    # rank via dense (V small)
    try:
        rnk = int(np.linalg.matrix_rank(Amat.toarray()))
    except Exception as e:
        rnk = None
        print(f"[J3] rank failed: {e}", flush=True)
    print(f"[J3] rank={rnk}", flush=True)
    tkeys = [k for k in vmap if k[0] == 't']
    rkeys = [k for k in vmap if k[0] == 'r']
    gfix = [tkeys[0], rkeys[0]] if tkeys and rkeys else []
    keep = [i for k, i in vmap.items() if k not in set(gfix)]
    print(f"[J3] gauge fix {gfix} keep={len(keep)}", flush=True)
    Ared = Amat[:, keep]
    if mode == "feas":
        Aub = sp.hstack([-Ared, np.ones((E, 1))]).tocsr()
        bub = -rhs
        cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
        res = linprog(cobj, A_ub=Aub, b_ub=bub,
                      bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
        margin = float(-res.fun) if res.status == 0 else None
        print(f"[J3] feas status={res.status} margin={margin}", flush=True)
        out = {"n": n, "E": E, "V": Vv, "rank": rnk, "lineality_t": at, "lineality_r": ar,
               "gauge": [str(g) for g in gfix], "status": res.status, "margin": margin}
        open(ROOT / f"artifacts/v04/wp6_present/0909c74a/dual_mine/j3clean_n{n}_feas.json", "w").write(json.dumps(out, indent=1, default=str))
        if res.status == 0:
            g = np.zeros(Vv); g[keep] = res.x[:len(keep)]
            drops = (Amat @ g) - rhs
            print(f"[J3] minslack={float(drops.min())} viol={int((drops < -1e-7).sum())} tight={int((np.abs(drops) < 1e-7).sum())}", flush=True)
        return 0
    if mode == "farkas":
        Aeq = sp.vstack([Ared.T, np.ones((1, E))]).tocsr()
        beq = np.concatenate([np.zeros(Ared.shape[1]), [1.0]])
        cobj = -rhs
        res = linprog(cobj, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * E, method="highs")
        print(f"[J3] farkas status={res.status} maxyTrhs={float(-res.fun) if res.status==0 else None}", flush=True)
        if res.status == 0:
            y = res.x
            sup = np.where(y > 1e-7)[0]
            print(f"[J3] support={len(sup)} maxy={float(y.max())}", flush=True)
            order = np.argsort(-y)
            for i in order[:12]:
                print(f"  y={float(y[i]):.4f} {metas[i]} rhs={float(rhs[i]):.2f}", flush=True)
        return 0
    if mode == "l1":
        # L1-min: min sum u s.t. -u<=g<=u, A g>=rhs, gauge fixed zeros
        Vred = len(keep)
        # vars [g(Vred), u(Vred), t? no t here; feasibility enforced]
        # min sum u s.t. A g >= rhs, g-u<=0, -g-u<=0
        # A_ub rows: -A g <= -rhs; g-u<=0; -g-u<=0
        A1 = sp.hstack([-Ared, sp.csr_matrix((E, Vred))]).tocsr()  # -A g +0u <= -rhs
        b1 = -rhs
        I = sp.identity(Vred, format="csr"); Z = sp.csr_matrix((Vred, Vred))
        A2 = sp.hstack([I, -sp.identity(Vred, format="csr")]).tocsr()  # g-u<=0
        A3 = sp.hstack([-I, -sp.identity(Vred, format="csr")]).tocsr()  # -g-u<=0
        Aub = sp.vstack([A1, A2, A3]).tocsr()
        bub = np.concatenate([b1, np.zeros(Vred), np.zeros(Vred)])
        cobj = np.concatenate([np.zeros(Vred), np.ones(Vred)])
        res = linprog(cobj, A_ub=Aub, b_ub=bub,
                      bounds=[(None, None)] * Vred + [(0, None)] * Vred, method="highs")
        print(f"[J3] l1 status={res.status} l1={float(res.fun) if res.status==0 else None}", flush=True)
        if res.status == 0:
            g = np.zeros(Vv); g[keep] = res.x[:Vred]
            drops = (Amat @ g) - rhs
            print(f"[J3] l1 minslack={float(drops.min())} viol={int((drops < -1e-7).sum())}", flush=True)
            invk = {i: k for k, i in vmap.items()}
            vals = sorted(((str(invk[i]), float(g[i])) for i in range(Vv) if abs(float(g[i])) > 1e-9), key=lambda kv: -abs(kv[1]))
            print(f"[J3] nnz={len(vals)}", flush=True)
            for k, v in vals[:60]:
                print(f"  {k} = {v:.4f}", flush=True)
            open(ROOT / f"artifacts/v04/wp6_present/0909c74a/dual_mine/j3clean_n{n}_l1.json", "w").write(json.dumps(
                {"n": n, "E": E, "V": Vv, "l1": float(res.fun), "vals": [(k, v) for k, v in vals]}, indent=1, default=str))
        return 0
    print(f"unknown mode {mode}")
    return 2

if __name__ == "__main__":
    sys.exit(main())
