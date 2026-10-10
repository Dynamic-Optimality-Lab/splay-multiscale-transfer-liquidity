# DIRECT-CDK5N-S1: one-successor transfer (PROVED · CDK5NS1P-A)

**Status: PROVED** (universal restricted class). Five genuine KEEP keys,
nine-node marked B-core throughout, exactly one exceptional interval
(c=1,q=3,H=1; w=1,R=0), immediate successor (c=1,q≤3,H≥2), all other positive
debts Type K/P ⇒ Q_B≤2A, for arbitrary n/length/order/DELETEs/prefixes/seams.
Complement, K≥6, universal Coarse-Double, DO remain OPEN. Disjoint from (not a
corollary of) CDK5NP-A: the exception fails both Type K and Type P by H=1.

## Proof (complete)

Cyclic KEEP-interval identities (exact seam; DELETEs once; C_K not C_X).
Baseline H≥c (A-root-change; disjoint reservation). Nine-core ⇒ d_B≤8 ⇒ q≤4;
c=0⇒q=0; positive debt w∈{1,2} (no Q≤2C_K claim). Exception w=1,R=0 (excludes
K/P universally). Successor w≤1,R≥2 (all q_k≤3: w_k∈{−2,−1,0,1}) ⇒ pair
1+w_k≤R_k jointly. Others: w≤0 via R≥0; w>0 via K (d_A≥3⇒H≥2) or P (distinct
DELETE+KEEP in-interval ⇒H≥2); overlap charged once. Pair+singletons partition
(s≥5⇒j*≠k; successor never recharged) ⇒ Σw≤ΣR ⇒ Q_B−2C_K≤2(A−C_K) ⇒ **Q_B≤2A**.
Full derivations + 24-point audit + 12-attack audit in 06_CERTIFICATES files.

## Evidence

SHA-pinned fixtures (c920… rejected); INC 33/18/8 + CTL 29/18/8; exact closure;
both engines; core 9; intervals exact (K5 exception + K7 successor; K3 Type P;
CTL successor H=1 excluded). Independent tuple-first verifier PASS. Strict
novelty retained (K3 AM-G G2+G4 fail; K5 local AM-G pass openly noted; five
REJECTs; no superseding theorem).

## Scope

Exactly the authorized S1 class — no complement, no K≥6, no universal.
