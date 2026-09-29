"""WP-6 STEP AS-00: Stage-B direct falsifier (max_b min-load-before).

Objective: maximize over B-events min-load-before under canonical least-loaded.
Mutations bias: repeat B-heavy same-key, sterile ancestors, thin E1/E2/E4,
suppressed refreshment, long tenure, concentrated loads.
Kill: minload>=3 (STARVE + starve.json + exit 2). minload>=2: SAVE witness,
CONTINUE (stronger claim already dead; Stage B needs >=3).
Phase W: seed from banked M2 witness (m2witness.json) + mutate to extend drain.
Phase G: generic DRBG seeds + hillclimb.
NEW artifacts: advstage.json (+starve.json ONLY on kill). Sealed files untouched.
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


def maxminload(n, T0, H):
    pre = E.precompute(n, T0, H)
    res = E.exec_counts(pre, "P_all", 6, 2, (2, 2))
    if res["violations"]:
        return -2, None
    g = build_tagged(n, T0, H)
    Aevs, Bevs, elig = g["Aevs"], g["Bevs"], g["elig"]
    load = {}
    best = -1
    best_at = None
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
        else:
            return 99, j
    return best, best_at


def mutate(H, n, r):
    H2 = copy.deepcopy(H)
    op = r % 5
    if op == 0 and H2:
        i = (r >> 5) % len(H2)
        H2[i][0] = "DELETE" if H2[i][0] == "KEEP" else "KEEP"
    elif op == 1 and H2:
        i = (r >> 5) % len(H2)
        H2[i][1] = 1 + (r >> 13) % n
    elif op == 2 and len(H2) < 70:
        H2.insert((r >> 5) % (len(H2) + 1), ["KEEP" if r % 2 else "DELETE", 1 + (r >> 13) % n])
    elif op == 3 and H2:
        # repeat-key: duplicate a KEEP (sustain same-key pressure)
        keeps = [i for i, a in enumerate(H2) if a[0] == "KEEP"]
        if keeps:
            i = keeps[(r >> 5) % len(keeps)]
            H2.insert(i + 1, ["KEEP", H2[i][1]])
    elif len(H2) > 4:
        del H2[(r >> 5) % len(H2)]
    return H2


def main() -> int:
    step("AS-00", "Stage-B direct falsifier")
    import json
    best = -1
    m2wit = None
    evals = 0
    holders = []
    # Phase W: M2 witness seed
    try:
        w = json.load(open(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "m2witness.json"))["witness"]
        holders.append((w["T0"], w["H"], w["n"], 2))
        step("AS-W", "seeded M2 witness n=%d lenH=%d" % (w["n"], len(w["H"])))
    except Exception as ex:
        step("AS-W", "no M2 seed (%s)" % ex)
    # Phase G: generic seeds
    for s in range(120):
        rng = Rng(("s%d" % s).encode(), b"as")
        r = rng(0)
        n = [32, 64, 128][r % 3]
        T0 = vine(n, (r >> 8) % 2 == 0)
        rr = Rng(("s%d" % s).encode(), b"ash")
        H = H_walk(rr, n, 12 + (r >> 16) % 24, 1 + (r >> 24) % n)
        v, at = maxminload(n, T0, H)
        evals += 1
        if v == -2:
            step("AS-KILL", "present kill s=%d" % s)
            return 2
        if v == 99:
            step("AS-KILL", "STARVATION seed s=%d bev=%s" % (s, at))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "where": at, "H": H}, indent=1, default=str),
                encoding="utf-8")
            return 2
        if v > best:
            best = v
        holders.append((T0, H, n, v))
        if v >= 2 and m2wit is None and len(holders) > 4:
            m2wit = {"n": n, "H": copy.deepcopy(H), "ml": v, "at": at}
    holders.sort(key=lambda z: z[3], reverse=True)
    holders = holders[:12]
    step("AS-01", "seeds evals=%d best=%d" % (evals, best))
    it = 0
    while evals < 20000:
        it += 1
        r = int.from_bytes(_h.sha256(b"asm|%d" % it).digest(), "big")
        T0, H, n, _ = holders[(r >> 2) % len(holders)]
        H2 = mutate(H, n, r)
        v, at = maxminload(n, T0, H2)
        evals += 1
        if v == -2:
            step("AS-KILL", "present kill it=%d" % it)
            return 2
        if v == 99:
            step("AS-KILL", "STARVATION it=%d bev=%s" % (it, at))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "starve.json").write_text(
                json.dumps({"kill": True, "where": at, "H": H2}, indent=1, default=str),
                encoding="utf-8")
            return 2
        if v > best:
            best = v
            holders.append((T0, H2, n, v))
            holders.sort(key=lambda z: z[3], reverse=True)
            holders = holders[:12]
            if v >= 2 and m2wit is None:
                m2wit = {"n": n, "H": copy.deepcopy(H2), "ml": v, "at": at}
        if it % 2000 == 0:
            step("AS-02", "it=%d evals=%d best=%d" % (it, evals, best))
    step("AS-03", "evals=%d best=%d" % (evals, best))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "advstage.json").write_text(
        json.dumps({"evals": evals, "best": best, "m2witness": m2wit},
                   indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
