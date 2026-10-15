# STRICT_TERMINAL_VERDICT.md — OUTCOME E (PARTIAL / UNKNOWN)

## Strongest proved result
Source-semantic hardening of the persistent-port compiler complete and verified: 9 audit findings
dispositioned (8 repaired+tested, 0 dismissed without proof); repaired low relation (1,400,081
nodes) with 108 grounded edges, 0 mismatches, full adversarial rejection suite green (A1/A2/A4/A7/A8),
A3 normalization 60/60; marked-splay C_M monotonicity proved (0 growth/1118) with exact growth
characterization (<= target join); all prior construction evidence stands undisplaced.

## First open obligation (SC10)
Universal marked-core/q correspondence: universal monotonicity REFUTED by minimal admissible
counterexample (B=10(1,20), M={20}, KEEP(1): C_M {10,20}->{1,10,20}); C_M=S REFUTED by admissible
boundary (root 5, marked 9 with fringe ancestors [12,7]); fringe-ancestor q OPEN. No repair exists
inside the frozen architecture (R3 prohibits new observables/coordinates; restriction would violate
R1-T universality; conservative q would break exact weights). HARD STOP per R3/Gate-B.

## Completed executable artifacts
STRICT_* implementation (repairs, compilers-assemblies-minus-product, certifier, adversarial suite,
monotonicity probe) + 10 theorem docs + evidence JSONs, all committed additively.

## Failed/unexecuted
SC10 (refuted premise); SC12/17/19/20/21/22/24 downstream of the stop (OPEN, not attempted).
No UNKNOWN relabeled; no conditional passed; no promotion.

## Resource ledger
See STRICT_RESOURCE_LEDGER.json (to be written at commit; usage ~1 CPU-h, DAG 1.4M/4M).

Stage 11F OPEN. No promotion. HARD STOP.
