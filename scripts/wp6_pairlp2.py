"""WP-6 STEP LP2-00: staged pair-potential LP (pure witness vs full Phi).

STAGE P (differences-only, super-source S->v, NO v->S: negative cycles are
PURE-TRANSITION (replayable!). INFEASIBLE => periodic E_B>3*S_A witness
=> independent replay (E_B-ratio, J3, 14P-viol) => RETURN 2 if confirmed.
STAGE F (full: + diag-pin S<->diag(0) + Phinonneg v->S(0) all v):
FEASIBLE => Phi potential (mine for closed form). Teleport-cycles here are
Farkas (no-Phi) but NOT replayable; distinguish pure vs teleport.
n=5 BF-exact; n=6 SPFA-bounded if time permits.
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
    seen = set()
    dq = deque()
    for t0 in S:
        seen.add((t0, t0))
        dq.append((t0, t0))
    while dq:
        A, B = dq.popleft()
        for x in range(1, n + 1):
            for s in ((nxt[(A, x)], B), (nxt[(A, x)], nxt[(B, x)])):
                if s not in seen:
                    seen.add(s)
                    dq.append(s)
    nodes = list(seen)
    idx = {v: i for i, v in enumerate(nodes)}
    tedges = []
    for (A, B) in nodes:
        u = idx[(A, B)]
        for x in range(1, n + 1):
            A2 = nxt[(A, x)]
            tedges.append((u, idx[(A2, B)], 3 * cst[(A, x)], "D", x))
            B2 = nxt[(B, x)]
            tedges.append((u, idx[(A2, B2)], 3 * cst[(A, x)] - cst[(B, x)], "K", x))
    return nodes, tedges


def bf_pure(nV, edges):
    """Differences-only (super-source init 0). Neg cycle => pure (replayable)."""
    INF = 10 ** 30
    dist = [0] * nV
    parent = [-1] * nV
    pe = [None] * nV
    x = -1
    for _ in range(nV):
        x = -1
        for (u, v, w, m, k) in edges:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                pe[v] = (u, m, k, w)
                x = v
    if x == -1:
        return {"feasible": True, "dist": dist}
    y = x
    for _ in range(nV):
        y = parent[y]
    cyc, cur = [], y
    while True:
        cyc.append((cur, pe[cur]))
        cur = pe[cur][0]
        if cur == y or len(cyc) > nV + 5:
            break
    return {"feasible": False, "cycle": cyc}


def bf_full(nV, edges, diag_ids):
    """Full LP: + super S (nV): S->v (0) all [super-source],
    v->S (0) all [Phi>=0], S<->d (0) diag [diag-pin, redundant w/ above
    except diag<=0 from S->d]. Teleport cycles (via S) are Farkas
    (no-Phi), NOT replayable. Returns feasible/pure-vs-teleport info."""
    N = nV + 1
    S = nV
    E = list(edges)
    for v in range(nV):
        E.append((S, v, 0, "S", -1))
        E.append((v, S, 0, "B", -1))
    INF = 10 ** 30
    dist = [0] * N
    parent = [-1] * N
    pe = [None] * N
    x = -1
    for _ in range(N):
        x = -1
        for (u, v, w, m, k) in E:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                parent[v] = u
                pe[v] = (u, m, k, w)
                x = v
    if x == -1:
        phi = dist[:nV]
        return {"feasible": True, "phi": phi}
    y = x
    for _ in range(N):
        y = parent[y]
    cyc, cur = [], y
    usesS = False
    while True:
        cyc.append((cur, pe[cur]))
        if cur == S or pe[cur][0] == S:
            usesS = True
        cur = pe[cur][0]
        if cur == y or len(cyc) > N + 5:
            break
    return {"feasible": False, "teleport": usesS, "len": len(cyc)}


def main() -> int:
    # WP-6 STEP LP2-00: staged LP.
    step("LP2-00", "Staged pair-potential LP")
    import json
    out = {}
    for n in (5,):
        nodes, tedges = build(n)
        step("LP2-n%d" % n, "pairs=%d tedges=%d" % (len(nodes), len(tedges)))
        r = bf_pure(len(nodes), tedges)
        if not r["feasible"]:
            cyc = r["cycle"]
            wsum = sum(e[1][3] for e in cyc)
            # replay access pattern from cycle (pe order is reversed!)
            pat = [(e[1][1], e[1][2]) for e in reversed(cyc)]
            step("LP2-n%d" % n, "PURE-INFEASIBLE len=%d wsum=%d" % (len(cyc), wsum))
            step("LP2-n%d" % n, "pattern=%s" % pat[:20])
            out[str(n)] = {"pure": False, "len": len(cyc), "wsum": wsum,
                           "pattern": pat}
        else:
            dg = [i for i, v in enumerate(nodes) if v[0] == v[1]]
            dv = [r["dist"][i] for i in dg]
            step("LP2-n%d" % n, "PURE-FEASIBLE; diag dist min=%d max=%d; global min=%d" %
                 (min(dv), max(dv), min(r["dist"])))
            out[str(n)] = {"pure": True, "diag_min": min(dv),
                           "diag_max": max(dv), "global_min": min(r["dist"])}
            # STAGE F: full LP (diag-pin + nonnegativity)
            rf = bf_full(len(nodes), tedges, dg)
            if rf["feasible"]:
                import statistics as _st
                ph = rf["phi"]
                step("LP2-n%d" % n, "FULL-FEASIBLE; Phi range [%d,%d] diagmax=%d" %
                     (min(ph), max(ph), max(ph[i] for i in dg)))
                out[str(n)]["full"] = True
                out[str(n)]["phi_min"] = min(ph)
                out[str(n)]["phi_max"] = max(ph)
                # mine: Phi vs Delta/reverse/root-features on sample
                out[str(n)]["phi_sample"] = [[str(nodes[i]), ph[i]] for i in range(0, len(nodes), max(1, len(nodes)//12))]
            else:
                step("LP2-n%d" % n, "FULL-INFEASIBLE teleport=%s len=%d" %
                     (rf["teleport"], rf["len"]))
                out[str(n)]["full"] = False
                out[str(n)]["teleport"] = rf["teleport"]
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pairlp2.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
