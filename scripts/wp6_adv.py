"""WP-6 ADV: adversarial diverged-burst assault (C165, mission §6/§11).

Greedy builders targeting the structures the dossier isolates:
  S1 FREERIDE: shallow x in A for free (bystander ride-ups, min banking)
      while keeping x deep in B, then burst x. Objective per step:
      maximize (dA-drop) - (dB-drop) - banking/8.
  S2 STARVE: bank B0 via deep DELETEs, then supply-free-deepening chains
      (DELETE-setup + KEEP-splash on fresh keys) to grind pool while
      deepening x, then burst. Objective: minimize pool (Phi).
  S3 KEEPONLY: all-KEEP histories (twin-symmetry predicts: never diverge,
      Phi nondecreasing). Objective: minimize Phi (expect floor 0 Stall).
  S4 SHAPE: greedy max-drain on non-vine T0 (balanced, comb, zigzag).
Margin<0 at any access <=> Phi<0 after <=> GC-STATIC REFUTED (counting
form); any such witness is re-validated via LG.check + independent
recompute before classification. Artifacts: adv.json. Sealed untouched.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_tightest import Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import legality as LG


def step(sid, msg):
    print("[WP-6][ADV %s] %s" % (sid, msg), flush=True)


def depths_of(T):
    dd = {}
    stack = [(T, 0)]
    while stack:
        nd, d = stack.pop()
        if nd is None:
            continue
        dd[nd["k"]] = d
        stack.append((nd["l"], d + 1))
        stack.append((nd["r"], d + 1))
    return dd


def balanced(ks):
    if not ks:
        return None
    m = len(ks) // 2
    return [ks[m], balanced(ks[:m]), balanced(ks[m + 1:])]


def comb(n):
    # deep pocket: chain on the right with left leaves
    t = None
    for k in range(n, 0, -1):
        t = [k, None, t] if k % 3 else [k, [k - 1, None, None] if k > 1 else None, t]
    return t


def zigzag(n):
    t = None
    for k in range(n, 0, -1):
        t = [k, t, None] if k % 2 else [k, None, t]
    return t


def vine(n, left=False):
    t = None
    for k in (range(n, 0, -1) if not left else range(1, n + 1)):
        t = [k, None, t] if not left else [k, t, None]
    return t


def sim_access(A, B, SA, EB, mode, x):
    """One access on COPIES; returns (A2,B2,eA,eB,phi_after,margin)."""
    A2 = copy.deepcopy(A)
    B2 = copy.deepcopy(B)
    A2, invs = splay_A(A2, x)
    eA = len(invs)
    if mode == "KEEP":
        B2, pushes = splay_B_push(B2, x)
        eB = len(pushes)
    else:
        eB = 0
    SA2 = SA + eA
    EB2 = EB + (eB if mode == "KEEP" else 0)
    phi = 3 * SA2 - EB2
    buf = 3 * SA - EB
    return A2, B2, SA2, EB2, eA, eB, phi, buf - (eB - 3 * eA)


def greedy(n, T0, L, obj, keys=None, seed_tag=b"ad"):
    """Greedy history builder. obj in {freeride-x, starve, drain, phimin}.
    Returns dict with min margin/phi + trace."""
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    H = []
    minmargin = None
    minphi = 0
    worst = None
    xc = n // 2
    keys = keys or list(range(1, n + 1))
    for i in range(L):
        dA = depths_of(A)
        dB = depths_of(B)
        best = None
        bestscore = None
        for x in keys:
            for mode in ("KEEP", "DELETE"):
                try:
                    A2, B2, SA2, EB2, eA, eB, phi, margin = sim_access(
                        A, B, SA, EB, mode, x)
                except Exception:
                    continue
                if obj == "drain":
                    score = (eB - 3 * eA, -phi)
                elif obj == "phimin":
                    score = (phi, eB - 3 * eA)
                elif obj == "freeride":
                    da0 = dA.get(xc, 0)
                    db0 = dB.get(xc, 0)
                    dA2 = depths_of(A2).get(xc, 0)
                    dB2 = depths_of(B2).get(xc, 0)
                    score = (-(da0 - dA2) + (db0 - dB2)
                             + (eA * 3) / 8.0, -phi)
                elif obj == "starve":
                    score = (phi, eB - 3 * eA)
                else:
                    raise ValueError(obj)
                if bestscore is None or score < bestscore:
                    bestscore = score
                    best = (mode, x, A2, B2, SA2, EB2, eA, eB, phi,
                            margin)
        if best is None:
            break
        mode, x, A, B, SA, EB, eA, eB, phi, margin = best
        H.append([mode, x])
        if minmargin is None or margin < minmargin:
            minmargin = margin
            worst = {"i": i, "mode": mode, "x": x, "eA": eA, "eB": eB,
                     "phi": phi, "margin": margin}
        if phi < minphi:
            minphi = phi
        if mode == "KEEP":
            xc = x
    return {"minmargin": minmargin, "minphi": minphi, "worst": worst,
            "H": H, "n": n, "L": len(H)}


def validate(n, T0, H):
    """Independent recompute + legality. Returns (phi_min, margin_min)."""
    LG.check(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    SA = EB = 0
    minphi = 0
    minmargin = None
    for mode, x in H:
        buf = 3 * SA - EB
        A, invs = splay_A(A, x)
        eA = len(invs)
        if mode == "KEEP":
            B, pushes = splay_B_push(B, x)
            eB = len(pushes)
        else:
            eB = 0
        SA += eA
        EB += eB if mode == "KEEP" else 0
        phi = 3 * SA - EB
        if phi < minphi:
            minphi = phi
        m = buf - (eB - 3 * eA)
        if minmargin is None or m < minmargin:
            minmargin = m
    return minphi, minmargin


def main() -> int:
    step("AV-00", "adversarial diverged assault")
    out = {"runs": [], "kills": []}
    cfgs = []
    for n in (32, 64):
        for nm, T0 in (("vine", vine(n)), ("vineL", vine(n, True)),
                       ("bal", balanced(list(range(1, n + 1)))),
                       ("comb", comb(n)), ("zigzag", zigzag(n))):
            cfgs.append((nm, n, T0))
    for nm, n, T0 in cfgs:
        for obj, L in (("drain", 60), ("phimin", 60), ("starve", 100),
                       ("freeride", 80)):
            try:
                r = greedy(n, T0, L, obj)
            except Exception as ex:
                step("AV-ERR", "%s %s: %r" % (nm, obj, ex))
                continue
            rec = {"shape": nm, "n": n, "obj": obj, "L": r["L"],
                   "minmargin": r["minmargin"], "minphi": r["minphi"],
                   "worst": r["worst"]}
            out["runs"].append(rec)
            step("AV-R", "%s n=%d %s L=%d margin=%s phi=%s" % (
                nm, n, obj, r["L"], r["minmargin"], r["minphi"]))
            if (r["minmargin"] is not None and r["minmargin"] < 0) or \
               r["minphi"] < 0:
                # candidate kill: validate
                try:
                    vp, vm = validate(n, T0, r["H"])
                except Exception as ex:
                    rec["validate"] = "invalid:%r" % (ex,)
                    continue
                rec["validate"] = {"phi": vp, "margin": vm}
                if vp < 0 or (vm is not None and vm < 0):
                    out["kills"].append({"shape": nm, "n": n, "obj": obj,
                                         "H": r["H"], "phi": vp,
                                         "margin": vm})
                    step("AV-KILL", "MARGIN/PHI NEGATIVE shape=%s obj=%s" % (
                        nm, obj))
    # all-KEEP twin run (S3): expect no divergence, floor 0
    for nm, n, T0 in cfgs[:6]:
        A, B = to_ptr(T0), to_ptr(T0)
        SA = EB = 0
        div_n = 0
        for i in range(60):
            x = 1 + (i * 7) % n
            A, invs = splay_A(A, x)
            B, pushes = splay_B_push(B, x)
            SA += len(invs)
            EB += len(pushes)
            if abs(depths_of(A).get(x, 0) - depths_of(B).get(x, 0)) > 2:
                div_n += 1
        out["runs"].append({"shape": nm, "n": n, "obj": "keeponly",
                            "div_n": div_n,
                            "phi": 3 * SA - EB})
        step("AV-R", "%s keeponly div=%d phi=%d" % (nm, div_n, 3 * SA - EB))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "adv.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("AV-01", "kills=%d runs=%d" % (len(out["kills"]), len(out["runs"])))
    return 2 if out["kills"] else 0


if __name__ == "__main__":
    sys.exit(main())
