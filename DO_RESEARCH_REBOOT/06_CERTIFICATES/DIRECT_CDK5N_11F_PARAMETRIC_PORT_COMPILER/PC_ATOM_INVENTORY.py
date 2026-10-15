# PC_ATOM_INVENTORY.py — structural ports ((slot,side) identities) + (gap,port) allocation.
# Port (s,side) active ⟺ slot s present with kind=1 child on side (DEFINED, no search vars).
# Bounds per potential port DEFINED from slot bounds. Hidden-S: 9 bools/port, interval-checked.
# Allocation z[i][s][side] (gap x port cells); conservation equalities; exact S-cover.
# Order fidelity: port interiors contain no exposed slots (BST argument); hidden-S exact positions
# + anonymous fillers reconstruct faithfully (atoms derived test-side only).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_STRUCTURAL_WITNESS import NSLOT, W_REF, W_CREF, W_RANK, NULL_CREF

W_CNT, W_SIG = 9, 9


class Inventory:
    def __init__(self, dag, wit, tag, sig_ext=None):
        self.d = dag
        self.w = wit
        self.t = tag
        self.hS = [[[dag.var_bool(f'{tag}_hs{s}_{b}_{k}') for k in range(9)] for b in range(2)] for s in range(NSLOT)]
        self.z = [[[dag.var_int(f'{tag}_z{i}_{s}_{b}', W_CNT) for b in range(2)] for s in range(NSLOT)] for i in range(10)]
        self.sig = sig_ext if sig_ext is not None else [dag.var_int(f'{tag}_sg{i}', W_SIG) for i in range(10)]
        self.hsrank = [[[dag.var_int(f'{tag}_hsr{s}_{b}_{k}', W_RANK) for k in range(9)] for b in range(2)] for s in range(NSLOT)]
        self._sr = None
        self._fr = None

    def fullrank(self, k):
        """Rank of S-index k whether exposed (slot) or hidden (port bill)."""
        if self._fr is None:
            self._fr = {}
        if k not in self._fr:
            d = self.d
            r = self.srank_all()[k]
            for s in range(NSLOT):
                for b in range(2):
                    r = d.ITE(d.AND(self.port_active(s, b), self.hS[s][b][k]), self.hsrank[s][b][k], r)
            self._fr[k] = r
        return self._fr[k]

    def srank_all(self):
        if self._sr is None:
            d, w = self.d, self.w
            sr = []
            for k in range(9):
                r = d.const_int(0, W_RANK)
                for i in range(NSLOT):
                    iss = d.AND(w.p[i], w.isS[i], d.EQ(w.sidx[i], d.const_int(k, 4)))
                    r = d.ITE(iss, w.rank[i], r)
                sr.append(r)
            self._sr = sr
        return self._sr

    def port_active(self, s, b):
        d, w = self.d, self.w
        kch = w.kleft[s] if b == 0 else w.kright[s]
        return d.AND(w.p[s], d.EQ(kch, d.const_int(1, 2)))

    def port_bounds(self, s, b):
        d, w = self.d, self.w
        if b == 0:
            return (w.lo[s], w.rank[s])
        return (d.ADD(w.rank[s], d.const_int(1, W_RANK + 1), W_RANK + 1), w.hi[s])

    def attach(self):
        """Port labels pinned (kind=1 at (s,b) => ref s*2+b: immutable cut identity, unique by
        construction) + hidden-S strictly inside port intervals (bounds defined from slots)."""
        d = self.d
        w = self.w
        sr = self.srank_all()
        C = []
        for s in range(NSLOT):
            for b, kch, cch in ((0, w.kleft[s], w.cleft[s]), (1, w.kright[s], w.cright[s])):
                isport = d.AND(w.p[s], d.EQ(kch, d.const_int(1, 2)))
                C.append(d.OR(d.NOT(isport), d.EQ(cch, d.const_int(s * 2 + b, W_CREF))))
            for b in range(2):
                act = self.port_active(s, b)
                lo, hi = self.port_bounds(s, b)
                for k in range(9):
                    has = self.hS[s][b][k]
                    C.append(d.OR(d.NOT(d.AND(act, has)), d.LE(lo, self.fullrank(k))))
                    C.append(d.OR(d.NOT(d.AND(act, has)), d.LT(self.fullrank(k), hi)))
        # full S-order over true ranks (exposed or hidden)
        for a in range(9):
            for b in range(a + 1, 9):
                C.append(d.LT(self.fullrank(a), self.fullrank(b)))
        return d.AND(*C)

    def _gapof(self, ranknode):
        d = self.d
        g = d.const_int(0, 4)
        for k in range(9):
            g = d.ADD(g, d.ITE(d.LT(self.fullrank(k), ranknode), d.const_int(1, 4), d.const_int(0, 4)), 4)
        return g

    def valid(self):
        d, w = self.d, self.w
        C = []
        for i in range(10):
            C.append(d.LE(self.sig[i], d.const_int(266, W_SIG)))
        # conservation per gap: sum over ports == sig - exposed
        for i in range(10):
            tot = d.const_int(0, 12)
            for s in range(NSLOT):
                for b in range(2):
                    tot = d.ADD(tot, self.z[i][s][b], 12)
            pexp = d.const_int(0, 12)
            for s in range(NSLOT):
                isexp = d.AND(w.p[s], d.NOT(w.isS[s]))
                g = self._gapof(w.rank[s])
                pexp = d.ADD(pexp, d.ITE(d.AND(isexp, d.EQ(g, d.const_int(i, 4))),
                                        d.const_int(1, 12), d.const_int(0, 12)), 12)
            C.append(d.EQ(tot, d.SUB(self.sig[i], pexp, 12)))
        # exact S-cover: each S key exactly once (exposed slot XOR one hidden claim)
        for k in range(9):
            opts = []
            for i in range(NSLOT):
                opts.append(d.AND(w.p[i], w.isS[i], d.EQ(w.sidx[i], d.const_int(k, 4))))
            for s in range(NSLOT):
                for b in range(2):
                    opts.append(d.AND(self.port_active(s, b), self.hS[s][b][k]))
            one = d.const_int(0, 4)
            for o in opts:
                one = d.ADD(one, d.ITE(o, d.const_int(1, 4), d.const_int(0, 4)), 4)
            C.append(d.EQ(one, d.const_int(1, 4)))
        # inactive ports carry nothing
        for s in range(NSLOT):
            for b in range(2):
                act = self.port_active(s, b)
                for k in range(9):
                    C.append(d.OR(act, d.NOT(self.hS[s][b][k])))
                for i in range(10):
                    C.append(d.OR(act, d.EQ(self.z[i][s][b], d.const_int(0, W_CNT))))
        return d.AND(*C)
