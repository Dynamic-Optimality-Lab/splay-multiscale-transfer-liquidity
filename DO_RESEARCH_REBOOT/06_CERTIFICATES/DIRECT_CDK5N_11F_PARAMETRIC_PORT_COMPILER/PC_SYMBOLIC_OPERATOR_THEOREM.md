# PC_SYMBOLIC_OPERATOR_THEOREM.md — G17/G18/G19 (production Pre/Post/MinPre)

## Implementation (PC_SYMBOLIC_OPERATORS.py over PC_PRODUCT_COMPILER.py)
Canonical sorts (O ordinary, M midpoint); `Pre_w(X)(s) = Exists tvars (E_w(s,t) /\ X(t))`;
`Post` dually; `MinPre_w = Pre_w /\ ~\/{a<w} Pre_a` (finite alphabet -4..6). Full 14-function API:
valid_state/low_edge/high_source/high_destination/pre/post/minpre(+pre_mid)/union/intersection/
complement/equivalent/is_empty/extract_witness/extract_edge_witness. Nesting via capture-safe
subst renaming (O<->O2); shadowed binders tested; ordinary/midpoint type separation enforced
(mid predicates never merge into ordinary results).

## MinPre semantics theorem
`s in MinPre_w(X) <=> min_{s->t, t in X} w(s,t) = w`: (->) s has a w-edge into X and no a-edge for
a<w by the negated disjuncts (finite alphabet: all lower weights excluded); (<-) min = w gives a
w-edge (Pre_w) and no lower edge (negations hold). Finite alphabet exactness is load-bearing and
proved (q<=4 core-depth bound; H<=2; weights -4..6 exhaustive).

## Test summary (V11, PC_PRE_POST_MINPRE_TESTS.json)
Binder hygiene (capture/shadowing) SAT/UNSAT exact; MinPre structure (negations + EXISTS present);
empty-target exact-False; type separation; 20 grounded membership agreements (production predicates,
concrete edges); 20 bounded wrong-weight UNSAT (terminating proofs, micro scope, 0 UNKNOWN).

## Scope honesty (G20 interaction)
Predicate CONSTRUCTION is total (all operators built; 1,345,105 shared nodes). QUERY answering is
solver-backed: grounded + UNSAT-terminating queries exact; free-witness SAT synthesis terminates at
micro scope and returns UNKNOWN beyond (measured: 120-300s caps; per-visit cost; branching analysis
in PC_RESOURCE_LEDGER.json). No SAT answer is ever approximated: SAT/UNSAT/UNKNOWN only.

## Gates G17/G18/G19: PASS (constructed + semantics proved + V11 tested).
G20 (solver completeness at required scope): PARTIAL — exact at micro/bounded scope, UNKNOWN beyond
(see G22/verdict for the execution consequence).
