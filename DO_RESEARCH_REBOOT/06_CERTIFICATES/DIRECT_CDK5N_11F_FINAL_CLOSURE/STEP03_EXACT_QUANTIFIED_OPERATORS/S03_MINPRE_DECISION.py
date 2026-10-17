# S03_MINPRE_DECISION.py — finite-weight MinPre decision procedure (Gate F/G13/G14).
# minpre_member(s, X, w): weight-w existence + ascending lower-weight exclusion.
# Verdict discipline (frozen): Step-02 SAT => member-candidate; Step-02 certified
# B-level UNSAT (no-b-words/sig-mu-mismatch/marked-count/b-decode) => certified
# exclusion; Step-02 a-incomplete/word-truncated/time-cap => UNKNOWN (never exclusion).
# Tier-1/Z3 on normalized queries may additionally decide either way when sound.
# Proved equivalent to symbolic MinPre_w(X) (finite alphabet + sound per-weight
# decisions + UNKNOWN propagation); proof in S03_MINPRE_CORRECTNESS_THEOREM.md.
import sys
sys.path.insert(0, 'DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5N_11F_FINAL_CLOSURE/STEP02_FREE_WITNESS_SYNTHESIS')
from S02_B_SIDE_PROPAGATOR import b_bfs, decode_btopo, topo_key

SAT, UNSAT, UNKNOWN = 'SAT', 'UNSAT', 'UNKNOWN'
CERTIFIED_UNSAT = {'no-b-words', 'no-b-words(H>=1)', 'sig-mismatch', 'mu-mismatch',
                   'marked-count!=5', 'b-decode', 'tier1-ground-false', 'domain-violation',
                   'session-contradiction', 'session-call-contradiction'}


def bfs_certified_empty(s_pins, t_pins, w, prefix='SLs'):
    """B-level certified absence: no B-word (H>=1-filtered) ends at t.B.
    H>=1 is sound: macro_H sums event_a with a=0 only at depth 0, so H=0 forces
    all-depth-0 accesses hence B-identity, contradicting genuine-terminal change
    (both enforced: chg in BFS, `chg` conjunct + EQ(macro_H,Hv) in the relation).
    Returns (True, detail) if certified-empty, else (False, reason)."""
    tpre = 'SLt' if prefix == 'SLs' else ('SHt' if prefix == 'SHs' else None)
    mu = s_pins[prefix + '_mu']
    marked = set(i for i in range(9) if (mu >> i) & 1)
    stopo, sroot = decode_btopo(s_pins, prefix)
    ttopo, troot = decode_btopo(t_pins, tpre)
    try:
        words, _ = b_bfs(stopo, sroot, topo_key(ttopo, troot), marked, w)
    except AssertionError as e:
        return True, 'b-decode: %s' % (e,)
    words = [r for r in words if r['H'] >= 1]
    if not words:
        return True, 'no-b-words(H>=1)'
    return False, '%d-b-words' % len(words)


class MinPreDecider:
    def __init__(self, alphabet, edge_sat=None, edge_unsat=None):
        # edge_sat(s,X,w)->(verdict,detail): Step-02 engine / Tier-1 / Tier-2.
        # edge_unsat(s,X,w)->(verdict,detail): certified-exclusion oracles.
        self.alphabet = sorted(alphabet)
        self.edge_sat = edge_sat
        self.edge_unsat = edge_unsat
        self.trace = []

    def edge_decision(self, s, X, w):
        if self.edge_sat is not None:
            v, d = self.edge_sat(s, X, w)
            if v == SAT:
                return (SAT, d)
        if self.edge_unsat is not None:
            v, d = self.edge_unsat(s, X, w)
            if v == UNSAT and d in CERTIFIED_UNSAT:
                return (UNSAT, d)
        return (UNKNOWN, 'undecided')

    def minpre_member(self, s, X, w):
        """Returns (member?, certificate): member True/False/UNKNOWN.
        Order: lower-ascending scan first (any certified lower SAT => FALSE even if
        weight-w itself is undecided); then weight-w existence; then lower-absence
        completion. Sound in all orders; this order maximizes decisiveness."""
        self.trace = []
        unk_lower = []
        for a in self.alphabet:
            if a >= w:
                continue
            va, da = self.edge_decision(s, X, a)
            self.trace.append(('lower', a, va, da))
            if va == SAT:
                return (False, {'reason': 'lower-weight-edge', 'a': a, 'detail': da, 'trace': self.trace})
            if va == UNKNOWN:
                unk_lower.append((a, da))
        vw, dw = self.edge_decision(s, X, w)
        self.trace.append(('w', w, vw, dw))
        if vw == UNSAT:
            return (False, {'reason': 'no-weight-w-edge', 'detail': dw, 'trace': self.trace})
        if vw == UNKNOWN:
            return (UNKNOWN, {'reason': 'weight-w-undecided', 'detail': dw, 'trace': self.trace})
        if unk_lower:
            a, da = unk_lower[0]
            return (UNKNOWN, {'reason': 'lower-weight-undecided', 'a': a, 'detail': da, 'trace': self.trace})
        return (True, {'reason': 'min-member', 'trace': self.trace})
