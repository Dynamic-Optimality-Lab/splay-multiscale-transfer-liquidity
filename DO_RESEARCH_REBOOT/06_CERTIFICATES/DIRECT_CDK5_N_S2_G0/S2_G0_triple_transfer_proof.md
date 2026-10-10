# S2 triple-transfer universal proof audit (L1–L7, all n/lengths)

## S2-L1

H≥c/R≥0 (banked A-root-change argument, restated scope: identical semantics;
applies since S2 uses the same intervals). Debt w∈{1,2} for positives
(nine-core d_B≤8⇒q≤4; c=0⇒q=0 via B-root + frozen DELETEs). Q_B≤2C_K NOT
claimed (nine-node +2 refutation cited). PASS.

## S2-L2

Exception (1,3,1): w=1,R=0; H=1 excludes K (needs H≥2) and P (needs two costly
accesses) universally. S2∩CDK5NP-A=∅ by construction. PASS.

## S2-L3

Successor (c=1,H=1,q≤2): w=q−2≤0, R=0. No reserve, no debt — precisely the
S1-uncovered case (S1 needs H≥2). PASS.

## S2-L4

Second successor (c=1,H≥2,q≤3): w≤1 (covers q∈{0..3} ⇒ w∈{−2..1}), R≥2. PASS.

## S2-L5 (triple)

w_*+w_k+w_l ≤ 1+0+1 = 2 ≤ 0+0+2 ≤ R_*+R_k+R_l (using worst allowed values;
actual witness triple 1+0+0≤0+0+2). Joint charge, once. PASS.

## S2-L6 (others)

w≤0 via R≥0; w>0 via K (H≥2⇒R≥2≥w) or P (same) — K/P overlap charged once
(fixed H sums). Hypotheses exhaust positives outside the triple. PASS.

## S2-L7 (partition + global)

s≥5 (five genuine keys) ⇒ j*,k,l distinct mod s. {triple}+singletons disjoint,
exhaustive; k,l never recharged (even if K/P-eligible). Σw≤ΣR ⇒ Q_B−2C_K≤
2(A−C_K) ⇒ Q_B≤2A. Arbitrary size/length/DELETEs/prefixes/seams; no packet,
potential, or aggregate premise. PASS.

**Mechanism VERIFIED universally. No new splay lemma needed (uses banked
nine-core + interval results only).**
