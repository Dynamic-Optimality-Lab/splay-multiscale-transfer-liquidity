"""Joint cone (§26): da=0 gauge vars with DA0-ROW + ROW-SWITCH constraints.
Vars: B-type gauges g + c-only root gr. If feasible -> SCALE (proceed).
If infeasible -> STRUCTURAL (architecture refuted)."""
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


def parent_map(t):
    par = {t[0]: None}
    stack = [t]
    while stack:
        nd = stack.pop()
        for ch in (nd[1], nd[2]):
            if ch is not None:
                par[ch[0]] = nd[0]
                stack.append(ch)
    return par


def anc_set(t, y):
    s = set()
    nd = t
    while nd is not None and nd[0] != y:
        s.add(nd[0])
        nd = nd[1] if y < nd[0] else nd[2]
    if nd is not None:
        s.add(nd[0])
    return s


def lca(t, a, b):
    c = anc_set(t, a) & anc_set(t, b)
    if not c:
        return None
    d = depths_list(t)
    return max(c, key=lambda k: d[k])


def rel3(t, a, b):
    ca = anc_set(t, a)
    cb = anc_set(t, b)
    return (a in cb, b in ca, lca(t, a, b))


def main():
    from scipy.optimize import linprog
    import scipy.sparse as sp
    import wp6_cycle_ratio as O
    import sys as _s2
    _mode = _s2.argv[1] if len(_s2.argv) > 1 else "both"  # da0|rs|both
    n = 5
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

    cons = []  # (terms dict var->coef, rhs): sum coef*g >= rhs
    # (i) DA0-ROW on da=0 rows: H(B)-H(Bp) >= D0, H=-R+Gpart
    # => Gpart(B)-Gpart(Bp) >= D0 + R - Rp =: rhs
    nda0 = 0
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            da0 = depths_list(A)
            for y in range(1, n + 1):
                if da0[y] != 0:
                    continue
                if _mode == "rs":
                    continue
                r = rep(ia, ib, y)
                Bp = r["endB"]
                jb = idx[json.dumps(Bp, sort_keys=True)]
                R = R_static(B, y)
                Rp = R_static(Bp, y)
                b = 1 if B[0] == y else 0
                D0 = R - 2 * (1 - b)
                rhs = D0 + R - Rp  # Gpart drop needed... careful: H-H'=[-R+G]-[-Rp+Gp]=(Rp-R)+(G-G'); need >=D0 => (G-G')>=D0-(Rp-R)=D0+R-Rp
                terms = {}
                for z in range(1, n + 1):
                    if z == y:
                        continue
                    s0 = slot_of(B, y, z)
                    s1 = slot_of(Bp, y, z)
                    _, l0 = lamrows(ib)[y]
                    _, l1 = lamrows(jb)[y]
                    u = (s0, l0.get(z, 0))
                    v = (s1, l1.get(z, 0))
                    tv(u)
                    tv(v)
                    if u != v:
                        terms[tv(u)] = terms.get(tv(u), 0) + 1.0
                        terms[tv(v)] = terms.get(tv(v), 0) - 1.0
                c0, _ = lamrows(ib)[y]
                c1, _ = lamrows(jb)[y]
                rv(c0)
                rv(c1)
                terms[len(tvars) + rvars[c0]] = terms.get(len(tvars) + rvars[c0], 0) + 1.0
                terms[len(tvars) + rvars[c1]] = terms.get(len(tvars) + rvars[c1], 0) - 1.0
                cons.append((terms, rhs))
                nda0 += 1
    print(f"[JNT] DA0 rows={nda0}", flush=True)
    # (ii) ROW-SWITCH on all pairs: H_r-H_x >= DDEL
    # H_r-H_x = [R(x)-R(r)] + [Gpart(r)-Gpart(x)]; Gpart(r)-Gpart(x) = [gr(rho_r)+sum g] - [gr(rho_x)+sum g]
    nrs = 0
    if _mode != "da0":
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
                # Gpart(r)-Gpart(x) >= Dd - (R(x)-R(r)) =: rhs2
                Rx = R_static(B, x)
                Rr = R_static(B, r)
                rhs2 = Dd - (Rx - Rr)
                terms = {}
                # atoms of row r minus atoms of row x (same B! both rows on B)
                _, lamr = R_coeffs(B, r)
                _, lamx = R_coeffs(B, x)
                for z in range(1, n + 1):
                    if z != r:
                        s = slot_of(B, r, z)
                        u = (s, lamr.get(z, 0))
                        tv(u)
                        terms[tv(u)] = terms.get(tv(u), 0) + 1.0
                    if z != x:
                        s = slot_of(B, x, z)
                        u = (s, lamx.get(z, 0))
                        tv(u)
                        terms[tv(u)] = terms.get(tv(u), 0) - 1.0
                cr, _ = R_coeffs(B, r)
                cx, _ = R_coeffs(B, x)
                rv(cr)
                rv(cx)
                terms[len(tvars) + rvars[cr]] = terms.get(len(tvars) + rvars[cr], 0) + 1.0
                terms[len(tvars) + rvars[cx]] = terms.get(len(tvars) + rvars[cx], 0) - 1.0
                cons.append((terms, rhs2))
                nrs += 1
    print(f"[JNT] RS rows={nrs} total={len(cons)} tvars={len(tvars)} rvars={len(rvars)}", flush=True)
    Vv = len(tvars) + len(rvars)
    rd = []
    cd = []
    vd = []
    rhs = []
    for i, (terms, r) in enumerate(cons):
        for v, c in terms.items():
            rd.append(i)
            cd.append(v)
            vd.append(float(c))
        rhs.append(float(r))
    Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))),
                         shape=(len(cons), Vv))
    rhs = np.array(rhs)
    # feasibility + max slack margin t: A g - t*1 >= rhs? use max-min slack
    # max t s.t. A g - t >= rhs, t free-ish: add var t
    E = len(cons)
    Aub = sp.hstack([-Amat, np.ones((E, 1))]).tocsr()
    bub = -rhs
    cobj = np.zeros(Vv + 1)
    cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=bub,
                  bounds=[(None, None)] * Vv + [(None, 1e6)], method="highs")
    print(f"[JNT] status={res.status} maxminslack={-res.fun if res.status==0 else None}", flush=True)
    json.dump({"rows": len(cons), "tvars": len(tvars),
               "status": res.status,
               "margin": float(-res.fun) if res.status == 0 else None},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/joint_cone.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
