"""PIVOT-25R-DISC §2-3: exhaustive access-profile census.

For EVERY KEEP access (pairs x keys, n=5 exhaustive; n=6 sample/held-out):
per-double (pat, sizes, twinDrop, DbDrop) sequence + zig residual,
prefix surplus profile vs (+1/double, 0/zig) quotas, access totals
(w, twin, R_B, unpaid = w - (2Δt + R_B)).
NO candidate variable imposed; raw feature table for discovery.
"""
from __future__ import annotations
import sys
import copy
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_trcollect import harvest


def step(sid, msg):
    print("[DSC %s] %s" % (sid, msg), flush=True)


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    cap = int(_s.argv[2]) if len(_s.argv) > 2 else 0  # 0 = exhaustive
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = []
    dd = []
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt.append(r["k"])
        dd.append(V.depths_of(ptrs[ia]))
    recs = []
    rng = random.Random(4)
    order = [(ia, ib, x) for ia in range(nS) for ib in range(nS)
             for x in range(1, n + 1)]
    if cap:
        rng.shuffle(order)
        order = order[:cap]
    for (ia, ib, x) in order:
        ev = []
        harvest(Sh[ia], Sh[ib], x, "K", "ex", ev)
        a = (dd[ia][x] + 1) // 2
        q = dd[ib][x] // 2
        w = q - 2 * a
        tw0 = 1 if rt[ia] == rt[ib] else 0
        dbl = [(e["pat"], tuple(0 if b["empty"] else len(b["keys"])
                               for b in e["blocks"]), e["twinDrop"],
                e["DbDrop"]) for e in ev]
        tot = sum(t + d for _, _, t, d in dbl)
        # zig residual via state functions (exact, no intermediates needed)
        rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
        tw1 = 1 if rep["endA"][0] == rep["endB"][0] else 0
        pA = V.to_ptr(copy.deepcopy(rep["endA"]))
        pB = V.to_ptr(copy.deepcopy(rep["endB"]))
        RB = sum(dd[ib].values()) - sum(V.depths_of(pB).values())
        zigpay = (2 * (tw1 - tw0) + RB) - tot
        prof = []
        s = 0
        for (_, _, t, d) in dbl:
            s += (t + d) - 1
            prof.append(s)
        prof.append(s + zigpay)  # zig quota 0
        unpaid = w - (2 * (tw1 - tw0) + RB)
        recs.append({"ia": ia, "ib": ib, "x": x, "a": a, "q": q, "w": w,
                     "tw": [tw0, tw1], "RB": RB, "unpaid": unpaid,
                     "dbl": [[p, list(sz), t, d] for (p, sz, t, d) in dbl],
                     "zigpay": zigpay, "prof": prof,
                     "minpref": min(prof) if prof else 0})
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("profiles%d.json" % n)).write_text(
        json.dumps({"n": n, "nacc": len(recs), "recs": recs}, indent=0,
                   default=str), encoding="utf-8")
    un = [r for r in recs if r["unpaid"] > 0]
    step("S", "n=%d accesses=%d unpaid-accesses=%d (%.3f%%) maxunpaid=%s" %
         (n, len(recs), len(un),
          100.0 * len(un) / max(1, len(recs)),
          max([r["unpaid"] for r in un], default=None)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
