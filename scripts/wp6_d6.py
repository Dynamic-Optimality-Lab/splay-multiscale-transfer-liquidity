"""WP-6 D6: DIRECT-D6 deficit assault (C169).

DIRECT-D6 target: D(t) <= 6*S_A(t) for every present-legal prefix, where
D = sum over KEEPs of need = max(y-2a,0) (y = dB+1 B-cost, a = dA+1 A-cost),
S_A = all sited A-StepEvs (8S: all Aevs sited).
Key identity (D2 banked: need <= y-1 <= 2e_B per KEEP):
    D6-def := D - 6*S_A = 2*(E_B - 3*S_A) - slack,
    slack := sum over KEEPs of (2*e_B - need) >= 0 per access.
So D6 failsovic <=> GC-deficit > slack/2: big overflow with small slack.
Greedy + beam builders maximizing instant (need - 6*e_A) and terminal
D6-deficit, on vine/balanced/comb/zigzag T0, n=16..64, present domain
(absent-key accesses skipped: D2 needs present keys).
Any D6-def > 0 is re-validated via LG.check + independent recompute;
a valid witness REFUTES DIRECT-D6 (and GC-STATIC with it, since
D6-def > 0 => 2*GC-def > slack >= 0 => GC-def > 0).
Artifact: d6.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_adv import vine, balanced, comb, zigzag, depths_of
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import legality as LG
from liquidity import legacy_embedding as PE


def step(sid, msg):
    print("[WP-6][D6 %s] %s" % (sid, msg), flush=True)


def access_stats(A, B, SA, SAdel, EB, D, mode, x):
    """Simulate one access on COPIES. Returns full ledger deltas."""
    # present-domain gate: skip absent keys (D2 needs present)
    _, pathA = PE._depth_to(A, x)
    if not pathA or pathA[-1]["k"] != x:
        return None
    A2 = copy.deepcopy(A)
    B2 = copy.deepcopy(B)
    A2, invs = splay_A(A2, x)
    eA = len(invs)
    # A-cost a = depth+1 BEFORE splay (present): dA+1
    da = depths_of(A).get(x, 0)
    a = da + 1
    eB = 0
    y = 0
    need = 0
    if mode == "KEEP":
        db = depths_of(B).get(x, 0)
        y = db + 1
        B2, pushes = splay_B_push(B2, x)
        eB = len(pushes)
        need = y - 2 * a
        if need < 0:
            need = 0
    SA2 = SA + eA
    EB2 = EB + (eB if mode == "KEEP" else 0)
    D2 = D + (need if mode == "KEEP" else 0)
    d6def = D2 - 6 * SA2
    gcdef = EB2 - 3 * SA2
    slack = (2 * eB - need) if mode == "KEEP" else 0
    return (A2, B2, SA2, EB2, D2, eA, eB, a, y, need, d6def, gcdef, slack)


def greedy(n, T0, L, seed):
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = D = 0
    SAdel = 0
    H = []
    best = {"d6": None, "H": None}
    import hashlib
    rng = int.from_bytes(hashlib.sha256(b"d6|%d|%d" % (n, seed)).digest()[:8], "big")
    order = list(range(1, n + 1))
    for i in range(L):
        cands = []
        # rotate key order deterministically for diversity
        ks = order[i % n:] + order[:i % n]
        for x in ks:
            for mode in ("KEEP", "DELETE"):
                r = access_stats(A, B, SA, SAdel, EB, D, mode, x)
                if r is None:
                    continue
                (A2, B2, SA2, EB2, D2, eA, eB, a, y, need,
                 d6def, gcdef, slack) = r
                # instant D6-deficit contribution + terminal deficit
                inst = (need - 6 * eA) if mode == "KEEP" else (-6 * eA)
                cands.append((d6def, inst, mode, x, r))
        if not cands:
            break
        # maximize terminal deficit, tie-break by instant
        cands.sort(key=lambda c: (c[0], c[1]), reverse=True)
        _, _, mode, x, r = cands[0]
        (A, B, SA, EB, D, eA, eB, a, y, need, d6def, gcdef, slack) = r
        if mode == "DELETE":
            SAdel += eA
        H.append([mode, x])
        if best["d6"] is None or d6def > best["d6"]:
            best = {"d6": d6def, "H": list(H), "gc": gcdef,
                    "i": i, "mode": mode, "x": x, "eA": eA, "eB": eB,
                    "need": need}
        if d6def > 0:
            break
    return best


def validate(n, T0, H):
    LG.check(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = D = 0
    maxd6 = None
    for mode, x in H:
        _, pathA = PE._depth_to(A, x)
        if not pathA or pathA[-1]["k"] != x:
            continue
        da = depths_of(A).get(x, 0)
        A, invs = splay_A(A, x)
        eA = len(invs)
        eB = 0
        need = 0
        if mode == "KEEP":
            db = depths_of(B).get(x, 0)
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
            need = (db + 1) - 2 * (da + 1)
            if need < 0:
                need = 0
        SA += eA
        EB += eB if mode == "KEEP" else 0
        D += need if mode == "KEEP" else 0
        d6 = D - 6 * SA
        if maxd6 is None or d6 > maxd6:
            maxd6 = d6
    return maxd6


def main() -> int:
    step("D6-00", "DIRECT-D6 deficit assault")
    out = {"runs": [], "kills": []}
    shapes = []
    for n in (16, 32, 64):
        shapes.append(("vine%d" % n, n, vine(n)))
        shapes.append(("bal%d" % n, n, balanced(list(range(1, n + 1)))))
    shapes.append(("comb32", 32, comb(32)))
    shapes.append(("zig32", 32, zigzag(32)))
    for nm, n, T0 in shapes:
        for L in (60, 120):
            for seed in (0, 1):
                try:
                    b = greedy(n, T0, L, seed)
                except Exception as ex:
                    step("D6-ERR", "%s: %r" % (nm, ex))
                    continue
                rec = {"shape": nm, "L": L, "seed": seed,
                       "d6": b["d6"], "gc": b.get("gc"), "i": b.get("i"),
                       "mode": b.get("mode"), "x": b.get("x"),
                       "eA": b.get("eA"), "eB": b.get("eB"),
                       "need": b.get("need")}
                out["runs"].append(rec)
                step("D6-R", "%s L=%d s=%d d6=%s gc=%s" % (
                    nm, L, seed, b["d6"], b.get("gc")))
                if b["d6"] is not None and b["d6"] > 0 and b["H"]:
                    try:
                        v = validate(n, T0, b["H"])
                    except Exception as ex:
                        rec["validate"] = "invalid:%r" % (ex,)
                        continue
                    rec["validate"] = v
                    if v is not None and v > 0:
                        out["kills"].append({"shape": nm, "H": b["H"],
                                            "d6": v})
                        step("D6-KILL", "D6-DEFICIT POSITIVE %s" % nm)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "d6.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("D6-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
