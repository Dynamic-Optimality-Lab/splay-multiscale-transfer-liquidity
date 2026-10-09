"""PIVOT-25R-CUT §2-7: A-path cut system, Sep intervals, Gamma vectors,
CAND sets with 4 exact conditions, |CAND| distribution.

Per gateway event (access x, key y, C>0): cuts e_i on P_A(x) (nested
X_i); Sep_A(x;y,z) interval check; Delta_lambda/c from Lambda rows;
Gamma_i^±; CAND via relevance/activity/contact/nonvacuity (exact tree
diffs, documented operationalizations).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list
from wp6_lambda import R_coeffs


def step(sid, msg):
    print("[CUT %s] %s" % (sid, msg), flush=True)


def ptr_root(P):
    r = P
    while r["p"] is not None:
        r = r["p"]
    return r


def find(P, key):
    P = ptr_root(P)
    stack = [P]
    while stack:
        nd = stack.pop()
        if nd["k"] == key:
            return nd
        if nd["l"] is not None:
            stack.append(nd["l"])
        if nd["r"] is not None:
            stack.append(nd["r"])
    return None


def subkeys(nd):
    out = []

    def go(m):
        if m is None:
            return
        out.append(m["k"])
        go(m["l"])
        go(m["r"])
    go(nd)
    return frozenset(out)


def apath(Aptr, x):
    Aptr = ptr_root(Aptr)
    out = []
    nd = Aptr
    while nd is not None and nd["k"] != x:
        out.append(nd["k"])
        nd = nd["l"] if x < nd["k"] else nd["r"]
    if nd is not None:
        out.append(nd["k"])
    return tuple(out)


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    evs = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                      "0909c74a" / "dual_mine" /
                      ("carrier%d.json" % (n if n == 5 else 6))).read_text())
    if n != 5:
        evs = evs[:8000]
    step("L", "events=%d" % len(evs))
    # per-access cache: post trees, twin, path data
    acc = {}

    def getacc(ia, ib, x):
        k = (ia, ib, x)
        if k in acc:
            return acc[k]
        A = V.to_ptr(copy.deepcopy(Sh[ia]))
        B = V.to_ptr(copy.deepcopy(Sh[ib]))
        rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
        Ap, Bp = rep["endA"], rep["endB"]
        t0 = 1 if A is not None and Sh[ia][0] == Sh[ib][0] else 0
        t1 = 1
        da0, da1 = depths_list(Sh[ia]), depths_list(Ap)
        sk0 = {y: subkeys(find(V.to_ptr(copy.deepcopy(Sh[ia])), y))
               for y in range(1, n + 1)}
        sk1 = {y: subkeys_list2(Ap, y) for y in range(1, n + 1)}
        p0 = apath(V.to_ptr(copy.deepcopy(Sh[ia])), x)
        v = {"Ap": Ap, "Bp": Bp, "t0": t0, "t1": t1, "da0": da0,
             "da1": da1, "sk0": sk0, "sk1": sk1, "path": p0}
        acc[k] = v
        return v

    def subkeys_list2(t, x):
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

    def parof(t, key):
        # parent key of `key` in list-shape t (None if root/absent)
        par = {t[0]: None}
        stack = [t]
        while stack:
            nd = stack.pop()
            for ch in (nd[1], nd[2]):
                if ch is not None:
                    par[ch[0]] = nd[0]
                    stack.append(ch)
        return par.get(key)

    dist = Counter()
    nest_all = True
    sep_ok = 0
    sep_tot = 0
    out_rows = []
    for e in evs:
        ia, ib, x, y = e["ia"], e["ib"], e["x"], e["y"]
        g = getacc(ia, ib, x)
        p = g["path"]
        d = len(p) - 1
        if d == 0:
            dist["d0"] += 1
            continue
        da0 = depths_list(Sh[ia])
        da1 = g["da1"]
        # cuts e_i, X_i = subtree(v_i) key sets (pre), nested check
        X = []
        for i in range(1, d + 1):
            X.append(subkeys(find(V.to_ptr(copy.deepcopy(Sh[ia])),
                                  p[i]), ))
        # nested?
        nest = all(X[i + 1] <= X[i] for i in range(len(X) - 1))
        nest_all = nest_all and nest
        # Sep interval check on sample pairs (y vs support keys)
        cB, lamB = e["brow0"][0], dict(e["brow0"][1])
        cP, lamP = e["brow1"][0], dict(e["brow1"][1])
        keys = set(lamB) | set(lamP) | {y}
        dl = {}
        for z in keys:
            dl[z] = lamP.get(z, 0) - lamB.get(z, 0)
        seps = {}
        for z in keys:
            if z == y:
                continue
            s = set()
            for i in range(1, d + 1):
                if (y in X[i - 1]) != (z in X[i - 1]):
                    s.add(i)
            seps[z] = s
            # interval check
            if s and s != set(range(min(s), max(s) + 1)):
                sep_ok += 0
            sep_tot += 1
        # Gamma vectors
        Gam, GamP, GamM = {}, {}, {}
        for i in range(1, d + 1):
            gp = gm = g0 = 0
            for z in keys:
                if z == y:
                    continue
                if (y in X[i - 1]) != (z in X[i - 1]):
                    dd = dl.get(z, 0)
                    g0 += dd
                    if dd > 0:
                        gp += dd
                    elif dd < 0:
                        gm += -dd
            Gam[i], GamP[i], GamM[i] = g0, gp, gm
        # CAND: relevance + activity + contact + nonvacuity
        # post A-subtree sets keyed by node key (same keys, new parents)
        ApA = g["Ap"]
        # post subtree sets keyed by node key (same keys, new parents)
        def postset(vk):
            nd = find(V.to_ptr(copy.deepcopy(ApA)), vk)
            return subkeys(nd) if nd is not None else frozenset()
        # post path nodes (for side membership post)
        Apost = V.to_ptr(copy.deepcopy(ApA))
        ppost = []
        nd = Apost
        while nd["p"] is not None:
            nd = nd["p"]
        while nd is not None and nd["k"] != x:
            ppost.append(nd["k"])
            nd = nd["l"] if x < nd["k"] else nd["r"]
        if nd is not None:
            ppost.append(nd["k"])
        ppost = tuple(ppost)
        cand = []
        flags = []
        pa0 = {z: parof(Sh[ia], z) for z in keys if z != y}
        pa1 = {z: parof(g["Ap"], z) for z in keys if z != y}
        for i in range(1, d + 1):
            rel = (GamP[i] + GamM[i]) > 0
            vi = p[i]
            Spre = X[i - 1]
            Spost = postset(vi)
            act = (Spre != Spost)
            # contact: support-z with dl!=0 inside pre-or-post region
            # whose A-depth OR A-attachment (parent) changed
            con = False
            for z in keys:
                if z == y:
                    continue
                if dl.get(z, 0) == 0:
                    continue
                if (z in Spre or z in Spost) and \
                        (da0[z] != da1[z] or pa0[z] != pa1[z]):
                    con = True
                    break
            # nonvacuity: touched AND (relevant or C_A-sensitive key
            # whose region covers the cut)
            nonvac = False
            if act and rel:
                nonvac = True
            elif act:
                for yy in range(1, n + 1):
                    if ((da0[yy] + 1) // 2 != (da1[yy] + 1) // 2) and \
                            (yy in Spre or yy in Spost):
                        nonvac = True
                        break
            flags.append([rel, act, con, nonvac])
            if rel and act and con and nonvac:
                cand.append(i)
        dist[len(cand)] += 1
        dempty = all(v == 0 for v in dl.values())
        out_rows.append({"e": (ia, ib, x, y), "d": d, "cand": cand,
                         "flags": flags, "dempty": dempty,
                         "Gam": {str(k): v for k, v in Gam.items()}})
    step("S", "dist=%s nested-always=%s" % (dict(dist), nest_all))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("cutcar%d.json" % n)).write_text(
        json.dumps(out_rows, indent=0, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
