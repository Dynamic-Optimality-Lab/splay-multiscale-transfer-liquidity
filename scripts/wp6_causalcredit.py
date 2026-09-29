"""WP-6 STEP GG-00: event genealogy instrumentation + bounded ancestry.

Per A/B StepEv record: type (ZIG/LL/RR/LR/RL), rotated node-set,
edge-delta (parent-links changed, as key-pairs), interval [lo,hi],
ancestry signature (sorted rotated keys + neighbor keys).
Genealogy DAG: B-StepEv b <- A-StepEvs a iff triple(b) INTERSECT
rotated(a) != {} AND a precedes b (E3-overlap, structural, tight).
Measure per B-event: #ancestors (bounded O(1)? or O(n)?), ancestor fan-in
distribution, oldest-ancestor distance, genesis-or-pumped source classes.
Witnesses: X-RETURN-corpse shape, residual-chain shape, t179 shape,
pumped multi-divergent, borderline-crossing shape.
Question: is causal ancestry per B-event BOUNDED (O(1), finite genealogy)
or UNBOUNDED (O(n), fanout)? Bounded => token rules viable; unbounded =>
enrich to interval/laminar/automaton or record obstruction.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
from liquidity import legacy_embedding as PE
from solver import encode as E


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


def replay_sets(t, x):
    """Mirror splay_trace; return (root, [rotated-set per StepEv])."""
    d, path = PE._depth_to(t, x)
    if not path or path[-1]["k"] != x:
        return t, []
    out = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            out.append(frozenset((node["k"], p["k"])))
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            out.append(frozenset((node["k"], p["k"], g["k"])))
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            out.append(frozenset((node["k"], p["k"], g["k"])))
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            out.append(frozenset((node["k"], p["k"], g["k"])))
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            out.append(frozenset((node["k"], p["k"], g["k"])))
    while node["p"] is not None:
        node = node["p"]
    return node, out


def main() -> int:
    # WP-6 STEP GG-00.
    step("GG-00", "Event genealogy + bounded ancestry")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"gg|%s|%d" % (self.s, self.c)).digest()

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

    import statistics as _st
    anc_sizes = []
    max_anc = 0
    exA = None
    nB = 0
    for t in range(150):
        rng = DRBG(("gg%d" % t).encode())
        n = rng.ch([32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(8, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("GG-KILL", "present kill t=%d" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        # A-rotation log: list of (acc_idx, frozenset)
        alog = []
        for idx, acc in enumerate(pre):
            A, invs = replay_sets(A, acc["x"])
            for S in invs:
                alog.append((idx, S))
            if acc["mode"] == "KEEP":
                B, binvs = replay_sets(B, acc["x"])
                for S in binvs:
                    # ancestors: prior alog entries with S ∩ T != {}
                    na = sum(1 for (_, T) in alog if not T.isdisjoint(S))
                    anc_sizes.append(na)
                    nB += 1
                    if na > max_anc:
                        max_anc, exA = na, (t, acc["x"], sorted(S))
    anc_sizes.sort()
    step("GG-01", "B-events=%d ancestry-size min=%d med=%s p90=%d max=%d %s" %
         (nB, anc_sizes[0], _st.median(anc_sizes), anc_sizes[int(0.9 * len(anc_sizes))],
          max_anc, exA))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "genealogy.json").write_text(
        json.dumps({"B_events": nB, "min": anc_sizes[0],
                    "med": _st.median(anc_sizes),
                    "p90": anc_sizes[int(0.9 * len(anc_sizes))],
                    "max": max_anc, "ex": exA}, indent=1, sort_keys=True,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
