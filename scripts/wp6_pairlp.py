"""WP-6 STEP LP-00: pair-potential LP via Bellman-Ford (DECISION at fixed n).

Constraints (reachable pair-states from diagonal, Pair-Access steps):
  Phi(T,T) = 0  (diagonal; enforce Phi<=0 and Phi>=0 via super-source? we
                 fix by checking: feasibleжки with Phi(diag)=0 shift-invariant?
                 NOT shift-invariant (Phi>=0 + laws). Handle: add super-source
                 0-edges + require min Phi 0 on diagonal via post-check.)
  DELETE x: Phi(S_xA,B) - Phi(A,B) <= 3*e_A.
  KEEP x:   Phi(S_xA,S_xB) - Phi(A,B) <= 3*e_A - e_B.
  Phi >= 0 (all).
Feasible => Phi potential => E_B<=3*S_A (telescope). Mine Phi for formula.
Infeasible => negative reachable cycle => PERIODIC E_B>3*S_A witness
  => replay independently (E_B-ratio, J3-stock, 14P-violations).
  If replay confirms: RETURN 2. If denies: transition-cost bug (but
  tuple-splay validated 0/500).
Bellman-Ford exact (n=5: 1764 pairs; SPFA attempt n=6/7 bounded).
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


def build(n):
    S = shapes(n)
    nxt, cst = {}, {}
    for t in S:
        for x in range(1, n + 1):
            t2, c = splay_cost_events(t, x)
            nxt[(t, x)] = t2
            cst[(t, x)] = c
    # reachable pairs from diagonals
    seen = set()
    dq = deque()
    for t0 in S:
        seen.add((t0, t0))
        dq.append((t0, t0))
    edges = []  # (u_idx, v_idx, w, mode, x)
    while dq:
        A, B = dq.popleft()
        for x in range(1, n + 1):
            A2 = nxt[(A, x)]
            s = (A2, B)
            if s not in seen:
                seen.add(s)
                dq.append(s)
            s = (A2, nxt[(B, x)])
            if s not in seen:
                seen.add(s)
                dq.append(s)
    nodes = list(seen)
    idx = {v: i for i, v in enumerate(nodes)}
    for (A, B) in nodes:
        u = idx[(A, B)]
        for x in range(1, n + 1):
            A2 = nxt[(A, x)]
            edges.append((u, idx[(A2, B)], 3 * cst[(A, x)], "D", x))
            B2 = nxt[(B, x)]
            edges.append((u, idx[(A2, B2)], 3 * cst[(A, x)] - cst[(B, x)], "K", x))
    return nodes, edges


def bellman_ford(nV, edges, source_extra=True):
    """Shortest paths with super-source (0 edges). Returns dist or neg-cycle."""
    INF = 10 ** 30
    dist = [0] * nV  # super-source init (0 to all) detects any neg cycle
    parent = [-1] * nV
    pe = [None] * nV
    x = -1
    for i in range(nV):
        x = -1
        for (u, v, w, m, k) in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                pe[v] = (u, m, k, w)
                x = v
    if x == -1:
        return {"feasible": True, "dist": dist}
    # negative cycle: walk back nV to enter it
    y = x
    for _ in range(nV):
        y = parent[y]
    cyc = []
    cur = y
    while True:
        cyc.append((cur, pe[cur]))
        cur = pe[cur][0]
        if cur == y or len(cyc) > nV + 5:
            break
    return {"feasible": False, "cycle": cyc}


def main() -> int:
    # WP-6 STEP LP-00: LP decision.
    step("LP-00", "Pair-potential LP (Bellman-Ford decision)")
    import json
    out = {}
    for n in (5,):
        nodes, edges = build(n)
        step("LP-n%d" % n, "pairs=%d edges=%d" % (len(nodes), len(edges)))
        r = bellman_ford(len(nodes), edges)
        if r["feasible"]:
            # Phi = -dist (dist<=0 as shortest from super-source; Phi>=-dist?)
            # Standard: x_v = dist[v] satisfies x_v - x_u <= w. Phi = -x?
            # We need Phi(v')-Phi(v) <= w i.e. Phi satisfies same: Phi = dist.
            # dist<=0 (super-source 0-edges). Phi>=0 fails (dist<=0)!
            # Shift? Laws are translation-invariant (differences!) but Phi>=0
            # and Phi(diag)=0 break invariance. Feasible-differences + bounds:
            # need dist with Phi>=0, Phi(diag)=0. Take Phi = dist - minDiag?
            # min over diagonal... Let m = min dist on diagonal; Phi=dist-m:
            # Phi>=? dist can be < m off-diagonal (Phi<0!). Check.
            import statistics
            dg = [i for i, v in enumerate(nodes) if v[0] == v[1]]
            m = min(r["dist"][i] for i in dg)
            neg = sum(1 for d in r["dist"] if d - m < 0)
            step("LP-n%d" % n, "FEASIBLE-differences; Phi>=0 viol=%d (shift m=%d)"
                 % (n, neg, m))
            out[str(n)] = {"feasible_diff": True, "neg_after_shift": neg,
                           "m": m}
        else:
            cyc = r["cycle"]
            wsum = sum(e[1][3] for e in cyc)
            step("LP-n%d" % n, "INFEASIBLE; neg-cycle len=%d wsum=%d"
                 % (n, len(cyc), wsum))
            out[str(n)] = {"feasible_diff": False, "cycle_len": len(cyc),
                           "wsum": wsum,
                           "cycle": [(str(nodes[e[0]]), e[1][1], e[1][2]) for e in cyc[:12]]}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pairlp.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
