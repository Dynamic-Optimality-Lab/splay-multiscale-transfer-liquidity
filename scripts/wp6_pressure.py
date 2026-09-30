"""WP-6 STEP PA-00: wall-pressure audit (are falsifiers testing the wall?).

For each history/access (causal builders) across MANY corpora (all generator
tags + banked witnesses): per KEEP-access compute e_B, f (fresh: |E1| or
pristine-|E4|), B-heavy? (e_B > 3f), old sizes (E2/E4/K/W sited counts),
old-thin? (|old| <= 2), STERILE? (W-new == 0 and E2/K/E4 empty-ish),
WALL-PRESSURE = B-heavy AND old-thin AND sterile.
Report: wall-pressure rate (fraction of KEEP-accesses), e_B distribution at
pressure events, minload there, shortfall contribution.
If wall-pressure ~0: falsifiers have a BLIND SPOT (never generate the danger
shape) -> build targeted wall-pressure falsifier next.
NEW artifact: pressure.json. Sealed files untouched.
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
from collections import defaultdict, Counter


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


def gen(t, tag, nset, Llo, Lhi, walk):
    rng = Rng(("s%d" % t).encode(), tag)
    r = rng(0)
    n = nset[r % len(nset)]
    T0 = vine(n, (r >> 8) % 2 == 0)
    L = Llo + (r >> 16) % (Lhi - Llo + 1)
    x = 1 + (r >> 24) % n
    H = []
    for i in range(L):
        rr = Rng(("s%d" % t).encode(), tag + b"h%d" % i)
        q = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + walk[r % len(walk)]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if q % 3 else "DELETE", x])
        x = min(n, max(1, x + walk[(r >> 9) % len(walk)]))
    return n, T0, H


def main() -> int:
    step("PA-00", "Wall-pressure audit")
    import json
    nkeep = 0
    nheavy = 0
    npressure = 0
    minloads = []
    eb_at_pressure = []
    ex = []
    cfgs = [
        (b"pa1", [16, 32, 64], 4, 18, [-16, -8, -4, -1, 1, 4, 8, 16]),
        (b"pa2", [64, 128], 8, 24, [-32, -16, 16, 32]),
        (b"pa3", [32, 64], 10, 30, [-4, -2, -1, 1, 2, 4]),
    ]
    for tag, nset, Llo, Lhi, walk in cfgs:
        for t in range(80):
            n, T0, H = gen(t, tag, nset, Llo, Lhi, walk)
            pre = E.precompute(n, T0, H)
            res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
            if res["violations"]:
                continue
            g = build_tagged(n, T0, H)
            Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
            pre2 = g["pre"]
            from wp6_eventflow import to_ptr, splay_A, splay_B_push
            A, B = to_ptr(T0), to_ptr(T0)
            Arot = {}
            acc_of = {}
            aid = 0
            for idx, acc in enumerate(pre2):
                A, invs = splay_A(A, acc["x"])
                for (S, sited) in zip(invs, acc["sites"]):
                    Arot[aid] = frozenset(S)
                    acc_of[aid] = idx
                    aid += 1
                if acc["mode"] == "KEEP":
                    B, _ = splay_B_push(B, acc["x"])
            byacc = defaultdict(list)
            for j in range(len(Bevs)):
                byacc[Bevs[j][0]].append(j)
            load = {}
            for acc, js in sorted(byacc.items()):
                xx = pre2[acc]["x"]
                eB = len(js)
                e = elig[js[0]]
                E1s = set(i for i in e["E1"] if Aevs[i][1])
                E4s = set(i for i in e["E4"] if Aevs[i][1])
                if acc > 0 and pre2[acc - 1]["x"] == xx:
                    f = len(E4s)
                else:
                    f = len(E1s)
                nkeep += 1
                if eB <= 3 * f:
                    for j in js:
                        N = set(i for k in elig[j] for i in elig[j][k] if Aevs[i][1])
                        cands = sorted((load.get(i, 0), i) for i in N)
                        if cands and cands[0][0] < 3:
                            ld, i = cands[0]
                            load[i] = ld + 1
                    continue
                nheavy += 1
                E3s = set(i for i in e["E3"] if Aevs[i][1])
                K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
                W = E3s - K - E1s
                E2s = set(i for i in e["E2"] if Aevs[i][1])
                oldn = len(E2s | E4s | K | W)
                # sterile? W-first-overlaps at this access (vs prev B-event N)
                ml = None
                for j in js:
                    N = set(i for k in elig[j] for i in elig[j][k] if Aevs[i][1])
                    cands = sorted((load.get(i, 0), i) for i in N)
                    if cands:
                        ml = cands[0][0] if ml is None else min(ml, cands[0][0])
                    if cands and cands[0][0] < 3:
                        ld, i = cands[0]
                        load[i] = ld + 1
                if oldn <= 2:
                    npressure += 1
                    eb_at_pressure.append(eB)
                    minloads.append(ml)
                    if len(ex) < 8:
                        ex.append({"t": t, "tag": tag.decode(), "acc": acc, "x": xx,
                                   "eB": eB, "f": f, "old": oldn, "ml": ml})
    step("PA-01", "KEEP=%d heavy=%d (%.3f) pressure[B-heavy+old<=2]=%d (%.4f)" % (
        nkeep, nheavy, nheavy / max(1, nkeep), npressure, npressure / max(1, nkeep)))
    import statistics
    step("PA-02", "eB@pressure med=%s max=%s; minload@pressure=%s" % (
        (sorted(eb_at_pressure)[len(eb_at_pressure) // 2] if eb_at_pressure else None),
        (max(eb_at_pressure) if eb_at_pressure else None),
        dict(Counter(minloads))))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pressure.json").write_text(
        json.dumps({"KEEP": nkeep, "heavy": nheavy, "pressure": npressure,
                    "eB_med": (sorted(eb_at_pressure)[len(eb_at_pressure) // 2] if eb_at_pressure else None),
                    "eB_max": (max(eb_at_pressure) if eb_at_pressure else None),
                    "minloads": dict(Counter(minloads)), "ex": ex},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
