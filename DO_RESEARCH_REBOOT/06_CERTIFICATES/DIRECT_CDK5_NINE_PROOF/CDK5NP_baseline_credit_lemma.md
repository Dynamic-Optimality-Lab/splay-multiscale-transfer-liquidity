# Lemma 1 — baseline A-credit (PROVED universally)

**Claim.** H_j≥c_j for every interval; hence R_j=2(H_j−c_j)≥0.

**Proof.** c_j=0: trivial (H_j≥0). c_j=1: x_j≠x_{j−1}. Immediately after KEEP
j−1, A is rooted at x_{j−1} (KEEP splays A to its key — source semantics).
KEEP j ends with A rooted at x_j≠x_{j−1}. A-root changes only at accesses
targeting a non-root key; the first such access in I_j has pre-depth ≥1 ⇒ a≥1.
Thus H_j≥1=c_j (cyclic wraparound uses exact A closure: the seam interval's
endpoints are consistent labeled states). Reserve that first StepEv as the
interval's baseline; intervals are disjoint ⇒ baselines are distinct accesses
⇒ no double reservation. ∎

Finite illustration (not proof): witness K3-interval contains D4(a=1)+K3(a=1).
