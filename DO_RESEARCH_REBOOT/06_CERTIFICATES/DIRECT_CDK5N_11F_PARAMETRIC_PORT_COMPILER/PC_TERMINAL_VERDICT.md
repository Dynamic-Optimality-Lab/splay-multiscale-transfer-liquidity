# PC_TERMINAL_VERDICT.md — OUTCOME B (mathematical construction valid, execution blocked)

## What was compiled (new, measured, within budget)
One shared parametric symbolic transition system (1,345,105 hash-consed DAG nodes ≤ 4M cap):
causal A-prefix (127 slots) + persistent port identities (cut-labels) + shared atom inventory
((gap,port) cells + hidden-S + fullrank) + exact primitive rotation interpreter (263/263 vs source,
C3-corrected ≤4 primitives) + source-exact 9-core B-controller (q from core depth, DELETE identity) +
one quantified low relation (138 grounded, 5 genuine negatives incl. E3/E4) + parametric high-cost
midpoints (63 grounded, WQ equivalence imported) + production Pre/Post/MinPre (V11: 20 agree, 20
unsat, 0 unknown at micro scope; binder/hygiene/type/empty tests) + all 126 masks parametric
(126/126 valid_state SAT). Independent verifier V1-V15 passes. No representation refuted. No original
counterexample (diagnostic graphs BF-clean; 138+63 grounded edges consistent).

## Exact failing operations (execution-blocked, not projected)
1. Free-witness SAT synthesis beyond micro scope: solver returns UNKNOWN (measured: 120-300s caps;
   ~0.15s/visit; 783 visits without convergence on 9-key queries; micro-scope synthesis also UNKNOWN
   while micro-UNSAT terminates in seconds). Consequence: G20 PARTIAL (exact at bounded scope only).
2. Fringe-ancestor-q class: representative q may differ from concrete q (measured skip rates
   120/720, 52/480, 182/720; explicit OPEN lemma, counted). Consequence: G23 item 9 CONDITIONAL.
No lower bound claimed (C1 respected): the compiled circuit EXISTS at 1.35M nodes; incompressibility
never asserted (guard diversity retired as evidence).

## Declarations
**STAGE 11F OPEN — EXECUTION BLOCKED (OUTCOME B).** Smallest obstruction: solver-backed free-witness
synthesis non-termination at full scope (operation, caps, visits measured above). Terminal
Coarse-Double OPEN. Bank25 at 25 (no promotion). No 11G. No successor. STOP.
