"""WP-6 BEAM: choreographed kill-attempt for the diverged step (C168).

Target shape (derived): pool ground to exactly 0 while target key xc sits
A-shallow (dA in 1..2) and B-deep (dB >= 7), then KEEP-xc burst has
overflow eB-3e_A >= 4-3 = 1 > 0 = pool => MARGIN NEGATIVE => GC-STATIC
REFUTED (counting form). Reaching it needs sustained asymmetric bystanding
(B-catch/A-miss pushes) + exact pool-zeroing, i.e. multi-step positioning
beyond myopic greedy: beam search (width/depth) with joint objective
(min pool AND max divergence gap), then forced burst on xc.
Any margin<0 is re-validated via LG.check + independent recompute before
classification (REFUTATION protocol, mission §18). Artifact: beam.json.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_adv import vine, balanced, depths_of, validate
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import legality as LG


def step(sid, msg):
    print("[WP-6][BEAM %s] %s" % (sid, msg), flush=True)


def burst_margin(A, B, SA, EB, xc):
    """Forced KEEP-xc burst margin from state (A,B,SA,EB)."""
    A2 = copy.deepcopy(A)
    B2 = copy.deepcopy(B)
    A2, invs = splay_A(A2, xc)
    eA = len(invs)
    B2, pushes = splay_B_push(B2, xc)
    eB = len(pushes)
    buf = 3 * SA - EB
    return buf - (eB - 3 * eA), eA, eB


def beam_run(n, T0, xc, L, W, seed):
    A0, B0 = to_ptr(T0), to_ptr(T0)
    # beam: list of (score, A, B, SA, EB, H)
    beam = [(0.0, A0, B0, 0, 0, [])]
    best = {"margin": None, "H": None, "eA": None, "eB": None}
    for i in range(L):
        cands = []
        for _, A, B, SA, EB, H in beam:
            dA = depths_of(A).get(xc, 0)
            dB = depths_of(B).get(xc, 0)
            gap = dB - 3 * dA
            pool = 3 * SA - EB
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
                    SA2 = SA + eA
                    EB2 = EB + (eB if mode == "KEEP" else 0)
                    dA2 = depths_of(A2).get(xc, 0)
                    dB2 = depths_of(B2).get(xc, 0)
                    gap2 = dB2 - 3 * dA2
                    pool2 = 3 * SA2 - EB2
                    if pool2 < 0:
                        continue  # uncovered path: prune (covered only)
                    score = pool2 - 2.0 * max(0, gap2)
                    cands.append((score, A2, B2, SA2, EB2, H + [[mode, x]]))
        if not cands:
            break
        cands.sort(key=lambda c: c[0])
        # diversity: keep best by score + a few random far
        beam = cands[:W]
        # probe forced burst from beam heads
        for _, A, B, SA, EB, H in beam[:8]:
            m, eA, eB = burst_margin(A, B, SA, EB, xc)
            if best["margin"] is None or m < best["margin"]:
                best = {"margin": m, "H": list(H), "eA": eA, "eB": eB,
                        "i": i}
                if m < 0:
                    return best, True
    return best, False


def main() -> int:
    step("BM-00", "choreographed diverged kill-attempt")
    out = {"runs": [], "kills": []}
    cfgs = []
    for n in (16, 32):
        cfgs.append((n, vine(n), n // 2))
        cfgs.append((n, balanced(list(range(1, n + 1))), n // 2))
    for n, T0, xc in cfgs:
        for (L, W) in ((30, 48), (45, 32)):
            best, kill = beam_run(n, T0, xc, L, W, 0)
            rec = {"n": n, "xc": xc, "L": L, "W": W,
                   "margin": best["margin"], "eA": best["eA"],
                   "eB": best["eB"], "i": best["i"]}
            out["runs"].append(rec)
            step("BM-R", "n=%d xc=%d L=%d W=%d margin=%s (eA=%s eB=%s)" % (
                n, xc, L, W, best["margin"], best["eA"], best["eB"]))
            if kill and best["H"] is not None:
                H = best["H"] + [["KEEP", xc]]
                try:
                    LG.check(n, T0, H)
                    A, B = to_ptr(T0), to_ptr(T0)
                    SA = EB = 0
                    for mode, x in H:
                        A, invs = splay_A(A, x)
                        eA = len(invs)
                        eB = 0
                        if mode == "KEEP":
                            B, pushes = splay_B_push(B, x)
                            eB = len(pushes)
                        SA += eA
                        EB += eB if mode == "KEEP" else 0
                    phi = 3 * SA - EB
                except Exception as ex:
                    rec["validate"] = "invalid:%r" % (ex,)
                    continue
                rec["validate"] = {"phi": phi}
                if phi < 0:
                    out["kills"].append({"n": n, "H": H, "phi": phi})
                    step("BM-KILL", "NEGATIVE PHI n=%d" % n)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "beam.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("BM-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
