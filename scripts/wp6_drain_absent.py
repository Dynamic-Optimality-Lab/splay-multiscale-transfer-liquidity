"""WP-6 STEP: post-drain absent-need probe.

For margin-0 KEEPs (ACTIVE_post=0), try EVERY absent key as follow-up KEEP and
record max need. If max need is always 0, absent followers can never kill on
drained pools (structural y<=2a); any need>=1 is a refutation setup.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from solver import encode as E
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


def bst(keys):
    if not keys:
        return None
    m = len(keys) // 2
    return [keys[m], bst(keys[:m]), bst(keys[m + 1:])]


def main() -> int:
    # WP-6 STEP DA-00: post-drain absent-need measurement.
    step("DA-00", "Measuring absent follow-up needs after margin-0 KEEPs")
    import random
    worst = (0, None)
    n_cases = 0
    for t in range(3000):
        rnd = random.Random(100000 + t)
        n = rnd.randint(8, 40)
        keep = sorted(rnd.sample(range(1, n + 1), min(rnd.randint(2, 6), n)))
        absent = [k for k in range(1, n + 1) if k not in keep]
        if not absent:
            continue
        T0 = bst(keep)
        L = rnd.randint(2, 8)
        H = [[rnd.choice(["KEEP", "DELETE"]), rnd.choice(keep)] for _ in range(L)]
        pre = E.precompute(n, T0, H)
        r = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if r["violations"]:
            step("DA-KILL", "kill in drain phase t=%d" % t)
            return 2
        # replay trees to each margin-0 KEEP, then probe absent keys
        for idx, (acc, kp) in enumerate(zip([a for a in pre if a["mode"] == "KEEP"],
                                            r["keeps"])):
            if kp["paid"] - kp["need"] != 0 or kp["need"] <= 0:
                continue
            A, B = to_ptr(T0), to_ptr(T0)
            for a2 in pre[: kp["idx"] + 1]:
                A, _ = PE.splay_trace(A, a2["x"])
                if a2["mode"] == "KEEP":
                    B, _ = PE.splay_trace(B, a2["x"])
            for z in absent:
                a = PE.splay_cost(A, z)
                y = PE.splay_cost(B, z)
                need = max(y - 2 * a, 0)
                n_cases += 1
                if need > worst[0]:
                    worst = (need, (t, n, keep, z, a, y))
    step("DA-01", "absent follow-up max need=%d over %d probes" % (worst[0], n_cases))
    print("[WP-6][STEP DA-01] worst=%s" % (worst[1],), flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
