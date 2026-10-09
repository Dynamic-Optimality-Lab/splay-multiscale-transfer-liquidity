"""WP-6 FREERIDE: free-ride-to-root assault (C172, rate-law direct assault).

The last untested structural question for the diverged rate law: can a
key ride to EXACTLY A-depth 0 purely as a bystander (never accessed, so
zero attributable banking) while staying B-deep? If YES: supply-free
setups exist without banking arrivals (pairing's hidden premise dies) and
a pool-starved burst may kill (REFUTATION path opens). If NO (even under
beam choreography): free-ride-impossibility evidence (pairing kernelizes;
rate law keeps its sole residual).
Beam (width W, depth L) forbidding xc-access, objective min dA(xc) with
dB(xc) held large: score = dA(xc) - 2*dB(xc). Then forced KEEP-xc burst
(e_A = 0 iff dA = 0) with margin check; margin<0 re-validated via
LG.check + independent recompute (REFUTATION protocol).
Artifact: freeride.json. Sealed files untouched.
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
    print("[WP-6][FREERIDE %s] %s" % (sid, msg), flush=True)


def beam_run(n, T0, xc, L, W, dmin):
    A0, B0 = to_ptr(T0), to_ptr(T0)
    beam = [(0.0, A0, B0, 0, 0, [])]
    best = {"dA": None, "dB": None, "H": None}
    for _ in range(L):
        cands = []
        for _, A, B, SA, EB, H in beam:
            for x in range(1, n + 1):
                if x == xc:
                    continue  # xc never accessed: free-ride only
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
                        continue  # keep pool nonnegative (covered paths)
                    dA2 = depths_of(A2).get(xc, 0)
                    dB2 = depths_of(B2).get(xc, 0)
                    score = dA2 - 2.0 * min(dB2, dmin + 4)
                    cands.append((score, A2, B2, SA2, EB2, H + [[mode, x]]))
        if not cands:
            break
        cands.sort(key=lambda c: c[0])
        beam = cands[:W]
        for _, A, B, SA, EB, H in beam[:6]:
            dA = depths_of(A).get(xc, 0)
            dB = depths_of(B).get(xc, 0)
            if best["dA"] is None or (dA, -dB) < (best["dA"], -best["dB"]):
                best = {"dA": dA, "dB": dB, "H": list(H),
                        "pool": 3 * SA - EB}
    return best


def main() -> int:
    step("FR-00", "free-ride-to-root assault")
    out = {"runs": [], "kills": []}
    for n in (16, 32):
        for nm, T0 in (("vine%d" % n, vine(n)),
                       ("bal%d" % n, balanced(list(range(1, n + 1))))):
            xc = n // 2
            for (L, W, dmin) in ((50, 48, 8), (70, 32, 10)):
                try:
                    b = beam_run(n, T0, xc, L, W, dmin)
                except Exception as ex:
                    step("FR-ERR", "%s: %r" % (nm, ex))
                    continue
                rec = {"shape": nm, "xc": xc, "L": L, "W": W,
                       "dA": b["dA"], "dB": b["dB"], "pool": b.get("pool")}
                out["runs"].append(rec)
                step("FR-R", "%s xc=%d dA=%s dB=%s pool=%s" % (
                    nm, xc, b["dA"], b["dB"], b.get("pool")))
                # free-ride success: dA==0, dB>=dmin, xc unaccessed
                if b["dA"] == 0 and b["dB"] is not None and \
                   b["dB"] >= dmin and b["H"] is not None:
                    H = list(b["H"]) + [["KEEP", xc]]
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
                    rec["burst"] = {"phi": phi}
                    if phi < 0:
                        out["kills"].append({"shape": nm, "H": H,
                                            "phi": phi})
                        step("FR-KILL", "NEGATIVE PHI %s" % nm)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "freeride.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("FR-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
