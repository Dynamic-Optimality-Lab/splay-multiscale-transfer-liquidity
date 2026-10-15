# PC_STRUCTURAL_WITNESS.py — symbolic prefix/ports/word/path variables + well-formedness.
# Slots 0..126 (NULL_REF=127). Ranks 0..135 (bound sentinel 136). Depths 0..6.
# Ports 0..127, atoms 0..136. Key lemma: witnesses use SMALL prefixes (paths+shadow+attachments);
# ports absorb all other structure (coarsening sound by commutation at shallower cuts).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT

NSLOT, NPORT, NATOM = 127, 128, 137
NULL_REF, RANK_INF = 127, 136
NULL_CREF = 255  # 8-bit child-ref null
W_REF, W_CREF, W_RANK, W_DEPTH, W_SIDX = 7, 8, 8, 3, 4


class Witness:
    def __init__(self, dag, tag):
        self.d = dag
        self.t = tag
        self.p = []      # present bits
        self.par = []    # parent refs
        self.side = []   # side bits (0=L,1=R)
        self.dep = []    # depths
        self.isS = []    # S bits
        self.sidx = []   # S indices
        self.rank = []   # V-ranks
        self.lo = []     # interval bounds
        self.hi = []
        self.kleft = []  # child kind bits (0=slot,1=port,2=empty)
        self.cleft = []
        self.kright = []
        self.cright = []
        for i in range(NSLOT):
            P = f'{tag}_p{i}'
            self.p.append(dag.var_bool(P))
            self.par.append(dag.var_int(f'{tag}_par{i}', W_REF))
            self.side.append(dag.var_bool(f'{tag}_side{i}'))
            self.dep.append(dag.var_int(f'{tag}_dep{i}', W_DEPTH))
            self.isS.append(dag.var_bool(f'{tag}_isS{i}'))
            self.sidx.append(dag.var_int(f'{tag}_sidx{i}', W_SIDX))
            self.rank.append(dag.var_int(f'{tag}_rank{i}', W_RANK))
            self.lo.append(dag.var_int(f'{tag}_lo{i}', W_RANK))
            self.hi.append(dag.var_int(f'{tag}_hi{i}', W_RANK))
            self.kleft.append(dag.var_int(f'{tag}_kl{i}', 2))
            self.cleft.append(dag.var_int(f'{tag}_cl{i}', W_CREF))
            self.kright.append(dag.var_int(f'{tag}_kr{i}', 2))
            self.cright.append(dag.var_int(f'{tag}_cr{i}', W_CREF))
        # word: <=5 events
        self.nev = dag.var_int(f'{tag}_nev', 3)
        self.evK = [dag.var_bool(f'{tag}_eK{e}') for e in range(5)]
        self.evT = [dag.var_int(f'{tag}_eT{e}', W_REF) for e in range(5)]  # target slot
        # rotation paths: per event, depth + ancestor slot list (d+1 refs, verified)
        self.evd = [dag.var_int(f'{tag}_ed{e}', W_DEPTH) for e in range(5)]
        self.evpath = [[dag.var_int(f'{tag}_ep{e}_{k}', W_REF) for k in range(5)] for e in range(5)]
        self.evdir = [[dag.var_bool(f'{tag}_edir{e}_{k}') for k in range(4)] for e in range(5)]

    def wellformed(self):
        d = self.d
        C = []
        C.append(self.p[0])  # root present
        C.append(d.EQ(self.dep[0], d.const_int(0, W_DEPTH)))
        for i in range(NSLOT):
            # absent slots: unconstrained (no requirements)
            pre = self.p[i]
            if i == 0:
                C.append(d.OR(d.NOT(pre), d.EQ(self.par[i], d.const_int(0, W_REF))))
            else:
                # present => parent present, depth = parent+1, depth<=6, parent link consistent
                need = []
                for j in range(NSLOT):
                    ispar = d.AND(pre, d.EQ(self.par[i], d.const_int(j, W_REF)))
                    need.append(d.OR(d.NOT(ispar), self.p[j]))
                    need.append(d.OR(d.NOT(ispar),
                                    d.EQ(self.dep[i], d.ADD(self.dep[j], d.const_int(1, W_DEPTH + 1), W_DEPTH + 1))))
                C.append(d.OR(d.NOT(pre), d.AND(*need)))
                C.append(d.OR(d.NOT(pre), d.LT(self.dep[i], d.const_int(7, W_DEPTH))))
            # intervals contain rank
            C.append(d.OR(d.NOT(pre), d.LE(self.lo[i], self.rank[i])))
            C.append(d.OR(d.NOT(pre), d.LT(self.rank[i], self.hi[i])))
            C.append(d.OR(d.NOT(pre), d.LT(self.rank[i], d.const_int(RANK_INF, W_RANK))))
            C.append(d.OR(d.NOT(pre), d.LE(self.lo[i], d.const_int(RANK_INF, W_RANK))))
            C.append(d.OR(d.NOT(pre), d.LE(self.hi[i], d.const_int(RANK_INF + 1, W_RANK + 1) if False else d.const_int(RANK_INF, W_RANK))))
            # S slots: sidx<9; fringe: nothing extra
            C.append(d.OR(d.NOT(d.AND(pre, self.isS[i])), d.LT(self.sidx[i], d.const_int(9, W_SIDX))))
            # root bounds
            if i == 0:
                C.append(d.OR(d.NOT(pre), d.EQ(self.lo[i], d.const_int(0, W_RANK))))
                C.append(d.OR(d.NOT(pre), d.EQ(self.hi[i], d.const_int(RANK_INF, W_RANK))))
            # children kinds valid (0,1,2)
            C.append(d.OR(d.NOT(pre), d.LT(self.kleft[i], d.const_int(3, 2))))
            C.append(d.OR(d.NOT(pre), d.LT(self.kright[i], d.const_int(3, 2))))
        # sibling uniqueness: same present parent => different sides
        for i in range(1, NSLOT):
            for j in range(i + 1, NSLOT):
                same = d.AND(self.p[i], self.p[j], d.EQ(self.par[i], self.par[j]))
                C.append(d.OR(d.NOT(same), d.NOT(d.EQ(self.side[i], self.side[j]))))
        # S-index uniqueness among present S slots
        for i in range(NSLOT):
            for j in range(i + 1, NSLOT):
                both = d.AND(self.p[i], self.p[j], self.isS[i], self.isS[j], d.EQ(self.sidx[i], self.sidx[j]))
                C.append(d.NOT(both))
        # rank all-different among present slots
        for i in range(NSLOT):
            for j in range(i + 1, NSLOT):
                both = d.AND(self.p[i], self.p[j], d.EQ(self.rank[i], self.rank[j]))
                C.append(d.NOT(both))
        # S relative order: sib order respected by ranks
        for i in range(NSLOT):
            for j in range(NSLOT):
                if i == j:
                    continue
                cond = d.AND(self.p[i], self.p[j], self.isS[i], self.isS[j], d.LT(self.sidx[i], self.sidx[j]))
                C.append(d.OR(d.NOT(cond), d.LT(self.rank[i], self.rank[j])))
        return d.AND(*C)

    def link_both(self):
        """Reverse direction: present non-root slot is some slot's child (no floating slots)."""
        d = self.d
        C = []
        for c in range(1, NSLOT):
            opts = []
            for i in range(NSLOT):
                if i == c:
                    continue
                isL = d.AND(d.EQ(self.par[c], d.const_int(i, W_REF)),
                            d.EQ(self.side[c], d.const_bool(False)))
                opts.append(d.AND(isL, d.EQ(self.kleft[i], d.const_int(0, 2)),
                                      d.EQ(self.cleft[i], d.const_int(c, W_REF))))
                isR = d.AND(d.EQ(self.par[c], d.const_int(i, W_REF)),
                            d.EQ(self.side[c], d.const_bool(True)))
                opts.append(d.AND(isR, d.EQ(self.kright[i], d.const_int(0, 2)),
                                       d.EQ(self.cright[i], d.const_int(c, W_REF))))
            C.append(d.OR(d.NOT(self.p[c]), d.OR(*opts)))
        return d.AND(*C)

    def child_bound_prop(self):
        """BST interval propagation parent->child for slot children (ports checked at attachment)."""
        d = self.d
        C = []
        for i in range(NSLOT):
            for side, kch, cch in ((0, self.kleft[i], self.cleft[i]), (1, self.kright[i], self.cright[i])):
                for c in range(NSLOT):
                    isc = d.AND(self.p[i], d.EQ(kch, d.const_int(0, 2)), d.EQ(cch, d.const_int(c, W_REF)))
                    C.append(d.OR(d.NOT(isc), self.p[c]))
                    C.append(d.OR(d.NOT(isc), d.EQ(self.par[c], d.const_int(i, W_REF))))
                    C.append(d.OR(d.NOT(isc), d.EQ(self.side[c], d.const_bool(bool(side)))))
                    if side == 0:
                        C.append(d.OR(d.NOT(isc), d.EQ(self.hi[c], self.rank[i])))
                        C.append(d.OR(d.NOT(isc), d.EQ(self.lo[c], self.lo[i])))
                    else:
                        C.append(d.OR(d.NOT(isc), d.EQ(self.lo[c], d.ADD(self.rank[i], d.const_int(1, W_RANK + 1), W_RANK + 1))))
                        C.append(d.OR(d.NOT(isc), d.EQ(self.hi[c], self.hi[i])))
        return d.AND(*C)
