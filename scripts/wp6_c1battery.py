"""PIVOT-25R-C §7 battery: test grammar C1 Phi=-2*twin+(D_B-2*D_A) (total
depths; unbounded range; full A-shape sensitive) on the hard-witness battery.
Every entry replayed canonically; PASS/FAIL per concrete inequality."""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[C1B %s] %s" % (sid, msg), flush=True)


def totdepth(ptr):
    return sum(V.depths_of(ptr).values())


def rootof(ptr):
    r = ptr
    while r["p"] is not None:
        r = r["p"]
    return r["k"]


def phi_of(pA, pB):
    tw = 1 if rootof(pA) == rootof(pB) else 0
    return -2 * tw + (totdepth(pB) - 2 * totdepth(pA)), tw


def path_nodes(ptr, y):
    """Root-to-y node sequence on ptr (keys ordered)."""
    cur = ptr
    while cur["p"] is not None:
        cur = cur["p"]
    out = []
    while True:
        out.append(cur["k"])
        if cur["k"] == y:
            break
        cur = cur["l"] if y < cur["k"] else cur["r"]
    return tuple(out)


def agr_of(pA, pB, keys):
    return sum(1 for y in keys if path_nodes(pA, y) == path_nodes(pB, y))


def phi_cand(name, pA, pB, keys):
    tw = 1 if rootof(pA) == rootof(pB) else 0
    if name == "C1":
        return -2 * tw + (totdepth(pB) - 2 * totdepth(pA)), tw
    if name == "C3":
        return -2 * tw - totdepth(pA), tw
    if name == "C4":
        return -2 * tw + totdepth(pB), tw
    if name == "C5":
        return -2 * tw - agr_of(pA, pB, keys), tw
    raise AssertionError(name)


def main():
    bat = []
    # n=7 fixed witnesses
    # NOTE: shapes_of only (O.build also constructs the full pair-graph adj;
    # 425M tuples at n=9 — never build it here).
    Sh7 = O.shapes_of(list(range(1, 8)))
    idx7 = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh7)}
    bat += [(7, 28, 0, 7, "K", "L1e1"), (7, 297, 428, 1, "K", "L1e2")]
    # n=7 twin-only class samples via targeted scan
    D7 = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                              "0909c74a" / "trans7.pkl"), "rb"))
    A7, B7 = D7["Atrans"], D7["Btrans"]
    ptrs7 = [V.to_ptr(copy.deepcopy(s)) for s in Sh7]
    rt7, dd7 = {}, {}
    for ia in range(len(Sh7)):
        rt7[ia] = rootof(ptrs7[ia])
        dd7[ia] = V.depths_of(ptrs7[ia])
    got03 = got13 = gotR = None
    for ia in range(len(Sh7)):
        for ib in range(len(Sh7)):
            tw = 1 if rt7[ia] == rt7[ib] else 0
            for x in range(1, 8):
                a = (dd7[ia].get(x, 0) + 1) // 2
                q = dd7[ib].get(x, 0) // 2
                ia2, _ = A7[(ia, x)]
                ib2, _ = B7[(ib, x)]
                tw2 = 1 if rt7[ia2] == rt7[ib2] else 0
                if got03 is None and a == 0 and q == 3 and tw == 0 \
                        and tw2 == 1:
                    got03 = (ia, ib, x)
                if got13 is None and a == 1 and q == 3 and tw == 1 \
                        and tw2 == 1:
                    got13 = (ia, ib, x)
                if gotR is None and x == 1 and (rt7[ia], rt7[ib]) == (1, 5) \
                        and (rt7[ia2], rt7[ib2]) == (1, 1) \
                        and dd7[ia].get(x, 0) == 0 \
                        and dd7[ib].get(x, 0) == 3:
                    gotR = (ia, ib, x)
    step("SC", "n7 samples: (0,3)=%s (1,3)=%s recharge=%s" %
         (got03, got13, gotR))
    if got03:
        bat.append((7, got03[0], got03[1], got03[2], "K", "tw03"))
    if got13:
        bat.append((7, got13[0], got13[1], got13[2], "K", "tw13"))
    if gotR:
        bat.append((7, gotR[0], gotR[1], gotR[2], "K", "recharge"))
    # n=7 §4 A-variants: same rootA=1, same B=right-vine, x=7
    def build(lo, hi):
        if lo > hi:
            return None
        k = (lo + hi) // 2
        return [k, build(lo, k - 1), build(k + 1, hi)]

    def build_rooted(lo, hi, k):
        return [k, build(lo, k - 1), build(k + 1, hi)]

    A_a1 = [1, build(1, 0), build_rooted(2, 7, 7)]
    # valid root-1 BST with 7 deep (right vine over 2..7): dA(7)=6, a=3
    A_a3 = [1, None, [2, None, [3, None, [4, None, [5, None, [6, None,
                                                          [7, None, None]]]]]]]

    def inorder(t):
        out = []

        def go(nd):
            if nd is None:
                return
            go(nd["l"])
            out.append(nd["k"])
            go(nd["r"])
        go(t)
        return out

    def is_vine_list(t):
        st = [t]
        while st:
            nd = st.pop()
            if nd is None:
                continue
            if nd[1] is not None and nd[2] is not None:
                return False
            st.append(nd[1])
            st.append(nd[2])
        return True

    for tag, A in (("S4a1", A_a1), ("S4a3", A_a3)):
        p = V.to_ptr(copy.deepcopy(A))
        dd = V.depths_of(p)
        ok = inorder(p) == list(range(1, 8)) and rootof(p) == 1
        step("A", "%s dA7=%s valid=%s" % (tag, dd.get(7), ok))
        if ok:
            bat.append((7, idx7[json.dumps(A, sort_keys=True)], 0, 7, "K",
                        tag))
    # §2-construction edge: non-vine A (branching M), same B/x as S4a1
    M2 = [4, [2, None, [3, None, None]], [6, [5, None, None], None]]
    A_s2 = [1, None, [7, M2, None]]
    p = V.to_ptr(copy.deepcopy(A_s2))
    dd = V.depths_of(p)
    ok = inorder(p) == list(range(1, 8)) and rootof(p) == 1
    vn = is_vine_list(A_s2)
    step("A", "S2nv dA7=%s valid=%s nonvine=%s" % (dd.get(7), ok, not vn))
    if ok:
        bat.append((7, idx7[json.dumps(A_s2, sort_keys=True)], 0, 7, "K",
                    "S2nv"))
    # A-control: non-vine root-1 A, dA(7)=3 (a=2), same B/x
    A_ctl = [1, None, [3, [2, None, None],
                       [5, [4, None, None], [7, [6, None, None], None]]]]
    p = V.to_ptr(copy.deepcopy(A_ctl))
    dd = V.depths_of(p)
    ok = inorder(p) == list(range(1, 8)) and rootof(p) == 1
    step("A", "ACTL dA7=%s valid=%s nonvine=%s" % (dd.get(7), ok,
                                                  not is_vine_list(A_ctl)))
    if ok:
        bat.append((7, idx7[json.dumps(A_ctl, sort_keys=True)], 0, 7, "K",
                    "ACTL"))
    # n=8 witnesses
    bat += [(8, 457, 429, 8, "K", "L2a"), (8, 1091, 1003, 7, "K", "L2b"),
            (8, 869, 910, 2, "K", "L2c"), (8, 1093, 1003, 7, "K", "L3b"),
            (8, 90, 2, 8, "K", "L4a"), (8, 255, 2, 8, "K", "L4c"),
            (8, 1001, 1359, 1, "K", "L4d"), (8, 1003, 1359, 1, "K", "L4e"),
            (8, 0, 89, 3, "K", "TR8")]
    # n=9 probe examples (mapping validated by probe script)
    P9 = json.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                            "0909c74a" / "dual_mine" / "l2_probe9.json"))
                   )["examples"]
    seen04 = seen14 = 0
    for e in P9:
        if e["a"] == 0 and seen04 < 2:
            bat.append((9, e["ia"], e["ib"], e["x"], "K", "PR904"))
            seen04 += 1
        if e["a"] == 1 and seen14 < 2:
            bat.append((9, e["ia"], e["ib"], e["x"], "K", "PR914"))
            seen14 += 1
    # instantiated A-free q=4 edge at n=9 (a=0, twin 0->1): first B with
    # dB(x)>=8 and rB!=x, paired with an A rooted at x. Canonical replay
    # below instantiates it (§10 rule).
    Sh9 = O.shapes_of(list(range(1, 10)))
    ptrs9 = [V.to_ptr(copy.deepcopy(s)) for s in Sh9]
    rt9 = [rootof(p) for p in ptrs9]
    dd9 = [V.depths_of(p) for p in ptrs9]
    pr = None
    for ib in range(len(Sh9)):
        for x in range(1, 10):
            if dd9[ib].get(x, 0) // 2 >= 4 and rt9[ib] != x:
                ia = next(i for i in range(len(Sh9)) if rt9[i] == x)
                pr = (ia, ib, x)
                break
        if pr:
            break
    step("PR", "instantiated A-free q=4: %s" % (pr,))
    if pr:
        bat.append((9, pr[0], pr[1], pr[2], "K", "PR904"))
    try:
        EX = json.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                                "0909c74a" / "vine_excursion" /
                                "exc_n7.json")))
        step("EX", "exc_n7 keys=%s" % sorted(EX.keys())[:8])
    except Exception as ex:
        step("EX", "unavailable: %s" % ex)
    SH = {7: Sh7, 8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    CANDS = ["C1", "C3", "C4", "C5"]
    fails = {}
    for (n, ia, ib, x, mo, tag) in bat:
        Sh = SH[n]
        keys = list(range(1, (8 if n == 7 else (9 if n == 8 else 10))))
        rep = V.replay(Sh[ia], Sh[ib], [(mo, x)])
        acc = rep["accesses"][0]
        w = acc["eps"]
        pA = V.to_ptr(copy.deepcopy(Sh[ia]))
        pB = V.to_ptr(copy.deepcopy(Sh[ib]))
        pA2 = V.to_ptr(copy.deepcopy(rep["endA"]))
        pB2 = V.to_ptr(copy.deepcopy(rep["endB"]))
        line = []
        for cn in CANDS:
            f0, tw0 = phi_cand(cn, pA, pB, keys)
            f1, tw1 = phi_cand(cn, pA2, pB2, keys)
            drop = f0 - f1
            ok = drop >= w
            line.append("%s:%+d%s" % (cn, drop, "" if ok else "*"))
            if not ok:
                fails.setdefault(cn, []).append(
                    (tag, n, ia, ib, x, mo, acc["a"], acc["q"], w,
                     tw0, tw1, f0, f1, drop))
        step("T", "%s n=%d (%d,%d)x%d %s a=%d q=%d w=%d | %s" %
             (tag, n, ia, ib, x, mo, acc["a"], acc["q"], w, " ".join(line)))
    step("S", "battery=%d %s" %
         (len(bat), {c: len(fails.get(c, [])) for c in CANDS}))
    json.dump({"fails": {c: fails.get(c, []) for c in CANDS},
               "n": len(bat), "candidates": CANDS},
              open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                       "0909c74a" / "dual_mine" / "c1_battery.json"), "w"),
              indent=1, default=str)
    return 0


if __name__ == "__main__":
    sys.exit(main())
