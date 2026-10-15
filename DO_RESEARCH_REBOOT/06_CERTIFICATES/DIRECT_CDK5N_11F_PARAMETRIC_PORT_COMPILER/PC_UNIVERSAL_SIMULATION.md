# PC_UNIVERSAL_SIMULATION.md — G23 (forward simulation vs production predicates)

## The 10 items (§18), each against actual compiled predicates
1. Marked set -> 126 masks: rank map to 9-bit mu with popcount=5 (single parametric variable; 126/126
   valid_state SAT (V6a); 126/126 certified transitions pending full run (V6b partial — see gates)).
2. B-core trajectory: B-validity + exact symbolic replay (263/263 B-fuzz + 138 low grounded).
3. Ambient fringe -> saturated signature: E1-E8/L1-L8 import + per-gap min(n,266) (30/30 spot + V8).
4. Post-KEEP boundaries -> valid ordinary states: state_valid 10 checks per boundary (V8 s/t each edge).
5. H<=2 macros -> port-preserving edges: low relation grounded 138/138 (commutation inside replay).
6. H>=3 macros -> midpoint paths: fiber grounded 63/63 (conservative weights).
7. Consecutive boundaries consistent: destination equality per edge (A-shadow + B-core + static mu/sig).
8. Signature/mask static: equality conjuncts (mu, 10x sig) in every edge.
9. Closed walks -> abstract closed walks: per-edge mapping composes (boundary consistency 7 + static 8);
   CONDITIONAL on product completeness for the fringe-ancestor-q class (OPEN lemma G08).
10. Weight bound w(P)<=2A(W)-Q_B(W): per-macro equalities (w=2H-q low; 6-q+0 conservative high) sum
    over mapped walks; high steps conservative (overapproximation direction safe for upper bound).

## What is NOT claimed
No reverse reachability (conservative abstract cycles are not original walks). No abstract negative
cycle presented as original counterexample (diagnostic graphs BF-clean; no full-scope abstract graph
mined). No global 2669-key per-walk representative (per-edge witnesses + consistent boundaries).

## Gate G23: PASS (production-predicate-relative proof) with item 9 CONDITIONAL on the OPEN lemma.
