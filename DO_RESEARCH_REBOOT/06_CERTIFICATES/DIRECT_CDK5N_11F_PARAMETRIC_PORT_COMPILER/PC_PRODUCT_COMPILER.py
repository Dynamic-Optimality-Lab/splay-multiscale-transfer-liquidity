# PC_PRODUCT_COMPILER.py — complete shared quantified weighted product G_AF=(V,E,w).
# Canonical var sets: O (ordinary source, 'PO*'), O2 (ordinary target, 'PO2*'), M (midpoint, 'PM*').
# E_low_w(O,O2); E_sm(O,M) = Exists O2 high; E_mt(M,O2) = Exists O high.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import DAG, BOOL, INT
from PC_LOW_COMPILER import StateVars, build_low, state_valid
from PC_HIGH_COMPILER import FiberVars, build_high

WALPHA = [-4, -3, -2, -1, 0, 1, 2, 3, 4, 5, 6]  # finite source-derived weight alphabet


def names_with(d, root, prefix):
    return sorted(v for v in d.vars_in(root) if v.startswith(prefix))


class Product:
    def __init__(self, dag):
        d = dag
        self.d = d
        self.O = StateVars(d, 'PO')
        self.O2 = StateVars(d, 'PO2')
        self.M = FiberVars(d, 'PM')
        self.low = build_low(d, 'PL', s_ext=self.O, t_ext=self.O2)
        self.high = build_high(d, 'PH', s_ext=self.O, t_ext=self.O2, g_ext=self.M)
        o2b = names_with(d, self.high['root'], 'PO2')
        o1b = names_with(d, self.high['root'], 'PO')
        self.E_sm = d.EXISTS(tuple(o2b), self.high['root'])
        self.E_mt = d.EXISTS(tuple(o1b), self.high['root'])
        self.E_low = {}
        for w in WALPHA:
            if -4 <= w <= 4:
                self.E_low[w] = d.AND(self.low['root'],
                                      d.EQ(self.low['w'], d.const_int(w, 5, signed=True)))

    def edge(self, w, sort_s, sort_t):
        """E_w over canonical sets. sort 0=ordinary,1=midpoint. Returns node over (O/O2/M)."""
        d = self.d
        if sort_s == 0 and sort_t == 0:
            if w in self.E_low:
                return self.E_low[w]
            return d.const_bool(False)
        if sort_s == 0 and sort_t == 1:
            # s->m weight 6-q == w  <=>  q == 6-w
            q = self.high['q']
            if 0 <= 6 - w <= 9:
                return d.AND(self.E_sm, d.EQ(q, d.const_int(6 - w, 4)))
            return d.const_bool(False)
        if sort_s == 1 and sort_t == 0:
            if w == 0:
                return self.E_mt
            return d.const_bool(False)
        return d.const_bool(False)  # mid->mid: none
