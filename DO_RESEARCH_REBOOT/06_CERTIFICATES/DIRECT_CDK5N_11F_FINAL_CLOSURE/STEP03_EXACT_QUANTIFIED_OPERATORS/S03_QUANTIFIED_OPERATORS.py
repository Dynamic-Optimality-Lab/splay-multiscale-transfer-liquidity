# S03_QUANTIFIED_OPERATORS.py — full two-sort Pre/Post/MinPre + 15-function algebra.
# Backend-agnostic over sort predicates (production QO/QO2/QM or small-graph names).
# Two interfaces: symbolic construction (exact quantified predicates) + executable
# decision (injected decide() callable). Production execution routes grounded
# membership through the certified Step-02 engine / normalized Tier-1 path
# (Gate-F procedure, proved equivalent); small graphs execute fully through Z3.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
from PC_TYPED_DAG import BOOL
import S03_TYPED_STATE_SETS as TS

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'


class QOps:
    def __init__(self, d, is_src, is_dst, is_mid, EOO, EOM, EMO, U_O, U_M,
                 decide=None, rename_s2d=None, rename_d2s=None, alphabet=None,
                 U_O2=None):
        self.d = d
        self.is_src = is_src
        self.is_dst = is_dst
        self.is_mid = is_mid
        self.EOO = EOO
        self.EOM = EOM
        self.EMO = EMO
        self.U_O = U_O
        self.U_M = U_M
        # destination-side ordinary universe (post results live in dst namespace;
        # default: U_O — backends with distinct dst namespaces must supply U_O2)
        self.U_O2 = U_O2 if U_O2 is not None else U_O
        self.decide = decide  # (root, pins, timeout) -> (status, model-or-None, reason)
        self.rename_s2d = rename_s2d or {}
        self.rename_d2s = rename_d2s or {}
        self.alphabet = alphabet or []

    def _bind(self, root, keep_fn):
        d = self.d
        vs = sorted(v for v in d.vars_in(root) if not keep_fn(v))
        # only bind names that actually occur bound-or-free inside (binder-safe:
        # normalization downstream assigns ownership; binding free-only names here
        # would be vacuous but harmless -- keep it exact: bind all non-kept)
        if not vs:
            return root
        return d.EXISTS(tuple(vs), root)

    def _o2names(self, root):
        return set(v for v in self.d.vars_in(root) if self.is_dst(v))

    def _mnames(self, root):
        return set(v for v in self.d.vars_in(root) if self.is_mid(v))

    def _onames(self, root):
        return set(v for v in self.d.vars_in(root) if self.is_src(v))

    def _side_false(self, x):
        return TS.is_side_empty_const(self.d, x)

    # ---- symbolic construction (exact quantified predicates) ----
    def low_edge(self, w):
        return self.EOO(w)

    def high_source(self):
        return self.EOM('src')

    def high_destination(self):
        return self.EMO('dst')

    def pre(self, X, w):
        """Full two-sort Pre: {0: O-predecessors, 1: M-predecessors (w==0 only)}.
        Const-False target sides contribute no disjunct (exact: empty target side
        admits no witnesses; avoids vacuous binders)."""
        d = self.d
        eOO, eOM = self.EOO(w), self.EOM(w)
        parts0 = []
        if X.get(0) is not None and not self._side_false(X[0]):
            c = d.AND(eOO, X[0])
            vs = sorted(self._o2names(c))
            parts0.append(d.EXISTS(tuple(vs), c) if vs else c)
        if X.get(1) is not None and not self._side_false(X[1]):
            c = d.AND(eOM, X[1])
            vs = sorted(self._mnames(c))
            parts0.append(d.EXISTS(tuple(vs), c) if vs else c)
        r0 = d.OR(*parts0) if parts0 else d.const_bool(False)
        if w == 0 and X.get(0) is not None and not self._side_false(X[0]):
            c = d.AND(self.EMO(0), X[0])
            vs = sorted(self._o2names(c))
            r1 = d.EXISTS(tuple(vs), c) if vs else c
        else:
            r1 = d.const_bool(False)
        return {0: d.AND(self.U_O, r0), 1: d.AND(self.U_M, r1)}

    def post(self, X, w):
        d = self.d
        eOO, eOM = self.EOO(w), self.EOM(w)
        partsO = []
        if X.get(0) is not None and not self._side_false(X[0]):
            c = d.AND(eOO, X[0])
            vs = sorted(self._onames(c))
            partsO.append(d.EXISTS(tuple(vs), c) if vs else c)
        if w == 0 and X.get(1) is not None and not self._side_false(X[1]):
            c = d.AND(self.EMO(0), X[1])
            vs = sorted(self._mnames(c))
            partsO.append(d.EXISTS(tuple(vs), c) if vs else c)
        rO = d.OR(*partsO) if partsO else d.const_bool(False)
        if X.get(0) is not None and not self._side_false(X[0]):
            c = d.AND(eOM, X[0])
            vs = sorted(self._onames(c))
            rM = d.EXISTS(tuple(vs), c) if vs else c
        else:
            rM = d.const_bool(False)
        return {0: d.AND(self.U_O2, rO), 1: d.AND(self.U_M, rM)}

    def minpre_sym(self, X, w):
        """Symbolic MinPre = Pre_w AND NOT(OR_{a<w} Pre_a), per sort."""
        d = self.d
        base = self.pre(X, w)
        out = {}
        for s in (0, 1):
            lowers = []
            for a in self.alphabet:
                if a < w:
                    pa = self.pre(X, a)
                    if pa.get(s) is not None and not TS.is_side_empty_const(d, pa[s]):
                        lowers.append(pa[s])
            if lowers:
                out[s] = d.AND(base[s], d.NOT(d.OR(*lowers)))
            else:
                out[s] = base[s]
        return out

    # ---- set algebra (14-function API over pairs) ----
    def valid_state(self, S):
        return self.U_O if S == 0 else self.U_M

    def union(self, X, Y):
        return TS.union(self.d, X, Y)

    def intersection(self, X, Y):
        return TS.intersection(self.d, X, Y)

    def complement(self, X):
        return TS.complement(self.d, X, self.U_O, self.U_M)

    def equivalent(self, X, Y):
        """Actual decision via symmetric-difference emptiness (needs decide)."""
        return self.is_empty_status(TS.symdiff(self.d, X, Y))

    def is_empty_status(self, X):
        """True/False/UNKNOWN (UNKNOWN if either sort undecided)."""
        r0 = self.decide(X[0], {}, None) if X.get(0) is not None else (UNSAT, None, '')
        r1 = self.decide(X[1], {}, None) if X.get(1) is not None else (UNSAT, None, '')
        if r0[0] == UNSAT and r1[0] == UNSAT:
            return True
        if r0[0] == SAT or r1[0] == SAT:
            return False
        return UNKNOWN

    def contains(self, X, pins, sort):
        """Membership decision under grounded pins. Returns status string."""
        if self.decide is None:
            raise AssertionError('no decide procedure')
        r = self.decide(X[sort], pins, None)[0]
        return r

    def extract_edge_witness(self, w, ss, st):
        e = self.EOO(w) if (ss, st) == (0, 0) else (self.EOM(w) if (ss, st) == (0, 1) else self.EMO(0))
        r = self.decide(e, {}, None)
        if r[0] == SAT:
            return (SAT, r[1])
        return (r[0], None)

    def extract_witness(self, X):
        for s in (0, 1):
            if X.get(s) is not None:
                r = self.decide(X[s], {}, None)
                if r[0] == SAT:
                    return (SAT, s, r[1])
        r0 = self.decide(X.get(0), {}, None) if X.get(0) is not None else (UNSAT, None, '')
        r1 = self.decide(X.get(1), {}, None) if X.get(1) is not None else (UNSAT, None, '')
        if r0[0] == UNKNOWN or r1[0] == UNKNOWN:
            return (UNKNOWN, None, None)
        return (UNSAT, None, None)

    # ---- nesting (canonical coordinate maps supplied by backend) ----
    def rename_O_to_O2(self, node):
        return self.d.subst(node, self.rename_s2d)

    def rename_O2_to_O(self, node):
        return self.d.subst(node, self.rename_d2s)
