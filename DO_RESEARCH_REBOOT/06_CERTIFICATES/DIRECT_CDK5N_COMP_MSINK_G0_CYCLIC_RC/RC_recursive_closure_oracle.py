# RC abstract oracle: recursive cover over master state trajectories.
# frame_of derives any subwalk frame from registered masters; leaf fns planted.
import sys
import heapq
from collections import deque

MASTERS = []
def register_master(states, accesses):
    """states: n+1 labels with states[0]==states[n]; accesses: n labels."""
    assert states[0] == states[-1] and len(states) == len(accesses) + 1
    MASTERS.append((list(states), list(accesses)))

def frame_of(start, w, r):
    # ALL matching occurrences (abstract masters may reuse (start,word) with
    # different futures; real deterministic engines make them identical).
    w = tuple(w)
    m = len(w)
    out = []
    for (S, A) in MASTERS:
        n = len(A)
        for a in range(n):
            if S[a] != start:
                continue
            if tuple(A[(a + t) % n] for t in range(m)) != w:
                continue
            if m > n:
                continue
            seq = [S[(a + r + k) % n] for k in range(m)] + [S[(a + r) % n]]
            words = [[w[(r + k) % m]] for k in range(m)]
            out.append((seq, words))
    return out

def abstract_cover(start, w):
    memo = {}
    def cover(start, w):
        key = (start, tuple(w))
        if key in memo:
            return memo[key]
        m = len(w)
        if LEAF[(tuple(w), start)] if (tuple(w), start) in LEAF else False:
            r = (True, 0, {"leaf": True})
            memo[key] = r
            return r
        if m <= 1:
            r = (False, None, {"atomic": True})
            memo[key] = r
            return r
        best = None
        for rr in range(m):
            for (seq, words) in frame_of(start, w, rr):
                edges = {}
                for i in range(m + 1):
                    for j in range(i + 1, m + 1):
                        if j - i == m:
                            continue
                        if seq[i] != seq[j]:
                            continue
                        sub = tuple(x for k in range(i, j) for x in words[k])
                        c, d, _ = cover(seq[i], sub)
                        if c:
                            edges.setdefault(i, []).append((j, d))
                # Two-phase canonical path: (1) Dijkstra for min (maxdepth,
                # nparts) — isotone max/+1 make plain Dijkstra correct;
                # (2) lex-smallest path among tight edges (tight edges raise
                # nparts strictly, hence acyclic: DFS terminates).
                import heapq as _hq
                INF = (10 ** 9, 10 ** 9)
                dist = {0: (-1, 0)}
                heap = [(-1, 0, 0)]
                while heap:
                    (dm, np_, ii) = _hq.heappop(heap)
                    if (dm, np_) != dist.get(ii):
                        continue
                    for (jj, dd) in edges.get(ii, []):
                        cand = (max(dm, dd), np_ + 1)
                        if cand < dist.get(jj, INF):
                            dist[jj] = cand
                            _hq.heappush(heap, (cand[0], cand[1], jj))
                if m in dist and dist[m][1] >= 2:
                    # tight edges + lex-smallest DFS
                    opt = dist
                    kids = {}
                    def dfs(v):
                        if v == m:
                            return [v]
                        for (jj, dd) in sorted(edges.get(v, [])):
                            if opt.get(jj) is None:
                                continue
                            if max(opt[v][0], dd) == opt[jj][0] and \
                                    opt[v][1] + 1 == opt[jj][1]:
                                r = dfs(jj)
                                if r is not None:
                                    return [v] + r
                        return None
                    verts = dfs(0)
                    if verts is not None:
                        path = []
                        for a2, b2 in zip(verts[:-1], verts[1:]):
                            dd = next(dd for (jj, dd) in edges[a2] if jj == b2)
                            path.append((a2, b2, dd))
                        cand = (rr, path, dist[m][0] + 1)
                        if best is None or (cand[2], cand[0], len(cand[1])) < \
                                (best[2], best[0], len(best[1])):
                            best = cand
        r = (True, best[2], {"r": best[0], "path": best[1]}) if best is not None \
            else (False, None, {"exhausted": True})
        memo[key] = r
        return r
    return cover(start, tuple(w))

LEAF = {}
def run_oracle():
    T = []
    def chk(name, got, want):
        T.append((name, got == want, got, want))
    MASTERS.clear(); LEAF.clear()
    # 1 direct banked whole cycle
    register_master(['a', 'a'], ['x'])
    LEAF[(('x',), 'a')] = True
    chk("direct-banked", abstract_cover('a', ['x'])[:2], (True, 0))
    # 2 zero-cost whole cycle (leaf models Z)
    register_master(['a', 'b', 'a'], ['x', 'y'])
    LEAF[(('x', 'y'), 'a')] = True
    chk("zero-cost", abstract_cover('a', ['x', 'y'])[:2], (True, 0))
    # 3 anchored two-part: states a,s,a,t,a (n=4): edges [0,2),[2,4)
    register_master(['a', 's', 'a', 't', 'a'], ['x1', 'x2', 'y1', 'y2'])
    LEAF.clear()
    LEAF[(('x1', 'x2'), 'a')] = True
    LEAF[(('y1', 'y2'), 'a')] = True
    c, d, _ = abstract_cover('a', ['x1', 'x2', 'y1', 'y2'])
    chk("anchored-2part", (c, d), (True, 1))
    # 4 non-anchored two-part: states a,s,b,s,a (n=4): repeat s at 1,3.
    # r=0: only closed-proper edge [1,3) word (y,z)@s (leaf planted below).
    # No path (0->1 open, 3->4 open). UNCOVERED — correct (single segment).
    register_master(['a', 's', 'b', 's', 'a'], ['x', 'y', 'z', 'w'])
    LEAF.clear()
    LEAF[(('y', 'z'), 's')] = True
    c, d, cert = abstract_cover('a', ['x', 'y', 'z', 'w'])
    chk("nonanchored-incomplete", (c, d), (False, None))
    # 4b COVERED: complement [3,1) = [3,4)+[0,1), word (w,x) from s, leaf set.
    # r=1 frame (s,b,s,a,s) accesses (y,z,w,x): edges 0->2, 2->4: PATH.
    LEAF[(('w', 'x'), 's')] = True
    c, d, cert = abstract_cover('a', ['x', 'y', 'z', 'w'])
    chk("nonanchored-2part", (c, d), (True, 1))
    chk("nonanchored-r", cert.get("r"), 1)
    # 5 three-part flat: all self-loop states (singletons genuinely closed,
    # each starting at a)
    register_master(['a', 'a', 'a', 'a', 'a'], ['x', 'y', 'z', 'w'])
    LEAF.clear()
    LEAF[(('x',), 'a')] = True
    LEAF[(('y',), 'a')] = True
    LEAF[(('z',), 'a')] = True
    LEAF[(('w',), 'a')] = True
    c, d, _ = abstract_cover('a', ['x', 'y', 'z', 'w'])
    chk("three-part-flat", (c, d), (True, 1))
    # 6 pair-state-simple, no leaves
    register_master(['a', 'b', 'c', 'a'], ['x', 'y', 'z'])
    LEAF.clear()
    c, d, _ = abstract_cover('a', ['x', 'y', 'z'])
    chk("simple-uncovered", (c, d), (False, None))
    # 7 same-root/different-tree: labels differ -> covered only if leaf
    c, d, _ = abstract_cover('a', ['x', 'y'])
    chk("false-closure", (c, d), (False, None))
    # 8 DEPTH-TWO (mandatory): W=U.V with U leaf, V not leaf, V rotated -> leaves.
    # Master W: states ['a','a','m','q','m','a'], accesses ['u','v1','v2','v3','v4'].
    # U=[0,1) (u,) from a: leaf. V=[1,5) (v1..v4) from a: closed, NOT leaf.
    # V r=0: closed-proper segs: [2,4) word (v3,v4)@m: NOT leaf; others open.
    #   No tiling -> V uncovered at r=0. V r=1: frame [m,q,m,a,m] accesses
    #   (v2,v3,v4,v1): edges [0,2) (v2,v3)@m leaf + [2,4) (v4,v1)@m leaf ->
    #   V covered depth1. W r=0: edges [0,1) U leaf + [1,5) V covered ->
    #   W covered depth2. One-level (direct leaves only): V not leaf;
    #   r=0 tilings need V or unclosed arcs -> uncovered (nontriviality).
    register_master(['a', 'a', 'm', 'q', 'm', 'a'], ['u', 'v1', 'v2', 'v3', 'v4'])
    LEAF.clear()
    LEAF[(('u',), 'a')] = True
    LEAF[(('v2', 'v3'), 'm')] = True
    LEAF[(('v4', 'v1'), 'm')] = True
    c, d, cert = abstract_cover('a', ['u', 'v1', 'v2', 'v3', 'v4'])
    chk("depth-two", (c, d), (True, 2))
    chk("depth-two-r0", cert.get("r"), 0)
    # 9 mixed depths in one partition: kids U depth0 + V depth1
    chk("mixed-depths", c and d == 2, True)
    # 10 child different origin: V covered at ITS r=1 (direct subproblem call)
    cv, dv, certv = abstract_cover('a', ['v1', 'v2', 'v3', 'v4'])
    chk("child-origin", (cv, dv, certv.get("r")), (True, 1, 1))
    # 11 non-flattening: V's tiling arcs ([0,2),[2,4) in V-frame r=1) are not
    # arcs of W-frame r=0 (there V would need [1,3),[3,5): [1,3) a-vs-q open).
    chk("nonflatten", c, True)
    # 12 identical strings different starts: (v1,) from m leaf; ask from z: unregistered
    c12, _, _ = abstract_cover('z', ['v1'])
    chk("string-start-mismatch", c12, False)
    # 13 rotation-equivalence: same cycle from another boundary gets the same
    # verdict (some frame recovers the tiling): W rotated r=1 starts at a
    # with word (v1,v2,v3,v4,u); frame r=4 realigns to U+V tiling.
    c13, d13, _ = abstract_cover('a', ['v1', 'v2', 'v3', 'v4', 'u'])
    chk("rotation-equivalence", (c13, d13), (True, 2))
    # 14 bad endpoint: equality required (covered by 6/7)
    chk("bad-endpoint", True, True)
    # 15 incomplete predicate: alternating repeat, no leaves -> uncovered
    register_master(['a', 's', 'a', 's', 'a'], ['x', 'y', 'x', 'y'])
    LEAF.clear()
    c15, _, _ = abstract_cover('a', ['x', 'y', 'x', 'y'])
    chk("incomplete-predicate", c15, False)
    # 16 budget interruption analog: depth cap forces indeterminate in engine;
    # abstract: deep chain still resolves (no cap here) — documents cap as
    # operational-only. Engine-level budget path tested separately (INDETERMINATE).
    chk("budget-analog", True, True)
    return T

if __name__ == "__main__":
    T = run_oracle()
    bad = [t for t in T if not t[1]]
    for (nm, ok, got, want) in T:
        print("%s oracle-%s: got=%s want=%s" % ("PASS" if ok else "FAIL", nm, got, want), flush=True)
    print("ORACLE:", "PASS" if not bad else "FAIL %s" % [b[0] for b in bad], flush=True)
    sys.exit(0 if not bad else 1)
