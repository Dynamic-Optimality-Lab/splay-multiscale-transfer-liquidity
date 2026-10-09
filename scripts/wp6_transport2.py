"""PIVOT-25R-COMP §3-5: all-key deficit-profile transport census.

For every KEEP transition s--x-->s': D_s(y), D_s'(y) for ALL y.
Tests K_+/K_sum/K_max drops vs D_s(x); majorization prefixes;
deficit-transport ledger (disappear/appear/grow/shrink coords).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list


def step(sid, msg):
    print("[TPC %s] %s" % (sid, msg), flush=True)


def D_profile(A, B, n):
    da = depths_list(A)
    t = 1 if A[0] == B[0] else 0
    return [R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
            for y in range(1, n + 1)]


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    K = {"plus": [0, 0], "sum": [0, 0], "max": [0, 0]}
    Kg = {"plus": [0, 0], "sum": [0, 0], "max": [0, 0]}
    worst = {"plus": None, "sum": None, "max": None}
    worstn = {"plus": None, "sum": None, "max": None}
    maj_viol = 0
    maj_tot = 0
    led = Counter()
    nd = 0
    nacc = 0
    for ia in range(nS):
        for ib in range(nS):
            for x in range(1, n + 1):
                Ds = D_profile(Sh[ia], Sh[ib], n)
                # post-trees via single replay (shapes only, for D')
                rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
                Dp = D_profile(rep["endA"], rep["endB"], n)
                d = Ds[x - 1]
                nacc += 1
                # uniform test on ALL edges + positivity-gated split stats.
                kp = sum(max(v, 0) for v in Ds)
                kp2 = sum(max(v, 0) for v in Dp)
                ks = sum(Ds)
                ks2 = sum(Dp)
                km = max(Ds)
                km2 = max(Dp)
                for name, a, b in (("plus", kp, kp2), ("sum", ks, ks2),
                                   ("max", km, km2)):
                    ok = (a - b) >= d
                    K[name][0 if ok else 1] += 1
                    if d > 0:
                        Kg[name][0 if ok else 1] += 1
                        if not ok and (worst[name] is None or
                                       (a - b) < worst[name][0]):
                            worst[name] = (a - b, d, ia, ib, x)
                    elif not ok and (worstn[name] is None or
                                     (a - b) - d < worstn[name][0]):
                        worstn[name] = ((a - b) - d, d, ia, ib, x)
                if d > 0:
                    nd += 1
                    # majorization: sorted-desc positive prefixes
                    s1 = sorted([v for v in Ds if v > 0], reverse=True)
                    s2 = sorted([v for v in Dp if v > 0], reverse=True)
                    m = 0
                    for k in range(1, max(len(s1), len(s2)) + 1):
                        p1 = sum(s1[:k])
                        p2 = sum(s2[:k])
                        if p1 - p2 < d:
                            m += 1
                            break
                    maj_tot += 1
                    maj_viol += 1 if m else 0
                    # ledger: coordinate fates (positive coords)
                    pre = {y for y in range(n) if Ds[y] > 0}
                    post = {y for y in range(n) if Dp[y] > 0}
                    for y in pre - post:
                        led["disappear"] += 1
                    for y in post - pre:
                        led["appear"] += 1
                    for y in pre & post:
                        if Dp[y] > Ds[y]:
                            led["grow"] += 1
                        elif Dp[y] < Ds[y]:
                            led["shrink"] += 1
                        else:
                            led["same"] += 1
        step("G", "ia=%d/%d accesses=%d dpos=%d" % (ia + 1, nS, nacc, nd))
    step("R", "Kplus pass/fail=%s (dpos=%s) Ksum=%s Kmax=%s" %
         (K["plus"], Kg["plus"], K["sum"], K["max"]))
    step("R", "worst dpos: %s" %
         {k: (v[:2] if v else None) for k, v in worst.items()})
    step("R", "worst excess-rise dneg: %s" %
         {k: (v[:2] if v else None) for k, v in worstn.items()})
    step("R", "majorization violations=%d/%d ledger=%s" %
         (maj_viol, maj_tot, dict(led)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("transport%d.json" % n)).write_text(
        json.dumps({"K": K, "Kg": Kg, "worst": worst, "worstn": worstn,
                    "maj": [maj_viol, maj_tot],
                    "ledger": dict(led), "nacc": nacc, "npos": nd},
                   indent=1, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
