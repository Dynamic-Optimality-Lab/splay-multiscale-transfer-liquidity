"""WP-6 STEP EH-00: entry@3 adversarial hunt (ENTRY-FRESH direct target).

Objective: maximize over B-events/sources the load-at-entry (entering N(b)
vs previous B-event's N). Re-entry engineering bias: sustain B-heavy same-key
(triple-pick sources), then swing triples back (new keys near old rotated sets),
repeat-key concentration, long tenures.
entry@3 found => SAVE witness (full context) + CONTINUE (does NOT refute Stage B;
needs convergence). No entry@3 => bank max-2 (ENTRY-FRESH finite evidence).
Also: M2 load-3 re-entry check (does the known load-3 ever re-enter later?).
NEW artifact: entryhunt.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import copy
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


def H_walk(rr, n, L, x0):
    H = []
    x = x0
    for i in range(L):
        r = rr(1000 + i)
        if i % 4 == 3:
            y = min(n, max(1, x + [-32, -16, 16, 32][r % 4]))
            H.append(["DELETE", y if y != x else 1])
            H.append(["KEEP", x])
        else:
            H.append(["KEEP" if r % 3 else "DELETE", x])
        x = min(n, max(1, x + [-16, -8, -4, -1, 1, 4, 8, 16][(r >> 9) % 8]))
    return H


def maxentry(n, T0, H):
    """Max entry-load + minload info. Returns (me, me_at, ml_best, starve)."""
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None, None, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    me = -1
    me_at = None
    ml_best = -1
    starve = 0
    prevN = None
    for j in range(len(Bevs)):
        e = elig[j]
        N = set(i for k in e for i in e[k] if Aevs[i][1])
        new = N - prevN if prevN is not None else set()
        for i in new:
            lv = load.get(i, 0)
            if lv > me:
                me, me_at = lv, (j, i)
        prevN = N
        cands = sorted((load.get(i, 0), i) for i in N)
        if not cands:
            continue
        ml_best = max(ml_best, cands[0][0])
        if cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
        else:
            starve += 1
    return me, me_at, ml_best, starve


def main() -> int:
    step("EH-00", "Entry@3 adversarial hunt")
    import json
    # M2 load-3 re-entry check first
    w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
    g = build_tagged(w["n"], w["T0"], w["H"])
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    l3src = None
    reenter = []
    seen = set()
    prevN = None
    for j in range(len(Bevs)):
        e = elig[j]
        N = set(i for k in e for i in e[k] if Aevs[i][1])
        if prevN is not None:
            for i in N - prevN:
                if i in seen and load.get(i, 0) >= 2:
                    reenter.append((j, i, load.get(i, 0)))
        seen |= N
        prevN = N
        cands = sorted((load.get(i, 0), i) for i in N)
        if cands and cands[0][0] < 3:
            ld, i = cands[0]
            load[i] = ld + 1
            if ld + 1 >= 3 and l3src is None:
                l3src = (j, i)
    step("EH-M2", "load3 minted at %s; later re-entries@>=2: %s" % (l3src, reenter[:10]))
    best = -1
    bestwit = None
    evals = 0
    holders = [(w["T0"], w["H"], w["n"], 0)]
    for s in range(80):
        rng = Rng(("s%d" % s).encode(), b"eh")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"ehh")
        H = H_walk(rr, n, 12 + (r >> 16) % 20, 1 + (r >> 24) % n)
        me, at, ml, st = maxentry(n, T0, H)
        evals += 1
        if me == -2:
            step("EH-KILL", "present kill s=%d" % s)
            return 2
        if st:
            step("EH-KILL", "STARVATION s=%d" % s)
            return 2
        best = max(best, me)
        holders.append((T0, H, n, me))
        if me >= 3 and bestwit is None:
            bestwit = {"n": n, "H": copy.deepcopy(H), "at": at}
    holders.sort(key=lambda z: z[3], reverse=True)
    holders = holders[:12]
    step("EH-01", "seeds evals=%d best_entry=%d" % (evals, best))
    it = 0
    while evals < 30000:
        it += 1
        r = int.from_bytes(_h.sha256(b"ehm|%d" % it).digest(), "big")
        T0, H, n, _ = holders[(r >> 2) % len(holders)]
        H2 = copy.deepcopy(H)
        op = r % 5
        if op == 0 and H2:
            i = (r >> 5) % len(H2)
            H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
        elif op == 1 and H2:
            i = (r >> 5) % len(H2)
            H2[i][1] = 1 + (r >> 13) % n
        elif op == 2 and len(H2) < 70:
            # re-entry engineering: repeat a recent KEEP key (swing triples back)
            keeps = [a[1] for a in H2 if a[0] == "KEEP"][-6:]
            k = keeps[(r >> 5) % len(keeps)] if keeps else 1 + (r >> 13) % n
            H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", k])
        elif op == 3 and H2:
            keeps = [a[1] for a in H2 if a[0] == "KEEP"][-6:]
            if keeps:
                H2.append(["KEEP", keeps[(r >> 5) % len(keeps)]])
            else:
                H2.append(["KEEP", 1 + (r >> 13) % n])
        elif len(H2) > 4:
            del H2[(r >> 5) % len(H2)]
        me, at, ml, st = maxentry(n, T0, H2)
        evals += 1
        if me == -2:
            step("EH-KILL", "present kill it=%d" % it)
            return 2
        if st:
            step("EH-KILL", "STARVATION it=%d" % it)
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "H": H2}, indent=1, default=str), encoding="utf-8")
            return 2
        if me > best:
            best = me
            holders.append((T0, H2, n, me))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:12]
            if me >= 3 and bestwit is None:
                bestwit = {"n": n, "H": copy.deepcopy(H2), "at": at}
                step("EH-WIT", "ENTRY@3 it=%d at=%s" % (it, at))
        elif (r >> 6) % 4 == 0:
            holders.append((T0, H2, n, me))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:12]
        if it % 5000 == 0:
            step("EH-02", "it=%d evals=%d best_entry=%d" % (it, evals, best))
    step("EH-03", "evals=%d best_entry=%d wit=%s" % (evals, best, bestwit is not None))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "entryhunt.json").write_text(
        json.dumps({"evals": evals, "best_entry": best, "witness": bestwit,
                    "m2_l3src": l3src, "m2_reenter": reenter[:10]},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
