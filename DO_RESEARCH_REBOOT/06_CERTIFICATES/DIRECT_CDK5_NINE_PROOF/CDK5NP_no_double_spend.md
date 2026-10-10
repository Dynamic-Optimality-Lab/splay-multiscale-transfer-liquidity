# Lemma 5 + no-double-spend (PROVED)

**Overlap.** An interval may satisfy both Type K and Type P (e.g. deep KEEP
after a distinct costly DELETE). It is still charged once: the conclusion is
the single inequality w_j≤R_j for interval j; H_j is a fixed sum, not a fund
drawn twice. No credit is created by overlap.

**Disjointness.** R_j=2(H_j−c_j) with H_j over disjoint access sets ⇒ every A
StepEv funds at most one interval's reserve. Baseline StepEvs are distinct
accesses (Lemma 1). Extra StepEvs likewise belong to exactly one I_j.

**Case exhaustion (universal local inequality w_j≤R_j).**
- w_j≤0: R_j≥0 (Lemma 1) ⇒ w_j≤R_j.
- w_j>0 + Type K: Lemma 3.
- w_j>0 + Type P: Lemma 4.
The class hypothesis leaves no fourth case (every positive-debt interval meets
K or P by definition of the domain). ∎
