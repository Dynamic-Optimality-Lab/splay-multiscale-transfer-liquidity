"""PIVOT-25R-V §7: collision ladder S0-S3 for structural prediction of V.

S0: multiset/ordered D-profile. S1: +argmax locations/order of positive D.
S2: +Lambda_B rows for positive-D keys. S3: +A ancestor/path incidence.
For each failed summary: smallest state pair, same summary, different V.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list
from wp6_lambda import R_coeffs


def step(sid, msg):
    print("[VCL %s] %s" % (sid, msg), flush=True)


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    VD = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" / "vfull5.json").read_text())
    Vf = VD["V"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    dd = [V.depths_of(p) for p in ptrs]

    def feat(ia, ib, lv):
        A, B = Sh[ia], Sh[ib]
        da = depths_list(A)
        t = 1 if A[0] == B[0] else 0
        D = [R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
             for y in range(1, n + 1)]
        d = [tuple(sorted(D)), tuple(D)]
        if lv >= 1:
            pos = tuple(y for y in range(1, n + 1) if D[y - 1] > 0)
            d += (pos,)
        if lv >= 2:
            rows = []
            for y in range(1, n + 1):
                if D[y - 1] > 0:
                    _, lam = R_coeffs(B, y)
                    rows.append((y, tuple(sorted(lam.items()))))
            d += (tuple(rows),)
        if lv >= 3:
            # A ancestor incidence for positive-D keys: (key, A-path nodes)
            Ap = V.to_ptr(copy.deepcopy(A))

            def apath(y):
                p = []
                cur = Ap
                while cur["p"] is not None:
                    cur = cur["p"]
                while True:
                    p.append(cur["k"])
                    if cur["k"] == y:
                        break
                    cur = cur["l"] if y < cur["k"] else cur["r"]
                return tuple(p)
            d += (tuple((y, apath(y)) for y in range(1, n + 1)
                        if D[y - 1] > 0),)
        return tuple(d)

    for lv in range(4):
        groups = defaultdict(list)
        for ia in range(nS):
            for ib in range(nS):
                u = ia * nS + ib
                groups[feat(ia, ib, lv)].append((u, Vf[u]))
        amb = {k: v for k, v in groups.items() if len(set(vv for _, vv in
                                                          v)) > 1}
        step("S%d" % lv, "classes=%d amb=%d" % (len(groups), len(amb)))
        if amb:
            k0 = min(amb, key=lambda k: len(amb[k]))
            step("S%d" % lv, "smallest amb (%d states): %s" %
                 (len(amb[k0]), amb[k0][:4]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
