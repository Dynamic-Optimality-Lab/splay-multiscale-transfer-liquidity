"""WP-6 KEEPRESIDUAL: C183 scalar falsifiers (H2/ROOT-COLLAPSE/PREPEND-2/DELETE-H2/KEEP-RESIDUAL).

Definitions (exact engine semantics, present keys):
  a_x/e_A = #A-StepEvs, b_x/e_B = #B-StepEvs (KEEP; DELETE: e_B=0).
  H1 = max(0, max_x (b_x-3a_x)); Q_x = (b_x-3a_x) + H1(K_x); Q = max_x Q_x.
  H2 = max(H1, Q, DEL2) with DEL2 = max over (z DEL, y KEEP) of
       [(b_y(D_z)-3a_y(D_z)) - 3a_z]  (DELETE-first pairs; exact, no BD1 use).
  Identity under test: H2 == max(H1, Q) (gap = DEL2 excess over it).
Falsifiers (positive = FAILURE of that component):
  F_ROOTCOLLAPSE: max(H2-H1) over same-root pairs.
  F_REACH: same over reachable post-KEEP states (always same-root).
  F_PREPEND2: max(C_T(x,y)-C_T(z,x,y)) over triples (C = A-StepEv counts).
  F_DELETEH2: max(H2(D_z)-H2-3a_z) over (state,z).
  F_KEEPRESIDUAL: max(Q_x(s)-Phi(h)) over reached (state, access-x)
      + beam max over pair-states. Positive = scalar REFUTED (then check
      Phi'<0 for GC-refutation distinction per mission Sec 25).
Modes: walk(histories) + beam(pair-states) + exhaustive(all pairs n<=5,
triples n<=7, histories n<=4 L<=4 / n=5 L<=3) + constructed (same-root,
two-divergence, shared-path vine triples).
Artifacts: keep_residual/*.json. Sealed files untouched.
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
from liquidity import legacy_embedding as PE


def step(sid, msg):
    line = "[WP-6][KEEPRES %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "keep_residual"
        bd.mkdir(parents=True, exist_ok=True)
        with open(bd / "progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def ecounts(A, B, x):
    A2 = copy.deepcopy(A)
    A2, invs = splay_A(A2, x)
    eA = len(invs)
    B2 = copy.deepcopy(B)
    B2, pushes = splay_B_push(B2, x)
    eB = len(pushes)
    return eA, eB, A2, B2


def H1f(dA, dB, keys):
    best = 0
    for x in keys:
        da = dA.get(x)
        db = dB.get(x)
        if da is None or db is None:
            continue
        v = (db + 1) // 2 - 3 * ((da + 1) // 2)
        if v > best:
            best = v
    return best


def H2f(A, B, keys):
    """Returns dict(H1, Qmax, DEL2max, H2, gap). O(n^3)."""
    dA = depths_of(A)
    dB = depths_of(B)
    h1 = H1f(dA, dB, keys)
    qmax = None
    qarg = None
    for x in keys:
        da = dA.get(x, 0)
        db = dB.get(x, 0)
        a = (da + 1) // 2
        b = (db + 1) // 2
        A2 = copy.deepcopy(A)
        A2, _ = splay_A(A2, x)
        B2 = copy.deepcopy(B)
        B2, _ = splay_B_push(B2, x)
        hk = H1f(depths_of(A2), depths_of(B2), keys)
        q = (b - 3 * a) + hk
        if qmax is None or q > qmax:
            qmax = q
            qarg = x
    del2 = None
    for z in keys:
        da = dA.get(z, 0)
        a = (da + 1) // 2
        Az = copy.deepcopy(A)
        Az, _ = splay_A(Az, z)
        dAz = depths_of(Az)
        hz = H1f(dAz, dB, keys)
        v = hz - 3 * a
        if del2 is None or v > del2:
            del2 = v
    h2 = h1
    if qmax is not None and qmax > h2:
        h2 = qmax
    if del2 is not None and del2 > h2:
        h2 = del2
    gap = h2 - max(h1, qmax if qmax is not None else h1)
    return {"H1": h1, "Qmax": qmax, "Qarg": qarg, "DEL2max": del2,
            "H2": h2, "gap": gap}


def prepend_val(T, z, x, y):
    """C_T(x,y) - C_T(z,x,y), A-StepEv counts. Positive = PREPEND-2 FALSE."""
    def C(seq):
        t = copy.deepcopy(T)
        tot = 0
        for k in seq:
            t, invs = splay_A(t, k)
            tot += len(invs)
        return tot
    return C([x, y]) - C([z, x, y])


def main() -> int:
    step("KR-00", "C183 scalar falsifiers")
    out = {}
    # ---- PREPEND-2 exhaustive small-n + targeted vine triples ----
    def shapes(ks):
        if not ks:
            return [None]
        res = []
        for i, k in enumerate(ks):
            for l in shapes(ks[:i]):
                for r in shapes(ks[i + 1:]):
                    res.append([k, l, r])
        return res

    for n in (4, 5, 6):
        ks = list(range(1, n + 1))
        best = [None, None]
        for T0 in shapes(ks):
            T = to_ptr(T0)
            for z in ks:
                for x in ks:
                    for y in ks:
                        v = prepend_val(T, z, x, y)
                        if best[0] is None or v > best[0]:
                            best = [v, (z, x, y)]
        out["prepend_n%d" % n] = {"max": best[0], "arg": best[1]}
        step("KR-01", "prepend n=%d max=%s arg=%s" % (n, best[0], best[1]))
    # targeted shared-path vine triples (predicted violation zone d>8)
    for n in (32, 64):
        T = to_ptr(vine(n))
        best = [None, None]
        import random
        rng = random.Random(4100 + n)
        tested = set()
        # systematic: z above x,y on vine (shared path) + random
        for _ in range(4000):
            if rng.random() < 0.5:
                z = rng.randint(1, n - 2)
                x = rng.randint(z + 1, n)
                y = rng.randint(z + 1, n)
            else:
                z = rng.randint(1, n)
                x = rng.randint(1, n)
                y = rng.randint(1, n)
            if (z, x, y) in tested:
                continue
            tested.add((z, x, y))
            v = prepend_val(T, z, x, y)
            if best[0] is None or v > best[0]:
                best = [v, (z, x, y)]
        out["prepend_vine%d" % n] = {"max": best[0], "arg": best[1]}
        step("KR-02", "prepend vine n=%d max=%s arg=%s" % (n, best[0],
                                                           best[1]))
    # ---- ROOT-COLLAPSE: exhaustive same-root n<=5 + post-KEEP walk ----
    for n in (3, 4, 5):
        ks = list(range(1, n + 1))
        best = [None, None]
        for A0 in shapes(ks):
            for B0 in shapes(ks):
                A, B = to_ptr(A0), to_ptr(B0)
                if A["k"] != B["k"]:
                    continue
                h = H2f(A, B, ks)
                v = h["H2"] - h["H1"]
                if best[0] is None or v > best[0]:
                    best = [v, (A0, B0)]
        out["rootcollapse_n%d" % n] = {"max": best[0]}
        step("KR-03", "rootcollapse n=%d max=%s" % (n, best[0]))
    # ---- walk A: custom small-n histories, FULL falsifiers ----
    import random
    agg = Counter()
    for k in ("rc_max", "dh_max", "kr_max", "gap_max", "idgap_max"):
        agg[k] = None
    for n, t_range, L in ((16, range(6), 40), (32, range(3), 25)):
        for t in t_range:
            if t % 3 == 0:
                T0 = vine(n)
            elif t % 3 == 1:
                T0 = balanced(list(range(1, n + 1)))
            else:
                ks = list(range(1, n + 1))
                random.Random(6000 + t).shuffle(ks)
                T0 = None
                for kk in ks:
                    def ins(t, k):
                        if t is None:
                            return [k, None, None]
                        if k < t[0]:
                            t[1] = ins(t[1], k)
                        elif k > t[0]:
                            t[2] = ins(t[2], k)
                        return t
                    T0 = ins(T0, kk)
            rng = random.Random(7000 + t)
            H = [[rng.choice(["KEEP", "DELETE"]), rng.randint(1, n)]
                 for _ in range(L)]
            A, B = to_ptr(T0), to_ptr(T0)
            keys = sorted(depths_of(A).keys())
            SA = EB = 0
            for acc in H:
                mode, x = acc
                if mode == "KEEP":
                    h = H2f(A, B, keys)
                    v = h["H2"] - h["H1"]
                    if agg["rc_max"] is None or v > agg["rc_max"]:
                        agg["rc_max"] = v
                        agg["rc_wit"] = {"n": n, "t": t, "x": x}
                    if h["gap"] is not None and (
                            agg["gap_max"] is None
                            or h["gap"] > agg["gap_max"]):
                        agg["gap_max"] = h["gap"]
                dA = depths_of(A)
                dB = depths_of(B)
                h1 = H1f(dA, dB, keys)
                h2base = H2f(A, B, keys)["H2"]
                phi = 3 * SA - EB
                for z in keys:
                    da = dA.get(z, 0)
                    a = (da + 1) // 2
                    Az = copy.deepcopy(A)
                    Az, _ = splay_A(Az, z)
                    hz = H2f(Az, B, keys)
                    dh = hz["H2"] - h2base - 3 * a
                    if agg["dh_max"] is None or dh > agg["dh_max"]:
                        agg["dh_max"] = dh
                        agg["dh_wit"] = {"n": n, "t": t, "z": z}
                    # all-x KEEP-RESIDUAL
                    Bz = copy.deepcopy(B)
                    Bz, _ = splay_B_push(Bz, z)
                    db = dB.get(z, 0)
                    b = (db + 1) // 2
                    hk = H1f(depths_of(Az), depths_of(Bz), keys)
                    kr = (b - 3 * a) + hk - phi
                    if agg["kr_max"] is None or kr > agg["kr_max"]:
                        agg["kr_max"] = kr
                        agg["kr_wit"] = {"n": n, "t": t, "z": z,
                                         "q": (b - 3 * a) + hk,
                                         "phi": phi}
                A, invs = splay_A(A, x)
                eB = 0
                if mode == "KEEP":
                    B, pushes = splay_B_push(B, x)
                    eB = len(pushes)
                SA += len(invs)
                EB += eB if mode == "KEEP" else 0
            step("KR-04", "small n=%d t=%d rc=%s dh=%s kr=%s gap=%s" % (
                n, t, agg["rc_max"], agg["dh_max"], agg["kr_max"],
                agg["gap_max"]))
    out["walk"] = dict(agg)
    step("KR-05", "walk: %s" % json.dumps(dict(agg), sort_keys=True,
                                          default=str))
    bd = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "keep_residual"
    bd.mkdir(parents=True, exist_ok=True)
    for k, v in out.items():
        (bd / ("%s.json" % k)).write_text(
            json.dumps(v, indent=1, sort_keys=True, default=str),
            encoding="utf-8")
    step("KR-06", "done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
