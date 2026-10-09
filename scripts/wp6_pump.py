"""WP-6 PUMP: repeatable-drain (negative-cycle) hunt (C182).

Theory: pair-state dynamics are deterministic given (trees, accesses).
If a walk revisits the SAME (A,B) pair-state with STRICTLY LOWER pool
(Phi = 3*SA - EB), the loop segment is repeatable with identical negative
net per iteration => pump pool to -infinity => Phi<0 prefix exists =>
GC-STATIC REFUTED (after explicit pump validation + LG.check).
This channel is NOT covered by one-shot margin assaults (it needs long
repetition, not deep single bursts).
Method: random + greedy-min-pool long walks; canonical pair-state encoding
(nested tuples); map state -> pool-at-first-visit; on revisit with lower
pool, extract loop, pump K times, check Phi<0, validate.
Artifact: bellman/pump.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
import random
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_pushledger import gen
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import vine, balanced, depths_of
from solver import encode as E
from solver import legality as LG


def step(sid, msg):
    print("[WP-6][PUMP %s] %s" % (sid, msg), flush=True)


def canon(T):
    if T is None:
        return None
    return (T["k"], canon(T["l"]), canon(T["r"]))


def run_walk(n, T0, H):
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    seen = {}
    for i, (mode, x) in enumerate(H):
        key = (canon(A), canon(B))
        pool = 3 * SA - EB
        if key in seen:
            prev_pool, prev_i = seen[key]
            if pool < prev_pool:
                return {"pump": True, "loop": H[prev_i:i],
                        "drop": prev_pool - pool, "at": i,
                        "prefix": list(H[:prev_i])}
        else:
            seen[key] = (pool, i)
        A, invs = splay_A(A, x)
        eA = len(invs)
        eB = 0
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
        SA += eA
        EB += eB if mode == "KEEP" else 0
    return {"pump": False, "states": len(seen)}


def pump_validate(n, T0, prefix, loop, times):
    H = list(prefix) + list(loop) * times
    LG.check(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    minphi = 0
    for mode, x in H:
        A, invs = splay_A(A, x)
        eB = 0
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
        SA += len(invs)
        EB += eB if mode == "KEEP" else 0
        phi = 3 * SA - EB
        if phi < minphi:
            minphi = phi
    return minphi, len(H)


def main() -> int:
    step("PU-00", "repeatable-drain pump hunt")
    out = {"runs": [], "kills": []}
    cfgs = []
    for n in (16, 32, 64):
        cfgs.append((n, vine(n)))
        cfgs.append((n, balanced(list(range(1, n + 1)))))
    for n, T0 in cfgs:
        for s in range(12):
            rng = random.Random(30000 + s)
            _, _, H0 = gen(31000 + s, b"pu")
            H0 = [st for st in H0 if st[1] <= n]
            # extend: random long walk biased to revisits (cycle-friendly keys)
            H = list(H0)
            keys = list(range(1, n + 1))
            for _ in range(400):
                if rng.random() < 0.7 and H:
                    # repeat recent key (revisit pressure)
                    H.append([rng.choice(["KEEP", "DELETE"]),
                              rng.choice(H[-8:])[1]
                              if len(H) >= 8 else rng.choice(keys)])
                else:
                    H.append([rng.choice(["KEEP", "DELETE"]),
                              rng.choice(keys)])
            try:
                pre = E.precompute(n, T0, H)
                bad = E.exec_counts(pre, "P_all", 6, 2, (2, 2))["violations"]
            except Exception:
                continue
            if bad:
                continue
            try:
                r = run_walk(n, T0, H)
            except Exception as ex:
                step("PU-ERR", "%r" % (ex,))
                continue
            rec = {"n": n, "s": s, "states": r.get("states"),
                   "pump": r.get("pump"), "drop": r.get("drop")}
            out["runs"].append(rec)
            if r.get("pump"):
                step("PU-PUMP", "n=%d s=%d drop=%d loop=%d" % (
                    n, s, r["drop"], len(r["loop"])))
                times = 2 + (r["drop"] and 50 // max(1, r["drop"]) or 50)
                try:
                    mp, L = pump_validate(n, T0, r["prefix"], r["loop"],
                                          times)
                except Exception as ex:
                    rec["validate"] = "invalid:%r" % (ex,)
                    continue
                rec["validate"] = {"minphi": mp, "L": L}
                if mp < 0:
                    out["kills"].append({"n": n, "s": s, "phi": mp,
                                        "Hlen": L})
                    step("PU-KILL", "PUMPED NEGATIVE PHI n=%d" % n)
    bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "bellman"
    bd.mkdir(parents=True, exist_ok=True)
    (bd / "pump.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str),
        encoding="utf-8")
    step("PU-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
