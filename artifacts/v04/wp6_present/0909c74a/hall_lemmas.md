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
