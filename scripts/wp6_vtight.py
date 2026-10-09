"""PIVOT-25R-V §4-5: tight graph anatomy + positive-D trajectories.

Loads V + rebuilds graph; tight edges; Tarjan SCC; degree/sign stats;
for every D>0 tight edge follows tight successors to V=0/zero-SCC with
full per-step records (D/R_B/A-depth/twin/Lambda rows).
"""
from __future__ import annotations
import sys
import copy
import json
from pathlib import Path
from collections import Counter, deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
import wp6_overflow as V
from wp6_vintegrator import build


def step(sid, msg):
    print("[VTG %s] %s" % (sid, msg), flush=True)


def tarjan(nV, adj):
    index_of = {}
    low = {}
    onstack = set()
    stack = []
    sccs = []
    counter = [0]
    for root in range(nV):
        if root in index_of:
            continue
        work = [(root, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index_of[v] = low[v] = counter[0]
                counter[0] += 1
                stack.append(v)
                onstack.add(v)
            rec = False
            nbrs = adj[v]
            for i in range(pi, len(nbrs)):
                t = nbrs[i]
                if t not in index_of:
                    work[-1] = (v, i + 1)
                    work.append((t, 0))
                    rec = True
                    break
                elif t in onstack:
                    low[v] = min(low[v], index_of[t])
            if rec:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index_of[v]:
                comp = []
                while True:
                    w = stack.pop()
                    onstack.discard(w)
                    comp.append(w)
                    if w == v:
                        break
                sccs.append(comp)
    return sccs


def main():
    import sys as _s
    n = int(_s.argv[1]) if len(_s.argv) > 1 else 5
    Sh, nS, adj = build(n)
    Vcount = nS * nS
    VD = json.loads((ROOT / "artifacts" / "v04" / "wp6_present" /
                     "0909c74a" / "dual_mine" /
                     ("vfull%d.json" % n)).read_text())
    Vf = VD["V"]
    # tight edges
    tight = [[] for _ in range(Vcount)]
    tadj = [[] for _ in range(Vcount)]
    npos = nneg = nz = 0
    for u in range(Vcount):
        for (to, mo, x, w) in adj[u]:
            if Vf[u] - Vf[to] - w == 0:
                tight[u].append((to, mo, x, w))
                tadj[u].append(to)
                if w > 0:
                    npos += 1
                elif w < 0:
                    nneg += 1
                else:
                    nz += 1
    step("T", "tight=%d pos=%d neg=%d zero=%d" %
         (npos + nneg + nz, npos, nneg, nz))
    outd = Counter(len(t) for t in tight)
    step("T", "outdegree hist: %s" % dict(sorted(outd.items())))
    sccs = tarjan(Vcount, tadj)
    step("T", "tight SCCs=%d sizes=%s" %
         (len(sccs), sorted([len(c) for c in sccs], reverse=True)[:12]))
    # zero-D tight SCCs: all internal edges D==0?
    comp_of = {}
    for i, c in enumerate(sccs):
        for v in c:
            comp_of[v] = i
    zscc = 0
    for c in sccs:
        ok = True
        for v in c:
            for (to, _, _, w) in tight[v]:
                if comp_of[to] == comp_of[v] and w != 0:
                    ok = False
        if ok:
            zscc += 1
    step("T", "zero-D tight SCCs=%d/%d" % (zscc, len(sccs)))
    uniq = sum(1 for t in tight if len(t) == 1)
    multi = sum(1 for t in tight if len(t) > 1)
    step("T", "unique-tight-succ=%d multi=%d zero-out=%d" %
         (uniq, multi, sum(1 for t in tight if not t)))
    # positive-D tight trajectories: follow tight successors to V=0/SCC
    from wp6_staticR import R_static, depths_list
    from wp6_lambda import R_coeffs
    chains = []
    for u in range(Vcount):
        for (to, mo, x, w) in tight[u]:
            if w <= 0:
                continue
            # follow first-tight-successor chain (record branching count)
            chain = [{"s": u, "x": x, "w": w, "V": Vf[u],
                      "branch": len(tight[u])}]
            v = to
            seen = {u}
            while Vf[v] != 0 and v not in seen:
                seen.add(v)
                if not tight[v]:
                    chain.append({"s": v, "x": None, "w": 0, "V": Vf[v],
                                  "branch": 0, "dead": True})
                    break
                t2 = tight[v][0]
                chain.append({"s": v, "x": t2[2], "w": t2[3],
                              "V": Vf[v], "branch": len(tight[v])})
                v = t2[0]
            chain.append({"s": v, "V": Vf[v], "term": True})
            chains.append(chain)
    step("P", "positive-D tight edges=%d chains=%d" % (npos, len(chains)))
    ln = Counter(len(c) - 1 for c in chains)
    step("P", "chain-length hist: %s" % dict(sorted(ln.items())))
    (ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" /
     "dual_mine" / ("vtight%d.json" % n)).write_text(
        json.dumps({"npos": npos, "nneg": nneg, "nzero": nz,
                    "outdeg": {str(k): v for k, v in outd.items()},
                    "nscc": len(sccs),
                    "top_scc": sorted([len(c) for c in sccs],
                                      reverse=True)[:12],
                    "zero_scc": zscc, "unique": uniq, "multi": multi,
                    "chains": chains}, indent=1, default=str),
        encoding="utf-8")
    step("S", "saved vtight%d.json" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
