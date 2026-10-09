"""J4 SHARED B-only generator: tau=(slot,lambda,delta,d_y), root=c.
Unique SELF per (B,x) + ROW-DIAMETER per (B,r!=x), global vars across sizes.
Phase 1 symbolic raw; Phase 2 fixed vmap; A J>=rhs with A_ub=-A,b_ub=-rhs.
Usage: python scripts/wp6_j4shared.py <modes...>
Modes: counts | feas56 | feas567 | feas8 | farkas56 | farkas567 | l1_56 | l1_567 | homog56 | homog567
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

def tau4_of(T, y, z, lam):
    s = slot_of(T, y, z)
    dd = depths_list(T)
    return (s, lam, dd[z] - dd[y], dd[y])

def build_shared(sizes):
    import wp6_cycle_ratio as O
    raw = []
    info = {}
    for n in sizes:
        Sh = O.shapes_of(list(range(1, n + 1)))
        nS = len(Sh)
        nself = ndiam = 0
        for bi, B in enumerate(Sh):
            for x in range(1, n + 1):
                Bp = V.replay(B, B, [("K", x)])["endB"]
                R = R_static(B, x)
                Rp = R_static(Bp, x)
                G = n - subsize(B, x)
                Gp = n - subsize(Bp, x)
                b = 1 if B[0] == x else 0
                D0 = R - 2 * (1 - b)
                Hdrop = (-R + KAPPA * G) - (-Rp + KAPPA * Gp)
                s0 = Hdrop - D0
                _, l0 = R_coeffs(B, x)
                _, l1 = R_coeffs(Bp, x)
                terms = {}
                pre = []
                post = []
                for z in range(1, n + 1):
                    if z == x:
                        continue
                    u = tau4_of(B, x, z, l0.get(z, 0))
                    v = tau4_of(Bp, x, z, l1.get(z, 0))
                    pre.append(u)
                    post.append(v)
                    if u != v:
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                        terms[('t', v)] = terms.get(('t', v), 0) - 1.0
                c0, _ = R_coeffs(B, x)
                c1, _ = R_coeffs(Bp, x)
                terms[('r', c0)] = terms.get(('r', c0), 0) + 1.0
                terms[('r', c1)] = terms.get(('r', c1), 0) - 1.0
                raw.append((terms, -s0, ('SELF', n, bi, x, -s0, Hdrop, D0, s0,
                                         sorted(map(str, pre)), sorted(map(str, post)))))
                nself += 1
            bB = B[0]
            for r in range(1, n + 1):
                _, lamr = R_coeffs(B, r)
                Hr = H0(B, r, n)
                br = 1 if bB == r else 0
                for x in range(1, n + 1):
                    if x == r:
                        continue
                    _, lamx = R_coeffs(B, x)
                    Hx = H0(B, x, n)
                    bx = 1 if bB == x else 0
                    Psi1 = -2 + 2 * (br - bx) - (Hr - Hx)
                    terms = {}
                    mr = []
                    mx = []
                    for z in range(1, n + 1):
                        if z != r:
                            u = tau4_of(B, r, z, lamr.get(z, 0))
                            mr.append(u)
                            terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                        if z != x:
                            u = tau4_of(B, x, z, lamx.get(z, 0))
                            mx.append(u)
                            terms[('t', u)] = terms.get(('t', u), 0) - 1.0
                    cr, _ = R_coeffs(B, r)
                    cx, _ = R_coeffs(B, x)
                    terms[('r', cr)] = terms.get(('r', cr), 0) + 1.0
                    terms[('r', cx)] = terms.get(('r', cx), 0) - 1.0
                    raw.append((terms, Psi1, ('DIAM', n, bi, r, x, Psi1, br, bx, Hr, Hx,
                                             sorted(map(str, mr)), sorted(map(str, mx)))))
                    ndiam += 1
        info[n] = {"shapes": nS, "self": nself, "diam": ndiam}
        print(f"[J4] n={n} shapes={nS} self={nself} diam={ndiam}", flush=True)
    return raw, info

def assemble(raw):
    import scipy.sparse as sp
    vmap = {}
    for (terms, _, _) in raw:
        for k in terms:
            if k not in vmap:
                vmap[k] = len(vmap)
    Vv, E = len(vmap), len(raw)
    rd, cd, vd, rhs, metas = [], [], [], [], []
    for i, (terms, rh, meta) in enumerate(raw):
        for k, c in terms.items():
            rd.append(i); cd.append(vmap[k]); vd.append(float(c))
        rhs.append(float(rh)); metas.append(meta)
    Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))), shape=(E, Vv))
    return Amat, np.array(rhs), metas, vmap

def gauge_keep(vmap):
    tkeys = [k for k in vmap if k[0] == 't']; rkeys = [k for k in vmap if k[0] == 'r']
    gfix = [tkeys[0], rkeys[0]] if tkeys and rkeys else []
    keep = [i for k, i in vmap.items() if k not in set(gfix)]
    return gfix, keep

def solve_feas(Amat, rhs, vmap, tag):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    Vv = len(vmap); E = Amat.shape[0]
    inv = {i: k for k, i in vmap.items()}
    is_t = np.array([1.0 if inv[i][0] == 't' else 0.0 for i in range(Vv)])
    is_r = np.array([1.0 if inv[i][0] == 'r' else 0.0 for i in range(Vv)])
    at = float(np.abs(Amat @ is_t).max()); ar = float(np.abs(Amat @ is_r).max())
    try:
        rnk = int(np.linalg.matrix_rank(Amat.toarray()))
    except Exception as e:
        rnk = None; print(f"[{tag}] rank fail {e}", flush=True)
    gfix, keep = gauge_keep(vmap)
    print(f"[{tag}] E={E} V={Vv} rank={rnk} null={Vv - rnk if rnk is not None else None} "
          f"A*1t={at} A*1r={ar} gauge={gfix} keep={len(keep)}", flush=True)
    Ared = Amat[:, keep]
    Aub = sp.hstack([-Ared, np.ones((E, 1))]).tocsr(); bub = -rhs
    cobj = np.zeros(len(keep) + 1); cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * len(keep) + [(None, 1e6)], method="highs")
    margin = float(-res.fun) if res.status == 0 else None
    print(f"[{tag}] feas status={res.status} margin={margin}", flush=True)
    viol = tight = msl = mxsl = None
    if res.status == 0:
        g = np.zeros(Vv); g[keep] = res.x[:len(keep)]
        drops = (Amat @ g) - rhs
        msl = float(drops.min()); mxsl = float(drops.max())
        viol = int((drops < -1e-7).sum()); tight = int((np.abs(drops) < 1e-7).sum())
        print(f"[{tag}] minslack={msl} maxslack={mxsl} viol={viol} tight={tight}", flush=True)
    return {"tag": tag, "E": E, "V": Vv, "rank": rnk, "null": (Vv - rnk) if rnk is not None else None,
            "at": at, "ar": ar, "gauge": [str(g) for g in gfix], "status": res.status,
            "margin": margin, "minslack": msl, "maxslack": mxsl, "viol": viol, "tight": tight}

def solve_farkas(Amat, rhs, metas, vmap, tag, top=16):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    Vv = len(vmap); E = Amat.shape[0]
    _, keep = gauge_keep(vmap)
    Ared = Amat[:, keep]
    Aeq = sp.vstack([Ared.T, np.ones((1, E))]).tocsr()
    beq = np.concatenate([np.zeros(Ared.shape[1]), [1.0]])
    res = linprog(-rhs, A_eq=Aeq, b_eq=beq, bounds=[(0, None)] * E, method="highs")
    print(f"[{tag}] farkas status={res.status} maxyTrhs={float(-res.fun) if res.status==0 else None}", flush=True)
    if res.status == 0:
        y = res.x
        sup = int((y > 1e-7).sum())
        print(f"[{tag}] support={sup} maxy={float(y.max())}", flush=True)
        import wp6_cycle_ratio as O
        cache = {}
        for i in np.argsort(-y)[:top]:
            m = metas[i]
            n = m[1]; bi = m[2]
            key = (n, bi)
            if key not in cache:
                cache[key] = O.shapes_of(list(range(1, n + 1)))[bi]
            print(f"  y={float(y[i]):.4f} {m[:7]} rhs={float(rhs[i]):.2f} B={cache[key]}", flush=True)
    return res

def solve_l1(Amat, rhs, metas, vmap, tag, outname):
    from scipy.optimize import linprog
    import scipy.sparse as sp
    Vv = len(vmap); E = Amat.shape[0]
    _, keep = gauge_keep(vmap)
    Vred = len(keep); Ared = Amat[:, keep]
    A1 = sp.hstack([-Ared, sp.csr_matrix((E, Vred))]).tocsr()
    I = sp.identity(Vred, format="csr")
    Aub = sp.vstack([A1, sp.hstack([I, -sp.identity(Vred, format="csr")]).tocsr(),
                     sp.hstack([-I, -sp.identity(Vred, format="csr")]).tocsr()]).tocsr()
    bub = np.concatenate([-rhs, np.zeros(Vred), np.zeros(Vred)])
    cobj = np.concatenate([np.zeros(Vred), np.ones(Vred)])
    res = linprog(cobj, A_ub=Aub, b_ub=bub, bounds=[(None, None)] * Vred + [(0, None)] * Vred, method="highs")
    print(f"[{tag}] l1 status={res.status} l1={float(res.fun) if res.status==0 else None}", flush=True)
    if res.status == 0:
        g = np.zeros(Vv); g[keep] = res.x[:Vred]
        drops = (Amat @ g) - rhs
        print(f"[{tag}] minslack={float(drops.min())} maxslack={float(drops.max())} viol={int((drops < -1e-7).sum())}", flush=True)
        invk = {i: k for k, i in vmap.items()}
        vals = sorted(((str(invk[i]), float(g[i])) for i in range(Vv) if abs(float(g[i])) > 1e-9), key=lambda kv: -abs(kv[1]))
        print(f"[{tag}] nnz={len(vals)}", flush=True)
        for k, v in vals[:80]:
            print(f"  {k} = {v:.4f}", flush=True)
        open(ROOT / f"artifacts/v04/wp6_present/0909c74a/dual_mine/{outname}.json", "w").write(json.dumps(
            {"tag": tag, "E": E, "V": Vv, "l1": float(res.fun), "vals": vals}, indent=1, default=str))
        return g
    return None

def solve_homog(Amat, vmap, tag):
    from scipy.optimize import linprog
    Vv = len(vmap); E = Amat.shape[0]
    cobj = -(np.asarray(Amat.sum(axis=0)).ravel())
    res = linprog(cobj, A_ub=-Amat, b_ub=np.zeros(E), bounds=[(-1, 1)] * Vv, method="highs")
    ms = float(-res.fun) if res.status == 0 else None
    print(f"[{tag}] homog maxsum status={res.status} maxsum={ms}", flush=True)
    return {"tag": tag, "status": res.status, "maxsum": ms}

def main():
    modes = sys.argv[1:] or ["counts"]
    if "counts" in modes:
        for n in [5, 6, 7]:
            import wp6_cycle_ratio as O
            nS = len(O.shapes_of(list(range(1, n + 1))))
            print(f"[COUNTS] n={n} Catalan={nS} self={nS*n} diam={nS*n*(n-1)} total={nS*n*n}", flush=True)
    if "feas56" in modes:
        raw, info = build_shared([5, 6])
        Amat, rhs, metas, vmap = assemble(raw)
        out = solve_feas(Amat, rhs, vmap, "J4-SH56")
        open(ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4shared_56_feas.json", "w").write(
            json.dumps({**out, "info": info}, indent=1, default=str))
    if "feas567" in modes:
        raw, info = build_shared([5, 6, 7])
        Amat, rhs, metas, vmap = assemble(raw)
        out = solve_feas(Amat, rhs, vmap, "J4-SH567")
        open(ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4shared_567_feas.json", "w").write(
            json.dumps({**out, "info": info}, indent=1, default=str))
    if "feas8" in modes:
        raw, info = build_shared([8])
        Amat, rhs, metas, vmap = assemble(raw)
        out = solve_feas(Amat, rhs, vmap, "J4-SH8")
        open(ROOT / "artifacts/v04/wp6_present/0909c74a/dual_mine/j4shared_8_feas.json", "w").write(
            json.dumps({**out, "info": info}, indent=1, default=str))
    if "farkas56" in modes:
        raw, info = build_shared([5, 6])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_farkas(Amat, rhs, metas, vmap, "J4-SH56-FARKAS")
    if "farkas567" in modes:
        raw, info = build_shared([5, 6, 7])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_farkas(Amat, rhs, metas, vmap, "J4-SH567-FARKAS")
    if "l1_56" in modes:
        raw, info = build_shared([5, 6])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_l1(Amat, rhs, metas, vmap, "J4-SH56-L1", "j4shared_56_l1")
    if "l1_567" in modes:
        raw, info = build_shared([5, 6, 7])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_l1(Amat, rhs, metas, vmap, "J4-SH567-L1", "j4shared_567_l1")
    if "homog56" in modes:
        raw, info = build_shared([5, 6])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_homog(Amat, vmap, "J4-SH56-HOMOG")
    if "homog567" in modes:
        raw, info = build_shared([5, 6, 7])
        Amat, rhs, metas, vmap = assemble(raw)
        solve_homog(Amat, vmap, "J4-SH567-HOMOG")
    return 0

if __name__ == "__main__":
    sys.exit(main())
