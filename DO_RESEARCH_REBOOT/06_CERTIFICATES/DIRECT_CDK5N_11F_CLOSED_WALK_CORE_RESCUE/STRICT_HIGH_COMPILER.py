# STRICT_HIGH_COMPILER.py — Gate F: high-cost midpoint relation with WITNESSED q.
# Fiber g=(mu,sig,b',v) + terminal genuine B-trace (path-verified, depth, genuine chg, marked)
# + source s + destination t (STRICT states) + weights 6-q / 0. No Cartesian materialization.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_B_CONTROLLER import BState, BTrace, b_valid, verify_bpath, b_splay_event, muxb, NB, NCORE
from STRICT_LOW_COMPILER import StateVars7, state_valid7, popcount5, mubit
from STRICT_B_CONTROLLER import BStruct, b_tree_valid
from STRICT_B_CONTROLLER import BStruct, b_tree_valid


class FiberVars7:
    def __init__(self, dag, tag):
        d = dag
        self.mu = d.var_int(f'{tag}_fmu', 9)
        self.sig = [d.var_int(f'{tag}_fsg{i}', 9) for i in range(10)]
        self.b = BState(d, tag + '_fb')
        self.v = d.var_int(f'{tag}_fv', 4)


def b_equal(d, b1, b2):
    C = [d.EQ(b1.root, b2.root)]
    for a1, a2 in ((b1.kl, b2.kl), (b1.rl, b2.rl), (b1.kr, b2.kr), (b1.rr, b2.rr)):
        for x, y in zip(a1, a2):
            C.append(d.EQ(x, y))
    return d.AND(*C)


def build_shigh(dag, tag='SH', s_ext=None, t_ext=None, g_ext=None):
    d = dag
    g = g_ext if g_ext is not None else FiberVars7(d, tag + 'g')
    s = s_ext if s_ext is not None else StateVars7(d, tag + 's')
    t = t_ext if t_ext is not None else StateVars7(d, tag + 't')
    bt = BTrace(d, tag + 'bt')
    q = d.var_int(tag + '_q', 4)
    w1 = d.var_int(tag + '_w1', 5, signed=True)
    C = [state_valid7(d, s), state_valid7(d, t), b_valid(d, g.b)]
    sbS = BStruct(d, s.b, tag + 'sbs')
    sbT = BStruct(d, t.b, tag + 'sbt')
    sbG = BStruct(d, g.b, tag + 'sbg')
    C.append(b_tree_valid(d, s.b, sbS, s.sig))
    C.append(b_tree_valid(d, t.b, sbT, t.sig))
    C.append(b_tree_valid(d, g.b, sbG, g.sig))
    C.append(d.EQ(popcount5(d, g.mu), d.const_int(5, 4)))
    for i in range(10):
        C.append(d.LE(g.sig[i], d.const_int(266, 9)))
    C.append(d.LT(g.v, d.const_int(9, 4)))
    # static mask/signature + exact B successor + marked terminal root
    C.append(d.EQ(s.mu, g.mu))
    C.append(d.EQ(t.mu, g.mu))
    for i in range(10):
        C.append(d.EQ(s.sig[i], g.sig[i]))
        C.append(d.EQ(t.sig[i], g.sig[i]))
    C.append(b_equal(d, t.b, g.b))
    C.append(t.aS[0])
    C.append(d.EQ(t.aI[0], g.v))
    mv = d.const_bool(False)
    for k in range(9):
        mv = d.OR(mv, d.AND(d.EQ(g.v, d.const_int(k, 4)), mubit(d, g.mu, k)))
    C.append(mv)
    # WITNESSED terminal genuine B transition (source s.b --terminal KEEP--> g.b, q constrained)
    # witness: single B-trace (target, path, depth) + genuine change + marked target
    C.append(verify_bpath(d, s.b, bt, 0))
    bs1 = b_splay_event(d, s.b, bt, 0, d.const_bool(False))
    # destination of witness splay == g.b (exact B successor)
    C.append(b_equal(d, bs1, g.b))
    # genuine: witnessed transition changes B + target marked in mu
    diff = d.const_bool(False)
    for a1, a2 in ((s.b.kl, bs1.kl), (s.b.rl, bs1.rl), (s.b.kr, bs1.kr), (s.b.rr, bs1.rr)):
        for x, y in zip(a1, a2):
            diff = d.OR(diff, d.NOT(d.EQ(x, y)))
    diff = d.OR(diff, d.NOT(d.EQ(s.b.root, bs1.root)))
    C.append(diff)
    tt = bt.bT[0]
    # target marked: core (S-index bit) — fringe terminal KEEPs are nongenuine (no q needed... but
    # high macros end at GENUINE marked KEEPs; enforce core+marked)
    C.append(d.LT(tt, d.const_int(9, 5)))
    mv2 = d.const_bool(False)
    for k in range(9):
        mv2 = d.OR(mv2, d.AND(d.EQ(tt, d.const_int(k, 5)), mubit(d, s.mu, k)))
    C.append(mv2)
    # q from witnessed depth
    C.append(d.LE(q, d.const_int(9, 4)))
    C.append(d.LE(d.ADD(q, q, 5), bt.bd[0]))
    C.append(d.LT(bt.bd[0], d.ADD(d.ADD(q, q, 5), d.const_int(2, 5), 5)))
    C.append(d.EQ(w1, d.SUB(d.const_int(6, 5), q, 5)))
    root = d.AND(*C)
    return {'root': root, 'g': g, 's': s, 't': t, 'q': q, 'w1': w1, 'dag': d}
