"""WP-6 STEP AP-00: C37 augmenting-path anatomy (greedy-vs-offline repair).

Replay killer Hmin (n=128 left-vine) with (a) canonical least-loaded greedy
(record assignment/starvation) and (b) optimal cap-3 max-flow with assignment
recovery. For the starving B-event(s): extract alternating repair paths
(b* -> O-neighbor a* -> greedy-assigned B there -> their O-homes -> ... ->
greedy-spare source) via BFS over (O-edges B->A, greedy-edges A->B).
Report: greedy homes of the 5 blockers' 15 units vs optimal homes; class
breakdown of optimal overflow placement (fresh E1 vs old K/E2/W/E4);
path list with (bev, acc, x, edge-class); structural resource enabling repair.
NEW artifact: augment.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic
from wp6_spread import vine
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    step("AP-00", "C37 augmenting-path anatomy")
    import json
    from collections import defaultdict, deque
    dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    n, T0, H = dk["n"], vine(dk["n"], dk["T0left"]), dk["Hmin"]
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre = g["pre"]
    na, nb = len(Aevs), len(Bevs)
    # (a) greedy
    load = {}
    Gassign = {}
    starve = []
    for j in range(nb):
        e = elig[j]
        cands = sorted((load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1])
        if not cands:
            continue
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
            Gassign[j] = i
        else:
            starve.append(j)
    step("AP-01", "greedy: B=%d starved=%s maxload=%d" % (nb, starve[:8], max(load.values()) if load else 0))
    # (b) optimal with assignment recovery
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    for j, e in enumerate(elig):
        es = set()
        for k in e:
            es |= e[k]
        for i in es:
            if Aevs[i][1]:
                D.add(1 + i, 1 + na + j, 1)
    f, _ = D.flow(S, T)
    Oassign = {}
    for j in range(nb):
        for (to, c, rev) in D.adj[1 + na + j]:
            pass
        # incoming flow: scan A-nodes' edges to this B-node with residual 0
        for i in range(na):
            for (to, c, rev) in D.adj[1 + i]:
                if to == 1 + na + j and c == 0 and Aevs[i][1]:
                    # edge existed (orig cap 1) and saturated => flow 1; verify edge existed:
                    Oassign[j] = i
                    break
            if j in Oassign:
                break
    step("AP-02", "optimal: flow=%d/%d assigned=%d" % (f, nb, len(Oassign)))
    # greedy-load per source under OPTIMAL homes (for comparison)
    from collections import Counter
    optclass = Counter()
    for j, i in Oassign.items():
        e = elig[j]
        lab = sorted(k for k in e if i in e[k])
        optclass[tuple(lab)] += 1
    # alternating repair BFS for first starved bev
    paths = []
    for bs in starve[:3]:
        # BFS: B-nodes via O-edges to A, A-nodes via greedy-edges to B
        prev = {("b", bs): None}
        dq = deque([("b", bs)])
        found = None
        while dq:
            typ, v = dq.popleft()
            if typ == "b":
                e = elig[v]
                ns = set(i for k in e for i in e[k] if Aevs[i][1])
                for a in ns:
                    if ("a", a) not in prev:
                        prev[("a", a)] = ("b", v)
                        # spare under greedy?
                        if load.get(a, 0) < 3:
                            found = ("a", a)
                            dq.clear()
                            break
                        dq.append(("a", a))
            else:
                for b2, a2 in Gassign.items():
                    if a2 == v and ("b", b2) not in prev:
                        prev[("b", b2)] = ("a", v)
                        dq.append(("b", b2))
        if found is None:
            paths.append({"bev": bs, "path": None})
            continue
        # reconstruct
        chain = [found]
        while prev[chain[-1]] is not None:
            chain.append(prev[chain[-1]])
        chain.reverse()
        desc = []
        for (typ, v) in chain:
            if typ == "b":
                desc.append("B%d(acc%d,x%s)" % (v, Bevs[v][0], pre[Bevs[v][0]]["x"]))
            else:
                desc.append("A%d(acc%d,load%d)" % (v, Aevs[v][0], load.get(v, 0)))
        paths.append({"bev": bs, "path": desc})
    step("AP-03", "optimal edge-class hist: %s" % dict(optclass.most_common(10)))
    for p in paths:
        step("AP-04", "bev %s repair: %s" % (p["bev"], p["path"]))
    # greedy homes of blockers' units vs optimal: for starved bev's N
    e = elig[starve[0]]
    Ns = set(i for k in e for i in e[k] if Aevs[i][1])
    units = {i: [b for b, a in Gassign.items() if a == i] for i in Ns}
    optin = {i: [b for b, a in Oassign.items() if a == i] for i in Ns}
    step("AP-05", "starved-N greedy-units=%s optimal-units=%s" % (
        {i: len(v) for i, v in units.items()}, {i: len(v) for i, v in optin.items()}))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "augment.json").write_text(
        json.dumps({"B": nb, "flow": f, "starved": starve[:8],
                    "opt_classes": {"|".join(k): v for k, v in optclass.most_common(10)},
                    "paths": paths,
                    "greedy_units": {str(i): v for i, v in units.items()},
                    "optimal_units": {str(i): v for i, v in optin.items()}},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
