"""PIVOT-22 n=7 exact decision: Bellman-Ford feasibility on c=-w (integers).

Finds positive-W_Q cycle (=> NO certificate) or certifies none via dual
potentials (YES n=7, independently verifiable). Early exit; diameter-bound
passes expected on splay pair-graph.
"""
from __future__ import annotations
import sys
import json
import pickle
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))


def step(sid, msg):
    print("[BF %s] %s" % (sid, msg), flush=True)


def main():
    import wp6_howard as H
    n = 7
    n, nS, Sh, Atrans, Btrans, dA, dB = H.load(n)
    Vcount = nS * nS
    N = 2 * n
    step("B-0", "V=%d E=%d" % (Vcount, Vcount * N))
    # materialize edges as (u, to, c=-w) int lists for speed
    Eu, Et, Ec = [], [], []
    for u in range(Vcount):
        ia, ib = u // nS, u % nS
        for x in range(1, n + 1):
            ia2, a = Atrans[(ia, x)]
            Eu.append(u)
            Et.append(ia2 * nS + ib)
            Ec.append(2 * a)  # c = -w = 2a (DELETE q=0)
            ib2, _ = Btrans[(ib, x)]
            Eu.append(u)
            Et.append(ia2 * nS + ib2)
            Ec.append(2 * a - dB[(ib, x)] // 2)  # c = 2a-q
    E = len(Eu)
    step("B-0", "materialized %d edges" % E)
    import array
    dist = [0] * Vcount
    parent = [-1] * Vcount
    # Bellman-Ford passes with early exit
    for i in range(Vcount):
        changed = False
        for j in range(E):
            u, v, c = Eu[j], Et[j], Ec[j]
            nd = dist[u] + c
            if nd < dist[v]:
                dist[v] = nd
                parent[v] = u
                changed = True
        if (i + 1) % 10 == 0:
            step("B-1", "pass %d" % (i + 1))
        if not changed:
            step("B-2", "FEASIBLE after %d passes (no positive-W cycle)" %
                 (i + 1))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf7.json").write_text(json.dumps(
                 {"feasible": True, "passes": i + 1, "V": Vcount, "E": E}),
                encoding="utf-8")
            pickle.dump({"dist": dist},
                        open(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "bf7.pkl", "wb"))
            return 0
    # V passes with changes => negative cycle (positive-W cycle). Extract.
    step("B-2", "NEGATIVE CYCLE detected (positive-W cycle exists)")
    y = -1
    # find a node relaxed in last pass: re-run one pass tracking
    for j in range(E):
        u, v, c = Eu[j], Et[j], Ec[j]
        if dist[u] + c < dist[v]:
            dist[v] = dist[u] + c
            parent[v] = u
            y = v
    for _ in range(Vcount):
        y = parent[y]
    cyc = []
    cur = y
    while True:
        cyc.append(cur)
        cur = parent[cur]
        if cur == y or len(cyc) > Vcount + 5:
            break
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "bf7.json").write_text(json.dumps(
         {"feasible": False, "cycle": cyc,
          "nodelabels": [[c // nS, c % nS] for c in cyc[:20]]}),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
