# PC_SYMBOLIC_OPERATORS.py — production symbolic Pre/Post/MinPre + 14-function API.
# Canonical sets: O/O2 ordinary, M midpoint. Target sets X = {0: pred over O2 (or None),
# 1: pred over M (or None)}. Nesting via DAG.subst renaming (O<->O2, capture-safe).
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_STRICT_CLOSURE')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_CLOSED_WALK_CORE_RESCUE')
from PC_TYPED_DAG import DAG, BOOL, INT
from CW_PRODUCT_COMPILER import Product, WALPHA
from STRICT_LOW_COMPILER import state_valid7 as state_valid


def _o2names(d, root):
    return sorted(v for v in d.vars_in(root) if v.startswith('QO2'))


def _onames(d, root):
    return sorted(v for v in d.vars_in(root) if v.startswith('QO') and not v.startswith('QO2'))


def _mnames(d, root):
    return sorted(v for v in d.vars_in(root) if v.startswith('QM'))


class Operators:
    def __init__(self, prod):
        self.P = prod
        self.d = prod.d
        d = prod.d
        self.U_O = state_valid(d, prod.O)
        self.U_O2 = state_valid(d, prod.O2)
        self.U_M = self._mid_universe()

    def _mid_universe(self):
        from PC_LOW_COMPILER import popcount5, mubit
        from PC_B_CONTROLLER import b_valid
        d, M = self.d, self.P.M
        C = [d.EQ(popcount5(d, M.mu), d.const_int(5, 4)), b_valid(d, M.b)]
        for i in range(10):
            C.append(d.LE(M.sig[i], d.const_int(266, 9)))
        C.append(d.LT(M.v, d.const_int(9, 4)))
        return d.AND(*C)

    # ---- base predicates ----
    def valid_state(self, S):
        return self.U_O if S == 0 else self.U_M

    def low_edge(self, w):
        return self.P.E_low.get(w, self.d.const_bool(False))

    def high_source(self):
        d = self.d
        mn = _mnames(d, self.P.E_sm)
        return d.EXISTS(tuple(mn), self.P.E_sm)

    def high_destination(self):
        d = self.d
        mn = _mnames(d, self.P.E_mt)
        return d.EXISTS(tuple(mn), self.P.E_mt)

    # ---- quantified operators (results over O for sort 0, over M for sort 1) ----
    # Convention: pre takes X over TARGET side (O2 and/or M); post takes X over SOURCE side (O and/or M).
    def pre(self, X, w):
        d = self.d
        r0 = None
        if X.get(0) is not None:
            e = self.P.edge(w, 0, 0)
            o2n = _o2names(d, d.AND(e, X[0]))
            r0 = d.EXISTS(tuple(o2n), d.AND(e, X[0]))
        if X.get(1) is not None and w != 0:
            e = self.P.edge(w, 0, 1)
            mn = _mnames(d, d.AND(e, X[1]))
            r1 = d.EXISTS(tuple(mn), d.AND(e, X[1]))
            r0 = r1 if r0 is None else d.OR(r0, r1)
        return {0: r0 if r0 is not None else d.const_bool(False), 1: None}

    def pre_mid(self, X, w):
        d = self.d
        if w != 0 or X.get(0) is None:
            return {0: None, 1: d.const_bool(False)}
        e = self.P.edge(0, 1, 0)
        o2n = _o2names(d, d.AND(e, X[0]))
        return {0: None, 1: d.EXISTS(tuple(o2n), d.AND(e, X[0]))}

    def post(self, X, w):
        d = self.d
        r0, r1 = None, None
        if X.get(0) is not None:
            e = self.P.edge(w, 0, 0)
            on = _onames(d, d.AND(e, X[0]))
            r0 = d.EXISTS(tuple(on), d.AND(e, X[0]))
            if w != 0:
                es = self.P.edge(w, 0, 1)
                on2 = _onames(d, d.AND(es, X[0]))
                r1 = d.EXISTS(tuple(on2), d.AND(es, X[0]))
        if X.get(1) is not None and w == 0:
            e = self.P.edge(0, 1, 0)
            mn = _mnames(d, d.AND(e, X[1]))
            rm = d.EXISTS(tuple(mn), d.AND(e, X[1]))
            r0 = rm if r0 is None else d.OR(r0, rm)
        return {0: r0 if r0 is not None else d.const_bool(False),
                1: r1 if r1 is not None else d.const_bool(False)}

    def minpre(self, X, w):
        d = self.d
        base = self.pre(X, w)
        lower = None
        for a in WALPHA:
            if a < w:
                pa = self.pre(X, a)
                if pa.get(0) is not None and not self._is_false(pa[0]):
                    lower = pa[0] if lower is None else d.OR(lower, pa[0])
        if lower is None:
            return base
        r0 = base.get(0)
        return {0: d.AND(r0, d.NOT(lower)) if r0 is not None else d.const_bool(False), 1: None}

    def _is_false(self, n):
        k, t, a, e = self.d.nodes[n]
        return k == 'const' and t == BOOL and not e

    # ---- boolean algebra over predicate pairs ----
    def union(self, X, Y):
        return {s: self._bop(self.d.OR, X.get(s), Y.get(s)) for s in (0, 1)}

    def intersection(self, X, Y):
        return {s: self._bop(self.d.AND, X.get(s), Y.get(s)) for s in (0, 1)}

    def complement(self, X):
        d = self.d
        return {0: d.AND(self.U_O, d.NOT(X[0])) if X.get(0) is not None else d.const_bool(False),
                1: d.AND(self.U_M, d.NOT(X[1])) if X.get(1) is not None else d.const_bool(False)}

    def _bop(self, op, a, b):
        if a is None:
            return b
        if b is None:
            return a
        return op(a, b)

    def equivalent(self, X, Y):
        d = self.d
        C = []
        for s, U in ((0, self.U_O), (1, self.U_M)):
            xa, ya = X.get(s), Y.get(s)
            if xa is None and ya is None:
                continue
            xa = xa if xa is not None else d.const_bool(False)
            ya = ya if ya is not None else d.const_bool(False)
            C.append(d.OR(d.AND(xa, ya), d.AND(d.NOT(xa), d.NOT(ya))))
        return d.AND(*C) if C else d.const_bool(True)

    def is_empty(self, X, solver=None):
        from CW_QUANTIFIED_BACKEND import QSolver, SAT, UNSAT, UNKNOWN
        d = self.d
        parts = []
        for s in (0, 1):
            if X.get(s) is not None:
                parts.append(X[s])
        if not parts:
            return True
        sv = solver or QSolver(d)
        r, _, _ = sv.solve(d.OR(*parts) if len(parts) > 1 else parts[0])
        if r == UNSAT:
            return True
        if r == SAT:
            return False
        return UNKNOWN

    def extract_witness(self, X, solver=None):
        from CW_QUANTIFIED_BACKEND import QSolver, SAT
        d = self.d
        parts = [X[s] for s in (0, 1) if X.get(s) is not None]
        if not parts:
            return None
        sv = solver or QSolver(d)
        r, env, _ = sv.solve(d.OR(*parts) if len(parts) > 1 else parts[0])
        return env if r == SAT else None

    def extract_edge_witness(self, w, ss, st, solver=None):
        from CW_QUANTIFIED_BACKEND import QSolver, SAT
        d = self.d
        e = self.P.edge(w, ss, st)
        sv = solver or QSolver(d)
        r, env, _ = sv.solve(e)
        return env if r == SAT else None

    # ---- renaming helpers for nesting (capture-safe: canonical O<->O2 maps) ----
    def rename_O_to_O2(self, node):
        direct = {}
        for v in self.d.vars_in(node):
            if v.startswith('QO') and not v.startswith('QO2'):
                direct[v] = 'QO2' + v[2:]
        return self.d.subst(node, direct)

    def rename_O2_to_O(self, node):
        direct = {}
        for v in self.d.vars_in(node):
            if v.startswith('QO2'):
                direct[v] = 'QO' + v[3:]
        return self.d.subst(node, direct)
