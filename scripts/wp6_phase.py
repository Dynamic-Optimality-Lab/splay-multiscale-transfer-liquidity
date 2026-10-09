"""WP-6 PHASE: phased kill-attempt for the diverged step (C173).

Kill blueprint: (1) FREERIDE xc to (dA>=1, dB large) [beam, xc unaccessed];
(2) GRIND pool to exactly 0 via covered drains that leave xc UNDISTURBED
(delta 0 in both trees); (3) BURST xc (e_A>=1 from floor, e_B large):
overflow > 0 = pool => MARGIN NEGATIVE => GC-STATIC REFUTED.
Phase 2 uses only accesses with zero depth-delta on xc in both trees
(x-frozen) and nonnegative pool throughout (covered). If grind stalls
(pool>0) or bursts stay covered, the boundary is documented.
Any margin<0 re-validated via LG.check + independent recompute.
Artifact: phase.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_adv import vine, balanced, depths_of
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import legality as LG


def step(sid, msg):
    print("[WP-6][PHASE %s] %s" % (sid, msg), flush=True)


def phase1(n, T0, xc, L, W):
    A0, B0 = to_ptr(T0), to_ptr(T0)
    beam = [(0.0, A0, B0, 0, 0, [])]
    for _ in range(L):
        cands = []
        for _, A, B, SA, EB, H in beam:
            for x in range(1, n + 1):
                if x == xc:
                    continue
                for mode in ("KEEP", "DELETE"):
                    A2 = copy.deepcopy(A)
                    B2 = copy.deepcopy(B)
                    A2, invs = splay_A(A2, x)
                    eA = len(invs)
                    eB = 0
                    if mode == "KEEP":
                        B2, pushes = splay_B_push(B2, x)
                        eB = len(pushes)
                    SA2 = SA + eA
                    EB2 = EB + (eB if mode == "KEEP" else 0)
                    if 3 * SA2 - EB2 < 0:
                        continue
                    dA2 = depths_of(A2).get(xc, 0)
                    dB2 = depths_of(B2).get(xc, 0)
                    score = dA2 - 2.0 * min(dB2, 14)
                    cands.append((score, A2, B2, SA2, EB2, H + [[mode, x]]))
        if not cands:
            break
        cands.sort(key=lambda c: c[0])
        beam = cands[:W]
    # return diverse heads: lowest dA with dB>=7
    scored = []
    for _, A, B, SA, EB, H in beam:
        dA = depths_of(A).get(xc, 0)
        dB = depths_of(B).get(xc, 0)
        if dB >= 7:
            scored.append((dA, A, B, SA, EB, H))
    scored.sort(key=lambda s: s[0])
    return scored[:12]


def phase2(states, n, xc, L):
    """Grind pool to 0 with xc undisturbed. Returns best (pool, state)."""
    out = []
    for dA0, A0, B0, SA0, EB0, H0 in states:
        A, B, SA, EB = copy.deepcopy(A0), copy.deepcopy(B0), SA0, EB0
        H = list(H0)
        for _ in range(L):
            dAx = depths_of(A).get(xc, 0)
            dBx = depths_of(B).get(xc, 0)
            best = None
            for x in range(1, n + 1):
                for mode in ("KEEP", "DELETE"):
                    A2 = copy.deepcopy(A)
                    B2 = copy.deepcopy(B)
                    A2, invs = splay_A(A2, x)
                    eA = len(invs)
                    eB = 0
                    if mode == "KEEP":
                        B2, pushes = splay_B_push(B2, x)
                        eB = len(pushes)
                    # x-frozen: xc depth unchanged in both trees
                    if depths_of(A2).get(xc, -1) != dAx:
                        continue
                    if depths_of(B2).get(xc, -1) != dBx:
                        continue
                    SA2 = SA + eA
                    EB2 = EB + (eB if mode == "KEEP" else 0)
                    pool2 = 3 * SA2 - EB2
                    if pool2 < 0:
                        continue
                    if best is None or pool2 < best[0]:
                        best = (pool2, A2, B2, SA2, EB2, mode, x)
            if best is None:
                break
            pool2, A, B, SA, EB, mode, x = best
            H.append([mode, x])
            if pool2 == 0:
                break
        dA = depths_of(A).get(xc, 0)
        dB = depths_of(B).get(xc, 0)
        out.append({"pool": 3 * SA - EB, "dA": dA, "dB": dB,
                    "H": H, "A": A, "B": B, "SA": SA, "EB": EB})
    out.sort(key=lambda r: (r["pool"], -r["dB"]))
    return out


def main() -> int:
    step("PH-00", "phased kill-attempt (freeride-grind-burst)")
    out = {"runs": [], "kills": []}
    for n in (16, 32):
        for nm, T0 in (("vine%d" % n, vine(n)),
                       ("bal%d" % n, balanced(list(range(1, n + 1))))):
            xc = n // 2
            try:
                states = phase1(n, T0, xc, 50, 48)
            except Exception as ex:
                step("PH-ERR", "%s p1: %r" % (nm, ex))
                continue
            if not states:
                step("PH-R", "%s no freeride states" % nm)
                continue
            try:
                res = phase2(states, n, xc, 120)
            except Exception as ex:
                step("PH-ERR", "%s p2: %r" % (nm, ex))
                continue
            for r in res[:4]:
                # phase 3: burst xc
                A2 = copy.deepcopy(r["A"])
                B2 = copy.deepcopy(r["B"])
                A2, invs = splay_A(A2, xc)
                eA = len(invs)
                B2, pushes = splay_B_push(B2, xc)
                eB = len(pushes)
                margin = r["pool"] - (eB - 3 * eA)
                rec = {"shape": nm, "pool": r["pool"], "dA": r["dA"],
                       "dB": r["dB"], "eA": eA, "eB": eB, "margin": margin}
                out["runs"].append(rec)
                step("PH-R", "%s pool=%d (%d,%d) burst(%d,%d) margin=%d" % (
                    nm, r["pool"], r["dA"], r["dB"], eA, eB, margin))
                if margin < 0:
                    H = list(r["H"]) + [["KEEP", xc]]
                    try:
                        LG.check(n, T0, H)
                        A, B = to_ptr(T0), to_ptr(T0)
                        SA = EB = 0
                        for mode, x in H:
                            A, invs = splay_A(A, x)
                            eA2 = len(invs)
                            eB2 = 0
                            if mode == "KEEP":
                                B, pushes = splay_B_push(B, x)
                                eB2 = len(pushes)
                            SA += eA2
                            EB += eB2 if mode == "KEEP" else 0
                        phi = 3 * SA - EB
                    except Exception as ex:
                        rec["validate"] = "invalid:%r" % (ex,)
                        continue
                    rec["validate"] = {"phi": phi}
                    if phi < 0:
                        out["kills"].append({"shape": nm, "H": H,
                                            "phi": phi})
                        step("PH-KILL", "NEGATIVE PHI %s" % nm)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "phase.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("PH-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
