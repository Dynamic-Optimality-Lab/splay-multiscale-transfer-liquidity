# DIRECT-CDK5N-MSINK — Mixed-Relay Shared-Sink Repayment

**Status: PROVED — CDK5NMSP-A (restricted class).**

## 1. Exact frozen H1–H6 domain and scope

Admissible reachable exactly closed A/B pair-walks. H1: exactly five
distinct genuine KEEP keys; complete marked B-ancestor core exactly nine at
every cyclic state. H2: complete exception set E={j:c_j=1,q_j=3,H_j=1} with
|E|=2 (w=1,R=0 each; no hidden indices). H3: maximal creditless successor
runs (c=1,H=1,q≤2); exactly one short t∈{0,1} + one long t≥2. H4/H5 joint
existential: ∃p∉E with c_p=1,H_p≥3 such that every other positive-debt
interval satisfies strict Type K (d_A≥3) or strict Type P (immediately
preceding DELETE(y), y≠x, a≥1 both, cyclic order). H6: Q_B≤2A (conclusion,
never assumed). Arbitrary n/tree size/DELETEs/order/prefixes/divergence/
seams. Complement, K≥6, universal Coarse-Double, DO remain OPEN.

## 2. Source semantics

T0 banked nine-node tree; KEEP(x) splays A+B; DELETE(x) splays A, B frozen;
keys never removed; a=⌈d_A/2⌉ pre-access; KEEP q=⌊d_B/2⌋; DELETE q=0;
A=Σa, Q_B=Σq; exact labeled closure.

## 3. Universal proof (L1–L7)

L1: cyclic KEEP intervals partition accesses (ΣH=A, Σq=Q, Σc=C_K,
Σw=Q−2C_K, ΣR=2(A−C_K)); H≥c by A-root-change (a=0 ⟺ current root; root
splays are no-ops); R≥0. L2: nine B-nodes ⇒ d_B≤8 ⇒ q≤4; c=0 ⇒ B rooted ⇒
q=0 ⇒ w=0; w>0 ⇒ w∈{1,2}. L3: exceptions (1,0); H=1 excludes strict K/P
(both imply H≥2). L4: joint sink R_p≥4, w_p≤2 over full q_p∈{0..4} table
(tight at q=4,H=3): 1+1+w_p≤R_p. L5: others by hypothesis satisfy strict-K
(d_A≥3 ⇒ a≥2 ⇒ H≥2) or strict-P (two a≥1 accesses ⇒ H≥2); with c=1,
R=2(H−1)≥2≥w. L6: {e1,e2,p} distinct; triple+singletons disjoint; sink spent
once; nothing recharged; accesses counted once. L7: Σw≤ΣR ⇒ Q−2C_K≤2(A−C_K)
⇒ Q≤2A. No aggregate premise, no circularity.

## 4. Strict predicates, sink, no-double-spend

Per §1 definitions; joint existential (all sinks enumerated); partition
disjointness as in L6. Type-K documentation erratum recorded separately
(nonfatal: joint uses H≥3 arithmetic, never K-membership).

## 5. Witness certificates

IN `788b459d…efd6d0a` (36 accesses, A=64, Q=36, C_K=16): five genuine keys,
core9 ×37, closure, engines agree, E=[4,12], t=(0,2), unique sink p=0
(H=13,q=3,w=1,R=24; 3≤24), other-positive strict-P, Σw=4≤96=ΣR.
OUT `b8b02be76c04033741d5f8534d286bbd14f571d3cd995961ac3d3cacb4bedab3`
(34 accesses, A=55, Q=36, C_K=16): same validity; t=(2,2) breaks H3;
MR-H6 fails at iv0 (dA=0, KEEP a=0); 34 distinct pre-closure states.

## 6. Recursive novelty certificate (relative to pre-promotion bank)

IN: 20/20 direct negatives (pointer-push AS incl.); recursive C* negative
(two independent decision procedures agree: 19 subproblems, 0 budget hits,
complete DAGs). OUT: 20/20 negatives; primitive ⇒ no partition. Hence
∅≠(S∩R_5^*)⊊R_5^*. Novelty is relative to the explicit closure C_*^old,
not to all conceivable proofs.

## 7. Dependencies

Original pair-access source semantics; banked cyclic interval identities;
A-root-change baseline; nine-core B-depth bound; frozen exception/relay
predicates; joint-sink L1–L7 proof above; independent strict novelty
certificates (recursive closure, both witnesses). No open conjectures.

## 8. Scope limits

Exactly this class. No nine-core complement closure, no K≥6, no universal
Coarse-Double, no Dynamic Optimality. Novelty (HI1–H5 + §6) and payment
(§3) are logically separate: the latter is universal, the former relative.
