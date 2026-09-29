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

## What the scaffold closes / leaves open

Closes: E1-zone (with E1-CAP), K persistence, setup freshness (conditional),
riser geometry, W block structure, causality (E4 snapshot fix).
Leaves open (exact): B-heavy all-3 convergence — entry-load ≤ 2 unproved
(0 sat-entries / 44,000+), young-transient-exposure unproved, load-3 scattering
unproved. No counting argument attempted (GC-reduction forbidden and avoided).
