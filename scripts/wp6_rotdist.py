"""PIVOT-25R-R §5: exact rotation-distance payment falsifier.

Builds the primitive-rotation graph on all n-key BSTs, exact rho via BFS,
single-StepEv emulation (mirroring splay_cap), then checks EVERY triple
(A,B,x) with root(A)=x: (RD) B-double => rho drops >=1; (RZ) final zig
=> rho does not rise. Saves smallest counterexamples.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[RDD %s] %s" % (sid, msg), flush=True)


def single_step(root, x):
    """Exactly one canonical splay StepEv at x (mirrors splay_cap).
    Returns (newroot, kind) with kind in zig/zigzig/zigzag/none."""
    import liquidity.legacy_embedding as PE
    d, path = PE._depth_to(root, x)
    if not path or path[-1]["k"] != x:
        return root, "absent"
    node = path[-1]
    if node["p"] is None:
        return root, "none"
    p = node["p"]
    g = p["p"]
    if g is None:
        if p["l"] is node:
            PE._rot_right(p)
        else:
            PE._rot_left(p)
        kind = "zig"
    else:
        if p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            kind = "zigzig"
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            kind = "zigzig"
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            kind = "zigzag"
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            kind = "zigzag"
    while node["p"] is not None:
        node = node["p"]
    return node, kind


def enc(P):
    if P is None:
        return None
    return [P["k"], enc(P["l"]), enc(P["r"])]


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 6
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    step("G", "n=%d shapes=%d" % (n, nS))
    # rotation graph: single left/right rotation at every eligible node
    import liquidity.legacy_embedding as PE
    adj = [set() for _ in range(nS)]
    for ia in range(nS):
        for y in range(1, n + 1):
            for side, fn in (("l", PE._rot_right), ("r", PE._rot_left)):
                P = V.to_ptr(copy.deepcopy(Sh[ia]))
                # find node y
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
                # rotate at nd (nd goes down, child comes up): fn takes the
                # node that moves down? check convention: _rot_right(p)
                # rotates p right (p down, left child up).
                fn(nd)
                r = nd
                while r["p"] is not None:
                    r = r["p"]
                jb = idx[json.dumps(enc(r), sort_keys=True)]
                if jb != ia:
                    adj[ia].add(jb)
    # all-pairs rho via BFS
    INF = 10 ** 9
    rho = [[INF] * nS for _ in range(nS)]
    for s in range(nS):
        rho[s][s] = 0
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if rho[s][w] == INF:
                    rho[s][w] = rho[s][u] + 1
                    dq.append(w)
    import numpy as np
    R = np.array(rho)
    assert np.all(R < INF), "rotation graph must be connected"
    step("G", "rotation graph connected; diameter=%d" % R.max())
    # verify single-step emulation vs splay_cap first step on samples
    import random
    rng = random.Random(5)
    for _ in range(200):
        ia = rng.randrange(nS)
        x = rng.randint(1, n)
        P1 = V.to_ptr(copy.deepcopy(Sh[ia]))
        P1, iv = V.splay_cap(P1, x, 0, [])
        P2 = V.to_ptr(copy.deepcopy(Sh[ia]))
        P2, kd = single_step(P2, x)
        # compare after ONE step: replay splay_cap is full; emulate prefix:
        # instead check: single step then full splay_cap == full splay_cap
        P3 = V.to_ptr(copy.deepcopy(Sh[ia]))
        P3, _ = single_step(P3, x)
        P3, _ = V.splay_cap(P3, x, 0, [])
        assert enc(P1) == enc(P3), (ia, x, kd)
    step("V", "single-step emulation consistent (200/200)")
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
        for ib in range(nS):
            r0 = rho[ia][ib]
            for x in range(1, n + 1):
                if rt[ia] != x:
                    continue
                P = V.to_ptr(copy.deepcopy(Sh[ib]))
                d = V.depths_of(P).get(x, 0)
                if d == 0:
                    continue
                P2, kd = single_step(copy.deepcopy(P), x)
                jb = shape_of(P2)
                r1 = rho[ia][jb]
                if d >= 2:
                    nrd += 1
                    if not (r1 <= r0 - 1):
                        if len(rd_bad) < 5:
                            rd_bad.append((ia, ib, x, kd, d, r0, r1))
                else:
                    nrz += 1
                    if not (r1 <= r0):
                        if len(rz_bad) < 5:
                            rz_bad.append((ia, ib, x, kd, d, r0, r1))
        if (ia + 1) % 44 == 0:
            step("T", "%d/%d RDviol=%d RZviol=%d" %
                 (ia + 1, nS, len(rd_bad), len(rz_bad)))
    step("S", "n=%d triples: doubles=%d RDviol-sample=%d; zigs=%d RZviol=%d" %
         (n, nrd, len(rd_bad), nrz, len(rz_bad)))
    out = {"n": n, "shapes": nS, "diameter": int(R.max()), "ndouble": nrd,
           "nzig": nrz, "rd_bad": rd_bad, "rz_bad": rz_bad}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("rotdist%d.json" % n)).write_text(
        json.dumps(out, indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
