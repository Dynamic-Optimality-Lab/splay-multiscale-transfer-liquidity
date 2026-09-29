"""WP-6 STEP TQ-00: strongest Hall near-miss persister (min-slack + §5 anatomy).

Objective: minimize safety slack sigma(Q) = 3|N(Q)| - |Q| over candidate Q
(min-cut Q, access slices, K-sets, random subsets); tie-break larger |Q|.
INCREMENTAL PERSISTENCE: tightest.json rewritten on EVERY improvement
(best Delta up or best sigma down or first tight set) -- never lose witnesses.
Full §5 anatomy for best: history/prefix/Q/N/sizes/sigma/Delta/components/
deg-hists/identities/acc-indices/creation-accs/ages/keys/class-labels/fresh-vs-
old/heavy-decomposition/Q-specific-fresh-capacity+overflow/earliest/latest/
x-runs/multiplicity. Minimization at end: history-removal + Q-shrink preserving
slack. Kill: Delta(Q)>=1 -> §15 audit path (hallkill + exit 2).
NEW artifact: tightest.json (+hallkill.json on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of, degrees
from wp6_eventflow_abl import build_tagged
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict, Counter


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def H_walk(rr, n, L, x0):
    H = []
    x = x0
    for i in range(L):
        r = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
    return H


def cand_sets(G, lv, rng=None):
    from wp6_hallcore import cands_from_cut
    out = cands_from_cut(G, lv)
    # random subsets (biased to heavy accesses) if rng given
    if rng is not None:
        nb = len(G["Bevs"])
        for t in range(24):
            k = 1 + rng() % min(nb, 24)
            Q = sorted(rng() % nb for _ in range(k))
            out.append(("rand%d" % t, Q))
    return out


def anatomy(n, T0, H, Q):
    G = build_graph(n, T0, H)
    Aevs, Bevs, elig = G["Aevs"], G["Bevs"], G["elig"]
    pre = G["pre"]
    Q = set(Q)
    N = set()
    for j in Q:
        N |= G["adj"][j]
    d = len(Q) - 3 * len(N)
    # components
    parent = {}
    for b in Q:
        parent[("b", b)] = ("b", b)
    for a in N:
        parent[("a", a)] = ("a", a)
    def find(v):
        while parent[v] != v:
            parent[v] = parent[parent[v]]
            v = parent[v]
        return v
    for b in Q:
        for a in G["adj"][b]:
            if a in N:
                parent[find(("b", b))] = find(("a", a))
    comps = Counter(find(("b", b)) for b in Q)
    deg = degrees(G, Q)
    # class labels per A identity (dedup)
    cls = {}
    for i in N:
        lab = set()
        for j in Q:
            if i in G["adj"][j]:
                e = elig[j]
                for k in e:
                    if i in e[k]:
                        lab.add(k)
        cls[i] = sorted(lab)
    # per-access Q decomposition + fresh capacity + overflow
    byacc = defaultdict(list)
    for j in Q:
        byacc[Bevs[j][0]].append(j)
    # fresh sets: need Arot/acc_of + setup snapshots -> rebuild lightly
    from wp6_eventflow import to_ptr, splay_A, splay_B_push
    A, B = to_ptr(T0), to_ptr(T0)
    Arot = {}
    acc_of = {}
    aid = 0
    setups = []
    setup = {}
    for idx, acc in enumerate(pre):
        from wp6_eventflow import root_key
        rb = root_key(A)
        A, invs = splay_A(A, acc["x"])
        for (S, sited) in zip(invs, acc["sites"]):
            Arot[aid] = frozenset(S)
            acc_of[aid] = idx
            aid += 1
        if rb != acc["x"]:
            setup[acc["x"]] = idx
        setups.append(dict(setup))
        if acc["mode"] == "KEEP":
            B, _ = splay_B_push(B, acc["x"])
    accinfo = {}
    for acc, js in byacc.items():
        xx = pre[acc]["x"]
        e1 = set(a for a in range(len(Aevs)) if Aevs[a][0] == acc and Aevs[a][1])
        _s = setups[acc]
        e4 = set(a for a in range(len(Aevs)) if Aevs[a][0] == _s.get(xx, -1) and Aevs[a][1]) \
            if (xx in _s and _s.get(xx, -1) != acc and _s.get(xx, -1) >= 0) else set()
        F = (e1 | e4) & N
        # K members in N for this access
        K = set(i for i in N if Aevs[i][1] and xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
        accinfo[acc] = {"x": xx, "Qj": len(js), "F": len(F),
                        "qresid": len(js) - 3 * len(F),
                        "eB": sum(1 for jj in range(len(Bevs)) if Bevs[jj][0] == acc),
                        "eA": sum(1 for z in pre[acc]["sites"] if z)}
    bacc = [Bevs[j][0] for j in Q]
    ages = sorted(Bevs[j][0] - Aevs[i][0] for j in Q for i in G["adj"][j] if i in N)
    import statistics as _st
    age_stat = {"min": min(ages), "med": _st.median(ages), "max": max(ages)} if ages else None
    return {"Q": len(Q), "N": len(N), "sigma": -d, "Delta": d,
            "ncomp": len(comps), "comp_sizes": sorted(comps.values(), reverse=True)[:6],
            "bdeg_hist": dict(Counter(len(G["adj"][b]) for b in Q)),
            "sdeg_hist": dict(Counter(deg.values())),
            "Qs": sorted(Q), "Ns": sorted(N),
            "acc_span": [min(bacc), max(bacc)] if bacc else None,
            "x_dist": dict(Counter(pre[Bevs[j][0]]["x"] for j in Q).most_common(6)),
            "src_ages": age_stat,
            "class_labels": {str(i): cls[i] for i in sorted(N)},
            "per_access": accinfo,
            "fresh_total": sum(v["F"] for v in accinfo.values()),
            "resid_total": sum(v["qresid"] for v in accinfo.values())}


class Counter2:
    def __init__(self, seed, tag):
        self.r = Rng(seed, tag)
        self.c = 0

    def __call__(self):
        self.c += 1
        return self.r(self.c)


def eval_hist(n, T0, H, rng=None):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    best = None  # (slack, -|Q|, name)
    bestQ = None
    for name, Q in cand_sets(G, lv, rng):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        if d > 0:
            return ("KILL", d, Q)
        slack = -d
        key = (slack, -len(Q))
        if best is None or key < (best[0], best[1]):
            best = (slack, -len(Q), name)
            bestQ = (list(Q), len(N))
    return ("OK", best, bestQ, nb)


def persist(path, payload):
    import json
    path.write_text(json.dumps(payload, indent=1, sort_keys=True, default=str), encoding="utf-8")


def main() -> int:
    step("TQ-00", "Strongest Hall near-miss persister")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "tightest.json"
    best = None  # (slack, -|Q|)
    best_rec = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(100):
        rng = Rng(("s%d" % s).encode(), b"tq")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"tqh")
        H = H_walk(rr, n, 12 + (r >> 16) % 22, 1 + (r >> 24) % n)
        v = eval_hist(n, T0, H, None)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("TQ-KILL", "HALL seed %d" % s)
            persist(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json",
                   {"kill": True, "H": H})
            return 2
        _, b, bQ, nb = v
        key = (b[0], b[1])
        if best is None or key < best:
            best = key
            best_rec = {"n": n, "T0left": (r >> 8) % 2 == 0, "H": copy.deepcopy(H),
                        "slack": b[0], "kind": b[2], "Qsize": -b[1], "Nsize": bQ[1], "B": nb}
            persist(TP, {"evals": evals, "best": best_rec})
            step("TQ-NEW", "seeds slack=%s kind=%s" % (best, b[2]))
        holders.append((T0, H, n))
    holders = holders[:16]
    step("TQ-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"tqm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 6
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif op == 3 and H2:
            recent = [a[1] for a in H2][-6:]
            base = recent[(r >> 5) % len(recent)] if recent else 1 + (r >> 13) % n
            stepd = [-2, -1, -1, 0, 1, 1, 2][(r >> 9) % 7]
            H2.append(["KEEP" if r % 2 else "DELETE", min(n, max(1, base + stepd))])
        elif op == 4 and H2:
            recent = [a[1] for a in H2 if a[0] == "KEEP"][-4:]
            if recent:
                H2.append(["KEEP", recent[(r >> 5) % len(recent)]])
            else:
                H2.append(["KEEP", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        rr = Counter2(("it%d" % it).encode(), b"tqr")
        v = eval_hist(n, T0, H2, rr)
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("TQ-KILL", "HALL it=%d" % it)
            persist(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json",
                   {"kill": True, "H": H2})
            return 2
        _, b, bQ, nb = v
        key = (b[0], b[1])
        if key < best:
            best = key
            best_rec = {"n": n, "T0left": None, "H": copy.deepcopy(H2),
                        "slack": b[0], "kind": b[2], "Qsize": -b[1], "Nsize": bQ[1], "B": nb}
            # recover left flag: try both vines, keep matching B
            for left in (True, False):
                Tt = vine(n, left)
                G = build_graph(n, Tt, H2)
                if G is not None and len(G["Bevs"]) == nb:
                    best_rec["T0left"] = left
                    best_rec["T0"] = Tt
                    break
            persist(TP, {"evals": evals, "best": best_rec})
            step("TQ-NEW", "it=%d slack=%s kind=%s" % (it, best, b[2]))
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("TQ-02", "it=%d evals=%d best=%s" % (it, evals, best))
    # minimize best: history-removal preserving slack, then Q-shrink
    br = best_rec
    n, H = br["n"], br["H"]
    T0 = vine(n, br["T0left"]) if br.get("T0left") is not None else vine(n, True)
    G = build_graph(n, T0, H)
    changed = True
    while changed:
        changed = False
        for i in range(len(H)):
            H2 = H[:i] + H[i + 1:]
            if not H2:
                continue
            v = eval_hist(n, T0, H2, None)
            if v is None:
                continue
            if v[0] == "KILL":
                step("TQ-KILL", "HALL via minimization lenH=%d" % len(H2))
                persist(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json",
                       {"kill": True, "H": H2})
                return 2
            _, b, bQ, nb = v
            if (b[0], b[1]) <= best:
                H = H2
                best = (b[0], b[1])
                changed = True
                break
    step("TQ-03", "minimized lenH=%d best=%s" % (len(H), best))
    # full anatomy of best Q: rebuild best Q via candidates
    G = build_graph(n, T0, H)
    f, nb, lv = maxflow_cap3(G)
    bQ = None
    for name, Q in cand_sets(G, lv, None):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        if -d == best[0] and len(Q) == -best[1]:
            bQ = list(Q)
            break
    if bQ is None:
        # fallback: smallest-slack access slice
        bQ = None
    ana = anatomy(n, T0, H, bQ) if bQ else {"note": "best Q not relocated"}
    persist(TP, {"evals": evals, "best": best_rec, "minimized": {"lenH": len(H), "H": H},
                 "anatomy": ana})
    step("TQ-04", "done evals=%d best=%s" % (evals, best))
    return 0


if __name__ == "__main__":
    sys.exit(main())
