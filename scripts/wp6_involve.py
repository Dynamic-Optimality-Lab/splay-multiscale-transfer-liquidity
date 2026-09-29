"""WP-6 STEP IV-00: per-key involvement bound screen.

Involvement: A-StepEv rotates key-set S (|S|<=3 structurally: ZIG 2, doubles 3).
I_x = #{A-StepEvs with x in S}. Candidate per-key lemma:
  sum_{KEEPs of x} need <= 2 * I_x   (sited involvements; U=0 says all sited)
Summation closes stock IFF: sum_x I_x <= 3 * S_A (structural: |S|<=3/StepEv).
Measure per-INTERVAL form (need at x-KEEP vs 2*involve_x since prev x-KEEP,
own-access involvements included) + global sum check + unsited count.
A per-key violation kills the LEMMA (sufficient, not necessary for stock).
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


def splay_involve(t, x):
    """Mirror splay_trace; return (new_root, [rotated key-set per StepEv])."""
    d, path = PE._depth_to(t, x)
    if not path or path[-1]["k"] != x:
        return t, []
    inv = []
    node = path[-1]
    while node["p"] is not None:
        p = node["p"]
        g = p["p"]
        if g is None:
            if p["l"] is node:
                PE._rot_right(p)
            else:
                PE._rot_left(p)
            inv.append({node["k"], p["k"]})
        elif p["l"] is node and g["l"] is p:
            PE._rot_right(g)
            PE._rot_right(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["r"] is p:
            PE._rot_left(g)
            PE._rot_left(p)
            inv.append({node["k"], p["k"], g["k"]})
        elif p["r"] is node and g["l"] is p:
            PE._rot_left(p)
            PE._rot_right(g)
            inv.append({node["k"], p["k"], g["k"]})
        else:
            PE._rot_right(p)
            PE._rot_left(g)
            inv.append({node["k"], p["k"], g["k"]})
    while node["p"] is not None:
        node = node["p"]
    return node, inv


def main() -> int:
    # WP-6 STEP IV-00: per-key involvement screen.
    step("IV-00", "Per-key involvement bound screen")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"iv|%s|%d" % (self.s, self.c)).digest()

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

    worst_iv = 0.0  # max over x-KEEPs of need - 2*involve_since_prev (want <=0)
    worst_gl = 0.0  # max over keys of sumneed - 2*I_x (want <=0)
    ex_iv = ex_gl = None
    maxset = 0
    unsited = 0
    sumI = 0
    sumSA = 0
    n_hist = 0
    for t in range(500):
        rng = DRBG(("iv%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(2, 14)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 3 == 2:
                # freeze-then-cash bias: DELETE others, then KEEP x
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("IV-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        kps = list(res["keeps"])
        A = to_ptr(T0)
        Ix = {}
        lastkeep = {}
        sumneed = {}
        ki = 0
        for idx, acc in enumerate(pre):
            mode, xx = acc["mode"], acc["x"]
            A, invs = splay_involve(A, xx)
            for S in invs:
                if len(S) > maxset:
                    maxset = len(S)
                for v in S:
                    Ix[v] = Ix.get(v, 0) + 1
                    sumI += 1
            sumSA += sum(1 for z in acc["sites"] if z)
            # NOTE: sites are per-A-StepEv; A-StepEvs here == len(invs)
            if len(invs) != len(acc["Aev"]):
                step("IV-FAIL", "trace mismatch t=%d" % t)
                return 2
            for ev_sited in acc["sites"]:
                if not ev_sited:
                    unsited += 1
            if mode == "KEEP":
                nd = kps[ki]["need"]
                ki += 1
                since = Ix.get(xx, 0) - lastkeep.get(xx, (0, 0))[1]
                gap = nd - 2 * since
                if gap > worst_iv:
                    worst_iv, ex_iv = gap, (t, xx, nd, since)
                sumneed[xx] = sumneed.get(xx, 0) + nd
                lastkeep[xx] = (idx, Ix.get(xx, 0))
        for v, sn in sumneed.items():
            gap = sn - 2 * Ix.get(v, 0)
            if gap > worst_gl:
                worst_gl, ex_gl = gap, (t, v, sn, Ix.get(v, 0))
        n_hist += 1
    step("IV-01", "hist=%d max-rotset=%d unsited-A-StepEvs=%d sumI=%d sumSA-sited=%d"
         % (n_hist, maxset, unsited, sumI, sumSA))
    step("IV-01", "worst per-interval gap (need-2*involve) = %s %s (want<=0)"
         % (worst_iv, ex_iv))
    step("IV-01", "worst per-key global gap (sumneed-2*Ix) = %s %s (want<=0)"
         % (worst_gl, ex_gl))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "involve.json").write_text(
        json.dumps({"histories": n_hist, "max_rotset": maxset, "unsited": unsited,
                    "sumI": sumI, "sumSA": sumSA,
                    "worst_interval_gap": worst_iv, "iv_ex": ex_iv,
                    "worst_key_gap": worst_gl, "gl_ex": ex_gl},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
