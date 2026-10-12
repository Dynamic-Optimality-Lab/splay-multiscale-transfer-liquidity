# Concrete prototype: lazy product BFS (T0-universe, odd mask) + exact h<=2 macros.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import core_of
import splay as S

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
M = (1, 3, 5, 7, 9)
CAP_STATES = 300000
CAP_MACROS = 20000000

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

def T0tree():
    def conv(t):
        if t is None:
            return S.LEAF
        k, l, r = t
        return S.node(k, conv(l), conv(r))
    return conv([9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None])

def serial(t):
    if t[0] == "leaf":
        return '.'
    _, k, l, r = t
    return (k, serial(l), serial(r))

def macros_of(A, B, budget=2):
    # effective words H<=2 ending KEEP(v in M); returns list of (A2, B2, H, q, w, word)
    out = []
    # single KEEP(v), a(v)<=2
    for v in M:
        d = depth(A, v)
        if d is None:
            continue
        a = (d + 1) // 2
        if a > budget:
            continue
        A2 = S.trace(A, v)[0]
        B2 = S.trace(B, v)[0]
        q = depth(B, v) // 2
        out.append((A2, B2, a, q, 2 * a - q, (("K", v),)))
    # DELETE(y) + KEEP(v), a(y)>=1, total<=2
    cands = [(y, depth(A, y)) for y in range(1, 10)]
    cands = [(y, d) for y, d in cands if d is not None and 1 <= d <= 4]
    for y, dy in cands:
        ay = (dy + 1) // 2
        if ay < 1 or ay > budget:
            continue
        A1 = S.trace(A, y)[0]
        for v in M:
            dv = depth(A1, v)
            if dv is None:
                continue
            av = (dv + 1) // 2
            if ay + av > budget:
                continue
            A2 = S.trace(A1, v)[0]
            B2 = S.trace(B, v)[0]
            q = depth(B, v) // 2
            out.append((A2, B2, ay + av, q, 2 * (ay + av) - q, (("D", y), ("K", v))))
    # DELETE(y1)+DELETE(y2)+KEEP(v), a1=a2=1, aT=0
    for y1, d1 in cands:
        if (d1 + 1) // 2 != 1:
            continue
        A1 = S.trace(A, y1)[0]
        c2 = [(y, depth(A1, y)) for y in range(1, 10)]
        c2 = [(y, d) for y, d in c2 if d is not None and (d + 1) // 2 == 1]
        for y2, d2 in c2:
            A2m = S.trace(A1, y2)[0]
            for v in M:
                if depth(A2m, v) != 0:
                    continue
                A2 = A2m
                B2 = S.trace(B, v)[0]
                q = depth(B, v) // 2
                out.append((A2, B2, 2, q, 4 - q, (("D", y1), ("D", y2), ("K", v))))
    return out

if __name__ == "__main__":
    t0 = T0tree()
    start = (serial(t0), serial(t0))
    states = {start: 0}
    adj = {}
    nmac = 0
    frontier = [start]
    t_start = time.time()
    t_bfs0 = time.time()
    At = {serial(t0): t0}
    Bt = {serial(t0): t0}
    last_report = 0
    while frontier and len(states) < CAP_STATES and nmac < CAP_MACROS:
        s = frontier.pop()
        sa, sb = s
        A = At[sa]
        B = Bt[sb]
        # core-9 + roots sync check
        ms = macros_of(A, B)
        outs = {}
        for (A2, B2, H, q, w, wd) in ms:
            nmac += 1
            ka, kb = serial(A2), serial(B2)
            if ka not in At:
                At[ka] = A2
            if kb not in Bt:
                Bt[kb] = B2
            k2 = (ka, kb)
            outs.setdefault(k2, []).append((H, q, w, wd))
        # keep min-weight edge per dst (sound for negative-cycle detection? NO: keep all, dedup identical)
        adj[s] = [(k, min(w for _, _, w, _ in v)) for k, v in outs.items()]
        for k in outs:
            if k not in states:
                # check roots sync + core9 (domain W_5^9)
                A2, B2 = At[k[0]], Bt[k[1]]
                if A2[0] == "leaf" or B2[0] == "leaf":
                    continue
                if A2[1] != B2[1]:
                    continue
                c9 = core_of(k[1])
                if c9 is None or len(c9) != 9:
                    continue
                states[k] = len(states)
                frontier.append(k)
        if len(states) - last_report >= 20000:
            last_report = len(states)
            print("  ... states=%d macros=%d frontier=%d t=%.1fs" % (len(states), nmac, len(frontier), time.time() - t_bfs0), flush=True)
    t_bfs = time.time() - t_bfs0
    closed = (not frontier) and nmac < CAP_MACROS
    print("states=%d macros=%d bfs_time=%.1fs closed=%s" % (len(states), nmac, t_bfs, closed), flush=True)
    # negative cycle via Bellman-Ford (super source, |V| relaxations)
    N = len(states)
    ids = states
    edges = []
    for s, lst in adj.items():
        for k, w in lst:
            if k in ids:
                edges.append((ids[s], ids[k], w))
    print("edges=%d" % len(edges), flush=True)
    # vectorized Bellman-Ford with early exit (pure-Python O(VE) loop was the bottleneck)
    import numpy as np
    t_bf0 = time.time()
    U = np.array([u for u, v, w in edges], dtype=np.int64)
    V = np.array([v for u, v, w in edges], dtype=np.int64)
    W = np.array([w for u, v, w in edges], dtype=np.int64)
    dist = np.zeros(N, dtype=np.int64)
    iters = 0
    stable = False
    for i in range(N):
        prev = dist.copy()
        np.minimum.at(dist, V, dist[U] + W)
        iters += 1
        if (dist == prev).all():
            stable = True
            break
        if iters % 500 == 0:
            print("  ... BF iter %d t=%.1fs" % (iters, time.time() - t_bf0), flush=True)
    t_bf = time.time() - t_bf0
    neg = not stable
    print("negative_cycle=%s (iters=%d bf_time=%.1fs)" % (neg, iters, t_bf), flush=True)
    json.dump({"states": N, "edges": len(edges), "macros": nmac, "negcycle": neg,
               "closed": closed, "bf_iters": iters, "bf_stable": stable,
               "bfs_time": round(t_bfs, 1), "bf_time": round(t_bf, 1),
               "time": round(time.time() - t_start, 1)},
              open(PDIR + "CC_PROTO.json", "w"), indent=1)
