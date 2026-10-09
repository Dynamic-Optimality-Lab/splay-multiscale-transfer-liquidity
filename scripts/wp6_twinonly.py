"""Twin-only candidate check at n=8,9: Phi=-2*[roots equal].
Records violation classes (a,q,w,Delta)."""
from __future__ import annotations
import sys
import copy
import json
import pickle
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
import wp6_cycle_ratio as O


def step(sid, msg):
    print("[TWIN %s] %s" % (sid, msg), flush=True)


def main():
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 8
    G = O.build(n)
    nS, Sh = G["nS"], G["Sh"]
    D = pickle.load(open(str(ROOT / "artifacts" / "v04" / "wp6_present" /
                             "0909c74a" / ("trans%d.pkl" % n)), "rb"))
    At, Bt = D["Atrans"], D["Btrans"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    rt = {}
    ddall = {}
    for ia in range(nS):
        r = ptrs[ia]
        while r["p"] is not None:
            r = r["p"]
        rt[ia] = r["k"]
        ddall[ia] = V.depths_of(ptrs[ia])

    def Phi(ia, ib):
        return -2 * (1 if rt[ia] == rt[ib] else 0)

    bad = 0
    chk = 0
    vc = Counter()
    for ia in range(nS):
        for ib in range(nS):
            pu = Phi(ia, ib)
            for x in range(1, n + 1):
                ia2, a = At[(ia, x)]
                if -2 * a > pu - Phi(ia2, ib):
                    bad += 1
                chk += 1
                ib2, _ = Bt[(ib, x)]
                w = ddall[ib].get(x, 0) // 2 - 2 * a
                if w > pu - Phi(ia2, ib2):
                    bad += 1
                    vc[(a, ddall[ib].get(x, 0) // 2, w,
                        pu - Phi(ia2, ib2))] += 1
                chk += 1
        if (ia + 1) % 200 == 0:
            step("T-%d" % n, "%d/%d bad=%d" % (ia + 1, nS, bad))
    step("T-%d" % n, "n=%d checked=%d bad=%d classes=%s" %
         (n, chk, bad, dict(sorted(vc.items()))))
    return 0


if __name__ == "__main__":
    sys.exit(main())
