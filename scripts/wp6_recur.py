"""PIVOT-25R-R §7B: deletion-normalized recursive alignment energy.

E(A,B): identical -> 0; roots agree r -> E(L)+E(R) on shared intervals;
roots differ -> 1 + E(del_{rA}(A), del_{rA}(B)) [successor-splice,
deterministic; n-1 keys; well-founded]. Tested as D=E and D=-2twin+E
on the 21-edge hard battery (canonical replays). A failure refutes the
candidate (not joint/recursive potentials in general).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[RCA %s] %s" % (sid, msg), flush=True)


def demote(t):
    if t is None:
        return None
    return [t[0], demote(t[1]), demote(t[2])]


def delkey(t, k):
    """Canonical BST deletion (successor-splice, else predecessor)."""
    if t is None:
        return None
    if k < t[0]:
        return [t[0], delkey(t[1], k), t[2]]
    if k > t[0]:
        return [t[0], t[1], delkey(t[2], k)]
    # found
    if t[1] is None:
        return t[2]
    if t[2] is None:
        return t[1]
    # successor = min of right
    m = t[2]
    while m[1] is not None:
        m = m[1]
    return [m[0], t[1], delkey(t[2], m[0])]


def Erec(A, B, depth=0):
    assert depth < 64
    if A is None and B is None:
        return 0
    assert A is not None and B is not None
    if A == B:
        return 0
    if A[0] == B[0]:
        return Erec(A[1], B[1], depth + 1) + Erec(A[2], B[2], depth + 1)
    return 1 + Erec(delkey(A, A[0]), delkey(B, A[0]), depth + 1)


def twin_of(A, B):
    return 1 if A[0] == B[0] else 0


def main():
    import wp6_cycle_ratio as O
    # battery assembly (mirrors wp6_c1battery edge set incl. extensions)
    Sh7 = O.shapes_of(list(range(1, 8)))
    idx7 = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh7)}
    edges = [(7, 28, 0, 7, "K", "L1e1"), (7, 297, 428, 1, "K", "L1e2")]

    def build(lo, hi):
        if lo > hi:
            return None
        k = (lo + hi) // 2
        return [k, build(lo, k - 1), build(k + 1, hi)]

    def build_rooted(lo, hi, k):
        return [k, build(lo, k - 1), build(k + 1, hi)]

    A_a1 = [1, build(1, 0), build_rooted(2, 7, 7)]
    A_a3 = [1, None, [2, None, [3, None, [4, None, [5, None, [6, None,
                                                          [7, None, None]]]]]]]
    M2 = [4, [2, None, [3, None, None]], [6, [5, None, None], None]]
    A_s2 = [1, None, [7, M2, None]]
    A_ctl = [1, None, [3, [2, None, None],
                       [5, [4, None, None], [7, [6, None, None], None]]]]
    for tag, A in (("S4a1", A_a1), ("S4a3", A_a3), ("S2nv", A_s2),
                   ("ACTL", A_ctl)):
        edges.append((7, idx7[json.dumps(A, sort_keys=True)], 0, 7, "K",
                      tag))
    SH = {7: Sh7, 8: O.shapes_of(list(range(1, 9))),
          9: O.shapes_of(list(range(1, 10)))}
    D7 = __import__("pickle").load(open(str(ROOT / "artifacts" / "v04" /
                                            "wp6_present" / "0909c74a" /
                                            "trans7.pkl"), "rb"))
    A7, B7 = D7["Atrans"], D7["Btrans"]
    ptrs7 = [V.to_ptr(copy.deepcopy(s)) for s in SH[7]]

    def rootof(p):
        r = p
        while r["p"] is not None:
            r = r["p"]
        return r["k"]
    rt7 = [rootof(p) for p in ptrs7]
    dd7 = [V.depths_of(p) for p in ptrs7]
    got03 = got13 = gotR = None
    for ia in range(len(SH[7])):
        for ib in range(len(SH[7])):
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
    if got03:
        edges.append((7, got03[0], got03[1], got03[2], "K", "tw03"))
    if got13:
        edges.append((7, got13[0], got13[1], got13[2], "K", "tw13"))
    if gotR:
        edges.append((7, gotR[0], gotR[1], gotR[2], "K", "recharge"))
    edges += [(8, 457, 429, 8, "K", "L2a"), (8, 1091, 1003, 7, "K", "L2b"),
              (8, 869, 910, 2, "K", "L2c"), (8, 1093, 1003, 7, "K", "L3b"),
              (8, 90, 2, 8, "K", "L4a"), (8, 255, 2, 8, "K", "L4c"),
              (8, 1001, 1359, 1, "K", "L4d"), (8, 1003, 1359, 1, "K",
                                               "L4e"),
              (8, 0, 89, 3, "K", "TR8"),
              (9, 297, 0, 9, "K", "PR914"), (9, 3432, 0, 9, "K", "PR904")]
    fails = {"E": [], "tE": []}
    for (n, ia, ib, x, mo, tag) in edges:
        Sh = SH[n]
        rep = V.replay(Sh[ia], Sh[ib], [(mo, x)])
        acc = rep["accesses"][0]
        w = acc["eps"]
        e0 = Erec(Sh[ia], Sh[ib])
        e1 = Erec(rep["endA"], rep["endB"])
        t0, t1 = twin_of(Sh[ia], Sh[ib]), twin_of(rep["endA"], rep["endB"])
        okE = (e0 - e1) >= w
        oktE = (-2 * t0 + e0) - (-2 * t1 + e1) >= w
        step("T", "%s n=%d a=%d q=%d w=%d E %d->%d d=%+d%s | tE d=%+d%s" %
             (tag, n, acc["a"], acc["q"], w, e0, e1, e0 - e1,
              "" if okE else " *FAIL*",
              (-2 * t0 + e0) - (-2 * t1 + e1), "" if oktE else " *FAIL*"))
        if not okE:
            fails["E"].append((tag, w, e0 - e1))
        if not oktE:
            fails["tE"].append((tag, w, (-2 * t0 + e0) - (-2 * t1 + e1)))
    step("S", "battery=%d E-fails=%d tE-fails=%d" %
         (len(edges), len(fails["E"]), len(fails["tE"])))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "recur_battery.json").write_text(
        json.dumps(fails, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
