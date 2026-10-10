"""DIRECT-U1-06: bounded n=7 pair-state BFS (caps 50k states / 700k transitions).

Tuple-tree engine; SPFA-style longest-path (max W from diagonal) with
positive-cycle detection via relaxation counts. No frozen invariant exists
(obstruction recorded) — invariant columns N/A. Caps strictly enforced."""
import sys, json
sys.path.insert(0, 'scripts')
sys.path.insert(0, 'python/independent')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U1')
import splay as S
import wp6_cycle_ratio as O

def iserial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, iserial(l), iserial(r))
def idepths(t):
    out = {}
    def go(nd, d):
        if nd[0] == "leaf":
            return
        _, k, l, r = nd
        out[k] = d; go(l, d + 1); go(r, d + 1)
    go(t, 0)
    return out
def to_tup(t):
    if t is None:
        return S.LEAF
    return S.node(t[0], to_tup(t[1]), to_tup(t[2]))

N = 7
CAP_STATES = 50000
CAP_TRANS = 700000
MAX_RELAX = 4000000

starts = [to_tup(sh) for sh in O.shapes_of(list(range(1, N + 1)))]
print("diagonal starts:", len(starts), flush=True)
visited = {}
dist = []
parent = []
patrans = []
states_A = []
states_B = []
q = deque()
for T in starts:
    key = (iserial(T), iserial(T))
    if key in visited:
        continue
    i = len(dist)
    visited[key] = i
    dist.append(0)
    parent.append(-1)
    patrans.append(None)
    states_A.append(T)
    states_B.append(T)
    q.append(i)
ntrans = 0
nrelax = 0
inqueue = [True] * len(dist)
cnt = [0] * len(dist)
pos_cycle = None
capped = False
while q:
    u = q.popleft()
    inqueue[u] = False
    A, B = states_A[u], states_B[u]
    dA = idepths(A)
    dB = idepths(B)
    for md in ('K', 'D'):
        for x in range(1, N + 1):
            if ntrans >= CAP_TRANS:
                capped = True
                break
            ntrans += 1
            da = dA.get(x, -1)
            if da < 0:
                continue
            a = (da + 1) // 2
            if md == 'K':
                db = dB.get(x, -1)
                if db < 0:
                    continue
                qq = db // 2
            else:
                qq = 0
            w = qq - 2 * a
            A2, _ = S.trace(A, x)
            B2 = B if md == 'D' else S.trace(B, x)[0]
            key = (iserial(A2), iserial(B2))
            v = visited.get(key)
            if v is None:
                if len(dist) >= CAP_STATES:
                    capped = True
                    continue
                v = len(dist)
                visited[key] = v
                dist.append(dist[u] + w)
                parent.append(u)
                patrans.append((md, x))
                states_A.append(A2)
                states_B.append(B2)
                inqueue.append(True)
                cnt.append(1)
                q.append(v)
            else:
                if dist[u] + w > dist[v]:
                    dist[v] = dist[u] + w
                    parent[v] = u
                    patrans[v] = (md, x)
                    nrelax += 1
                    if nrelax > MAX_RELAX:
                        capped = True
                        break
                    cnt[v] += 1
                    if cnt[v] > len(dist):
                        # positive cycle reachable; reconstruct
                        cyc = v
                        for _ in range(len(dist)):
                            cyc = parent[cyc]
                        cyc_nodes = []
                        cur = cyc
                        for _ in range(len(dist) + 1):
                            cyc_nodes.append(cur)
                            cur = parent[cur]
                            if cur == cyc or cur < 0:
                                break
                        pos_cycle = {"entry": cyc, "nodes": cyc_nodes}
                        q.clear()
                        break
                    if not inqueue[v]:
                        inqueue[v] = True
                        q.append(v)
            if ntrans >= CAP_TRANS:
                capped = True
                break
        if capped or pos_cycle:
            break
    if capped or pos_cycle:
        break
print("states:", len(dist), "transitions:", ntrans, "capped:", capped, flush=True)
print("positive_cycle:", bool(pos_cycle), flush=True)
json.dump({"n": N, "states": len(dist), "transitions": ntrans, "capped": capped,
           "positive_cycle": bool(pos_cycle),
           "cycle": pos_cycle,
           "invariant": "NONE FROZEN (obstruction recorded); residuals N/A"},
          open(RDIR / 'DIRECT_U1_n7_reachability_results.json', 'w'), indent=1)
