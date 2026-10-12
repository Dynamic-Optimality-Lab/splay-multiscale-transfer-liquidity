# Per-mask reachable-size probe (concrete 9-key): odd + 3 other masks.
import sys, time
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_COST_CONE_TERMINAL')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_N_COMP_CYCLIC_RESIDUAL_AUDIT')
sys.path.insert(0, 'python/independent')
from CRA_pointer_tuple_replay import core_of
import splay as S
import CC_proto as P

def run_mask(mask, cap=40000):
    P.M = tuple(mask)
    t0 = P.T0tree()
    r = mask[len(mask) // 2]
    A0 = S.trace(t0, r)[0]
    start = (P.serial(A0), P.serial(A0))
    states = {start: 0}
    At = {start[0]: A0}
    Bt = {start[1]: A0}
    frontier = [start]
    nmac = 0
    while frontier and len(states) < cap:
        s = frontier.pop()
        A = At[s[0]]
        B = Bt[s[1]]
        for (A2, B2, HH, q, w, wd) in P.macros_of(A, B):
            nmac += 1
            ka, kb = P.serial(A2), P.serial(B2)
            if ka not in At:
                At[ka] = A2
            if kb not in Bt:
                Bt[kb] = B2
            k2 = (ka, kb)
            if k2 not in states:
                if A2[0] == "leaf" or B2[0] == "leaf" or A2[1] != B2[1]:
                    continue
                c9 = core_of(kb, set(mask))
                if c9 is None or len(c9) != 9:
                    continue
                states[k2] = len(states)
                frontier.append(k2)
    return len(states), nmac, bool(frontier)

for mask in ((1, 3, 5, 7, 9), (1, 2, 3, 4, 5), (5, 6, 7, 8, 9), (1, 2, 8, 9, 5)):
    t = time.time()
    n, m, open_ = run_mask(mask)
    print("mask=%s states=%d macros=%d open=%s t=%.1fs" % (mask, n, m, open_, time.time() - t), flush=True)
