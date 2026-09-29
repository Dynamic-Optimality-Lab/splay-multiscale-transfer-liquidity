"""WP-6 STEP MG-00: safety-margin probe (distance to starvation).

For each history/B-event (canonical least-loaded, causal builders):
  margin(b) = 3*|N| - loadsum(N) - remaining_in_access (optimistic: ignores waste
              on exited-W and future refreshment; true margin larger).
  spread(b) = max-min load within N (synchrony: collapse => synchronous drain).
  dilution(t) = fresh-0 count at access start (E1-0 + E4-0 + first-event W@0)
              vs e_B(t) demand (dilution race per access).
  near-misses: B-events with margin <= 2 (falsifier seeds).
Kill: minload>=3 (starve.json + exit 2).
NEW artifact: margin.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class Rng:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag

    def __call__(self, c):
        return int.from_bytes(_h.sha256(self.tag + b"|%s|%d" % (self.s, c)).digest(), "big")


def gen_corpus(t, tag):
    rng = Rng(("s%d" % t).encode(), tag)
    r = rng(0)
    n = [32, 64, 128][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = 12 + (r >> 16) % 24
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][q % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(q >> 9) % 8]))
    return n, T0, H


def main() -> int:
    step("MG-00", "Safety-margin probe")
    import json
    from collections import Counter, defaultdict
    margins = []
    spreads = Counter()
    spread_at_drain = Counter()
    dil = []
    near = []
    nB = 0
    NBY = 0
    for t in range(300):
        tag = b"mg" if t % 2 == 0 else b"mg2"
        n, T0, H = gen_corpus(t, tag)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("MG-KILL", "present kill t=%d" % t)
            return 2
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        byacc = defaultdict(list)
        for j in range(len(Bevs)):
            byacc[Bevs[j][0]].append(j)
        load = {}
        for acc, js in sorted(byacc.items()):
            eB = len(js)
            # dilution: fresh-0 at access start
            j0 = js[0]
            e0 = elig[j0]
            N0 = set(i for k in e0 for i in e0[k] if Aevs[i][1])
            fresh0 = sum(1 for i in N0 if load.get(i, 0) == 0)
            dil.append((fresh0, eB))
            for p, j in enumerate(js):
                nB += 1
                e = elig[j]
                N = set(i for k in e for i in e[k] if Aevs[i][1])
                if not N:
                    continue
                ls = [load.get(i, 0) for i in N]
                lo, hi = min(ls), max(ls)
                spreads[hi - lo] += 1
                if lo >= 1:
                    NBY += 1
                    spread_at_drain[hi - lo] += 1
                R = len(js) - p  # remaining including current
                margin = 3 * len(N) - sum(ls) - R
                margins.append(margin)
                if margin <= 2 and len(near) < 15:
                    near.append({"t": t, "bev": j, "acc": acc, "ml": lo,
                                 "nanc": len(N), "margin": margin, "R": R})
                cands = sorted((load.get(i, 0), i) for i in N)
                if cands[0][0] < 3:
                    ld, i = cands[0]
                    load[i] = ld + 1
                else:
                    step("MG-KILL", "STARVATION t=%d bev=%d" % (t, j))
                    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                        json.dumps({"kill": True, "H": H}, indent=1, default=str),
                        encoding="utf-8")
                    return 2
    margins.sort()
    step("MG-01", "B=%d margin min=%d p1=%s med=%s" % (
        nB, margins[0], margins[len(margins) // 100], margins[len(margins) // 2]))
    step("MG-02", "spread all=%s; spread|drain(min>=1, n=%d)=%s" % (
        dict(spreads), NBY, dict(spread_at_drain)))
    import statistics
    fr = [f for (f, e) in dil]
    de = [e for (f, e) in dil]
    step("MG-03", "per-access fresh0 med=%s max=%s; eB med=%s max=%s; fresh0<eB frac=%.3f" % (
        sorted(fr)[len(fr) // 2], max(fr), sorted(de)[len(de) // 2], max(de),
        sum(1 for (f, e) in dil if f < e) / max(1, len(dil))))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "margin.json").write_text(
        json.dumps({"B": nB, "margin_min": margins[0],
                    "margin_p1": margins[len(margins) // 100],
                    "margin_med": margins[len(margins) // 2],
                    "spread": dict(spreads), "spread_drain": dict(spread_at_drain),
                    "ndrain": NBY, "dil_fresh_med": sorted(fr)[len(fr) // 2],
                    "dil_eB_med": sorted(de)[len(de) // 2],
                    "near": near}, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
