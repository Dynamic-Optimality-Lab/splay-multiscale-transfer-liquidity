"""WP-6 STEP ML2-00: minload-2 boundary mining + adversarial max-minload.

Least-loaded online allocation (E1+E2+E3+E4, cap 3, canonical tiebreak).
For every B-event with min-eligible-load == 2 (one step from starvation):
  ancestry size; E1/E2/E3/E4 composition; temporal ages (acc spread);
  which A's at load 2 and how they got there; what new source appears next
  (setup arrival? fresh pump? own access?) before any could hit 3.
Adversarial hillclimb maximizing max-over-B min-load (kill >= 3 =
starvation witness => capacity rule dead). Mutations target pump-fanout
(deep pumps, shared ancestors) and setup-starvation (shallow arrivals).
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


def run_alloc(g):
    """Least-loaded online; return (maxload, starved, minload2_cases)."""
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    maxload = 0
    starved = 0
    m2 = []
    for j in range(len(Bevs)):
        cands = sorted((load.get(i, 0), i) for i in elig[j] if Aevs[i][1])
        if not cands:
            starved += 1
            continue
        if cands[0][0] >= 3:
            starved += 1
            continue
        if cands[0][0] == 2:
            m2.append((j, len(cands)))
        ld, i = cands[0]
        load[i] = ld + 1
        if ld + 1 > maxload:
            maxload = ld + 1
    return maxload, starved, m2


def main() -> int:
    # WP-6 STEP ML2-00.
    step("ML2-00", "Minload-2 mining + adversarial max-minload")
    import hashlib
    import copy

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"ml2|%s|%d" % (self.s, self.c)).digest()

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

    def H_of(rng, n, L, x0):
        H = []
        x = x0
        for i in range(L):
            if i % 4 == 3:
                y = min(n, max(1, x + rng.ch([-32, -16, 16, 32])))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append([rng.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng.ch([-32, -16, -8, -4, -1, 1, 4, 8, 16, 32])))
        return H

    # baseline: minload-2 frequency over corpus
    tot_m2 = 0
    tot_B = 0
    worst_ml = 0
    for t in range(80):
        rng = DRBG(("ml2a%d" % t).encode())
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        H = H_of(rng, n, rng.ir(4, 18), rng.ir(1, n))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ML2-KILL", "present kill t=%d" % t)
            return 2
        g = build2(n, T0, H)
        ml, st, m2 = run_alloc(g)
        tot_m2 += len(m2)
        tot_B += len(g["Bevs"])
        # max min-load over B = worst boundary pressure
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        for j in range(len(Bevs)):
            cands = sorted((load.get(i, 0), i) for i in elig[j] if Aevs[i][1])
            if cands and cands[0][0] > worst_ml:
                worst_ml = cands[0][0]
            if cands and cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
    step("ML2-01", "minload2-cases=%d/%d worst-minload=%d" % (tot_m2, tot_B, worst_ml))
    # adversarial: maximize max-min-load (hillclimb, kill>=3)
    best = -1
    ex = None
    evals = 0
    holders = []
    for s in range(60):
        rng = DRBG(("ml2b%d" % s).encode())
        n = rng.ch([32, 64])
        T0 = vine(n, rng.below(2) == 0)
        H = H_of(rng, n, rng.ir(6, 20), rng.ir(1, n))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ML2-KILL", "present kill s=%d" % s)
            return 2
        g = build2(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        wm = -1
        for j in range(len(Bevs)):
            cands = sorted((load.get(i, 0), i) for i in elig[j] if Aevs[i][1])
            if cands:
                if cands[0][0] > wm:
                    wm = cands[0][0]
                if cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
        evals += 1
        if wm > best:
            best, ex = wm, (n, len(H))
            holders.append((T0, H, n))
            holders = holders[-8:]
    for it in range(800):
        import hashlib as _h
        r = int.from_bytes(_h.sha256(b"ml2m|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 50:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        pre = E.precompute(n, T0, H2)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("ML2-KILL", "present kill it=%d" % it)
            return 2
        g = build2(n, T0, H2)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        wm = -1
        for j in range(len(Bevs)):
            cands = sorted((load.get(i, 0), i) for i in elig[j] if Aevs[i][1])
            if cands:
                if cands[0][0] > wm:
                    wm = cands[0][0]
                if cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
                if wm >= 3:
                    break
        evals += 1
        if wm > best:
            best, ex = wm, (n, len(H2))
            holders.append((T0, H2, n))
            holders = holders[-8:]
            if best >= 3:
                step("ML2-KILL", "minload>=3 STARVATION %s" % str(ex))
                import json as _j
                (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                    _j.dumps({"kill": True, "ex": ex,
                              "H": [[m, x] for (m, x) in H2]}, indent=1, default=str),
                    encoding="utf-8")
                return 2
    step("ML2-02", "adversarial evals=%d best-minload=%d %s (kill>=3)" % (evals, best, ex))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "minload.json").write_text(
        json.dumps({"m2_cases": tot_m2, "B_total": tot_B, "worst_ml": worst_ml,
                    "adv_evals": evals, "adv_best": best, "adv_ex": ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
