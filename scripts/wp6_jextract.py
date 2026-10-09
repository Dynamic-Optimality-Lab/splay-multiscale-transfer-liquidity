"""J extraction v2 (two-phase, correct): J-SELF + J-SWITCH cone, maxsum + dump."""
import sys, copy, json
from pathlib import Path
import numpy as np
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/"python"))
sys.path.insert(0, str(ROOT/"scripts"))
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

    raw = []  # (dict key->coef, rhs) keys ('t',u)/('r',c)
    # J-SELF on da=0 rows
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
                assert s0 >= -1e-9
                terms = {}
                _, l0 = lamrows(ib)[y]
                _, l1 = lamrows(jb)[y]
                for z in range(1, n + 1):
                    if z == y:
                        continue
                    s0t = slot_of(B, y, z)
                    s1t = slot_of(Bp, y, z)
                    u = (s0t, l0.get(z, 0))
                    v = (s1t, l1.get(z, 0))
                    if u != v:
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                        terms[('t', v)] = terms.get(('t', v), 0) - 1.0
                c0, _ = lamrows(ib)[y]
                c1, _ = lamrows(jb)[y]
                terms[('r', c0)] = terms.get(('r', c0), 0) + 1.0
                terms[('r', c1)] = terms.get(('r', c1), 0) - 1.0
                raw.append((terms, -s0))
    nself = len(raw)
    print(f"[JX2] J-SELF rows={nself}", flush=True)
    # J-SWITCH on all pairs
    for ia in range(nS):
        for ib in range(nS):
            A, B = Sh[ia], Sh[ib]
            r = A[0]
            daA = depths_list(A)
            br = 1 if B[0] == r else 0
            Hr = H0(B, r, n)
            for x in range(1, n + 1):
                a = (daA[x] + 1) // 2
                bx = 1 if B[0] == x else 0
                Dd = -2 * a - 2 * (bx - br)
                Hx = H0(B, x, n)
                Psi = Dd - (Hr - Hx)
                terms = {}
                _, lamr = R_coeffs(B, r)
                _, lamx = R_coeffs(B, x)
                for z in range(1, n + 1):
                    if z != r:
                        s = slot_of(B, r, z)
                        u = (s, lamr.get(z, 0))
                        terms[('t', u)] = terms.get(('t', u), 0) + 1.0
                    if z != x:
                        s = slot_of(B, x, z)
                        u = (s, lamx.get(z, 0))
                        terms[('t', u)] = terms.get(('t', u), 0) - 1.0
                cr, _ = R_coeffs(B, r)
                cx, _ = R_coeffs(B, x)
                terms[('r', cr)] = terms.get(('r', cr), 0) + 1.0
                terms[('r', cx)] = terms.get(('r', cx), 0) - 1.0
                raw.append((terms, Psi))
        if (ia + 1) % 14 == 0:
            print(f"[JX2] ia={ia+1} rows={len(raw)}", flush=True)
    print(f"[JX2] total={len(raw)}", flush=True)
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
    import os as _os
    _w = _os.environ.get("JOBJ", "sum")
    if _w == "psi":
        # maximize drops on positive-demand rows only (rhs>0)
        w = (rhs > 1e-9).astype(float)
        cobj = -(Amat.T @ w)
    else:
        # maximize total drops (transport-effectiveness test)
        import numpy as _np
        cobj = -(np.asarray(Amat.sum(axis=0)).ravel())
    res = linprog(cobj, A_ub=-Amat, b_ub=np.zeros(E),
                  bounds=[(-1, 1)] * Vv, method="highs")
    print(f"[JX2] maxsum status={res.status} val={-res.fun if res.status==0 else None}", flush=True)
    if res.status == 0:
        g = res.x
        drops = (Amat @ g).ravel()
        print(f"[JX2] strict rows={int((drops>1e-9).sum())}/{E} maxdrop={drops.max():.3f}", flush=True)
        inv = {i: k for k, i in vmap.items()}
        gg = sorted(((inv[i], g[i]) for i in range(Vv) if abs(g[i]) > 1e-9),
                    key=lambda kv: -abs(kv[1]))[:24]
        print("[JX2] top J-vars:", [(str(k), round(float(v), 3)) for k, v in gg], flush=True)
        json.dump({"rows": E, "vars": Vv, "maxsum": float(-res.fun),
                   "strict": int((drops > 1e-9).sum()),
                   "top": [(str(k), round(float(v), 3)) for k, v in gg]},
                  open(ROOT/f"artifacts/v04/wp6_present/0909c74a/dual_mine/jextract.json", "w"), indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
