# 26AN: double-positive shallow-surplus packet repayment (PROVED + OUTCOME A)

**Status: PROVED** — universal shallow-surplus lemma, two-splay former-root
repayment, universal signed four-block theorem, global cyclic packet theorem,
certified eight-key witness with two positive deficits in one packet, verified
exclusion from every prior domain. No J4, ROW-DIAMETER, J-SELF, DTQ, UG,
potentials, LP, or compactness used anywhere.

## 26AN-L1 — shallow intermediate credit (PROVED, pure source arithmetic)

Let an A-root block have total A cost a≥1 whose genuine B-changing KEEP occurs
at B-depth 1≤d_B≤3. Then q=⌊d_B/2⌋≤1, so δ=q−2a≤1−2=−1. Independent of any
later repayment. (Source defs: `wp6_coarse_double.py:28-53`.)

## 26AN-L2 — two-splay former-root displacement (PROVED by composition)

Let r be B's former root immediately before a nontrivial splay of x: after it,
d_B(r)≤2 (26AJ Lemma 2). Let two subsequent genuine B-changing splays occur,
neither accessing r: 26AL-L1 (`d'≤d+2`, frame joining/re-carry proof) applied
twice gives d_B(r)≤2+2+2=6. A later block KEEP of r hence has q_final≤3.
(26AL-L1 needs the splayed keys ≠ r — exactly the stated hypothesis.)

## 26AN-L3 — final negative credit (PROVED, arithmetic)

If the final former-root block has a_final≥2, then
δ_final=q_final−2a_final≤3−4=−1. No aggregate packet condition assumed.

## 26AN-P — double-positive signed four-block theorem (PROVED)

Four consecutive DISTINCT cyclic A-root blocks B_i..B_{i+3} with P1 (δ_i=1,
genuine splay of x, former root r), P2 (genuine splay of y≠x,r at 1≤d_B≤3,
a_{i+1}≥1), P3 (genuine splay of z≠y,r with source-computed δ_{i+2}=1),
P4 (block i+3 led by r, KEEP of r, interveners keyed ≠r), P5 (a_{i+3}≥2),
P6 (distinct positions), P7 (no geometry). Then δ_i=1 (P1);
δ_{i+1}≤−1 (L1 via P2); δ_{i+2}=1 (P3); δ_{i+3}≤−1 (L2+L3 via P4/P5); so
δ_i+δ_{i+1}+δ_{i+2}+δ_{i+3}≤1−1+1−1=0. Universal over all finite BST states
meeting the explicit source conditions. (Not via 26AM-G capacity.)

## Global cyclic packet theorem (PROVED)

Packet-admissible class: reachable closed walk + explicit anchor set I, each
P_i={i,...,i+3} satisfying 26AN-P, pairwise disjoint, every positive block in
exactly one packet, positives only at packet slots 0/2 (slots 1,3 are forced
nonpositive by L1/L2-L3 under the certified conditions), all unassigned blocks
nonpositive, checkable from source traces. Every certified packet sums ≤0;
unassigned blocks ≤0; hence Σδ_i≤0, i.e. Q_B≤2A. Covers zero-positive walks
(trivial), m<4 (P6 unsatisfiable ⟹ no anchors ⟹ all nonpositive), m=4,
arbitrary m, wraparound, multiple packets, cycle repetition. Admissibility is
NOT claimed for all closed walks.

Disjointness: distinct anchors' 4-sets sharing k give k slot≥1 in one packet,
which forces δ_k≤−1 — so a positive k anchors its own disjoint packet; with
req-2 coverage no positive is double-counted or uncovered.

## Witness (OUTCOME A coverage)

n=8, T0=`(1.(2.(3.(4.(5.(8(7(6..).).))))))`, prefix D2,D8,D4,D6,D3, cycle
K6,K8,K4,K1,K2,K5,K8,K2,K3,K1,D6,D4,D3: exact A/B closure (serial-compared),
table 13/13, A=20, Q_B=14, W=−26, engine comparison 18/18. Sole positives
blocks 1,3 (+1,+1) in packet {1,2,3,4}=(+1,−1,+1,−4)=−3; tail nonpositive;
K8,K4 genuine; r=1 (h=1 after K6); r'=8 before K4. Anchor I={1}.

## Strict novelty (both positives vs C_old)

K6: successor key 8≠1 (26AJ ✗); i+2 key 4≠1 (26AK/26AL-G/26AL-S ✗);
δ(i+2)=+1 (26AM-G G3 ✗, 26AM-S ✗). K4 (r'=8): successors 1,2,5, none 8
(26AJ/26AK/26AL-G/26AL-S ✗); packet {K4,K1,K2,K5} has key 5≠8 at i+3
(26AM-G G4 ✗). n=8, B-depths 7,6, A=20 (zero-A/n≤6/bounded-depth ✗).
Hence γ*∈C_26AN∖C_old: C_old ⊂neq C_old∪C_26AN. No inclusion C_old⊆C_26AN
claimed. 26AM Outcome B preserved (this witness is not a 26AM certificate).

## Scope (exact)

Covers packet-admissible closed walks only. NOT covered: multi-splay delays,
deficits beyond the signed pattern, indirect repayment, unrestricted
Coarse-Double. PIVOT-2, LT, Dynamic Optimality remain OPEN/CONDITIONAL.
