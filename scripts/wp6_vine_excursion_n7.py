"""PIVOT-9-2 vine excursion oracle, phase B (n=7 streaming census).

Memory-safe (no pair adjacency): shape-level transitions + on-the-fly
successors; reverse multi-source BFS from all vine-pairs (dist + parent);
reconstruct shortest first-return per exit edge; W_2 / twin / E3-residual /
E4b census. Run from repo root; writes vine_excursion/exc_n7.json.
"""
from __future__ import annotations
import sys
import json
import copy
from pathlib import Path
from collections import deque, Counter

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "python"))
sys.path.insert(0, str(ROOT / "scripts"))
from wp6_eventflow import to_ptr, splay_A, splay_B_push
from wp6_adv import depths_of

BD = ROOT / "artifacts" / "v04" / "wp6_present" / "0909c74a" / "vine_excursion"


def shapes_of(kk):
    if not kk:
        return [None]
    res = []
    for i, k in enumerate(kk):
        for l in shapes_of(kk[:i]):
            for r in shapes_of(kk[i + 1:]):
                res.append([k, l, r])
    return res


def main():
    n = 7
    ks = list(range(1, n + 1))
    Sh = shapes_of(ks)
    nS = len(Sh)
    idx = {json.dumps(s, sort_keys=True): i for i, s in enumerate(Sh)}
    ptrs = [to_ptr(copy.deepcopy(s)) for s in Sh]

    def enc(P):
        return None if P is None else (P["k"], enc(P["l"]), enc(P["r"]))

    def shape_of(P):
        return idx[json.dumps(list(enc(P)), sort_keys=True)]

    ATn = [[0] * (n + 1) for _ in range(nS)]
    ATa = [[0] * (n + 1) for _ in range(nS)]
    BTn = [[0] * (n + 1) for _ in range(nS)]
    BTb = [[0] * (n + 1) for _ in range(nS)]
    dep = [[0] * (n + 1) for _ in range(nS)]
    for ia in range(nS):
        d = depths_of(copy.deepcopy(ptrs[ia]))
        for x in ks:
            dep[ia][x] = d.get(x, 0)
            A2 = copy.deepcopy(ptrs[ia])
            A2, iv = splay_A(A2, x)
            ATn[ia][x], ATa[ia][x] = shape_of(A2), len(iv)
            B2 = copy.deepcopy(ptrs[ia])
            B2, p = splay_B_push(B2, x)
            BTn[ia][x], BTb[ia][x] = shape_of(B2), len(p)
    print("[VEX-7] trans done nS=%d" % nS, flush=True)
    vine = set(ia for ia in range(nS) if max(dep[ia][1:]) == n - 1)
    roots = [s[0] for s in Sh]
    N = nS * nS
    isV = bytearray(N)
    for ia in vine:
        for ib in vine:
            isV[ia * nS + ib] = 1
    invA, invB = {}, {}
    for ia in range(nS):
        for x in ks:
            invA.setdefault((ATn[ia][x], x), []).append(ia)
            invB.setdefault((BTn[ia][x], x), []).append(ia)
    dist = [-1] * N
    par = [-1] * N
    dq = deque()
    for u in range(N):
        if isV[u]:
            dist[u] = 0
            dq.append(u)
    while dq:
        u = dq.popleft()
        ia, ib = u // nS, u % nS
        du = dist[u] + 1
        for x in ks:
            for ja in invA.get((ia, x), []):
                v = ja * nS + ib
                if dist[v] == -1:
                    dist[v] = du
                    par[v] = u
                    dq.append(v)
            la = invA.get((ia, x), [])
            for jb in invB.get((ib, x), []):
                for ja in la:
                    v = ja * nS + jb
                    if dist[v] == -1:
                        dist[v] = du
                        par[v] = u
                        dq.append(v)
    print("[VEX-7] unreachable=%d" % sum(1 for d in dist if d == -1), flush=True)

    def edge_between(u, v):
        ia, ib = u // nS, u % nS
        for x in ks:
            if ATn[ia][x] * nS + ib == v:
                return ("D", x, ATa[ia][x], 0)
            if ATn[ia][x] * nS + BTn[ib][x] == v:
                return ("K", x, ATa[ia][x], BTb[ib][x])
        raise KeyError((u, v))

    Wc, ABc = Counter(), Counter()
    npos = nres1 = ne4b = nex = 0
    posex = []
    for ia in vine:
        for ib in vine:
            u0 = ia * nS + ib
            t0 = roots[ia] != roots[ib]
            for x in ks:
                for kind in (0, 1):
                    if kind == 0:
                        v, e0 = ATn[ia][x] * nS + ib, ("D", x, ATa[ia][x], 0)
                    else:
                        v = ATn[ia][x] * nS + BTn[ib][x]
                        e0 = ("K", x, ATa[ia][x], BTb[ib][x])
                    if isV[v]:
                        continue
                    A, B = e0[2], e0[3]
                    u = v
                    L = 1
                    while not isV[u]:
                        w = par[u]
                        e = edge_between(u, w)
                        A += e[2]
                        B += e[3]
                        L += 1
                        u = w
                    W = B - 2 * A
                    Wc[W] += 1
                    nex += 1
                    ja, jb = u // nS, u % nS
                    t1 = roots[ja] != roots[jb]
                    if W > 0:
                        npos += 1
                        posex.append({"W": W, "A": A, "B": B, "len": L,
                                      "t0": t0, "t1": t1,
                                      "exit": [e0[0], e0[1]]})
                        ABc[(A, B)] += 1
                    if W > A:
                        ne4b += 1
                    if W - ((1 if t0 else 0) - (1 if t1 else 0)) > 0:
                        nres1 += 1
    print("[VEX-7] excursions=%d Wrange=[%d,%d] positives=%d residual-pos=%d E4b=%d"
          % (nex, min(Wc), max(Wc), npos, nres1, ne4b), flush=True)
    BD.mkdir(parents=True, exist_ok=True)
    (BD / "exc_n7.json").write_text(json.dumps(
        {"n": 7, "exits": nex, "Wmin": min(Wc), "Wmax": max(Wc),
         "positives": npos, "residual_pos": nres1, "E4b_viol": ne4b,
         "Whist": dict(sorted(Wc.items())),
         "posAB": [[list(k), v] for k, v in sorted(ABc.items())],
         "posW": dict(sorted(Counter(p["W"] for p in posex).items())),
         "posT": [[list(k), v] for k, v in
                  sorted(Counter((p["t0"], p["t1"]) for p in posex).items())]},
        indent=1, sort_keys=True, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
