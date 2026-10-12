# Per-mask B-controller table (all 126 masks): SCCs + depth-8 edges + self-loops.
import sys, json, time
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

ALL9 = shapes(list(range(1, 10)))
MASKS = list(combinations(range(1, 10), 5))
trans = {}  # (mi, si, x) -> dj  (dj = index)
for mi, mask in enumerate(MASKS):
    for si, t in enumerate(ALL9):
        for x in mask:
            trans[(mi, si, x)] = None  # placeholder
print("tables init", flush=True)
# compute transitions per mask (trace)
edge_of = {}
for mi, mask in enumerate(MASKS):
    for si, t in enumerate(ALL9):
        for x in mask:
            t2 = S.trace(t, x)[0]
            edge_of[(mi, si, x)] = t2
    if mi % 30 == 0:
        print("mask %d traced" % mi, flush=True)

def sig(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, sig(l), sig(r))

idx = {sig(t): i for i, t in enumerate(ALL9)}
rec = {}
for mi, mask in enumerate(MASKS):
    triples = 0
    pairs = set()
    zloops = 0
    d8 = 0
    adj = {}
    for si, t in enumerate(ALL9):
        for x in mask:
            t2 = edge_of[(mi, si, x)]
            dj = idx[sig(t2)]
            triples += 1
            pairs.add((si, dj))
            if dj == si:
                zloops += 1
            if depth(t, x) == 8:
                d8 += 1
            adj.setdefault(si, set()).add(dj)
    # SCC count (iterative Tarjan)
    index_of = {}
    low = {}
    onst = set()
    st = []
    comps = 0
    ix = [0]
    for s in range(len(ALL9)):
        if s in index_of:
            continue
        work = [(s, 0)]
        while work:
            v, pi = work[-1]
            if pi == 0:
                index_of[v] = low[v] = ix[0]
                ix[0] += 1
                st.append(v)
                onst.add(v)
            rec2 = False
            nbrs = sorted(adj.get(v, ()))
            for i in range(pi, len(nbrs)):
                w = nbrs[i]
                if w not in index_of:
                    work[-1] = (v, i + 1)
                    work.append((w, 0))
                    rec2 = True
                    break
                elif w in onst:
                    low[v] = min(low[v], index_of[w])
            if rec2:
                continue
            work.pop()
            if work:
                u = work[-1][0]
                low[u] = min(low[u], low[v])
            if low[v] == index_of[v]:
                while True:
                    w = st.pop()
                    onst.discard(w)
                    if w == v:
                        break
                comps += 1
    rec[str(mask)] = {"states": len(ALL9), "triples": triples, "pairs": len(pairs),
                      "selfloops": zloops, "sccs": comps, "d8": d8}
    if mi % 30 == 0:
        print("mask %d scc done" % mi, flush=True)
json.dump(rec, open(PDIR + "CC_B_MASK_TABLE.json", "w"), indent=1)
tot_d8 = sum(v["d8"] for v in rec.values())
print("masks=%d total_d8=%d" % (len(rec), tot_d8), flush=True)
print("scc range:", min(v["sccs"] for v in rec.values()), max(v["sccs"] for v in rec.values()), flush=True)
