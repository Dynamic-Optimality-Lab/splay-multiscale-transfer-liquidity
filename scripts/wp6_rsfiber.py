"""RS-alone with fiber vars: can fiber dependence rescue row-switch?
Vars: ((slot,lambda),da) + c-root. Constraints: RS rows only. Reports margin."""
import sys, copy, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
import wp6_overflow as V
from wp6_staticR import depths_list, path_nodes, R_static
from wp6_lambda import R_coeffs


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


def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import wp6_cycle_ratio as O
    import sys as _sn
    n = int(_sn.argv[1]) if len(_sn.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    tvars = {}
    rvars = {}

    def tv(t):
        if t not in tvars:
            tvars[t] = len(tvars)
        return tvars[t]

    def rv(r):
        if r not in rvars:
            rvars[r] = len(rvars)
        return rvars[r]

    cons = []
    # two-phase assembly (avoid mid-growth len() bug): symbolic first
    raw = []  # (dict key->coef with keys ('t',u)/('r',c), rhs)
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            r = A[0]
            daA = depths_list(A)
            br = 1 if B[0] == r else 0
            for x in range(1, n + 1):
                a = (daA[x] + 1) // 2
                bx = 1 if B[0] == x else 0
                Dd = -2 * a - 2 * (bx - br)
                Rx = R_static(B, x)
                Rr = R_static(B, r)
                rhs2 = Dd - (Rx - Rr)
                terms = {}
                _, lamr = R_coeffs(B, r)
                _, lamx = R_coeffs(B, x)
                for z in range(1, n + 1):
                    if z != r:
                        s = slot_of(B, r, z)
                        u = ((s, lamr.get(z, 0)), daA[r])
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                    if z != x:
                        s = slot_of(B, x, z)
                        u = ((s, lamx.get(z, 0)), daA[x])
                        terms[('t', u)] = terms.get(('t', u), 0) - 1.0
                cr, _ = R_coeffs(B, r)
                cx, _ = R_coeffs(B, x)
                terms[('r', cr)] = terms.get(('r', cr), 0) + 1.0
                terms[('r', cx)] = terms.get(('r', cx), 0) - 1.0
                raw.append((terms, rhs2))
        if (ia + 1) % 14 == 0:
            print(f"[RSF] ia={ia+1} rows={len(raw)}", flush=True)
    vmap = {}
    for (terms, _) in raw:
        for k in terms:
            if k not in vmap:
                vmap[k] = len(vmap)
    # add DA0-ROW constraints (da=0 fiber rows) in same fiber vars
    import wp6_cycle_ratio as O2
    Sh5 = O2.shapes_of(list(range(1, n+1)))
    idx5 = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh5)}
    rep_cache2 = {}

    def rep2(ia, ib, x):
        k = (ia, ib, x)
        if k not in rep_cache2:
            rep_cache2[k] = V.replay(Sh5[ia], Sh5[ib], [("K", x)])
        return rep_cache2[k]

    lam_cache2 = {}

    def lamrows2(ti):
        if ti not in lam_cache2:
            lam_cache2[ti] = {y: R_coeffs(Sh5[ti], y) for y in range(1, n+1)}
        return lam_cache2[ti]

    nda0 = 0
    nS5 = len(Sh5)
    for ia in range(nS5):
        for ib in range(nS5):
            A, B = Sh5[ia], Sh5[ib]
            da0 = depths_list(A)
            for y in range(1, n+1):
                if da0[y] != 0:
                    continue
                r = rep2(ia, ib, y)
                Bp = r["endB"]
                jb = idx5[json.dumps(Bp, sort_keys=True)]
                R = R_static(B, y)
                Rp = R_static(Bp, y)
                b = 1 if B[0] == y else 0
                D0 = R - 2 * (1 - b)
                rhs = D0 + R - Rp
                terms = {}
                _, l0 = lamrows2(ib)[y]
                _, l1 = lamrows2(jb)[y]
                for z in range(1, n+1):
                    if z == y:
                        continue
                    s0 = slot_of(B, y, z)
                    s1 = slot_of(Bp, y, z)
                    u = ((s0, l0.get(z, 0)), 0)
                    v = ((s1, l1.get(z, 0)), 0)
                    if u != v:
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                        terms[('t', v)] = terms.get(('t', v), 0) - 1.0
                c0, _ = lamrows2(ib)[y]
                c1, _ = lamrows2(jb)[y]
                terms[('r', c0)] = terms.get(('r', c0), 0) + 1.0
                terms[('r', c1)] = terms.get(('r', c1), 0) - 1.0
                raw.append((terms, rhs))
                nda0 += 1
    print(f"[RSF] + DA0 rows={nda0}", flush=True)
    vmap = {}
    for (terms, _) in raw:
        for k in terms:
            if k not in vmap:
                vmap[k] = len(vmap)
    Vv = len(vmap)
    E = len(raw)
    rd = []
    cd = []
    vd = []
    bub = []
    for i, (terms, rh) in enumerate(raw):
        for k, c in terms.items():
            rd.append(i)
            cd.append(vmap[k])
            vd.append(float(c))
        bub.append(-float(rh))
    import os as _os
    _obj = _os.environ.get("FIBEROBJ", "minmax")
    if _obj == "maxsum":
        # maximize total drops (transport-effectiveness test)
        Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))),
                             shape=(E, Vv))
        tot = np.asarray(Amat.sum(axis=0)).ravel()
        cobj = -tot
        res = linprog(cobj, A_ub=-Amat, b_ub=np.zeros(E),
                      bounds=[(-1, 1)] * Vv, method="highs")
        print(f"[RSF] fiber JOINT maxsum: rows={E} vars={Vv} status={res.status} maxsum={-res.fun if res.status==0 else None}", flush=True)
        json.dump({"rows": E, "vars": Vv, "status": res.status, "mode": "maxsum",
                   "maxsum": float(-res.fun) if res.status == 0 else None},
                  open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/rsfiber_maxsum.json", "w"), indent=1)
        return 0
    Aub = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))),
                        shape=(E, Vv + 1))
    # max-min slack t: -A g + t*1 <= -rhs  <=> A g - t >= rhs
    import scipy.sparse as _sp
    Aub2 = _sp.hstack([-Aub[:, :Vv], np.ones((E, 1))]).tocsr()
    bub2 = np.array(bub)
    cobj = np.zeros(Vv + 1)
    cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub2, b_ub=bub2,
                  bounds=[(None, None)] * Vv + [(None, 1e6)], method="highs")
    print(f"[RSF] fiber RS-alone: rows={E} vars={Vv} status={res.status} margin={-res.fun if res.status==0 else None}", flush=True)
    json.dump({"rows": E, "vars": Vv, "status": res.status,
               "margin": float(-res.fun) if res.status == 0 else None},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/rsfiber.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
