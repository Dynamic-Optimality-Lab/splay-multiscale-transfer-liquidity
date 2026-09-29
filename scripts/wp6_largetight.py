"""WP-6 STEP LT-00: large-tight Hall probe (violator-shaped near-miss).

Objective: maximize |Q| subject to slack(Q) = 3|N(Q)|-|Q| <= 6 (tie: min slack).
Rationale: slack-2 singletons are degenerate (smallness, not pressure); danger
lives in LARGE Q on few sources (high reuse efficiency). Candidates: min-cut Q,
per-access slices, K-sets, random subsets, plus greedy Q-GROWTH (add B-events
while slack stays <= 6).
INCREMENTAL persist on (larger Q | smaller slack). Kill Delta>=1 -> hallkill.
NEW artifact: largetight.json (+hallkill.json on kill). Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_hallcore import build_graph, maxflow_cap3, delta_of
from wp6_tightest import vine, Rng, H_walk, persist
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h
from collections import defaultdict


def cand_sets(G, lv, rng):
    from wp6_hallcore import cands_from_cut
    out = cands_from_cut(G, lv)
    nb = len(G["Bevs"])
    # greedy growth seeds: start from each access slice, grow while slack<=6
    byacc = defaultdict(list)
    for j in range(nb):
        byacc[G["Bevs"][j][0]].append(j)
    for acc, js in byacc.items():
        Q = set(js)
        d, N = delta_of(G, Q)
        if -d <= 6:
            # grow: add random B-events while slack<=6
            order = list(range(nb))
            for t in range(len(order)):
                j = order[rng() % len(order)]
                if j in Q:
                    continue
                d2, _ = delta_of(G, Q | {j})
                if -d2 <= 6:
                    Q.add(j)
            out.append(("grow%d" % acc, sorted(Q)))
    for t in range(16):
        k = 2 + rng() % min(nb, 40)
        Q = sorted(rng() % nb for _ in range(k))
        out.append(("rand%d" % t, Q))
    return out


class Counter2:
    def __init__(self, seed, tag):
        self.r = Rng(seed, tag)
        self.c = 0

    def __call__(self):
        self.c += 1
        return self.r(self.c)


def eval_hist(n, T0, H, rng):
    G = build_graph(n, T0, H)
    if G is None:
        return None
    f, nb, lv = maxflow_cap3(G)
    if nb - f > 0:
        return ("KILL", nb - f, nb)
    best = None  # (|Q|, -slack)
    bestQ = None
    for name, Q in cand_sets(G, lv, rng):
        if not Q:
            continue
        d, N = delta_of(G, set(Q))
        if d > 0:
            return ("KILL", d, list(Q))
        slack = -d
        if slack <= 6:
            key = (len(Q), -slack)
            if best is None or key > best[0]:
                best = (key, name)
                bestQ = (list(Q), len(N))
    return ("OK", best, bestQ, nb)


def main() -> int:
    step("LT-00", "Large-tight Hall probe")
    import json
    TP = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "largetight.json"
    best = None
    best_rec = None
    evals = 0
    holders = []
    import json as _j
    dk = _j.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve_min.json"))
    holders.append((vine(dk["n"], dk["T0left"]), dk["Hmin"], dk["n"]))
    for s in range(100):
        rng = Rng(("s%d" % s).encode(), b"lt")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"lth")
        H = H_walk(rr, n, 12 + (r >> 16) % 22, 1 + (r >> 24) % n)
        v = eval_hist(n, T0, H, Counter2(("s%d" % s).encode(), b"ltc"))
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("LT-KILL", "HALL seed %d" % s)
            persist(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json",
                   {"kill": True, "H": H})
            return 2
        _, b, bQ, nb = v
        if b is not None and (best is None or b[0] > best):
            best = b[0]
            best_rec = {"n": n, "H": copy.deepcopy(H), "Qsize": b[0][0],
                        "slack": -b[0][1], "kind": b[1], "Nsize": bQ[1], "B": nb,
                        "Q": sorted(bQ[0])}
            persist(TP, {"evals": evals, "best": best_rec})
            step("LT-NEW", "seeds Q=%d slack=%d kind=%s" % (b[0][0], -b[0][1], b[1]))
        holders.append((T0, H, n))
    holders = holders[:16]
    step("LT-01", "seeds evals=%d best=%s" % (evals, best))
    it = 0
    while evals < 12000:
        it += 1
        r = int.from_bytes(_h.sha256(b"ltm|%d" % it).digest(), "big")
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
        v = eval_hist(n, T0, H2, Counter2(("it%d" % it).encode(), b"ltc"))
        evals += 1
        if v is None:
            continue
        if v[0] == "KILL":
            step("LT-KILL", "HALL it=%d" % it)
            persist(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hallkill.json",
                   {"kill": True, "H": H2})
            return 2
        _, b, bQ, nb = v
        if b is not None and (best is None or b[0][0] > best[0] or (b[0][0] == best[0] and b[0][1] > best[1])):
            best = (b[0][0], b[0][1])
            best_rec = {"n": n, "H": copy.deepcopy(H2), "Qsize": b[0][0],
                        "slack": -b[0][1], "kind": b[1], "Nsize": bQ[1], "B": nb,
                        "Q": sorted(bQ[0])}
            persist(TP, {"evals": evals, "best": best_rec})
            step("LT-NEW", "it=%d Q=%d slack=%d kind=%s" % (it, b[0][0], -b[0][1], b[1]))
            holders.append((T0, H2, n))
            holders = holders[-16:]
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n))
            holders = holders[-16:]
        if it % 3000 == 0:
            step("LT-02", "it=%d evals=%d best=%s" % (it, evals, best))
    step("LT-03", "evals=%d best=%s" % (evals, best))
    return 0


if __name__ == "__main__":
    sys.exit(main())
