# S03_SMALL_GRAPH_RUN.py — exhaustive small-graph oracle comparisons (Gate I).
# For each adversarial family: build (oracle graph, mirror DAG + S03 operators),
# compare EVERY membership/emptiness/equivalence/extraction query state-by-state.
# Mirror DAGs use sort-tagged vars (Os/Os2/Ms) with edge predicates as explicit
# pair-disjunctions; S03 QOps execute them through compiled Z3 (tiny, decisive).
# FAIL CLOSED with counts. No 16-case limit: exhaustive subsets + adversarial families.
import sys, json, itertools
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_PARAMETRIC_PORT_COMPILER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP01_PRODUCTION_CONSTRAINT_SOLVER')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS')

PDIR = 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP03_EXACT_QUANTIFIED_OPERATORS/'
FAIL = []
NCMP = [0]
NOK = [0]


def J(p, o):
    json.dump(o, open(PDIR + p, 'w'), indent=1)


def cmp(name, got, want):
    NCMP[0] += 1
    ok = (got == want)
    if ok:
        NOK[0] += 1
    else:
        FAIL.append((name, got, want))


from PC_TYPED_DAG import DAG
from S01_SOLVER_INTERFACE import ProductionSolver, SAT, UNSAT, UNKNOWN
from S02_SEMANTIC_SAFETY_PATCH import install_scoped_compile
from S03_SCOPE_REPAIR import install_fixed_compile
from S03_INDEPENDENT_FINITE_GRAPH_ORACLE import FiniteGraph
from S03_QUANTIFIED_OPERATORS import QOps
import S03_TYPED_STATE_SETS as TS


def _or_pairs(d, eqv, pairs, sv, tv, mv):
    # pairs: list of (kind, x, y)
    ds = []
    for (kind, x, y) in pairs:
        if kind == 'OO':
            ds.append(d.AND(eqv(sv, x), eqv(tv, y)))
        elif kind == 'OM':
            ds.append(d.AND(eqv(sv, x), eqv(mv, y)))
        elif kind == 'MO':
            ds.append(d.AND(eqv(mv, x), eqv(tv, y)))
    return d.OR(*ds) if ds else d.const_bool(False)


class Mirror:
    def __init__(self, O, M, edges):
        self.O, self.M = list(O), list(M)
        self.g = FiniteGraph(O, M, edges)
        d = DAG()
        B = max(1, (max(O + M + [1])).bit_length())
        self.d, self.B = d, B
        self.sv = d.var_int('Os_v', B)
        self.tv = d.var_int('Os2_v', B)
        self.mv = d.var_int('Ms_v', B)

        def E(kind, w):
            ps = [(kind, x, y) for (x, y) in edges.get(kindmap(kind) + (w,), set())]
            return _or_pairs(d, lambda v, c: d.EQ(v, d.const_int(c, B)), ps, self.sv, self.tv, self.mv)

        def kindmap(k):
            return (0, 0) if k == 'OO' else ((0, 1) if k == 'OM' else (1, 0))

        U_O = d.OR(*[d.EQ(self.sv, d.const_int(x, B)) for x in O])
        U_M = d.OR(*[d.EQ(self.mv, d.const_int(x, B)) for x in M])
        U_O2 = d.OR(*[d.EQ(self.tv, d.const_int(x, B)) for x in O])
        ps = ProductionSolver(d, timeout_ms=30000)
        install_fixed_compile(ps)
        self.ps = ps
        self._hc = {}

        def decide(root, pins, timeout):
            # compile-once per root id; many pin-sets per handle (Gate-H caching)
            key = root
            if key not in self._hc:
                h = ps.compile(root, 'r%d' % len(self._hc))
                self._hc[key] = h
            r = ps.solve(self._hc[key], pins)
            return (r['status'], r.get('model'), r.get('reason', ''))

        self.ops = QOps(d, lambda v: v == 'Os_v', lambda v: v == 'Os2_v', lambda v: v == 'Ms_v',
                        EOO=lambda w: E('OO', w), EOM=lambda w: E('OM', w), EMO=lambda w: E('MO', w),
                        U_O=U_O, U_M=U_M, decide=decide,
                        rename_s2d={'Os_v': 'Os2_v'}, rename_d2s={'Os2_v': 'Os_v'},
                        alphabet=sorted(set(w for (_, _, w) in edges)), U_O2=U_O2)

    def Xpred(self, XO, XM):
        d = self.d
        B = self.B
        po = d.OR(*[d.EQ(self.tv, d.const_int(x, B)) for x in XO]) if XO else d.const_bool(False)
        pm = d.OR(*[d.EQ(self.mv, d.const_int(x, B)) for x in XM]) if XM else d.const_bool(False)
        return {0: po, 1: pm}

    def pins(self, v, x):
        return {v: x}

    def member_O(self, pred, x):
        return self.ops.decide(pred, {'Os_v': x}, None)[0]

    def member_M(self, pred, x):
        return self.ops.decide(pred, {'Ms_v': x}, None)[0]


def subsets(s):
    out = []
    for r in range(len(s) + 1):
        for c in itertools.combinations(s, r):
            out.append(set(c))
    return out


if __name__ == '__main__':
    RES = {'families': [], 'comparisons': 0, 'agreements': 0}
    # Family 1: OO chain weights -1,0,2
    fams = []
    fams.append(('chain', [0, 1, 2], [0], {(0, 0, -1): {(0, 1)}, (0, 0, 2): {(1, 2)}, (0, 0, 0): {(0, 2)}}))
    fams.append(('diamond', [0, 1], [0], {(0, 1, 3): {(0, 0)}, (1, 0, 0): {(0, 1)}, (0, 0, 1): {(0, 1)}}))
    fams.append(('negchain', [0, 1, 2, 3], [0], {(0, 0, -4): {(0, 1)}, (0, 0, -3): {(1, 2)}, (0, 0, -2): {(2, 3)}, (0, 0, -1): {(0, 3)}}))
    fams.append(('multi', [0, 1], [0, 1], {(0, 0, 1): {(0, 1)}, (0, 0, 2): {(0, 1)}, (0, 1, 1): {(0, 0), (0, 1)}, (1, 0, 0): {(0, 1), (1, 1)}}))
    for (name, O, M, edges) in fams:
        mir = Mirror(O, M, edges)
        alpha = sorted(set(w for (_, _, w) in edges))
        nfam = [0]
        # exhaustive X subsets x pre/post per weight
        for XO in subsets(O):
            for XM in subsets(M):
                X = mir.Xpred(XO, XM)
                for w in alpha:
                    oO, oM = mir.g.pre(XO, XM, w)
                    P = mir.ops.pre(X, w)
                    for s in O:
                        cmp('%s preO w=%s X=%s s=%s' % (name, w, (XO, XM), s),
                            mir.member_O(P[0], s), SAT if s in oO else UNSAT)
                    for m in M:
                        cmp('%s preM w=%s X=%s m=%s' % (name, w, (XO, XM), m),
                            mir.member_M(P[1], m), SAT if m in oM else UNSAT)
                    pO, pM = mir.g.post(XO, XM, w)
                    # post takes SOURCE-side X: rename dst-position predicate to src
                    Xs = {0: mir.ops.rename_O2_to_O(X[0]), 1: X[1]}
                    Q = mir.ops.post(Xs, w)
                    for t in O:
                        # post_O over Os2 (destination names!): pins use tv var
                        cmp('%s postO w=%s X=%s t=%s' % (name, w, (XO, XM), t),
                            mir.ops.decide(Q[0], {'Os2_v': t}, None)[0], SAT if t in pO else UNSAT)
                    for m in M:
                        cmp('%s postM w=%s X=%s m=%s' % (name, w, (XO, XM), m),
                            mir.ops.decide(Q[1], {'Ms_v': m}, None)[0], SAT if m in pM else UNSAT)
                    mO, mM = mir.g.minpre(XO, XM, w, alpha)
                    S = mir.ops.minpre_sym(X, w)
                    for s in O:
                        cmp('%s minpreO w=%s X=%s s=%s' % (name, w, (XO, XM), s),
                            mir.member_O(S[0], s), SAT if s in mO else UNSAT)
                    for m in M:
                        cmp('%s minpreM w=%s X=%s m=%s' % (name, w, (XO, XM), m),
                            mir.member_M(S[1], m), SAT if m in mM else UNSAT)
                # set algebra on this X vs complement/empty/equiv
                C = mir.ops.complement(X)
                oC = mir.g.compl((XO, XM))
                for s in O:
                    # complement of dst-side X is dst-side: pin Os2_v
                    cmp('%s complO X=%s s=%s' % (name, (XO, XM), s),
                        mir.ops.decide(C[0], {'Os2_v': s}, None)[0], SAT if s in oC[0] else UNSAT)
                for m in M:
                    cmp('%s complM X=%s m=%s' % (name, (XO, XM), m), mir.member_M(C[1], m), SAT if m in oC[1] else UNSAT)
                Y = mir.Xpred(set(O[:1]), set())
                eq_oracle = mir.g.equiv((XO, XM), (set(O[:1]), set()))
                eq_got = mir.ops.equivalent(X, Y)
                cmp('%s equiv X=%s' % (name, (XO, XM)), eq_got, eq_oracle)
                emp_oracle = mir.g.isempty((XO, XM))
                emp_got = mir.ops.is_empty_status(X)
                cmp('%s empty X=%s' % (name, (XO, XM)), emp_got, emp_oracle)
                # extraction: SAT with right-state model iff nonempty; never conflated
                ex = mir.ops.extract_witness(X)
                cmp('%s extract-status X=%s' % (name, (XO, XM)),
                    ex[0], SAT if not emp_oracle else UNSAT)
        # nested: Pre_a(Post_b(X)) and MinPre_a(Pre_b(X)) on selected X
        X = mir.Xpred(set(O[:1]), set(M[:1]) if M else set())
        Xs = {0: mir.ops.rename_O2_to_O(X[0]), 1: X[1]}
        for a in alpha:
            for b in alpha:
                inner = mir.ops.post(Xs, b)
                # rename inner result (over src/dst vars) into target position: inner O-part
                # is over Os2 (post destination); pre expects X over Os2/Ms: direct reuse
                nested = mir.ops.pre({0: inner[0], 1: inner[1]}, a)
                on, om = mir.g.post(set(O[:1]), set(M[:1]) if M else set(), b)
                nn, nm = mir.g.pre(on, om, a)
                for s in O:
                    cmp('%s nested Pre%d(Post%d) s=%s' % (name, a, b, s), mir.member_O(nested[0], s), SAT if s in nn else UNSAT)
                Mp = mir.ops.pre(X, b)
                # MinPre_a(Pre_b): rename Pre_b O-part (over Os source vars) to dst position
                # via rename map for nesting check
                Mp_dst = {0: mir.ops.rename_O_to_O2(Mp[0]), 1: Mp[1]}
                op_, om_ = mir.g.pre(set(O[:1]), set(M[:1]) if M else set(), b)
                mm, mmm = mir.g.minpre(op_, om_, a, alpha)
                Sm = mir.ops.minpre_sym({0: Mp_dst[0], 1: Mp_dst[1]}, a)
                for s in O:
                    cmp('%s nested MinPre%d(Pre%d) s=%s' % (name, a, b, s), mir.member_O(Sm[0], s), SAT if s in mm else UNSAT)
        RES['families'].append(name)
    RES['comparisons'] = NCMP[0]
    RES['agreements'] = NOK[0]
    RES['mismatches'] = [f for f in FAIL[:10]]
    J('S03_SMALL_GRAPH_ORACLE_RESULTS.json', RES)
    print('comparisons=%d agreements=%d FAIL=%d' % (NCMP[0], NOK[0], len(FAIL)), flush=True)
    assert not FAIL, FAIL[:5]
    print('SMALL-GRAPH ORACLE PASS')
