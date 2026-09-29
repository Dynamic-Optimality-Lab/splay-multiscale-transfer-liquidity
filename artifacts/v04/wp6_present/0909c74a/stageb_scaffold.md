# Stage-B Scaffold — rigorous micro-lemmas (author-level PROVED)

Status: PROVED_AUTHOR (each: proof + finite check, 0 violations). GC-independent.
Lean-pending as a block. Date: 2026-09-30 (C30). Verifiers: `wp6_microverify.py`
(`microverify.json`), `wp6_stepprobe.py` (`stepprobe.json`).

## ML-E1-ENTRY (E1 members enter at load 0)

Statement: E1(t) members first appear in N at the first B-StepEv of access t,
with load exactly 0.
Proof: aev ids are created during t's A-part. E2/E4 reference strictly earlier
accesses (pump windows u<idx; setup-at-idx snapshot ≠ idx). E3 same-access
eligibility is exactly access-t B-events. Hence no earlier B-event can include
them; at t's first B-event zero in-access picks have occurred.
Check: 5046 entries, 0 violations (the 11 phantom E1@1 under future-leaking E4
vanished after the causality fix — they were pre-loads from future E4 picks).

## ML-K-PERSIST (per-key persistent core)

Statement: for every x-access t and every B-StepEv b of t, every sited A-StepEv
a of a strictly earlier x-access with x ∈ rotated(a) is E3-eligible for b.
Proof: A-side node is always the splayed key (verified 2870/2870 steps), so every
A-StepEv triple of an x-access contains x; B-side likewise, so every B triple of
an x-access contains x; intersection ∋ x.
Check: 15316/15316, 0 violations.

## ML-ADJ-E4 (adjacent DELETE→KEEP pristine setup)

Statement (conditional): adjacent DELETE-x → KEEP-x with x non-root-before the
DELETE (so setup[x] = DELETE idx): at KEEP's first B-event, E4 members have
load exactly 0.
Proof: E4 = DELETE's A-StepEvs (fresh ids); DELETE accesses emit no B-events;
adjacency gives zero intervening B-events; E2/E3-past-only cannot predate
creation. Hence loads 0.
Check: 65 adjacent pairs with nonempty E4, all members load 0, 0 violations
(covers both setup-updated and setup-older subcases empirically; lemma claims
only the updated subcase).

## ML-DISPLACE-STEP (per-StepEv riser containment)

Statement: within one A-StepEv on x, every key whose depth decreases is x or a
member of x's pre-step subtree.
Proof: rotation case analysis (zig / zig-zig / zig-zag): the ascending key is
always x; p/g descend or hold; reattached subtrees shift ±1 with only x's
other-side subtree rising. Verified: node always x (2870/2870), triple always
∋ x (2870/2870), riser violations 0/2870.
Corollary (multi-step hoisting): per-access rises of outsiders decompose into
descendant-position hoist steps. Raw per-access "displacement monotonicity" is
FALSE (24% bystander rises); the per-StepEv form above is the correct statement.
Consequence: H4 "B-heavy ⟹ recent x-access" is WEAKENED (hoists shallow without
x-access); K-deposits remain the x-fodder source (ML-K-PERSIST), freshness at
creation with transient leak still open.

## ML-RISE-WITNESS (node/triple exactness)

Statement: bottom-up splay node is always the splayed key; every StepEv triple
contains it. Hence every x-access creates e_A(x) x-containing sited A-StepEvs
(future K-deposits / E3-fodder for x). Verified 2870/2870, 0 violations.
Note: hoisted (non-node) keys do NOT create own-key triples — only own accesses
supply per-key fodder. K-deposit freshness is at-creation only.

## ML-W-BLOCKS (transient match structure)

Statement: per (B-splay, W-member), E3 matches arrive in ≤ 3 blocks
(≤ |S| for rotated triple S ∌ x), each block short.
Argument: B-triples sweep rootward monotonically within a splay; each non-x key
of S persists in triples over a contiguous ancestor-occupancy block; blocks per
S-key, gaps split. Check: 5562 member-splays, max 3 blocks, max run 3, 0 over.
Status: author-proof-sketch + strong finite check (occupancy contiguity per key
is sketched, not fully audited — flagged for tightening).

## ML-RUN-STRUCTURE (≤1 demanding KEEP per x-run)

Statement: in any maximal run of consecutive x-accesses, at most one KEEP has
e_B > 0 (the first KEEP of the run). DELETEs never have B-events.
Proof: B moves only at KEEPs (B-freeze, banked T3). After the run's first x-KEEP,
x is B-root. Run-interior DELETEs skip B. Later x-KEEPs splay x at B-root =
no-op (root-dislodge), e_B = 0. DELETE accesses emit no B-StepEvs by Pair Access
definition (DELETE: (A,B) -> (S_x A, B), y = 0).
Dependencies: Pair Access defs, B-freeze, root-dislodge. (No corpus needed.)

## ML-FRESH-CHANNEL (every demand has fresh supply)

Statement: every demanding KEEP (e_B > 0) has E1 ≥ 1 sited-fresh, OR (E1 = ∅
AND E4 = pristine accA[s] with e_A(s) ≥ 1, s = run-start DELETE, loads exactly 0
at t's start).
Proof: demanding ⟹ access is KEEP. A-root is always the last-accessed key.
Case (a) H[t-1].x ≠ x: x is A-nonroot ⟹ A-splay nontrivial ⟹ e_A ≥ 1, all sited
(U=0) ⟹ E1 ≥ 1 fresh-0 at start (ML-E1-ENTRY).
Case (b) H[t-1].x = x: x is A-root ⟹ E1 = ∅. Demanding ⟹ t-1 is DELETE (a
KEEP→KEEP repeat leaves x B-root = B-no-op, e_B = 0). So t continues a DELETE-run;
let s be the run's first x-access. If s is KEEP then s = t (t first KEEP),
contradicting H[t-1] = x — hence s is DELETE with H[s-1] ≠ x, x nonroot ⟹
setup[x] = s, e_A(s) ≥ 1. Interior DELETEs see x at root (no setup change); no
interior KEEPs precede t. Hence E4(t) = accA[s], ≥ 1 sited. Loads: members created
at s; zero B-events between s and t (interior DELETEs emit none; t first KEEP);
run-interior all-x (no other-key transient picks) ⟹ loads exactly 0 at t's start.
Corner: run from access 0 with x = T0-root gives setup-absent + E1 = ∅, but then
B never moved x (B-root throughout) ⟹ e_B = 0, no demand. Complementarity: E4 = ∅
with demand forces setup[x] = idx (self) ⟹ x nonroot-before ⟹ E1 ≠ ∅.
Dependencies: Pair Access, B-freeze, root-dislodge, U=0, setup rule, ML-E1-ENTRY,
ML-ADJ-E4 (generalized by the run argument above), ML-RUN-STRUCTURE.

## FRESH-CAP (subsumes E1-CAP)

Statement: demanding KEEP with e_B ≤ 3f, f = fresh slots (|E1| in case (a),
|E4|-pristine in case (b)), satisfies minload ≤ 2; e_B ≤ 2f gives ≤ 1.
Proof: fresh loads ≤ in-access picks only (E1: E2/E4-earlier + E3-same-access;
E4-pristine: run-interior x-only + creation-at-s). Pigeonhole over 3f slots.
E1-CAP is the case-(a) instance; kept as separate artifact for history.

## ML-DILUTION-ZERO (deep-safe zone, minload exactly 0)

Statement: demanding KEEP with e_B ≤ f, f = structural fixed-fresh slots
(|E1| case (a); pristine-|E4| case (b)), has minload 0 at every B-event.
Proof: fixed-fresh members (E1: fixed set, fresh-0, loads only in-access;
pristine-E4: fixed set, loads exactly 0 at start, only in-access after) cannot
exit; in-access picks before the last B-event ≤ e_B − 1 < e_B ≤ f = their count,
so one remains at 0. It lies in N (fixed ⊆ N).
Check: 9252/9252 B-events, 0 violations (`dilution.json`). Strengthens E1-CAP in
the deep-safe zone (exact 0, not just ≤1). Dependencies: ML-E1-ENTRY,
ML-FRESH-CHANNEL, E1/E4 fixity within access.

## ML-K-RATCHET (old-K monotone + per-round dilution + fill order)

Statement: (i) old-K-member loads are monotone non-decreasing across x-accesses
(picks only add; K-membership persistent per ML-K-PERSIST; new deposits are fresh
ids at 0). (ii) Within an access, least-loaded fills by level, oldest-first
within a level (hence spread ≤ 1 surfaces; C33 synchrony).
Status: (i) PROVED_AUTHOR (immediate from banked structure). (ii) Descriptive
(water-filling view). WARNING: water-filling taken as closure ≡ GC-counting
(total picks vs capacity) — explicitly DISCARDED as a proof path per the
no-GC-reduction rule; kept only as qualitative description of synchrony/ladder/
dilution. The race inequality (picks vs dilution) is empirical (C33 margins),
not universal.
Empirical (B-heavy, `dilution.json`): K-0 median 3 (stayed minload-0, n=177) vs 0
(elevated, n=25) — K-0 absence characterizes elevation (round-2+ gate); E2-0/W0
medians 0/0 (thin at access start; W arrives mid-splay).

Closes: E1-zone (with E1-CAP/FRESH-CAP), K persistence, setup freshness
(conditional + run-pristine), riser geometry, W block structure, causality
(E4 snapshot fix), demand/supply pairing (RUN + FRESH-CHANNEL: B-heavy overflow
is the ONLY remainder).
Leaves open (exact): B-heavy all-3 convergence — entry-load ≤ 2 unproved
(0 sat-entries / 44,000+), young-transient-exposure unproved, load-3 scattering
unproved. No counting argument attempted (GC-reduction forbidden and avoided).
