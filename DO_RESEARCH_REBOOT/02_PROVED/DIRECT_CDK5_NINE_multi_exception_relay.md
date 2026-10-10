# DIRECT-CDK5N-MR: disjoint multi-exception relays (PROVED · CDK5NMRP-A)

**Status: PROVED** (universal restricted class). Five genuine KEEP keys,
nine-node marked B-core throughout, complete exception set E (|E|≥2) with
(c=1,q=3,H=1; w=1,R=0 each), maximal creditless relays (c=1,H=1,q≤2;
w≤0,R=0), first-nonbridge payers (c=1,H≥2,q≤3; w≤1,R≥2), pairwise disjoint
packets, all other positive debts Type K/P ⇒ Q_B≤2A, for arbitrary n/length/
m/t_e/order/DELETEs/prefixes/seams. Complement, K≥6, universal Coarse-Double,
DO remain OPEN. Disjoint from CDK5NP-A (H=1 exceptions), S1/S2 (creditless
successors), VR (multiple exceptions); not a corollary of any.

## Proof (complete)

Cyclic interval identities (exact seam; DELETEs once; C_K not C_X). Baseline
H≥c (A-root-change; disjoint reservation; no-op-tolerant). Nine-core ⇒ d_B≤8
⇒ q≤4; c=0⇒q=0; positive debt w∈{1,2} (no Q≤2C_K claim). Exceptions (1,0)
exclude K/P universally; E-complete by definition (no hidden exception: any
(c=1,q=3,H=1) interval IS listed; bridge/payer predicates reject it). Bridges:
finite summation over arbitrary t_e (all q∈{0,1,2}; negatives help; no tree
induction). Payers over full q≤3 (worst w=1≤R). Per-packet 1+0+1≤0+0+2.
Maximal scans deterministic (one E ⇒ one packet family). Pairwise disjointness
(H5 index arithmetic; no shared payer/bridge; no exception inside another
packet). Others: w≤0 via R≥0; w>0 via K (H≥2) or P (same-interval distinct
DELETE+KEEP); overlap once. Partition disjoint/exhaustive ⇒ Σw≤ΣR ⇒
Q_B−2C_K≤2(A−C_K) ⇒ **Q_B≤2A**. Full derivations + 32-point audit + 46-attack
audit in 06_CERTIFICATES files.

## Evidence

SHA-pinned fixtures (forbidden rejected); INC 55/36/16 + CTL-A 31/18/8 + CTL-B
62/36/16 + CTL-C 58/36/16; exact closure; both engines; core 9; intervals exact
(two t=2 packets {4,5,6,7},{12,13,14,15}; K3 debts Type P/K; CTL roles verified:
A-S1-shape, B-doubled-VR-member-non-novel, C-doubled-S2). Independent tuple-first
verifier (raise-based, optimization-safe) PASS. Strict novelty retained
(K3a AM-G G2+G4 fail; K5-local AM-G/S pass openly noted; five REJECTs; primitivity;
anti-concatenation; no superseder).

## Scope

Exactly the authorized MR class — no complement, no K≥6, no universal.
