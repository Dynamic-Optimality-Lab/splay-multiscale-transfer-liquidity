# 26AP: variable-length bulk repayment (PROVED + OUTCOME A)

**Status: PROVED** — parameterized depth lemma, signed bulk-repayment theorem,
global maximal-run theorem, O(m) cut-independent recognizer, certified 16-key
p=3 witness, strict extension beyond 26AO and all prior domains. No J4,
ROW-DIAMETER, J-SELF, DTQ, UG, potentials, LP, or compactness. No claim of
witnesses for all p; no credit transfer between runs.

## 26AP-L1 — parameterized former-root depth (PROVED, induction)

p≥1 consecutive unit-positive (δ=1) blocks; each has q≥3 (a≥1), hence a genuine
B-changing KEEP (at most one per block). Let r = B-root before block i's splay:
after it d_B(r)≤2 (26AJ Lemma 2, h_i∈{1,2} sharp form d≤h_i+2(p−1)). Each of the
next p−1 blocks splays B at most once; 26AL-L1 (d'≤d+2) per splay — applied
once per genuine intervening B splay (N8), not per rotation — gives
d_B(r)≤2+2(p−1)=2p. Hence q_return=⌊d/2⌋≤⌊(h_i+2(p−1))/2⌋≤p. No geometry.

## 26AP-L2 — signed bulk return (PROVED)

Return block led by r with KEEP of r (B frozen within block before it) and
source-tested a_return≥p (⟺ d_A(r)≥2p−1; an explicit restriction, N9):
δ=q−2a≤p−2p=−p. Derived, not assumed (N10).

## 26AP-P — variable-length unit-run repayment (PROVED, all p≥1)

Distinct consecutive blocks B_i..B_{i+p} with P1 (δ_j=1, j<i+p), P2 (r = former
root at i), P3 (block i+p led by r, KEEP of r), P4 (a_{i+p}≥p), P5 (distinct),
P6 (no geometry): run sums to p (L1 gives q-structure; P1 is the hypothesis),
return ≤−p (L2); total ≤0.

## Global maximal-run theorem (PROVED)

Class C_26AP (R1–R6): maximal cyclic unit-positive runs, each followed
immediately by its first-block-root return with a≥p; returns unique per run
(R6: no return serves two runs, no return lies in a run); rest nonpositive.
Run+return groups satisfy 26AP-P (≤0), are disjoint, cover all positives;
Σδ≤0 ⟹ Q_B≤2A. Cases: no positives (trivial), p=1, several runs, wraparound,
m=1 (positive needs a distinct return — impossible, so positive m=1 walks are
correctly excluded), all-positive (rejected: no distinct return), repetition.

## Recognizer (PROVED sound/complete/cut-independent, O(m))

Amended cut: no positives→ACCEPT; all positive→REJECT; else smallest-index
nonpositive j, linearize j+1..j, one scan (run = maximal positives, each
verified =1; return = next block with leader/KEEP r and a≥p; else singleton).
Sound (accepted ⟹ R1–R6 ⟹ theorem); complete for C_26AP (scan is forced —
maximal runs are unique, returns pinned); cut-independent (cut after a
nonpositive never splits a cyclic run; run/return identities are trace-
intrinsic; verified: all 24 cuts agree on witness); rotation-invariant;
O(m) time / O(m) space on precomputed metadata.

## Witness + novelty (OUTCOME A)

16-key vine start; 9-DELETE prefix (B stays vine); 29-access cycle, exact
A/B closure + repetition closure; 29/29 table; A=46,Q=27,W=−65; 27 blocks
(two a=0 no-ops grouped, N5); positives exactly blocks 0,1,2 (+1,+1,+1);
packet (+1,+1,+1,−4)=−1; roots 1/11/9; r-trajectory 2,2,4 (≤6 ✓); K11 a=2
(N6); engines 38/38. 26AP ACCEPT (p=3, return a=3). 26AO banked recognizer
(sha256 4f4b40e0…) REJECT, zero Type I/II candidates; parity (2k positives
per accepted walk — banked lines 15/39/45/78 + proved slot-1/3 signs) confirms
odd-3 exclusion. Per-block AJ/AK/AL/AM exclusions (successor keys, G3/G4,
non-unit intermediates); n=16, depths 10/6/6, A=46. ⟹ γ*∈C_26AP∖C_old;
C_old⊂neqC_old∪C_26AP. 26AM Outcome B preserved.

## Scope

Unit runs + immediate returns only. NOT covered: non-unit deficits,
nonconsecutive liabilities, inter-run credit, arbitrary returns, unrestricted
Coarse-Double. Downstream unchanged.
