"""WP-6 STEP CY-00: pair-state cycle hunt (convergence decider).

Long hostile histories; track pair-state canonicals; on repeat, measure
cycle reward (E_B-3*S_A over the cycle). POSITIVE cycle => periodic witness
=> replay (E_B-ratio, J3, 14P-viol) => RETURN 2 if confirmed.
ALL-NONPOSITIVE => value iteration converges everywhere observable (no
positive塔cycles); supports V-laws/telescope shape (not proof for n=128).
Also longest-simple-path stats (useless-bound diagnostic).
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


def canon(t):
    r = t
    while r["p"] is not None:
        r = r["p"]
    return PE.canonical(r)


def main() -> int:
    # WP-6 STEP CY-00.
    step("CY-00", "Pair-state cycle hunt")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"cy|%s|%d" % (self.s, self.c)).digest()

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

    pos_cyc = 0
    tot_cyc = 0
    worst_cyc = -10**18
    exC = None
    maxlen = 0
    n_hist = 0
    for t in range(120):
        rng = DRBG(("cy%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(30, 120)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("CY-KILL", "present kill t=%d (refutes MSTL-14P!)" % t)
            return 2
        A, B = to_ptr(T0), to_ptr(T0)
        seen = {}
        eb = sa = 0
        EB = [0]
        SA = [0]
        for idx, acc in enumerate(pre):
            key = (canon(A), canon(B))
            if key in seen:
                j0 = seen[key]
                cyc = (eb - EB[j0]) - 3 * (sa - SA[j0])
                tot_cyc += 1
                if cyc > worst_cyc:
                    worst_cyc, exC = cyc, (t, j0, idx)
                if cyc > 0:
                    pos_cyc += 1
            else:
                seen[key] = idx
            mode = acc["mode"]
            if mode == "KEEP":
                eb += len(acc["Bev"])
            sa += sum(1 for z in acc["sites"] if z)
            EB.append(eb)
            SA.append(sa)
            if mode == "KEEP":
                A, _ = PE.splay_trace(A, acc["x"])
                B, _ = PE.splay_trace(B, acc["x"])
            else:
                A, _ = PE.splay_trace(A, acc["x"])
        if len(seen) > maxlen:
            maxlen = len(seen)
        n_hist += 1
    step("CY-01", "hist=%d cycles=%d positive=%d worst-cycle-reward=%d %s maxlen=%d" %
         (n_hist, tot_cyc, pos_cyc, worst_cyc, exC, maxlen))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "cycles.json").write_text(
        json.dumps({"histories": n_hist, "cycles": tot_cyc, "positive": pos_cyc,
                    "worst": worst_cyc, "ex": exC, "maxlen": maxlen},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
