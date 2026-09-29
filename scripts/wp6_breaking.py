"""WP-6 STEP BR-00: breaking-shape hunt for growth-vs-consumption.

Target conjunction (all three at one B-StepEv b, same access):
  (i)   E3 strictly shrinks along the splay (lost >> new at b),
  (ii)  same-access overflow (remaining e_B demand >> 3*e_A E1-cap),
  (iii) thin E2/E4 (few pump/setup ancestors).
Score = shrinkage * overflow / (1 + E2E4). Maximize; report min-load reached.
Kill: min-load >= 2 (first! then push to >=3 starvation witness).
Also log E3-size trajectory per splay (shrink events) + E1-saturation points.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow import Dinic
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


def main() -> int:
    # WP-6 STEP BR-00.
    step("BR-00", "Breaking-shape hunt (shrink+overflow+thin)")
    import hashlib
    import copy

    class DRBG:
        def __init__(self, s): self.s = s; self.c = 0

        def b(self):
            self.c += 1
            return hashlib.sha256(b"br|%s|%d" % (self.s, self.c)).digest()

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

    def H_of(rng, n, L, x0, tag):
        H = []
        x = x0
        for i in range(L):
            r = rng(tag, 1000 + i)
            if i % 4 == 3:
                y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
                H.append(["DELETE", y if y != x else 1])
                H.append(["KEEP", x])
            else:
                H.append(["KEEP" if r % 3 else "DELETE", x])
            x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
        return H

    class Rng:
        def __init__(self, s): self.s = s; self.c = 0

        def __call__(self, tag, c):
            import hashlib as _h
            if isinstance(tag, str):
                tag = tag.encode()
            return int.from_bytes(_h.sha256(b"br|%s|%s|%d" % (self.s, tag, c)).digest(), "big")

    def score_hist(n, T0, H):
        """Max over B-events of shrink*overflow/(1+E2E4); also max minload."""
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            return ("KILL", None)
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        # per-access B order + E3 trajectory: Bevs carry acc idx; E3 sets
        best = -1.0
        best_ml = -1
        # chronological least-loaded for minload
        load = {}
        # group Bev ids by access preserving order
        from collections import defaultdict
        byacc = defaultdict(list)
        for j, (idx,) in enumerate(Bevs):
            byacc[idx].append(j)
        for idx in sorted(byacc):
            e3prev = None
            for j in byacc[idx]:
                e = elig[j]
                e3 = set(e["E3"])
                if e3prev is not None:
                    lost = len(e3prev - e3)
                    new = len(e3 - e3prev)
                    shrink = max(0, lost - new)
                    e24 = len([i for i in e["E2"] | e["E4"] if Aevs[i][1]])
                    eA = sum(1 for z in pre[idx]["sites"] if z)
                    eB = len(pre[idx]["Bev"])
                    over = max(0, eB - 3 * eA)
                    sc = shrink * over / (1.0 + e24)
                    if sc > best:
                        best = sc
                e3prev = e3
                # minload under least-loaded
                cands = sorted((load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1])
                if cands and cands[0][0] > best_ml:
                    best_ml = cands[0][0]
                if cands and cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
                elif cands:
                    return ("STARVE", (idx, j))
        return (best, best_ml)

    best = -1.0
    ex = None
    bestml = -1
    holders = []
    for s in range(80):
        rng = Rng(("s%d" % s).encode())
        r = rng("s", 0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode())
        H = H_of(rr, n, 10 + (r >> 16) % 22, 1 + (r >> 24) % n, "h")
        v = score_hist(n, T0, H)
        if v[0] == "KILL":
            step("BR-KILL", "present kill s=%d" % s)
            return 2
        if v[0] == "STARVE":
            step("BR-KILL", "STARVATION %s" % str(v[1]))
            import json as _j
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                _j.dumps({"kill": True, "where": v[1], "H": H}, indent=1, default=str),
                encoding="utf-8")
            return 2
        sc, ml = v
        if sc > best or ml > bestml:
            if ml > bestml:
                bestml = ml
            if sc > best:
                best, ex = sc, (n, len(H))
            holders.append((T0, H, n))
            holders = holders[-10:]
    step("BR-01", "seeds best-score=%.2f best-minload=%d %s" % (best, bestml, ex))
    it = 0
    evals = 80
    import hashlib as _h
    while evals < 2500 and it < 2000:
        it += 1
        r = int.from_bytes(_h.sha256(b"brm|%d" % it).digest(), "big")
        T0, H, n = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 4
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 60:
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        v = score_hist(n, T0, H2)
        evals += 1
        if v[0] == "KILL":
            step("BR-KILL", "present kill it=%d" % it)
            return 2
        if v[0] == "STARVE":
            step("BR-KILL", "STARVATION it=%d %s" % (it, v[1]))
            import json as _j
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                _j.dumps({"kill": True, "where": v[1], "H": H2}, indent=1, default=str),
                encoding="utf-8")
            return 2
        sc, ml = v
        if sc > best or ml > bestml:
            if ml > bestml:
                bestml = ml
            if sc > best:
                best = sc
            holders.append((T0, H2, n))
            holders = holders[-10:]
    step("BR-02", "evals=%d best-score=%.2f best-minload=%d" % (evals, best, bestml))
    import json
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "breaking.json").write_text(
        json.dumps({"evals": evals, "best_score": best, "best_minload": bestml},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
