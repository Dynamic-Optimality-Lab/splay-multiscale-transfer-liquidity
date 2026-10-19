# CORE-01 Conditional Low-Edge Monotonicity (PROVED, Gate C scoped)

THEOREM (conditional): for every frozen low edge E^OO_w(s,t) witnessed with
all B-changing KEEP events targeting marked keys, C(t) subset C(s).
Proof: induction over events; DELETE/inactive identical (R4); each marked-
target splay preserves C by R1-R3 composition. COROLLARY: every
single-event low edge (nev=1: sole event is terminal = genuine marked;
ssertify pins nev=len(word), so all single-KEEP words) satisfies
monotonicity unconditionally. OPEN HOLE (blocks universality): multi-event
edges with intermediate unmarked-target B-changing KEEPs (A8 explicitly
admits them: only marked+B-changing intermediates are banned). No such
witness shape is ruled out by validity/compat/A-side conjuncts found.
No certified violating edge (forbidden to generate; 110+ samples clean).
