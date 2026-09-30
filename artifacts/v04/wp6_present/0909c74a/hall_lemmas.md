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

## 8G. E2-HOLE via DELETE-then-KEEP pushers (§11E multiplicity, BOUNDED C41)

B-pushes need nontrivial B-splays, but e_A = 0 pushing accesses exist:
DELETE-z(nonroot) → KEEP-z gives e_A = 0 with a real (stale-deep) B-splash
that pushes others. Such a pusher contributes accA[t] = ∅ to E2 (E2 records
pump-KEEPs only; the supplying DELETE's A-StepEvs are not E2). Hence E2 can
miss existing supply; E3-catch is hub-luck only (sterile possible). Pure
e_A = 0 chains cannot push (repeats are B-no-ops/skips), so every push chain
contains real splays — but E2 attribution still leaks the DELETE half.
Consequence: E2-thinness with B-deep x is structurally possible (triple-
exception conjunction with sterile-E3 + thin-K/E4 + B-heavy); 26k offline
evals show it never saturates to a cut. C41 BOUND: supply-free pushing needs
repeat-cycles (A-root + stale-B-deep), but every repeat-cycle anchors supply at
its run-start (first x-access splays if nonroot → E1 fresh; run-start DELETE
gives pristine-E4 for the victim's own later KEEP via FRESH-CHANNEL case (b)).
Pure e_A = 0 push chains cannot close (repeats without stale-B are B-no-ops;
stale-B repeats need a run-start that supplied). Residual hole: E2 misses the
DELETE half (pump-KEEPs only) + E3-hub-luck + sterile + thin-K/E4 + B-heavy
conjunction. Open (same wall, narrowed to the conjunction).

## 8H. HALL-FRESH-BOUND + NONHEAVY-Q (fresh-disjointness)

Statement: for any B-set Q, Delta(Q) ≤ Σ over Q's B-heavy accesses of
(e_B(j) − 3f_j), where f_j = fresh slots (|E1(j)| case (a); pristine-|E4(j)|
case (b)). In particular a Q with NO B-heavy access never violates
(Delta(Q) ≤ 0) — non-heavy Hall zone law.
Proof: each demanding access j contributes pairwise-disjoint fresh F_j
(E1(j): fresh ids per access; pristine-E4(j): distinct setup accesses across runs
— RUN-STRUCTURE gives ≤1 demanding KEEP per run; mixed E1/E4 double-duty with
BOTH demanding is impossible: E4(j2)=E1(u) forces u = setup[x]-at-j2 with u
demanding, hence u, j2 same-key consecutive demanding accesses with no setup
update between, forcing one x-run with two demanding KEEPs — RUN contradiction;
genesis-T0-root corner demands nothing). Each F_j ⊆ N(Q). So |N(Q)| ≥ Σ f_j and
Delta(Q) = |Q| − 3|N(Q)| ≤ Σ_j (|Q_j| − 3f_j) ≤ Σ_{heavy} (e_B(j) − 3f_j)
(non-heavy terms ≤ 0 since |Q_j| ≤ e_B(j) ≤ 3f_j... precisely |Q_j|−3f_j ≤ 0).
Dependencies: FRESH-CHANNEL, RUN-STRUCTURE, E1-completeness, E4-eligibility,
U=0. GC-independent. (Sums noted for Lean: finset formalization skipped,
author-only.)
Consequence: violators REQUIRE B-heavy accesses (consistent with E1-CAP);
falsifier guidance (B-heavy concentration) + proof halving (non-heavy done).

## 8I. RESIDUAL-SUFFICIENCY SHAPE (Q-specific fresh/overflow)

For Hall subset Q, per access j with Q_j ≠ ∅: F_j = fresh of j (E1(j), or
pristine-E4(j) in DELETE-runs), f_j^Q = |F_j ∩ N(Q)| (Q-specific fresh capacity),
q_j(Q) = |Q_j| − 3|F_j ∩ N(Q)| (Q-specific residual; naive e_B−3f is WRONG when
Q selects some B-events — use |Q_j|). Residual theorem shape: with disjoint
fresh (8H argument) Delta(Q) ≤ Σ_j q_j(Q), and only B-heavy-Q blocks
(q_j > 0) can contribute positively. Non-heavy-Q-block additions are safe
individually; danger = Σ over heavy blocks exceeding shared-old absorption.
This is algebra (8H + per-access split); the old-abundance content is entirely
in bounding shared-old from below (open §10).

## 8J. EXTREME-ACCESS NECESSITY (|Q_L| ≥ 3|U_L|+1)

Let L = latest access in Q (any Q, then specialized to minimal violator):
Q_<L (strictly earlier accesses), Q_L ≠ ∅, U_L = N(Q_L) \ N(Q_<L|) (genuinely
new identities at L). Then |N(Q)| = |N(Q_<L|)| + |U_L| (disjoint by def).
For MINIMAL deficient Q: Delta(Q_<L|) ≤ 0 (strict subset), Delta(Q) = 1, so
1 = Delta(Q_<L|) + |Q_L| − 3|U_L| ≤ |Q_L| − 3|U_L|, i.e. |Q_L| ≥ 3|U_L| + 1.
U_L characterization: new identities at L = aev with ai = L in N(Q_L)
(E2/E4/K/W members all have ai < L — old ids; E3-same-access non-E1 impossible
since E1 = all sited accA[idx]). Hence U_L ⊇ E1(L) (complete edges; E1(L) ∩
N(Q_<L|) = ∅ since ai = L > earlier idx), with equality iff no old-id
first-overlaps at L (W-returns, E2-window shifts, intervening-access young
sources). So |U_L| ≥ e_A(L); violator with E1(L) ≠ ∅ has |Q_L| ≥ 3e_A(L)+1
(Q-heavy AND whole-B-heavy: |Q_L| ≤ e_B(L) forces e_B(L) > 3e_A(L)); with
E1(L) = ∅ (repeat-L) only Q_L ≠ ∅ is forced (demand-without-supply habitat).
(Rigorous; pure algebra + causal edge defs + E1-completeness.)

## 8K. REVERSE-INDUCTION FRAME (GC-STATIC ⇒ single geometric lemma)

Strong induction on |Q|: for arbitrary Q with latest access L,
|Q| = |Q_<L|| + |Q_L||, |N(Q)| = |N(Q_<L|)| + |U_L||; IH gives
|Q_<L|| ≤ 3|N(Q_<L|)| (strictly smaller); suffices |Q_L| ≤ 3|U_L|.
Since |U_L| ≥ e_A(L), non-heavy Q_L (|Q_L| ≤ 3e_A) closes free (8H again);
B-heavy Q_L needs old-new entries (W-first-overlaps, E2-window, intervening
young) covering overflow/3. The induction is clean (no circularity: IH is
strictly-smaller-Hall, the step is access-local geometry). THE single missing
lemma: old-new sufficiency at B-heavy Q-blocks (≡ old-abundance §10).
Slack-transfer (§9) is this induction in cumulative form (sigma_new = sigma_old
+ 3·new − |R|; IH supplies sigma_old ≥ 0 — NOT circular, NOT GC-equivalent;
the dangerous step is exactly the lemma above).

## 8N. EPISODE-TAX + FOURTH-USE VERDICTS (C44 reuse-growth assault)

Definitions (§27.5-6 telemetry): first_Q(a) = earliest B-index in Q adjacent;
bk(a) kth chronological Q-neighbor; incidence split per (a,b): K-inc
(x_b ∈ S(a), ai ≤ acc(b), sited: complete per access) vs W-inc (x_b ∉ S(a),
E3-tagged: ≤3 per splay by OCCUPANCY — each z ∈ S in ≤1 triple, |S| ≤ 3);
others = E1/E2/E4/E7-nonE3 complete-class incidences. Degree ≠ load (§27.20
observed throughout: adjacency is signal, assignment separate).

VERDICTS (fourth.json rerun: 3045 Qs, 31,331 deg≥4):
(a) FOURTH-USE ASCENT (universal) FALSE: E1|E3 fail 2859 (same-access E1 ties),
E2 769 (complete concentration), E3 93, others scattered. E1-last-access-B-heavy
gives companionless deg≥4 maximals universally → DAG (§27.10/13) DEAD as closure
(not weakened: structurally impossible via E1-complete + B-heavy).
(b) W-INCIDENCE FORCING (rigorous): W-inc ≥ 4 ⟹ ≥2 splays (STEPS ≤3/splay),
verified 7943/7943 multi-episode, 0 single. Companions (later-nonrepeat-episode
E1s or dormant-returners): 7943/7943 have them (nocomp 0) — repeat-hole EMPTY
in finite corpus (histories continue; violator-Q-relative version open).
(c) E1/E2/K/E4-complete: EXEMPT (single-access concentration needs no episodes;
fresh machinery covers first-3 loads; §21.A confirmed).
(d) AGGREGATE (F ≤ C·G) DEAD: one later E1 companions unboundedly many earlier
pressures (sharing multiplicity ∞) — no finite C (banked honestly).
(e) Repeat-hole (W-inc≥4, all-later-episodes-repeats, E4-early, no-returners):
0 instances (finite); open as universal (needs repeat-episode W-ladder proof).
Net: fourth-use yields W-conditional-tax + E1-exemption + DAG/aggregate corpses;
GC-STATIC NOT closed (needs the wall: old-abundance for B-heavy Q-blocks).

## 8M. ML-HUB (top-triple universal overlap; connectivity only) (C43)

Statement: the LAST B-StepEv of every nontrivial B-splay is E3-adjacent to the
LAST A-StepEv of every nontrivial past A-splay (all contain root).
Proof: bottom-up splays end in a root-zig (path length ≥ 1 ⟹ final pivot is
root); pushed set ∋ root; triple = pushed ∪ {key} ∋ root on both sides;
sited (U=0); causal (past ai). Code: splay_B_push zig appends {p=root};
splay_A invs contain node/p/g; builders' triple/P|{x} construction exact
(B-node always key, verified node_not_x=0).
Content: CONNECTIVITY (alternating-path/PEEL relevance: hub spokes exist).
Explicitly NOT counts (hub supply = 3 slots per past access = the model
itself; hub-bank vs deep-KEEP demand has no universal sign — deep KEEPs
outrun it; all-deep-Q avoids hub entirely). First-top-injection (+3·#past-lasts
slack) is real but offsettable by elsewhere-deficit. No violator-contradiction
extracted (deep-KEEP + all-deep-Q remain consistent shapes; 46k+ hunts clean).

## 8L. INDUCTION-WITH-CARRY AUTOPSY: SUFFICIENCY CIRCULAR (C42)

Carry version (d_L ≤ sigma_{prev}, i.e. |Q_L| ≤ 3|U_L| + sigma_{prev}):
d_L ≤ sigma_{prev} ⟺ |Q_L| − 3|U_L| ≤ 3|N(Q_<L|)| − |Q_<L|| ⟺
|Q_L| + |Q_<L|| ≤ 3(|U_L| + |N(Q_<L|)|) ⟺ |Q| ≤ 3|N(Q)| = HALL(Q ITSELF).
So carry-sufficiency for Q is BICONDITIONAL with Hall(Q) — assuming carry to
prove Hall(Q) assumes the goal. 8K-sufficiency (strong form without carry, and
carry form alike) is CIRCULAR as a proof strategy: DEAD (banked honestly; this
is the §25-audit trap "inequality equivalent to Hall itself", caught live).
What STANDS: 8J-necessary (violator constraints, no circularity — minimality
applies to strict subsets legitimately); sigma-transfer IDENTITY (pure algebra);
UL-measurements (margin<0 exists: strong step dead empirically too).
Carry-measurement (d_L ≤ sigma_{prev} on full histories, 187/187 holds) =
shortfall-0 restated (biconditional above) — consistent, adds nothing.
The induction frame contributes NO leverage; the wall is bare: old-abundance
must come from elsewhere (or a violator exists).

## Finite status (C38 + C40-8H)

M2 history yields a stalled PEEL 4-core (R=42, N=75, mindeg EXACTLY 4,
Delta=−183, connected, acc span 2–37) with max-flow STILL saturating:
CAP3-PEEL-as-universal REFUTED, GC-STATIC unaffected (recorded distinction).
Killer + ENTRY@3 histories PEEL-empty fully. No Delta>0 anywhere yet.
