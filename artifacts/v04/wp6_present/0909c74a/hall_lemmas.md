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

## 8M. ML-HUB REFUTED + NARROW SYNC-HUB (C46 autopsy of C43 claim)

ML-HUB-as-universal (top-triple universal root-overlap) is REFUTED.
Exact witness (C37 killer, n=128 left-vine): acc8-KEEP-19 top B-triple
[18,19,123] vs past A-last-triples acc0 [1,128], acc1 [1,20], acc2 [12,20],
acc3 [1,10,12], acc5 [10,12]: FIVE of six disjoint (only acc6 [12,18,20]
meets at 18). Root MIGRATES every access (rotations involving root descend
it; mid-splay transient roots differ per step); there is NO universal hub key.
The C43 "root" argument conflated pre-splay root (stable label) with triple
membership (mid-splay configurations). Consequence: hub-supply is not
universal; top-sterile is possible; the wall stands longer (consistent with
zone-theory/C37-drain).
NARROW SYNC-HUB (surviving, proved): x-top-B-triple ∋ B-root-before (w) by
top-pivot mechanics (final zig/double involves root) and w-access A-triples ∋
w (node always w); hence E3(x-top, sited-accA[w]) ∋ w ≠ ∅ — PROVIDED w-access
is nontrivial-A (e_A(w) ≥ 1; else accA[w] empty). Killer consistent: w=18 via
trivial acc7 (repeat, e_A=0) → hub EMPTY; aev97 connects via pushed-18 (zone,
not hub). So tops get hub-neighbors iff B-root-before's own access was
nontrivial (else zone-only). Narrow, honest, no counts content.

[C43 ORIGINAL 8M BODY — SUPERSEDED C46, preserved for audit:]
Statement: the LAST B-StepEv of every nontrivial B-splay is E3-adjacent to the
LAST A-StepEv of every nontrivial past A-splay (all contain root).
[Status of the above two lines: REFUTED by killer witness (5/6 past lasts miss
acc8-top; transient roots). The error: "root" conflated pre-splay label with
mid-splay configurations; root migrates every access. Original C43 proof text
resides in git history (commit a5bc427); not reproduced here since false.]

## 8P. DISPLACEMENT-SUPPLY COUPLING + SURGICAL FIZZLE (C46)

Claim (refined conjunction, open): supply-free B-heavy needs ALL of
avoidance (x untouched in A: no x-triples created) + repeat-pushers (e_A=0
B-splashes: E2-hole) + sterile zone (no E3-overlap of pusher paths).
Evidence: surgical first-x-strike (wp6_surgical.py, 8k evals, first-x + zone
avoidance + repeat-pushers): shortfall 0 throughout, best slack 34 (LOOSE) —
the construction fizzles because B-heavy requires asymmetric displacement
(A-shallow + B-deep), and displacing x TOUCHES x (hoist-rotations carry x in
triples → E3-fodder; pushes come with pumpers → E2 unless repeat-holed!) while
undisplaced x isn't B-heavy (E1 covers: e_A ≈ e_B at T0-depths).
Why repeats don't save the conjunction: repeat-pushers are single-shot
(B-root after splash); rebuilding needs displacing accesses (which supply);
run-starts anchor supply (C41 bound). Residual hole (all three at once) open.
Surgical fizzle is FINITE_EVIDENCE for coupling, not a theorem.

SG2 sharpening (C48): T0-shallow-x (depth<=6, E1 1-3 naturally thin) + pushes +
avoidance + repeats + sterile, 10k evals (wp6_surgical2.py → surgical2.json):
shortfall 0, best slack 27. Strike-shape diagnostic: e_B>=8 NEVER occurs at
strikes (300 histories) — pushing B-deep while holding A-shallow+sterile fails;
pushers' B-paths through x force A-contact (shapes correlate via synced roots)
or miss x in B (no push). Push/avoidance incompatibility is the forcing behind
the fizzle (finite face). E2-alone arithmetic (push-supply ≈ demand order)
suggests E2 nearly covers first-x-access demand; root-pusher fraction bounded
by single-shot+rebuild (C43); residual = sterile-rebuild sustain (open).

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

## 8O. POOL-DEFICIT BOUND + SUPPLY-AVENUE EXHAUSTION (C45)

Bound (author): for any Q, with FRESH-UNION F = ⊔ demanding-access fresh sets
(disjoint, 8H) and R_old = N(Q) \ F (old-exclusive): |N(Q)| = Σf + |R_old|
exactly, so Delta(Q) = Σ_j(|Q_j| − 3f_j) − 3|R_old| ≤ overflow(D_Q) − 3|R_old|
=: deficit(Q) (non-heavy terms ≤ 0 dropped). Hence deficit(Q) ≤ 0 ⟹ Hall(Q),
but NOT conversely (buffers: deficit can exceed Delta; deficit>0 is pressure,
not kill). Full-B form toothless (R_old massive → deficit ≤ −6 universally,
12k evals (pooldef.json)). Sharp per-Q form = one-access-Hall+ (open, wall).
Single-access-Q deficit = Delta exactly (no buffers dropped) ⟹ deficit-hunt
there ≡ shortfall-hunt (46k+ clean).
Supply avenues, all mapped with verdicts: fresh ✓ done (8H/non-heavy);
E1/E4-complete (no forcing; §21.A); E2 (hole-y §8G, bounded C41); K
(ratchet/dilute); W (transient/sterile, OCC/STEPS; hub-luck); E7 (+2);
hub (counts-nil §8M); pushes (zone-mismatch); runs (miskeyed deposits);
induction (circular §8L); fluid/counting (forbidden ≡GC); augmenting
(circular §C41); DAG/aggregate (dead §8N); fourth-use (mapped §8N);
deficit (restatement, this section). NO avenue untried; new idea or violator
required — nothing left in the current arsenal closes it.

## 8Q. CONDITIONAL MINDEG-SAFETY + VIOLATOR-ZONE REDUCTION (C51)

Lemma (conditional, rigorous): let Q with mindeg(N(Q)) = d ≤ 3. Suppose every
strictly smaller B-set satisfies Hall. Then Q satisfies Hall (Delta ≤ 0).
Proof: min-degree a* (d ≥ 1 since a* ∈ N(Q) has ≥1 neighbor); R = neighbors
(|R| = d); Q' = Q\R strictly smaller so Delta(Q') ≤ 0 (hypothesis);
N(Q') ⊆ N(Q)\{a*\} so |N(Q')| ≤ |N|−1; Delta(Q') ≥ |Q|−d−3(|N|−1) =
Delta(Q)+3−d; hence Delta(Q) ≤ Delta(Q')−(3−d) ≤ −(3−d) = d−3 ≤ 0. ∎
Status: PROVED_AUTHOR conditional on smaller-Hall (NOT unconditional — the
hypothesis is exactly what's open globally; no circularity in the conditional
form). Violator-zone corollary: Hall(Q) for mindeg(Q) ≥ 4 is the entire
remainder (= violator zone; 8B consistent). Mindeg-4-removal constraint
(bonus): minimal violator with min-degree exactly 4 has every such removal
tight (Delta = 0 exactly, no orphans) — else a smaller violator contradicts
minimality. Consistent, not contradictory (does not close).

## Finite status (C38 + C40-8H, plus C51-8Q/C52 below)

M2 history yields a stalled PEEL 4-core (R=42, N=75, mindeg EXACTLY 4,
Delta=−183, connected, acc span 2–37) with max-flow STILL saturating:
CAP3-PEEL-as-universal REFUTED, GC-STATIC unaffected (recorded distinction).
Killer + ENTRY@3 histories PEEL-empty fully. No Delta>0 anywhere yet.

## 8R. PINNING-IMPOSSIBILITY + SUPPLY-FREE-PUSH COROLLARY (C53)

Lemma (rigorous): every nontrivial splay (A or B, >=1 StepEv) moves its
pre-splay root (final StepEv pivots old root down: zig sends p to child;
double sends g to grandchild). Hence A-root-pinning across a nontrivial
access is impossible; pinning survives only trivial accesses (repeats/no-ops).
Check: 2661/2661 nontrivial splays move old root (120 histories, present).
Corollary: supply-free pushes (e_A=0 + real B-splash = DELETE-then-KEEP
repeats with stale-deep-B) are single-shot per state (splash roots in B);
rebuilding (A-root + B-deep-stale) needs unpinning/redeepening accesses which
are nontrivial (create E1 supply) or no-ops (stall). So supply-free pushes
alternate with supplying accesses (zone-overlap for x still required and open;
sterile-rebuild sustain needs fresh-far keys (finite pool) else repeats stall
or near keys overlap-save). Code: splay_A/splay_B_push zig/double branches;
root_key before/after.

## 8S. SITED-ALWAYS (UNIVERSAL, code-proved) [PROVED_AUTHOR C58]

Statement: every A-StepEv (hence every Aev counted in S_A) is sited.
Proof: `splay_trace` emits ZIG with `(lo,hi)=(min(node,p),max(node,p))` and
doubles with `(min,max)` of `(node,p,g)` (`python/liquidity/legacy_embedding.py`
lines 121–140) — node≠p distinct keys, so `lo<hi` always. `_sites`
(lines 156–161) and `encode._sites_nonempty` return nonempty given `lo<hi`:
`i=lo ∈ [lo,hi)` satisfies `1≤lo` (min key), `lo<nkeys` (`lo<hi≤nkeys`),
`lo+1≤hi` (distinct integers). Failure needs `lo==hi` (single point = no
rotation = not a StepEv). Finite face: 3871/3871 sited (`imprint.json`) — was
theorem all along. Consequence: S_A = #A-StepEvs exactly; no filtering;
T7 banking per StepEv unconditional.
Update C109: closed end-to-end in kernel (`lean/WP6/GCStaticArith.lean`:
`sited_zig`/`sited_double`, exit 0; triple needs only ONE disequality (b≠c),
stronger than geometric distinctness). Status now PROVED_KERNEL modulo
Layer-A triple-emission correspondence (code-cited above).

## 8T. FIRST-ACCESS NON-HEAVY (UNIVERSAL one-liner) [PROVED_AUTHOR C58]

Statement: the first access of any history is never B-heavy.
Proof: pre-states `A=B=T0`; same key, same tree ⟹ same splay cost and trace
length: `e_A=e_B` (0 if trivial/no-op with zero demand, else `e_B=e_A≤3e_A`).
Heavy needs divergence (DELETE-decoupling), which needs past accesses that bank
sited supply (8S) with zero B-demand. So heaviness is always bought with prior
pure supply — decoupling-budget face (cycle-closure queued).

## 8U. K-UNIVERSAL: past-x-Aevs anchor all future x-bursts [PROVED_AUTHOR C58]

Statement: fix key x and KEEP access J on x. Every sited Aev of every past
x-access is K-adjacent (hence E3-adjacent) to every B-event of J.
Proof: (i) `splay_A` rotated sets are `{node,p[,g]}` with `node=x` fixed
(`scripts/wp6_eventflow.py` lines 111–145, never reassigned) — so `x ∈ S(a)`
for ALL Aevs of x-accesses. (ii) All are sited (8S). (iii) ML-K-PERSIST
(`scripts/wp6_microverify.py` MV-02: 15316 checks, viol 0): sited past-x-access
A-StepEv with rotated∋x is in E3 of later x-KEEP B-events. K-def adds only
`ai<acc` (past ✓). Hence `K_x(J) ⊇ {all past x-access Aevs}`, count
`Σ e_A` over past x-accesses, cap-3 each, plus E1 (same-access) + E4-pristine
(setup; FRESH-CHANNEL-b) + E2/W/E7. Finite face: 75 trivial bursts all with
E4 + K≥2 + E3-union med 17 (`imprint.json`); K2A one-access Δ≤−2 universal-side
pressure. Residual (NOT closed): cap-exhaustion (few imprints ×3 vs big e_B —
transients cover finitely, chase 95%) + cross-x contention on multi-key triples
+ E3-variation formalization. Wall purified to anchored-supply contention.

## 8V. PUSHER-COUNTING SKETCH (atom closure direction) [SKETCH C59]

Claim-shape: B-depth d of x at burst needs ~d/2 KEEP pushers post-T0 (each
re-deepens x by ≤2 levels; T0-depth is free but then A=B same-shape so
E1 covers: e_A=e_B). Each pusher access on z banks e_A(z) sited Aevs (8S) ALL
with triple ∋ z (`splay_A` node-fixed, cf. 8U(i)); if z lies on burst B-chain,
ALL of them E3-hit burst B-events with triple ∋ z (E3 = rotated∩triple,
`wp6_e3order.py`). So pushers imprint their own chain positions: ~d/2 pushers
× e_A(z) Aevs × cap-3 vs burst demand d-ish + pushers' own demand (covered by
their own E1 first). Cycler finite face (`cycler.json`, 10k): worst anchored-local
margin −9 (dem 12, new 1) yet global shortfall 0 — transients/imprints cover
exactly the anchored gap. Missing for theorem: (a) per-pusher depth-yield bound
(≤2 levels — splay bystander mechanics); (b) contention bound (pusher supply
shared with pusher demand + cross-x multi-key triples — maxflow assignment,
counts insufficient since online greedy REFUTED starve_min); (c) T0-chain-fresh
keys (never-A-touched — covered by E1 same-shape only at history start; later
need variation). With (a)+(b)+(c), first-x-burst atom closes; induction over
bursts via 8U (K grows ~3/cycle) + 8K frame closes the rest. Status: SKETCH with
finite backbone; NOT proved.

## 8W. BYSTANDER-YIELD BOUND + ANCHORED-INSUFFICIENCY (C60)

Yield (finite, 50k+ bystander events, `yield.json`): per KEEP, bystander depth-gain
distribution {+1: 37597, +2: 13083}, NEVER ≥+3, max +2. Gives pusher-counting teeth:
burst depth d needs ≥d/2 prior KEEP accesses, each banking ≥1 sited Aev (8S).

## 8W.2 YIELD-BOUND ROTATION TABLE (SKETCH, Lean-ready) (C62)

Per-StepEv bystander shifts from `_rot_right/_rot_left` (`legacy_embedding.py`
lines 77–99): single rotation (edge p−x): x −1, p +1, p-outer-subtree +1,
inner-b +0, rest 0. Splay StepEvs: ZIG: p +1 only (ancestors incl. G unchanged).
ZIGZIG (LL/RR, two rotations): node −2, p 0, g 0, triple-parent G +2 (+G-outer),
rest rigid-0. ZIGZAG (LR/RL): node −2, p 0, g +1, G +0. Per-StepEv bystander max:
+2 (zigzig/zagzag triple-parent-outer only), else ≤+1. De-pathing lemma (mechanics):
every push puts the bystander train OFF the z-path (zig: p becomes sibling-side;
zigzig: G lands sibling-side of z; zigzag: g sibling-side) — pushed trains never
rejoin (rotations only shorten the path; side-subtrees stay side). Rides after
de-pathing: rigid with train root (−1 per higher StepEv as path compresses; +1
only if train root is outer child of a final ZIG at root). Net per access ≤ +2 PROVED by lift-accounting (C63): ride-ups (+1 to an
uninvolved outer child) happen ONLY at root-changing FINAL StepEvs (non-final steps
keep the root: outsiders rigid-0; only zigzig moves a non-triple outsider, +2 to
triple-parent-outer). A +2-push leaves its train at depth ≥2 (node depth d≥3 for
zigzig; train lands d−1≥2). Final-zig ride-up hits ONLY the root's outer child
(depth 1). Reaching it needs ≥1 lift (−1 per subsequent StepEv as the path
compresses; rigid-0 zigzig-chains don't lift but then position never reached —
ride-up misses). So net = +2 −L +1 with L≥1 forced, i.e. ≤+2; +1-push cases give
≤1+1=2 similarly; re-pushes barred by de-pathing. Hence every bystander gains ≤+2
per access UNIVERSALLY. Exact verification: ALL BST shapes n=4..7 × all keys
(8304 gain events: +1: 6658, +2: 1646, never +3); two-splay max net +4 = +2/access
consistent; 50k sampled large-n events agree. Status: PROVED_AUTHOR (rotation table
+ de-pathing + lift-accounting; Lean-pending). Consequence: 8V(a) PROVED — burst
B-depth d ⟹ ≥d/2 prior KEEP accesses, each banking ≥1 sited Aev (8S).
Update C107: per-StepEv single-rotation rows PROVED_KERNEL
(`lean/WP6/SplayRotate.lean`, exit 0, no sorry: STree+sdepth+rotR/rotL,
sdepth_self + 10 region rows (up/down/ride/middle/outer, both sides));
de-pathing + lift-accounting + splay-loop still need the loop model.

## 8Y. ATOM-CLOSURE: key-identity E3-backstop + ride-sterility (SKETCH, C64)

Defs (`scripts/wp6_eventflow2.py` lines 79–107): E2 = pump-KEEPs u ∈ (prevkeep,idx)
with xx ∈ pump_push(u) (windowed, E2-hole via DELETE-half unrecorded); E3 = sited
past/same Aevs with ROTATED ∩ B-triple ≠ ∅ (ageless; B-triple = pushed ∪ {xx});
E7 = pump-chain closure (depth-8); E4 = setup; E1 = same-access.
Chain-identity (mechanical): past sited A-access on chain key z has rotated ∋ z
(node-fixed, 8U(i)) and is sited (8S); burst triples tile the B-path; z E3-hits
burst events with triple ∋ z — unavoidable key-identity hit. Every post-T0 pusher
(chain ancestor by pushing mechanics) imprints its chain position; E2-hole's
DELETE-half STILL E3-hits (E3 backstops E2). Diverger-hit: accesses that moved x
hit the first burst triple (∋ xx always). Misses need ALL of: chain-fresh +
neighbor-spill-absent + E1-empty + E4-empty + E2-miss + E7-miss + K-empty.
Ride-sterility (deepest hole): G-outer trains deepen +2 SILENTLY (no triple ∋ x,
unpushed ⟹ E2/E7 miss); full atom = ride-depth × A-shallow-without-DELETE-x ×
region-fresh × trivial-setup. Never assembled (varhole 0/5405; triple 3k; K2A −2).
Contention (`reuse.json`, 150 hist): max-reuse 6..137, over-subscribed 6909/8599
(80%), EVERY history — trivial matching hopeless, maxflow routes via density.
Cover at E1-empty bursts (35): K 10.9 + W 6.1 + E2 4.1 + E4 1.5 + E7 1.5 avg.
Status: SKETCH with def-pointers; residuals = silent-ride conjunction (finite:
never) + contention assignment (finite: always saturates).

## 8Z. SHAPE-DICHOTOMY: deep-self-covering vs shallow-fresh-covered (SKETCH, C65)

Steering verdict (`steer.json` vine 40 seeds: maxsplit 115, burst Δ −188..−716,
N ≈ 3.5–4× e_B, kills 0; `steer3.json` bal/rbst 60 seeds: splits −8..+12,
e_B ≤ 12, kills 0): the two dangers are mutually exclusive by tree geometry.
Vine case: chains are key-intervals of length ~e_B spanning half the key-space;
any activity imprints its path-interval across them (the ±2-avoidance was useless
— chain length 60 vs exclusion 5); cover scales with demand (N ≈ 4·e_B measured)
because demand-size ≈ chain-length ≈ hit-surface. Balanced case: chains O(log n),
depth/split bounded (steering caps at 12 even adversarial), fresh/E1 covers small
demand. Formal shape: vine-chain = interval (interval-covering/pigeonhole over
imprint-intervals); balanced-chain = narrow (demand small). Missing: interval-cover
counting (union of t path-intervals vs chain-interval in [1..n]) + balanced drift
bound (rides cancel). On close with 8V/8W/8Y: proportional-variation PROVED.
Anchored-insufficiency (measured): maxflow on ANCHORED edges only (E1+E4+K, no
E2/W/E7) fails 19/140 histories (13.6%), worst shortfall 49 of 76 demand — transients
are LOAD-BEARING, not bonus. Anchored-only cycle-closure DEAD (banked honestly).
Wall final form: universal anchored base (8S/8T/8U) + load-bearing transient variation
(E3-union first-overlaps); missing universal = variation (every E1-empty heavy access
brings new-old — emptiness hunt queued; fullsplit-bleed + pressure-17 are the finite
faces on both sides).

## 8AA. ROOT-ANCHOR + FRESH-FULL REFINEMENT (finite-strong, C66)

Census (`anchor.json`, 464 bursts e_B≥4 + 60-history split-verify): bursts with ZERO
past-final-triple hits are (i) acc=0 first-access (vacuous — no past; N=E1-full by
8T same-shape) or (ii) post-first with N=E1 exactly (fully fresh-covered non-heavy;
5 cases, all n=16, e_B 4–8, N=e_B). No post-first burst with old-dependence lacks
root-hits in corpus. Refined dichotomy: (fresh-full ⟹ safe by 8H counting) or
(old-dependent ⟹ root/variation hits observed). Status: FINITE_STRONG.

## 8AB. HEAVY ⟹ ROOT-HIT (joint 2×2, finite-universal) (C67)

Joint census (345 bursts e_B≥4, 80 histories): (non-heavy,zero-hit) 43 /
(non-heavy,hit) 252 / (heavy,hit) 50 / (heavy,zero-hit) 0. Zero-hit ⟺
fresh-full-non-heavy (43 acc0-or-N=E1); heavy ⟹ past-final-triple hit ≥1 (50/50;
varhole heavy-E1empty new≥4 consistent — stronger). With 8T (acc0 never heavy:
trivial-root has no demand) the (heavy,zero-hit) cell is empty on both sides.
Mechanical sketch: heavy ⟹ divergence (8T-contrapositive) ⟹ past final triples
in root-area; burst chain crosses root-area (path ends at root; final B-triples
root-area); old-root-pivot (8R: final StepEv pivots old root down — final triples
contain pre-splay roots of both trees) forces overlap modulo root-migration
(roots migrate per access — the residual). Candidate universal: every heavy burst
carries ≥1 root-anchored new source + growing K (8U) + chain-hits ∝ length (8Z).

## 8X. VARIATION-EMPTINESS (finite-strong; universal candidate) (C61)

Measures (`varhole.json` + inline pinned census): 4107 accesses / 159 heavy /
4 heavy+E1empty → ATOMS (heavy + E1empty + new-old 0) = 0; newdist {4:2, 8:1, 9:1}
(new-old NEVER <4 when E1-empty+heavy). Victim-pinned micro-cycles (1298 accesses):
heavy = 0 outright (setup-DEPTH self-funds: E4-pristine with deep setup covers;
shallow-setup needs A-far pushers = triple conjunction). Shape-aware triple assembler
(`triple.json`: B-near/A-far + DELETE-then-KEEP E2-hole + root-burst, 120 shaped seeds
+ hillclimb, 3k evals): NO KILL. Candidate universal: heavy + E1empty ⟹ new-old ≥ 1
(observed ≥4); with proportional form (overflow/3 ≤ new) it closes 8K-step; unproved.
Resonance noted: new ≥ 4 matches 8B mindeg ≥ 4 (both sides of violator demand 4+).

## 8AC. PER-BLOCK PROPORTIONAL COVER WITH REUSE BUDGET (OBLIGATION, C97)

Statement (to prove): for every B-heavy access-block Q_j (overflow o_j =
|Q_j| - 3f_j > 0, f_j fresh slots), with new_j = first-overlap sources at j
(E1(J) union E4-setup-portion union first E2/W/E7-hits; pairwise DISJOINT across
accesses since first-adjacency is once-ever) and old-stock R = N(Q)\F:
  o_j <= 3*|new_j| + 3*c_j   with   SUM_j c_j <= |R_old-shared| (contention-bounded).
Then 8I closes globally: Delta(Q) <= SUM o_j - 3|R| <= 3*SUM|new_j| + 3*SUM c_j
- 3|R| <= 0 since UNION(new_j) conserved plus contention within cap (c_j exact
reuse allocation from an explicit assignment). The assignment is the content:
BLOCK-GREEDY (E1-fresh first (disjoint, exact); K-anchored second (nested per x
by 8U: later bursts see supersets); transients E2/W/E7 by least-loaded top-up).
Sufficiency test (greedy.json): chronological block-greedy vs maxflow-optimal
over corpus. If greedy == maxflow everywhere finitely, the constructive path is
open (formalize non-failure: fresh-exactness + K-nesting + transient density from
8Z/8AB). If greedy fails where maxflow succeeds, contention needs true matching
(theory beyond greedy; wall stands). Status: OBLIGATION + executable test.
Chain on close: Hall(Q) all Q -> GC-STATIC -> E_B <= 3 S_A (GC counting) ->
D <= 6 S_A (D2 banked) -> service generation -> MSTL-14P (conditional C0-C4).

## 8AC-GREEDY. T-BEFORE-K SUFFICIENCY + EXCHANGE REDUCTION (finite-strong, C97)

Measures (greedy.json 150 hist: FWD|E1E4KT 149/150 (one gap t75); greedy2.json
501 hist x 72 combos: ALL 29 T-before-K combos (FWD+MINN) PERFECT (0 gaps each);
ALL K-before-T combos gap; REV|E1E4KT gaps 30/worst-7). Gap t75 is pure order
artifact (12 orders incl. all-REV and T-first-FWD saturate it). Rule: FWD or MINN
event order with tiers T before K (E1/E4 first, K LAST): K preserved as backstop
for K-only needy (late repeat bursts, E1/E4/T-empty, K-nonempty by 8U); fresh
owner-first (E1 used same-access before later theft as old); transients shared
middle. Symmetric hoarding explains failures (K-early starves late-K-only;
REV lets late events steal early-E1 as old). Exchange-reduction sketch: E1
(disjoint, 8H) + K (nested per x, 8U) assigned structurally exact; T-residual
(overflows only) by density (8Z/8AB) � residual Hall = variation (hole, smaller:
only post-E1K overflow needs transient cover). Status: FINITE_STRONG (29x0/501)
+ reduction sketch; NOT closed (T-residual variation = same wall, narrowed).

## 8AC-X. EXCHANGE/CHARGING SKELETON FOR FWD+T-FIRST GREEDY (C100)

Suppose FWD|E1,E4,T,K-least-loaded sticks at B-event j (all N(j) full from
earlier-or-equal placements). KEY 1 (causality): E1(j) (ai=J) is invisible to all
strictly-earlier accesses (need ai <= acc < J); its load comes ONLY from same-block
earlier-j' events. So either E1(j) = EMPTY (repeat/trivial burst) or the block is
locally heavy (same-block saturation, >= 3|E1(j)| same-block users); either way j
sits in a heavy-ish block with fresh locally exhausted, N(j)-rest = E4+K+T past.
KEY 2 (lexicographic regress): W = earlier
users filling N(j) has |W| >= 3|N(j)| (cap-3 counting, one unit per event). Each
w in W with E1(w) nonempty preferred own fresh (tier 1) yet landed in N(j):
hence E1(w) was FULL at w's turn, filled by strictly-earlier (acc,j') pairs
(FWD order; later pairs unrunnable) — or E1(w) empty (repeat, grounded). KEY 3
(disjoint fresh, 8H): non-repeat fillers contribute pairwise-disjoint E1-sets
into N(Q') for Q' = W union {j}. Grounding: regress strictly decreases (acc,j)
lexicographically (same-block: smaller j first), terminating at repeats
(E1-empty, placed into K/T/E4-old) and first-users (E1 free by causality).
COUNT (skeleton): with W_rep grounded repeats and W_fresh bringing disjoint
|E1| >= 1 each, Delta(Q') <= 1 - 3|W_fresh| + [K/T-tier corrections] — the
displayed bound needs the tier-interplay ledger (w may land in N(j) via T-tier
with K(w) untouched; K(j)-full needs nested-consumption counting via 8U;
E4-setup disjointness across runs). RESIDUAL (open): exact tier-ledger
accounting + termination counting to force Delta(Q') >= 1 (deficiency) or
restructure to a strictly-smaller deficient set, contradicting finiteness
without assuming Hall. Status: SKETCH with well-founded regress + causal
fresh-freedom identified; tier-ledger + final count open. If closed: FWD-greedy
never sticks = GC-STATIC constructively (explicit rule), then GC/GC-chain.

## 8AC-D. PER-BLOCK PROPORTIONALITY DEAD + DEGREE-1 ENVELOPE (C102)

Density (`density.json`, 103 heavy blocks): solo-sufficiency E1 66 / K 61 /
W 58 / E2 50 / E7 15 / E4 3 — NO single channel always covers o/3 (worst margins
all negative); union N worst margin +5.67 (heavy blocks deeply safe globally).
Per-block proportionality (o/3 <= new) REFUTED finitely (new < o/3 occurs;
global saturates via old-reuse, budget margin 26x) — counting-form closures DEAD,
honestly. B-degree census (120 hist): min-degree 1 (8 hist!), <4 in 69/120 —
low-degree events are COMMON yet always served (greedy handles via T-diversity
spreading of mates + K-only backstop). Degree-1 envelope: all-degree-1-same-N
slices need |Q| <= 3 (one-access 8F universal, open); K2A-finite says mates always
diversify (steer N ~= 4*e_B). Wall final-final form: ROUTING RULE ONLY
(8AC-greedy-sufficiency: FWD+T-before-K never sticks; 0 gaps on 501+303+8000+
adversarial incl. kill-witnesses) with exchange skeleton 8AC-X (tier-ledger +
T-diversity enclosure-leak open).

## 8AC-H. CHAIN-HITS PROPORTIONALITY (C104: (i) PROVED, (ii) open)

Census (1070 bursts, 88 big e_B>=10): imprint-hits/e_B min 1.00 med 1.56;
hits/chainlen min 0.48 med 0.78; worst big (chain60, eB30, hits30).
(i) PROVED_AUTHOR: chain length L >= e_B (each StepEv climbs <= 2 levels, so
e_B >= d/2 with d+1 = L; hence L >= e_B). Per-burst demand e_B <= 3H needs only
H/e_B >= 1/3 (cap-3 over hitting Aevs, each hitting >= 1 burst event).
(ii) OPEN: hit-rate H >= L/3 (chain-fresh exists finitely (min-hit 0.000):
fresh chains occur, always non-heavy so far (E1 covers via shared rides);
universal hit-rate false without the heavy/fresh dichotomy). Composition with
E1/K/E4/E2/E7 = full N = one-access 8F (same wall). So 8AC-H sharpens but does
not reduce: the atom stays 8F-vs-sharing (routing).

## 8AC-MW. MOVER-VISIBILITY + RELATIONSHIP-IMMUNITY; W SOLE-POSITIONAL (C105)

Mover-visibility (mechanical): non-silent depth-movers imprint on-chain — path
movers (involved: rotated ∋ path keys incl. block-roots/train-roots on-chain),
pump movers (pump_push ∋ xx gives E2; rotated ∋ pusher gives E3-backstop).
Silent = G-outer rides only (+2, 8W; train-root off-chain). Channel immunity
audit (migration-adversary `mig.json`: co-location driven to 0.0078 with split
53 (e_B 59), 5k evals, NO KILL): E1 (same-access, current) + E4 (setup adoption,
key-identity) + K (8U, xx-in-S key-identity) + E2 (pump-window relationship) +
E7 (pump-chain relationship) are MIGRATION-IMMUNE (historical/key-identity, no
position); ONLY W (rotated-cap-triple, current positions) is migration-sensitive.
Hence migration kills W alone, while E2/E7/K/E1 carry (measured: coloc 0.8% yet
saturate). 8W-ride-debt counting: ride-depth <= 2 rides, each ride banks >= 1
sited Aev (nontrivial motion): ride-debt <= (2/3) banked slots globally (counts
close; assignment needs on-chain (8Z: chain-crossing carries (steer N ~= 4 e_B;
pack3 deep-confinement infeasible: paths cross recent-region))).
Wall final form: migration-proof historical backbone (E1/E4/K/E2/E7) + positional
W-variation (8Z shape-dichotomy) + routing rule (8AC-G). Missing universals:
W-density proportional (8Z counting) + drift bound (balanced) + exchange
tier-ledger. Status: MECHANISM-MAPPED (finite: mig/pack/steer/varhole).

## 8AC-MG. MIGRATION-POSITIONAL-MATCHING WALL SYNTHESIS (C106)

Four independent reductions converge here: (1) chain-identity backstop needs
CURRENT co-location (imprint-key positioned on burst chain at burst time);
(2) keys are static, positions migrate via rotations (8R); (3) E3/W hits need
key-identity co-location, while E1/E4/K/E2/E7 are relationship/key-identity
(migration-immune, 8AC-MW); (4) universal density false in principle
(adversarial packing conceivable) yet never assembled (pack/pack3/mig/triple/
steer/varhole all clean-or-infeasible). Finite-strong: recent-co-location
suffices always (roots migrate among recent pool (same-H recency shared by
both trees)); greedy rule migration-proof (greedymig 5k: ruledead 0; combined
rule record 0 failures on crowned order over 501+303+8000+5000). What universal
would need: positional tracking (temporal bipartite matching: supply/demand
co-location dynamics) — beyond current arsenal (needs Lean positional splay
model + online-matching-with-structure theory). Status: WALL CRISPLY STATED;
finite-strong everything; universal open.

## 8AC-BERGE. NO-ELEMENTARY-BYPASS META-LEMMA (C116)

Theorem-shape (Berge, standard matching theory applied to our cap-3 setting):
FWD-greedy processes chronologically, placing whenever ANY neighbor has free
cap (maximal partial matching). If it sticks at j, either an augmenting path
exists from j (resolvable — t75-style: other orders/augmentation fix it) or NO
augmenting path exists, in which case the matching is maximum (Berge) and
maxflow equally fails (same cardinality) — i.e., a Hall violator exists.
Contrapositive: maxflow-ok implies greedy either saturates or sticks
augmentably. Consequences: (1) pure-greedy-sufficiency can never be proved
without density/matching universals (any sticking point is either fixable or
witnesses a violator — the argument cannot bootstrap past maxflow); (2) the
8AC-greedy rule stays FINITE_STRONG (0 failures, 13k+) but not promoted;
(3) remaining doors are exactly: Lean positional model (multi-session) for
density universals, or a verified counterexample. This lemma HONESTLY closes
the elementary-proof search: no counting/greedy/peel/induction argument can
bypass Hall here (all reduce to it or assume it — cf. 8L circularity,
8AC-X tier-ledger, enclosure leaks). Status: META (proof by standard theory
instantiation; finite faces: t75 stuck-augmentable + budget-26x + reuse).

## 8AC-Z. VIOLATOR-ZONE LEMMA + INDUCTION ASSEMBLY (Mode-A, C118)

Statement (8AC-ZONE, OPEN): every $B$-set $Q$ with $\min\deg(N(Q)) \ge 4$
satisfies $\Delta(Q) \le 0$.
Assembly (verified): strong induction on $|Q|$ (base $\Delta(\emptyset)=0$;
IH = smaller-Hall). Case $\min\deg \le 3$: 8Q gives $\Delta(Q) \le 0$ (its
smaller-Hall hypothesis matches IH; $Q'=Q\setminus R$ strictly smaller since
$|R|=d\ge 1$; no orphans issue handled by $N(Q')\subseteq N(Q)\setminus\{a^*\}$).
Case $\min\deg \ge 4$: 8AC-ZONE directly. Hence 8AC-ZONE $\Rightarrow$ GC-STATIC,
with no circularity (8AC-ZONE never assumes smaller-Hall; it is standalone on
the violator zone). Strictly smaller than GC-STATIC (mindeg$\le$3 zone closed
by 8Q). Falsifiable with continuous objective: maximize $\Delta(Q)$ over
$\min\deg\ge 4$ (K2B: max $-8$ at 12k vine-only); $\Delta\ge 1$ = Hall kill
(global refutation path); $\Delta\ge -7$ = wall-thinning vs K2B (escalation).
Note: deficient $Q$ (any) shrinks to minimal violator (8A/B: $\Delta=1$,
$\min\deg\ge 4$), so 8AC-ZONE $\iff$ no violator $\iff$ GC-STATIC given 8Q+IH —
the equivalence is honest, not a shortcut (the work is entirely inside 8AC-ZONE).

## 8AC-FF. FIRST-FAILURE-FRESH-SUFFIX (C121; campaign §5)

Full proof: `audits/WP6_8AC_PROOF.md` §C121. Statement: under ¬8AC
(matching-form), chronologically-first unsaturable B-event b* at access L with
f = |E1(L)|, r = earlier same-access B-events, satisfies r >= 3f. Hence Case A
(f > 0): r >= 3, L B-heavy (e_B >= 3f+1); Case B (f = 0): vacuous, descent
required. Proof: E1(L) adjacent only to L-Bevs (per-Bev access scoping +
causality ai<=acc); prefix matching loads E1(L) by <= r; r < 3f leaves free
E1 cap, extending the matching through b* contradicts first-failure.
Dependencies: E1 construction/completeness (abl 64-66), cap 3 iff sited,
B-demand 1, 8S, chronological order, first-failure well-ordering.
Status: PROVED_AUTHOR. Lean: ffs_free, eb_suffix (kernel).

## 8AC-RM. ROUTE EQUIVALENCE MAP (C122; decision instrument, PROVED_AUTHOR)

For each candidate route R to GC-STATIC, exact logical relation (proved here or
banked; finite witnesses cited, never used as proof):
1. 8AC-ZONE (mindeg>=4 zone Hall) <=> GC-STATIC (given 8Q + strong induction).
   =>: C118 assembly (8Q closes mindeg<=3 by IH; zone closes rest; no circularity
   (zone standalone)). <=: violator shrinks to minimal (8A/B: Delta=1, mindeg>=4),
   which lies in the zone. EQUIVALENT (same hardness; zone is the honest target).
2. Greedy-universal (FWD+T<K never sticks) => GC-STATIC (constructive: exhibit
   the greedy assignment). CONVERSE FALSE: t75 (greedy shortfall 1, maxflow 0).
   So greedy-rule is STRICTLY STRONGER (overkill): do NOT pursue it as the route
   (harder than needed); pursue Hall-direct. Finite-strong stays valid evidence.
3. Per-block proportionality (o/3 <= new) REFUTED as universal (density.json:
   new < o/3 occurs; global saved by reuse). Dead as theorem; finite face kept.
4. Carry-sufficiency <=> Hall(Q) (8L, banked dead): assuming carry assumes goal.
5. Fluid/counting-only = GC-counting, insufficient for Hall (assignment missing).
6. Augmenting-repair circular (C41): repair needs spare that needs Hall.
7. CAP3-PEEL-as-universal REFUTED (M2: 4-core Delta=-183 saturates; peel stalls
   but maxflow succeeds). Peel-emptiness sufficient, not necessary.
8. DAG/aggregate closures DEAD (8N: E1-maximals kill DAG; sharing-infinity kills
   aggregate). Fourth-use mapped not closing. Hub-universal REFUTED (8M: 5/6
   past-lasts miss killer top). Deficit-form RESTATEMENT (8O: Delta <= deficit;
   deficit>0 is pressure, not kill). X-RETURN-universal, sterilization-strong,
   E1+E4-only, per-key-GC/flow: all DEAD (DAG banked).
9. One-access Hall (8F) does NOT imply global Hall (cross-access sharing/
   contention uncaptured). Necessary fragment only (K2A finite: Delta<=-2).
10. Anchored-only (E1+E4+K) INSUFFICIENT (yield.json: fails 19/140, worst 49/76;
    transients load-bearing 13.6%). E1+K-alone INSUFFICIENT (residual 18%, C98).
11. Online-chronological rules (Stage B family, incl. least-loaded): REFUTED as
    universals (starve_min); chronological FWD-greedy unrefuted finitely but
    covered by (2) (overkill direction only).
Conclusion: the ONLY non-dead, non-overkill, non-circular route is Hall-direct
via matching/contention theory with positional density (multi-session), or a
verified counterexample. All other doors are proved shut or proved harder.

## 8AC-R. COUNTING MARGIN 26x: WALL IS ROUTING ONLY (C98)

Measures (
esidual.json 200 hist: E1K-alone saturates 164 (82%), tail resid 1..60;
udget.json 200 hist: reuse-budget over 0/200, worst SUMc/R = 0.038 (3.33/88)):
capacity margin ~26x � shortage arguments are DEAD; the entire remainder is the
routing rule (explicit cap-3 assignment that never sticks). 8AC-greedy-sufficiency
(FWD + T-before-K never sticks) is the sharp obligation: finite-strong (29 perfect
combos/501 + t75-artifact), mechanism identified (K-last backstop, owner-first),
universal proof open (online-chronological rule; starve_min warns online rules can
fail � tiered rule unfalsified). Next: greedy-killer hunt (all-FWD-tiers fail +
maxflow ok) to kill-or-crown the rule; exchange formalization; Lean track.

## 8AC-TO. ELIGIBILITY TIME-ARROW: NO EDGE POINTS FORWARD IN TIME (C125, PROVED_AUTHOR-by-construction)

build_tagged (scripts/wp6_eventflow_abl.py): every channel draws sites only from accesses <= bev acc:
E1 = accA[idx] (same); E4 = accA[setup[xx]] with setup[xx]<=idx, !=idx (older); E2: u in (prevkeep,idx) (older);
E7: v<u<=idx (older); E3: ai<=idx explicit. Forward edges (site-acc > bev-acc) DO NOT EXIST structurally.
Finite confirmation: 51,292 greedy placements across walk+pusher families, 100 percent loader-newer-or-same,
zero forward uses (wcharge.json trel + wcharge_pusher.json trel). CORRECTION to C124 banked text: the arrow is
BACKWARD-grazing (bevs use older-or-same sites), NOT forward-escape; quartile gradient re-read: early bevs meet
few older sites (own-E1 40pct), late bevs graze the deep past (W 73pct on older sites).

## 8AC-PRISTINE. OWN-E1 PRISTINE AT BIRTH (C125, PROVED_AUTHOR-by-construction)

Corollary of 8AC-TO: at access t, sites_t have ZERO load from past bevs (past bevs cannot touch future sites:
edges do not exist). Own-E1 pool opens each access with full 3|sites_t| slots; only siblings compete for it.
Siblings-overflow spills to backward channels (E2/E4/K/W/E7 into older sites with residual capacity).

## 8AC-IND. FWD INDUCTION FRAME: PRISTINE-E1 + RESIDUAL-SUFFICIENCY (C125, SKETCH with one HOLE)

Induction over accesses t=0..L-1. At step t: siblings place E1-first into pristine 3|sites_t| (fits iff
siblings_t <= 3|sites_t|; overflow spills backward). Claim: older sites always hold enough residual for spill
+ their own future demand is already... HOLE-IND (residual-sufficiency universal): needs per-site demand bound
(total future W/K claims on site i <= 3 - E1-load_i) from rotation-occupancy budgets (ML OCC lemmas) or
positional density (multi-session theory). FWD greedy totality (340/340 T-first-FWD incl. C123 TB + C124/C125)
is its finite face. This replaces all forward-escape framings (C121-C124): the past is the reservoir, E1 is
the birthright, residual-sufficiency is the single remaining obligation (same wall, correct orientation).

## 8AC-HD. HOLEDEMAND: COUNTING RESIDUAL-SUFFICIENCY DEAD (C126, PROVED_AUTHOR)

Measure (holedemand.json, 80 hists walks+pushers): per sited site i, claim(i) =
#future bevs eligible via K/W/E2/E7/E4: 82.4% sites claim>3 (17127/20793),
median-claim med 15 / max 88, sitemax 406 (K-claims 108). Future demand exceeds
cap-3 almost everywhere, yet maxflow saturates in all 80 (and ~200M cumulative):
the assignment (matching), not per-site counting, carries GC-STATIC. Hence
HOLE-IND in counting form is DEAD (consistent with 8N(d) sharing-infinity and
8AC-D proportionality-dead). Residual-sufficiency survives only as matching/
contention theory (positional density, multi-session) = 8AC-RM door #1; else a
verified counterexample (door #2). No other doors remain.

## 8AC-IL. INTERVAL-LOCALIZED HALL DEAD AT SCALE (C142, FINITE_REFUTATION)

Candidate: contention localizes to key neighborhoods (t75 loaders: x39
siblings + x38 adjacent cohort), so Hall closes per key-interval with
bounded overlap. Finite verdict: loader key-distance |loader_x -
site_acc_x| at scale (n<=512, 42k placements): W med 23 / p90 129 / max
493; K med 0 / p90 23 / max 297 (codist.json). W grazes the whole key
space; t75 adjacency was small-n luck. Interval/counting localization
is DEAD (consistent with 8N(d) sharing-infinity and 8Z long chains).
E1 distance always 0 (structural same-access). Contention is key-global;
only matching/contention theory (8AC-RM door 1) or counterexample (door 2).

## 8AC-STUCK-SIB. STUCK IMPLIES E1-COHORT SATURATION (C143, PROVED_AUTHOR)

Definitions: greedy places bev j iff some eligible plotted neighbor has free
cap (maximal per-tier search); E1(j) = plotted accA[acc(j)] only (same-access,
build_tagged causal scoping); cap 3 per source.
Lemma: if E1(j) nonempty and greedy sticks at j, then every source of E1(j)
is full, and all loads on E1(j) come from same-access siblings (no forward
edges exist, 8AC-TO: past bevs cannot touch E1(j); future bevs have no edges
into it either). Hence stuck(j) with E1(j) nonempty ⟹ 3|E1(j)| sibling-loads
(same-access cohort saturation of the birthright pool, 8AC-PRISTINE inverted).
E1(j) empty (repeat/trivial bursts) ⟹ stuck is pure backward-spill exhaustion.
Finite faces: 76/76 REV-stuck E1-full-by-siblings (augment2.json: 982/982
slots, 2808 sib-loads, 0 past); t75 (sole FWD-stuck): E1=1 full by siblings
13,14,15 + K site12 by siblings 16,17,18 + shared site13 by x38 past cohort.
Repair corollary (Berge, C123): every stuck matching is augmentable; measured
repairs all length 5 via W/K (augment2.json 76/76 + t75).
FWD-TOTALITY TALLY (T-first-FWD, chronological): TB 40 + WC 150+150 +
C125 reruns 150+150 + CD 300 = 940 evals, ZERO stuck, zero kills.
E1-first/K-first FWD near-total with rare stuck (all cohort-saturated +
augmentable). Consequence for 8AC-X: the tier ledger at stuck points is
ALWAYS cohort-saturation (siblings + same/adjacent-x past cohorts); exotic
K-hoarding/T-theft by unrelated bevs never occurs finitely. The exchange
argument localizes to cohorts; global repair flows through W-augmentation.

## LEAN-BOUNDARY. KERNEL PAIR COMPLETE; ASSEMBLY NEEDS CARDINALITY (C146, META)

Kernel-closed in core Lean (no sorry/axioms, all exit 0): matching cores
(8Q/zone-step, GCStaticHall), migration locality (GCStaticPos), side dynamics
(GCStaticSplay), splay skeleton + key safety + delivery (GCStaticLoop,
GCStaticValid, GCStaticDeliver), engine simulation rotations/doubles/branch
(GCStaticSim, GCStaticStep2), traces + supply (GCStaticTrace, GCStaticSupply,
GCStaticLift, GCStaticSupplyTotal), greedy maximality (GCStaticMatch),
path-flip improvement (GCStaticCount). NOT closed (needs Mathlib finite-set
cardinality or open mathematics): augmenting-path EXISTENCE for non-maximum
matchings, flip load bookkeeping in full generality, Hall assembly
(maximal + unaugmentable => violator-or-saturated), 8AC-ZONE itself. The
wall stands exactly on 8AC-RM doors; formalization has done all it can in
core Lean.

## 8V-VERDICT. PUSHER-COUNTING ATOM: STRONG FORM DEAD, WEAK SURVIVES (C147)

Measure (rides.json, 535 heavy bursts, full-history window): 76.8 percent
of burst-built B-depth comes from SILENT pushes (no E3-imprint from the
pushing access to the burst); fully-silent bursts to eB=91. 8V-strong
(imprint-proportional burst cover) is REFUTED as the primary mechanism
(imprints cover ~23 percent). 8V-weak survives: pushers bank sited Aevs
(8S) into the global pool (K-persistence 8U, E2, W), routed elsewhere.
K_x med-cover 1.51x demand but min 0.0 (first/fresh bursts need E1/E4/
transients): cover is PORTFOLIO, no single channel dominant (consistent
with 8AC-D union-only safety and residual/budget margins). Ride-sterility
(G-outer bystander +2s without chain imprint) is the NORM. Consequence:
no atom shortcut; burst cover = general contention = the wall itself.

## 8AC-XC. COHORT-LOCALIZED EXCHANGE v2 (C148, SKETCH + FINITE FACES)

Refines 8AC-X (C100) with the stuck-anatomy campaign (C141-C143, augment2):
(1) PER-CHANNEL LOCALITY TABLE (finite-grounded): E1 same-access only
(structural, 8AC-TO; loaders = siblings + future-grazers via THEIR backward
channels; FWD sees siblings only); K nested per-x (8U) + same-x dominant
(codist med 0; loaders sib + recent-past-x); T global (W med 23; loaders
past-grazers + relational E2/E7 users); E4 rare key-identity. No single
global argument; five channel-local ledgers.
(2) PROCESSING-PRECEDENCE (definitional): stuck-loaders are always a subset
of processed-before-me (loads come only from placed bevs). Past-vs-future
labels are order-relative: REV-stuck sees siblings + time-future grazers
(depth med 20, max 69); FWD-stuck sees siblings + time-past cohort (t75:
depth 1). The regress (8AC-X KEY 2/3) terminates by lexicographic
well-foundedness regardless of depth (already banked); depth data only
calibrates it.
(3) AU-LEN5 SINGLE-DISPLACEMENT LAW (finite-strong, 526/526 REV + t75):
every stuck repair displaces EXACTLY ONE mate (length-5 uniform; no direct
free edge (maximality), no double displacement needed). The obstruction at
any stuck point is one displacement deep.
(4) PRECISE HOLE (unchanged in kind, narrowed in shape): assuming FWD+T-first
sticks at j, with E1 full-by-siblings (8AC-STUCK-SIB proved), K full by
x-cohort, T full by past-grazers: the W-set (|W| >= 3|N(j)| counting) regress
needs the TIER-LEDGER (which tier each w used + K-nesting consumption via 8U
+ E4-run-disjointness) to force a deficient subset or contradiction. The
W-global residual (54 percent of placements) is the load-bearing remainder.
(5) CONDITIONAL ASSEMBLY (pointer): tier-ledger closes => FWD never sticks
=> GC-STATIC (constructive) => E_B <= 3 S_A => D <= 6 S_A => service =>
MSTL-14P (conditional chain, WP6_CONDITIONAL_CHAIN.md). Status: SKETCH with
all finite faces green; tier-ledger + W-residual open (the wall).

## 8AC-WOLD. EVERY W-EDGE POINTS STRICTLY BACKWARD (C149, PROVED_AUTHOR)

Statement: every W-edge (bev j at acc, site i) satisfies acc_of(i) < acc.
Proof: W = E3 minus K minus E1set (chan_of tiers). E3 requires ai <= acc
(build_tagged E3: ai <= idx explicit). Same-access E3 (ai = acc) is sited
accA[acc] hence in E1set (E1 = accA[acc]-sited, build_tagged), so excluded
from W. Hence ai < acc for all W. Dependencies: build_tagged E1/E3
construction + accA scoping (code-cited, Layer A). Finite face: 51,292/51,292
placements loader-newer-or-same with W 100 percent loader-newer (wcharge
trel); strengthens C124/C125 arrow for W from finite law to theorem.

## 8AC-WWIT. W IS CHAIN-MEDIATED GRAZING (C149, PROVED_AUTHOR)

Statement: every W-edge (bev-x j, site i) has a witness w != xx with
w in Arot(i) intersect triple(j) (a non-xx chain key mediates).
Proof: by 8AC-WOLD, ai < acc. K-def is (xx in Arot(i) and acc_of(i) < acc);
W excludes K, so with older established, xx not in Arot(i). E3-def gives
nonempty Arot(i) intersect triple(j); any member w differs from xx.
Hence the witness. Pure logic + defs, no splay content.
Consequences: (i) explains codist split (C142): K loader-distance med 0
(xx-anchored, fixed key) vs W med 23/max 493 (chain keys migrate globally);
(ii) W-neighbors of x-bursts = sites imprinted with x's CHAIN keys
(positional!); (iii) t75 site-13 anatomy: K via path-touch (Arot[13] =
{38,39} ∋ xx=39, acc 2 < 3) — 8U across adjacent keys live; (iv) live
W-edges verified with far witnesses (bev xx379 via witness 31).
The W-residual is now precisely chain-key recurrence (multi-session
positional density), connectable to Lean co-location dynamics (C128/C129
side-break = co-location change) + migration (8R/8M). Status: PROVED_AUTHOR
(chain definitions); recurrence bound open (the wall, narrowed).

## 8AC-REC. RECENT-POOL RECURRENCE LAW + FRESH FALLBACK (C150, FINITE-STRONG)

Measure (recur.json, 120 histories, 59k triple-keys): 81.9 percent of
B-triple keys previously imprinted (sited A-rotated); recency med 1 (!!),
p90 16, max 86 — imprints live in the recent pool (C106 recent-co-location
quantified). Burst triple-coverage med 1.0; all zero-coverage cases are J=0
(first access, vacuous). Heavy-burst min over J>0: 0.005 (eB=67, s=1 J=20:
fresh chain) — universality FALSE, but that burst is E1-trivial (67 bevs,
67 fresh E1 sites, K/T ~0): recurrence gaps coincide with E1 abundance
(portfolio balance; silent-push debt repaid by burst E1).
Sketch status: recurrence (recent-pool, 82 percent/med-1) + fresh/anchored
fallback (E1/K) + relational (E2/E7) + setup (E4) = full supply-side map;
each channel characterized (locality, arrow, mechanism). Composition
(counting with reuse across channels) remains the wall (8AC-RM door 1).
No new idea for the count here; the supply side is closed.

## 8AC-PREFIX. PREFIX-HALL EQUIVALENCE + ACCESS INDUCTION (C155, PROVED_AUTHOR + OPEN UNIVERSAL)

Definitions: prefix sets P_t = {bevs acc <= t}, prefix sites S_t (sited,
plotted <= t). PREFIX-HALL: |P_t| <= 3|S_t| for all t (L inequalities).
Finite faces: implied by all clean runs (prefixes are subsets); prefix-slack
min 0 (!) / med 27 (prefix.json, 300 evals: binds but never negative);
mincut-prefix structure REFUTED (tight sets downward-closed 0.06 percent,
exact-prefix 0 percent: mincuts are scattered slices, not prefixes).
Theorem (proved): PREFIX-HALL <=> HALL. (=>) is trivial (subsets). (<=):
access induction constructing FWD-greedy saturation: assume bevs < t
saturated (matching M); at t, own-E1 pristine (8AC-TO/PRISTINE: zero
past-load, structural) with 3|sites_t| slots absorbs siblings up to cap;
overflow spills to older sites with M-residual R = 3|older| - M-load-older
>= 3|older| - |past| (each past bev loads once total); R >= overflow_t
<=> 3(|older|+|sites_t|) >= |past| + |sib_t| <=> 3|S_t| >= |P_t| =
PREFIX-HALL(t). So prefix counts imply FWD totality (constructive
assignment!) hence Hall (saturating matching => all-Q Hall by cap
pigeonhole). Thus L prefix counts replace 2^|B| subsets (and imply the
8AC-RM overkill route as a corollary).
Two-access warmup (closed, margin 2): t=0: e_B = e_A (8T same-shape) so
Phi = 2e_A(0) >= 0; t=1 burst depth d: pushers >= d/2 (8W, +2/access max)
banking >= d/2 sited Aevs (8S) + e_A(1) >= 1 (nontrivial; trivial-A gives
e_B = 0 too) + e_B(1) <= d (each StepEv consumes >= 1 path link):
Phi(1) = 2e_A(0) + 3e_A(1) - e_B(1) >= d + 3 - d = 2 >= 0.
Dependencies: 8T/8S/8W/8AC-H(i)/8AC-TO/8AC-PRISTINE (banked) + link-consumption
(C129 delivery rows are the per-StepEv consumption facts; loop-to-traceLen
correspondence queued in simulation).
OPEN UNIVERSAL (tight, margin 0): prefix-slack >= 0 for all t (cumulative
E_B <= 3 S_A over prefixes). Finite-strong (min exactly 0). Needs:
link-consumption universals + decoupling-budget (heavy bursts prepaid by
prior net supply, 8T-shape) + tight-prefix coupling (why tight buffers
suffice afterwards). Same hardness as GC-STATIC (equivalent), new shape:
cumulative splay-cost accounting instead of subset matching.

## 8AC-PUSH. PUSH-ACCOUNTING LINKS + TIGHT-WINDOW COUPLING (C156)

Finite links VERIFIED (pushledger.json, 150 histories): e_B <= B-depth + 1
(0/5642 viol); e_A >= A-depth/2 (0/5059 viol); cumulative Phi = 3S_A - E_B
min +2 (never negative). REFUTED/QUALIFIED: first-access equality is IDX-0
ONLY (8T is the very first access; per-key first bursts diverge: 2610/3293
mismatches — test-scope correction, 8T stands); naive global alternation
(#supplyfree <= #supplying + 1) is FALSE (2695 vs 1595; 8R single-shot is
per-state, not global count).
TIGHT-WINDOW COUPLING (precise open obligation for prefix-GC): heavy bursts
(e_B > 3e_A) need buffer Phi(t-1) >= overflow, but buffer can be 0 while
overflow is large; finite says it never breaks (Phi_min +2), so tight
windows must force subsequent-small (decoupling-budget, 8T-shape). Depth
resets at every x-access (both trees root) localize the problem to windows,
but window-net can be arbitrarily negative a priori. Same hardness as
GC-STATIC (equivalent via 8AC-PREFIX); new shape (splay-cost dynamics).
No global telescoping shortcut (rotation total-depth-delta depends on
subtree sizes, unbounded). Status: LINKS PROVED-FINITE + COUPLING STATED;
universal open.

## 8AC-COUPLE. DECOUPLING-BUDGET SHAPE: OVERFLOW SCALES WITH BUFFER (C157)

Measure (tightwin.json, 150 histories, 10,639 points, 2077 divergent
accesses e_B > 3e_A): worst (overflow - buffer) = -6 (global margin 6:
overflow never comes within 6 of buffer); low-buffer (Phi <= 20)
overflow max 5 (n = 11) vs high-buffer max 125 (n = 2066). Overflow
SCALES with available buffer: tight states diverge only mildly;
large bursts occur only when affordable. Tight prefixes: rare (0.2
percent), deep-synced trees (Amax/Bmax med ~60), low current demand
(eB med 1), followed by bigger bursts (med 18) that stay covered
(presumably self-covering via synced depth, cf. 8AC-PREFIX warmup).
This is the decoupling-budget (8T-shape) made quantitative. Mechanism
(WHY tight forces mild / affordable-only heaviness) remains open: needs
push-banking vs splash-drain accounting with state-distinctness (8R) and
freshness bounds. Status: FINITE-STRONG shape + open mechanism.
TRIPLE-COVER (C163, micro.json 150 histories, 2174 heavy bursts): every
heavy burst satisfies buf >= 3*eB (triple_min exactly 0; max burst eB=127
at buf=381=3*127, dA=0, dB=253); heavy bursts never synced (0/2174);
margin buf-overflow >= 4; low-buffer (<=20) heavy max overflow 5 (n=10).
Triple-cover implies prefix safety at heavy bursts with margin 2*eB.
GAP ANALYSIS (why mechanism stays open): B-depth built over window W
since x last rooted satisfies d^B <= 2*E_B(W) (one StepEv deepens a
bystander by <= 2), so e_B(burst) <= E_B(W); closing triple-cover from
prefix-IH alone needs window bank rate >= 4/3x spend rate
(buf(r)+3S(W) >= 4E(W) vs IH's E(W) <= 3S(W)+buf(r)), i.e. pushes that
deepen x must be banked — unproven (supply-free real splashes exist;
needs 8R/freshness). Status: FINITE-STRONG triple-cover + precise gap;
mechanism OPEN.

## 8AC-SYNCED. SYNCED DIVERGENCE IS EXACTLY THE A-TRIVIAL ZIG (C159+C161+C162;
COUNTING CORE PROVED_KERNEL; FINITE-CONFIRMED 674/674)

Statement: per-key synced access (|d^A - d^B| <= 2) with overflow >= 1
(e_B > 3e_A) satisfies (e_A, e_B) = (0, 1) exactly (A-trivial single
zig/double). In particular synced overflow <= 1 always, and synced with
d^A >= 1 is never divergent (overflow <= 0).
Finite face: 674/674 synced-divergent accesses are exactly (e_A, e_B) =
(0, 1) (synpairs); zero synced accesses with overflow >= 2.
Proof (exact StepEv counting): standard splay loop (engine splay_trace
lines 115-140: doubles while path length >= 2, zig iff length 1) gives
e(d) = ceil(d/2) StepEvs for depth-d paths (each StepEv consumes 1 (zig)
or 2 (double) links, telescoping; at most one zig since zig finishes).
Hence e_B = ceil(d^B/2), e_A = ceil(d^A/2). With m = ceil(d^A/2):
overflow = e_B - 3e_A <= ceil((d^A+2)/2) - 3m = (m+1) - 3m = 1 - 2m.
If m >= 1 (d^A >= 1): overflow <= -1 < 0, non-divergent. If m = 0
(d^A = 0, A-trivial): overflow = e_B <= ceil(2/2) = 1 (synced gives
d^B <= 2), with = 1 iff e_B = 1 (B-nontrivial single step) and = 0 iff
B-trivial. So divergent-synced forces (0,1) exactly. Dependencies closed
in kernel: exact counting e = ceil(d/2) via C161 ecount_eq + C162
steps_length_eq + C139 trace_length_eq (engine iterations = skeleton
steps); overflow arithmetic via C162 sync_overflow_le/sync_nondivergent;
consumption e_B <= d^B via C162 eb_le_depth; delivery rows C129 kernel;
zig-finishes via C130 mem_splay / C135 steps_nil_root/splay_noop kernels.
Consequence (decomposition): the prefix-GC universal splits into
synced-trivial (overflow <= 1, buffer suffices: micro-coupling CLOSED C163)
+ diverged-needs-buffer (unsynced, push-built: tier-ledger coupling open).
Status: counting core PROVED_KERNEL; engine-application PROVED_AUTHOR
via simulation kernels (C133/C134); finite face exact.
## 8AC-MICRO. MICRO-COUPLING: SYNCED STEPS PRESERVE PREFIX-GC (C163, CLOSED)
Kernel (GCStaticMicro.lean): micro_couple disjunction (synced depths =>
overflow <= 0 or exact (0,1): e_A = 0 and e_B = 1) + micro_step_zero
(covered steps never decrease buffer) + micro_step_one ((0,1) from
buffer >= 1 consumes exactly one). Buffer side (Lemma B, AUTHOR): (0,1)
splashes are A-trivial with prior rooting banking >= 3 and trivial no-op
intervening, so buffer >= 3 > 1. Finite (micro.json, 150 histories):
synced-disjunction 0 viol (7955 + 4702 nontrivial); synced overflow>=1 is
(0,1) with buffer>=1, 689/689 exact, buffer min 13; ceil-exactness
eB=(dB+1)//2, eA=(dA+1)//2 zero viol in 16776; global Phi_min +2.
Status: CLOSED (kernel counting + AUTHOR banking + finite-strong).

## 8AC-AROOT. A-ROOT PERSISTENCE FORCES BANKED ROOTING + SHALLOW STALE (C160)

Definitions: A-root-x (x at A-root); B-stale-depth (B-depth unchanged by
A-only accesses); supply-free splash ((e_A,e_B) = (0,1), A-trivial + B
single step); rooting event (access bringing x to A-root).
Lemma A (eviction): a B-push on z != x with x at A-root is A-nontrivial
(z not at root) hence moves A-root (delivery, C132 kernel given validity);
so A-root persistence across consecutive accesses implies all intervening
accesses are on x. Corollary: B-depth under persistence evolves only via
x-accesses (x-KEEP splashes reset to root or no-op; x-DELETE preserves).
Lemma B (stale bound): A-root + B-depth d>0 implies d is stale since the
rooting event (no pushes without eviction), and the rooting event (unless
T0/first-safe (8T idx-0)) is a DELETE-nontrivial banking e_A >= 1 (+3 Phi).
Lemma C ((0,1)-closure, kernel-closed C162): an A-trivial splash (e_A = 0) with
synced B-depth <= 2 takes exactly one StepEv (single zig/double finishes
depth <= 2: delivery 2->0/1->0, C129 kernel) so e_B = 1, overflow exactly 1;
prior rooting banked >= 3 (Lemma B) with trivial no-op intervening
(DELETE: e_A = e_B = 0; KEEP: B-trivial else it would have splashed and
lifted earlier), so with strong prefix induction (Phi >= 0 before) the
buffer is >= 3 > 1 and Phi stays >= 2 after. Hence (0,1)-splashes preserve
prefix-GC. Former dependencies now kernel: loop-to-traceLen StepEv
correspondence (C139 trace_length_eq + C162 steps_length_eq: e_B counts
engine iterations = skeleton steps) + single-finish-shallow (C162
shallow_single/shallow_exact) + e(d) = ceil(d/2) exactness (C161
ecount_eq; A-nontrivial-synced half via C162 sync_nondivergent, strictly
helping). Finite face: 674/674 synced-divergent are (0,1); A-nontrivial
synced never diverges (exactness links kernel).
Status: Lemma C kernel-closed; Lemmas A/B + prefix-IH application remain
PROVED_AUTHOR; the diverged (unsynced) branch remains open
(tier-ledger coupling).
## 8AC-TIER. DIVERGED-AFFORDABILITY: MINIMAL THEOREM + MECHANISM VERDICT
(C164-C166; DIVERGED STEP OPEN, funder structure CLOSED)
Minimal theorem (DIVERGED-AFFORDABILITY-WINDOW, repository-native): let H
legal, t a KEEP on x with overflow o(t) >= 2; let W be accesses strictly
after x's last KEEP (B-rooting r; genesis with Phi(r)=0 and dB0=T0-depth
if none). Then Phi(r) + sum_{p in W}(3e_A(p)-e_B(p)) >= o(t) (== buf_pre
>= overflow by ledger telescoping; window.json win_min=4, tele_viol=0).
Sufficient structural form: buffer >= depth at bursts (triple-cover
implies it). Circularity audit: telescoping (ledger arithmetic), delta<=2
(8W.2 rotation geometry), twin-symmetry (splay determinism), genesis
twin-depth equality (A/B both start T0) are all GC-free; the ONLY
GC-adjacent premise would be a window bank-rate law, which is NOT assumed
— it is the open item below.
Mechanism (funder attribution, window.json 2174 heavy windows): DELETE
banking dominates (+562137 vs deep-supplying +42831 vs nondeep +13654 vs
deep-free drain -40290 over 14592 deepening pushes, net +2541 ~ neutral).
Twin-symmetry breaking: A/B start twins; KEEP splays both identically so
all-KEEP histories stay twin forever (adv.json keeponly div=0 all shapes)
with e_A=e_B per access and Phi nondecreasing (kernel twin_run) — hence
DIVERGENCE IS CREATED ONLY BY DELETES (A-splay without B-splay), and every
DELETE banks 3*e_A (kernel delete_step/delete_bank). The (0,127) anatomy:
ONE DELETE banked 381 (e_A=127 on A-vine) then KEEP spent 127 on the twin
B-vine (dB0=253 genesis, window of length 1) — buf=3*127 is one banking
event at 3/unit + one spending event at 1/unit, not repeated units.
Four-routes verdict: (A) scalar global amortized ledger FAILS structurally
(4/3 gap vs prefix-IH, reproduced); (A') window ledger reduces to funder
decomposition (above) but window self-sufficiency is goal-equivalent
(circular) without per-funder rate laws; (B) charging/injection fails on
cap-exhaustion for big bursts (8U residual) except via DELETE-attribution
(same rate-law gap); (C) vector/tier (E1/E2/E4/K, 8H fresh-disjointness)
is the right structure for the maxflow form, but tiers collapse to scalar
for the counting form; (D) minimal-forbidden adds nothing beyond prefix-IH
(diagnosed weak). New route (E) twin-symmetry+DELETE-attribution is the
sole viable path; its missing rate law (deepening pushes banked at >=4/3x
spend, i.e. supply-free deepening sufficiently rare — 8R single-shot per
state + fresh-far rebuild) is UNPROVEN. Long-run grind (L~600): no ratchet,
late margins (1201+) >> early (26+), Phi floor 0 — pool accumulates.
Adversarial (adv.json: 46 greedy runs x 5 T0 shapes incl. non-vine +
starve/freeride/drain/phimin + 150 prior hillclimbs): zero kills.
PAIRING THEOREM (C167, AUTHOR + FINITE-CLOSED 2849/2849): every
supply-free push (e_A=0 + real B-splash) pairs with a same-key banking
DELETE-arrival with FROZEN B-depth between (frozen 2849/2849; no B-touch
possible between since any B-push unroots from A); arrival banks
3*ceil(dA/2), push spends ceil(dB/2) with identical dB (frozen). Kernel
edge: ecount_pos (arrival from depth>=1 forces >=1 skeleton step, hence
>=3 banked). Pair nets reach -118 (diverged arrivals bank ~0); coverage of
pairs comes from the global pool. Turtles verdict: arrival-divergence is
the same problem one level up (built by pushes + shallowness from
rooting/rides); regress bottoms at genesis twins but constants never
close — the aggregate rate law is irreducible and OPEN.
FREE-RIDE FLOOR (C172, FINITE-STRONG): beam-choreographed bystanders ride
16->1 (vine32: (1,15)) but NEVER to exactly 0 unaccessed; last root step
needs access (banking) or genesis-never-left (then B-shallow by 8R).
Hence every nontrivial burst banks e_A>=1 (own zig via ecount_pos) unless
at exact root, and exact-root occupancy postdates a banking arrival.
POOL-DIVERGENCE COUPLING (C173, FINITE-STRONGEST, AUTHOR-candidate):
phased freeride-grind-burst assault stalls — x-frozen accesses net-bank
(pool 21->30 during grind), bursts covered margins 8-43; pool-draining
pushes rotate large regions and disturb the burst key, while missing it
implies local/shallow (banking) splays. Draining the pool while preserving
a diverged burst geometry appears impossible.
Status: funder structure FINITE-CLOSED + twin/DELETE kernel
(GCStaticHistory.lean); DIVERGED-AFFORDABILITY rate law OPEN.
## 8AC-ROUTES. NEW-REPRESENTATION CORPSES FOR THE RATE LAW (C174)
All corpses below are analytic (logic mismatch, no experiment needed) except
where finite killers are cited. Route labels per closure-campaign priority.
- V COAREA/LEVEL-SET: DEAD three ways. (1) Birth-multiplicity: one rotation
  deepens subtree-sized bystander populations (unbounded) vs 6 slots per
  Aev (bounded by push depth). (2) Need-time locality: burst-local slots
  (E1+E2+E4+K) fail on cap-exhaustion (8U residual: rare-x bursts need 252
  with K_x ~ 1); global pool = counting = rate. (3) Level-geometry mismatch:
  B-need is depth-based, Aevs are key-intervals; no natural level map.
- VI DEPTH-TOKENS: DEAD. Token-birth multiplicity unbounded (same bystander
  populations); need-time charging collapses to pool (rate); lifetime/
  discharge exactness cannot survive path compression asymmetry.
- VIII MINIMAL RATE VIOLATOR: subset-minimality INVALID (dynamic replay:
  removing an access replays all downstream differently; no monotonicity).
  First-violation (prefix) form is VALID but yields only the known burst
  geometry (dB>5dA, kernel d6_no_first_violation) — no new leverage.
- I WEIGHTED EDGE/CUT: by-size weights inherit bystander-unboundedness;
  reciprocal/log weights give LOG-factor bounds (wrong constant class for
  6:1). No weighting makes rotation changes local with constant multiplicity.
- II/IV/X RANK/LOG/EARTHMOVER/CLASSICAL: supply-vanishing kills ALL
  classical interfacing (access lemma bounds DEMAND with additive log term;
  supply S_A is independent and vanishes (e_A=0) exactly on dangerous steps;
  no interface without controlling supply-vanishing = the rate problem).
- III PRIMAL/DUAL: dual-of-game certificates are potentials (dead per II);
  dual feasibility constraints are charging-validity constraints (same wall
  as VI). Deferred-heavy, no independent leverage identified.
- VII ROTATION INJECTION: weighted mass with controlled per-rotation total
  impossible (subtree populations); reciprocal weights give log, not constant.
- IX NORMAL FORM: splays/DELETEs do not commute or confluence (tree state);
  no canonical phased violator without changing semantics.
- XI RUN-CANONICAL (new object, BANKED not dead): runs partition history
  disjointly (no double-count); needs+S_A both at run starts (RUN-NEED);
  kernel shapes runstart_bank/genesis_run_surplus/synced_run_le1
  (GCStaticHistory.lean). Open remainder EXACTLY: div-runs deficit vs
  surplus-runs cover (global pool; the rate law in disjoint form).
## 8AC-RV. RUN+FIRST-VIOLATION+TENURE TAXONOMY (C175, AUTHOR precision)
First D6-violation is a run-start KEEP (DELETEs never cross: -6e_A<=0;
mid-run accesses contribute 0 (needs+S_A already posted at run start)).
Two shapes. (A) Run starts with KEEP (first access = burst, x off-root):
deficit need*-6e_A* with need*<=dB (D2), forcing dB>5dA+1+B (kernel
d6_no_first_violation). (B) Tenure shape (run starts DELETE, banks
e_A^del>=1 by root-dislodge, B frozen; first KEEP has e_A*=0):
need*=dB_del-1, deficit dB_del-1-0, needs pool>=dB_del-1 where pool
includes +6e_A^del; uncovered part dB_del-6e_A^del-1 needs global pool
(arrival-divergence: dB_del vs dA^del independent). Genesis/T0-root runs
always surplus (twins: need=0). Synced runs deficit<=1 (kernel
synced_run_le1). So first crossing forces an extreme-divergence burst
whose depth was built by others and whose cover is global pool — the rate
law in sharpest form. Does not close the aggregate (pool composition
needs the rate law). Banked as exact geometry, not proof.
## 8AC-TWINEX. TWIN-EXCLUSION + RE-ARRIVAL PAIR CONDITION (C176, AUTHOR)
Single A-root forbids co-rootedness: a supply-free push (push-key at A-root)
deepening an A-rooted key is impossible (two roots); hence supply-free
deepening forces the burst key off-root (dA>=1), so its burst banks e_A>=1
(ecount_pos), and (0,eB)-bursts pair with a banking arrival + frozen-B
window (arrival must be DELETE: KEEP would un-deep; between-accesses must
be DELETE no-ops else unroot/re-deep). Re-arrival pairs (DELETE-arrival +
supply-free push, same frozen dB): D6-net = 6*ceil(dA_arr/2) - (dB_arr - 1),
negative iff arrival-diverged (dB >> dA). Arrival-divergence regresses
(dB built by pushes, dA shallow via rooting/rides) with no constant
closure — same rate wall in sharpest pair form. Conditional on
free-ride-floor (FINITE-STRONG) for the no-free-return step. Does not
close the aggregate. Banked as exact structure, not proof.
## 8AC-BD1. DELETE BELLMAN UNIVERSAL, AUTHOR (C183)
H1(D_z) <= H1 + 3a_z for every DELETE z, all pair-states (rd<=0 measured
everywhere: walk+beam+exhaustive n<=5). Proof: per-rotation bystander
depth change in {-1,0,+1} exact per region (kernel SplayRotate rows
up/down/ll/lr/r/middle/outer); total rotations in x's splay = d_x exactly
(telescoping: zig 1/1, double 2/2; finite-exact 3517/3517 + banked
b_event_count_lemma); triangle gives depth-drop <= d_x; ceil-subadditivity
gives e_A-drop <= ceil(d_x/2) = a_x; max-algebra + B-freeze on DELETE
(B untouched: b_z fixed) close H1(D)<=H1+3a_x. Halves all Bellman closure
(DELETE branch redundant in F_2+; F_2 needs KEEP lookahead only).
Lean ride-induction deferred (non-sufficient half: BK1 dead +11 anyway;
both halves kernelize together if KEEP side ever closes).
## 8AC-ASYM. ASYMMETRIC ANCESTOR PAIRS DEAD BOTH SIDES (C180)
Phi = #{(u,v): ancestor_B but not ancestor_A} (zero diagonal, nonneg).
B-side: x-pairs destroyed exactly (-d, monotone shed, no new ancestors
for rising x) BUT bystander flips add unbounded signed net (measured B-net
-62173..+478 at n=512; creation O(n) from single-rotation subtree moves vs
cost_A=1 on A-rooted bursts). A-side: creation to +62173 (O(n^2): vine-B
makes every A-flip count since all pairs ancestor-related; ratio O(n) vs
cost_A). Granularity dilemma confirmed sharp: fine (per-pair) breaks CREATE
via bystander O(|b|) flips; coarse (boundaries/groups) breaks RELEASE
(reversed twin-chains: zero edge/segment disagreement at depth d);
path-local needs future burst key; level/count variants hit multiplicity;
rigid coherence kills signed cancellation (same-direction moves);
rotation-distance has CREATE-Lipschitz but NO contraction (splay oblivious,
does not move toward A). Reversed-chains + obliviousness + granularity +
rigidity = four independent exact killers. No Phi of this family closes
CREATE+RELEASE jointly. GC-STATIC + DIRECT-D6 OPEN.
## 8AC-LRI. LOCAL REWEIGHTING KILL TEST (C178; audit REWEIGHTING_BRIDGE_AUDIT.md)
R(A,A') positive log-reweight per single A StepEv (ZIG/LL/RR/LR/RL, every
site, vines/balanced to n=2048): W1-depth R~2n LINEAR unbounded (whole-
subtree gains); W2-subtree R~log n (8.9..21.0) unbounded slowly (merge
ratios); W4-heavy-light-no-max R=2.0 EXACTLY (1 gainer, LR-double, all n)
— bounded positive reweight EXISTS (genuine positive lemma) but LRI-1
fails around it (mass-divergence at c1<=3; log-terms ~11/access on trivial
accesses with zero banking; composition drowns: log-terms + 5.5*S_A reweight
alone exceed GC allowance). Trilemma/dilemma hold: depth-tracking +
persistence + local-increase triple-incompatible under subtree moves.
LRI-for-D6 DEAD. Pair-Access-large-C side door theoretically open
(not pursued; needs LT bridge + endpoints, multi-session scale).
## 8AC-LIT. LITERATURE ARSENAL EXHAUSTED (C177; see audits/LITERATURE_BRIDGE_AUDIT.md)
GI/Russo/L3/L6-theorem/Branch-A/B transplants all dead with exact killers
(log-depth/additive/moving-reference/open-conjecture/anti-correlation;
reference-update creation unbounded ~n^2/2 measured). Surviving fragments
(CP-existence, twin Phi_0=n, subject net-new<=0) insufficient for RATE.
No bridge survives; refinement terminates. Rate law OPEN.
## 8AC-KR. KEEP-RESIDUAL SCALAR SURVIVORS + COLLAPSE REFUTATIONS (C183-2)
PREPEND-2 dead universally with exact mechanism (prepending banks shared-path
depth; vine saving n/4-1 unbounded; minimal killer n=4). ROOT-COLLAPSE dead
both forms (+1 same-root n=32; +1 post-KEEP reachable; small-n collapse holds
but scale-emergent failure like BK1): H2=max(H1,Q) must be carried, never
collapsed. Three finite-held survivors, zero kills: H2-IDENTITY gap=0
(DEL2 redundant; COROLLARY of BD1 since DELETE freezes B); DELETE-H2
(H2(D_z)<=H2+3a_z, universal n=3,4 + scale walks); KEEP-RESIDUAL reach
(Q_x<=Phi, walks+beam+deepdiv; strictly weaker than BK1, holds with margin 55
where BK1 fails +11). Induction scaffold: these + KEEP-2STEP (two-step
lookahead bound, the remaining rate-adjacent gap) preserve Phi>=H2>=H1
(kernel GCStaticKeepResidual). GC-STATIC + DIRECT-D6 OPEN.
## 8AC-LIP. KEEP-2STEP LIPSCHITZ ARCHITECTURE + UNIVERSAL-KEEP-LIP +1 (C184)
R3=max_x[r_x+Q(K_x)]; KEEP-2STEP = Phi(h)>=R3(end(h)) by history induction
from R3(diag)=0 + DELETE-Lip (universal-clean everywhere, tight) + KEEP-Lip
(reachable-clean everywhere; REFUTED universally by +1 on rare large
arbitrary pairs: A-rooted attainer KEEP (0,3), excess exactly 1). y=x case
collapses to KEEP-RESIDUAL (proved+k deep root-noop); gap<=H1(s2) compression
proved; §20 saturation refuted. Remaining gap = reachable-KEEP-Lip =
bystander creation across KEEP in sharpest form. GC-STATIC OPEN.
## 8AC-LIPEX. DELETE z-CHAIN EXACTNESS + BOUNDED-PREPEND (C184-2/3)
Post-DELETE R3-attainer is z itself 98.6%; tight DELETE-Lip ⟹ attainer z;
z-chain grows exactly 3a_z by root-noop (kernelized conditionally;
`splay_at_root` grounds it, H1/Q tree layer pending). Bounded-prepend
(C(x,y)-C(z,x,y)<=a_z) finite-universal tight. Per-chain growth not
Lipschitz (+52 vs bank 45): max-structure mandatory. Remainder: non-z
attainer drop-correlation (2.5%). GC-STATIC OPEN.
## 8AC-TREE. TREE H1/Q/R3 LAYER + STEERED-SIGNATURE VERDICT (C185)
Grounded z-exactness kernel-proved to hNode (GCStaticKeep2Step.lean green);
non-z 1.4-2.5% all slack (tight⟹z up to ties); steered +1-signature holds
tight reachable (post-R3→0), +1 only arbitrary: reachability load-bearing,
pure-state proof impossible. GC-STATIC OPEN.
## 8AC-ZIGSHUT. C.ZIG PROVED; FORMALIZATION GAPS V1-V3 (PIVOT8-1)
Run-proof complete (no reachability/finiteness in math); green: deliver,
splay_at_root, ecount_root, mem_splay, delete_step, ecount_eq,
valid_rotR/L. Open mechanical: doubles-validity + splay induction (V1),
mem-sdepth (V2), history-fold + run/matching model (V3). DO OPEN.
## 8AC-FLEX3. V-CORRECTION + RUN-LOCAL SUM (PIVOT7-2)
V=0 unattained (max -2); run-local sums exactly to FLEX; open on
diverged-closed. DO OPEN.
## 8AC-FLEX2. DOUBLE-FLEX ASSAULT RESULT (PIVOT7-1)
ZIG stands; B<=2A unproved (telescoping dead, counting insufficient,
reformulations tautological); V=0 tight. DO OPEN.
## 8AC-FLEX. DOUBLE-FLEX SCAFFOLD + V=0 TIGHT (PIVOT6-1)
Matching saturates (overflow=FLEX); parse validated; V=0 attained;
run-local tight; ZIG proof + premise audit. Excess-slack open. DO OPEN.
## 8AC-ZIGDOUBLE. DOUBLE DEAD + ZIG PROVED-MODULO (PIVOT5-1)
DOUBLE refuted n=5 ([K5,K1,K5,K3], QB=6>4, all-doubles); ZIG proved by
run-structure (needs validity/ecount-chain assembly); B<=2A needs
excess-slack (open). DO OPEN.
## 8AC-TWOLANE. TWO-LANE VERDICTS + DEFECT FLOOR (PIVOT4-1)
DOUBLE+ZIG zero failures; sharp Z_B=A,Q_B=A-2; B=R_A pattern;
defect min 2; n=8 twin-locked. B<=2A needs proofs. DO OPEN.
## 8AC-ROTANAT. ROTATION/PARITY ANATOMY + RHO6 + LIFTS (PIVOT3-1)
StepEv green; ROT dead (min n=3); R_B<=R_A+Z_A tight; ZIG universal;
invariance twin-only; lip_compose green; rho_6=5/3 exact; 3/2 lifts
all n>=4, 5/3 verified lifts (sup>=5/3); mixed=max by noop-pad;
pattern suggests sup 2. DO OPEN.
## 8AC-RECURRENCE. EXACT CYCLE RATIOS + RECOVERY (PIVOT2-1)
Single SCC n<=6; zero-A impossible (theorem+finite); rho=1,1,3/2,3/2
certified (n=6 pending); extremals all-KEEP; recovery local-2->3/2;
checkpoint agrees; periodic<=1.0 to 256; bias~depth-disc 0.73.
Conjecture rho<=3/2. DO OPEN.
## 8AC-PIVOT. LITERATURE + HEAP-VIOL DEAD + TRANSLATION (PIVOT-1)
LT/Chmel read exactly; only coupled bound missing for DO; translation
green; heap-viol dead (C_min scale law); Chmel polylog under coupling;
wall invariant. DO OPEN.
## 8AC-MACRO. CASE-B MACRO CLOSED + SINGLE OPEN STEP (C193)
Strong induction: DEL/profitable/base free; a_z=0-drain fuses to shorter
(macro green); greedy/SA clean. OPEN: a_z>=1 draining cover only.
GC-STATIC OPEN.
## 8AC-TWIN0. TWIN R3=0 + RESTORATION, KERNEL (C192-2)
R3(twin)=0 exactly; twin+DEL+KEEP restores twin. Steered-clean explained;
diverged states not covered. GC-STATIC OPEN.
## 8AC-LEDGER. STRICT LEDGER + MENU COLLAPSE + TRACE VERDICT (C192)
19-word ledger (min gap 1); winners only {[],[z],[z]+sub,same}; B-single
holds / B-2-word dead; trace-fold absent (SP kernel = major project).
Neither END. GC-STATIC OPEN.
## 8AC-DEFECT. DEFECT IDENTITY + STRICT CENSUS + F3 VERDICTS (C191)
defect_identity green; plus1 defect pure-r_z no-tie; strict len-3 absent
walks/micro-post-KEEP, present micro-s10; F3 fails +2 (ladder dead);
B-saving dead; +1 onset>=19 genuine. Neither END. GC-STATIC OPEN.
## 8AC-TGT. TARGET DIRECT VERDICT (C190)
Closed: STOP/[z]/len2-exact/tie/len1-DEL-mod-SP/doubleroot-kernel. Hard:
strict len-3 same-chain (arbitrary-only failures). Neither END reached;
exact obligations stand. GC-STATIC OPEN.
## 8AC-EXCH. ATTAINER EXCHANGE SELECTOR COMPLETE (C189)
Menu {STOP,[z],[z]+sigma,[z]+sub-tie,same} covers all data; F3/F4 empty;
B-prepend dead (+4); KEEP len<=2 exact; ties diagnose violations; kernel
selector green (O5 word-model specified). Remain: drop-corr + O5 + ROT +
clean/macro + a>=1. GC-STATIC OPEN.
## 8AC-SUBCASE. 1-TERM CLOSED + SINGLE-PREPEND + 2-TERM FINITE (C188)
1-term DELETE closed mod single-prepend (kernel); single-prepend finite
0/2640+ with rotation-counting sketch; 2-term jointness finite-clean;
3-term + KEEP a>=1 open (bystander wall). GC-STATIC BLOCKED/OPEN.
## 8AC-KEEPSPLIT. KEEP = DELETE-Lip + B-FROM-D (C187)
Post-KEEP attainer never z (bystanders carry it); B-Lip false arbitrary,
tight from A-rooted D-states; z drops exactly b_z (kernel); split exact
(kernel). Remainder: non-z correlation both halves. GC-STATIC OPEN.
## 8AC-H1DIFF. SAME-B H1-DIFF + LAYERING IMPOSSIBILITY (C186)
h1_diff_sameB kernel green (floor-aware via foldmax_diff); single-key saving
<=a_z finite-clean; nested lifting multiplies budget per level (jointness
unavoidable); gap-zslack<=-3S derived (needs nested Q-diff). GC-STATIC OPEN.
## 8AC-MAXLIFT. FOLD-MAX DIFFERENCE LIFTING, KERNEL (C185-3)
Per-key drops lift to fold-max bounds mechanics-free (foldmax_diff green);
DELETE-Lip = kernel lifting + open per-key drops + non-z correlation.
GC-STATIC OPEN.
## 8AC-RKC. ROOT-KEEP CLEANLINESS + A-FREE CLOSE (C185-2)
A-free KEEP annihilates R3 on reachable (post=0 always) but not arbitrary
(post to 2): reachability-essential. a_z=0 KEEP-Lip follows (kernelized;
covers both +1 witnesses). Double-rooted-R3 unbounded in general (11).
Remaining: a_z>=1. GC-STATIC OPEN.
## 8AC-VINE. UNIVERSAL VINE-PAIR B<=A PROVED (PIVOT9-1)
V1 (n>=5): vine-preserving splay has depth<=1 (first-double-step analysis:
non-leaf branches via kernel LL/RR/LR/RL; x-leaf mirror continues to a
branching double; n=3/n=4 mirror exceptions real, measured, finite-checked).
Vine-internal costs in {0,1}^2; differ-bit classification ((0,1) flips
1->0 only; (0,0) loops; (1,0) weight -1 unrestricted; (1,1) never flips
0->1) + kernel counting (vine_cycle_nonpos green) => B<=A on vine cycles, all n (finite n<=5,
proof n>=5; re-verified n=6,7). First universal C=1 region; non-vine
excursions remain for general B<=2A. DO OPEN.
## 8AC-VEX. VINE EXCURSION DECOMPOSITION (PIVOT9-2)
Open vine law B-A<=tau(s)-tau(t) proved+kernelized (vine_path_bound green;
bit-convention fixed). Census: n=6 9600 excursions W in [-12,+2] (58 pos);
n=7 46592 W in [-18,+2] (104 pos); max surplus +2, no growth. E0/E1/E2/E3
refuted with exact witnesses (E3 holds all but 8+1 residual-+1 cases);
E4b (B<=3A) holds fully. Residual equation exact; E5-global open (cover
8+1). +2s self-repay (closures<=-11; no vine chaining). Entry=depth>=2
theorem + finite types; exit destroys last branches, costs A>=1. 5/3 cycle
avoids vine-pairs (non-vine max rho=5/3). Hub single-SCC to n=7; sweep
word universal one-way. Anchor conditional proved. DO OPEN.
## 8AC-VVC. VINE-VISITING-C2 CONDITIONAL THEOREM (PIVOT-10A)
9 residual-+1 classes share one signature (A-rooted deep exit + neutral
middles + (1,1) twin re-entry; (2,6)/(4,10)). Debt-machine proves closed
vine-visiting walks satisfy W_2<=0 given D1/F1/F2/R0 (finite+steered
supported; T1 kernel twin_exit_A green): debt-bit (<=1 outstanding via
F2+invariant), first-clearing pairing (disjoint), walk-start-twin tail
paired with payer-before; R0 kills twin-start chaining. n>=5 by V1, n<=6
by global rho. DEBT ROUTE CLOSED (PIVOT-10B: D1 refuted by sweep-return
W=+9/r=+8 witness; hypotheses false not open). Non-vine-only chamber
remains. DO OPEN.
## 8AC-EXBIT. EXCURSION-BIT LAW: REFUTED BY SWEEP FAMILY (PIVOT-10B)
r(E)<=d(s)-d(t) is FALSE universally. Witness n=32 (K1+K1..K32 from
(inc,dec)-vine, 33 all-KEEP): A=31,B=71,W=+9, DT needs W<=+2, residual +8
needs <=+1 (sha c7d01179; smaller n=20 sibling +4/+3). Growth ~n/4 (exit
deep-B + sweep sustaining B/A~2.29). Kills EXCURSION-BIT, D1, E3-universal,
PIVOT-10A debt-machine (hypotheses false). Spares: Lean kernels (true),
PIVOT-9, n<=6 rho, C.ZIG, E4b, global B<=2A (witness open). Universal
partial results stand: vine bit-change all-n (kernel green), re-entry
A-forcing, no-A-zero excursions, length-2 DD/TD. DO OPEN.
## 8AC-VDCR. VINE DISAGREEMENT CREDIT: NEGATIVE ENDPOINT (PIVOT-11)
Endpoint-choice vine encoding bijective (2^(n-1)); pos0=tau; deep-frozen
on vine moves (positions {0,1} only); 8 vine-edge combos. ~40 D variants
falsified (Hamming/weighted/directed/subset/rank/deep-mass/twin-augmented;
proven coefficient contradictions + creation/destruction overlap +
scale-vs-tightness). R0-rule D=2tau: 0 violations n=6,7 macro + UNIVERSAL
on vine paths (n>=5 proof, n<=4 finite; Lean vine_W2_twin_bound green),
range-capped +2 (witness needs +9). Bias flat/uncorrelated. n=32 anatomy:
A=n-1 exact, twin-roots but branched, H 31->0, W +16-10-repay to +9.
No additive positional D closes vine-visiting cycles. DO OPEN.
## 8AC-CDOUBLE. COARSE-DOUBLE Q_B<=2A: n<=6 PROVED + PROGRAM (PIVOT-12)
n<=6 analytic: Q<=B + rho<2 gives Q<2A (A>0; Q<=2A-1); A=0 gives B=Q=0
(direct universal: A-free closed walks never change B). max W_Q=0 exact.
Regressions: 5/3 true (6,4,6) W_Q=-8 eps<=0; 3620 blocks eps=0; n=32
(31,49,22) W_Q=-13 (old +9 was zig-noise); +2s tight. rho_Q<=rho_n.
Epsilon: 4 bad types (all a=0) n=6; 6 types n=7 (+(1,3,0)); ladder universal.
Vine slack q=0 (n>=5). Matching 5/3: 4/4 local. Per-excursion-Q program
(n=6,7 all<=0; universal open: restoration wall). n>=7 open. C=3 DO chain
conditional (B<=3A => 7LT+2g). No new Lean. DO OPEN.
## 8AC-OVF. OVERFLOW GENEALOGY CHARGING (PIVOT-13)
StepEv matching (B-doubles vs 2xA-credits; local+creator+setup; local-first;
Hall extraction). Overflow canonical deepest-first, empirically moot
(~all (0,1,+1); rare (0,2,+2); no (1,3)). lap2-steady FULL: 200/200 hunt-n6,
63/63 walk-n6, 35/35 walk-n7 (genesis 0; creators 1-9 back; chains<=10
terminating). 7 starved-(a=0) Hall failures -> setup rule fixed all.
Nonconsecution (runs all len-1), vine slack q=0 (n>=5), excursion W_2 cap +2,
n32 W_Q=-13, soup banked. Universalization (creator/chains/setup/wraparound)
+ non-vine chamber OPEN. DO OPEN.
## 8AC-U1U4. UNIVERSAL GENEALOGY U1/U2/U3 PROVED, U4 OPEN (PIVOT-14)
U1 cyclic creator in-epoch (consumed-descent; genesis structurally dead);
U2 starved setup exists (dethrone+quiet; mod-m wraparound, no duplication);
U3 <=2 hops (free-credit question separated to U4). H: starved blocks
pairwise disjoint, one starved/block, no shared setup, fan-in O(dB).
U4 closed-component capacity OPEN (fan-in + setup self-competition).
550+ adversarial cycles match (bred maxlen 52); Q_B>2A nowhere.
Lean GCStaticGenealogy green (U1 descent logic). DO path: U4+C.ZIG banked.
## 8AC-U4C. U4-CORE: L1/L2/L3 + MINIMAL-X, U4 OPEN
L1 starved setup always DELETE (dedicated slack, never creator). L2 setups
injective over starved B-active; namers <=1+<=1. L3 non-starved overflow
extremal (n=6 impossible; n<=8 only (1,3), residual <=1). Minimal-X =>
dance-or-concentration (coherent, needs new invariant). Era-correlation +
strong-form + single-builder evidence; no canonical route closes U4
(bubbles conserve; rotation counting tautological). 600+ tests green.
## 8AC-U4M. U4-MISSING: NO-TIGHT-DANCE (ONE LEMMA)
Minimal-X forces tight fully-shared dance (coherent). S1 half-pool OPEN
(cancellation wall vs greedy/census support). NO-TIGHT-DANCE unrealizability
=> U4 => Q_B<=2A. 700+ tests green, Q_B>2A nowhere.
## 8AC-NTD. NO-TIGHT-DANCE: E0 + GROSS/NET WALL, OPEN
Tight dance formal (|N|=|X|-1, no privates); bridge banked (minimal => dance
core). Cell chronology exact. E0: deficits sum to 1 (+fat-creator term).
Escapes/divergence/bracketing attacked; signature null; composition open.
ONE lemma: E0-dance unrealizability. 700+ green, unrefuted.
## 8AC-E0D. E0->DOUBLE: GAP DECOMPOSITION, PER-ACCESS ROOM, STILL OPEN
E0 code-frozen (complete naming); bridge + sole-naming-empty; gap =
excess - slacks; per-access room 150/150; sharing wall stands.
E0/U4/Double OPEN (composition ready, unrefuted). DO conditional.
## 8AC-SHI. SHARING->SLACK: CORRECTION + TWO BLOCKERS, OPEN
Excess=residuals (not namings); canonical needs era+concentration.
Blockers: (i) era (cancellation wall); (ii) residual concentration.
Per-access room 150/150; long-splice green. E0/U4/Double OPEN, unrefuted.
## 8AC-RESJ. RESIDUAL-JOINT: MARGINALS CONSERVED, OPEN
Residuals (not namers); locals-first sufficient; joint tradeoff analyzed
(luck conserved across projections); all falsifications fail=support;
tail ~5sigma (needs 1e6 cycles). ONE missing: joint marginal exclusion.
R<=H/E0/U4/Double OPEN, unrefuted. DO conditional.
## 8AC-FPL. FORCED-POOL + WALL EXHAUSTIVE, OPEN
Zero-fat E0-overfull => genuine Hall failure (no reorder escape).
10 formulations, one wall (sharing vs headroom, independent quantities).
E0 integers work; conjuncts observed; joint unobserved+coherent.
E0/U4/Double OPEN, unrefuted. DO conditional.
## 8AC-E0C. E0_CORE: n<=6 CLOSED + SIGN-LOCKING, OPEN n>=7
Mutations preserve joint-marginal core (all parts load-bearing).
n<=6 closed via era-route (caps+floor; independent proof).
Sign-locking 0/15000+ (sustained same-sign-or-still; fresh unlocks).
ONE irreducible: joint-marginal tight dance +1. E0/U4/Double OPEN.
## 8AC-FRT. FRESH-TRANSIENT: SIGN-LOCKING + PATH-HIT, OPEN
Sign frozen (builder sigma); FRESH structural (arrival+sign-change/T0-touch).
E0 needs freshness (sustained cannot discrepancy 0/15000+); T0-path marginal.
F-D saturated, F-K unproved room, F-T0 ineligible. Compensation OPEN.
ONE atomic: sustained sign-lock theorem. E0/U4/Double OPEN, unrefuted.
## 8AC-PHG. PATH-HIT GLOBAL BYPASS: EXACT YET WALL-BOUND, OPEN
Rotation r=d exact; inventory created=consumed=Q exact; genesis eliminable.
Need D_B<=2D_A+slack (same discrepancy wall, 31 formulations). Q_B<=2A OPEN,
unrefuted. DO conditional.
## 8AC-BIN. BINARY: n<=9 YES-CERTIFIED, n>=10 WALL (HONEST OPEN)
Howard mu*=0 + BF feasible (3/4/7 passes) + verifiers GREEN (2.6M/32.7M/425.5M
inequalities). Max-mean exactly 0 (self-loops). n=10 BF infeasible (time).
Obstruction circular; NO-hunt negative (best -2); 31 formulations one wall.
n<=9 YES; n>=10 OPEN (not NO: no witness). DO conditional.
## 8AC-DUL. DUAL UNIVERSAL: TWIN-MAX REFUTED, OBSTRUCTION BANKED
BF duals mined (battery; locality dead (D varies; roots insufficient)).
Twin-max falsified 80560 (max-recharge cancels twin-payment; max-preserved
caps +1; q>=3 needs setup-era wall). ONE obstruction: max-term dilemma.
n<=9 BF-certified; universal dual OPEN. DO conditional.
## 8AC-FSM. FSM COMPRESSION: INTERFACE BITS INSUFFICIENT, OPEN
Additivity refuted; offsets unbounded; max-depth inverse; projections insufficient.
Twin-max/exceedcount refuted (80560/147128). Interface bits leave 281 multi
(depths unbounded / shapes vacuous). n<=9 BF-certified; universal dual OPEN.
## 8AC-CGR. CEGAR: ABSTRACT-POSITIVE DIES IN DETOURS, OPEN
Twin/root-pair abstract infeasible (positive cycles +1/+2); witnesses
(1,3)-extremal; stitching incompatible (root-pairs differ); BFS detours
repay -32 vs +2 gain (17x; closures dominate). Refinement needs unbounded
info (wall). n<=9 BF-certified; universal OPEN.
## 8AC-L2R. L2 LOOP EXECUTED: GREEN n=7, BOUNDED-PAYMENT WALL n=8/9, OPEN
L2 (rootA,rootB,vineB)+twin-baseline FEASIBLE n=7 (63 classes, verifier
GREEN 2.6M/2.6M); compact form Phi=-2twin-[B non-vine]; DELETE proved
(AUTHOR). n=8: compact RED 72K (q=3), L2/L3 INFEASIBLE (+3 root cycles,
decoded). n=9 q>=4: RED 127K, short exactly 1 (ceiling 3 < need 4).
Unbounded q needs depth-proportional payment (E0-wall). n<=9
BF-certified; universal dual OPEN. DO conditional.
## 8AC-TWN. TWIN-ONLY BEST, MAX-DEPTH OBSTRUCTION, OPEN
Phi=-2*twin: n=7 4484 (classes (0,3),(1,3) x2108/2376), n=8 118760,
n=9 2.2M (adds q=4 corners) — all max-depth short 1-2; every extension
worse (80K/147K/328K). Finite-range universal dual impossible in
twin-family; infinite-range needs depths (wall). n<=9 BF-certified;
universal dual OPEN. DO conditional.
## 8AC-ACR. A-CARRIER: H8 DEAD, PATH-NEIGHBORHOOD SURVIVES, OPEN
31K events; H2/H3 path-determined; H7 necessary (mirror C=5v3);
H8 empty (eliminated). H* = path-neighborhood + y + support + twin/B.
No compressed law; no M. n<=9 BF-certified; OPEN.
## 8AC-GTK. GATEWAY KERNEL: V=V2 n=5 ONLY, POST-COEFFS NEEDED, OPEN
V=V2 82/82 (n=5), fails 1430 (n=6). Identity exact 671K/671K.
Collision datum: Lambda rows; residual = fresh post-coefficients.
328-chain ends vacuous (no compact Z). No M. n<=9 BF-certified; OPEN.
## 8AC-BCL. BELLMAN CLOSURE: PROFILE FAILS n=6, LAMBDA-ROWS NEXT, OPEN
Tight DAGs + D=0 self-loops; P->V clean n=5, 328 amb n=6. Datum:
Lambda-row (c,support), not R values. Horizons 2/5; C-vectors 3
patterns (C_2 only). Profile machine dead (1254/210 amb). No M.
n<=9 BF-certified; universal dual OPEN.
## 8AC-VIN. INTEGRATOR: V EXACT, PROPAGATION UP, NO M, OPEN
Full-graph V exact n=5/6 (mu=0; ranges 0-3/0-5). Tight DAGs; (9,83,1):
V=3=1+2 via K6. Propagation strictly up, 99.5% deterministic. Units:
max-deficit 95%, 86 fails; gateways non-twin/non-vine-B. No M.
n<=9 BF-certified; universal dual OPEN.
## 8AC-CMP. COMPILATION: R_T EXACT, AGGREGATIONS DEAD, OPEN
R_T fold + D_s exact; K_+/sum/max/major/K_1/K_abs all refuted (mass
moves+amplifies; spikes to 45). A-budget rewritten; pairing open.
Max-mean-D=0 (no cycle bar). No M; DO chain preserved. OPEN.
## 8AC-SLV. MACHINE SOLVED; TWIN+DB WALL ALGEBRAIZED; OPEN
R-fold exact (7/7 match); absorption universal; T-maps derived.
Identity: surplus=2a+2(1-t_pre)-R. DELETE proved; KEEP iff R<=budget.
No K emerges. M: fringe-mass payment terms. n<=9 BF-certified; OPEN.
## 8AC-RCM. RECOVERY MACHINE PROVED; ZIG UNBOUNDED; OPEN
X* (G maps, fringe, twin, supply) proved symbolically; 346/346 +
41/41 green. Residual: absorption monotone; zig-outer family unbounded
(r=n-4); no uniform bound; r<=2a false. Mixed induction + universal
proofs open. n<=9 BF-certified; universal dual OPEN.
## 8AC-HNR. HIGH-NEED RECURRENCE DETERMINISTIC, HELD-OUT, OPEN
55 high-need (3..15): X4-fringe exact (3247 states, 0 amb); (L,R)
recurrence + supply 41/41 held-out (RL bug fixed). A/B: NO (rises);
single invariants all fail; WORLD B (bounded, access-local). Next:
arbitrary-subtree update proofs. n<=9 BF-certified; universal dual OPEN.
## 8AC-RCV. RECOVERY: SECOND-DOUBLE + ZIG RULES, OPEN
Hard-first necessary 100%; second double => recovery 100% (484 cases);
zigpay exact from (first config,twin,top-outer). Boundary n<=6.
n<=9 BF-certified; universal dual OPEN.
## 8AC-DSC. DISCOVERY: FIRST-HARD NECESSARY, RECOVERY OPEN
Exhaustive census: unpaid=>first-hard 100%; first-easy=>never borrower.
77% recover via absorption+twin; unpaid in q=1 zigzig-hard-first.
Cross-access 0 persistence (access-local). Missing: recovery predictor.
n<=9 BF-certified; universal dual OPEN.
## 8AC-RLT. REALITY: PAY FACTORED, NAKED ARRIVAL, OPEN
650 doubles: pay=twin+size-formula exactly (shape-blind rigorously).
Hard=naked arrival (inner 0.40 vs 2.60) + outer mass + twin kept.
Debt inverts via absorption; lineage: persist/migrate/split.
Missing: size-evolution meter. n<=9 BF-certified; universal dual OPEN.
## 8AC-BDB. B-DOUBLE PAYMENT: 4 DEAD, TABLES EXACT, OPEN
rho 824 / D2 1318 @n6 dead (exchange false / trade); E1 dead n=2 zig;
E_del dead 11/20. Symbolic tables 346/346 (recharge=outer-descent).
Twin never destroyed in B-phase. No live D; conditional proof recorded.
n<=9 BF-certified; universal dual OPEN.
## 8AC-XCT. EXACTIFICATION: FROZEN EXACT, RESOURCE-UNRESOLVED, OPEN
41K rows replay-verified (0 real mismatch; 41,024 distinct primitive).
Gauge proved; no free equalities. Exact LP blocked (degenerate solves
>=20 min; no sparse exact simplex). t*~=0; no Farkas. Template
viable-at-float, unrefuted. n<=9 BF-certified; universal dual OPEN.
## 8AC-CUT. CUTTING-PLANE: FLOAT n=7 OK, EXACT UNRESOLVED, OPEN
67->41K genuine rows, LP always feasible (no Farkas). Float converged
(2.5M, tol 1e-4). Exact oscillates (rounding fragility at t*~=0;
3880/13588 break at /1024). Template viable-at-float; exact verdict needs
exact rational LP (unavailable). n=8 deferred. DELETE finite OK.
n<=9 BF-certified; universal dual OPEN.
## 8AC-GRW. GROWTH ROUND: 133 FEASIBLE, R1 DEAD, UPDATES DERIVED, OPEN
n=11 range law verified (ternary non-universal). 66 growth rows (to n=64).
Free g exact 0/133 (±5/22 ternary; range tight vs n=64 bound). R1
majority-list refuted 27/133 (candidate failure). Rotation eta-updates
engine-checked (rigid sets identical; down-push measured). DELETE finite
28 OK, universal open. n<=9 BF-certified; universal dual OPEN.
## 8AC-UCT. UNIFORM CONTEXT ROUND: DEPTH-TEMPLATE DEAD, ETA ALIVE, OPEN
42-transition cert verified twice (surplus 10971177); sum-f(dA,dB) dead
(scoped). eta=(dA,dB,nA,nB,omega) survives old multipliers (415 nonzero).
Free g on 67 edges: feasible exact, all coeffs in {-1/9,0,1/9} (sparse
only). No evaluator yet. DELETE proved (AUTHOR); KEEP open. n<=9
BF-certified; universal dual OPEN.
## 8AC-POS. POSITIONAL ROUND EXECUTED: ADDITIVE EXCLUDED, POS/POSA DEAD, OPEN
-2t+F(A)+G(B) impossible (n>=64, verified). alpha_pos splitting confirmed
(LCA 8v7/8v2); POS-8 infeasible (5-cycle), POSA(+mdA) infeasible (6-cycle,
same archetypes re-routed). No live candidate (C4 term-only). DELETE
proved (AUTHOR); KEEP open. n<=9 BF-certified; universal dual OPEN.
## 8AC-RPR. REPAIR ROUND: EXCLUSION PROVED, C4 REFUTED-AS-COMPLETE, OPEN
No F(rootA,vineA,T_B) (n>=64, verified); L2-L4 families universally void.
L4 stitches need keyed fuel-placement (no coarse A-bit separates; loop
diagnosed). Battery 21: C1/C3 dead, C5 7 fails, C4 3 fails (D_B-rise only;
term-only). DELETE proved (AUTHOR); KEEP open. n<=9 BF-certified;
universal dual OPEN.
## 8AC-PSR. PAIR-SENSITIVE ROUND: §4 PROVED, L4 DEAD, C4 ACTIVE, OPEN
F(root_A,T_B) impossible (n>=64, verified); A-shape necessary. L4
(+fuel bit) infeasible at n=8 (+2 cycle); stitches agree on all coarse
features (spine-geometry chase withheld). Battery: C1/C3 dead (14),
C5 wounded (5), C4 active (+D_B, 3 zig-rise fails). DELETE proved
(AUTHOR); KEEP open. n<=9 BF-certified; universal dual OPEN.


## 8AC-RSL. ROOT-SELECTED: GATE I PROVED, GATE II OPEN
H_y=-R+4*absorbed; DA0-ROW universal (fold bounds); regression 0/19K.
D=D0+DDEL exact; DDEL<=0 proved. Absorbed-H RS refuted (all kappa);
joint fiber feasible+strict. Universal RS + residual + CD open.
## 8AC-GRG. GAUGE RIGIDITY: FINITE R1 + FIBER R2-LEAD, OPEN
B-only gauges drop-free n=5/6 (LP+circulation); twin harvest dead
(DELETE). da=0 (x=y=A-root) fiber harvests robustly, atomwise-valid;
universal program open. VERDICT R4. n<=9 BF-certified; OPEN.
## 8AC-ATI. ATOMIC WEIGHT = TAUTOLOGY, COHOMOLOGY, OPEN
Single-atom Bellman solves exactly (16 types, cover 100%) but h =
2-lambda = forbidden tautology (slot-independent). No genuine margin
forced; merges/splits per-z exact; root bounded. Universal h_k +
aggregation open. n<=9 BF-certified; OPEN.
## 8AC-STC. STATIC CARRIER: STATIC-A PROVED, OPEN
5214 A-static events; fresh 100% latently sourced; full-claim Delta
0 amb; twin 0->1 99.5%; M_static naive 43.7% (weighting open);
static recharge exists (6972). Next: weighted integrator + coupling.
n<=9 BF-certified; universal dual OPEN.
## 8AC-SGX. SINGLE-CROSSING REFUTED, OPEN
B-coeffs appear on A-static keys (witness (18,12,5,1): d=1, single
support, no A-cut sees it). No motion-cut carrier suffices; richer
carrier (cut + static B-coeffs) forced but unlaunched. No M.
n<=9 BF-certified; universal dual OPEN.
