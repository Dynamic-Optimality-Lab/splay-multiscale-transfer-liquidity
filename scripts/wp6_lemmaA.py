"""WP-6 STEP LA-00: Lemma A verification (O(1) rooted-interval update).

I_T(v) = (min,max) key range of subtree rooted at v (inorder interval;
contiguous by BST property). L(T) = {v: interval}. For each frozen StepEv
(ROOT/ZIG/LL/RR/LR/RL) executed as 1-2 primitive rotations, count how many
nodes' subtree compositions (hence intervals) change. Claim: O(1) (bounded
by a small constant independent of n). Kill threshold: any StepEv changing
a non-constant (n-scaling) number of records.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def to_ptr(t):
    if t is None:
        return None
    root = PE.mknode(t[0])
    stack = [(t, root)]
    while stack:
        src, dst = stack.pop()
        if src[1] is not None:
            nd = PE.mknode(src[1][0])
            nd["p"] = dst
            dst["l"] = nd
            stack.append((src[1], nd))
        if src[2] is not None:
            nd = PE.mknode(src[2][0])
            nd["p"] = dst
            dst["r"] = nd
            stack.append((src[2], nd))
    return root


def intervals(p):
    """L(T): map key -> (lo,hi) subtree range. Iterative post-order."""
    if p is None:
        return {}
    r = p
    while r["p"] is not None:
        r = r["p"]
    out = {}
    stack = [(r, False)]
    while stack:
        u, done = stack.pop()
        if u is None:
            continue
        if done:
            # out[id(u)] = (lo, hi) subtree key-range; children resolved first.
            lo = u["k"] if u["l"] is None else out[id(u["l"])][0]
            hi = u["k"] if u["r"] is None else out[id(u["r"])][1]
            out[id(u)] = (lo, hi)
        else:
            stack.append((u, True))
            stack.append((u["r"], False))
            stack.append((u["l"], False))
    # rekey by node key (keys unique)
    res = {}
    stack = [r]
    while stack:
        u = stack.pop()
        if u is None:
            continue
        res[u["k"]] = out[id(u)]
        stack.append(u["l"])
        stack.append(u["r"])
    return res


def main() -> int:
    # WP-6 STEP LA-00: measure interval churn per StepEv over hostile splays.
    step("LA-00", "Measuring rooted-interval churn per StepEv")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"la|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

        def ir(self, a, b): return a + self.below(b - a + 1)

        def ch(self, s): return s[self.below(len(s))]

    def vine(n, left=False):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    from collections import Counter
    churn = Counter()
    worst = {}
    n_ev = 0
    for t in range(400):
        rng = DRBG(("la%d" % t).encode())
        n = rng.ch([8, 16, 32, 64]) if hasattr(rng, "ch") else 32
        T0 = vine(n, rng.below(2) == 0)
        T = to_ptr(T0)
        for _ in range(rng.ir(2, 10)):
            x = rng.ir(1, n)
            before = intervals(T)
            # replicate splay_trace step by step to attribute churn per event
            d, path = PE._depth_to(T, x)
            if not path or path[-1]["k"] != x:
                continue
            node = path[-1]
            while node["p"] is not None:
                p = node["p"]
                g = p["p"]
                pre = intervals(T)
                if g is None:
                    if p["l"] is node:
                        PE._rot_right(p)
                        case = "ZIG"
                    else:
                        PE._rot_left(p)
                        case = "ZIG"
                elif p["l"] is node and g["l"] is p:
                    PE._rot_right(g)
                    PE._rot_right(p)
                    case = "LL"
                elif p["r"] is node and g["r"] is p:
                    PE._rot_left(g)
                    PE._rot_left(p)
                    case = "RR"
                elif p["r"] is node and g["l"] is p:
                    PE._rot_left(p)
                    PE._rot_right(g)
                    case = "LR"
                else:
                    PE._rot_right(p)
                    PE._rot_left(g)
                    case = "RL"
                post = intervals(T)
                changed = sum(1 for k in pre if pre[k] != post.get(k))
                # keys sets identical; all keys present in both
                assert set(pre) == set(post)
                churn[case] += 1
                n_ev += 1
                worst[case] = max(worst.get(case, 0), changed)
                if changed > 8:
                    step("LA-KILL", "non-local update: %s changed %d" % (case, changed))
                    return 2
            while node["p"] is not None:
                node = node["p"]
    step("LA-01", "events=%d churn=%s worst=%s" % (n_ev, dict(churn), worst))
    import json
    out = {"events": n_ev, "by_case": dict(churn), "worst_by_case": worst,
           "verdict": "LOCAL-O1-VERIFIED"}
    p = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "lemmaA_intervals.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=1, sort_keys=True), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
