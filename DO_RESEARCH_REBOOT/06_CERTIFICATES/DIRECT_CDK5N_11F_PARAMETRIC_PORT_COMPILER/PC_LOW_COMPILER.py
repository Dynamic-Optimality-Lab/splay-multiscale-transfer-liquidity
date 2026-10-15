# PC_LOW_COMPILER.py — one shared parametric low-cost relation L_{H,q}(s,t) = Exists xi [...].
# q from source B-depth (C2); terminal KEEP genuine (B-change + marked target); w = 2H-q.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import Witness, NSLOT, NPORT, W_REF
from PC_ATOM_INVENTORY import Inventory
from PC_ROTATION_INTERPRETER import AState, verify_path_dyn, splay_event, macro_H, shadow2, mux_ref, blend
from PC_B_CONTROLLER import BState, BTrace, b_valid, verify_bpath, b_splay_event, muxb, NB, NCORE, b_blend


class StateVars:
    def __init__(self, dag, tag):
        d = dag
        self.mu = d.var_int(f'{tag}_mu', 9)
        self.b = BState(d, tag + '_b')
        self.arootS = d.var_bool(f'{tag}_arS')
        self.arootI = d.var_int(f'{tag}_arI', 4)
        self.aLk = d.var_int(f'{tag}_aLk', 2)
        self.aLS = d.var_bool(f'{tag}_aLS')
        self.aLI = d.var_int(f'{tag}_aLI', 4)
        self.aRk = d.var_int(f'{tag}_aRk', 2)
        self.aRS = d.var_bool(f'{tag}_aRS')
        self.aRI = d.var_int(f'{tag}_aRI', 4)
        self.sig = [d.var_int(f'{tag}_sg{i}', 9) for i in range(10)]


def mubit(d, mu, k):
    b = d.const_bool(False)
    for v in range(512):
        if (v >> k) & 1:
            b = d.OR(b, d.EQ(mu, d.const_int(v, 9)))
    return b


def popcount5(d, mu):
    tot = d.const_int(0, 4)
    for k in range(9):
        tot = d.ADD(tot, d.ITE(mubit(d, mu, k), d.const_int(1, 4), d.const_int(0, 4)), 4)
    return tot


def state_valid(d, s):
    C = []
    C.append(d.EQ(popcount5(d, s.mu), d.const_int(5, 4)))
    C.append(b_valid(d, s.b))
    for i in range(10):
        C.append(d.LE(s.sig[i], d.const_int(266, 9)))
    C.append(d.LT(s.arootI, d.const_int(9, 4)))
    C.append(d.LT(s.aLI, d.const_int(9, 4)))
    C.append(d.LT(s.aRI, d.const_int(9, 4)))
    C.append(d.LT(s.aLk, d.const_int(3, 2)))
    C.append(d.LT(s.aRk, d.const_int(3, 2)))
    return d.AND(*C)


def shadow_match(d, wit, st, s):
    """Depth-2 shadow of symbolic state == abstract alpha (root + L/R child kind/S-labels)."""
    sh = shadow2(d, wit, st)
    C = []
    (risS, risi) = sh['root']
    C.append(d.EQ(risS, s.arootS))
    C.append(d.OR(d.NOT(risS), d.EQ(risi, s.arootI)))
    (Lk, Lr), (Rk, Rr) = sh['L'], sh['R']
    C.append(d.EQ(Lk, s.aLk))
    C.append(d.EQ(Rk, s.aRk))
    for (kk, ref, cS, cI) in ((Lk, Lr, s.aLS, s.aLI), (Rk, Rr, s.aRS, s.aRI)):
        is_slot = d.EQ(kk, d.const_int(0, 2))
        cs = mux_ref(d, wit.isS, ref)
        ci = mux_ref(d, wit.sidx, ref)
        C.append(d.OR(d.NOT(is_slot), d.EQ(cs, cS)))
        C.append(d.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, cI)))
    return d.AND(*C)


def build_low(dag, tag='L', s_ext=None, t_ext=None):
    d = dag
    wit = Witness(d, tag + 'w')
    s = s_ext if s_ext is not None else StateVars(d, tag + 's')
    t = t_ext if t_ext is not None else StateVars(d, tag + 't')
    inv = Inventory(d, wit, tag + 'v', sig_ext=s.sig)
    bt = BTrace(d, tag + 'bt')
    Hv = d.var_int(tag + '_H', 2)
    wv = d.var_int(tag + '_w', 5, signed=True)
    C = [wit.wellformed(), wit.link_both(), wit.child_bound_prop(), inv.attach(), inv.valid()]
    C.append(state_valid(d, s))
    C.append(state_valid(d, t))
    C.append(d.EQ(s.mu, t.mu))
    for i in range(10):
        C.append(d.EQ(s.sig[i], t.sig[i]))
    # A endpoints
    st0 = AState(d, wit)
    C.append(shadow_match(d, wit, st0, s))
    # B chain starts AT s.b (merged; validity from state_valid(s))
    bs = [s.b]
    # root sync: A-shadow root S-index == B root S-index (boundaries: marked S roots)
    C.append(s.arootS)
    brootS = muxb(d, [d.const_int(1 if i < NCORE else 0, 1) for i in range(NB)], bs[0].root)
    C.append(d.EQ(brootS, d.const_int(1, 1)))
    C.append(d.EQ(s.arootI, muxb(d, [d.const_int(i if i < NCORE else 0, 4) for i in range(NB)], bs[0].root)))
    # macro legality
    C.append(d.LE(wit.nev, d.const_int(5, 3)))
    C.append(d.LT(d.const_int(0, 3), wit.nev))
    last = d.const_int(0, 3)
    for e in range(5):
        last = d.ITE(d.EQ(wit.nev, d.const_int(e + 1, 3)), d.const_int(e, 3), last)
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        pres = d.const_bool(False)
        for i in range(NSLOT):
            pres = d.OR(pres, d.AND(d.EQ(wit.evT[e], d.const_int(i, W_REF)), wit.p[i]))
        C.append(d.OR(d.NOT(active), pres))
        C.append(d.OR(d.NOT(active), d.LE(wit.evd[e], d.const_int(4, 3))))
    C.append(d.EQ(macro_H(d, wit), Hv))
    C.append(d.LE(Hv, d.const_int(2, 2)))
    C.append(mux_ref(d, wit.evK, last))  # terminal KEEP
    # exact A replay over active events
    st = st0
    sts = [st0]
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        C.append(d.OR(d.NOT(active), verify_path_dyn(d, wit, st, e)))
        st = splay_event(d, wit, st, e, active)
        sts.append(st)
    C.append(shadow_match(d, wit, st, t))
    # exact B replay over active events (KEEP splays, DELETE identity, inactive identity)
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        isK = wit.evK[e]
        C.append(d.OR(d.NOT(active), verify_bpath(d, bs[e], bt, e)))
        eff_del = d.OR(d.NOT(active), d.NOT(isK))
        bs.append(b_splay_event(d, bs[e], bt, e, eff_del))
    # terminal q from source B-depth (C2) + genuine (B-change on terminal event + marked target)
    bd_last = d.const_int(0, 5)
    for e in range(5):
        bd_last = d.ITE(d.EQ(last, d.const_int(e, 3)), bt.bd[e], bd_last)
    C.append(d.LE(bt.q, d.const_int(8, 4)))
    C.append(d.LE(d.ADD(bt.q, bt.q, 5), bd_last))
    C.append(d.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5)))
    # terminal target marked: A-slot target S-index bit in mu
    tt = mux_ref(d, wit.evT, last)
    tisS = mux_ref(d, wit.isS, tt)
    tsi = mux_ref(d, wit.sidx, tt)
    C.append(tisS)
    marked = d.const_bool(False)
    for k in range(9):
        marked = d.OR(marked, d.AND(d.EQ(tsi, d.const_int(k, 4)), mubit(d, s.mu, k)))
    C.append(marked)
    # B-change across terminal event (genuine): bs[last] != bs[last+1]
    chg = d.const_bool(False)
    for e in range(5):
        islast = d.EQ(last, d.const_int(e, 3))
        diff = d.const_bool(False)
        for a1, a2 in ((bs[e].kl, bs[e + 1].kl), (bs[e].rl, bs[e + 1].rl), (bs[e].kr, bs[e + 1].kr),
                       (bs[e].rr, bs[e + 1].rr)):
            for x, y in zip(a1, a2):
                diff = d.OR(diff, d.NOT(d.EQ(x, y)))
        diff = d.OR(diff, d.NOT(d.EQ(bs[e].root, bs[e + 1].root)))
        chg = d.OR(chg, d.AND(islast, diff))
    C.append(chg)
    # destination B == t.b
    for a1, a2 in ((t.b.kl, bs[5].kl), (t.b.rl, bs[5].rl), (t.b.kr, bs[5].kr), (t.b.rr, bs[5].rr)):
        for x, y in zip(a1, a2):
            C.append(d.EQ(x, y))
    C.append(d.EQ(t.b.root, bs[5].root))
    # weight w = 2H - q
    C.append(d.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5)))
    root = d.AND(*C)
    return {'root': root, 'wit': wit, 'inv': inv, 'bt': bt, 's': s, 't': t, 'H': Hv, 'w': wv,
            'dag': d, 'vars': d.vars, 'bs': bs, 'sts': sts, 'last': last}
