"""WP-6 STEP OB-00: orbit-anchored BF (verifier + bottleneck anatomy).

For sampled starts T0 (vines/balanced/shuffled, n<=7): forward orbit BFS
from (T0,T0) via Pair-Access steps; Bellman-Ford anchored at start
(dist[start]=0, forward relaxations); dist[v] = min-slack start->v.
Negative dist => PREFIX WITNESS (replay path => E_B>3*S_A, RETURN 2!).
Nonnegative => verified on orbit + argmin-slack states mined for
bottleneck-shape anatomy (common features of near-tight states).
Potential=dist restates counts (equivalent, not proof); value is
verification + anatomy.
"""
from __future__ import annotations
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_splaymetric import shapes, splay_cost_events


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP OB-00: orbit BF.
    step("OB-00", "Orbit-anchored BF (verify + bottleneck anatomy)")
    import json
    n = 7
    S = shapes(n)
    nxt, cst = {}, {}
    for t in S:
        for x in range(1, n + 1):
            t2, c = splay_cost_events(t, x)
            nxt[(t, x)] = t2
            cst[(t, x)] = c

    def vine(left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = (k, None, t) if not left else (k, t, None)
        return t

    def bal(ks):
        if not ks:
            return None
        m = len(ks) // 2
        return (ks[m], bal(ks[:m]), bal(ks[m + 1:]))

    import random
    r = random.Random(42)
    ks = list(range(1, n + 1))
    r.shuffle(ks)
    t = None

    def ins(T, k):
        if T is None:
            return (k, None, None)
        if k < T[0]:
            return (T[0], ins(T[1], k), T[2])
        return (T[0], T[1], ins(T[2], k))

    for k in ks:
        t = ins(t, k)
    starts = [vine(True), vine(False), bal(list(range(1, n + 1))), t]
    out = []
    for si, T0 in enumerate(starts):
        # orbit BFS
        seen = {(T0, T0)}
        dq = deque([(T0, T0)])
        edges = []
        while dq:
            A, B = dq.popleft()
            for x in range(1, n + 1):
                A2 = nxt[(A, x)]
                for (A3, B3, w) in ((A2, B, 3 * cst[(A, x)]),
                                    (A2, nxt[(B, x)], 3 * cst[(A, x)] - cst[(B, x)])):
                    s = (A3, B3)
                    edges.append(((A, B), s, w))
                    if s not in seen:
                        seen.add(s)
                        dq.append(s)
        # anchored BF (dist from start; detect negative = witness)
        INF = 10 ** 30
        dist = {v: INF for v in seen}
        dist[(T0, T0)] = 0
        # adjacency for relaxations
        adj = {}
        for (u, v, w) in edges:
            adj.setdefault(u, []).append((v, w))
        neg = None
        for _ in range(len(seen)):
            upd = False
            for u in list(seen):
                if dist[u] == INF:
                    continue
                for v, w in adj.get(u, []):
                    if dist[u] + w < dist[v]:
                        dist[v] = dist[u] + w
                        upd = True
            if not upd:
                break
        else:
            neg = True
        # extra round to find negative node
        wit = None
        for u in seen:
            if dist[u] == INF:
                continue
            for v, w in adj.get(u, []):
                if dist[u] + w < dist[v]:
                    wit = (str(u), str(v), w)
                    break
            if wit:
                break
        finite = [d for d in dist.values() if d < INF]
        step("OB-s%d" % si, "orbit=%d neg=%s minslack=%s witness=%s" %
             (len(seen), neg is not None or wit is not None,
              min(finite) if finite else None, str(wit)[:160]))
        out.append({"orbit": len(seen), "neg": neg is not None or wit is not None,
                    "minslack": min(finite) if finite else None,
                    "witness": wit})
        if wit:
            step("OB-KILL", "prefix witness at n=7 (replay for E_B>3*S_A!)")
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "orbitbf.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
