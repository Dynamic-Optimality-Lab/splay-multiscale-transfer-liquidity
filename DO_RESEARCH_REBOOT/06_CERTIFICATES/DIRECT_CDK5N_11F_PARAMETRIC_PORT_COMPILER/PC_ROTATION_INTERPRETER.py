# PC_ROTATION_INTERPRETER.py — source-original symbolic splay over mixed slot/port refs.
# Path-verified witness paths; _rebuild cases decoded to PRIMITIVE rotations (<=4, C3);
# guarded pointer rewrites move (kind,ref) pairs (ports ride as units).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import NSLOT, NPORT, NULL_REF, NULL_CREF, W_REF, W_CREF


class AState:
    """Symbolic A-tree state: per-slot child (kind,ref) + root. kind 0=slot,1=port,2=empty.
    Slot refs 0..126; port refs = immutable cut-labels s*2+b (0..253); 255 = null."""
    def __init__(self, dag, wit):
        d = dag
        self.d = d
        self.kl = [d.ITE(wit.p[i], wit.kleft[i], d.const_int(2, 2)) for i in range(NSLOT)]
        self.rl = [d.ITE(wit.p[i], wit.cleft[i], d.const_int(NULL_CREF, W_CREF)) for i in range(NSLOT)]
        self.kr = [d.ITE(wit.p[i], wit.kright[i], d.const_int(2, 2)) for i in range(NSLOT)]
        self.rr = [d.ITE(wit.p[i], wit.cright[i], d.const_int(NULL_CREF, W_CREF)) for i in range(NSLOT)]
        self.root = d.const_int(0, W_REF)

    def _clone(self, kl=None, rl=None, kr=None, rr=None, root=None):
        n = AState.__new__(AState)
        n.d = self.d
        n.kl, n.rl, n.kr, n.rr, n.root = (kl or self.kl), (rl or self.rl), (kr or self.kr), (rr or self.rr), (root or self.root)
        return n


def mux_ref(d, vec, idx):
    r = vec[0]
    for i in range(1, len(vec)):
        r = d.ITE(d.EQ(idx, d.const_int(i, W_REF)), vec[i], r)
    return r


def a_parent_of(d, st, c):
    """Parent slot of c in current state (NULL_REF if root/absent). Ports never on verified paths."""
    from PC_STRUCTURAL_WITNESS import NSLOT as _N, W_REF as _W, NULL_REF as _NR
    par = d.const_int(_NR, _W)
    for i in range(_N):
        isl = d.AND(d.EQ(st.kl[i], d.const_int(0, 2)), d.EQ(st.rl[i], c))
        par = d.ITE(isl, d.const_int(i, _W), par)
        isr = d.AND(d.EQ(st.kr[i], d.const_int(0, 2)), d.EQ(st.rr[i], c))
        par = d.ITE(isr, d.const_int(i, _W), par)
    return par


def a_side_of(d, st, c, par):
    from PC_STRUCTURAL_WITNESS import NSLOT as _N, W_REF as _W
    s = d.const_bool(False)
    for i in range(_N):
        isr = d.AND(d.EQ(par, d.const_int(i, _W)), d.EQ(st.kr[i], d.const_int(0, 2)), d.EQ(st.rr[i], c))
        s = d.ITE(isr, d.const_bool(True), s)
    return s


def verify_path_dyn(d, wit, st, ev):
    """Path verified against the CURRENT (evolved) state: adjacency via child refs + static rank order.
    Sound: port-on-path models rejected (parent search finds slots only)."""
    from PC_STRUCTURAL_WITNESS import NSLOT as _N, W_REF as _W
    C = []
    tgt = wit.evT[ev]
    dd = wit.evd[ev]
    C.append(d.EQ(wit.evpath[ev][0], tgt))
    C.append(d.LE(dd, d.const_int(4, 3)))
    tr = d.const_int(0, 8)
    for i in range(_N):
        tr = d.ITE(d.EQ(tgt, d.const_int(i, _W)), wit.rank[i], tr)
    for k in range(4):
        active = d.LT(d.const_int(k, 3), dd)
        pk = wit.evpath[ev][k]
        par = a_parent_of(d, st, pk)
        C.append(d.OR(d.NOT(active), d.EQ(wit.evpath[ev][k + 1], par)))
        side = a_side_of(d, st, pk, par)
        C.append(d.OR(d.NOT(active), d.EQ(wit.evdir[ev][k], side)))
        arank = d.const_int(0, 8)
        for i in range(_N):
            arank = d.ITE(d.EQ(wit.evpath[ev][k + 1], d.const_int(i, _W)), wit.rank[i], arank)
        isL = d.NOT(wit.evdir[ev][k])
        C.append(d.OR(d.NOT(active), d.OR(d.NOT(isL), d.LT(tr, arank))))
        C.append(d.OR(d.NOT(active), d.OR(isL, d.LT(arank, tr))))
    return d.AND(*C)


def verify_path(d, wit, ev):
    """evpath/evdir/evd = true access path of evT (adjacency + sides + BST descent order)."""
    C = []
    tgt = wit.evT[ev]
    dd = wit.evd[ev]
    C.append(d.EQ(wit.evpath[ev][0], tgt))
    C.append(d.LE(dd, d.const_int(4, 3)))
    tr = d.const_int(0, 8)
    for i in range(NSLOT):
        tr = d.ITE(d.EQ(tgt, d.const_int(i, W_REF)), wit.rank[i], tr)
    for k in range(4):
        active = d.LT(d.const_int(k, 3), dd)
        mpar = d.const_int(NULL_REF, W_REF)
        for i in range(NSLOT):
            mpar = d.ITE(d.EQ(wit.evpath[ev][k], d.const_int(i, W_REF)), wit.par[i], mpar)
        mside = d.const_bool(False)
        for i in range(NSLOT):
            mside = d.ITE(d.EQ(wit.evpath[ev][k], d.const_int(i, W_REF)), wit.side[i], mside)
        C.append(d.OR(d.NOT(active), d.EQ(wit.evpath[ev][k + 1], mpar)))
        C.append(d.OR(d.NOT(active), d.EQ(wit.evdir[ev][k], mside)))
        arank = d.const_int(0, 8)
        for i in range(NSLOT):
            arank = d.ITE(d.EQ(wit.evpath[ev][k + 1], d.const_int(i, W_REF)), wit.rank[i], arank)
        isL = d.NOT(wit.evdir[ev][k])
        C.append(d.OR(d.NOT(active), d.OR(d.NOT(isL), d.LT(tr, arank))))
        C.append(d.OR(d.NOT(active), d.OR(isL, d.LT(arank, tr))))
    return d.AND(*C)


def single_rot(d, st, x, p, gp, side_p, side_x, p_was_root):
    """One primitive rotation of x (child of p). side_x=False <=> x left child (right rotation).
    gp adopts x on side_p (side p occupied); if p_was_root, root := x. (kind,ref) pairs move rigidly."""
    xkl, xrl = mux_ref(d, st.kl, x), mux_ref(d, st.rl, x)
    xkr, xrr = mux_ref(d, st.kr, x), mux_ref(d, st.rr, x)
    pkl, prl = mux_ref(d, st.kl, p), mux_ref(d, st.rl, p)
    pkr, prr = mux_ref(d, st.kr, p), mux_ref(d, st.rr, p)
    right = d.NOT(side_x)  # x left child => right rotation
    # middle pair: x.right (right-rot) or x.left (left-rot) becomes p's opposite child
    midk = d.ITE(right, xkr, xkl)
    midr = d.ITE(right, xrr, xrl)

    def upd(vec, idx, val):
        return [d.ITE(d.EQ(idx, d.const_int(i, W_REF)), val, vec[i]) for i in range(len(vec))]

    nkl, nrl, nkr, nrr = st.kl, st.rl, st.kr, st.rr
    # p's opposite child <- middle
    nkl = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_REF)), right), midk, nkl[i]) for i in range(len(nkl))]
    nrl = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_REF)), right), midr, nrl[i]) for i in range(len(nrl))]
    nkr = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_REF)), d.NOT(right)), midk, nkr[i]) for i in range(len(nkr))]
    nrr = [d.ITE(d.AND(d.EQ(p, d.const_int(i, W_REF)), d.NOT(right)), midr, nrr[i]) for i in range(len(nrr))]
    # x's rotation-side child <- p  (x.right <- p for right-rot; x.left <- p for left-rot)
    zk = d.const_int(0, 2)
    nkr = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_REF)), right), zk, nkr[i]) for i in range(len(nkr))]
    nrr = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_REF)), right), p, nrr[i]) for i in range(len(nrr))]
    nkl = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_REF)), d.NOT(right)), zk, nkl[i]) for i in range(len(nkl))]
    nrl = [d.ITE(d.AND(d.EQ(x, d.const_int(i, W_REF)), d.NOT(right)), p, nrl[i]) for i in range(len(nrl))]
    # gp adopts x on side_p  (gp's side_p child pair <- (x-slot))
    xk = d.const_int(0, 2)
    gpl = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_REF)), d.NOT(side_p)), xk, nkl[i]) for i in range(len(nkl))]
    gplr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_REF)), d.NOT(side_p)), x, nrl[i]) for i in range(len(nrl))]
    gpr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_REF)), side_p), xk, nkr[i]) for i in range(len(nkr))]
    gprr = [d.ITE(d.AND(d.NOT(p_was_root), d.EQ(gp, d.const_int(i, W_REF)), side_p), x, nrr[i]) for i in range(len(nrr))]
    newroot = d.ITE(p_was_root, x, st.root)
    return st._clone(kl=gpl, rl=gplr, kr=gpr, rr=gprr, root=newroot)


def blend(d, active, new_st, old_st):
    b = lambda n, o: d.ITE(active, n, o)
    return old_st._clone(kl=[b(n, o) for n, o in zip(new_st.kl, old_st.kl)],
                         rl=[b(n, o) for n, o in zip(new_st.rl, old_st.rl)],
                         kr=[b(n, o) for n, o in zip(new_st.kr, old_st.kr)],
                         rr=[b(n, o) for n, o in zip(new_st.rr, old_st.rr)],
                         root=b(new_st.root, old_st.root))


def splay_event(d, wit, st0, ev, ev_active=None):
    """Source-original bottom-up splay: pairs decoded (zigzig: (p,g) then (x,p); zigzag: (x,p)
    then (x,g)); leftover single level = zig. Total primitives = depth <= 4."""
    from PC_STRUCTURAL_WITNESS import NSLOT as _N, W_REF as _W
    st = st0
    dd = wit.evd[ev]
    path = wit.evpath[ev]
    dirs = wit.evdir[ev]
    for j in range(2):
        t = 2 * j
        pair_on = d.LT(d.const_int(t + 2, 3), d.ADD(dd, d.const_int(1, 3), 3))
        zig_on = d.EQ(dd, d.const_int(t + 1, 3))
        if ev_active is not None:
            pair_on = d.AND(ev_active, pair_on)
            zig_on = d.AND(ev_active, zig_on)
        same = d.EQ(dirs[min(t, 3)], dirs[min(t + 1, 3)])
        # primA wirings (zigzig: x=path[t+1],p=path[t+2]; zigzag: x=path[0],p=path[t+1])
        xA = d.ITE(same, path[t + 1], path[0])
        pA = d.ITE(same, path[min(t + 2, 4)], path[t + 1])
        has3 = d.LT(d.const_int(t + 3, 3), d.ADD(dd, d.const_int(1, 3), 3))
        gpA = d.ITE(same, d.ITE(has3, path[min(t + 3, 4)], d.const_int(NULL_REF, _W)), path[min(t + 2, 4)])
        has_gpA = d.OR(d.AND(same, has3), d.NOT(same))
        sxA = d.ITE(same, dirs[min(t + 1, 3)], dirs[min(t, 3)])
        spA = d.ITE(same, dirs[min(t + 2, 3)], dirs[min(t + 1, 3)])
        pwrA = d.AND(same, d.EQ(d.const_int(t + 2, 3), dd))
        rotA = single_rot(d, st, xA, pA, d.ITE(has_gpA, gpA, d.const_int(NULL_REF, _W)),
                          d.ITE(has_gpA, spA, d.const_bool(False)), sxA, pwrA)
        st = blend(d, pair_on, rotA, st)
        # primB: x is ALWAYS the target path[0]; p zigzig=path[t+1], zigzag=path[t+2]
        gpB = path[min(t + 3, 4)]
        has_gpB = d.LT(d.const_int(t + 3, 3), d.ADD(dd, d.const_int(1, 3), 3))
        sxB = d.ITE(same, dirs[min(t, 3)], dirs[min(t + 1, 3)])
        spB = dirs[min(t + 2, 3)]
        pwrB = d.EQ(d.const_int(t + 2, 3), dd)
        pB = d.ITE(same, path[t + 1], path[min(t + 2, 4)])
        rotB = single_rot(d, st, path[0], pB,
                          d.ITE(has_gpB, gpB, d.const_int(NULL_REF, _W)),
                          d.ITE(has_gpB, spB, d.const_bool(False)), sxB, pwrB)
        st = blend(d, pair_on, rotB, st)
        # leftover zig: x is ALWAYS the target path[0]; p is the current root path[dd]
        dd1 = d.SUB(dd, d.const_int(1, 3), 3)
        pmux = path[0]
        for i in range(1, 5):
            pmux = d.ITE(d.EQ(dd, d.const_int(i, 3)), path[i], pmux)
        sxmux = dirs[0]
        for i in range(1, 4):
            sxmux = d.ITE(d.EQ(dd1, d.const_int(i, 3)), dirs[i], sxmux)
        gpZ = d.const_int(NULL_REF, _W)
        rotZ = single_rot(d, st, path[0], pmux, gpZ, d.const_bool(False),
                          sxmux, d.const_bool(True))
        st = blend(d, zig_on, rotZ, st)
    return st


def event_a(d, wit, ev):
    """a = ceil(d/2) for d in 0..4 (small table)."""
    dd = wit.evd[ev]
    a = d.const_int(0, 3)
    a = d.ITE(d.EQ(dd, d.const_int(1, 3)), d.const_int(1, 3), a)
    a = d.ITE(d.EQ(dd, d.const_int(2, 3)), d.const_int(1, 3), a)
    a = d.ITE(d.EQ(dd, d.const_int(3, 3)), d.const_int(2, 3), a)
    a = d.ITE(d.EQ(dd, d.const_int(4, 3)), d.const_int(2, 3), a)
    return a


def macro_H(d, wit):
    H = d.const_int(0, 3)
    for e in range(5):
        active = d.LT(d.const_int(e, 3), wit.nev)
        H = d.ADD(H, d.ITE(active, event_a(d, wit, e), d.const_int(0, 3)), 3)
    return H


def shadow2(d, wit, st):
    """Depth-2 shadow descriptor: (root label, L/R child (kind, S-or-fringe tag)). Labels via muxed slot data."""
    from PC_STRUCTURAL_WITNESS import NSLOT as _N
    r = st.root
    def lab(slot):
        isS = mux_ref(d, wit.isS, slot)
        si = mux_ref(d, wit.sidx, slot)
        return (isS, si)
    rl, rr = mux_ref(d, st.kl, r), mux_ref(d, st.kr, r)
    rL, rR = mux_ref(d, st.rl, r), mux_ref(d, st.rr, r)
    return {'root': lab(r), 'L': (rl, rL), 'R': (rr, rR)}
