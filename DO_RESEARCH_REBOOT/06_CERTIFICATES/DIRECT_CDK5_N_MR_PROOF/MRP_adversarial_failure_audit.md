# MRP adversarial audit — Gate-0 30 + 16 certification attacks, all discharged

Gate-0 30 (seam DELETEs in K3-H=18 ✓; 33 blocks=33 accesses, all a≥1 ✓; C_K=16
exact ✓; only K3/K5 debts (w=1 each; K3b w=1 too) ✓; bridges need nothing ✓;
payers ∀q≤3 ✓; K/P others ✓; scan deterministic ✓; t+2≤s distinct incl. seam
wrap and whole-cycle equality ✓; E-complete (H=1,q=3 scan finds both) ✓;
no hidden positives ✓; K/P overlap once ✓; payer/bridges never recharged ✓;
core 9 all 34 states ✓; DELETEs frozen (traced) ✓; no prefix/cycle confusion
(no prefix; cycle-only) ✓; finite⇒universal via per-interval arithmetic
(arbitrary m/t) ✓; K5-local AM-G/S affirmed, global denied ✓; K3 double
obstruction recorded ✓; five REJECTs (hashes kept) ✓; primitivity (aperiodic,
no pair-subcycle) ✓; DELETEs genuine (closure-necessary) ✓; Q≤2C_K refused
(+4 here) ✓; payer membership-tested (H4) ✓; MR≢universal (H1–H6 narrow) ✓;
no 02_PROVED in Gate 0 ✓; no auto-launch ✓).

Certification 16: (1) bridges need q≤2 not =2 (0/1 covered; negatives help) ✓;
(2) negative bridge debts fine (w≤0) ✓; (3) no-op in bridge keeps H-count exact
(H sums actual StepEvs; predicate intact) ✓; (4) t=s−2: packet length s, distinct,
valid ✓; (5) scan cannot skip payer (first-nonbridge rule) ✓; (6) E-complete ⇒
one packet per exception (scan from each) ✓; (7) Type P DELETE in same interval
by construction (preceding-occurrence rule) ✓; (8) payer reserve never reused
(partition-enforced) ✓; (9) negative singletons never compensate (they only
satisfy their own w≤R) ✓; (10) A=B never assumed (divergence traced) ✓;
(11) prefixes cycle-excluded by definition ✓; (12) no nine-key-tree dependence
(marked paths only) ✓; (13) fixture SHAs + forbidden rejection kept ✓;
(14) no older acceptance (full regression) ✓; (15) repeated cycles with two
exceptions excluded by E-completeness... precisely: CTL-B (doubled VR) HAS two
exceptions and IS MR-admissible by predicate — correctly distinguished as
nonnovel (additive VR cover), not as predicate failure ✓; (16) replay≠kernel-proof
labeled honestly (proof in lemma files) ✓.

No unresolved attack. Promotion may proceed.
