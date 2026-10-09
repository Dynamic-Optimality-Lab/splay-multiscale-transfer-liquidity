"""PIVOT-25R-SOLVE §4/§7: verify backward coefficient maps end-to-end.

Terminal (no-zig): (aL,aR,f,c)=(0,0,[],0). Fold T_sigma over the double
suffix in REVERSE (last double first); evaluate R_entry on X_0 fringes;
compare vs q - sum(DbDrop). Zig family: terminal zig form directly.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_hnrec import run_access
from wp6_transport import dbdrop_formula


def step(sid, msg):
    print("[MSL %s] %s" % (sid, msg), flush=True)


def Tmap(pat, st):
    aL, aR, f, c = st
    f = list(f)
    if pat == "LL":
        return (aL - 2, aR - 1, [1 + aR, 2 + aR] + f, c + 1 + 2 * aR)
    if pat == "RR":
        return (aL - 1, aR - 2, [1 + aL, 2 + aL] + f, c + 1 + 2 * aL)
    if pat == "LR":
        return (aL - 1, aR - 1, [aL, 1 + aR] + f, c + aL + aR)
    if pat == "RL":
        return (aL - 1, aR - 1, [aR, 1 + aL] + f, c + aL + aR)
    raise AssertionError(pat)


def fringe_masses(X):
    return [f[1] for f in X["fr"]]


def main():
    import wp6_cycle_ratio as O
    Sh9 = O.shapes_of(list(range(1, 10)))
    Sh8 = O.shapes_of(list(range(1, 9)))
    cases = [("L4c", Sh8[255], Sh8[2], 8), ("PR904", Sh9[3432], Sh9[0], 9)]
    # V1-9 vine: A rooted 1, B left-vine n=9
    def vr(keys):
        t = None
        for k in reversed(list(keys)):
            t = [k, None, t]
        return t

    def vl(keys):
        t = None
        for k in list(keys):
            t = [k, t, None]
        return t
    cases.append(("V19", [1, None, vr(range(2, 10))], vl(range(1, 10)), 1))
    HN = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     "highneed_bank.json").read_text())
    for tag in ("R10-29", "R11-9"):
        r = next(q for q in HN if q["tag"] == tag)
        cases.append((tag, r["A"], r["B"], r["x"]))
    for (tag, A0, B0, x) in cases:
        seq = run_access(A0, B0, x)
        # forward: q - sum DbDrop
        Andreas = [(X["pat"], X["L"], X["R"], X["U"], X["V"]) for
                   (X, s, Xp, t1) in seq]
        import wp6_jointlp as _J  # noqa (ensures module present)
        fwd = [(p, dbdrop_formula(p, L, R, U, Vv)) for (p, L, R, U, Vv) in
               Andreas]
        q = len(seq)
        R_fwd = q - sum(v for _, v in fwd)
        # backward fold from terminal zero
        st = (0, 0, [], 0)
        for (X, s, Xp, t1) in reversed(seq):
            st = Tmap(X["pat"], st)
        aL, aR, f, c = st
        X0 = seq[0][0]
        m = fringe_masses(X0)
        R_bwd = c + aL * X0["L"] + aR * X0["R"]
        for j, fj in enumerate(f):
            R_bwd += fj * (m[j] if j < len(m) else 0)
        step("C", "%s q=%d R_fwd=%d R_bwd=%d %s" %
             (tag, q, R_fwd, R_bwd,
              "MATCH" if R_fwd == R_bwd else "*** MISMATCH ***"))
    # zig-outer family: terminal zig form R = -xL + m_0
    for n in (9, 16):
        B = [2, [1, None, None], vr(range(3, n + 1))]
        A = [1, None, vr(range(2, n + 1))]
        x = 1
        # pre-zig state IS the initial state (dB=1, single zig, no doubles)
        R_form = -0 + (n - 2)  # -xL + m_0, x leaf, root.other = n-2 keys
        pB = V.to_ptr(copy.deepcopy(B))
        dd = V.depths_of(pB)
        assert dd[1] == 1
        rep = V.replay(A, B, [("K", x)])
        acc = rep["accesses"][0]
        qB = V.to_ptr(copy.deepcopy(rep["endB"]))
        RB = sum(V.depths_of(pB).values()) - sum(V.depths_of(qB).values())
        step("C", "zig n=%d R_form=%d actual(-DbDrop)=%d w=%d r=%d %s" %
             (n, R_form, -RB, acc["eps"], acc["eps"] - (2 + RB),
              "MATCH" if R_form == -RB else "*** MISMATCH ***"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
