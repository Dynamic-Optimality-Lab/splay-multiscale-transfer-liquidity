# 26AO: order-expanded consecutive-positive repayment (PROVED + OUTCOME A)

**Status: PROVED** — universal consecutive-positive four-block theorem,
two-order packet theorem with deterministic recognizer, certified ten-key
witness, strict extension beyond 26AN and all prior domains. No J4,
ROW-DIAMETER, J-SELF, DTQ, UG, potentials, LP, or compactness used. No claim of
arbitrary permutation invariance; exactly two credit orderings covered.

## AO-L1 — shallow-access credit (PROVED, source arithmetic)

AO-P3 (1≤d_B(z)≤3, a≥1): q=⌊d_B/2⌋≤1, δ=q−2a≤−1. (Same defs as 26AN-L1.)

## AO-L2 — former-root depth after two intervening splays (PROVED)

After nontrivial splay of x: d_B(r)≤2 (26AJ Lemma 2). Two subsequent genuine
B splays (neither accessing r, per AO-P2/P3 distinctness): 26AL-L1 twice gives
d_B(r)≤6, so the delayed KEEP of r has q≤3.

## AO-L3 — final credit (PROVED)

a_final≥2 gives δ_final≤3−4=−1. Independent of AO-L1; no aggregate assumed.

## 26AO-P — consecutive-positive theorem (PROVED)

Distinct consecutive cyclic blocks with P1 (δ_i=1, genuine splay of x,
former root r), P2 (genuine splay, δ_{i+1}=1, y≠x,r), P3 (genuine splay of
z≠y,r at 1≤d_B≤3, a≥1), P4 (block i+3 led by r with KEEP of r, interveners
keyed ≠r), P5 (a_{i+3}≥2), P6 (distinct), P7 (no geometry): 1+1+(≤−1)+(≤−1)≤0.
Universal over all finite BST states meeting the source conditions.

## Two-order packet theorem (PROVED)

P_two-order = P_26AN ∪ P_26AO with exact banked/new hypotheses (Type I
inherits 26AN-P verbatim; Type II uses AO-P1–P7). Deterministic recognizer:
m cyclic cuts × memoized DP (singleton-if-nonpositive / Type I / Type II,
fixed option order), O(m²) packet tests, emits cut/anchors/types/singletons.
Sound: accepted packets satisfy proved theorems; positives all covered;
singletons nonpositive; blocks disjoint — Σδ≤0, Q_B≤2A. Complete per cut by
DP exhaustiveness; some cut aligns with a certificate boundary, so every
admissible walk is accepted — hence C_26AN ⊆ C_two-order recognizably (no
greedy-completeness gap). Handles zero-positive/m<4 (P6 vacuous ⟹ accept iff
all nonpositive)/m=4/wrap/multi/mixed/repetition. Admissibility not claimed
universal.

## Witness + strict novelty (OUTCOME A)

Ten-key walk (certified 18/18 table, 27/27 engines, A=34/Q=19/W=−49): sole
positives blocks 1,2 (K7,K5, +1,+1); Type II packet {1,2,3,4}=(+1,+1,−1,−3);
r=1 with depth trajectory 1,1,2; r'=7; K5,K9 genuine. Recognizer accepts
(Type II @0); zero Type I matches anywhere ⟹ γ*∉C_26AN. K7: succ 5≠1
(AJ ✗), i+2 key 9≠1 (AK/AL-G/AL-S ✗), δ(i+1)=+1 (AM-G/AM-S ✗), slot-1
positive (26AN-I ✗). K5 (r'=7): succ 9,1,2 ≠7 (AJ/AK/AL-G/AL-S ✗; AM-G G4:
i+3 key 2≠7 ✗); as Type I anchor slot-2 K2 nonpositive ✗. n=10, depths 7,6,
A=34 (zero-A/n≤6/bounded-depth ✗). Hence C_26AN ⊂neq C_two-order and
C_old ⊂neq C_old∪C_two-order. 26AM Outcome B preserved.

## Scope

Two orderings only: (+1,≤−1,+1,≤−1) or (+1,+1,≤−1,≤−1). NOT covered:
three-plus liabilities, other permutations, general allocation, unrestricted
Coarse-Double. Downstream (PIVOT-2/LT/DO) unchanged.
