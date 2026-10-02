"""WP-6 TIGHTWIN: tight-prefix anatomy + coupling shape census (C157).

Tight-window coupling needs: tight Phi(t) forces subsequent-small bursts
(decoupling-budget). Measure directly: (Phi(t), max e_B in next 5 accesses)
correlation (does tightness predict small bursts?); (Phi(t), tree depth
A-max/B-max/avg at t) correlation (does tightness mean shallow trees?).
Phi = 3*SA - EB cumulative (StepEv costs). Families: walks + pushers.
Artifact: tightwin.json. Sealed files untouched.
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_tightest import vine, Rng
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from solver import encode as E


def step(sid, msg):
    print("[WP-6][TIGHTWIN %s] %s" % (sid, msg), flush=True)


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


def run_hist(n, T0, H):
    pre = E.precompute(n, T0, H)
    A, B = to_ptr(T0), to_ptr(T0)
    rows = []
    for idx, acc in enumerate(pre):
        da = depths_of(A)
        db = depths_of(B)
        A, invs = splay_A(A, acc["x"])
        eA = len(invs)
        if acc["mode"] == "KEEP":
            B, pushes = splay_B_push(B, acc["x"])
            eB = len(pushes)
        else:
            eB = 0
        rows.append({"eA": eA, "eB": eB,
                     "Amax": max(da.values()) if da else 0,
                     "Bmax": max(db.values()) if db else 0})
    return rows


def analyze(n, T0, H):
    rows = run_hist(n, T0, H)
    SA = EB = 0
    out = []
    L = len(rows)
    for t, r in enumerate(rows):
        SA += r["eA"]
        EB += r["eB"] if True else 0
        phi = 3 * SA - EB
        nxt = [rows[j]["eB"] for j in range(t + 1, min(L, t + 6))]
        div = (r["eB"] / max(1, 3 * r["eA"])) if r["eB"] > 0 else 0.0
        out.append({"phi": phi, "Amax": r["Amax"], "Bmax": r["Bmax"],
                    "eBnext": (max(nxt) if nxt else 0), "eB": r["eB"],
                    "div": div, "eA": r["eA"]})
    return out


def gen(s, tag):
    rng = Rng(("tw%d" % s).encode(), tag)
    r = rng(0)
    n = [64, 128, 256][r % 3]
    T0 = vine(n, (r >> 8) % 2 == 0)
    H = []
    L = 40 + (r >> 16) % 30
    xc = 2 + (r >> 24) % (n - 2)
    for i in range(L):
        rr = Rng(("tw%d" % s).encode(), tag + b"h%d" % i)
        q = rr(3000 + i)
        op = (q >> 2) % 10
        if op < 3:
            H.append(["DELETE", xc])
        elif op < 6:
            z = min(n, max(1, xc + [-3, -2, -1, 1, 2, 3][(q >> 9) % 6]))
            H.append(["DELETE", z])
            H.append(["KEEP", z])
        else:
            H.append(["KEEP", xc])
        if (q >> 5) % 4 == 0:
            xc = 1 + (q >> 11) % n
    return n, T0, H


def main() -> int:
    step("TW-00", "tight-prefix anatomy + coupling shape")
    pts = []
    done = 0
    for s in range(150):
        n, T0, H = gen(s, b"tw")
        try:
            res = E.precompute(n, T0, H)
            bad = E.exec_counts(res, "P_all", 6, 2, (2, 2))["violations"]
        except Exception:
            continue
        if bad:
            continue
        done += 1
        for r in analyze(n, T0, H):
            pts.append((r["phi"], r["eBnext"], r["Amax"], r["Bmax"], r["eB"],
                        r["div"], r["eA"]))
        if s % 30 == 29:
            step("TW-P", "s=%d" % s)
    # bucket by phi: tight (<=10), mid, loose; max next-burst + depths
    import statistics
    tight = [p for p in pts if p[0] <= 10]
    loose = [p for p in pts if p[0] > 50]
    # divergence (eB > 3*eA, B-heavy) vs phi-before: min phi among divergent
    divpts = [(p[0], p[5]) for p in pts if p[5] > 1.0]
    divpts.sort()
    ndiv = len(divpts)
    divminphi = divpts[0][0] if divpts else None
    divmaxd = max((d for (_, d) in divpts), default=None)
    # joint: overflow - phi_before per divergent access (coupling tightness)
    # pts: (phi_after, eBnext, Amax, Bmax, eB, div, eA); phi_before = phi - 3eA + eB
    worstfit = None
    ov_lo = []
    ov_hi = []
    for p in pts:
        if p[5] > 1.0:
            ov = p[4] - 3 * p[6]
            pb = p[0] - 3 * p[6] + p[4]
            gap = ov - pb
            if worstfit is None or gap > worstfit:
                worstfit = gap
            (ov_lo if pb <= 20 else ov_hi).append(ov)
    ov_lo.sort()
    ov_hi.sort()
    def summ(v):
        v = sorted(v)
        return {"n": len(v), "med": (v[len(v) // 2] if v else None),
                "max": (v[-1] if v else None)}
    out = {"evals": done, "points": len(pts),
           "tight_next": summ([p[1] for p in tight]),
           "loose_next": summ([p[1] for p in loose]),
           "tight_Bmax": summ([p[3] for p in tight]),
           "loose_Bmax": summ([p[3] for p in loose]),
           "tight_Amax": summ([p[2] for p in tight]),
           "tight_eB": summ([p[4] for p in tight]),
           "ndivergent": ndiv, "div_min_phi": divminphi, "div_max_d": divmaxd,
           "worst_overflow_gap": worstfit,
           "ov_lo_max": (ov_lo[-1] if ov_lo else None),
           "ov_lo_n": len(ov_lo),
           "ov_hi_max": (ov_hi[-1] if ov_hi else None),
           "ov_hi_n": len(ov_hi)}
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "tightwin.json").write_text(
        json.dumps(out, indent=1, sort_keys=True, default=str), encoding="utf-8")
    step("TW-01", json.dumps(out, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
