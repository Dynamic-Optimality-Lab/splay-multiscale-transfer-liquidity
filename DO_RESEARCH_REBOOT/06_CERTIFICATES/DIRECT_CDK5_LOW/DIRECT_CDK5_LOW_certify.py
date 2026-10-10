"""PHASE 4: exact longest-path potentials (SPFA) or positive countercycle.

Finds integer h with h[v] >= h[u]+w on every edge (no positive cycle), else
extracts an exact positive-weight directed cycle. Deterministic, exact ints.
"""
import sys, json
sys.path.insert(0, 'scripts')
from pathlib import Path
from collections import deque
RDIR = Path('DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW')

LOG = open(RDIR / 'DIRECT_CDK5_LOW_certify.log', 'w')
def log(s):
    LOG.write(s + "\n"); LOG.flush(); print(s, flush=True)

man = json.load(open(RDIR / 'DIRECT_CDK5_LOW_graph_manifest.json'))
E = json.load(open(RDIR / 'DIRECT_CDK5_LOW_graph_edges.json'))["edges"]
V = man["vertices"]
log("vertices=%d edges=%d" % (V, len(E)))
adj = [[] for _ in range(V)]
for (u, v, w, d, chg) in E:
    adj[u].append((v, w))

INF_NEG = -10 ** 18
h = [0] * V
inq = [True] * V
cnt = [0] * V
parent = [-1] * V
pw = [0] * V
q = deque(range(V))
nproc = 0
cycle = None
while q:
    u = q.popleft()
    inq[u] = False
    hu = h[u]
    for (v, w) in adj[u]:
        nproc += 1
        if h[v] < hu + w:
            h[v] = hu + w
            parent[v] = u
            pw[v] = w
            if not inq[v]:
                inq[v] = True
                q.append(v)
                cnt[v] += 1
                if cnt[v] > V:
                    # positive cycle: walk back V steps then collect
                    c = v
                    for _ in range(V):
                        c = parent[c]
                    cyc = []
                    cur = c
                    while True:
                        cyc.append(cur)
                        cur = parent[cur]
                        if cur == c or cur < 0 or len(cyc) > V + 5:
                            break
                    cycle = cyc
                    q.clear()
                    break
    if cycle is not None:
        break
log("relaxations processed: %d" % nproc)
if cycle is not None:
    tot = sum(pw[n] for n in cycle)
    log("POSITIVE CYCLE: %d nodes weight=%d" % (len(cycle), tot))
    json.dump({"positive_cycle": True, "nodes": cycle,
               "weight": tot,
               "vert_table": man["vert_table"]},
              open(RDIR / 'DIRECT_CDK5_LOW_positive_countercycle.json', 'w'))
else:
    # verify all edges
    bad = 0
    for (u, v, w, d, chg) in E:
        if h[v] < h[u] + w:
            bad += 1
    C0 = max(h)
    eta = [C0 - x for x in h]
    bad2 = 0
    for (u, v, w, d, chg) in E:
        if w + eta[v] - eta[u] > 0:
            bad2 += 1
    log("potential range: [%d, %d]; edge violations=%d; eta violations=%d" % (
        min(h), max(h), bad, bad2))
    assert bad == 0 and bad2 == 0
    json.dump({"positive_cycle": False, "h": h, "eta": eta,
               "lo": min(h), "hi": max(h)},
              open(RDIR / 'DIRECT_CDK5_LOW_potential_certificate.json', 'w'))
    log("potential certificate saved")
LOG.close()
