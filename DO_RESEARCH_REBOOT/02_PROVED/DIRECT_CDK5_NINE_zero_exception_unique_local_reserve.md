# DIRECT-CDK5N-COMP-ZULR — Zero-Exception Unique Local-Reserve Repayment

**Status: PROVED — CDK5NZULR-A (universal restricted class).**

## 1. Exact frozen H1–H6

Admissible reachable exactly closed pair-walks. H1: exactly five distinct
genuine KEEP keys; complete marked B-ancestor core nine at every cyclic
state; arbitrary ambient size/length. H2: E={j:c=1,q=3,H=1} EMPTY (zero
exceptional intervals; q=4,H=1 debts NOT excluded by this alone). H3:
U={j:w>0,¬K,¬P} has EXACTLY ONE element p (unique untyped positive payer).
H4: H_p≥2 for that same p (intrinsic local solvency; no borrowed credit).
H5: ∀j≠p: w>0 ⇒ (K∨P) (same p; completeness of classification). H6: Q≤2A
(conclusion only; no aggregate premise). Strict K: d_A≥3 (H alone
insufficient). Strict P: immediately preceding DELETE(y≠x) with a≥1 both,
same interval (earlier DELETE insufficient). H2/H5 retained as stated even
though H2 is implied by H3+H4 under source definitions (nonfatal redundancy
note). Authoritative bytes: Gate-0 `ZULR_frozen_theorem.md` (SHA-256
`e39e8447c08b3cd5adc8dad1d505cad7f0008ae222ecc1a27bad34aa97c0a447`).

## 2. Source semantics and arbitrary-ambient scope

Banked T0 fixture for witnesses:
`[9,[6,[1,null,[2,null,[5,[4,[3,null,null],null],null]]],[8,[7,null,null],null]],null]`;
KEEP splays A+B; DELETE splays A, B frozen; keys never removed; access key
present (absent-key fail-closed); a=⌈d_A/2⌉; KEEP q=⌊d_B/2⌋; DELETE q=0;
exact labeled full pair-state closure (root equality insufficient).
Universal scope: arbitrary ambient BSTs and reachable states; the nine-node
marked core (ancestor-closed path union) bounds genuine-KEEP B-depths by
eight definitionally (d_B≤8, q≤4).

## 3. Cyclic intervals and identities

I_j from just after the preceding KEEP through the current KEEP:
c_j=1[x_j≠x_{j-1}], H_j=Σa, w_j=q_j−2c_j, R_j=2(H_j−c_j), C_K=Σc;
ΣH=A, Σq=Q, Σc=C_K, Σw=Q−2C_K, ΣR=2(A−C_K) (genuine cyclic partition; each
access in exactly one interval; seam wraps exactly once).

## 4. Universal L1–L9 proof

L1 partition identities (above). L2 baseline + debt: H≥c (c=0 trivial; c=1
with H=0 would freeze the A-root at the previous key, contradicting a
different-key KEEP), so R≥0; core-nine gives q≤4 for genuine KEEPs; c=0 ⇒
q=0 ⇒ w=0; hence w>0 ⇒ c=1, q∈{3,4}, w∈{1,2}. L3 zero-exception
classification: E=∅ excludes (1,3,1) slots but NOT (1,4,1) w=2/R=0 — those
need H3/H5 reserve, never H2 (invalid inference explicitly rejected). L4
unique self-payer + sharp case: U={p} (H3), H_p≥2 (H4); with c_p=1,
q_p∈{3,4}: R_p=2(H_p−1)≥2 ≥ w_p=q_p−2 intrinsically, no borrowed credit;
sharp q_p=4,H_p=2: w=2,R=2, equality 2=2 (included); q_p=3,H_p=2: 1≤2; no H≥3
requirement. L5 others, predicates first: j≠p; w≤0 ⇒ w≤R; w>0 ⇒ strict-K
(d_A≥3 ⇒ a≥2 ⇒ H≥2) or strict-P (a≥1 both ⇒ H≥2) by H5; with c=1,
R=2(H−1)≥2≥w (H≥2 is a CONSEQUENCE, never the definition). L6 no double
spending: every interval pays only its own debt; no sink introduced; no
credit transfers; no reserve reused; K/P overlap never duplicates credit. L7
telescoping: Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K) ⇒ Q≤2A. L8 classification independence
(E=∅/uniqueness/H≥2 classify only; no sink/relay/transfer in any payment
step). L9 hypothesis audit (H2 redundant under H3+H4, retained; H3/H4
load-bearing; no generalization claimed). ∎

## 5. Unique payer, strict K/P, no sink

Exactly one mechanism: the single untyped positive interval self-finances
from its own H≥2 A-credit; every other positive debt is locally strict-K/P
financed. No borrowed sink, no packet, no potential, no unproved global
assumption. IN: p=0 (H=18,q=3,c=1,w=1,R=34; 1≤34 intrinsic); strict-K fails
(current KEEP A-depth 0); strict-P fails (preceding DELETE targets same key).
Other IN positives: j=4 strict-K (dA=4); j=8 strict-K (dA=3) + strict-P
(prev-D4 distinct, a≥1 both); j=12 strict-K (dA=4).

## 6. IN certificate

`593b3f3ac56101755ea8995a8c87fd35ed73ba54cec8b5ef16f296d2d44945b9`
(32 accesses, A=56, Q=36, C_K=16): five genuine KEEP keys {1,3,5,7,9};
core-nine at all 33 boundaries; exact full pair-state closure; 32/32 distinct
pre-closure pair states; E=∅; positives exactly {0,4,8,12}; unique untyped
payer p=0; Σw=4, ΣR=80 (4≤80 ⇒ 36≤112). Q−2A=−76 (no violation).

## 7. OUT certificate (properness)

`8cd970c71989fc3c4c852192a858a3d7f70d7e0b6db85f0a7fabb6d7add894bd`
(31 accesses, A=53, Q=36, C_K=16): same validity backbone (five keys,
core-nine throughout, closure, 31/31 distinct states); complete exception
set E={4} (H=1,q=3,c=1,w=1,R=0) breaks frozen H2; outside the full pre-ZULR
C23* banked closure. OUT = IN minus DELETE(8) at zero-based original access
index 7 (in-L1 idx4 rm7); first qualifying residual in canonical order
(idx0 rm0 non-closed; idx1 rm1 non-closed; idx2 rm2 NP-banked; idx3 rm5
ZULR-member; idx4 rm7 OUT). Q−2A=−70 (no violation; properness role only).

## 8. Recursive novelty (relative to pre-ZULR bank C23*)

Bank23 = 3 foundations (RT2/CDK4/CDK5L) + 8 five-key nine-core
(NP/S1/S2/VR/MR/MSINK/DLSS/UESINK, each with exact existential sink-domain
conditions at every legitimate recursive level) + 12 packets
(26AJ/26AK/26AL-G/26AL-S/26AM-G/26AM-S/26AN/26AO/26AP/26AQ/26AR/26AS);
ZULR excluded from its own baseline. IN: 32 rotations × 23 domains = 736
decisions, all EXCLUDED; OUT: 31 × 23 = 713, all EXCLUDED (1449 total);
one root subproblem per primitive witness; zero proper pair-closed children;
zero indeterminates; two independent engines agree (18/18 cross-validation);
19/19 recursive oracle (battery identical to Gate-0); 384-word corpus
regression (378 direct-banked + 6 cyclic-additive, 0 residual, 0
indeterminate); 90-obligation adversarial audit PASS (normal + -O) with 7
real fault injections all detected. Hence ∅≠(S_ZULR∩R_5,9^*)⊊R_5,9^*.

## 9. Dependencies and provenance

Source semantics; cyclic interval partition; A-root-change baseline;
nine-core bound; zero-exception/unique-payer predicates; strict K/P;
per-interval payment; telescoping. Novelty: 23-inventory, rotation
applicability, recursive soundness/completeness, IN/OUT negative
certificates, proper-subclass proof, frozen OUT provenance with honest R3
adjudication (pre-generated parent list = identity registration; SHA-dedup
equivalent to exact-canonical order on the executed frontier; budget guards
untriggered with 0 hits; manifest prose count corrected to 441 raw / 425
distinct). Novelty dependencies are not payment premises. Nonfatal records:
proof-stage frozen-theorem copy carries a two-line provenance footer (audited
content-identical; Gate-0 bytes authoritative); hypothesis redundancy H2/H5
(retained); Gate-0 adversarial mix of exec/proof kinds (this stage labels
every check and executes the executable class ±O).

## 10. Limits

Exactly this class. No remaining-complement closure, no H3-free
generalization, no K≥6, no universal Coarse-Double, no Dynamic Optimality.
Payment universal over H1–H5; novelty relative to the frozen pre-ZULR bank23.
