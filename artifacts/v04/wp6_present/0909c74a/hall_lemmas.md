# Generic minimal-Hall lemmas (author-level PROVED — pure combinatorics)

Status: PROVED_AUTHOR. No splay content; applies to ANY bipartite causal graph
with left side B (demand 1) and right side A (capacity 3). Arithmetic cores
AR-20/AR-21 kernel-checked (`lean/WP6/StageBArith.lean`, exit 0).
Date: 2026-09-30 (C38). Dual tooling: `scripts/wp6_hallcore.py`.

For left Q ⊆ B: N(Q) = distinct adjacent A identities; Delta(Q) = |Q| − 3|N(Q)|
(truncated at 0 in code; prose uses exact integers — sign agrees for Delta>0).

## 8A. MINIMAL-DEFICIT-ONE

Statement: inclusion-minimal deficient Q (Delta(Q) > 0, no proper deficient
subset) satisfies Delta(Q) = 1, i.e. |Q| = 3|N(Q)| + 1.
Proof: for every b ∈ Q, Q\{b} is non-deficient: |Q|−1 ≤ 3|N(Q\{b\})| ≤ 3|N(Q)|.
Deficiency: |Q| ≥ 3|N(Q)|+1. Forced equality. (AR-20 is the arithmetic core.)

## 8B. NO LOW-DEGREE SOURCE IN A MINIMAL VIOLATOR

Statement: with deg_Q(a) = |{b ∈ Q : a ∈ N(b)}|, every a ∈ N(Q) has deg ≥ 4.
Proof: else some a has r ≤ 3; R = its Q-neighborhood; Q' = Q\R has
|N(Q')| ≤ |N(Q)|−1 (a absent), so Delta(Q') ≥ |Q|−r−3(|N(Q)|−1)
= Delta(Q)+3−r ≥ 1 — a smaller deficient set, contradiction. Q'=∅ boundary:
then N(Q')=∅, Delta=0, contradicting Delta ≥ 1 (so Q' is nonempty automatically).
(AR-21 is the peel-step identity.)

## 8C. CONNECTED MINIMAL CORE

Statement: an inclusion-minimal deficient Q may be taken connected in the
induced bipartite graph on Q ∪ N(Q).
Proof: components have disjoint source neighborhoods (else connected); deficit
is additive Delta(Q) = Σ Delta(Q_i). Positive total ⟹ some component positive;
every vertex has an edge (A-side by N-definition; B-side by eligibility
nonemptiness, banked trichotomy), so a positive component is a STRICT deficient
subset unless unique. Minimality forces one component.

## Consequence (sharp violator signature)

Any genuine Hall counterexample contains an inclusion-minimal core with
|Q| = 3|N(Q)|+1, min source degree ≥ 4, connected. (§8D CAP3-PEEL route and
§13 extreme-access attack target exactly this signature.)

## 8E. LATEST-ACCESS CONSTRAINT (E1-only-same-access)

Statement: fix a residual/violator B-set R with latest access L (max acc idx).
Every E1(L) source is eligible ONLY for access-L members of R (same-access
E1/E3; E2/E4/E3-past need strictly earlier ai, but ai = L is latest).
Hence deg_R(a) = |R_L| exactly for sited a ∈ E1(L) (E1 edges complete).
Corollary (violator): if E1(L) ≠ ∅ then |Q_L| ≥ 4 (else mindeg ≥ 4 violated).
If E1(L) = ∅ (L repeat), L contributes demand with zero same-access supply —
the violator's natural habitat (demand-without-supply); C37 killer is case (a)
with E1 created, so its online kill is NOT a Hall violator (offline saturates).
Proof uses only causal edge defs + E1 completeness + B-freeze/T3 + root no-op.
Check: killer acc8 (E1={98}, |Q_8|... consistent); M2 4-core spans acc 2–37.

## 8F. ONE-ACCESS HALL STATUS (open, same wall)

Q_j (B-events of one access j): E1(j) ⊆ N(Q_j) always (complete edges), so
|N(Q_j)| ≥ e_A(j). One-access Hall (|Q_j| ≤ 3|N(Q_j)|) holds unless B-heavy
with sterile-thin old (e_B > 3e_A and E2/E4/K/W thin). Same wall as global
(old-abundance); fractal at access scale. Finite: 26k+ offline evals (which
subsume one-access violations as shortfalls) clean. Unproved.

## 8G. E2-HOLE via DELETE-then-KEEP pushers (§11E multiplicity)

B-pushes need nontrivial B-splays, but e_A = 0 pushing accesses exist:
DELETE-z(nonroot) → KEEP-z gives e_A = 0 with a real (stale-deep) B-splash
that pushes others. Such a pusher contributes accA[t] = ∅ to E2 (E2 records
pump-KEEPs only; the supplying DELETE's A-StepEvs are not E2). Hence E2 can
miss existing supply; E3-catch is hub-luck only (sterile possible). Pure
e_A = 0 chains cannot push (repeats are B-no-ops/skips), so every push chain
contains real splays — but E2 attribution still leaks the DELETE half.
Consequence: E2-thinness with B-deep x is structurally possible (triple-
exception conjunction with sterile-E3 + thin-K/E4 + B-heavy); 26k offline
evals show it never saturates to a cut. Open (same wall).

## Finite status (C38)

M2 history yields a stalled PEEL 4-core (R=42, N=75, mindeg EXACTLY 4,
Delta=−183, connected, acc span 2–37) with max-flow STILL saturating:
CAP3-PEEL-as-universal REFUTED, GC-STATIC unaffected (recorded distinction).
Killer + ENTRY@3 histories PEEL-empty fully. No Delta>0 anywhere yet.
