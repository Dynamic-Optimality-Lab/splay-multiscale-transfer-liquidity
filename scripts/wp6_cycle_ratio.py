"""PIVOT-2 CYCLE RATIO ORACLE (phase 1: graph build + SCC census).

For n: all BST shapes; pair graph with exact (A,B) StepEv weights;
BFS reachable per diagonal T0; Tarjan SCC; recurrent filter; report sizes
(decides exact max-ratio method). Artifacts: pivot_cycle/.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path
from collections import deque

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "pivot_cycle"


def step(sid, msg):
    line = "[CYCLE %s] %s" % (sid, msg)
    print(line, flush=True)
    try:
        BD.mkdir(parents=True, exist_ok=True)
        with open(BD / "progress.log", "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass


def save(name, obj):
    BD.mkdir(parents=True, exist_ok=True)
    (BD / name).write_text(json.dumps(obj, indent=1, sort_keys=True,
                                      default=str), encoding="utf-8")


def shapes_of(ks):
    if not ks:
        return [None]
    res = []
    for i, k in enumerate(ks):
        for l in shapes_of(ks[:i]):
            for r in shapes_of(ks[i + 1:]):
                res.append([k, l, r])
    return res


def enc_ptr(P):
    if P is None:
        return None
    return (P["k"], enc_ptr(P["l"]), enc_ptr(P["r"]))


def norm_enc(e):
    # list-shape [k,l,r] -> tuple form matching enc_ptr
    if e is None:
        return None
    return (e[0], norm_enc(e[1]), norm_enc(e[2]))


def build(n):
    ks = list(range(1, n + 1))
    Sh = shapes_of(ks)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    # per-shape ptr + per (shape,key) transitions
    ptrs = [to_ptr(copy.deepcopy(s)) for s in Sh]

    def shape_of(P):
        return idx[json.dumps(list(enc_ptr(P)), sort_keys=True)]

    # Atrans[ia][x] = (ia2, a); Btrans similarly (ptr-based, exact counts)
    Atrans = {}
    Btrans = {}
    for ia in range(len(Sh)):
        for x in ks:
            A2 = copy.deepcopy(ptrs[ia])
            A2, iv = splay_A(A2, x)
            Atrans[(ia, x)] = (shape_of(A2), len(iv))
            B2 = copy.deepcopy(ptrs[ia])
            B2, p = splay_B_push(B2, x)
            Btrans[(ia, x)] = (shape_of(B2), len(p))
    # pair graph edges: node id = ia*nS+ib; edges list per node:
    # (to, mode, key, a, b)
    nS = len(Sh)
    adj = {}
    for ia in range(nS):
        for ib in range(nS):
            u = ia * nS + ib
            el = []
            for x in ks:
                ia2, a = Atrans[(ia, x)]
                el.append((ia2 * nS + ib, "D", x, a, 0))
                ib2, b = Btrans[(ib, x)]
                el.append((ia2 * nS + ib2, "K", x, a, b))
            adj[u] = el
    return {"n": n, "nS": nS, "adj": adj, "Sh": Sh}


def tarjan_scc(nodes, adj):
    # iterative Tarjan over node subset (set); adj restricted
    index_of = {}
    low = {}
    onstack = set()
    stack = []
    sccs = []
    counter = [0]

    for root in nodes:
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
            nbrs = [t for (t, _, _, _, _) in adj[v] if t in nodes]
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
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    step("CY-00", "build n=%d" % n)
    G = build(n)
    nS = G["nS"]
    adj = G["adj"]
    V = nS * nS
    step("CY-01", "shapes=%d pairnodes=%d" % (nS, V))
    # per-T0 BFS reachable
    import collections
    reach = {}
    for i in range(nS):
        start = i * nS + i
        seen = {start}
        dq = deque([start])
        while dq:
            u = dq.popleft()
            for (t, _, _, _, _) in adj[u]:
                if t not in seen:
                    seen.add(t)
                    dq.append(t)
        reach[i] = seen
    sizes = sorted([len(v) for v in reach.values()])
    step("CY-02", "reachable-size min/med/max=%d/%d/%d" %
         (sizes[0], sizes[len(sizes) // 2], sizes[-1]))
    # union + SCC on union
    union = set()
    for v in reach.values():
        union |= v
    sccs = tarjan_scc(union, adj)
    # recurrent: size>1 or self-loop
    rec = []
    for c in sccs:
        if len(c) > 1:
            rec.append(c)
        else:
            v = c[0]
            if any(t == v for (t, _, _, _, _) in adj[v]):
                rec.append(c)
    step("CY-03", "SCCs=%d recurrent=%d" % (len(sccs), len(rec)))
    recsizes = sorted([len(c) for c in rec], reverse=True)[:10]
    step("CY-04", "top recurrent SCC sizes=%s" % recsizes)
    # zero-A-positive-B cycle check per T0: restrict to A=0 edges,
    # SCC with a B>0 edge
    za = 0
    for i in range(nS):
        nodes = reach[i]
        zadj = {u: [t for (t, _, _, a, _) in adj[u]
                    if a == 0 and t in nodes] for u in nodes}
        # SCC on zero-A subgraph (reuse tarjan with fake edge tuples)
        fadj = {u: [(t, "D", 0, 0, 0) for t in z] for u, z in zadj.items()}
        zc = tarjan_scc(nodes, fadj)
        for c in zc:
            cs = set(c)
            if len(c) > 1 or any(u in zadj[u] for u in c):
                # B>0 edge inside?
                for u in c:
                    for t in zadj[u]:
                        if t in cs:
                            # find B of that edge
                            for (t2, _, _, _, b) in adj[u]:
                                if t2 == t and b > 0:
                                    za += 1
                                    break
    step("CY-05", "T0s with zeroA-posB cycle: %d/%d" % (za, nS))
    save("census_n%d.json" % n, {
        "n": n, "shapes": nS, "pairnodes": V,
        "reach_sizes": sizes,
        "nscc": len(sccs), "nrec": len(rec),
        "top_rec_sizes": recsizes,
        "zeroA_posB_T0": za})
    return 0


if __name__ == "__main__":
    sys.exit(main())
