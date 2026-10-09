# Original Dynamic Optimality pipeline

## Fixed definitions

K is a finite totally ordered key set; T0 is any valid BST on K. X=(x_1,...,x_m), with every x_i in K. Choose an occurrence-index set I subset {1,...,m}; Y is the corresponding subsequence, preserving duplicates and order. A_i^tree always splays x_i. B_i^tree splays x_i on KEEP (i in I) and otherwise freezes. Both start at T0. Key sets remain K. Absent-key conventions in the broader liquidity repository are not used on this route.

Local edge-depth d has root value 0. A-side StepEv weight is a_i=ceil(d_A(x_i)/2). On KEEP define q_i=floor(d_B(x_i)/2), z_i=d_B(x_i) mod 2, b_i=q_i+z_i=ceil(d_B(x_i)/2); on DELETE set q_i=z_i=b_i=0. A DOUBLE counts one event for two primitive rotations; a terminal ZIG counts one event. These are not depth+1 search costs.

On a closed pair walk gamma define A=sum a_i, Q_B=sum q_i, Z_B=sum z_i, B=sum b_i. On a prefix H define S_A=sum a_i and E_B=sum b_i. Under P_all/U=0 all A events are sited, so the historical sited count S_A agrees with this event total; don't substitute a different eligibility policy. LT(X,T0)=sum_i(d_A(x_i)+1); LT(Y,T0) uses retained B accesses. Source g_C(T0) is a finite maximum residual over reachable simple paths, independent of history length. An explicit conservative bound is given in the reconstructed PIVOT-2 proof.

## Exact implication chain and status

| Node | Exact obligation / implication | Status |
|---|---|---|
| Pair Access | For every X,I,T0, A/B states represent the full/retained splay executions | PROVED mathematical encoding |
| COARSE-DOUBLE | For every finite K and closed pair walk reachable from some diagonal, Q_B<=2A | OPEN; finite reported bounds only |
| C.ZIG | For every finite closed present-key pair walk, Z_B<=A | PROVED mathematical; formal run assembly open |
| Event decomposition | B=Q_B+Z_B, therefore the two cycle inequalities imply B<=3A | PROVED arithmetic implication; conclusion CONDITIONAL |
| PIVOT-2 | If every reachable cycle has E_B−3S_A<=0, then every prefix has E_B<=3S_A+g(T0) | Complete conditional implication; actual bound OPEN |
| Cost comparison | That prefix bound implies LT(Y,T0)<=7LT(X,T0)+2g(T0), universally for Y subsequence X | Complete conditional implication; actual bound OPEN |
| Levy–Tarjan | Eventual monotonicity of Splay implies dynamic optimality (v3 Theorem 4.3) | External established reduction; application CONDITIONAL |
| Dynamic Optimality | Exists universal c>=1: LT(X,T0)<=c OPT(X,T0), every finite instance | OPEN |

The target model in the recovered L3 v3 paper is a rooted-hull/transition-tree execution: for each request choose a rooted hull containing its access path, reshape it with the same keys so the request becomes its root, and reattach hanging subtrees in symmetric order. Cost is the sum of transition-tree sizes. Splay's transition tree is its access path, so cost is d+1. OPT can use full future knowledge; Splay is online. The same specified T0 is used on both sides. The final conjecture has no startup term. Eventual monotonicity allows an arbitrary integer-valued overhead depending only on T0.

The paper's Appendix A compares this with rotational execution: search costs access-path nodes, each primitive rotation costs one, and rotations may occur anywhere before a request. These optimal costs are equivalent within factor 2. Pointer traversal/restructuring is accounted for by the chosen execution model; do not claim the literal primitive cost equals StepEv or LT cost. Different initial trees would need the paper's additional initial-tree argument, rather than silent substitution.

The required external result is Theorem 4.3, not merely Theorem 3.5 (which assumes approximate monotonicity without additive overhead). Source: local L3 PDF, printed/PDF pages 3–5, 8–10 and Appendix A; verified online [v3](https://arxiv.org/html/1907.06310v3). The historical bridge manifest pins different v1 bytes and an absent L2; those old registry gates are preserved and documented, not rewritten.

## Local sufficient route to COARSE-DOUBLE

One shared j(tau),rho(c) across all finite BSTs -> universal J-SELF and adjusted ROW-DIAMETER -> residual edge inequality -> telescope on cycles -> Q_B<=2A. This is a sufficient proof architecture, not a theorem that J4 is necessary.

The raw same-child target is |H_u−H_v|<=2. REBOOT-01 reduces equal-depth/equal-top-fold instances to the correctly oriented empty-sibling tree. Remaining arbitrary-T bases and other classes are OPEN. No source-verified list of 14 boundaries exists; the actual global pair partition is same child, opposite children, or one root, with each orientation and all depths included.
