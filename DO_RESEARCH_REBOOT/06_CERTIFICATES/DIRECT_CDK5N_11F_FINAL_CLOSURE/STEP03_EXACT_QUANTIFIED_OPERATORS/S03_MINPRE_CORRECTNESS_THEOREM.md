# S03_MINPRE_CORRECTNESS_THEOREM.md — exact minimum-weight exclusion (Gate F/G13)

Symbolic MinPre_w(X)_i = Pre_w(X)_i AND NOT(OR_{a<w} Pre_a(X)_i): correctly
scoped negated existentials (Step-02 in-scope bounds; Q1/Q4 regressions).
Execution by finite-weight procedure (lower-ascending SAT-first order), PROVED
equivalent: finite alphabet + per-weight sound decisions + UNKNOWN propagation
cover exactly the symbolic truth conditions (SAT lower edge => nonmember however
weight-w decides; all-lower-UNSAT + weight-w SAT => member; any needed UNKNOWN
=> UNKNOWN). Step-02 discipline frozen in: SAT => member-candidate; certified
B-level UNSAT (BFS-empty incl. proved H>=1 filter, sig/mu/validation) =>
exclusion; a-incomplete/word-truncated/time-cap => UNKNOWN (never exclusion).
H>=1 proof: macro_H sums event_a (0 only at depth 0); H=0 forces all-depth-0
accesses hence B-identity, contradicting genuine-terminal change. Evidence: J7
(FALSE via w=-1 edge), J8 (TRUE, lowers -4..-2 certified absent), small-graph
MinPre with/without lower weights (all X subsets).
