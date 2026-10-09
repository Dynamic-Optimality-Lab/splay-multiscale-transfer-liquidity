"""PIVOT-25R-V §8-9: residual-propagation graph on keys.

For each TIGHT D>0 edge (u--x-->v): pre positive keys, post positive
keys (amounts), twin, Lambda overlap between x-row and y-rows,
interval/order relations, ancestor relations, split/merge counts.
Aggregate: determinism, direction, ancestor-following, Lambda overlap,
endpoint preservation, split/merge. Exact counterexamples per pattern.
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_staticR import R_static, depths_list
from wp6_lambda import R_coeffs


def step(sid, msg):
    print("[VPG %s] %s" % (sid, msg), flush=True)


def main():
    import sys as _s
    import wp6_cycle_ratio as O
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh = O.shapes_of(list(range(1, n + 1)))
    nS = len(Sh)
    VD = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     ("vfull%d.json" % n)).read_text())
    Vf = VD["V"]
    ptrs = [V.to_ptr(copy.deepcopy(s)) for s in Sh]
    dd = [V.depths_of(p) for p in ptrs]

    def Dprof(ia, ib):
        A, B = Sh[ia], Sh[ib]
        da = depths_list(A)
        t = 1 if A[0] == B[0] else 0
        return [R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
                for y in range(1, n + 1)]

    def LamB(ib):
        return {y: R_coeffs(Sh[ib], y) for y in range(1, n + 1)}

    stat = Counter()
    det = defaultdict(set)
    split = Counter()
    toward = Counter()
    anchits = Counter()
    ov = Counter()
    posts = 0
    import json as J
    idx = {J.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            Dpre = Dprof(ia, ib)
            for x in range(1, n + 1):
                if Dpre[x - 1] <= 0:
                    continue
                rep = V.replay(Sh[ia], Sh[ib], [("K", x)])
                ia2 = idx[J.dumps(rep["endA"], sort_keys=True)]
                ib2 = idx[J.dumps(rep["endB"], sort_keys=True)]
                v = ia2 * nS + ib2
                if Vf[u] - Vf[v] - Dpre[x - 1] != 0:
                    continue  # only tight positive edges
                Dpost = Dprof(ia2, ib2)
                P = [y for y in range(1, n + 1) if Dpost[y - 1] > 0]
                posts += 1
                det[(tuple(Dpre), x)].add(tuple(P))
                split[len(P)] += 1
                # direction: y vs x relative to roots (toward root = smaller
                # B-depth post? use ancestor relation in Bpost)
                LB = LamB(ib2)
                for y in P:
                    # ancestor: is y ancestor of x or vice versa in Bpost?
                    B2 = rep["endB"]
                    pa = []
                    nd = B2
                    # find path to x and y via key search
                    for t_, yy in ((B2, x), (B2, y)):
                        p = []
                        m = t_
                        while m is not None and m[0] != yy:
                            p.append(m[0])
                            m = m[1] if yy < m[0] else m[2]
                        if yy == x:
                            px = p
                        else:
                            py = p
                    if x in py:
                        toward["up"] += 1
                    elif y in px:
                        toward["down"] += 1
                    else:
                        toward["side"] += 1
                    # Lambda overlap: shared fringe keys between row_x(B)
                    # and row_y(Bpost)? use pre/post row key sets
                    _, lamx = R_coeffs(Sh[ib], x)
                    _, lamy = R_coeffs(rep["endB"], y)
                    ox = set(lamx)
                    oy = set(lamy)
                    if ox & oy:
                        ov["overlap"] += 1
                    else:
                        ov["disjoint"] += 1
        if (ia + 1) % 10 == 0:
            step("G", "ia=%d/%d postedges=%d" % (ia + 1, nS, posts))
    detamb = sum(1 for v in det.values() if len(v) > 1)
    step("R", "tight-pos edges=%d det-classes=%d det-amb=%d" %
         (posts, len(det), detamb))
    step("R", "post-count hist=%s" % dict(sorted(split.items())))
    step("R", "direction=%s lambda=%s" % (dict(toward), dict(ov)))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("vprop%d.json" % n)).write_text(
        json.dumps({"edges": posts, "det_amb": detamb,
                    "counts": dict(split), "dir": dict(toward),
                    "lam": dict(ov)}, indent=1, default=str),
        encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
