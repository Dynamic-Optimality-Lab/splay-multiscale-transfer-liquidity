"""WP-6 STEP FS-00: forced-singleton hunt (decisive for least-loaded rule).

Singleton ancestry: B-StepEv with EXACTLY 1 eligible ancestor A (E1+E2+E3+E4).
If O(n) such B's share one A, least-loaded overdraws (load>3) and the rule
is dead. Hunt: max shared-singleton load (B's with |elig|==1 per A), and
maximal forced-load generally. Also E3-only singletons (is E3 the weak link
or is full-ancestry uniformly abundant?).
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow2 import build2
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP FS-00.
    step("FS-00", "Forced-singleton hunt")
    import hashlib
    from collections import Counter

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"fs|%s|%d" % (self.s, self.c)).digest()

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

    worst_shared = 0
    exS = None
    n_single = 0
    nB = 0
    for t in range(150):
        rng = DRBG(("fs%d" % t).encode())
        n = rng.ch([16, 32, 64, 128])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(6, 24)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("FS-KILL", "present kill t=%d" % t)
            return 2
        g = build2(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        # forced singletons: |elig|==1 (sited only)
        forced = Counter()
        for j in range(len(Bevs)):
            es = [i for i in elig[j] if Aevs[i][1]]
            nB += 1
            if len(es) == 1:
                n_single += 1
                forced[es[0]] += 1
        if forced:
            m = max(forced.values())
            if m > worst_shared:
                worst_shared, exS = m, (t, m)
    step("FS-01", "B=%d singletons=%d worst shared-singleton-load=%d %s (want<=3)" %
         (nB, n_single, worst_shared, exS))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "singleton.json").write_text(
        json.dumps({"B": nB, "singletons": n_single, "worst": worst_shared,
                    "ex": exS}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
