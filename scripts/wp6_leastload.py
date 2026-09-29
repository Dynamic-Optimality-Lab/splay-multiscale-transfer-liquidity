"""WP-6 STEP LL-00: least-loaded token allocation (deterministic, no matching).

RULE (online, deterministic): B-StepEv takes 1 token from eligible ancestor
A-StepEv (E1+E2+E3+E4 past-only, structural) with SMALLEST current load;
ties -> smallest (acc_idx, step_idx) canonical. A capacity 3 (sited).
Load = tokens consumed from A so far. NO reallocation (online greedy).
TEST: max load per A ever exceeds 3? (overdraw => rule dead); B starvation
(no eligible with load<3 => dead with witness class); prefix maxima.
33x local overcover (med-11 ancestry x3 slots) suggests balance possible;
popular-A concentration is what recency did wrong. Least-loaded spreads.
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
    # WP-6 STEP LL-00.
    step("LL-00", "Least-loaded token allocation")
    import hashlib

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ll|%s|%d" % (self.s, self.c)).digest()

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

    maxload = 0
    exL = None
    starve = 0
    exS = None
    nB = 0
    for t in range(120):
        rng = DRBG(("ll%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        L = rng.ir(4, 18)
        x = rng.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("LL-KILL", "present kill t=%d" % t)
            return 2
        g = build2(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        # process B in order (online)
        for j in range(len(Bevs)):
            nB += 1
            cands = [(load.get(i, 0), i) for i in elig[j] if Aevs[i][1]]
            cands.sort()
            placed = False
            for (ld, i) in cands:
                if ld < 3:
                    load[i] = ld + 1
                    if ld + 1 > maxload:
                        maxload, exL = ld + 1, (t, j, i)
                    placed = True
                    break
            if not placed:
                starve += 1
                if exS is None:
                    exS = (t, j, len(cands))
    step("LL-01", "B=%d maxload=%d %s starved=%d %s (want maxload<=3, starve=0)" %
         (nB, maxload, exL, starve, exS))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "leastload.json").write_text(
        json.dumps({"B": nB, "maxload": maxload, "exL": exL,
                    "starved": starve, "exS": exS}, indent=1, sort_keys=True,
                   default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
