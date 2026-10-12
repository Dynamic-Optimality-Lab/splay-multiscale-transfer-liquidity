# Convention-variant analysis for B-controller reconciliation.
import sys, json
sys.path.insert(0, 'python/independent')
import splay as S
from collections import deque

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

def conv(t):
    if t is None:
        return S.LEAF
    k, l, r = t
    return S.node(k, conv(l), conv(r))

ALL = shapes(list(range(1, 10)))
idx = {t: i for i, t in enumerate(ALL)}
T0t = conv([9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None])
mask = (1, 3, 5, 7, 9)

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

# reachable subgraph
seen = {T0t}
dq = deque([T0t])
trans = {}
while dq:
    t = dq.popleft()
    for x in mask:
        t2 = S.trace(t, x)[0]
        trans[(t, x)] = t2
        if t2 not in seen:
            seen.add(t2)
            dq.append(t2)
print("reachable states: %d" % len(seen), flush=True)
triples = len(trans)
pairs = len({(a, b) for (a, x), b in trans.items()})
zloops = sum(1 for (a, x), b in trans.items() if b == a)
genuine = triples - zloops
print("triples=%d pairs=%d selfloops=%d genuine=%d" % (triples, pairs, zloops, genuine), flush=True)
# SCC (Tarjan iterative) on reachable
nodes = sorted(seen, key=lambda t: idx[t])
nidx = {t: i for i, t in enumerate(nodes)}
adj = {}
for (a, x), b in trans.items():
    adj.setdefault(nidx[a], set()).add(nidx[b])
N = len(nodes)
index_of = {}
low = {}
onst = set()
st = []
comps = []
ix = [0]
for s in range(N):
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
print("SCCs=%d" % len(comps), flush=True)
# nontrivial (size>1 or self-loop)
nontriv = [c for c in comps if len(c) > 1 or any(trans.get((nodes[c[0]], x)) == nodes[c[0]] for x in mask)]
print("nontrivial=%d states_in_nontrivial=%d" % (len(nontriv), sum(len(c) for c in nontriv)), flush=True)
# edges with both ends in nontrivial states
cyc_states = set(s for c in nontriv for s in c)
cyc_triples = sum(1 for (a, x), b in trans.items() if nidx[a] in cyc_states and nidx[b] in cyc_states)
cyc_pairs = len({(a, b) for (a, x), b in trans.items() if nidx[a] in cyc_states and nidx[b] in cyc_states})
print("cyclic-subgraph triples=%d pairs=%d" % (cyc_triples, cyc_pairs), flush=True)
d8 = [(a, x) for (a, x), b in trans.items() if depth(a, x) == 8]
print("depth8 triples=%d" % len(d8), flush=True)
d8c = [(a, x) for (a, x) in d8 if nidx[a] in cyc_states and nidx[trans[(a, x)]] in cyc_states]
print("depth8 in cyclic subgraph=%d" % len(d8c), flush=True)
json.dump({"reachable": len(seen), "triples": triples, "pairs": pairs, "selfloops": zloops,
           "genuine": genuine, "sccs": len(comps), "nontrivial_sccs": len(nontriv),
           "cyclic_states": len(cyc_states), "cyclic_triples": cyc_triples, "cyclic_pairs": cyc_pairs,
           "d8": len(d8), "d8_cyclic": len(d8c)},
          open(PDIR + "CC_B_RECONCILE.json", "w"), indent=1)
