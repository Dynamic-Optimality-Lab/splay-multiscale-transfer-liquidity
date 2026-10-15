# PC_AZ_REPORT.md — parametric port compiler campaign (OUTCOME B)

## Entry (STEP 01)
HEAD 052d92d (== FETCH_HEAD == checkpoint). Sources 4/4. Prev verdict B (052d92d). Bank25@25.
Model/solver/representation/resources frozen (PC_SOURCE_AUDIT.md). Triage: proved vs imported vs
diagnostic recorded. No history modified.

## Corrections (STEP 02, mandatory C1/C2/C3)
- C1: guard census retired as lower-bound evidence (descriptors != subcircuits); actual compilation done.
- C2: q source-computed everywhere (constrained `2q<=d<2q+2`); q_terms recategorized diagnostic;
  5 genuine negatives with full replay provenance (E3 q=3, E4 q=4).
- C3: primitive rotations = depth/access (zigzig/zag = 2); macro total <=2H<=4 (3000/3000, max 4);
  displacement <=4; ports stay >=3; depth-2 shadow exact; L5 top-3 clause SUPERSEDED (top-2 proved).

## Construction (STEPs 04-13)
Typed hash-consed DAG (Bool + finite-domain Int; exact widths) + complete finite-domain solver
(backtracking + intervals + EQ-pinning + simplification; Dinic reused for inventory subproblems).
Witness: 127 slots + cut-label ports + <=5-event grammar (proved bound) + verified paths.
Inventory: (gap,port) cells + hidden-S (+ranks) + conservation + exact S-cover.
Interpreters: A (mixed slot/port refs) + B (19-node skeleton, gap-slot proxy, constrained q) —
263/263 exact vs source across all patterns/depths (two order bugs found and fixed in-test).
Low: one shared `Exists xi` relation, w=2H-q (138 grounded). High: parametric fibers/midpoints,
no Cartesian materialization (63 grounded; WQ imported). Product G_AF: 1,345,105 shared nodes.

## Operators + verification (STEPs 14-18)
Production Pre/Post/MinPre + 14-function API; MinPre theorem; V11 (binder/hygiene/type/empty +
20 grounded agree + 20 bounded UNSAT, 0 UNKNOWN at micro scope). Masks 126/126 SAT parametric.
Verifier V1-V15 passes. Simulation 10 items vs predicates (item 9 conditional on OPEN lemma).

## Verdict: OUTCOME B (execution blocked; obstructions measured, not projected).
Terminal OPEN. Bank25@25. No 11G. No successor. STOP.

## Reproduce (Python 3.13.7, stdlib only, repo root)
Commands in PC_BUILD_MANIFEST.json. Budgets in PC_RESOURCE_LEDGER.json. Gates in
PC_ACCEPTANCE_GATES.md. Full evidence JSON: PC_C3_AUDIT, PC_LOW_EDGE_TESTS,
PC_GENUINE_NEGATIVE_EDGES, PC_HIGH_FIBER_TESTS, PC_SAT_UNSAT_CERTIFICATES,
PC_PRE_POST_MINPRE_TESTS, PC_ALL_126_MASKS, PC_SHARED_DAG_COUNTS, PC_INDEPENDENT_VERIFICATION.

## Required artifacts checklist (§20)
Math (10): PC_SOURCE_AUDIT ✓ PC_PORT_COMMUTATION_CORRECTED ✓ PC_EFFECTIVE_MACRO_GRAMMAR ✓
PC_SHARED_ATOM_THEOREM ✓ PC_ORDERED_WITNESS_BICONDITIONAL ✓ PC_266_SATURATION_AUDIT ✓
PC_LOW_RELATION_EQUIVALENCE ✓ PC_HIGH_FIBER_COMPLETENESS ✓ PC_SYMBOLIC_OPERATOR_THEOREM ✓
PC_UNIVERSAL_SIMULATION ✓. Code (11): PC_TYPED_DAG ✓ PC_STRUCTURAL_WITNESS ✓ PC_ATOM_INVENTORY ✓
PC_ROTATION_INTERPRETER ✓ PC_B_CONTROLLER ✓ PC_LOW_COMPILER ✓ PC_HIGH_COMPILER ✓
PC_PRODUCT_COMPILER ✓ PC_SYMBOLIC_OPERATORS ✓ PC_SOLVER_BACKEND ✓ PC_INDEPENDENT_VERIFIER ✓.
Evidence (10): PC_BUILD_MANIFEST ✓ PC_SHARED_DAG_COUNTS ✓ PC_ALL_126_MASKS ✓ PC_LOW_EDGE_TESTS ✓
PC_GENUINE_NEGATIVE_EDGES ✓ PC_HIGH_FIBER_TESTS ✓ PC_PRE_POST_MINPRE_TESTS ✓
PC_SAT_UNSAT_CERTIFICATES ✓ PC_RESOURCE_LEDGER ✓ PC_INDEPENDENT_VERIFICATION ✓.
Verdict (4): PC_ACCEPTANCE_GATES ✓ PC_FOUR_RULE_EXIT ✓ PC_TERMINAL_VERDICT ✓ PC_AZ_REPORT ✓.
Support: PC_CONCRETIZE ✓ PC_CERTIFY ✓ PC_C3_AUDIT(.py/.json) ✓ PC_LOW_TEST_RUN ✓
PC_NEGATIVE_RUN ✓ PC_HIGH_TEST_RUN ✓ PC_MICRO_TEST ✓ PC_EXTRACT_TEST ✓ PC_OPERATOR_TEST ✓
PC_MASK_TEST ✓ PC_DESTINATION_SHARED? (n/a) PC_DEBUG1/2/3 (diagnostic, retained honestly).
WIDTHS table: counters 0..266 (9b); sums <=2660 (12b); ranks 0..135 (8b); bounds 0..136 (8b);
slots 0..126 (7b); child refs 8b (slots/labels/255=null); depths 0..6 (3b); S-idx 0..8 (4b);
B-refs 0..19 (5b); q 0..9 (4b); H 0..2 (2b); w -8..6 (5b signed); nev 0..5 (3b); mu 9b (5 bits).
All arithmetic exact within proved ranges (no wrap: Python-int semantics + width assertions).
