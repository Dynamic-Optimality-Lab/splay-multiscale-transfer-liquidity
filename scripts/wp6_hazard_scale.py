"""WP-6 STEP HZ2-00: hazard LAW-K at scale (single vs multi-divergence).

LAW-K (KEEP x): c(B,x)-3*c(A,x) + H(S_xA,S_xB)-H(A,B) <= 0 ?
Hypothesis: holds iff bystander-divergence by=0 (single-key divergence,
small-n); multi-divergence (large-n pumped histories) violates via
bystander push-up (by'>=by>by-e_B). Measure worst LAW-K gap + by/by'
at n=16/32/64/128 hostile pump-heavy. Violation kills H at scale.
H(A,B)=max_y max(0,c(B,y)-3*c(A,y)); c = StepEv splay cost (pointer engine).
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


def scost(t, x):
    d, path = PE._depth_to(t, x)
    if not path or path[-1]["k"] != x:
        return 0
    # StepEvs to splay: simulate count via trace length on clone? Use cost
    # formula: replay on a scratch clone is costly; instead count steps by
    # walking (each StepEv moves x up 1-2): replicate loop cheaply.
    # CHEAP: use precompute-style? Just run splay_trace on CLONE.
    import copy

    def clone(u, p=None):
        if u is None:
            return None
        nd = PE.mknode(u["k"])
        nd["p"] = p
        nd["l"] = clone(u["l"], nd)
        nd["r"] = clone(u["r"], nd)
        return nd

    r = t
    while r["p"] is not None:
        r = r["p"]
    c = clone(r)
    _, evs = PE.splay_trace(c, x)
    return len(evs)


def Hcost(A, B, n):
    best = 0
    for y in range(1, n + 1):
        g = scost(B, y) - 3 * scost(A, y)
        if g > best:
            best = g
    return best


def main() -> int:
    # WP-6 STEP HZ2-00.
    step("HZ2-00", "Hazard LAW-K at scale")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"hz|%s|%d" % (self.s, self.c)).digest()

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

    for n in (16, 32, 64, 128):
        worst = -10**18
        ex = None
        n_hist = 0
        for t in range(60):
            rng = DRBG(("hz%d" % t).encode())
            T0 = vine(n, rng.below(2) == 0)
            L = rng.ir(6, 20)
            x = rng.ir(1, n)
            H = []
            for i in range(L):
                if i % 4 == 3:
                    y = min(n, max(1, x + rng.ch([-16, -8, 8, 16])))
                    H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                    H.append(["KEEP", x])
                else:
                    H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
                x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
            pre = E.precompute(n, T0, H)
            res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
            if res["violations"]:
                step("HZ2-KILL", "present kill t=%d" % t)
                return 2
            A, B = to_ptr(T0), to_ptr(T0)
            for acc in pre:
                mode, xx = acc["mode"], acc["x"]
                if mode == "KEEP":
                    h0 = Hcost(A, B, n)
                    eA = scost(A, xx)
                    eB = scost(B, xx)
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
                    h1 = Hcost(A, B, n)
                    gap = (eB - 3 * eA) + (h1 - h0)
                    if gap > worst:
                        worst, ex = gap, (t, xx, eA, eB, h0, h1)
                else:
                    A, _ = PE.splay_trace(A, xx)
            n_hist += 1
        step("HZ2-n%d" % n, "worst LAW-K gap=%s %s (want<=0)" % (worst, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "hazard_scale.json").write_text(
        json.dumps({"note": "see log lines"}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
