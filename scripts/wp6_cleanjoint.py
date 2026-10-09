"""Clean B-only joint + RS-alone maxminslack (two-phase, no mid-growth bug).
Vars: (slot,lambda) + (c,twin)-root. Modes via argv: joint|rs|da0."""
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
    import sys as _s
    mode = _s.argv[1] if len(_s.argv) > 1 else "joint"
    n = 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    rep_cache = {}

    def rep(ia, ib, x, md="K"):
        k = (ia, ib, x, md)
        if k not in rep_cache:
            rep_cache[k] = V.replay(Sh[ia], Sh[ib], [(md, x)])
        return rep_cache[k]

    lam_cache = {}

    def lamrows(ti):
        if ti not in lam_cache:
            lam_cache[ti] = {y: R_coeffs(Sh[ti], y) for y in range(1, n + 1)}
        return lam_cache[ti]

    raw = []
    # DA0 rows
    if mode in ("joint", "da0"):
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
                    b = 1 if B[0] == y else 0
                    D0 = R - 2 * (1 - b)
                    rhs = D0 + R - Rp
                    terms = {}
                    _, l0 = lamrows(ib)[y]
                    _, l1 = lamrows(jb)[y]
                    for z in range(1, n + 1):
                        if z == y:
                            continue
                        s0 = slot_of(B, y, z)
                        s1 = slot_of(Bp, y, z)
                        u = (s0, l0.get(z, 0))
                        v = (s1, l1.get(z, 0))
                        if u != v:
                            terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                            terms[('t', v)] = terms.get(('t', v), 0) - 1.0
                    c0, _ = lamrows(ib)[y]
                    c1, _ = lamrows(jb)[y]
                    terms[('r', (c0, 1 if A[0] == B[0] else 0))] = \
                        terms.get(('r', (c0, 1 if A[0] == B[0] else 0)), 0) + 1.0
                    Ap = r["endA"]
                    terms[('r', (c1, 1 if Ap[0] == Bp[0] else 0))] = \
                        terms.get(('r', (c1, 1 if Ap[0] == Bp[0] else 0)), 0) - 1.0
                    raw.append((terms, rhs))
        print(f"[CJ] DA0 rows done: {len(raw)}", flush=True)
    # RS rows (KEEP + DELETE, A-static filtered)
    if mode in ("joint", "rs"):
        for ia in range(nS):
            for ib in range(nS):
                A, B = Sh[ia], Sh[ib]
                da0 = depths_list(A)
                pa0 = parent_map(A)
                for x in range(1, n + 1):
                    # KEEP
                    r = rep(ia, ib, x)
                    Ap, Bp = r["endA"], r["endB"]
                    da1 = depths_list(Ap)
                    pa1 = parent_map(Ap)
                    jb = idx[json.dumps(Bp, sort_keys=True)]
                    t0 = 1 if A[0] == B[0] else 0
                    t1 = 1 if Ap[0] == Bp[0] else 0
                    for y in range(1, n + 1):
                        _, l0 = lamrows(ib)[y]
                        _, l1 = lamrows(jb)[y]
                        part = [z for z in set(l0) | set(l1)
                                if l1.get(z, 0) - l0.get(z, 0) != 0]
                        ok = True
                        if da0[y] != da1[y] or pa0.get(y) != pa1.get(y):
                            ok = False
                        if rel3(A, x, y) != rel3(Ap, x, y):
                            ok = False
                        if lca(A, x, y) != lca(Ap, x, y):
                            ok = False
                        if ok:
                            for z in part:
                                if da0[z] != da1[z] or pa0.get(z) != pa1.get(z):
                                    ok = False
                                    break
                                if rel3(A, x, z) != rel3(Ap, x, z):
                                    ok = False
                                    break
                                if rel3(A, y, z) != rel3(Ap, y, z):
                                    ok = False
                                    break
                                if lca(A, x, z) != lca(Ap, x, z):
                                    ok = False
                                    break
                                if lca(A, y, z) != lca(Ap, y, z):
                                    ok = False
                                    break
                        if ok:
                            CA = -2 * (((da1[y] + 1) // 2) - ((da0[y] + 1) // 2))
                            if CA != 0:
                                ok = False
                        if not ok:
                            continue
                        a = (da0[x] + 1) // 2
                        bx = 1 if B[0] == x else 0
                        br = 1 if B[0] == A[0] else 0
                        rA = A[0]
                        br = 1 if B[0] == rA else 0
                        Dd = -2 * a - 2 * (bx - br)
                        Rx = R_static(B, x)
                        Rr = R_static(B, rA)
                        rhs2 = Dd - (Rx - Rr)
                        terms = {}
                        _, lamr = R_coeffs(B, rA)
                        _, lamx = R_coeffs(B, x)
                        for z in range(1, n + 1):
                            if z != rA:
                                s = slot_of(B, rA, z)
                                terms[('t', (s, lamr.get(z, 0)))] = \
                                    terms.get(('t', (s, lamr.get(z, 0))), 0) + 1.0
                            if z != x:
                                s = slot_of(B, x, z)
                                terms[('t', (s, lamx.get(z, 0)))] = \
                                    terms.get(('t', (s, lamx.get(z, 0))), 0) - 1.0
                        cr, _ = R_coeffs(B, rA)
                        cx, _ = R_coeffs(B, x)
                        tpre = 1 if A[0] == B[0] else 0
                        terms[('r', (cr, tpre))] = terms.get(('r', (cr, tpre)), 0) + 1.0
                        terms[('r', (cx, tpre))] = terms.get(('r', (cx, tpre)), 0) - 1.0
                        raw.append((terms, rhs2))
                    # DELETE
                    rD = rep(ia, ib, x, "D")
                    Ad = rD["endA"]
                    daD = depths_list(Ad)
                    paD = parent_map(Ad)
                    t0D = 1 if A[0] == B[0] else 0
                    for y in range(1, n + 1):
                        ok = True
                        if da0[y] != daD[y] or pa0.get(y) != paD.get(y):
                            ok = False
                        if rel3(A, x, y) != rel3(Ad, x, y):
                            ok = False
                        if lca(A, x, y) != lca(Ad, x, y):
                            ok = False
                        if ok:
                            CA = -2 * (((daD[y] + 1) // 2) - ((da0[y] + 1) // 2))
                            if CA != 0:
                                ok = False
                        if not ok:
                            continue
                        tD = 1 if Ad[0] == B[0] else 0
                        cB, _ = lamrows(ib)[y]
                        raw.append(({('r', (cB, t0D)): 1.0,
                                     ('r', (cB, tD)): -1.0}, 0.0))
            if (ia + 1) % 14 == 0:
                print(f"[CJ] ia={ia+1} rows={len(raw)}", flush=True)
    print(f"[CJ] total={len(raw)}", flush=True)
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
    rhs = []
    for i, (terms, rh) in enumerate(raw):
        for k, c in terms.items():
            rd.append(i)
            cd.append(vmap[k])
            vd.append(float(c))
        rhs.append(float(rh))
    Amat = sp.csr_matrix((np.array(vd), (np.array(rd), np.array(cd))),
                         shape=(E, Vv))
    rhs = np.array(rhs)
    # max-min slack
    Aub = sp.hstack([-Amat, np.ones((E, 1))]).tocsr()
    cobj = np.zeros(Vv + 1)
    cobj[-1] = -1.0
    res = linprog(cobj, A_ub=Aub, b_ub=-rhs,
                  bounds=[(None, None)] * Vv + [(None, 1e6)], method="highs")
    print(f"[CJ] mode={mode}: rows={E} vars={Vv} status={res.status} margin={-res.fun if res.status==0 else None}", flush=True)
    json.dump({"mode": mode, "rows": E, "vars": Vv, "status": res.status,
               "margin": float(-res.fun) if res.status == 0 else None},
              open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/cleanjoint_{mode}.json", "w"), indent=1)
    return 0


if __name__ == "__main__":
    sys.exit(main())
