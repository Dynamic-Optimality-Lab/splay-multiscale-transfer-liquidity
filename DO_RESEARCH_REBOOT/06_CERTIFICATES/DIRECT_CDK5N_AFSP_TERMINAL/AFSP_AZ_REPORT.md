# AFSP_AZ_REPORT.md (condensed; evidence in linked artifacts)

Entry 56191f3==origin; sources 4/4; Bank25@25; Outcome-B predecessor read; additive dir only.
Theorem frozen (W_5^9, costs, closure); architecture single (cones→holes→allocation→saturation→factorization→product→DC; h=2, T=266, 126 masks, caps).
Foundations re-audited; TWO prior-work bugs confirmed+fixed (shadow raw-key leakage in hole bounds — canonical order-type fix, K 200/200; initial-depth H vs sequential — 71% differ, corrected, lemmas stand).
AF-1 cone-cut (rotation-path induction + 572+60 fuzz); AF-2 allocation (max-flow; brute-force 80/80; reconstruction 64/64); AF-3 pumping (occupied-discipline; 30 tests + saturation to 2000 keys; two development artifacts correctly classified); AF-4 factorization (guard theorem; 5,280-template H=1 kernel, all step cases incl. D(v)+K(v)).
Gates: A (4.26M states from all 612k... 26,368 valid diagonal starts, closed, reconciles-vs-1.31M: previous seed-relative incomplete); B (124/124 guard-feasible); C (triage 100/100).
Product: low-only all-mask CLOSED (4.26M/29.1M deduped — cap overrun x1.94 recorded); BF stable 5 iters; potential verified 9,348/9,348 (±O smokes); high-cost fanout explosive (measured); fringe symbolic blocked (measured bounds + unproved lifting).
Uniform gate: B-only ansatz fails (90 groups); signature quotient theorem conditional, classes uncomputed.
Verdict OUTCOME E (partial/resource). R1-T OPEN, R2 OPEN, R3 PASS-WITH-DEVIATION, R4 OPEN. No promotion/successor. STOP.
