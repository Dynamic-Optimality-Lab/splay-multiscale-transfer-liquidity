# VRP adversarial audit — 30 Gate-0 + 16 certification attacks, all discharged

Gate-0 30 (seam DELETEs in K3-H=13 ✓; 18 blocks=18 accesses, all a≥1 ✓; C_K=8
exact ✓; only K3/K5 debts ✓; bridges need nothing ✓; payer ∀q≤3 ✓; K/P others ✓;
scan deterministic (exact predicates, bounded s) ✓; t+2≤s distinct incl. seam
wrap and whole-cycle equality ✓; uniqueness from H2 ✓; census complete (K3-Type-P
only other) ✓; K/P overlap once ✓; payer never recharged ✓; core 9 all 19 ✓;
DELETEs frozen (traced) ✓; no prefix/cycle confusion (no prefix; cycle-only) ✓;
finite⇒universal via per-interval arithmetic (no witness induction) ✓; K5-local
AM-G/S affirmed, global denied ✓; K3 double obstruction recorded ✓; five
REJECTs (hashes kept) ✓; primitivity (aperiodic, no subcycle) ✓; DELETEs genuine
(closure-necessary) ✓; Q≤2C_K refused ✓; payer membership not existence ✓;
VR≢universal (H1–H5 narrow) ✓; no 02_PROVED in Gate 0 ✓; no auto-launch ✓).

Certification 16: (1) bridges need q≤2 not =2 (0/1/2 exhausted, negatives help) ✓;
(2) negative bridge debts fine (w≤0) ✓; (3) no-op in bridge keeps H=1 only if
a=0... a no-op KEEP (a=0) in a bridge would still give H=1 iff exactly one a=1
access present — H counts actual StepEvs, predicate intact ✓; (4) t=s−2: packet
length s, distinct, valid ✓; (5) scan cannot skip payer (first-nonbridge rule) ✓;
(6) uniqueness ⇒ one packet (scan from the unique j*) ✓; (7) Type P DELETE in
same interval by construction (preceding-occurrence rule) ✓; (8) payer reserve
not reused (partition-enforced) ✓; (9) negative singletons never compensate
(they only satisfy their own w≤R) ✓; (10) A=B never assumed (divergence traced) ✓;
(11) prefixes cycle-excluded by definition ✓; (12) no nine-key-tree dependence
(marked paths only) ✓; (13) fixture SHAs + forbidden rejection kept ✓; (14) no
older acceptance (full regression) ✓; (15) repeated cycles with two exceptions
excluded by H2-uniqueness (CTL-B demonstrates) ✓; (16) replay≠kernel-proof
labeled honestly (proof in lemma files) ✓.

No unresolved attack. Promotion may proceed.
