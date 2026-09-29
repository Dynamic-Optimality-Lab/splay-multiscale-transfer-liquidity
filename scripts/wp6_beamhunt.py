"""WP-6 STEP BM-00 (patched): beam adversarial falsifier, execution-optimized.

Kill condition preserved: EVERY generated successor gets exact cumulative
reward checked; cumulative > 0 => replay artifact + kill GC immediately.
Optimization (math untouched):
  dedup successors by canonical (A,B); cheap prescore (cumulative + depth
  hazard proxy, no splays); keep PRE=60; exact V1 only on PRE survivors
  with memoization on canonical pairs; final W by cumulative + exact_V1.
Deterministic DRBG. D8, n64/128.
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


def clone(t):
    r = t
    while r["p"] is not None:
        r = r["p"]

    def rec(u, p):
        if u is None:
            return None
        nd = PE.mknode(u["k"])
        nd["p"] = p
        nd["l"] = rec(u["l"], nd)
        nd["r"] = rec(u["r"], nd)
        return nd

    return rec(r, None)


def canon(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def depths_of(t, n):
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


def main() -> int:
    # WP-6 STEP BM-00 patched.
    step("BM-00", "Beam adversarial falsifier (optimized)")
    import hashlib
    import json

    def vine(n, left):
        t = None
        for k in (range(n, 0, -1) if not left else range(1, n + 1)):
            t = [k, None, t] if not left else [k, t, None]
        return t

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"bm|%s|%d" % (self.s, self.c)).digest()

        def below(self, n):
            bound = (1 << 256) - ((1 << 256) % n)
            while True:
                v = int.from_bytes(self.b(), "big")
                if v < bound:
                    return v % n

    W = 10
    PRE = 60
    DEPTH = 8
    V1memo = {}
    cache_hits = 0
    best_all = -10**18
    ex_all = None

    def exact_V1(A, B, n):
        nonlocal cache_hits
        key = (canon(A), canon(B))
        if key in V1memo:
            cache_hits += 1
            return V1memo[key]
        best = 0
        for yy in range(1, n + 1):
            _, eA = PE.splay_trace(clone(A), yy)
            _, eB = PE.splay_trace(clone(B), yy)
            r = len(eB) - 3 * len(eA)
            if r > best:
                best = r
        V1memo[key] = best
        return best

    for t in range(12):
        rng = DRBG(("bm%d" % t).encode())
        n = 64 if t % 2 == 0 else 128
        T0 = vine(n, rng.below(2) == 0)
        beam = [(to_ptr(T0), to_ptr(T0), 0, [])]
        for d in range(DEPTH):
            gen = 0
            uniq = {}
            # generate all successors; exact cumulative kill-check on each
            for (A, B, cum, hist) in beam:
                for xx in range(1, n + 1):
                    A2, eA = PE.splay_trace(clone(A), xx)
                    na = len(eA)
                    # KEEP successor
                    B2, eB = PE.splay_trace(clone(B), xx)
                    nb = len(eB)
                    c = cum + nb - 3 * na
                    gen += 1
                    if c > best_all:
                        best_all = c
                    if c > 0:
                        ex_all = (t, d, hist + [("K", xx, na, nb, nb - 3 * na)])
                        step("BM-KILL", "cumulative>0 %s" % str(ex_all))
                        (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "beamkill.json").write_text(
                            json.dumps({"ex": ex_all}, indent=1, default=str), encoding="utf-8")
                        return 2
                    k = (canon(A2), canon(B2))
                    if k not in uniq or c > uniq[k][0]:
                        uniq[k] = (c, A2, B2, hist + [("K", xx, na, nb, nb - 3 * na)])
                    # DELETE successor
                    c2 = cum - 3 * na
                    gen += 1
                    if c2 > best_all:
                        best_all = c2
                    if c2 > 0:
                        ex_all = (t, d, hist + [("D", xx, na, 0, -3 * na)])
                        step("BM-KILL", "cumulative>0 %s" % str(ex_all))
                        (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "beamkill.json").write_text(
                            json.dumps({"ex": ex_all}, indent=1, default=str), encoding="utf-8")
                        return 2
                    k = (canon(A2), canon(B))
                    if k not in uniq or c2 > uniq[k][0]:
                        uniq[k] = (c2, A2, B, hist + [("D", xx, na, 0, -3 * na)])
            # cheap prescore: cumulative + depth hazard proxy (no splays)
            scored = []
            for (k, (c, A2, B2, hist)) in uniq.items():
                dA = depths_of(A2, n)
                dB = depths_of(B2, n)
                px = 0
                for y in range(1, n + 1):
                    g = dB.get(y, 0) - 3 * dA.get(y, 0)
                    if g > px:
                        px = g
                scored.append((c + px, c, A2, B2, hist))
            scored.sort(key=lambda z: -z[0])
            pre = scored[:PRE]
            # exact V1 only on PRE survivors
            rescored = []
            nv1 = 0
            for (_, c, A2, B2, hist) in pre:
                v1 = exact_V1(A2, B2, n)
                nv1 += 1
                rescored.append((c + v1, c, A2, B2, hist))
            rescored.sort(key=lambda z: -z[0])
            beam = [(A2, B2, c, hist) for (_, c, A2, B2, hist) in rescored[:W]]
            best_beam = rescored[0][0] if rescored else None
            step("BM-t%dd%d" % (t, d), "gen=%d uniq=%d V1eval=%d bestcum=%d bestbeam=%s cache=%d" %
                 (gen, len(uniq), nv1, best_all, best_beam, cache_hits))
    step("BM-01", "best cumulative=%d (want<=0)" % best_all)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "beam.json").write_text(
        json.dumps({"best": best_all, "W": W, "PRE": PRE, "depth": DEPTH,
                    "cache": cache_hits}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
