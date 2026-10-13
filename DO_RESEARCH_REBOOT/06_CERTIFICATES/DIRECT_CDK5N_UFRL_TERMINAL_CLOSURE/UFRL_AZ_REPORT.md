# UFRL_AZ_REPORT.md (condensed; details in linked artifacts)

Entry b2d42ac==origin; sources 4/4; Bank25@25; Outcome-D predecessor read; additive dir only.
Theorem frozen (W_5^9, costs, closure); architecture single (prefix→critical→saturated-rep→macros→lifting→certificate; h=2, T=266, caps).
Foundations audited (B-core, normalization, H=1 form, cones) + E1-E8 implemented (bounds exact: |E|≤264, |U*|≤2669).
L1-L8 fuzz-verified (2,305 general + 180 adversarial + 60 G/J; saturation to 2000-key gaps; 0 mismatch); B-compat 30,773 (incl. 30,720 corpus), 0 mismatch.
Grammar 3,060/3,060; high-cost 3,084/3,084; composition exact-boundary; U1-U10 STAGE 10 PROVED.
Product: 9-key all-126-mask unified graph CLOSED (312k low → 1.31M states, 21.8M edges deduped 11.9M, 1,467 mids); BF stable 6 iters; potential verified 6,914+650 (±O smokes).
Regressions A-J PASS (A 30/52/36; B 31/53/36; C 29/50/36; D Q14; E Q18 unique start; F non-commute; G/H/I/J fuzz).
Caps respected (states 13%, transitions 12%, A-states 4,862, macros 7.93M/15M after dedup correction, CPU ~1h, RAM <6GiB).
Universal blocked (measured): completions, 5.5B UB, 612k seeds, lifting lemma open; h=4 unwarranted; E4 structural-ready/vacuous.
Verdict OUTCOME B (Stage 10 proved; terminal open). R1-T OPEN, R2 OPEN, R3 PASS, R4 OPEN. No promotion/successor. STOP. K≥6/universal/DO remain OPEN.
