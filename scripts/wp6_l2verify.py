"""Independent verifier for PIVOT-25R L2 (no shared code with prover beyond
fresh trans derivation): reloads shapes+trans from scratch, recomputes
alpha/twin, loads FREE P_c values, checks ALL concrete inequalities
Phi(s)-Phi(s') >= w with Phi=-2*twin+P_alpha."""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))


def main():
    import wp6_overflow as V
    import wp6_cycle_ratio as O
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 7
    bits = _s.argv[2] if len(_s.argv) > 2 else "B"
    tag = {"B": "l2", "AB": "l3", "ABF": "l4", "POS": "lpos",
           "POSA": "lposa"}[bits]
    Sh = O.build(n)["Sh"]
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]

    def shape_of(P):
        return idx[json.dumps(list(O.enc_ptr(P)), sort_keys=True)]

    def is_vine(t):
        stack = [t]
        while stack:
            nd = stack.pop()
            if nd is None:
                continue
            if nd[1] is not None and nd[2] is not None:
                return False
            stack.append(nd[1])
            stack.append(nd[2])
        return True

    def path_to(t, y):
        p, nd = [], t
        while nd is not None and nd[0] != y:
            p.append(nd[0])
            nd = nd[1] if y < nd[0] else nd[2]
        if nd is None:
            return None
        p.append(y)
        return p

    def lca_of(t, a, b):
        pa, sb = path_to(t, a), set(path_to(t, b))
        return next(u for u in reversed(pa) if u in sb)  # deepest-first

    # fresh trans + depths + roots + vine + maxdepth (independent derivation)
    rt, dd, vine, md, da8, lc8 = {}, {}, {}, {}, {}, {}
    Atrans, Btrans = {}, {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        dd[ia] = V.depths_of(ptrs[ia])
        vine[ia] = is_vine(Sh[ia])
        mx = 0
        st = [(Sh[ia], 0)]
        while st:
            nd, d = st.pop()
            if nd is None:
                continue
            mx = max(mx, d)
            st.append((nd[1], d + 1))
            st.append((nd[2], d + 1))
        md[ia] = mx
        da8[ia] = dd[ia].get(n, 0)
        lc8[ia] = lca_of(Sh[ia], 2, n) if n >= 2 else 1
        for x in range(1, n + 1):
            A2 = copy.deepcopy(ptrs[ia])
            A2, iv = V.splay_cap(A2, x, 0, [])
            Atrans[(ia, x)] = (shape_of(A2), len(iv))
            B2 = copy.deepcopy(ptrs[ia])
            B2, p = V.splay_cap(B2, x, 0, [])
            Btrans[(ia, x)] = (shape_of(B2), len(p))
    print("[L2V] trans re-derived fresh: shapes=%d" % nS, flush=True)
    # cross-check against stored artifact tables
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    for k, v in D["Atrans"].items():
        assert Atrans[k] == v, k
    for k, v in D["Btrans"].items():
        assert Btrans[k] == v, k
    print("[L2V] trans tables match stored artifact", flush=True)

    L2 = json.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                            "0909c74a" / "dual_mine" /
                            ("%s_refine%d.json" % (tag, n)))))
    assert L2["result"]["feasible"] is True
    P = {eval(k): v for k, v in L2["result"]["pot"].items()}

    def cls(ra, rb, vb, va=0, fb=0, pa8=None, ma4=0):
        if bits == "POSA":
            da, db, lc = pa8
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0,
                    da, db, lc, 1 if ma4 else 0)
        if bits == "POS":
            da, db, lc = pa8
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0,
                    da, db, lc)
        if bits == "ABF":
            return (ra, rb, 1 if vb else 0, 1 if va else 0, 1 if fb else 0)
        if bits == "AB":
            return (ra, rb, 1 if vb else 0, 1 if va else 0)
        return (ra, rb, 1 if vb else 0)

    bad = 0
    checked = 0
    badclasses = set()
    for ia in range(nS):
        for ib in range(nS):
            U = cls(rt[ia], rt[ib], vine[ib], vine[ia], md[ib] >= 6,
                    (da8[ia], da8[ib], lc8[ia]), md[ia] >= 4)
            pu = -2 * (1 if rt[ia] == rt[ib] else 0) + P[U]
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                Vd = cls(rt[ia2], rt[ib], vine[ib], vine[ia2], md[ib] >= 6,
                         (da8[ia2], da8[ib], lc8[ia2]), md[ia2] >= 4)
                pv = -2 * (1 if rt[ia2] == rt[ib] else 0) + P[Vd]
                if -2 * a > pu - pv:
                    bad += 1
                    badclasses.add((U, Vd))
                checked += 1
                ib2, _ = Btrans[(ib, x)]
                Vk = cls(rt[ia2], rt[ib2], vine[ib2], vine[ia2],
                         md[ib2] >= 6, (da8[ia2], da8[ib2], lc8[ia2]),
                         md[ia2] >= 4)
                pv = -2 * (1 if rt[ia2] == rt[ib2] else 0) + P[Vk]
                if dd[ib].get(x, 0) // 2 - 2 * a > pu - pv:
                    bad += 1
                    badclasses.add((U, Vk))
                checked += 1
        if (ia + 1) % 60 == 0:
            print("[L2V] %d/%d bad=%d" % (ia + 1, nS, bad), flush=True)
    print("[L2V] checked=%d bad=%d badclasses=%d" %
          (checked, bad, len(badclasses)), flush=True)
    print("[L2V] CERTIFICATE: %s" % ("GREEN" if bad == 0 else "RED"))
    return 0 if bad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
