"""PIVOT-22 n=9 exact decision: on-demand Bellman-Ford (integers, capped)."""
from __future__ import annotations
import sys
import copy
import json
import pickle
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))


def step(sid, msg):
    print("[BF9 %s] %s" % (sid, msg), flush=True)


def main():
    import wp6_overflow as V
    import wp6_cycle_ratio as O
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans9.pkl"), "rb"))
    nS, Atrans, Btrans = D["nS"], D["Atrans"], D["Btrans"]
    n = 9
    # depths (read-only, fast)
    Sh = O.shapes_of(list(range(1, n + 1)))
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    dB = {}
    for ib in range(nS):
        dd = V.depths_of(ptrs[ib])
        for x in range(1, n + 1):
            dB[(ib, x)] = dd.get(x, 0)
    del ptrs
    Vcount = nS * nS
    step("B-0", "V=%d E=%d" % (Vcount, Vcount * 2 * n))
    dist = [0] * Vcount
    CAP = 15
    start_pass = 0
    # resume from checkpoint if present
    import os as _os
    ck = str(ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf9dist.pkl")
    if _os.path.exists(ck):
        try:
            S = pickle.load(open(ck, "rb"))
            dist = S["dist"]
            start_pass = S["passes"]
            step("B-0", "resumed at pass %d" % start_pass)
        except Exception as e:
            step("B-0", "checkpoint unreadable: %s" % e)
    t0 = time.time()
    for i in range(start_pass, Vcount):
        if i >= CAP:
            step("B-1", "pass cap reached without convergence: INCONCLUSIVE")
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf9.json").write_text(json.dumps(
                 {"feasible": None, "passes": i}), encoding="utf-8")
            return 0
        changed = False
        dloc = dist
        for ia in range(nS):
            base = ia * nS
            for ib in range(nS):
                u = base + ib
                du = dloc[u]
                for x in range(1, n + 1):
                    ax = Atrans[(ia, x)]
                    ia2, a = ax[0], ax[1]
                    v = ia2 * nS + ib
                    nd = du + 2 * a
                    if nd < dloc[v]:
                        dloc[v] = nd
                        changed = True
                    ib2 = Btrans[(ib, x)][0]
                    v = ia2 * nS + ib2
                    nd = du + 2 * a - (dB[(ib, x)] >> 1)
                    if nd < dloc[v]:
                        dloc[v] = nd
                        changed = True
            if ia % 1000 == 0:
                pass
        step("B-1", "pass %d done (%.0fs)" % (i + 1, time.time() - t0))
        if (i + 1) % 2 == 0:
            pickle.dump({"dist": dist, "passes": i + 1},
                        open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                                 "0909c74a" / "bf9dist.pkl"), "wb"))
        if not changed:
            step("B-2", "FEASIBLE after %d passes" % (i + 1))
            (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
             "bf9.json").write_text(json.dumps(
                 {"feasible": True, "passes": i + 1, "V": Vcount}),
                encoding="utf-8")
            pickle.dump({"dist": dist},
                        open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                                 "0909c74a" / "bf9.pkl"), "wb"))
            return 0
    step("B-2", "NEGATIVE CYCLE (positive-W exists)")
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "bf9.json").write_text(json.dumps({"feasible": False}),
                            encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
