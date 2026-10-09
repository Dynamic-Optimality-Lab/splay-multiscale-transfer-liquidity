"""PIVOT-25R-V §10-11: structural unit interpretations vs V.

Candidates (all state-computable, no future oracle):
  Mmax  = max(0,max_y D_s(y))
  MpathB= max over B-root-to-leaf paths P of sum_{y in P} max(D,0)
  MpathA= same on A paths
  Mdep  = max_y [D_s(y) + depth_B(y)] clipped at 0
  M anc = max_y [D_s(y) + #B-ancestors(y)] clipped at 0
Tests: exact equality M==V (all states); Bellman M(s)-M(s')>=D(e)
(all edges) with smallest violation saved. Diagnostic only.
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
from wp6_staticR import R_static, depths_list


def step(sid, msg):
    print("[VUT %s] %s" % (sid, msg), flush=True)


def rootpaths(t, n):
    out = []

    def go(nd, cur):
        if nd is None:
            return
        cur = cur + [nd[0]]
        if nd[1] is None and nd[2] is None:
            out.append(cur)
            return
        go(nd[1], cur)
        go(nd[2], cur)
    go(t, [])
    return out


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

    def prof(ia, ib):
        A, B = Sh[ia], Sh[ib]
        da = depths_list(A)
        t = 1 if A[0] == B[0] else 0
        return [R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
                for y in range(1, n + 1)]

    def cand(ia, ib, which):
        D = prof(ia, ib)
        pos = [max(v, 0) for v in D]
        if which == "Mmax":
            return max([0] + D)
        if which == "MpathB":
            return max([0] + [sum(pos[y - 1] for y in p)
                              for p in rootpaths(Sh[ib], n)])
        if which == "MpathA":
            return max([0] + [sum(pos[y - 1] for y in p)
                              for p in rootpaths(Sh[ia], n)])
        if which == "Mdep":
            db = depths_list(Sh[ib])
            return max([0] + [D[y - 1] + db[y] for y in range(1, n + 1)])
        if which == "Manc":
            # positive-ancestor count: #{ancestors z of y (incl y): D(z)>0}
            best = 0
            for y in range(1, n + 1):
                nd = Sh[ib]
                chain = []
                while nd is not None and nd[0] != y:
                    chain.append(nd[0])
                    nd = nd[1] if y < nd[0] else nd[2]
                chain.append(y)
                c = sum(1 for z in chain if D[z - 1] > 0)
                if D[y - 1] + c > best:
                    best = D[y - 1] + c
            return best
        raise AssertionError(which)

    for which in ("Mmax", "MpathB", "MpathA", "Mdep", "Manc"):
        eq = 0
        tot = 0
        for ia in range(nS):
            for ib in range(nS):
                u = ia * nS + ib
                if cand(ia, ib, which) == Vf[u]:
                    eq += 1
                tot += 1
        step("EQ", "%s == V: %d/%d" % (which, eq, tot))
    # Bellman test for the two most interesting (MpathB, Mdep) + Mmax ref
    import pickle
    for which in ("Mmax", "MpathB", "Mdep"):
        bad = 0
        worst = None
        tot = 0
        for ia in range(nS):
            for ib in range(nS):
                u = ia * nS + ib
                mu = cand(ia, ib, which)
                # D_s(x) per key from prof
                A, B = Sh[ia], Sh[ib]
                da = depths_list(A)
                t = 1 if A[0] == B[0] else 0
                D = [R_static(B, y) - 2 * ((da[y] + 1) // 2) - 2 * (1 - t)
                     for y in range(1, n + 1)]
                for x in range(1, n + 1):
                    rep = V.replay(A, B, [("K", x)])
                    import json as J
                    idx = {J.dumps(s, sort_keys=True): i for i, s in
                           enumerate(Sh)}
                    ja = idx[J.dumps(rep["endA"], sort_keys=True)]
                    jb = idx[J.dumps(rep["endB"], sort_keys=True)]
                    mv = cand(ja, jb, which)
                    tot += 1
                    if mu - mv < D[x - 1]:
                        bad += 1
                        if worst is None or (mu - mv) - D[x - 1] < worst[0]:
                            worst = ((mu - mv) - D[x - 1], D[x - 1],
                                     ia, ib, x)
        step("BF", "%s Bellman bad=%d/%d worst=%s" %
             (which, bad, tot, worst))
    return 0


if __name__ == "__main__":
    sys.exit(main())
