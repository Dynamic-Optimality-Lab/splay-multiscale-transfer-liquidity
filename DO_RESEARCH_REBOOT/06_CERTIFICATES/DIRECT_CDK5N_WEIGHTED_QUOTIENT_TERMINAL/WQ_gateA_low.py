# WQ Gate-A: all-starts low-only multi-mask product (5A fix: every qualifying (T,r), no first-only break).
import sys, json, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_UFRL_TERMINAL_CLOSURE')
sys.path.insert(0, 'python/independent')
import splay as S
import numpy as np
import UFRL_multimask as MM
from UFRL_multimask import MASKS

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_WEIGHTED_QUOTIENT_TERMINAL/'
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
    Aidx = {s: i for i, s in enumerate(At)}
    Bidx = {s: i for i, s in enumerate(Bt)}
    Alist = [At[s] for s in sorted(Aidx, key=lambda s: Aidx[s])]
    Blist = [Bt[s] for s in sorted(Bidx, key=lambda s: Bidx[s])]
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
                k = (mi, Aidx[st], Bidx[st])
                if k not in states:
                    states[k] = len(states)
                    frontier.append(k)
                    nstarts += 1
                # NO break: every qualifying (T, r) seeds (5A completeness)
    print("starts=%d t=%.1fs" % (nstarts, time.time() - t0), flush=True)
    low_done = set()
    EU = []
    EV = []
    EW = []
    def emit_low(s):
        if s in low_done:
            return
        low_done.add(s)
        mi, ai, bi = s
        mask = MASKS[mi]
        A = Alist[ai]
        B = Blist[bi]
        seen = set()
        for (A2, B2, HH, q, w) in MM.macros_of(A, B, mask):
            ka, kb = MM.serial(A2), MM.serial(B2)
            if ka not in At:
                At[ka] = A2
                Aidx[ka] = len(Alist)
                Alist.append(A2)
            if kb not in Bt:
                Bt[kb] = B2
                Bidx[kb] = len(Blist)
                Blist.append(B2)
            k2 = (mi, Aidx[ka], Bidx[kb])
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
                EU.append(states[s])
                EV.append(states[k2])
                EW.append(w)
    last_rep = 0
    while frontier and len(states) < CAP_STATES and len(EU) < CAP_EDGES:
        emit_low(frontier.pop())
        if len(states) - last_rep >= 500000:
            last_rep = len(states)
            print("  ... states=%d edges=%d t=%.1fs" % (len(states), len(EU), time.time() - t0), flush=True)
    closed = (not frontier) and len(EU) < CAP_EDGES
    print("phase1: states=%d edges=%d closed=%s t=%.1fs" % (len(states), len(EU), closed, time.time() - t0), flush=True)
    U = np.array(EU, dtype=np.int64)
    V = np.array(EV, dtype=np.int64)
    W = np.array(EW, dtype=np.int64)
    N = len(states)
    print("BF-low: N=%d E=%d" % (N, len(EU)), flush=True)
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
    print("BF-low: stable=%s iters=%d t=%.1fs" % (stable, iters, time.time() - t_bf), flush=True)
    neg = int((W < 0).sum())
    json.dump({"starts": nstarts, "states": N, "edges": len(EU), "closed": closed,
               "stable": stable, "iters": iters, "negedges": neg,
               "time": round(time.time() - t0, 1)}, open(PDIR + "WQ_GATE_A_LOW.json", "w"), indent=1)
    if stable:
        np.save(PDIR + "WQ_GATE_A_LOW_POT.npy", dist.astype(np.int32))
        order = sorted(states, key=lambda s: states[s])
        np.save(PDIR + "WQ_GATE_A_LOW_MI.npy", np.array([s[0] for s in order], dtype=np.uint8))
        np.save(PDIR + "WQ_GATE_A_LOW_AI.npy", np.array([s[1] for s in order], dtype=np.uint32))
        np.save(PDIR + "WQ_GATE_A_LOW_BI.npy", np.array([s[2] for s in order], dtype=np.uint32))
        import pickle as _pk
        _pk.dump({"At": sorted(At, key=lambda s: Aidx[s]), "Bt": sorted(Bt, key=lambda s: Bidx[s])},
                 open(PDIR + "WQ_GATE_A_LOW_TREES.pkl", "wb"), protocol=4)
        # negative edges saved explicitly for exhaustive verification (5C)
        m = (W < 0)
        np.save(PDIR + "WQ_GATE_A_LOW_NEGU.npy", U[m].astype(np.int64))
        np.save(PDIR + "WQ_GATE_A_LOW_NEGV.npy", V[m].astype(np.int64))
        np.save(PDIR + "WQ_GATE_A_LOW_NEGW.npy", W[m].astype(np.int64))
        print("saved compact + %d negative edges" % neg, flush=True)
