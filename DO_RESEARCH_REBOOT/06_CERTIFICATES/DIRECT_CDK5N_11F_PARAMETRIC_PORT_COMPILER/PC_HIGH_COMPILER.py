# PC_HIGH_COMPILER.py — parametric high-cost midpoint relation (no Cartesian materialization).
# Fiber g=(mu,sig,b',v): S_g(s) and D_g(t) are PREDICATES over state vars; edges s->m (6-q), m->t (0).
# q source-computed (terminal genuine B-depth, C2); mask/signature static; B successor exact.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_LOW_COMPILER import StateVars, state_valid, mubit, popcount5
from PC_B_CONTROLLER import BState, b_valid, muxb, NB, NCORE


class FiberVars:
    def __init__(self, dag, tag):
        d = dag
        self.mu = d.var_int(f'{tag}_fmu', 9)
        self.sig = [d.var_int(f'{tag}_fsg{i}', 9) for i in range(10)]
        # b': B-successor core topology (shared shape vars)
        self.b = BState(d, tag + '_fb')
        self.v = d.var_int(f'{tag}_fv', 4)  # terminal root S-index
        self.q = d.var_int(f'{tag}_fq', 4)  # source-computed q (constrained at use)


def b_equal(d, b1, b2):
    C = [d.EQ(b1.root, b2.root)]
    for a1, a2 in ((b1.kl, b2.kl), (b1.rl, b2.rl), (b1.kr, b2.kr), (b1.rr, b2.rr)):
        for x, y in zip(a1, a2):
            C.append(d.EQ(x, y))
    return d.AND(*C)


def in_S(d, g, s, Hv=None):
    """Source membership: mask/sig match, B-transition compatible (B successor checked at edge)."""
    C = [d.EQ(s.mu, g.mu)]
    for i in range(10):
        C.append(d.EQ(s.sig[i], g.sig[i]))
    return d.AND(*C)


def in_D(d, g, t):
    """Destination membership: mask/sig match, A-root S-index == v (marked terminal root)."""
    C = [d.EQ(t.mu, g.mu)]
    for i in range(10):
        C.append(d.EQ(t.sig[i], g.sig[i]))
    C.append(t.arootS)
    C.append(d.EQ(t.arootI, g.v))
    return d.AND(*C)


def build_high(dag, tag='H', s_ext=None, t_ext=None, g_ext=None):
    """Returns handles with edge predicates:
    E1(s,mid,q): s ordinary, mid fiber-state; E2(mid,t): zero edge. Weights 6-q and 0."""
    d = dag
    g = g_ext if g_ext is not None else FiberVars(d, tag + 'g')
    s = s_ext if s_ext is not None else StateVars(d, tag + 's')
    t = t_ext if t_ext is not None else StateVars(d, tag + 't')
    q = d.var_int(tag + '_q', 4)
    w1 = d.var_int(tag + '_w1', 5, signed=True)
    C = [state_valid(d, s), state_valid(d, t), b_valid(d, g.b)]
    C.append(d.EQ(popcount5(d, g.mu), d.const_int(5, 4)))
    for i in range(10):
        C.append(d.LE(g.sig[i], d.const_int(266, 9)))
    C.append(d.LT(g.v, d.const_int(9, 4)))
    C.append(d.EQ(s.mu, g.mu))
    C.append(d.EQ(t.mu, g.mu))
    for i in range(10):
        C.append(d.EQ(s.sig[i], g.sig[i]))
        C.append(d.EQ(t.sig[i], g.sig[i]))
    # B successor: t.b == g.b (exact)
    C.append(b_equal(d, t.b, g.b))
    # destination root marked v
    C.append(t.arootS)
    C.append(d.EQ(t.arootI, g.v))
    # v marked in mu
    mv = d.const_bool(False)
    for k in range(9):
        mv = d.OR(mv, d.AND(d.EQ(g.v, d.const_int(k, 4)), mubit(d, g.mu, k)))
    C.append(mv)
    # q range + weight 6-q
    C.append(d.LE(q, d.const_int(9, 4)))
    C.append(d.EQ(w1, d.SUB(d.const_int(6, 5), q, 5)))
    root = d.AND(*C)
    return {'root': root, 'g': g, 's': s, 't': t, 'q': q, 'w1': w1, 'dag': d}
