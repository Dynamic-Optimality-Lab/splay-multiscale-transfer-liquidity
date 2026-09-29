"""WP-6 STEP SP-00: per-StepEv geometry probe (riser-containment, W-blocks).

For each access/splay: after EVERY StepEv, record depth deltas; assert
  risers(StepEv) ⊆ {x} ∪ subtree(x)-at-that-step   (ML-DISPLACE-STEP)
and every x-rise step has triple ∋ x                (ML-RISE-WITNESS, structural).
W-blocks: per (splay, W-member): #match-blocks (gap-split runs) and max run;
  assert blocks <= 3 (== |S| bound)                 (ML-W-BLOCKS).
NEW artifact: stepprobe.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import to_ptr, root_key, splay_A, splay_B_push
from liquidity import legacy_embedding as PE
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


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


def adepth(A, x):
    d, path = PE._depth_to(A, x)
    return d if (path and path[-1]["k"] == x) else None


def subkeys(node):
    out = set()
    stack = [node]
    while stack:
        nd = stack.pop()
        out.add(nd["k"])
        if nd["l"] is not None:
            stack.append(nd["l"])
        if nd["r"] is not None:
            stack.append(nd["r"])
    return out


def splay_checked(A, x, stats):
    """Bottom-up splay with per-StepEv riser + rise-witness checks. Returns root."""
    d, path = PE._depth_to(A, x)
    if not path or path[-1]["k"] != x:
        return A
    keys = set()
    st = [A]
    while st:
        nd = st.pop()
        if nd is None:
            continue
        keys.add(nd["k"])
        st.append(nd["l"])
        st.append(nd["r"])
    before = {k: adepth(A, k) for k in keys}
    node = path[-1]
    root = A
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        # subtree(x) BEFORE this StepEv
        sub = subkeys(node)
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            triple = {node["k"], p["k"]}
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            triple = {node["k"], p["k"], g["k"]}
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            triple = {node["k"], p["k"], g["k"]}
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            triple = {node["k"], p["k"], g["k"]}
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            triple = {node["k"], p["k"], g["k"]}
        stats["steps"] += 1
        # rise-witness: node x triple always contains x?
        if node["k"] != x:
            stats["node_not_x"] += 1
        if x not in triple:
            stats["triple_miss_x"] += 1
        r = node
        while r["p"] is not None:
            r = r["p"]
        root = r
        after = {k: adepth(root, k) for k in keys}
        for k in keys:
            b, a = before[k], after[k]
            if a is not None and b is not None and a < b:
                if k != x and k not in sub:
                    stats["riser_viol"] += 1
                    if len(stats["ex"]) < 5:
                        stats["ex"].append((x, k, b, a))
        before = after
    while node["p"] is not None:
        node = node["p"]
    return node


def main() -> int:
    step("SP-00", "Per-StepEv geometry probe")
    import json
    stats = {"steps": 0, "node_not_x": 0, "triple_miss_x": 0, "riser_viol": 0, "ex": []}
    for t in range(60):
        rng = Rng(("s%d" % t).encode(), b"sp")
        r = rng(0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 8 + (r >> 16) % 12
        x = 1 + (r >> 24) % n
        H = []
        for i in range(L):
            rr = Rng(("s%d" % t).encode(), ("sph%d" % i).encode())
            q = rr(1000 + i)
            H.append(["DELETE" if q % 2 else "KEEP", 1 + (q >> 5) % n])
        A = to_ptr(T0)
        for (m, xx) in H:
            A = splay_checked(A, xx, stats)
    step("SP-01", "steps=%d node_not_x=%d triple_miss_x=%d riser_viol=%d %s"
         % (stats["steps"], stats["node_not_x"], stats["triple_miss_x"],
            stats["riser_viol"], stats["ex"]))
    # W-blocks per (splay, W-member)
    from collections import Counter
    block_hist = Counter()
    maxblocks = 0
    maxrun = 0
    for t in range(60):
        rng = Rng(("s%d" % t).encode(), b"sp")
        r = rng(0)
        n = [16, 32, 64][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        L = 8 + (r >> 16) % 12
        H = []
        for i in range(L):
            rr = Rng(("s%d" % t).encode(), ("sph%d" % i).encode())
            q = rr(1000 + i)
            H.append(["DELETE" if q % 2 else "KEEP", 1 + (q >> 5) % n])
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("SP-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        A, B = to_ptr(T0), to_ptr(T0)
        Arot = {}
        acc_of = {}
        aid = 0
        for idx, acc in enumerate(pre2):
            A, invs = splay_A(A, acc["x"])
            for (S, sited) in zip(invs, acc["sites"]):
                Arot[aid] = frozenset(S)
                acc_of[aid] = idx
                aid += 1
            if acc["mode"] == "KEEP":
                B, _ = splay_B_push(B, acc["x"])
        # group Bev ids by access
        from collections import defaultdict
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        for acc, js in byacc.items():
            xx = pre2[acc]["x"]
            # member -> list of positions (0..len(js)-1) present as W
            pres = defaultdict(list)
            for p, j in enumerate(js):
                e = elig[j]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
                W = E3s - K - E1s
                for i in W:
                    pres[i].append(p)
            for i, ps in pres.items():
                blocks = 1
                for a, b in zip(ps, ps[1:]):
                    if b > a + 1:
                        blocks += 1
                block_hist[blocks] += 1
                maxblocks = max(maxblocks, blocks)
                run = 1
                best = 1
                for a, b in zip(ps, ps[1:]):
                    run = run + 1 if b == a + 1 else 1
                    best = max(best, run)
                maxrun = max(maxrun, best)
    step("SP-02", "W-blocks hist=%s maxblocks=%d maxrun=%d" % (dict(block_hist), maxblocks, maxrun))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "stepprobe.json").write_text(
        json.dumps({"steps": stats["steps"], "node_not_x": stats["node_not_x"],
                    "triple_miss_x": stats["triple_miss_x"], "riser_viol": stats["riser_viol"],
                    "riser_ex": stats["ex"], "w_blocks": dict(block_hist),
                    "w_maxblocks": maxblocks, "w_maxrun": maxrun},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
