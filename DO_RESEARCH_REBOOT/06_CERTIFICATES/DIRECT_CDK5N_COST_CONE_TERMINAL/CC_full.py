# Full certificate build: low-cost BFS + sound high-cost expansion + vectorized BF + potential.
import sys, json, time, pickle
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
from CRA_pointer_tuple_replay import core_of
import splay as S
import numpy as np

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL/'
M = (1, 3, 5, 7, 9)
CAP_STATES = 2000000
CAP_EDGES = 60000000
H = 2
WH = 2 * (H + 1)  # high-cost base weight 2(h+1)-q

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

def shapes9():
    def sh(keys):
        if not keys:
            return [S.LEAF]
        out = []
        for i, k in enumerate(keys):
            for l in sh(keys[:i]):
                for r in sh(keys[i + 1:]):
                    out.append(S.node(k, l, r))
        return out
    return sh(list(range(1, 10)))

def macros_of(A, B, budget=2):
    out = []
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
        out.append((A2, B2, a, q, 2 * a - q))
    cands = [(y, depth(A, y)) for y in range(1, 10)]
    cands = [(y, d) for y, d in cands if d is not None and 1 <= d <= 2 * budget]
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
            if ay + av > budget or ay + av < 1:
                continue
            A2 = S.trace(A1, v)[0]
            B2 = S.trace(B, v)[0]
            q = depth(B, v) // 2
            out.append((A2, B2, ay + av, q, 2 * (ay + av) - q))
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
                B2 = S.trace(B, v)[0]
                q = depth(B, v) // 2
                out.append((A2m, B2, 2, q, 4 - q))
    return out

if __name__ == "__main__":
    t_start = time.time()
    t0 = T0tree()
    ALL9 = shapes9()
    print("shapes9=%d" % len(ALL9), flush=True)
    by_root = {}
    for t in ALL9:
        by_root.setdefault(t[1], []).append(t)
    print("per-root counts:", {k: len(v) for k, v in sorted(by_root.items())}, flush=True)
    At = {serial(t0): t0}
    Bt = {serial(t0): t0}
    start = (serial(t0), serial(t0))
    states = {start: 0}
    low_edges = []  # (src, dst, w) all
    frontier = [start]
    # Phase 1: low-cost BFS to closure
    while frontier and len(states) < CAP_STATES:
        s = frontier.pop()
        A = At[s[0]]
        B = Bt[s[1]]
        for (A2, B2, HH, q, w) in macros_of(A, B):
            ka, kb = serial(A2), serial(B2)
            if ka not in At:
                At[ka] = A2
            if kb not in Bt:
                Bt[kb] = B2
            k2 = (ka, kb)
            if k2 not in states:
                if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
                    continue
                c9 = core_of(kb)
                if c9 is None or len(c9) != 9:
                    continue
                states[k2] = len(states)
                frontier.append(k2)
            low_edges.append((states[s], states[k2], w))
    closed_low = not frontier
    print("phase1: states=%d low_edges=%d closed=%s t=%.1fs" % (len(states), len(low_edges), closed_low, time.time() - t_start), flush=True)
    # Phase 2: high-cost expansion to fixed point (new dstates get low macros too)
    mids = {}  # (kb2, v) -> mid id
    hi_edges = []  # (src, mid, w) + (mid, dst, 0)
    fanout_done = set()
    low_done = set()  # states whose low macros were enumerated (phase-1 states added below)
    fq = list(states.keys())
    done_hi = set()

    def emit_low(s):
        # enumerate low macros of state s (once); returns True (soundness-critical)
        if s in low_done:
            return
        low_done.add(s)
        A = At[s[0]]
        B = Bt[s[1]]
        for (X2, Y2, HH, qq, w) in macros_of(A, B):
            xa, yb = serial(X2), serial(Y2)
            if xa not in At:
                At[xa] = X2
            if yb not in Bt:
                Bt[yb] = Y2
            k3 = (xa, yb)
            if k3 not in states:
                if X2[0] == "leaf" or Y2[0] == "leaf" or X2[1] != Y2[1]:
                    continue
                cc = core_of(yb)
                if cc is None or len(cc) != 9:
                    continue
                states[k3] = len(states)
                fq.append(k3)
            low_edges.append((states[s], states[k3], w))

    for s in list(states.keys()):
        # phase-1 states: mark (their macros were enumerated in phase 1)
        low_done.add(s)
    # single fixed-point loop: every state gets low macros AND high-cost edges exactly once
    while fq and len(states) < CAP_STATES and len(low_edges) + len(hi_edges) < CAP_EDGES:
        s = fq.pop()
        if s not in low_done:
            emit_low(s)
        if s in done_hi:
            continue
        done_hi.add(s)
        B = Bt[s[1]]
        for v in M:
            dB = depth(B, v)
            if dB is None:
                continue
            q = dB // 2
            B2 = S.trace(B, v)[0]
            kb2 = serial(B2)
            if kb2 not in Bt:
                Bt[kb2] = B2
            c9 = core_of(kb2)
            if c9 is None or len(c9) != 9:
                continue
            mk = (kb2, v)
            if mk not in mids:
                mids[mk] = len(mids)
            hi_edges.append((states[s], mk, WH - q))
            if mk in fanout_done:
                continue
            fanout_done.add(mk)
            for A2 in by_root.get(v, []):
                ka = serial(A2)
                if ka not in At:
                    At[ka] = A2
                k2 = (ka, kb2)
                if k2 not in states:
                    states[k2] = len(states)
                    fq.append(k2)
                emit_low(k2)
                hi_edges.append((mk, states[k2], 0))
    phase2_closed = (not fq) and (len(low_edges) + len(hi_edges) < CAP_EDGES)
    print("phase2: states=%d mids=%d hi_edges=%d low_edges=%d closed=%s t=%.1fs" % (len(states), len(mids), len(hi_edges), len(low_edges), phase2_closed, time.time() - t_start), flush=True)
    # renumber mids to N..
    N0 = len(states)
    midmap = {m: N0 + i for i, m in enumerate(mids)}
    E2 = []
    for (u, v, w) in low_edges:
        E2.append((u, v, w))
    for (u, v, w) in hi_edges:
        a = midmap[u] if isinstance(u, tuple) else u
        b = midmap[v] if isinstance(v, tuple) else v
        E2.append((a, b, w))
    N = N0 + len(mids)
    U = np.array([u for u, v, w in E2], dtype=np.int64)
    V = np.array([v for u, v, w in E2], dtype=np.int64)
    W = np.array([w for u, v, w in E2], dtype=np.int64)
    print("BF: N=%d E=%d" % (N, len(E2)), flush=True)
    t_bf = time.time()
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
        if iters % 200 == 0:
            print("  BF %d t=%.1fs" % (iters, time.time() - t_bf), flush=True)
    print("BF: stable=%s iters=%d t=%.1fs" % (stable, iters, time.time() - t_bf), flush=True)
    json.dump({"states": N0, "mids": len(mids), "N": N, "low_edges": len(low_edges),
               "hi_edges": len(hi_edges), "stable": stable, "iters": iters,
               "closed_low": closed_low, "phase2_closed": phase2_closed,
               "time": round(time.time() - t_start, 1)},
              open(PDIR + "CC_CERT.json", "w"), indent=1)
    if stable:
        np.save(PDIR + "CC_POTENTIAL.npy", dist)
        states_list = [None] * N0
        for k, i in states.items():
            states_list[i] = [str(k[0]), str(k[1])]
        json.dump({"states": states_list,
                   "mids": [[str(m[0]), m[1]] for m in mids]},
                  open(PDIR + "CC_STATES.json", "w"))
        print("potential+states saved", flush=True)
