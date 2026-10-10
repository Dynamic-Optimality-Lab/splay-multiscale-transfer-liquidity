# S1 two-interval universal proof (NEW — independent of CDK5NP-A Type K/P audit)

Proves §7 L1–L6 for arbitrary source-valid walks satisfying the frozen S1
hypotheses (five keys, nine-core, one exception (c=1,q=3,H=1), successor
(c=1,q≤3,H≥2), all other positive debts Type K/P). The Type K/P *theorem* is
reused for unchanged supporting facts (baseline H≥c, debt bound w≤2, per-type
H≥2⇒R≥w); everything about the exception, successor, pairing, and disjointness
is proved here, not imported.

## S1-L1 (reserves)

Banked interval partition (disjoint cyclic cover; ΣH=A, Σq=Q_B, Σc=C_K) +
baseline H_j≥c_j (A-root-change argument) ⇒ R_j≥0 ∀j. Holds for the S1 class
since it uses only source semantics + closure, no packet premise.

## S1-L2 (exceptional debt)

c=1,q=3,H=1 ⇒ w=3−2=1, R=2(1−1)=0. Type K would need H≥2 (d_A≥3⇒a≥2);
Type P would need H≥2 (two distinct costly accesses). H=1 excludes both —
so the exception is disjoint from CDK5NP-A by construction (not by total).

## S1-L3 (successor capacity)

c=1,q≤3,H≥2 ⇒ w=q−2≤1, R=2(H−1)≥2 ⇒ w_*+w_k≤1+1=2≤0+2=R_*+R_k. Valid with
w_k=1 (joint reserve pays both) or w_k≤0. No key identities used beyond the
frozen inequalities — the proof is structural, not witness-specific.

## S1-L4 (remaining intervals)

w≤0 ⇒ R≥0 suffices; w>0 ⇒ frozen K/P (H≥2⇒R≥2≥w, w≤2 by nine-core debt bound
q≤4: nine nodes ⇒ d_B≤8; c=0⇒q=0 via B-root + frozen DELETEs).

## S1-L5 (disjointness)

s≥5 KEEP occurrences (five genuine keys ⇒ s≥5) ⇒ j_*≠k=j_*+1 mod s. Partition
{pair} + singletons is disjoint and exhaustive. The pair's combined reserve is
spent once; the successor is never recharged even if independently K/P-eligible
(mandatory no-double-spend). Every StepEv lies in one interval.

## S1-L6 (telescoping)

Σw≤ΣR ⇒ Q_B−2C_K≤2(A−C_K) ⇒ Q_B≤2A. Arbitrary n (marked paths only), length
(finite sums), DELETEs (exact H sums), prefixes (cycle-only), seams (closure).
No AJ–AS premise — hence strict novelty is meaningful.

**Rule 2: PASS.** Complete universal implication from frozen hypotheses.
