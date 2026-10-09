"""PIVOT-23 tight-edge anatomy: slack distribution, tight graph SCCs,
zero-cycle structure, KEEP/DELETE + depth splits."""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path
from collections import Counter, deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V


def step(sid, msg):
    print("[TIGHT %s] %s" % (sid, msg), flush=True)


def main():
    import wp6_cycle_ratio as O
    n = 7
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "trans7.pkl"), "rb"))
    nS, Atrans, Btrans, Sh = D["nS"], D["Atrans"], D["Btrans"], D["Sh"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    dA, dB = {}, {}
    for ia in range(nS):
        dd = V.depths_of(ptrs[ia])
        for x in range(1, n + 1):
            dA[(ia, x)] = dd.get(x, 0)
            dB[(ia, x)] = dd.get(x, 0)
    P = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / "bf7.pkl"), "rb"))["dist"]
    Vcount = nS * nS
    slack_hist = Counter()
    tight_by = Counter()
    # tight adjacency for SCC (store as lists of ints per node? memory:
    # tight edges likely many; use iterative Tarjan on the fly is complex.
    # Instead: count tight + record per-node tight-out-degree histogram.)
    tout_hist = Counter()
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            pu = P[u]
            ntight = 0
            for x in range(1, n + 1):
                ia2, a = Atrans[(ia, x)]
                v = ia2 * nS + ib
                w = -2 * a
                lam = (pu - P[v]) - w
                assert lam >= 0, (u, x, "D", lam)
                slack_hist[("D", lam)] += 1
                if lam == 0:
                    ntight += 1
                    tight_by[("D", a)] += 1
                ib2, _ = Btrans[(ib, x)]
                v = ia2 * nS + ib2
                w = dB[(ib, x)] // 2 - 2 * a
                lam = (pu - P[v]) - w
                assert lam >= 0, (u, x, "K", lam)
                slack_hist[("K", lam)] += 1
                if lam == 0:
                    ntight += 1
                    tight_by[("K", a, dB[(ib, x)] // 2)] += 1
            tout_hist[ntight] += 1
        if (ia + 1) % 60 == 0:
            step("T-1", "%d/%d" % (ia + 1, nS))
    step("T-2", "slack hist (mode,lambda): %s" %
         dict(sorted(slack_hist.items())))
    step("T-2", "tight-out-degree hist: %s" % dict(sorted(tout_hist.items())))
    tk = sum(v for (m, *_), v in tight_by.items() if True)
    step("T-2", "total tight edges=%d / %d (%.2f%%)" %
         (tk, Vcount * 2 * n, 100.0 * tk / (Vcount * 2 * n)))
    # top tight types
    top = sorted(tight_by.items(), key=lambda z: -z[1])[:15]
    step("T-2", "top tight (type,count): %s" % top)
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / "tight7.json").write_text(json.dumps(
         {"slack": {str(k): v for k, v in slack_hist.items()},
          "tout": dict(tout_hist),
          "top_tight": [(str(k), v) for k, v in top]},
         indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
