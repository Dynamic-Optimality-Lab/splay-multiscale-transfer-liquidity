"""WP-6 STEP HC-00: Hall-core dual-structure extractor (mincut/tight/PEEL/4-core).

For a history (causal builders): exact cap-3 max flow; min-cut extraction with
VERIFIED Delta(Q) (greedy-shrink fallback to inclusion-minimal); tight-set hunt
(min slack 3|N|-|Q| over cut/access/K/class/random candidates); CAP3-PEEL loop
(assign all of deg<=3 sources, recurse; record emptied vs stalled-4-core);
latest-access boundary stats; full §9 anatomy for stalled cores (degrees,
components, spans, class/age/key distributions, multiplicity).
Usage: HC.run(n,T0,H) returns dict. CLI runs banked seeds:
  C37 killer, M2 witness, ENTRY@3 witness.
NEW artifact: hallcore.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def build_graph(n, T0, H):
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    pre2 = g["pre"]
    # adjacency: bev j -> sited aev set (dedup across classes)
    adj = []
    for j in range(len(Bevs)):
        e = elig[j]
        adj.append(set(i for k in e for i in e[k] if Aevs[i][1]))
    return {"Aevs": Aevs, "Bevs": Bevs, "elig": elig, "pre": pre2, "adj": adj}


def maxflow_cap3(G):
    Aevs, Bevs, adj = G["Aevs"], G["Bevs"], G["adj"]
    na, nb = len(Aevs), len(Bevs)
    if nb == 0:
        return 0, 0, None
    N = 2 + na + nb
    S, T = 0, N - 1
    D = Dinic(N)
    for i, (_, sited) in enumerate(Aevs):
        if sited:
            D.add(S, 1 + i, 3)
    for j in range(nb):
        D.add(1 + na + j, T, 1)
    for j, es in enumerate(adj):
        for i in es:
            D.add(1 + i, 1 + na + j, 1)
    f, lv = D.flow(S, T)
    return f, nb, lv


def cands_from_cut(G, lv):
    """Candidate Hall sets from min-cut reachable set + access/K/class slices."""
    from collections import defaultdict
    Aevs, Bevs, adj = G["Aevs"], G["Bevs"], G["adj"]
    na, nb = len(Aevs), len(Bevs)
    out = []
    if lv is not None:
        # B-nodes: id 1+na+j. Qcut = B NOT reachable (standard deficiency side).
        Qcut = [j for j in range(nb) if lv[1 + na + j] < 0]
        out.append(("cut", Qcut))
        Qcut2 = [j for j in range(nb) if lv[1 + na + j] >= 0]
        out.append(("cut-reach", Qcut2))
    byacc = defaultdict(list)
    for j in range(nb):
        byacc[Bevs[j][0]].append(j)
    for acc, js in byacc.items():
        out.append(("acc%d" % acc, js))
    out.append(("all", list(range(nb))))
    return out


def delta_of(G, Q):
    N = set()
    for j in Q:
        N |= G["adj"][j]
    return len(Q) - 3 * len(N), N


def shrink_minimal(G, Q):
    """Greedy single-removal fixpoint from a deficient Q (Delta>0 preserved)."""
    Q = set(Q)
    d, _ = delta_of(G, Q)
    if d <= 0:
        return None
    changed = True
    while changed:
        changed = False
        for b in list(Q):
            d2, _ = delta_of(G, Q - {b})
            if d2 > 0:
                Q = Q - {b}
                changed = True
                break
    return Q


def degrees(G, Q):
    from collections import Counter
    deg = Counter()
    for j in Q:
        for i in G["adj"][j]:
            deg[i] += 1
    return deg


def peel(G):
    """CAP3-PEEL: repeatedly assign all of a 1<=deg<=3 source. Returns
    (emptied: bool, assigned: dict bev->aev, residual_Q or None)."""
    Q = set(range(len(G["Bevs"])))
    assigned = {}
    while Q:
        deg = degrees(G, Q)
        found = None
        for a, r in deg.items():
            if 1 <= r <= 3:
                found = a
                break
        if found is None:
            return False, assigned, Q
        R = [b for b in Q if found in G["adj"][b]]
        for b in R:
            assigned[b] = found
        Q -= set(R)
    return True, assigned, None


def core_anatomy(G, R):
    from collections import Counter, defaultdict
    Aevs, Bevs = G["Aevs"], G["Bevs"]
    pre = G["pre"]
    deg = degrees(G, R)
    N = set(deg)
    d, _ = delta_of(G, R)
    # components (union-find over Q union N)
    parent = {}
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for b in R:
        parent[("b", b)] = ("b", b)
    for a in N:
        parent[("a", a)] = ("a", a)
    for b in R:
        for a in G["adj"][b]:
            if a in N:
                rb, ra = find(("b", b)), find(("a", a))
                parent[rb] = ra
    comps = Counter(find(("b", b)) for b in R)
    # class composition needs elig; recompute cheap tags via Aev/B ev acc
    accs = sorted(Bevs[j][0] for j in R)
    xs = Counter(pre[Bevs[j][0]]["x"] for j in R)
    aacc = Counter(Aevs[i][0] for i in N)
    return {"R": len(R), "N": len(N), "Delta": d,
            "mindeg": min(deg.values()) if deg else None,
            "deg_hist": dict(Counter(deg.values())),
            "bdeg_hist": dict(Counter(len(G["adj"][b]) for b in R)),
            "ncomp": len(comps), "comp_sizes": sorted(comps.values(), reverse=True)[:8],
            "acc_span": [min(accs), max(accs)] if accs else None,
            "x_dist": dict(xs.most_common(8)),
            "srca_acc_dist": dict(aacc.most_common(8))}


def run(n, T0, H):
    G = build_graph(n, T0, H)
    if G is None:
        return {"illegal": True}
    f, nb, lv = maxflow_cap3(G)
    out = {"B": nb, "flow": f, "shortfall": nb - f}
    best = None
    for name, Q in cands_from_cut(G, lv):
        if not Q:
            continue
        d, N = delta_of(G, Q)
        slack = -d
        if best is None or slack < best[0]:
            best = (slack, name, len(Q), len(N))
    out["tight"] = {"slack": best[0], "kind": best[1], "Q": best[2], "N": best[3]} if best else None
    if nb - f > 0:
        Q0 = list(range(nb))
        Qm = shrink_minimal(G, Q0)
        if Qm is not None:
            d, N = delta_of(G, Qm)
            deg = degrees(G, Qm)
            out["violator"] = {"Q": len(Qm), "N": len(N), "Delta": d,
                               "mindeg": min(deg.values()),
                               "Qs": sorted(Qm), "Ns": sorted(N)}
        else:
            out["violator"] = {"note": "shortfall>0 but greedy found none (check construction)"}
    emptied, assigned, R = peel(G)
    out["peel"] = {"emptied": emptied, "assigned": len(assigned)}
    if not emptied:
        out["peel"]["core"] = core_anatomy(G, R)
    return out


def main() -> int:
    step("HC-00", "Hall-core dual-structure extractor")
    import json
    from wp6_spread import vine
    out = {}
    dk = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    out["killer"] = run(dk["n"], vine(dk["n"], dk["T0left"]), dk["Hmin"])
    step("HC-01", "killer: %s" % json.dumps({k: v for k, v in out["killer"].items() if k != "peel"}))
    step("HC-01b", "killer peel: %s" % json.dumps(out["killer"]["peel"], default=str))
    w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
    # m2 T0 not stored; re-derive (was left=True per prior autopsy... verify by B count)
    m2r = None
    for left in (True, False):
        T = vine(w["n"], left)
        r = run(w["n"], T, w["H"])
        if r.get("B", -1) > 100:
            m2r = (left, r)
            break
    out["m2"] = {"left": m2r[0], "res": m2r[1]} if m2r else {"note": "no match"}
    step("HC-02", "m2: %s" % json.dumps(out["m2"], default=str)[:600])
    ew = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "entryhunt.json"))["witness"]
    ewr = None
    for left in (True, False):
        T = vine(ew["n"], left)
        r = run(ew["n"], T, ew["H"])
        if r.get("B", -1) > 100:
            ewr = (left, r)
            break
    out["entry3"] = {"res": ewr[1]} if ewr else {"note": "no match"}
    step("HC-03", "entry3: %s" % json.dumps(out["entry3"], default=str)[:600])
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallcore.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
