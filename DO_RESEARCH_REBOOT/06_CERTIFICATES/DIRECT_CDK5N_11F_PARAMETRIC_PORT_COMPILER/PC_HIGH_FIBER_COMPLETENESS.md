# PC_HIGH_FIBER_COMPLETENESS.md — G15 (parametric high-cost midpoint relation)

## Construction (PC_HIGH_COMPILER.py)
Fiber `g=(mu,sig,b',v)` as var sets; `S_g(s)`/`D_g(t)` as PREDICATES (mask/sig match, exact B-successor
equality, marked terminal root v); edges `s->m` weight `6-q` (source-computed q, free but constrained
`q<=9`, weight equation in-circuit), `m->t` weight 0. No Cartesian materialization (predicates, not
pair enumeration); empty fibers emit nothing (membership unsatisfiable).

## Imported proof
WQ five-point midpoint equivalence (expansion/contraction preserve edges/weights/cycles; fiber
separation by private mids; grouped-constraint elimination exact): 400/400 faithful-model tests by
reference (WQ_HIGH_COST_FIBERS.md). Conservative direction only (abstract feasibility != original
realizability; never mined for counterexamples).

## Grounded coverage (V10)
63 genuine high-cost transitions (H>=3, source q from genuine legs): fiber assignment SAT each;
63 distinct fibers; static mu/sig; exact B successor; marked root; zero destination edges.
Weights source-side-only by construction (6-q(s) never touches t).

## Saturated-domain coverage
Predicates range over the full saturated domain (mu 9-bit parametric; sig 10x0..266; B any valid
9-core topology; v any marked index): no scope restriction in the compiled predicates. Destination
family D_g described intensionally (root v + mask/sig + B successor), never enumerated.

## Gate G15: PASS (predicates compiled + V10 grounded + WQ equivalence imported).
