"""WP-6 STEP RF-00: post-E4-causality-fix re-verification battery.

Recomputes headline Stage-B numbers with causal E4 (setup-at-idx snapshot):
  1. LL-corpus (leastload seeds): maxload / starved.
  2. ML-corpus (minload seeds): minload-2 count + worst.
  3. M2-witness reverify (fixed tagged): minload trace around bev88; any >=3?
  4. E1-zone recheck (E1-CAP empirical leg still stands?).
  5. Entry census (E1@1 should vanish) + savior-class spot.
  6. Exhaustive n=3,4 cells re-run (fixed builders).
  7. Fixed-builder minload-3 hillclimb (1500 evals): THE critical question —
     does causal E4 yield minload>=3 / starvation?
NEW artifact: refix.json. Sealed artifacts NEVER overwritten.
"""
from __future__ import annotations
import sys
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow_abl import build_tagged
from wp6_eventflow2 import build2
from solver import encode as E


def step(sid: str, msg: str) -> None:
    print("[WP-6][STEP %s] %s" % (sid, msg), flush=True)


import hashlib as _h


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


class DRBG:
    def __init__(self, s, tag):
        self.s = s
        self.tag = tag
        self.c = 0

    def b(self):
        self.c += 1
        return _h.sha256(self.tag + b"|%s|%d" % (self.s, self.c)).digest()

    def below(self, n):
        bound = (1 << 256) - ((1 << 256) % n)
        while True:
            v = int.from_bytes(self.b(), "big")
            if v < bound:
                return v % n

    def ir(self, a, b): return a + self.below(b - a + 1)

    def ch(self, s): return s[self.below(len(s))]


def H_walk(rng, n, L, x0, tag_extra=None):
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


def replay_minload(g):
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    best = -1
    best_at = None
    maxload = 0
    starve = 0
    for j in range(len(Bevs)):
        e = elig[j]
        cands = sorted((load.get(i, 0), i) for k in e for i in e[k] if Aevs[i][1])
        if not cands:
            continue
        if cands[0][0] > best:
            best, best_at = cands[0][0], j
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
            maxload = max(maxload, ld + 1)
        else:
            starve += 1
    return best, best_at, maxload, starve, len(Bevs)


def main() -> int:
    step("RF-00", "Post-fix re-verification battery")
    import json
    out = {}
    # 1. LL corpus (same seeds as wp6_leastload)
    maxload = starve = nB = 0
    for t in range(120):
        rng = DRBG(("ll%d" % t).encode(), b"ll")
        n = rng.ch([16, 32, 64])
        T0 = vine(n, rng.below(2) == 0)
        H = H_walk(rng, n, rng.ir(4, 18), rng.ir(1, n))
        # NOTE ll-corpus walk differs slightly (x drift set); recompute inline:
        # (rebuild exactly as wp6_leastload for fidelity)
        rng2 = DRBG(("ll%d" % t).encode(), b"ll")
        n = rng2.ch([16, 32, 64])
        T0 = vine(n, rng2.below(2) == 0)
        L = rng2.ir(4, 18)
        x = rng2.ir(1, n)
        H = []
        for i in range(L):
            if i % 4 == 3:
                y = rng2.ir(1, n)
                H.append(["DELETE", y if y != x else (1 if x != 1 else n)])
            else:
                H.append([rng2.ch(["KEEP", "DELETE", "DELETE", "KEEP"]), x])
            x = min(n, max(1, x + rng2.ch([-16, -8, -4, -1, 1, 4, 8, 16])))
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("RF-KILL", "present kill ll t=%d" % t)
            return 2
        g = build2(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        load = {}
        for j in range(len(Bevs)):
            nB += 1
            cands = [(load.get(i, 0), i) for i in elig[j] if Aevs[i][1]]
            cands.sort()
            for (ld, i) in cands:
                if ld < 3:
                    load[i] = ld + 1
                    maxload = max(maxload, ld + 1)
                    break
            else:
                if cands:
                    starve += 1
    out["LL"] = {"B": nB, "maxload": maxload, "starved": starve}
    step("RF-01", "LL fixed: B=%d maxload=%d starved=%d (was 2331/2/0)" % (nB, maxload, starve))
    # 2. ML corpus (same seeds as wp6_minload? approximate: ma-style + minload-style)
    # use saturation MA corpus (deterministic, banked B=3852 baseline)
    sys.path.insert(0, str(ROOT / "scripts"))
    from wp6_saturation import ma_history, replay
    m2 = 0
    for t in range(100):
        n, T0, H = ma_history(t)
        g = build_tagged(n, T0, H)
        best, at, _, _, _ = replay_minload(g)
        if best >= 2:
            m2 += 1
    out["MAm2"] = {"hist_with_m2": m2}
    step("RF-02", "MA fixed: hist_with_m2=%d/100 (was 0/100)" % m2)
    # 3. M2 witness reverify
    w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
    g = build_tagged(w["n"], w["T0"], w["H"])
    best, at, maxload_w, starve_w, nBw = replay_minload(g)
    out["M2"] = {"best": best, "at": at, "maxload": maxload_w, "starve": starve_w, "B": nBw}
    step("RF-03", "M2 fixed: best=%d at=%s maxload=%d starve=%d (was 2/88/-/-)" % (best, at, maxload_w, starve_w))
    # 4. E1-zone recheck on LS corpus (120 hist)
    sys.path.insert(0, str(ROOT / "scripts"))
    from wp6_loadstruct import gen
    n1 = v1 = n2 = v2 = 0
    e1e1 = 0
    for t in range(120):
        n, T0, H = gen(t)
        g = build_tagged(n, T0, H)
        Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
        pre2 = g["pre"]
        load = {}
        prevN = None
        for j in range(len(Bevs)):
            acc = Bevs[j][0]
            e = elig[j]
            N = set(i for k in e for i in e[k] if Aevs[i][1])
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            for i in (N - prevN if prevN is not None else set()):
                if i in E1s and load.get(i, 0) != 0:
                    e1e1 += 1
            prevN = N
            eA = sum(1 for z in pre2[acc]["sites"] if z)
            eB = sum(1 for jj in range(len(Bevs)) if Bevs[jj][0] == acc)
            cands = sorted((load.get(i, 0), i) for i in N)
            ml = cands[0][0] if cands else None
            if ml is not None:
                if eB <= 2 * eA:
                    n1 += 1
                    v1 += (ml > 1)
                if eB <= 3 * eA:
                    n2 += 1
                    v2 += (ml > 2)
            if cands and cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
    out["E1zone"] = {"n1": n1, "viol1": v1, "n2": n2, "viol2": v2, "E1nonzero_entry": e1e1}
    step("RF-04", "E1zone fixed: ml<=1 %d/%d v=%d; ml<=2 %d/%d v=%d; E1@>0 entries=%d"
         % (n1 - v1, n1, v1, n2 - v2, n2, v2, e1e1))
    # 5. savior spot (SV corpus, 150 hist): savior classes + entry loads
    from wp6_savior import gen as sgen
    from collections import Counter
    sav = Counter()
    ent3 = 0
    nBm = 0
    for t in range(150):
        n, T0, H = sgen(t)
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
        load = {}
        first_seen = {}
        for j in range(len(Bevs)):
            nBm += 1
            acc = Bevs[j][0]
            xx = pre2[acc]["x"]
            e = elig[j]
            E1s = set(i for i in e["E1"] if Aevs[i][1])
            E3s = set(i for i in e["E3"] if Aevs[i][1])
            K = set(i for i in E3s if xx in Arot.get(i, ()) and acc_of.get(i, acc) < acc)
            W = E3s - K - E1s
            E2s = set(i for i in e["E2"] if Aevs[i][1])
            E4s = set(i for i in e["E4"] if Aevs[i][1])
            N = E1s | E3s | E2s | E4s
            for i in N:
                if i not in first_seen:
                    first_seen[i] = load.get(i, 0)
                    if load.get(i, 0) >= 3:
                        ent3 += 1
            cands = sorted((load.get(i, 0), i) for i in N)
            if cands and cands[0][0] >= 1:
                ld, sv = cands[0]
                cls = ("E1" if sv in E1s else ("K" if sv in K else ("W" if sv in W
                    else ("E2" if sv in E2s else ("E4" if sv in E4s else "E7")))))
                sav[cls] += 1
            if cands and cands[0][0] < 3:
                ld, i = cands[0]
                load[i] = ld + 1
    out["SAV"] = {"B": nBm, "savior": dict(sav), "entry3": ent3}
    step("RF-05", "SAV fixed: B=%d sav=%s entry3=%d (was W65/K25/E2-11/E1-3, e3=0)" % (nBm, dict(sav), ent3))
    # 6. exhaustive n=3,4 fixed
    from wp6_exhaustive import all_bsts, maxminload
    ex = {}
    for (n, L) in ((3, 7), (4, 5)):
        trees = all_bsts(range(1, n + 1))
        moves = [[m, x] for m in ("KEEP", "DELETE") for x in range(1, n + 1)]
        cmax = -1
        tot = 0
        for T0 in trees:
            seq = [0] * L
            done = False
            while not done:
                H = [list(moves[i]) for i in seq]
                v, at = maxminload(n, T0, H)
                tot += 1
                if v == -2:
                    step("RF-KILL", "present kill n=%d" % n)
                    return 2
                if v == 99:
                    step("RF-KILL", "STARVATION n=%d H=%s" % (n, H))
                    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                        json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
                    return 2
                cmax = max(cmax, v)
                for p in range(L - 1, -1, -1):
                    seq[p] += 1
                    if seq[p] < len(moves):
                        break
                    seq[p] = 0
                    if p == 0:
                        done = True
        ex[str(n)] = {"total": tot, "max": cmax}
        step("RF-06", "exhaustive fixed n=%d total=%d max=%d" % (n, tot, cmax))
    out["EX"] = ex
    # 7. fixed-builder minload-3 hillclimb 1500 evals
    import hashlib as _hh
    best = -1
    holders = []
    for s in range(60):
        r = int.from_bytes(_hh.sha256(b"rf|%d" % s).digest(), "big")
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = DRBG(("s%d" % s).encode(), b"rfh")
        H = H_walk(rr, n, 12 + (r >> 16) % 20, 1 + (r >> 24) % n)
        pre = E.precompute(n, T0, H)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("RF-KILL", "present kill seed %d" % s)
            return 2
        g = build_tagged(n, T0, H)
        v, at, _, _, _ = replay_minload(g)
        if v == 99:
            step("RF-KILL", "STARVATION seed %d" % s)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "H": H}, indent=1, default=str), encoding="utf-8")
            return 2
        best = max(best, v)
        holders.append((T0, H, n, v))
    holders.sort(key=lambda z: z[3], reverse=True)
    holders = holders[:10]
    evals = 60
    it = 0
    while evals < 1500:
        it += 1
        r = int.from_bytes(_hh.sha256(b"rfm|%d" % it).digest(), "big")
        T0, H, n, _ = holders[(r >> 2) % len(holders)]
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
        pre = E.precompute(n, T0, H2)
        res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
        if res["violations"]:
            step("RF-KILL", "present kill it %d" % it)
            return 2
        g = build_tagged(n, T0, H2)
        v, at, _, _, _ = replay_minload(g)
        evals += 1
        if v == 99:
            step("RF-KILL", "STARVATION it=%d bev=%s" % (it, at))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "where": at, "H": H2}, indent=1, default=str),
                encoding="utf-8")
            return 2
        if v > best:
            best = v
            holders.append((T0, H2, n, v))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:10]
    out["HILL"] = {"evals": evals, "best": best}
    step("RF-07", "hillclimb fixed: evals=%d best=%d" % (evals, best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "refix.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
