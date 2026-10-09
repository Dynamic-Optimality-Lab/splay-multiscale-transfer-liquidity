"""PIVOT-25R-R §7A: interval-disagreement D2 = |I(A) triangle I(B)|/2.

I(T) = set of subtree inorder intervals (lo,hi) over all nodes.
Per-rotation Lipschitz<=1 PROVED structurally (Ix_new == Ip_old as sets:
net one removal + one addition) and asserted over every rotation at n.
Then EVERY triple (A,B,x), root(A)=x, B-double-able: D2 must drop >=1;
final zig must not rise. Saves smallest counterexamples.
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
from wp6_rotdist import single_step, enc


def step(sid, msg):
    print("[IVD %s] %s" % (sid, msg), flush=True)


def intervals(t):
    """Set of (lo,hi) subtree intervals over all nodes of list-shape."""
    out = set()

    def go(nd):
        if nd is None:
            return (None, None)
        l = go(nd[1])
        r = go(nd[2])
        lo = nd[0] if l[0] is None else l[0]
        hi = nd[0] if r[1] is None else r[1]
        out.add((lo, hi))
        return (lo, hi)
    go(t)
    return out


def D2(A, B):
    ia, ib = intervals(A), intervals(B)
    assert len(ia) == len(ib)
    return (len(ia - ib) + len(ib - ia)) // 2


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    import liquidity.legacy_embedding as PE
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 6
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    # Lipschitz: every primitive rotation changes D2 by <={-1,0,1}.
    # Check all ordered shape pairs differing by one rotation is implied by
    # checking all single rotations from every shape against every A.
    worst = 0
    for ia in range(nS):
        for ib in range(nS):
            d0 = D2(Sh[ia], Sh[ib])
            for y in range(1, n + 1):
                for side, fn in (("l", PE._rot_right), ("r", PE._rot_left)):
                    P = V.to_ptr(copy.deepcopy(Sh[ib]))
                    stack = [P]
                    nd = None
                    while stack:
                        m = stack.pop()
                        if m["k"] == y:
                            nd = m
                            break
                        if m["l"] is not None:
                            stack.append(m["l"])
                        if m["r"] is not None:
                            stack.append(m["r"])
                    if nd is None or nd[side] is None:
                        continue
                    fn(nd)
                    r = nd
                    while r["p"] is not None:
                        r = r["p"]
                    from wp6_rotdist import enc as _enc
                    B2 = _enc(r)
                    d1 = D2(Sh[ia], B2)
                    worst = max(worst, abs(d1 - d0))
    step("L", "per-rotation |dD2| max=%d (need <=1)" % worst)
    assert worst <= 1, "Lipschitz-1 FAILED"
    # triple check
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = []
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt.append(r["k"])

    def shape_of(P):
        return idx[json.dumps(enc(P), sort_keys=True)]

    rd_bad, rz_bad, nrd, nrz = [], [], 0, 0
    for ia in range(nS):
        A0 = Sh[ia]
        for ib in range(nS):
            r0 = D2(A0, Sh[ib])
            for x in range(1, n + 1):
                if rt[ia] != x:
                    continue
                P = V.to_ptr(copy.deepcopy(Sh[ib]))
                d = V.depths_of(P).get(x, 0)
                if d == 0:
                    continue
                P2, kd = single_step(copy.deepcopy(P), x)
                r1 = D2(A0, enc(P2))
                if d >= 2:
                    nrd += 1
                    if not (r1 <= r0 - 1) and len(rd_bad) < 200:
                        rd_bad.append((ia, ib, x, kd, d, r0, r1))
                else:
                    nrz += 1
                    if not (r1 <= r0) and len(rz_bad) < 200:
                        rz_bad.append((ia, ib, x, kd, d, r0, r1))
    step("S", "n=%d doubles=%d RDviol=%d; zigs=%d RZviol=%d" %
         (n, nrd, len(rd_bad), nrz, len(rz_bad)))
    out = {"n": n, "lip_max": worst, "ndouble": nrd, "nzig": nrz,
           "rd_nviol": len(rd_bad), "rz_nviol": len(rz_bad),
           "rd_bad": rd_bad[:8], "rz_bad": rz_bad[:8]}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("interval%d.json" % n)).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
