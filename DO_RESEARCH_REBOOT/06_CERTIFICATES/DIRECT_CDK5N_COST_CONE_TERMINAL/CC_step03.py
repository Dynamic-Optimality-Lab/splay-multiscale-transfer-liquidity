# STEP 03: universal B-controller (all 126 masks) + reconciliation.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S
from itertools import combinations

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'

def shapes(keys):
    if not keys:
        return [S.LEAF]
    out = []
    for i, k in enumerate(keys):
        for l in shapes(keys[:i]):
            for r in shapes(keys[i + 1:]):
                out.append(S.node(k, l, r))
    return out

KEYS9 = list(range(1, 10))
ALL = shapes(KEYS9)
print("9-node shapes: %d" % len(ALL), flush=True)
MASKS = list(combinations(KEYS9, 5))
print("masks: %d" % len(MASKS), flush=True)

def depth(t, x):
    d = 0
    cur = t
    while cur[0] != "leaf":
        _, k, l, r = cur
        if x == k:
            return d
        cur = l if x < k else r
        d += 1
    return None

# full enumeration: state = (shape_idx, mask_idx); edges per marked key
shape_index = {t: i for i, t in enumerate(ALL)}
per_mask = {}
for mi, mask in enumerate(MASKS):
    mset = set(mask)
    # BFS reachable from every shape? Use full set (closed under marked splays? verify)
    edges = {}
    for si, t in enumerate(ALL):
        for x in mask:
            t2 = S.trace(t, x)[0]
            edges[(si, x)] = shape_index[t2]
    per_mask[mi] = edges
    if mi % 30 == 0:
        print("mask %d done" % mi, flush=True)

# collapse check: image shapes subset?
# SCC per mask via Tarjan (iterative)
import sys as _s
_s.setrecursionlimit(1000000)

def sccs_mask(edges, nstates=4862):
    # adjacency distinct dst
    adj = {}
    for (si, x), dj in edges.items():
        adj.setdefault(si, set()).add(dj)
    index_of = {}
    low = {}
    onst = set()
    st = []
    comps = []
    idx = [0]
    for s in range(nstates):
        if s in index_of:
            continue
        work = [(s, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index_of[v] = low[v] = idx[0]
                idx[0] += 1
                st.append(v)
                onst.add(v)
            rec = False
            nbrs = sorted(adj.get(v, ()))
            for i in range(pi, len(nbrs)):
                w = nbrs[i]
                if w not in index_of:
                    work[-1] = (v, i + 1)
                    work.append((w, 0))
                    rec = True
                    break
                elif w in onst:
                    low[v] = min(low[v], index_of[w])
            if rec:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index_of[v]:
                c = []
                while True:
                    w = st.pop()
                    onst.discard(w)
                    c.append(w)
                    if w == v:
                        break
                comps.append(c)
    return comps

odd = MASKS.index((1, 3, 5, 7, 9))
E = per_mask[odd]
# edge-count conventions
triples = len(E)  # (src,key)->dst
pairs = len({(si, dj) for (si, x), dj in E.items()})  # distinct (src,dst)
# zero-cost loops: KEEP at root (depth 0)
zloops = sum(1 for (si, x), dj in E.items() if dj == si)
print("odd-mask: triples=%d pairs=%d selfloops=%d" % (triples, pairs, zloops), flush=True)
comps = sccs_mask(E)
print("odd-mask SCCs=%d nontrivial=%d" % (len(comps), sum(1 for c in comps if len(c) > 1 or any(E.get((c[0], x)) == c[0] for x in MASKS[odd]))), flush=True)
# depth-8 edges
d8 = [(si, x) for (si, x), dj in E.items() if depth(ALL[si], x) == 8]
print("odd-mask depth8 edges=%d" % len(d8), flush=True)
# nontrivial-SCC membership
comp_of = {}
for ci, c in enumerate(comps):
    for s in c:
        comp_of[s] = ci
nontriv = set()
for ci, c in enumerate(comps):
    if len(c) > 1:
        nontriv.add(ci)
    elif E.get((c[0], MASKS[odd][0])) == c[0] or any(E.get((c[0], x)) == c[0] for x in MASKS[odd]):
        nontriv.add(ci)
d8nt = [e for e in d8 if comp_of[e[0]] in nontriv]
print("odd-mask depth8 in nontrivial SCCs=%d" % len(d8nt), flush=True)
# reachable-from-initial count (initial = T0 projected shape?) use balanced-ish start: count states with in/out
json.dump({"odd": {"triples": triples, "pairs": pairs, "selfloops": zloops, "sccs": len(comps),
                   "d8": len(d8), "d8_nontrivial": len(d8nt)}}, open(PDIR + "CC_B_GRAPH.json", "w"), indent=1)
