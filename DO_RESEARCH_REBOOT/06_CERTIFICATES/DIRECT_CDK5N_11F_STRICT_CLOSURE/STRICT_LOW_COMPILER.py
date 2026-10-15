# STRICT_LOW_COMPILER.py — repaired low relation: authoritative alpha-7 + beta + A1/A2/A4/A7/A8.
# Reuses PC interpreters/inventory/B-trace/BState unchanged; new state assembly + repair conjuncts.
# R3: same state tuple (mu,b,alpha,sigma); alpha completed to authoritative content (A6 mandate).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import Witness, NSLOT, W_REF
from PC_ATOM_INVENTORY import Inventory
from PC_ROTATION_INTERPRETER import AState, verify_path_dyn, splay_event, macro_H, mux_ref
from PC_B_CONTROLLER import BState, BTrace, b_valid, verify_bpath, b_splay_event, muxb, NB, NCORE
from PC_LOW_COMPILER import popcount5, mubit
from STRICT_SOURCE_REPAIRS import same_keep_target, root_terminated, no_intermediate_genuine
from STRICT_B_CONTROLLER import BStruct, b_tree_valid
from STRICT_INVENTORY import compat_pred

# alpha positions: 0=root, 1=L, 2=R, 3=LL, 4=LR, 5=RL, 6=RR (authoritative depth-two shadow)
APOS = 7
INORDER = [3, 1, 4, 0, 5, 2, 6]


class StateVars7:
    def __init__(self, dag, tag):
        d = dag
        self.mu = d.var_int(f'{tag}_mu', 9)
        self.b = BState(d, tag + '_b')
        self.ak = [d.var_int(f'{tag}_ak{p}', 2) for p in range(APOS)]
        self.aS = [d.var_bool(f'{tag}_aS{p}') for p in range(APOS)]
        self.aI = [d.var_int(f'{tag}_aI{p}', 4) for p in range(APOS)]
        # beta DERIVED (canonical fringe inorder ordinal; 0 if not fringe): no search vars
        self.ab = []
        for p in range(APOS):
            n = d.const_int(1, 3)
            for q in INORDER:
                if q == p:
                    break
                isf = d.AND(d.EQ(self.ak[q], d.const_int(0, 2)), d.NOT(self.aS[q]))
                n = d.ADD(n, d.ITE(isf, d.const_int(1, 3), d.const_int(0, 3)), 3)
            isfp = d.AND(d.EQ(self.ak[p], d.const_int(0, 2)), d.NOT(self.aS[p]))
            self.ab.append(d.ITE(isfp, n, d.const_int(0, 3)))
        self.sig = [d.var_int(f'{tag}_sg{i}', 9) for i in range(10)]


def state_valid7(d, s):
    C = [d.EQ(popcount5(d, s.mu), d.const_int(5, 4)), b_valid(d, s.b)]
    for i in range(10):
        C.append(d.LE(s.sig[i], d.const_int(266, 9)))
    for p in range(APOS):
        C.append(d.LT(s.ak[p], d.const_int(3, 2)))
        C.append(d.LT(s.aI[p], d.const_int(9, 4)))
    # beta is derived canonical (increasing by construction); no separate constraint needed
    return d.AND(*C)


def shadow7(d, wit, st):
    """Depth-two shadow reader: 7 positions (root, L, R, LL, LR, RL, RR) as (kind, ref).
    Port/empty coarse-prefix children propagate (opaque positions)."""
    r = st.root
    rl, rr = mux_ref(d, st.rl, r), mux_ref(d, st.rr, r)
    kl, kr = mux_ref(d, st.kl, r), mux_ref(d, st.kr, r)
    # explicit: grandchildren (port/empty propagate through coarse prefixes)
    def gk(kk, ref, dkk, dref):
        k = d.ITE(d.EQ(kk, d.const_int(0, 2)), dkk, kk)
        r = d.ITE(d.EQ(kk, d.const_int(0, 2)), dref, ref)
        return k, r
    LLk, LLr = gk(kl, rl, mux_ref(d, st.kl, rl), mux_ref(d, st.rl, rl))
    LRk, LRr = gk(kl, rl, mux_ref(d, st.kr, rl), mux_ref(d, st.rr, rl))
    RLk, RLr = gk(kr, rr, mux_ref(d, st.kl, rr), mux_ref(d, st.rl, rr))
    RRk, RRr = gk(kr, rr, mux_ref(d, st.kr, rr), mux_ref(d, st.rr, rr))
    return {'root': r, 'L': (kl, rl), 'R': (kr, rr),
            'LL': (LLk, LLr), 'LR': (LRk, LRr), 'RL': (RLk, RLr), 'RR': (RRk, RRr)}


def shadow_match7(d, wit, st, s):
    """7-position match (kind/S-label). Beta canonical-derived on both sides (implied by pattern)."""
    sh = shadow7(d, wit, st)
    C = []
    order = ['root', 'L', 'R', 'LL', 'LR', 'RL', 'RR']
    for p, key in enumerate(order):
        if key == 'root':
            C.append(d.EQ(mux_ref(d, wit.isS, sh['root']), s.aS[p]))
            C.append(d.OR(d.NOT(s.aS[p]), d.EQ(mux_ref(d, wit.sidx, sh['root']), s.aI[p])))
            continue
        kk, ref = sh[key]
        C.append(d.EQ(kk, s.ak[p]))
        is_slot = d.EQ(kk, d.const_int(0, 2))
        cs = mux_ref(d, wit.isS, ref)
        ci = mux_ref(d, wit.sidx, ref)
        C.append(d.OR(d.NOT(is_slot), d.EQ(cs, s.aS[p])))
        C.append(d.OR(d.NOT(d.AND(is_slot, cs)), d.EQ(ci, s.aI[p])))
    return d.AND(*C)


def build_slow(dag, tag='SL'):
    """Repaired low relation: PC base + A1 (same KEEP key) + A2 (root-terminated, no-repeat) +
    A4 (B tree validity) + A7 (compat) + A8 (no intermediate genuine). Same xi everywhere."""
    from PC_ROTATION_INTERPRETER import verify_path_dyn, blend
    from PC_B_CONTROLLER import BTrace, b_valid, verify_bpath, b_splay_event, muxb, NB, NCORE
    d = dag
    wit = Witness(d, tag + 'w')
    s = StateVars7(d, tag + 's')
    t = StateVars7(d, tag + 't')
    inv = Inventory(d, wit, tag + 'v', sig_ext=s.sig)
    bt = BTrace(d, tag + 'bt')
    Hv = d.var_int(tag + '_H', 2)
    wv = d.var_int(tag + '_w', 5, signed=True)
    C = [wit.wellformed(), wit.link_both(), wit.child_bound_prop(), inv.attach(), inv.valid()]
    C.append(compat_pred(d, inv))
    C.append(state_valid7(d, s))
    C.append(state_valid7(d, t))
    C.append(d.EQ(s.mu, t.mu))
    for i in range(10):
        C.append(d.EQ(s.sig[i], t.sig[i]))
    st0 = AState(d, wit)
    C.append(shadow_match7(d, wit, st0, s))
    bs = [s.b]
    # root sync (boundaries: marked S roots, A-shadow root == B root)
    C.append(s.aS[0])
    brootS = muxb(d, [d.const_int(1 if i < NCORE else 0, 1) for i in range(NB)], bs[0].root)
    C.append(d.EQ(brootS, d.const_int(1, 1)))
    C.append(d.EQ(s.aI[0], muxb(d, [d.const_int(i if i < NCORE else 0, 4) for i in range(NB)], bs[0].root)))
    # macro legality (<=5 events, present targets, depth<=4, H==Hv<=2, terminal KEEP)
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
    C.append(mux_ref(d, wit.evK, last))
    # exact B replay first (independent of A): bs[0..5], DELETE/KEEP/inactive gating
    bs = [s.b]
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        isK = wit.evK[e]
        C.append(d.OR(d.NOT(active), verify_bpath(d, bs[e], bt, e)))
        eff_del = d.OR(d.NOT(active), d.NOT(isK))
        bs.append(b_splay_event(d, bs[e], bt, e, eff_del))
    # B structural validity at every event boundary (A4); fringe targets need nonempty gaps
    bsts = [BStruct(d, bs[0], tag + 'sb0')]
    C.append(b_tree_valid(d, bs[0], bsts[0], s.sig))
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        isfr = d.AND(active, wit.evK[e], d.NOT(d.LT(bt.bT[e], d.const_int(9, 5))))
        gg = d.SUB(bt.bT[e], d.const_int(9, 5), 5)
        occ = d.const_bool(False)
        for i in range(10):
            occ = d.OR(occ, d.AND(d.EQ(gg, d.const_int(i, 4)), d.NOT(d.EQ(s.sig[i], d.const_int(0, 9)))))
        C.append(d.OR(d.NOT(isfr), occ))
        # intermediate boundary validity (structure-only: intervals stale by design post-rewrite)
        bst = BStruct(d, bs[e + 1], tag + 'sb%d' % (e + 1))
        C.append(d.OR(d.NOT(active), b_tree_valid(d, bs[e + 1], bst, s.sig, intervals=False)))
    # exact A replay + A1 (same key) + A2 (root-terminated, no-repeat) per active event
    st = st0
    sts = [st0]
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        C.append(d.OR(d.NOT(active), verify_path_dyn(d, wit, st, e)))
        C.append(root_terminated(d, wit, bt, st, bs[e], e, active))
        C.append(same_keep_target(d, wit, inv, bt, e, active))
        C.append(no_intermediate_genuine(d, wit, s, bs, last, e, active))
        st = splay_event(d, wit, st, e, active)
        sts.append(st)
    C.append(shadow_match7(d, wit, st, t))
    # terminal q from source B-depth (C2/A8) + genuine (B-change on terminal + marked)
    bd_last = d.const_int(0, 5)
    for e in range(5):
        bd_last = d.ITE(d.EQ(last, d.const_int(e, 3)), bt.bd[e], bd_last)
    C.append(d.LE(bt.q, d.const_int(8, 4)))
    C.append(d.LE(d.ADD(bt.q, bt.q, 5), bd_last))
    C.append(d.LT(bd_last, d.ADD(d.ADD(bt.q, bt.q, 5), d.const_int(2, 5), 5)))
    tt = mux_ref(d, wit.evT, last)
    tisS = mux_ref(d, wit.isS, tt)
    tsi = mux_ref(d, wit.sidx, tt)
    C.append(tisS)
    marked = d.const_bool(False)
    for k in range(9):
        marked = d.OR(marked, d.AND(d.EQ(tsi, d.const_int(k, 4)), mubit(d, s.mu, k)))
    C.append(marked)
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
    # destination B structural validity (A4, both ends)
    bst5 = BStruct(d, t.b, tag + 'sb5')
    C.append(b_tree_valid(d, t.b, bst5, t.sig))
    # weight w = 2H - q
    C.append(d.EQ(wv, d.SUB(d.ADD(Hv, Hv, 3), bt.q, 5)))
    root = d.AND(*C)
    return {'root': root, 'wit': wit, 'inv': inv, 'bt': bt, 's': s, 't': t, 'H': Hv, 'w': wv,
            'dag': d, 'vars': d.vars, 'bs': bs, 'sts': sts, 'last': last}
