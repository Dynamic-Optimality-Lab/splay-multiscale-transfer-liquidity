# Unified multi-mask concrete product (9-key universes): shared caches + caps + BF.
import sys, json, time
sys.path.insert(0, 'python/independent')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
import splay as S
import numpy as np
from itertools import combinations

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE/'
MASKS = list(combinations(range(1, 10), 5))
CAP_STATES = 6000000
CAP_EDGES = 80000000
WH = 6  # 2(h+1)-q base with h=2

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

def core_of_mask(ps, M):
    # ps: (k,l,r)/'.' pair-serial B component; M: set of marked keys
    c = set()
    def path(nd, x, p):
        if nd == '.':
            return None
        k, l, r = nd
        p = p + [k]
        if k == x:
            return p
        return path(l, x, p) or path(r, x, p)
    for m in M:
        pp = path(ps, m, [])
        if pp is None:
            return None
        c.update(pp)
    return c

def macros_of(A, B, mask, budget=2):
    out = []
    for v in mask:
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
        for v in mask:
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
            for v in mask:
                if depth(A2m, v) != 0:
                    continue
                B2 = S.trace(B, v)[0]
                q = depth(B, v) // 2
                out.append((A2m, B2, 2, q, 4 - q))
    return out

if __name__ == "__main__":
    t_start = time.time()
    ALL9 = shapes9()
    by_root = {}
    for t in ALL9:
        by_root.setdefault(t[1], []).append(t)
    # balanced + vines + T0-shape canonical starts per mask (core-9 + marked root filtered)
    def conv(t):
        if t is None:
            return S.LEAF
        k, l, r = t
        return S.node(k, conv(l), conv(r))
    T0 = conv([9, [6, [1, None, [2, None, [5, [4, [3, None, None], None], None]]], [8, [7, None, None], None]], None])
    vines = []
    t = S.LEAF
    for k in reversed(range(1, 10)):
        t = S.node(k, S.LEAF, t)
    vines.append(t)
    t = S.LEAF
    for k in range(1, 10):
        t = S.node(k, t, S.LEAF)
    vines.append(t)
    bal = S.node(5, S.node(3, S.node(2, S.node(1, S.LEAF, S.LEAF), S.LEAF), S.node(4, S.LEAF, S.LEAF)), S.node(7, S.node(6, S.LEAF, S.LEAF), S.node(8, S.LEAF, S.node(9, S.LEAF, S.LEAF))))
    cands0 = [T0] + vines + [bal]
    At = {}
    Bt = {}
    states = {}
    def Skey(t):
        return serial(t)
    for m in [serial(t) for t in ALL9]:
        pass
    for t in ALL9:
        At.setdefault(serial(t), t)
        Bt.setdefault(serial(t), t)
    print("trees cached: %d" % len(At), flush=True)
    frontier = []
    nstarts = 0
    for mi, mask in enumerate(MASKS):
        M = set(mask)
        for base in cands0:
            for r in mask:
                T = S.trace(base, r)[0]
                if T[1] != r:
                    continue
                st = serial(T)
                c = core_of_mask(st, M)
                if c is None or len(c) != 9:
                    continue
                k = (mi, st, st)
                if k not in states:
                    states[k] = len(states)
                    frontier.append(k)
                    nstarts += 1
                break
    print("masks=%d starts=%d t=%.1fs" % (len(MASKS), nstarts, time.time() - t_start), flush=True)
    low_edges = []
    low_done = set()
    def emit_low(s):
        if s in low_done:
            return
        low_done.add(s)
        mi, sa, sb = s
        mask = MASKS[mi]
        A = At[sa]
        B = Bt[sb]
        seen = set()  # exact-triple dedup (duplicate constraints add nothing to BF)
        for (A2, B2, HH, q, w) in macros_of(A, B, mask):
            ka, kb = serial(A2), serial(B2)
            if ka not in At:
                At[ka] = A2
            if kb not in Bt:
                Bt[kb] = B2
            k2 = (mi, ka, kb)
            if k2 not in states:
                if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
                    continue
                c9 = core_of_mask(kb, set(mask))
                if c9 is None or len(c9) != 9:
                    continue
                states[k2] = len(states)
                frontier.append(k2)
            if (states[k2], w) not in seen:
                seen.add((states[k2], w))
                low_edges.append((states[s], states[k2], w))
    for s in list(states.keys()):
        pass  # starts get emit_low when popped (low_done starts empty)
    last_rep = 0
    # Phase 1: low BFS to closure (emit for every popped state)
    while frontier and len(states) < CAP_STATES and len(low_edges) < CAP_EDGES:
        s = frontier.pop()
        emit_low(s)
        if len(states) - last_rep >= 500000:
            last_rep = len(states)
            print("  ... states=%d edges=%d t=%.1fs" % (len(states), len(low_edges), time.time() - t_start), flush=True)
    closed_low = (not frontier) and len(low_edges) < CAP_EDGES
    print("phase1: states=%d low_edges=%d closed=%s t=%.1fs" % (len(states), len(low_edges), closed_low, time.time() - t_start), flush=True)
    json.dump({"states": len(states), "low_edges": len(low_edges), "closed_low": closed_low,
               "time": round(time.time() - t_start, 1)}, open(PDIR + "UFRL_MM_PHASE1.json", "w"), indent=1)
    # Phase 2: high-cost expansion to fixed point
    ALL9b = ALL9
    by_root = {}
    for t in ALL9b:
        by_root.setdefault(t[1], []).append(t)
    mids = {}
    hi_edges = []
    fanout_done = set()
    done_hi = set()
    fq = list(states.keys())
    while fq and len(states) < CAP_STATES and len(low_edges) + len(hi_edges) < CAP_EDGES:
        s = fq.pop()
        if s not in low_done:
            emit_low(s)
        if s in done_hi:
            continue
        done_hi.add(s)
        mi = s[0]
        mask = MASKS[mi]
        B = Bt[s[2]]
        for v in mask:
            dB = depth(B, v)
            if dB is None:
                continue
            q = dB // 2
            B2 = S.trace(B, v)[0]
            kb2 = serial(B2)
            if kb2 not in Bt:
                Bt[kb2] = B2
            c9 = core_of_mask(kb2, set(mask))
            if c9 is None or len(c9) != 9:
                continue
            mk = (kb2, v, mi)
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
                k2 = (mi, ka, kb2)
                if k2 not in states:
                    states[k2] = len(states)
                    fq.append(k2)
                emit_low(k2)
                hi_edges.append((mk, states[k2], 0))
    phase2_closed = (not fq) and (len(low_edges) + len(hi_edges) < CAP_EDGES)
    print("phase2: states=%d mids=%d hi=%d low=%d closed=%s t=%.1fs" % (len(states), len(mids), len(hi_edges), len(low_edges), phase2_closed, time.time() - t_start), flush=True)
    import numpy as np
    N0 = len(states)
    midmap = {m: N0 + i for i, m in enumerate(mids)}
    E2 = [(u, v, w) for (u, v, w) in low_edges]
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
    print("BF: stable=%s iters=%d t=%.1fs" % (stable, iters, time.time() - t_bf), flush=True)
    json.dump({"states": N0, "mids": len(mids), "N": N, "low_edges": len(low_edges),
               "hi_edges": len(hi_edges), "stable": stable, "iters": iters,
               "closed_low": closed_low, "phase2_closed": phase2_closed,
               "time": round(time.time() - t_start, 1)}, open(PDIR + "UFRL_MM_CERT.json", "w"), indent=1)
    if stable:
        np.save(PDIR + "UFRL_MM_POTENTIAL.npy", dist)
        sl = [None] * N0
        for k, i in states.items():
            sl[i] = [k[0], str(k[1]), str(k[2])]
        json.dump({"states": sl, "masks": [list(m) for m in MASKS],
                   "mids": [[str(m[0]), m[1], m[2]] for m in mids]}, open(PDIR + "UFRL_MM_STATES.json", "w"))
        print("saved", flush=True)
