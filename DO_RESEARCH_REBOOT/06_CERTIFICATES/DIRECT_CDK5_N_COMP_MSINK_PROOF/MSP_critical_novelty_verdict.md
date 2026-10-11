# OUTCOME B erratum — cyclic novelty obstruction (append-only, supersedes novelty)

## Decision: CYCLIC NOVELTY OBSTRUCTION — CERTIFIED

The frozen IN witness (`19ff110a…78df`, n=34, A=61, Q=36) admits a
source-valid cyclic decomposition into banked-covered closed segments.
Evidence: `MSP_rotation_replay.py` (fresh independent machinery, no Gate-0
imports) + `MSP_cyclic_decomposition_certificate.json` (full values below).

## Certificate

- P_1 == P_17 exactly (full labeled A/B serials, both engines agree).
- Segment 1 = accesses [1,17) (16):
  `D4,K3,K7,D5,K1,D4,K9,K5,K7,K1,K9,D2,D5,D6,D9,D5`,
  replayed from live P_1 trees: closed (ends P_17=P_1), A=30, Q=18,
  five genuine keys {1,3,5,7,9}, core9 at all 17 boundaries, s=8 intervals,
  S1-H1–H5 strict ALL HOLD (unique (c=1,q=3,H=1) exception, successor
  c=1/q≤3/H≥2, all other positives strict-K/P). **S1-covered from P_1.**
- Segment 2 = accesses [17,34)+[0,1) (18), string-identical to the banked VR
  word rotated left by one (`D4,…,D9,D5`); starts P_17=P_1 = VR post-D5 state
  (verified equal); first 17 transitions identical to VR tail (dA/dB/a/q
  per-access equal); closed back to P_1; A=31, Q=18; VR-H1–H5 strict ALL HOLD
  (unique exception, relay t=2 ∈ [2,6], payer H≥2/q≤3, others strict-K/P,
  domain 5 keys + core9). **VR-covered from P_1.**
- B4 additivity: 30+31=61=A, 18+18=36=Q (partition, each access once).
  Banked S1 gives 18≤60, banked VR gives 18≤62, hence Q(IN)≤2A(IN) follows
  from CDK5NS1P-A + CDK5NVRP-A alone.

## Applicability (non-diagonal start)

Both frozen domains read "admissible reachable exactly-closed pair-walks"
(S1P: "No A=B assumption on the measured cycle"); P_1 is reachable (IN
prefix from T0) with core9 throughout; all proof lemmas (interval
identities, A-root-change baseline, nine-core debt) are start-independent
for closed walks. No diagonal-start hypothesis is used by either proof.

## Consequences (frozen)

- R4 certification FAILED on the frozen IN witness; R1 new-coverage
  certificate NOT ESTABLISHED (∅ ≠ MSINK∩R5 unwitnessed; OUT alone
  insufficient per authorization). R2/R3 not reached for promotion.
- The Gate-0 anchored (P_0-split) additive checker missed this decomposition:
  IN has no proper P_0-split, but rotation at boundary 1 exposes it. The
  Gate-0 decomposition-impossibility lemma is valid only for S0-anchored
  partitions and does not cover cyclic rotations — recorded here as the
  precise Gate-0 evidence defect (no rewrite of historical files).
- The MSINK universal L1–L7 payment argument is NOT refuted by this finding
  (no counterexample to Q≤2A; both segments satisfy it). It is preserved
  separately as an uncertified mathematical result; no promotion follows.
- No witness replacement, no new search, no H1–H6 change, no MSINK-PROOF
  launch, no ledger/dependency promotion, no 02_PROVED change.

## Scope preserved

Gate-0 record immutable. Banked S1/VR/MR theorems untouched. Complement, K≥6,
universal Coarse-Double, Dynamic Optimality remain OPEN.
