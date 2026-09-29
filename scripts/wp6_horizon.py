"""WP-6 STEP HZ3-00: hazard-horizon scaling (does h* grow with n?).

V==V_1 (h*=0/1) at n<=6. Test n=16/32/64/128: for sampled pair-states on
real hostile orbits, compute V_h (h=1..H) by forward-capped DP and find h*
(stabilization). Constant h* => bounded-horizon (local lemma suffices!).
Growing h* => recursive/deferred hazard (needs deeper recursion).
Genuinely unbounded => history-global.
Forward orbits capped (BFS dedup, cap 50k states); V_h bottom-up per layer.
"""
from __future__ import annotations
import sys
from collections import deque
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


def key_of(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return r["k"]


def main() -> int:
    # WP-6 STEP HZ3-00.
    step("HZ3-00", "Hazard-horizon scaling")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"hz3|%s|%d" % (self.s, self.c)).digest()

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

    import json
    out = {}
    for n in (16, 32, 64):
        # hostile orbit to harvest pair-states (use legacy replay)
        rng = DRBG(("hz3%d" % n).encode())
        T0 = vine(n, True)
        L = 24
        x = n // 2
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
            step("HZ3-KILL", "present kill n=%d" % n)
            return 2
        # collect pair-states along replay (canonical strings as ids)
        A, B = to_ptr(T0), to_ptr(T0)

        def canon(t):
            r = t
            while r["p"] is not None:
                r = r["p"]
            return PE.canonical(r)

        states = [(canon(A), canon(B))]
        for acc in pre:
            A, _ = PE.splay_trace(A, acc["x"])
            if acc["mode"] == "KEEP":
                B, _ = PE.splay_trace(B, acc["x"])
            states.append((canon(A), canon(B)))
        # V_h on these states needs successor V_{h-1}: successors may leave
        # the harvested set; expand by forward closure (cap).
        # SIMPLIFICATION: V_h estimated on harvested set closed under the
        # orbit's own transitions only (lower bound on true V_h).
        # Full closure: BFS from harvested states (cap 20k).
        from wp6_splaymetric import splay_cost_events

        def tup_of_ptr(t):
            r = t
            while r["p"] is not None:
                r = r["p"]

            def rec(u):
                if u is None:
                    return None
                return (u["k"], rec(u["l"]), rec(u["r"]))

            return rec(r)

        # rebuild tuple orbit for exact transitions
        def totup(lst):
            # lst is nested list [k,l,r]
            if lst is None:
                return None
            return (lst[0], totup(lst[1]), totup(lst[2]))

        A, B = to_ptr(T0), to_ptr(T0)
        # map canonical->tuple via replay
        seen = {}

        def reg(t):
            tt = tup_of_ptr(t)
            seen[canon(t)] = tt
            return tt

        At, Bt = reg(A), reg(B)
        fwd = {(At, Bt)}
        dq = deque([(At, Bt)])
        cap = 20000
        trans = {}
        while dq and len(fwd) < cap:
            a, b = dq.popleft()
            lst = []
            for xx in range(1, n + 1):
                a2, ca = splay_cost_events(a, xx)
                s = (a2, b)
                lst.append(("D", xx, ca, 0, -3 * ca, s))
                if s not in fwd and len(fwd) < cap:
                    fwd.add(s)
                    dq.append(s)
                b2, cb = splay_cost_events(b, xx)
                s = (a2, b2)
                lst.append(("K", xx, ca, cb, cb - 3 * ca, s))
                if s not in fwd and len(fwd) < cap:
                    fwd.add(s)
                    dq.append(s)
            trans[(a, b)] = lst
        nodes = list(fwd)
        V = {v: 0 for v in nodes}
        hstar = {}
        V1 = {}
        for h in range(1, 25):
            Vn = {}
            for v in nodes:
                best = 0
                for (_, _, _, _, r, s) in trans.get(v, []):
                    q = r + V.get(s, 0)
                    if q > best:
                        best = q
                Vn[v] = best
            if h == 1:
                V1 = dict(Vn)
            done = all(Vn[v] == V[v] for v in nodes)
            V = Vn
            if done:
                for v in nodes:
                    hstar[v] = h
                break
        mx = max(V.values())
        hs = [hstar[v] for v in nodes if v in hstar]
        # V vs V1
        agree = sum(1 for v in nodes if V.get(v, 0) == V1.get(v, 0))
        step("HZ3-n%d" % n, "fwd=%d stableh=%s maxV=%d VeqV1=%.3f h*max=%s" %
             (len(nodes), (h if done else None), mx, agree / max(1, len(nodes)),
              max(hs) if hs else None))
        out[str(n)] = {"fwd": len(nodes), "maxV": mx,
                       "VeqV1": agree / max(1, len(nodes)),
                       "hmax": max(hs) if hs else None}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "horizon.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
