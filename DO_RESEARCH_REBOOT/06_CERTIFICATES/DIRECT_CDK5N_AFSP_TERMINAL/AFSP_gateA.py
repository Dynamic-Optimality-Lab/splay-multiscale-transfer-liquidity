# GATE A: complete nine-key product from ALL diagonal seeds (612k) + reconcile vs 1.31M product.
import sys, json, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
import UFRL_multimask as MM

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_AFSP_TERMINAL/'
MASKS = MM.MASKS
CAP_STATES = 6000000
CAP_EDGES = 80000000

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

if __name__ == "__main__":
    t0 = time.time()
    ALL9 = shapes9()
    At = {}
    Bt = {}
    for t in ALL9:
        At.setdefault(MM.serial(t), t)
        Bt.setdefault(MM.serial(t), t)
    states = {}
    frontier = []
    nstarts = 0
    for mi, mask in enumerate(MASKS):
        M = set(mask)
        for t in ALL9:
            for r in mask:
                T = S.trace(t, r)[0]
                if T[1] != r:
                    continue
                st = MM.serial(T)
                c = MM.core_of_mask(st, M)
                if c is None or len(c) != 9:
                    continue
                k = (mi, st, st)
                if k not in states:
                    states[k] = len(states)
                    frontier.append(k)
                    nstarts += 1
                break
    print("masks=126 starts=%d t=%.1fs" % (nstarts, time.time() - t0), flush=True)
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
        seen = set()
        for (A2, B2, HH, q, w) in MM.macros_of(A, B, mask):
            ka, kb = MM.serial(A2), MM.serial(B2)
            if ka not in At:
                At[ka] = A2
            if kb not in Bt:
                Bt[kb] = B2
            k2 = (mi, ka, kb)
            if k2 not in states:
                if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
                    continue
                c9 = MM.core_of_mask(kb, set(mask))
                if c9 is None or len(c9) != 9:
                    continue
                states[k2] = len(states)
                frontier.append(k2)
            if (states[k2], w) not in seen:
                seen.add((states[k2], w))
                low_edges.append((states[s], states[k2], w))
    last_rep = 0
    while frontier and len(states) < CAP_STATES and len(low_edges) < CAP_EDGES:
        emit_low(frontier.pop())
        if len(states) - last_rep >= 500000:
            last_rep = len(states)
            print("  ... states=%d edges=%d t=%.1fs" % (len(states), len(low_edges), time.time() - t0), flush=True)
    closed_low = (not frontier) and len(low_edges) < CAP_EDGES
    print("phase1: states=%d edges=%d closed=%s t=%.1fs" % (len(states), len(low_edges), closed_low, time.time() - t0), flush=True)
    json.dump({"starts": nstarts, "states": len(states), "edges": len(low_edges),
               "closed": closed_low, "prev_product_states": 1310004,
               "time": round(time.time() - t0, 1)}, open(PDIR + "AFSP_GATE_A.json", "w"), indent=1)
    # Phase 2: high-cost expansion + BF + potential (complete 9-key certificate)
    import numpy as _np
    ALL9b = MM.shapes9()
    by_root = {}
    for _t in ALL9b:
        by_root.setdefault(_t[1], []).append(_t)
    mids = {}
    hi_edges = []
    fanout_done = set()
    done_hi = set()
    fq = list(states.keys())
    WH = 6
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
            dB = MM.depth(B, v)
            if dB is None:
                continue
            q = dB // 2
            B2 = S.trace(B, v)[0]
            kb2 = MM.serial(B2)
            if kb2 not in Bt:
                Bt[kb2] = B2
            c9 = MM.core_of_mask(kb2, set(mask))
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
                ka = MM.serial(A2)
                if ka not in At:
                    At[ka] = A2
                k2 = (mi, ka, kb2)
                if k2 not in states:
                    states[k2] = len(states)
                    fq.append(k2)
                emit_low(k2)
                hi_edges.append((mk, states[k2], 0))
        if len(done_hi) % 200000 == 0 and len(done_hi) > 0 and len(done_hi) % 200000 < 5:
            print("  ... p2 states=%d hi=%d t=%.1fs" % (len(states), len(hi_edges), time.time() - t0), flush=True)
    p2closed = (not fq) and (len(low_edges) + len(hi_edges) < CAP_EDGES)
    print("phase2: states=%d mids=%d hi=%d low=%d closed=%s t=%.1fs" % (len(states), len(mids), len(hi_edges), len(low_edges), p2closed, time.time() - t0), flush=True)
    N0 = len(states)
    midmap = {m: N0 + i for i, m in enumerate(mids)}
    E2 = [(u, v, w) for (u, v, w) in low_edges]
    for (u, v, w) in hi_edges:
        a = midmap[u] if isinstance(u, tuple) else u
        b = midmap[v] if isinstance(v, tuple) else v
        E2.append((a, b, w))
    N = N0 + len(mids)
    U = _np.array([u for u, v, w in E2], dtype=_np.int64)
    V = _np.array([v for u, v, w in E2], dtype=_np.int64)
    W = _np.array([w for u, v, w in E2], dtype=_np.int64)
    print("BF: N=%d E=%d" % (N, len(E2)), flush=True)
    t_bf = time.time()
    dist = _np.zeros(N, dtype=_np.int64)
    iters = 0
    stable = False
    for i in range(N):
        prev = dist.copy()
        _np.minimum.at(dist, V, dist[U] + W)
        iters += 1
        if (dist == prev).all():
            stable = True
            break
        if iters % 200 == 0:
            print("  BF %d t=%.1fs" % (iters, time.time() - t_bf), flush=True)
    print("BF: stable=%s iters=%d t=%.1fs" % (stable, iters, time.time() - t_bf), flush=True)
    json.dump({"states": N0, "mids": len(mids), "N": N, "low_edges": len(low_edges),
               "hi_edges": len(hi_edges), "stable": stable, "iters": iters,
               "closed_low": closed_low, "phase2_closed": p2closed,
               "time": round(time.time() - t0, 1)}, open(PDIR + "AFSP_GATE_A_CERT.json", "w"), indent=1)
    if stable:
        _np.save(PDIR + "AFSP_GATE_A_POTENTIAL.npy", dist)
        print("potential saved", flush=True)
