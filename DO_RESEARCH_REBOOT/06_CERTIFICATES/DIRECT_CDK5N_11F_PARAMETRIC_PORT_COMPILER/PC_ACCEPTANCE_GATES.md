# PC_ACCEPTANCE_GATES.md — G01-G24 evaluation

| Gate | Status | Evidence |
|---|---|---|
| G01 sources/model frozen | PASS | PC_SOURCE_AUDIT.md (4/4 SHA256, HEAD, Bank25@25, solver/rep/resource freeze) |
| G02 KEEP/DELETE grammar | PASS | PC_EFFECTIVE_MACRO_GRAMMAR.md (root-run collapse; <=5 events; full coverage proved) |
| G03 four-rotation bound | PASS | PC_PORT_COMMUTATION_CORRECTED.md + PC_C3_AUDIT.json (3000/3000 prim==depth, max 4) |
| G04 port commutation | PASS | corrected induction + 4000/4000 replay (imported) + 263/263 interpreter exactness |
| G05 shared atoms | PASS | PC_SHARED_ATOM_THEOREM.md + 138 grounded + micro SAT/UNSAT |
| G06 hidden-S placement | PASS | PC_ORDERED_WITNESS_BICONDITIONAL.md (strict intervals, fullrank, exact cover) |
| G07 same-gap ordering | PASS | biconditional doc + position-order verification per edge |
| G08 T=266 audit | PASS | PC_266_SATURATION_AUDIT.md (13-item ledger + imports + explicit OPEN lemma) |
| G09 126 masks | PASS | PC_ALL_126_MASKS.json (126/126 valid_state SAT, parametric 9-bit var) + transitions |
| G10 state-validity compiled | PASS | state_valid in product; 10 checks; 138+63 grounded states |
| G11 rotation interpreter | PASS | PC_ROTATION_INTERPRETER.py; 263/263 exact vs source; 4-primitive bound |
| G12 B-controller | PASS | PC_B_CONTROLLER.py; q from core depth; DELETE identity; 263/263 + 138 grounded |
| G13 low relation | PASS | PC_LOW_RELATION_EQUIVALENCE.md; one shared circuit; 138 grounded; 5 negatives |
| G14 genuine weights | PASS | C2 (q constrained, never supplied); E3+E4 certified negatives with provenance |
| G15 high midpoints | PASS | PC_HIGH_FIBER_COMPLETENESS.md; 63 grounded; WQ equivalence imported |
| G16 arbitrary-fringe graph | PASS | G_AF over (mu,b,alpha,sigma) + midpoints; saturated domain unrestricted in predicates |
| G17 Pre | PASS | constructed + MinPre/theorem + V11 (20 agree + binder/hygiene/type/empty tests) |
| G18 Post | PASS | constructed + V11 (structure + grounded membership) |
| G19 MinPre | PASS | semantics theorem + exclusion construction + V11 |
| G20 solver SAT/UNSAT | PARTIAL | exact at micro/bounded scope (UNSAT terminates; SAT grounded); free-synthesis UNKNOWN beyond |
| G21 DAG <=4M | PASS | 1,345,105 shared nodes (PC_SHARED_DAG_COUNTS.json), recomputed by verifier |
| G22 resources | PASS | within all caps (PC_RESOURCE_LEDGER.json); solver frozen; UNKNOWNs recorded |
| G23 simulation | PASS | PC_UNIVERSAL_SIMULATION.md (10 items vs predicates; item 9 conditional on OPEN lemma) |
| G24 verifier/repro | PASS | PC_INDEPENDENT_VERIFICATION.json (V1-V15); commands in AZ; fresh rebuild |

G20 PARTIAL: free-witness SAT synthesis returns UNKNOWN beyond micro scope (measured, capped runs).
G23 item 9 conditional on the fringe-ancestor-q OPEN lemma (explicit, counted, not hidden).
Verdict follows in PC_TERMINAL_VERDICT.md.
