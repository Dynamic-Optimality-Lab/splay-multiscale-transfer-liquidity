"""PIVOT-14 U4-core: hunt dangerous accesses (a>=1, q-2a>=3) in closed cycles.

Generator: build B-depth for x (many other-key KEEPs), DELETE x (A-root, B
frozen), optional single dethroner, KEEP x. BFS-close at n=6 via pair-graph.
For each closed cycle with dangerous access: cyclic charge + Q-2A classify.
Also: broad random/bred scan recording max (q-2a | a>=1).
"""
from __future__ import annotations
import sys
import json
import copy
import random
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_siege as S
import wp6_cycle_ratio as O
from wp6_ovf_anal import vine


def bfs_close(adj, s_end, s_start):
    """BFS path of (mode,key) from s_end to s_start. None if unreachable."""
    prev = {s_end: None}
    dq = deque([s_end])
    while dq:
        u = dq.popleft()
        if u == s_start:
            break
        for (to, md, x, _a, _b) in adj[u]:
            if to not in prev:
                prev[to] = (u, md, x)
                dq.append(to)
    if s_start not in prev:
        return None
    path = []
    u = s_start
    while prev[u] is not None:
        pu, md, x = prev[u]
        path.append((md, x))
        u = pu
    path.reverse()
    return path


def trace_states(n, sA, sB, w):
    A = V.to_ptr(copy.deepcopy(sA))
    B = V.to_ptr(copy.deepcopy(sB))
    tr = [(S.enc_shape(A), S.enc_shape(B))]
    for i, (md, x) in enumerate(w):
        A, _ = V.splay_cap(A, x, i, [])
        if md == "K":
            B, _ = V.splay_cap(B, x, i, [])
        tr.append((S.enc_shape(A), S.enc_shape(B)))
    return tr


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 51
    ntrials = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    rng = random.Random(seed)
    n = 6
    T0 = vine(n)
    G = O.build(n)
    nS, adj = G["nS"], G["adj"]
    V.step("D-0", "danger hunt seed=%d trials=%d" % (seed, ntrials))
    best = (0, None)  # (maxeps_a1, info)
    dangerous = []
    tested_closed = 0
    for t in range(ntrials):
        x = rng.randint(1, n)
        others = [k for k in range(1, n + 1) if k != x]
        rng.shuffle(others)
        # build phase: deep KEEPs of others (each splayed from vine-ish depth)
        w = [("K", k) for k in others * rng.randint(1, 3)]
        w += [("D", x)]
        if rng.random() < 0.7:
            w += [(rng.choice(["K", "D"]), rng.choice(others))]
        w += [("K", x)]
        rep = V.replay(T0, T0, w)
        legs = rep["accesses"]
        cand = [(a["a"], a["q"], a["eps"]) for a in legs
                if a["m"] == "K" and a["a"] >= 1]
        if not cand:
            continue
        me = max(e for (_, _, e) in cand)
        if me > best[0]:
            best = (me, (w, cand))
        if me >= 3:
            # close it: trace end state -> BFS back to start state
            tr = trace_states(n, T0, T0, w)
            # map enc-shapes to pair ids: need Sh index; use adj walk instead:
            # replay word through adj from start id
            ia0 = ib0 = 0  # vine index? find vine idx
            # find vine shape idx
            Sh = G["Sh"]
            import json as J
            vj = J.dumps(T0, sort_keys=True)
            # Sh entries are lists; T0 vine list: compare
            vi = next(i for i, s in enumerate(Sh) if J.dumps(s, sort_keys=True) == vj)
            u = vi * nS + vi
            for (md, xk) in w:
                for (to, md2, x2, _a, _b) in adj[u]:
                    if md2 == md and x2 == xk:
                        u = to
                        break
            u_end = u
            u_start = vi * nS + vi
            closer = bfs_close(adj, u_end, u_start)
            if closer is None:
                continue
            wc = w + closer
            r = S.cyclic_test(T0, T0, wc)
            tested_closed += 1
            A, Q = r["A"], r["Q"]
            dangerous.append({"w": wc, "lap2full": r["lap2full"],
                              "A": A, "Q": Q, "WQ": Q - 2 * A,
                              "hall": r.get("hall")})
            V.step("D-1", "DANGEROUS closed len=%d lap2full=%s A=%d Q=%d WQ=%d" %
                   (len(wc), r["lap2full"], A, Q, Q - 2 * A))
    V.step("D-2", "best non-starved eps=%s tested_closed=%d dangerous=%d" %
           (best[0], tested_closed, len(dangerous)))
    if best[1]:
        V.step("D-2", "best word=%s legs=%s" % (best[1][0], best[1][1]))
    V.save("danger.json", {"seed": seed, "best": best[0],
                           "dangerous": dangerous})
    return 0


if __name__ == "__main__":
    sys.exit(main())
