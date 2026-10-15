# STRICT_B_CONTROLLER.py — A4 repair: B parent/depth vars + one-parent + connectivity.
# Imports PC BState/topology/rewrites unchanged; ADDS structural validity (encoding-auxiliary vars;
# state space (mu,b,alpha,sigma) unchanged — same trees representable). R3 justification in doc.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_B_CONTROLLER import BState, b_valid, muxb, NB, NCORE, NULLB, W_BREF

TAG = 'SB'


class BStruct:
    """Parent + depth vars over a BState's topology (same var namespace via tag)."""
    def __init__(self, dag, bs, tag):
        d = dag
        self.bpar = [d.var_int(f'{tag}_bpar{i}', W_BREF) for i in range(NB)]
        self.bdep = [d.var_int(f'{tag}_bdep{i}', 5) for i in range(NB)]
        self.bs = bs


def b_tree_valid(d, bs, st, sig=None, intervals=True):
    """Full ordered-rooted-tree validity + gap presence (gap slot exists <=> gap nonempty).
    intervals=False: structure-only (one-parent/counting/depths/root; for replay-derived states
    whose interval annotations are stale by design)."""
    C = [b_valid(d, bs)] if intervals else []
    def present(g):
        if sig is None:
            return d.const_bool(True)
        return d.NOT(d.EQ(sig[g], d.const_int(0, 9)))
    # claimant matrix: claim[i][c] = slot i names c as a node-child
    for c in range(NB):
        # claimant counts: core non-root exactly one; gap: one iff present&non-root, zero otherwise;
        # root (whoever it is) zero.
        isroot = d.EQ(bs.root, d.const_int(c, W_BREF))
        tot = d.const_int(0, 5)
        for i in range(NB):
            isl = d.AND(d.EQ(bs.kl[i], d.const_int(0, 2)), d.EQ(bs.rl[i], d.const_int(c, W_BREF)))
            tot = d.ADD(tot, d.ITE(isl, d.const_int(1, 5), d.const_int(0, 5)), 5)
            isr = d.AND(d.EQ(bs.kr[i], d.const_int(0, 2)), d.EQ(bs.rr[i], d.const_int(c, W_BREF)))
            tot = d.ADD(tot, d.ITE(isr, d.const_int(1, 5), d.const_int(0, 5)), 5)
        if c < 9:
            C.append(d.OR(isroot, d.EQ(tot, d.const_int(1, 5))))
        else:
            pg = present(c - 9)
            C.append(d.OR(isroot, d.OR(d.NOT(pg), d.EQ(tot, d.const_int(1, 5)))))
            C.append(d.OR(d.NOT(d.AND(d.NOT(isroot), d.NOT(pg))), d.EQ(tot, d.const_int(0, 5))))
        C.append(d.OR(d.NOT(isroot), d.EQ(tot, d.const_int(0, 5))))
        # parent consistency: bpar[c] is a real claimant (or NULLB iff root);
        # empty gaps: bpar NULLB, dep 0, no claimant needed.
        C.append(d.OR(d.NOT(isroot), d.EQ(st.bpar[c], d.const_int(NULLB, W_BREF))))
        claimed = d.const_bool(False)
        for i in range(NB):
            isl = d.AND(d.EQ(bs.kl[i], d.const_int(0, 2)), d.EQ(bs.rl[i], d.const_int(c, W_BREF)))
            isr = d.AND(d.EQ(bs.kr[i], d.const_int(0, 2)), d.EQ(bs.rr[i], d.const_int(c, W_BREF)))
            claimed = d.OR(claimed, d.AND(isl, d.EQ(st.bpar[c], d.const_int(i, W_BREF))))
            claimed = d.OR(claimed, d.AND(isr, d.EQ(st.bpar[c], d.const_int(i, W_BREF))))
        if c < 9:
            C.append(d.OR(isroot, claimed))
        else:
            pg = present(c - 9)
            C.append(d.OR(isroot, d.OR(d.NOT(pg), claimed)))
            C.append(d.OR(d.NOT(d.AND(d.NOT(isroot), d.NOT(pg))), d.EQ(st.bpar[c], d.const_int(NULLB, W_BREF))))
            C.append(d.OR(d.NOT(d.AND(d.NOT(isroot), d.NOT(pg))), d.EQ(st.bdep[c], d.const_int(0, 5))))
        # depths: root 0; others par-dep+1 (empty gaps exempt: dep==0 with par NULLB)
        C.append(d.OR(d.NOT(isroot), d.EQ(st.bdep[c], d.const_int(0, 5))))
        pd = d.const_int(0, 5)
        for i in range(NB):
            pd = d.ITE(d.EQ(st.bpar[c], d.const_int(i, W_BREF)), st.bdep[i], pd)
        depok = d.EQ(st.bdep[c], d.ADD(pd, d.const_int(1, 5), 5))
        if c < 9:
            C.append(d.OR(isroot, depok))
        else:
            C.append(d.OR(isroot, d.OR(d.NOT(present(c - 9)), depok)))
    # dep-0 uniqueness is implied (chains decrease to exactly one depth-0 node = root):
    # every chain strictly decreases depth, terminates >=0; only root has dep 0 (others >=1).
    # gap slots hang under core (leaves have no children; parents of gaps must be core).
    for g in range(10):
        gp = st.bpar[9 + g]
        C.append(d.OR(d.EQ(gp, d.const_int(NULLB, W_BREF)), d.LT(gp, d.const_int(NCORE, W_BREF))))
    return d.AND(*C)


def reconstruct_B(env, tag, Sset):
    """Reconstruct source-compatible B-tree from satisfying assignment (A4 test support).
    Returns nested tuple-tree over S keys + gap blocks (balanced over recorded pops if present)."""
    import splay as _S
    sys.path.insert(0, 'python/independent')
    # read core topology
    kids = {}
    for i in range(9):
        kl = env.get(f'{tag}_bkl{i}', 2)
        rl = env.get(f'{tag}_brl{i}', 19)
        kr = env.get(f'{tag}_bkr{i}', 2)
        rr = env.get(f'{tag}_brr{i}', 19)
        kids[i] = ((kl, rl), (kr, rr))
    root = env.get(f'{tag}_broot', 0)
    Ss = sorted(Sset)
    def build(i):
        if i is None or i >= 9:
            return _S.LEAF
        (kl, rl), (kr, rr) = kids[i]
        l = build(rl) if kl == 0 else _S.LEAF
        r = build(rr) if kr == 0 else _S.LEAF
        return _S.node(Ss[i], l, r)
    return build(root)
