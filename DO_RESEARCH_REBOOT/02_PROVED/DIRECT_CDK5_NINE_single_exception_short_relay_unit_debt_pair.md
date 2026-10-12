# DIRECT-CDK5N-SELR — Single-Exception Short-Relay Unit-Debt Pair Repayment

**Status: PROVED — CDK5NSELR-A (universal restricted class).**

## 1. Exact frozen H1–H6

Admissible reachable exactly closed pair-walks. H1: exactly five distinct
genuine KEEP keys; complete marked B-ancestor core nine at every cyclic
state; arbitrary ambient size/length. H2: E={e} UNIQUE bare exception
(c=1,q=3,H=1; w=1,R=0). H3: maximal cyclic successor run after e with
c=1,H=1,q≤2 has length t_e∈{0,1} (maximal, not prefix). H4: U={e,p} with
p≠e, c_p=1, q_p=3, H_p≥2 (distinct unit-debt donor; ¬K_p, ¬P_p; w_p=1,
R_p≥2; same p every clause). H5: ∀j∉{e,p}: w>0 ⇒ (K∨P) (retained for
payment-completeness auditing). H6: Q≤2A (conclusion only). Strict K:
d_A≥3 (H alone insufficient). Strict P: immediately preceding DELETE(y≠x)
with a≥1 both, same interval. Authoritative theorem SHA-256:
`a36eccac9db01f0d92a8721d1eb8b9ecc7782302368cfb0fd63707db3da574fe`
(Gate-0 bytes; proof-stage copies are provenance-separated).

## 2. Source semantics and arbitrary-ambient scope

Banked T0 fixture for witnesses:
`[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null]`;
KEEP splays A+B; DELETE splays A, B frozen; keys never removed; access
key present (absent-key ReplayError: fail-closed); a=⌈d_A/2⌉; KEEP
q=⌊d_B/2⌋; DELETE q=0; exact labeled full pair-state closure (root
equality insufficient). Universal scope: arbitrary ambient BSTs and
reachable states; nine-node marked core bounds genuine-KEEP B-depths by
eight (d_B≤8, q≤4).

## 3. Cyclic intervals and identities

I_j after preceding KEEP through current KEEP: c_j=1[x_j≠x_{j-1}],
H_j=Σa, w_j=q_j−2c_j, R_j=2(H_j−c_j), C_K=Σc; ΣH=A, Σq=Q, Σc=C_K,
Σw=Q−2C_K, ΣR=2(A−C_K) (exact cyclic partition; seam wraps once).

## 4. Universal L1–L10 proof

L1 partition. L2 H≥c baseline (c=1/H=0 freezes A-root, contradicting
different-key KEEP); R≥0; core-nine q≤4; c=0⇒q=w=0. L3 w>0⇒c=1,q∈{3,4},
w∈{1,2}. L4 E={e}: w_e=1,R_e=0; ¬K_e (needs H≥2), ¬P_e (needs a≥1 both):
e untyped. L5 donor: U={e,p}; c_p=1,q_p=3,H_p≥2 ⇒ w_p=1,
R_p=2(H_p−1)≥2; w_e+w_p=2≤R_p from R_p alone. L6 sharp H_p=2,q_p=3:
w_e+w_p=R_p=2 equality (algebraic; NO physical H=2 witness claimed —
frozen IN donor is H=18); q_p=4,H_p=2 excluded (3>2). L7 others:
predicates-first strict K/P ⇒ H≥2 ⇒ R=2(H−1)≥2≥w; w≤0 trivial. L8
disjoint pair+singletons (e≠p; overlap counted once; relay pays
nothing; no double-count). L9 telescoping Σw≤ΣR ⇒ Q≤2A (IN: 4≤74 ⇒
36≤106; OUT: 36≤104). L10 scope/redundancy/noncircularity (H3
classifies only; H5 retained; H4 q=3/H≥2 load-bearing; no aggregate
premise; no generalization). ∎

## 5. Joint payment, sharp boundary, no-double-spend

Exactly one mechanism: {e,p} jointly from R_p; every other positive debt
from its own R_j. IN: p=0 (H=18,q=3,c=1,w=1,R=34; 1+1=2≤34); ¬K (dA=0);
¬P (prev DELETE same key). Others: j=8 K(dA=3)+P (single cover); j=12
K(dA=4). H=2 boundary symbolic only (sharp-case audit).

## 6. IN certificate

`8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd`
(31 accesses, A=53, Q=36, C_K=16): five keys {1,3,5,7,9}; core-nine ×32;
closure; 31/31 distinct states; E={4} (H=1,c=1,q=3,w=1,R=0); successor
j=5 (c=1,H=2,q=2) ⇒ maximal relay t=0; U={0,4}; Σw=4, ΣR=74
(4≤74 ⇒ 36≤106). Q−2A=−70 (no violation).

## 7. OUT certificate (properness)

`c3a55f13475c6ca0d75cfa8b0e355510171d19a73b250cab173ddc5fc431ec9e`
(30 accesses, A=52, Q=36, C_K=16): same backbone (five keys, core-nine,
closure, 30/30 states); E={4,12} (both H=1,c=1,q=3,w=1,R=0) breaks H2;
U={0,4,12}. OUT = IN minus DELETE(8) at original index 18 (selr-in d1
rm18); first-eligible in canonical order (rm0/rm1 non-closed, rm2
S1-banked, rm5 AMG+UESINK-banked, rm12 SELR-member, rm13/rm16
non-closed). Q−2A=−68 (properness role only).

## 8. C24* proof closure (corrected, rotation-aware)

C_0 = Rot(B_24) ∪ Z (all n whole-cycle rotations from true boundary
starts at every subproblem + certified zero-cost leaves); additive
closure over proper exactly closed children (actual starts, exact
additive costs, strictly shorter). Engines: DP boundary checker +
independent DFS checker (shared disclosed primitives; 15/15 agreement
incl. rotated queries). Soundness by induction; completeness relative to
calculus (caps/unknowns ⇒ INDETERMINATE, never negatives). IN: 31×24=744
EXCLUDED; OUT: 30×24=720 EXCLUDED (1,464 per-entry verified); primitive
roots ⇒ no proper decomposition; UNCOVERED both (0 unknowns).

## 9. Novelty, properness, provenance

∅≠(S_SELR∩R_5,9^(24))⊊R_5,9^(24) (IN member/residual; OUT
residual-nonmember; first-eligible provenance reconstructed; 384-word
corpus 378+6 unchanged; 27-case oracle; 90-audit 70exec/3hybrid/17proof
normal+-O; 16/16 fault injections incl. recognizer-unknown/raises→
INDETERMINATE, matrix-flip localized, budget-forced). Gate-0 errata A–F
adjudicated append-only (IN 36≤106 corrected; 19-vs-22 count corrected;
rotation repair with no witness change; recognizer wiring repaired;
-O-safe checks; rich certificates).

## 10. Limits

Exactly this class. No H3/H5 removal, no long-relay/multi-exception/q=4
generalization, no witnessed H=2 donor, no complement closure, no K≥6,
no universal Coarse-Double, no Dynamic Optimality. Payment universal;
novelty relative to frozen pre-SELR bank24.
