# PC_B_CONTROLLER.py — source-exact symbolic 9-core B-controller (+10 gap pseudo-nodes).
# Core nodes 0..8 (S-index = id, rank 2k+1). Gap slots 9..18 (gap g=id-9, rank 2g). NULL=19 (5-bit refs).
# Genuine q from CORE depth only (core ancestors of core targets are all core). Fringe targets
# splay via gap-slot proxy (S-visible effect exact; intra-block prims abstract-invisible).
# DELETE: B identity. q_var constrained (2q<=d<2q+2) per §9 allowance.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT

NCORE, NGAP, NB = 9, 10, 19
NULLB = 19
W_BREF = 5


def crank(nid):
    return 2 * nid + 1 if nid < 9 else 2 * (nid - 9)


class BState:
    def __init__(self, dag, tag):
        d = dag
        self.d = d
        self.kl = [d.var_int(f'{tag}_bkl{i}', 2) for i in range(NB)]
        self.rl = [d.var_int(f'{tag}_brl{i}', W_BREF) for i in range(NB)]
        self.kr = [d.var_int(f'{tag}_bkr{i}', 2) for i in range(NB)]
        self.rr = [d.var_int(f'{tag}_brr{i}', W_BREF) for i in range(NB)]
        self.root = d.var_int(f'{tag}_broot', W_BREF)
        self.lo = [d.var_int(f'{tag}_blo{i}', 5) for i in range(NB)]
        self.hi = [d.var_int(f'{tag}_bhi{i}', 5) for i in range(NB)]

    def _clone(self, kl=None, rl=None, kr=None, rr=None, root=None):
        n = BState.__new__(BState)
        n.d = self.d
        n.kl, n.rl, n.kr, n.rr, n.root = kl or self.kl, rl or self.rl, kr or self.kr, rr or self.rr, root or self.root
        n.lo, n.hi = self.lo, self.hi
        return n


def b_valid(d, bs):
    C = []
    C.append(d.LT(bs.root, d.const_int(NB, W_BREF)))
    # root bounds full; connectivity via parent-chains is enforced by construction refs below;
    # BST rank containment + gap leaves empty + core labels fixed (static)
    for i in range(NB):
        r = crank(i)
        C.append(d.LE(bs.lo[i], d.const_int(r, 5)))
        C.append(d.LE(d.const_int(r, 5), bs.hi[i]))
    # children BST intervals (core nodes; gap slots must have empty children)
    for i in range(NB):
        if i >= NCORE:
            C.append(d.EQ(bs.kl[i], d.const_int(2, 2)))
            C.append(d.EQ(bs.kr[i], d.const_int(2, 2)))
            continue
        r = crank(i)
        for (kch, cch, isL) in ((bs.kl[i], bs.rl[i], True), (bs.kr[i], bs.rr[i], False)):
            for c in range(NB):
                isc = d.AND(d.EQ(kch, d.const_int(0, 2)), d.EQ(cch, d.const_int(c, W_BREF)))
                C.append(d.OR(d.NOT(isc), d.EQ(bs.lo[c], bs.lo[i] if isL else d.const_int(r + 1, 5))))
                C.append(d.OR(d.NOT(isc), d.EQ(bs.hi[c], d.const_int(r - 1, 5) if isL else bs.hi[i])))
    # root spans full range
    C.append(d.EQ(muxb(d, bs.lo, bs.root), d.const_int(0, 5)))
    C.append(d.EQ(muxb(d, bs.hi, bs.root), d.const_int(18, 5)))
    return d.AND(*C)


def muxb(d, vec, idx):
    r = vec[0]
    for i in range(1, len(vec)):
        r = d.ITE(d.EQ(idx, d.const_int(i, W_BREF)), vec[i], r)
    return r


def b_single_rot(d, st, x, p, gp, side_p, side_x, p_was_root):
    xkl, xrl = muxb(d, st.kl, x), muxb(d, st.rl, x)
    xkr, xrr = muxb(d, st.kr, x), muxb(d, st.rr, x)
    right = d.NOT(side_x)
    midk = d.ITE(right, xkr, xkl)
    midr = d.ITE(right, xrr, xrl)
    zk = d.const_int(0, 2)

    def upd(vec, idx, val):
        return [d.ITE(d.EQ(idx, d.const_int(i, W_BREF)), val, vec[i]) for i in range(len(vec))]
    nkl, nrl, nkr, nrr = st.kl, st.rl, st.kr, st.rr
    nkl = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_BREF)), right), midk, nkl[i]) for i in range(NB)]
    nrl = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_BREF)), right), midr, nrl[i]) for i in range(NB)]
    nkr = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_BREF)), d.NOT(right)), midk, nkr[i]) for i in range(NB)]
    nrr = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_BREF)), d.NOT(right)), midr, nrr[i]) for i in range(NB)]
    nkr = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_BREF)), right), zk, nkr[i]) for i in range(NB)]
    nrr = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_BREF)), right), p, nrr[i]) for i in range(NB)]
    nkl = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_BREF)), d.NOT(right)), zk, nkl[i]) for i in range(NB)]
    nrl = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_BREF)), d.NOT(right)), p, nrl[i]) for i in range(NB)]
    gpl = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_BREF)), d.NOT(side_p)), zk, nkl[i]) for i in range(NB)]
    gplr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_BREF)), d.NOT(side_p)), x, nrl[i]) for i in range(NB)]
    gpr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_BREF)), side_p), zk, nkr[i]) for i in range(NB)]
    gprr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_BREF)), side_p), x, nrr[i]) for i in range(NB)]
    return st._clone(kl=gpl, rl=gplr, kr=gpr, rr=gprr, root=d.ITE(p_was_root, x, st.root))


class BTrace:
    """Per-event B access descriptor: target, depth, path, dirs, q (terminal genuine only)."""
    def __init__(self, dag, tag):
        d = dag
        self.bT = [d.var_int(f'{tag}_bT{e}', W_BREF) for e in range(5)]
        self.bd = [d.var_int(f'{tag}_bd{e}', 5) for e in range(5)]
        self.bpath = [[d.var_int(f'{tag}_bp{e}_{k}', W_BREF) for k in range(19)] for e in range(5)]
        self.bdir = [[d.var_bool(f'{tag}_bdir{e}_{k}') for k in range(18)] for e in range(5)]
        self.q = d.var_int(f'{tag}_q', 4)


def b_parent_of(d, bs, c):
    """Mux-search the parent slot of c (NULLB if root/c absent)."""
    par = d.const_int(NULLB, W_BREF)
    for i in range(NB):
        isl = d.AND(d.EQ(bs.kl[i], d.const_int(0, 2)), d.EQ(bs.rl[i], c))
        par = d.ITE(isl, d.const_int(i, W_BREF), par)
        isr = d.AND(d.EQ(bs.kr[i], d.const_int(0, 2)), d.EQ(bs.rr[i], c))
        par = d.ITE(isr, d.const_int(i, W_BREF), par)
    return par


def b_side_of(d, bs, c, par):
    """Side of c under par (False=L)."""
    s = d.const_bool(False)
    for i in range(NB):
        isr = d.AND(d.EQ(par, d.const_int(i, W_BREF)), d.EQ(bs.kr[i], d.const_int(0, 2)), d.EQ(bs.rr[i], c))
        s = d.ITE(isr, d.const_bool(True), s)
    return s


def verify_bpath(d, bs, bt, ev):
    C = []
    C.append(d.EQ(bt.bpath[ev][0], bt.bT[ev]))
    C.append(d.LE(bt.bd[ev], d.const_int(18, 5)))
    trank = d.const_int(0, 5)
    for i in range(NB):
        trank = d.ITE(d.EQ(bt.bT[ev], d.const_int(i, W_BREF)), d.const_int(crank(i), 5), trank)
    for k in range(18):
        active = d.LT(d.const_int(k, 5), bt.bd[ev])
        # parent of path[k] is path[k+1]; side matches; static BST order vs ancestor S-index
        par = b_parent_of(d, bs, bt.bpath[ev][k])
        C.append(d.OR(d.NOT(active), d.EQ(bt.bpath[ev][k + 1], par)))
        side = b_side_of(d, bs, bt.bpath[ev][k], par)
        C.append(d.OR(d.NOT(active), d.EQ(bt.bdir[ev][k], side)))
        # static order: ancestor core S[kk] (rank 2kk+1): side L iff trank < 2kk+1
        ak = d.const_int(0, 4)
        for i in range(NCORE):
            ak = d.ITE(d.EQ(bt.bpath[ev][k + 1], d.const_int(i, W_BREF)), d.const_int(i, 4), ak)
        is_anc_core = d.LT(bt.bpath[ev][k + 1], d.const_int(NCORE, W_BREF))
        shouldL = d.LT(trank, d.ADD(ak, ak, 5))
        shouldL = d.LT(trank, d.ADD(d.ADD(ak, ak, 5), d.const_int(1, 5), 5))
        C.append(d.OR(d.NOT(d.AND(active, is_anc_core)), d.EQ(d.NOT(bt.bdir[ev][k]), shouldL)))
    return d.AND(*C)


def b_blend(d, active, new_st, old_st):
    b = lambda n, o: d.ITE(active, n, o)
    return old_st._clone(kl=[b(n, o) for n, o in zip(new_st.kl, old_st.kl)],
                         rl=[b(n, o) for n, o in zip(new_st.rl, old_st.rl)],
                         kr=[b(n, o) for n, o in zip(new_st.kr, old_st.kr)],
                         rr=[b(n, o) for n, o in zip(new_st.rr, old_st.rr)],
                         root=b(new_st.root, old_st.root))


def b_splay_event(d, bs0, bt, ev, is_delete):
    """Source-original bottom-up B-splay: pairs decoded (zigzig first (p,g); zigzag first (x,p));
    leftover single = zig. DELETE (or inactive via caller flag) = identity."""
    st = bs0
    dd = bt.bd[ev]
    path = bt.bpath[ev]
    dirs = bt.bdir[ev]
    for j in range(9):
        t = 2 * j
        pair_on = d.AND(d.NOT(is_delete), d.LT(d.const_int(t + 2, 5), d.ADD(dd, d.const_int(1, 5), 5)))
        zig_on = d.AND(d.NOT(is_delete), d.EQ(dd, d.const_int(t + 1, 5)))
        same = d.EQ(dirs[min(t, 17)], dirs[min(t + 1, 17)])
        xA = d.ITE(same, path[t + 1], path[0])
        pA = d.ITE(same, path[min(t + 2, 18)], path[t + 1])
        has3 = d.LT(d.const_int(t + 3, 5), d.ADD(dd, d.const_int(1, 5), 5))
        gpA = d.ITE(same, d.ITE(has3, path[min(t + 3, 18)], d.const_int(NULLB, W_BREF)), path[min(t + 2, 18)])
        has_gpA = d.OR(d.AND(same, has3), d.NOT(same))
        sxA = d.ITE(same, dirs[min(t + 1, 17)], dirs[min(t, 17)])
        spA = d.ITE(same, dirs[min(t + 2, 17)], dirs[min(t + 1, 17)])
        pwrA = d.AND(same, d.EQ(d.const_int(t + 2, 5), dd))
        rotA = b_single_rot(d, st, xA, pA, d.ITE(has_gpA, gpA, d.const_int(NULLB, W_BREF)),
                            d.ITE(has_gpA, spA, d.const_bool(False)), sxA, pwrA)
        st = b_blend(d, pair_on, rotA, st)
        gpB = path[min(t + 3, 18)]
        has_gpB = d.LT(d.const_int(t + 3, 5), d.ADD(dd, d.const_int(1, 5), 5))
        sxB = d.ITE(same, dirs[min(t, 17)], dirs[min(t + 1, 17)])
        spB = dirs[min(t + 2, 17)]
        pwrB = d.EQ(d.const_int(t + 2, 5), dd)
        pB = d.ITE(same, path[t + 1], path[min(t + 2, 18)])
        rotB = b_single_rot(d, st, path[0], pB,
                            d.ITE(has_gpB, gpB, d.const_int(NULLB, W_BREF)),
                            d.ITE(has_gpB, spB, d.const_bool(False)), sxB, pwrB)
        st = b_blend(d, pair_on, rotB, st)
        # leftover zig: x is ALWAYS the target path[0]; p is the current root path[dd]
        dd1 = d.SUB(dd, d.const_int(1, 5), 5)
        pmux = path[0]
        for i in range(1, 19):
            pmux = d.ITE(d.EQ(dd, d.const_int(i, 5)), path[i], pmux)
        sxmux = dirs[0]
        for i in range(1, 18):
            sxmux = d.ITE(d.EQ(dd1, d.const_int(i, 5)), dirs[i], sxmux)
        rotZ = b_single_rot(d, st, path[0], pmux, d.const_int(NULLB, W_BREF),
                            d.const_bool(False), sxmux, d.const_bool(True))
        st = b_blend(d, zig_on, rotZ, st)
    end = bs0._clone(kl=[d.ITE(is_delete, o, n) for o, n in zip(bs0.kl, st.kl)],
                     rl=[d.ITE(is_delete, o, n) for o, n in zip(bs0.rl, st.rl)],
                     kr=[d.ITE(is_delete, o, n) for o, n in zip(bs0.kr, st.kr)],
                     rr=[d.ITE(is_delete, o, n) for o, n in zip(bs0.rr, st.rr)],
                     root=d.ITE(is_delete, bs0.root, st.root))
    return end
