"""WP-6 STEP RK2-00: rank-candidate deltas at scale (does maxAcc rise?).

For tight positive-reward KEEPs (V-tight via 1-step lookahead proxy since
full V unavailable at scale: tight iff r + V1(s') == V1(s)? approximate by
reward-positive KEEPs), measure deltas of maxAcc/hazKeys/maxHaz/divKeys.
rises>0 at scale kills rank (like H: small-n single-divergence artifact).
Pure-created bystander hazard is the predicted killer (41% pure pumps).
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


def depths_keys(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u, d):
        if u is None:
            return
        out[u["k"]] = d
        rec(u["l"], d + 1)
        rec(u["r"], d + 1)

    rec(r, 0)
    return out


def sub_sets(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    out = {}

    def rec(u):
        if u is None:
            return set()
        s = {u["k"]} | rec(u["l"]) | rec(u["r"])
        out[u["k"]] = s
        return s

    rec(r)
    return out


def stepcount(t, x):
    # StepEvs to splay x: simulate on clone (cheap enough at these sizes?)
    # CHEAPER: depth-based bounds are insufficient (need exact steps).
    # Use trace length on a lightweight tuple copy instead.
    r = t
    while r["p"] is not None:
        r = r["p"]

    def totup(u):
        if u is None:
            return None
        return (u["k"], totup(u["l"]), totup(u["r"]))

    import sys as _s
    _s.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from wp6_splaymetric import splay_cost_events
    _, c = splay_cost_events(totup(r), x)
    return c


def anat(A, B, n):
    dA, dB = depths_keys(A), depths_keys(B)
    mx = -10**18
    hk = 0
    mh = 0
    for y in range(1, n + 1):
        cb = dB[y]  # NOTE: uses depth as step proxy (see below)
        ca = dA[y]
        r = cb - 3 * ca
        if r > mx:
            mx = r
        g = cb - 3 * ca
        if g > 0:
            hk += 1
        if g > mh:
            mh = g
    sA, sB = sub_sets(A), sub_sets(B)
    dk = sum(1 for k in range(1, n + 1) if sA[k] != sB[k])
    return {"maxAcc": mx, "hazKeys": hk, "maxHaz": mh, "divKeys": dk}


def main() -> int:
    # WP-6 STEP RK2-00. NOTE: depth-proxy for steps (d vs e~d/1.5) shifts
    # constants; rises>0 signal is robust to monotone proxy (order kept
    # iff proxy monotone in steps -- depths are NOT monotone in steps!
    # depth<=steps<=depth exactly? e in [d/2,d]. Proxy direction unclear;
    # treat as SCREEN (confirm positives with exact steps if rises found).
    step("RK2-00", "Rank-candidate deltas at scale (depth-proxy screen)")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"rk|%s|%d" % (self.s, self.c)).digest()

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

    for n in (32, 64, 128):
        rises = {}
        exmax = {}
        npos = 0
        for t in range(60):
            rng = DRBG(("rk%d" % t).encode())
            T0 = vine(n, rng.below(2) == 0)
            L = rng.ir(6, 20)
            x = rng.ir(1, n)
            H = []
            for i in range(L):
                if i % 4 == 3:
                    y = min(n, max(1, x + rng.ch([-16, -8, 8, 16])))
                    H.append(["DELETE", y if y != x else 1])
                    H.append(["KEEP", x])
                else:
                    H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
                x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
            pre = E.precompute(n, T0, H)
            res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
            if res["violations"]:
                step("RK2-KILL", "present kill n=%d t=%d" % (n, t))
                return 2
            A, B = to_ptr(T0), to_ptr(T0)
            for acc in pre:
                mode, xx = acc["mode"], acc["x"]
                if mode == "KEEP":
                    eA = sum(1 for z in acc["sites"] if z)
                    eB = len(acc["Bev"])
                    if eB - 3 * eA <= 0:
                        A, _ = PE.splay_trace(A, xx)
                        B, _ = PE.splay_trace(B, xx)
                        continue
                    a0 = anat(A, B, n)
                    A, _ = PE.splay_trace(A, xx)
                    B, _ = PE.splay_trace(B, xx)
                    a1 = anat(A, B, n)
                    npos += 1
                    for k in a0:
                        d = a1[k] - a0[k]
                        if d > 0:
                            rises[k] = rises.get(k, 0) + 1
                            if d > exmax.get(k, -10**18):
                                exmax[k] = d
                else:
                    A, _ = PE.splay_trace(A, xx)
        step("RK2-n%d" % n, "pos=%d rises=%s exmax=%s" % (npos, rises, exmax))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "rankscale.json").write_text(
        json.dumps({"note": "see log (depth-proxy screen)"}, indent=1), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
