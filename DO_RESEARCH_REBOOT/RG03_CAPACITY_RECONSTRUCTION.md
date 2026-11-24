# RG-03 — Controlled structural capacity reconstruction

Date: 2026-11-09, Asia/Karachi.

## Scope freeze and prerequisite audit

RG-01 has PASS status. RG-02 rejected BOTH tested B-side laws and produced no accepted B-side certificate. Both reports were read; their exact physical edges, original SET labels, source periods, rotation IDs, complete cyclic windows and literal source counterexamples remain unchanged.

BEFORE the formal derivation:

1. Strictly smaller: decide only the prescribed signed linear span of E, P, F and S, in the required Class I / II / III order. Do not test other motifs, radii, history capacities or a different proof architecture.
2. Concrete mechanism: enumerate the changed edge/path/fork/SET occurrences of one literal rotation; then count these same occurrences in the already preserved RG-02 full physical B recurrences. A coefficient-independent full-access motif plateau is a possible exact elimination certificate, not an assumed result.
3. One principal objective: a complete certificate or a proof excluding the frozen classes. No solver, sample fit, source query, replay, experiment or additional open theorem is needed.
4. Upward advancement: establish the four requested A-side locality bounds and decide these three candidate classes. If excluded, place the exact failure data in the RG-04 input packet IN THIS REPORT. No RG-04/RG-05 work follows.

All coefficients are fixed signed rational numbers, independent of source and tree size; the exclusion proof may establish the stronger assertion for arbitrary fixed finite real coefficients. beta,gamma, when posited, are finite nonnegative absolute constants. The strong and complete-window weak laws are separate obligations.

Only this new RG03_CAPACITY_RECONSTRUCTION.md is written under DO_RESEARCH_REBOOT. Prior reports, programs, source words, owners and resource records are read-only. The repository artifact is not duplicated into Notion.


## 1. Frozen state features and exact difference convention

All trees below are COMPLETE labelled BSTs on the same finite physical key set X. KEEP splays A and then B; DELETE splays A only and removes no key. All real actor/operation/StepEv/bit IDs and all original intermediate states remain. The original fixed carrier S and SET convention are exactly RG-01's.

Use precisely the requested features:

\[
\begin{aligned}
f_E(A,B)&=|E(B)\setminus E(A)|,\\
f_P(A,B)&=|P_2(B)\setminus P_2(A)|,\\
f_F(A,B)&=|\mathcal F(B)\setminus\mathcal F(A)|,\\
f_S(A,B)&=|J_S(B)\setminus J_S(A)|=\Psi(A,B).
\end{aligned}
\tag{1.1}
\]

A path occurrence is (a,b,c;s_1,s_2) with ACTUAL edges (a,b,s_1),(b,c,s_2), each side LEFT or RIGHT. All four side pairs LL,LR,RL,RR are included. It is a downward directed two-edge path, not a fork or an ancestor shortcut. A fork occurrence is (v,l,r), with BOTH actual children nonempty in their original left/right order. No null slot, virtual bit or projected S adjacency is a physical motif.

For any one motif collection M_i and rotation T->T', define its ACTUAL deleted/created occurrence sets

\[
D_i=M_i(T)\setminus M_i(T'),\qquad
C_i=M_i(T')\setminus M_i(T).
\]

With B fixed during an A rotation, exact finite-set cancellation gives

\[
\Delta_A f_i=|D_i\cap M_i(B)|-|C_i\cap M_i(B)|.
\tag{1.2}
\]

This holds even when |D_i|!=|C_i|. It is a difference of two counts, not a sum of their upper bounds. SET labels require duplicate suppression as specified below.

## 2. Four A-side locality proofs

### 2.1 Complete context notation

Start with the literal LEFT rotation

\[
g(L,p(H,R))\longrightarrow p(g(L,H),R).
\tag{2.1}
\]

Let c be the external parent of g, if present, with slot sigma. Let d be the parent of c, if present, with slot tau at d. Let l=rt(L), h=rt(H), r=rt(R), when nonempty. If H is nonempty, h_L,h_R are its ACTUAL nonempty left/right children, when present.

A conditional row is omitted when one of its required vertices/edges does not exist. The whole frame preserves its key set and external slot. Its root metadata is not an edge or a motif. Subtree internal edges remain unchanged, but motifs crossing their attachment boundaries must be checked.

### 2.2 E: exact edge occurrences, L_E=3

For (2.1) the deleted edges are

    (c,g,sigma), (g,p,RIGHT), (p,h,LEFT),

and the created edges are

    (c,p,sigma), (p,g,LEFT), (g,h,RIGHT).

The c and h rows are conditional. The edges g->l LEFT and p->r RIGHT, all internal subtree edges and all other external edges are unchanged.

For the separate RIGHT rotation

\[
g(p(L,H),R)\longrightarrow p(L,g(H,R)),
\tag{2.2}
\]

the deleted edges are

    (c,g,sigma), (g,p,LEFT), (p,h,RIGHT),

and the created edges are

    (c,p,sigma), (p,g,RIGHT), (g,h,LEFT).

Here p->l LEFT and g->r RIGHT and every other unaffected edge are unchanged. These are the exact RG-01 sets, each of cardinality at most three. Equation (1.2) proves

\[
\boxed{|\Delta_A f_E|\le3,\qquad L_E=3.}
\tag{2.3}
\]

### 2.3 P: exact two-edge path occurrences, L_P=7

A two-edge path can change ONLY if it contains a deleted/created physical edge. Inspect the physical incoming/outgoing edges immediately adjacent to the three boundary-edge changes in Section 2.2.

For the LEFT rotation (2.1), the exact path sets are:

| Deleted path occurrence | Required condition | Created path occurrence | Required condition |
| --- | --- | --- | --- |
| (d,c,g;tau,sigma) | d exists | (d,c,p;tau,sigma) | d exists |
| (c,g,p;sigma,RIGHT) | c exists | (c,p,g;sigma,LEFT) | c exists |
| (c,g,l;sigma,LEFT) | c and L nonempty | (c,p,r;sigma,RIGHT) | c and R nonempty |
| (g,p,h;RIGHT,LEFT) | H nonempty | (p,g,l;LEFT,LEFT) | L nonempty |
| (g,p,r;RIGHT,RIGHT) | R nonempty | (p,g,h;LEFT,RIGHT) | H nonempty |
| (p,h,h_L;LEFT,LEFT) | H and h_L exist | (g,h,h_L;RIGHT,LEFT) | H and h_L exist |
| (p,h,h_R;LEFT,RIGHT) | H and h_R exist | (g,h,h_R;RIGHT,RIGHT) | H and h_R exist |

Each listed old occurrence contains an actually deleted edge and therefore cannot persist. Each listed new occurrence contains an actually created edge and was absent before. Paths containing TWO changed edges, such as c->g->p, are listed once.

There are no further paths to count. A path touching an affected edge must extend it by its unique incoming edge or one of its two outgoing edges. The table includes those extensions. For example g->l->a is UNCHANGED if l->a exists, since both of its edges are unchanged even though g's parent moves. Internal H paths also remain unchanged; the two boundary-crossing p->h->h_child paths do not.

For the RIGHT rotation (2.2), derived with its own sides:

| Deleted path occurrence | Required condition | Created path occurrence | Required condition |
| --- | --- | --- | --- |
| (d,c,g;tau,sigma) | d exists | (d,c,p;tau,sigma) | d exists |
| (c,g,p;sigma,LEFT) | c exists | (c,p,g;sigma,RIGHT) | c exists |
| (c,g,r;sigma,RIGHT) | c and R nonempty | (c,p,l;sigma,LEFT) | c and L nonempty |
| (g,p,l;LEFT,LEFT) | L nonempty | (p,g,h;RIGHT,LEFT) | H nonempty |
| (g,p,h;LEFT,RIGHT) | H nonempty | (p,g,r;RIGHT,RIGHT) | R nonempty |
| (p,h,h_L;RIGHT,LEFT) | H and h_L exist | (g,h,h_L;LEFT,LEFT) | H and h_L exist |
| (p,h,h_R;RIGHT,RIGHT) | H and h_R exist | (g,h,h_R;LEFT,RIGHT) | H and h_R exist |

For either orientation each of D_P,C_P has at most SEVEN occurrences. More exactly for the left rotation, writing epsilon_U=1[U nonempty] and deg(h)=0 when H is empty,

\[
\begin{aligned}
|D_P|&=\mathbf1[d\text{ exists}]
 +\mathbf1[c\text{ exists}](1+\epsilon_L)
 +\epsilon_H+\epsilon_R+\deg(h),\\
|C_P|&=\mathbf1[d\text{ exists}]
 +\mathbf1[c\text{ exists}](1+\epsilon_R)
 +\epsilon_L+\epsilon_H+\deg(h).
\end{aligned}
\tag{2.4}
\]

The right rotation interchanges the corresponding L/R roles as its table shows. Since deg(h)<=2, both bounds are seven. Equation (1.2) yields

\[
\boxed{|\Delta_A f_P|\le7,\qquad L_P=7.}
\tag{2.5}
\]

In particular this proof includes the external GRANDPARENT d. Calling paths "local" without that row would not be a complete derivation.

### 2.4 F: exact fork occurrences, L_F=3

Only parents whose OUTGOING children change can have a changed fork: c, g and p. A middle-subtree root h changes its parent but NOT its children, so its own fork and every fork internal to H remain unchanged.

For the LEFT rotation:

| Parent | Deleted fork, if present | Condition | Created fork, if present | Condition |
| --- | --- | --- | --- | --- |
| c | (c,g,o) if sigma=LEFT; (c,o,g) if sigma=RIGHT | c's other child o exists | (c,p,o) or (c,o,p), same order | same condition |
| g | (g,l,p) | L nonempty | (g,l,h) | L,H nonempty |
| p | (p,h,r) | H,R nonempty | (p,g,r) | R nonempty |

For the RIGHT rotation:

| Parent | Deleted fork, if present | Condition | Created fork, if present | Condition |
| --- | --- | --- | --- | --- |
| c | (c,g,o) or (c,o,g), according to sigma | other child o exists | (c,p,o) or (c,o,p), same order | same condition |
| g | (g,p,r) | R nonempty | (g,h,r) | H,R nonempty |
| p | (p,l,h) | L,H nonempty | (p,l,g) | L nonempty |

All listed old/new tuples differ. Every other parent keeps the same children, including d and h. Hence these are ACTUAL set differences, with at most three deletions and three creations, not a bound on possible sites alone. From (1.2),

\[
\boxed{|\Delta_A f_F|\le3,\qquad L_F=3.}
\tag{2.6}
\]

### 2.5 S: genuine SET occurrences, L_S=1

Put J(U)=S intersect keys(U), and eta(v)={v} intersect S. The latter is empty at a private A vertex.

For the left rotation the only candidate old label lost and new label created are

\[
U=\eta(p)\cup J(H)\cup J(R),\qquad
V=J(L)\cup\eta(g)\cup J(H).
\]

For the right rotation they are

\[
U=J(L)\cup\eta(p)\cup J(H),\qquad
V=J(H)\cup\eta(g)\cup J(R).
\tag{2.7}
\]

The WHOLE frame label persists at its new root. Labels inside L,H,R and at every other vertex persist. Let K be the SET of these common nonempty labels, including the whole frame. Omitting an empty U or V,

    J_S(A)=K union {U},
    J_S(A')=K union {V}.

Thus the exact deleted SET labels are ({U} minus {V}) minus K, and the exact created labels are ({V} minus {U}) minus K. A candidate represented elsewhere is not lost; a duplicate newly represented candidate is not created. Each actual difference set has cardinality at most one. Applying (1.2) with M_S=J_S proves

\[
\boxed{|\Delta_A f_S|\le1,\qquad L_S=1.}
\tag{2.8}
\]

This permits arbitrary physical private A ancestors and SET duplicates. It is not a multiset or a fork/edge count.

### 2.6 Signed combination and access bound

For the EXACT frozen family

\[
\Phi_\lambda=\lambda_E f_E+\lambda_P f_P+\lambda_F f_F+\lambda_S f_S,
\]

the universal one-real-rotation bound is

\[
\boxed{|\Delta_A\Phi_\lambda|
 \le L_\lambda
 :=3|\lambda_E|+7|\lambda_P|+3|\lambda_F|+|\lambda_S|.}
\tag{2.9}
\]

A full original A access with r_t actual rotations has bound L_lambda*r_t by summing its actual primitive differences. A double uses the two successive current tables; a terminal zig uses one real table, and its virtual bit creates no occurrence of ANY feature. At a global-root rotation c,d rows are absent; at empty subtrees their conditional rows are omitted. Empty and one-key physical universes admit no real rotation. No constant depends on tree size, S size, source length or private population.

All four locality obligations are therefore PROVED, independently of whether a candidate passes the B-side test.


## 3. Exact B-side accounting from the literal primitives

### 3.1 Cardinality terms must be retained for paths and forks

Keep ONE complete post-A tree A_t fixed during the B phase. For i=E,P,F, put chi_i(Z)=|Z intersect M_i(A_t)|. Applying the exact occurrence tables to a B rotation gives

\[
\delta_B f_i=|C_i\setminus M_i(A_t)|-|D_i\setminus M_i(A_t)|
            =(|C_i|-|D_i|)+\chi_i(D_i)-\chi_i(C_i).
\tag{3.1}
\]

The indicators come from the SAME actual complete A_t. They cannot be assigned independently.

Let epsilon_L,epsilon_H,epsilon_R indicate nonempty physical subtrees, and epsilon_c indicate an external parent. For the LEFT primitive (2.1),

\[
\begin{array}{c|c}
i&|C_i|-|D_i|\\ \hline
E&0\\
P&(1-\epsilon_c)(\epsilon_L-\epsilon_R)\\
F&(\epsilon_R-\epsilon_L)(1-\epsilon_H).
\end{array}
\tag{3.2}
\]

For the RIGHT primitive (2.2), the last two entries are respectively

\[
(1-\epsilon_c)(\epsilon_R-\epsilon_L),\qquad
(\epsilon_L-\epsilon_R)(1-\epsilon_H).
\tag{3.3}
\]

The P formulas follow directly by subtracting the path-table cardinalities. For F, the external c has a fork both before and after or neither, and the pivot/promoted-node conditions in Section 2.4 give the displayed difference.

Globally, for any nonempty physical tree T,

\[
|P_2(T)|=|X|-1-\deg_T(\mathrm{root}).
\tag{3.4}
\]

Every nonroot vertex contributes an incoming edge; exactly root's children fail to have TWO ancestors along a downward two-edge path. This is also a direct count by the last vertex of each path. Hence a B access satisfies

\[
\Delta_B f_P
 =\deg_{B_{\rm before}}(\mathrm{root})
  -\deg_{B_{\rm after}}(\mathrm{root})
  +|P_2(B_{\rm before})\cap P_2(A_t)|
  -|P_2(B_{\rm after})\cap P_2(A_t)|.
\tag{3.5}
\]

A root-degree change cannot be silently dropped. Similarly,

\[
\Delta_B f_F=
|\mathcal F(B_{\rm after})|-|\mathcal F(B_{\rm before})|
+\text{shared forks before}-\text{shared forks after}.
\tag{3.6}
\]

Only E has fixed total cardinality |X|-1. All formulas concern physical motifs, irrespective of S.

### 3.2 RR, LL, LR, RL and zig substitutions

Write L[c^sigma;g,p;U,V,W] for g(U,p(V,W))->p(g(U,V),W), and R[c^sigma;g,p;U,V,W] for g(p(U,V),W)->p(U,g(V,W)). The c entry is omitted when absent.

These are the literal actual primitive steps of each original double:

| Double input and complete result | Actual bit 0 | Actual bit 1 |
| --- | --- | --- |
| RR: g(L,p(H,x(C,R))) -> x(p(g(L,H),C),R) | L[c;g,p;L,H,x(C,R)] | L[c;p,x;g(L,H),C,R] |
| LL: g(p(x(L,C),H),R) -> x(L,p(C,g(H,R))) | R[c;g,p;x(L,C),H,R] | R[c;p,x;L,C,g(H,R)] |
| LR: g(p(L,x(H,C)),R) -> x(p(L,H),g(C,R)) | L[g^LEFT;p,x;L,H,C] | R[c;g,x;p(L,H),C,R] |
| RL: g(L,p(x(C,H),R)) -> x(g(L,C),p(H,R)) | R[g^RIGHT;p,x;C,H,R] | L[c;g,x;L,C,p(H,R)] |

The first LR/RL step has the ACTUAL external parent g and its indicated slot, even if the whole frame is at the root. A terminal left or right zig is the corresponding one primitive at the global root, c absent.

Equations (3.1)–(3.3), with the actual full subtrees in EACH row, give the exact B change of all physical features. Internal transported paths/forks cancel only when their actual tuples are unchanged; a motif crossing an attachment is handled by the tables.

For S, RG-01's actual SET test says a real B rotation creates one proper label K and

    delta_B f_S = -1[K in J_S(A_t)].

In RR the two created labels are J(L) union {g} union J(H), then that label union {p} union J(C). LL is the corresponding right-side pair. In LR they are J(L) union {p} union J(H) and J(C) union {g} union J(R); RL reverses the sides. A terminal zig creates the actual full S side of x and decreases.

Thus on a COMPLETE B access

\[
\boxed{\Delta_{B,t}f_S=-d_t.}
\tag{3.7}
\]

A fully neutral double contributes one to b_(0,t) only when BOTH SET tests are zero. A B1 double's single neutral bit is not half a neutral double. u_t additionally retains its full historical window test and cannot be decided by one primitive.

### 3.3 Exact coefficient condition

Let c_t mean b_(0,t) for the strong law or u_t for the weak law. Summing (3.1) along the full access and using (3.7), the REQUIRED condition is exactly

\[
c_t+\lambda_E\Delta_E+\lambda_P\Delta_P+\lambda_F\Delta_F
 \le(\beta+\lambda_S)d_t+\gamma k_t,
\tag{3.8}
\]

where Delta_i is the ACTUAL complete B-phase change of f_i. It must hold for every original admissible W,t. In Classes I/II the unused coefficients are zero.

Adding the original SET feature only shifts the decrease coefficient by lambda_S. It supplies no separate neutral count when d_t is bounded. This is an algebraic fact about the original SET test, not an assumption that beta+lambda_S has a prescribed sign.

A root-repeat KEEP or DELETE has c_t=d_t=k_t=Delta_i=0. These are not zero-denominator counterexamples.

## 4. Preserved source transitions and diagnosis of RG-02

### 4.1 Full physical W_(p,q) / H_(p,q) recurrence

Use the EXISTING RG-02 families, with p here the family parameter, unrelated to a primitive's node named p:

\[
N=2^{p+1}(q+1)+1,\quad x_j=N+1-2^j,\quad
n_j=(N-1)/2^{j+1}.
\tag{4.1}
\]

Both start at the permitted complete diagonal A=B=V+(1,N), with empty prefix and X=S=M=[N].

W has DELETE 2,...,N; then every adjacent descent N,...,x_p, KEEP exactly at x_0,...,x_p and DELETE elsewhere; then KEEP 1,...,N; then KEEP N-1,...,1. H extends the adjacent descent all the way to 1, with the same KEEP targets. Their full lengths remain 3N+2^p-2 and 4N-2. Both complete physical trees return to the initial right vine by the two original closing scans. H has its original A=4(N-1), including all preparation and restoration.

At critical t_j=N-1+2^j, the post-A tree is the COMPLETE physical

\[
A_{x_j}=x_j(V^-(1,x_j-1),V^+(x_j+1,N)).
\tag{4.2}
\]

Its exact edge tests are LEFT a->a-1 for 2<=a<=x_j and RIGHT a->a+1 for x_j<=a<N. Its directed two-edge paths are precisely the consecutive LL triples below its root and consecutive RR triples above it. If 1<x_j<N its only physical fork is (x_j,x_j-1,x_j+1).

Let P_h(c) be the FULL perfect BST of height h, with P_1(c)=c and

    P_(h+1)(c)=c(P_h(c-2^(h-1)),P_h(c+2^(h-1))).

The original physical state after critical x_j is

\[
B_j=x_j(C^{(j)}_0,H_j),
\]

\[
\begin{aligned}
r_i&=2+2^{j+1}i,\qquad i=0,\ldots,n_j-1,\\
C^{(j)}_i&=r_i(T_i,C^{(j)}_{i+1}),\\
T_0&=1,\quad T_i=P_{j+1}(r_i-2^j)\quad(i\ge1),\\
C^{(j)}_{n_j}&=R_j.
\end{aligned}
\tag{4.3}
\]

R_0=H_0=empty; for j>=1,

\[
R_j=P_j(N+1-3\cdot2^{j-1}),\qquad
H_j=P_j(N+1-2^{j-1}).
\tag{4.4}
\]

Every block is a physical subtree, not one vertex. In particular the exact failed transition F1/F2/F3 is

    (A_(x_j), B_(j-1)) -> (A_(x_j), B_j).

There are n_j-1 neutral RR doubles and one final LR with two decreasing bits. The initial maximum access has n_0-1 neutral RR doubles plus one decreasing RR.

For j>=1 and neutral double k=1,...,n_j-1, its actual whole frame is

\[
F_{j,k}=[N+2-2^{j+1}(k+1),\,N-2^{j-1}].
\tag{4.5}
\]

Every lower endpoint is >=3; every upper endpoint is <N. In H, every actual A snapshot is a two-vine, so EVERY such frame is A-absent throughout the ENTIRE period. Therefore it is absent on its COMPLETE original cyclic Pi window, regardless of where its preceding kappa lies.

For W the preserved RG-02 full reset argument is also retained: upper endpoint v>=x_p starts as an ancestor of N; accesses <=v preserve that ancestry through KEEP v; later accesses preserve v's ancestry of 1. Thus its reset also never exposes (4.5). Preparation, adjacent descents and reverse restoration are two-vine states. Hence for BOTH words,

\[
b_{0,t_j}=u_{t_j}=n_j-1,\qquad d_{t_j}=2,\quad k_{t_j}=1
\quad(j\ge1).
\tag{4.6}
\]

At j=0, u=0 since the whole frames contain max S=N. No source access is independently closed or substituted for the period.

### 4.2 Original physical event mechanism

In RR double k of row j>=1, the actual grandparent and parent keys are

\[
g=x_j-2^{j+1}k,\qquad y=g+2^j.
\]

Its complete left blocks are P_j(g-2^(j-1)) and P_j(g+2^(j-1)). The first real rotation promotes y above g and creates g's new subtree by joining those physical blocks to g; the second promotes actual target x_j above y. The old WHOLE frame is transported first to y and then to x_j. It is not SET-removed by that same double; the recorded later promotion ends its original run.

In the F1 subfamily p=1, N=4q+5, x=N-1, original t=N+1, the real IDs and changed-edge agreements are the preserved exact ones:

* B(t,k,0), k=1,...,q: g=x-4k, y=g+2, external parent c=g-2 in its RIGHT slot. It deletes the actual A-shared (y,g+1,LEFT), replacing it by (g,g+1,RIGHT). The other pivot/external replacements are nonshared in A_x. This creates one additional physical edge disagreement.
* B(t,1,1) also deletes the actual shared (x,x-1,LEFT); later RR bit-1 replacements are nonshared at both ends.
* The final LR has no shared-edge change in bit 0 and adds the actual shared (x,N,RIGHT) in bit 1.
* All internal edges and motif occurrences wholly inside transported hangers remain unchanged. Motifs crossing their attachment boundaries change exactly as Section 2 lists.

The actual local frame in this F1 case is, with y=g+2 and the external c=g-2 in its RIGHT slot,

\[
g((g-1),y((g+1),x(C,\varnothing)))
 \longrightarrow y(g((g-1),(g+1)),x(C,\varnothing))
 \longrightarrow x(y(g((g-1),(g+1)),C),\varnothing).
\]

The parent of the whole old frame changes c->g to c->y to c->x, while the old frame's S label is transported to each successive root. Here g-1,g+1 are actual physical leaf keys, and C is the full carried subtree.

Thus the FULL old vector (b_0,u,Delta f_E,d,k)=(q,q,q,2,1) remains intact. Its whole labels and run IDs remain

\[
F_k=[x-4k-1,x],\qquad \Gamma_k=B(N,2k+1,1),
\]

\[
\sigma_k=B(N+1,k+1,1)\ (k<q),\qquad
\sigma_q=B(N+1,q+1,0),
\tag{4.7}
\]

with kappa the previous cyclic sigma. Complete-window A absence is the original full-period fact, not a local edge inference.

At F2 and F3, perfect side blocks grow through these SAME original RR operations. Forks and paths can be replaced in equal numbers although their actual tuples change. Zero net feature change does NOT mean no physical event or no changed occurrence.

The diagnosed failure is physical edge/motif replacement and redistribution within one original B access, with rigid subtree-label transport. The historical run records and complete cyclic A-absence certify weak membership; they do not supply a different local cause of edge/motif loss. No long-range genealogy assumption is used to build these transitions. No event is described as "free regeneration": every merge/promotion has its original physical B ID, and every source retains its original A preparation and closing operations.

### 4.3 Warmed F4/F5: exact physical transitions retained

The already reachable warmed pair is A=V-(1,N), B=B_p. The old prefix is unchanged: DELETE preparation; the critical N,...,x_p packet; then DELETE x_p+1,...,N. The actual repeated period descends EVERY integer N,...,x_p with KEEP exactly at x_j and DELETE elsewhere, then DELETE x_p+1,...,N.

Its original carrier is S=M={x_p,...,x_0}, the actual root-to-support spine of B_p. The complete low subtree C^(p)_0 and all gaps R_i remain physical S-free hangers. The period returns BOTH entire trees, with original A cost 2(2^p-1). No old full-support frame is assigned membership under this different source.

For a completely explicit F4/F5 transition take p=4r, v_i=x_(p-i), i=0,...,p. Let

    L_0=C^(p)_0,
    L_i=R_(p-i), i=1,...,p, so L_p=empty.

Then the starting B_p is the ACTUAL physical spine

    v_0(L_0,v_1(L_1,...,v_p(L_p,empty)...)).

Set s=p/2 and Z_s=L_p. For i=s-1,...,0 put

    Z_i=v_(2i+1)(v_(2i)(L_(2i),L_(2i+1)),Z_(i+1)).

The COMPLETE first-access result is B_max=v_p(Z_0,empty), by its s original RR doubles. Hence F4 is

    (A_N,B_p) -> (A_N,B_max).

For F5 put a_i=v_(2i+1), M_i=v_(2i)(L_(2i),L_(2i+1)), i=0,...,s-1. Initialize C=M_(s-1); for i=r-2,...,0 put

    C=a_(2i+2)(a_(2i+1)(M_(2i+1),M_(2i+2)),C).

The complete result at target a_(s-1)=N-1 is

    B_next=a_(s-1)(a_0(M_0,C),N).

Thus F5 is

    (A_(N-1),B_max) -> (A_(N-1),B_next).

Every L_i,M_i,C here is a COMPLETE physical subtree. The formula retains every low/gap key and is a literal RR/final-LR fold, not a contracted marked execution.

The old F4/F5 vectors remain

    F4: (b_0,u,Delta f_E,d,k)=(2r-1,0,1,2,1);
    F5: (b_0,u,Delta f_E,d,k)=(r-1,r-1,-1,2,1).

In F5 the actual source positions are t_0=1,t_1=2, retaining any original absolute offset. For k=1,...,r-1 its whole frame is the S interval v_(p-2-4k),...,v_(p-1), with Gamma=B(t_0,2k+1,1), sigma=B(t_1,k+1,1) except the last sigma=B(t_1,r,0), and preceding kappa the previous cyclic sigma. These are exactly the RG-02 records. A's actual physical two-vine states have only S-prefix/suffix labels, so full-window absence is preserved.

The changing physical agreements are the original ones: the gap vertex N-2 moves from LEFT of N-1 to RIGHT of N-3 in F4; F5 creates the shared physical (N-1,N,RIGHT). Larger gaps are nonadjacent physical attachments. Unvisited low/gap subtree internals remain unchanged. None of these keys is physically deleted.


## 5. Exact four-feature changes on the preserved source families

### 5.1 Directed paths: total size versus shared occurrences

A physical two-vine A_x has ONLY consecutive LL paths (a,a-1,a-2) below x and consecutive RR paths (a,a+1,a+2) above x.

Every adjacent edge INSIDE a perfect P_h block ends at a bottom leaf. It cannot be followed by another adjacent edge. In (4.3), the chain edges jump 2^(j+1)>=2 physical keys; the T_i boundary jumps 2^j, except j=0 where it attaches to a leaf. The root/right-remainder boundaries jump 2^(j-1), except j=1 where again the attached block is a leaf. The root-to-2 attachment is nonadjacent. The special edge 2->1 also ends at a leaf.

Consequently NO B_j has a downward path with two consecutive physical-key edges in either monotone orientation. In particular

\[
P_2(B_j)\cap P_2(A_x)=\varnothing
\quad\text{for every critical post-A two-vine }A_x.
\tag{5.1}
\]

This uses all physical nodes in the perfect blocks; it does not replace each block by its root.

The initial B right vine has no shared path with A_N's LL paths. The root degree is one before/after the initial maximum, changes one->two at row 1, and is two->two at every later row. Equation (3.5) therefore gives

\[
\Delta_{B,t_j}f_P=
\begin{cases}
0,&j=0,\\
-1,&j=1,\\
0,&j\ge2.
\end{cases}
\tag{5.2}
\]

The -1 is a REAL path-cardinality change at the root. It is not shared-path cancellation.

### 5.2 Forks: exact physical branch count and actual matching test

A perfect P_h has 2^(h-1)-1 physical forks. In B_0 the first n_0-1 chain vertices have two children and the last has one; all attached odd nodes are leaves. Hence

    |F(B_0)|=n_0-1.

For j>=1, the physical root has two children, all n_j chain vertices have two children, the n_j-1 blocks P_(j+1) each have 2^j-1 forks, and R_j,H_j each have 2^(j-1)-1 forks. Therefore

\[
|\mathcal F(B_j)|
 =1+n_j+(n_j-1)(2^j-1)+2(2^{j-1}-1)
 =2^j n_j=n_0.
\tag{5.3}
\]

The original right vine has no fork.

No fork is shared with the fixed A_(x_j). For j=0, A_N has no fork at all. For j>=1 its only fork is (x_j,x_j-1,x_j+1). Before the access, B's target x_j has no right child at j=1; at j>=2 its left child is x_j-2^(j-1), not x_j-1. Afterward its left child is 2, not x_j-1. Forks with another parent cannot match A's unique fork. Thus shared-fork counts are ZERO before AND after.

It follows that

\[
\Delta_{B,t_j}f_F=
\begin{cases}
n_0-1,&j=0,\\
+1,&j=1,\\
0,&j\ge2.
\end{cases}
\tag{5.4}
\]

Many fork tuples change during the rotations. Equality of the unmatched counts at later rows comes from equal total counts and no common tuple, not persistence of every fork.

### 5.3 Complete full-access vector

Combining (5.2), (5.4), the preserved exact RG-02 edge counts, and Delta f_S=-d gives:

| Row in original W/H | b_0 | u | d | k | Delta f_E | Delta f_P | Delta f_F | Delta f_S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | n_0-1 | 0 | 2 | 1 | -n_0 | 0 | n_0-1 | -2 |
| 1 | n_1-1 | n_1-1 | 2 | 1 | n_1-1 | -1 | +1 | -2 |
| 2 | n_2-1 | n_2-1 | 2 | 1 | +1 | 0 | 0 | -2 |
| j>=3 | n_j-1 | n_j-1 | 2 | 1 | 0 | 0 | 0 | -2 |

For clarity the inherited edge counts are actual shared-edge before/after values with the SAME A_(x_j):

    row 0: 0 -> n_0;
    row 1: 2n_1 -> n_1+1;
    row 2: 2n_2+2 -> 2n_2+1;
    row j>=3: 1+2^(j-1)n_j -> the same count.

These are full-access differences, with every transient attachment cancellation retained. The A-state constraints are the explicit complete BST (4.2), not independent motif/edge indicators.

### 5.4 Enrichment of warmed F4/F5, with full physical hangers

For p=4r the two complete transitions in Section 4.3 have:

| Preserved warmed packet | b_0 | u | d | k | Delta f_E | Delta f_P | Delta f_F | Delta f_S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| F4, first KEEP N | 2r-1 | 0 | 2 | 1 | +1 | +1 | -1 | -2 |
| F5, second KEEP N-1 | r-1 | r-1 | 2 | 1 | -1 | -1 | +1 | -2 |

Here are the additional motif checks, beyond the preserved edge counts.

At F4 the B root changes from degree two to degree one; at F5 it changes back to degree two. No physical two-edge path is shared with the respective A_N or A_(N-1), before or after. The internal low/gap trees are the same perfect/block structures of (4.3), with no two consecutive monotone physical edges. The only newly relevant adjacent high-key edges involve N-1,N and the gap N-2; they do not form a shared TWO-edge LL path, and A_(N-1) has only one edge on its right. Hence the path changes are +1 and -1 by (3.5).

All physical L_i in Section 4.3 are nonempty except L_p. In F4, RR first rotations have nonempty middle subtrees; the first target promotion has empty old target-left subtree and loses exactly one fork by (3.2). Subsequent target-left subtrees are nonempty and cause no fork-cardinality change. Thus total fork change is -1. In F5, the RR steps and first LR bit have nonempty middle subtrees; the last right rotation has empty target-right gap and adds exactly one fork by (3.3). No fork is shared with A_N (which has none), or with A_(N-1)'s fork (N-1,N-2,N), since B's target-left child is a lower support node. Therefore the unmatched-fork changes are exactly -1,+1.

In particular F5 itself gives, for EVERY fixed four-feature coefficient tuple,

\[
u_t+\Delta_B\Phi_\lambda
 =r-1-\lambda_E-\lambda_P+\lambda_F-2\lambda_S
 \longrightarrow\infty,
\tag{5.5}
\]

with d=2,k=1. This is an independent complete-window exclusion of the entire class. The required original warmed S=M and all physical gap populations are unchanged.

For the preserved p=1 two-zig warmed control, the two full vectors are

    first left zig:  (Delta E,Delta P,Delta F,Delta S)=(-1,+1,-1,-1);
    next right zig:  (Delta E,Delta P,Delta F,Delta S)=(-1,-1,+1,-1).

Both have b_0=u=0,d=k=1. Their B root degrees are two->one and one->two; no path/fork matches are introduced. The actual nonadjacent low-tree attachment remains present. Necessary terminal-zig constraints for any proposed certificate are therefore

\[
-\lambda_E+\lambda_P-\lambda_F-\lambda_S\le\beta+\gamma,
\qquad
-\lambda_E-\lambda_P+\lambda_F-\lambda_S\le\beta+\gamma.
\tag{5.6}
\]

These finite constraints do not by themselves prove feasibility or infeasibility.

### 5.5 Saved actual 97-key source remains distinct

Preserve the complete original 293-operation word: DELETE 2,...,97; KEEP 97,96,95,94; KEEP 1,...,97; KEEP 96,...,1, from its common right-vine diagonal. It is NOT the dyadic W_(3,5). The exact full B states and whole-frame histories remain RG-02 Section 6.

For explicit identification, after 97 its left chain has even roots 2,...,96 with odd left leaves. After 96 its left chain roots 4i+2, i=0,...,23, have T_0=1 and T_i=P_2(4i), with right remainder 95. After 95 its left chain roots 8i+6, i=0,...,11, have L_0=2(1,4(3,5)) and L_i=P_3(8i+2), no right remainder. After 94 its left chain roots 16i+6, i=0,...,5, have R_0=L_0 and R_i=P_4(16i-2), with right remainder P_3(90). Their global right sides are respectively empty, 97, 96->97, and 95->96->97. All these blocks are complete physical trees.

The exact enriched access table is:

| Original t / target | b_0 | u | d | k | Delta E | Delta P | Delta F | Delta S |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 97 / 97 | 47 | 0 | 2 | 1 | -48 | 0 | +47 | -2 |
| 98 / 96 | 23 | 23 | 2 | 1 | +23 | -1 | +1 | -2 |
| 99 / 95 | 11 | 11 | 3 | 1 | -1 | -1 | -1 | -3 |
| 100 / 94 | 5 | 5 | 2 | 1 | -1 | -1 | 0 | -2 |

Physical fork counts after these KEEPs are 47,48,47,47, and no fork matches the post-A root's fork. For P, shared before/after counts are 0/0,0/0,0/1,1/2. Only the consecutive RIGHT suffix chains supply these matched paths; the left perfect/irregular blocks have no consecutive LL pair. Root-degree changes supply an additional -1 only at t=98. These observations prove the new columns by (3.5)–(3.6).

At t=99 the last RR is decreasing in BOTH bits and the terminal right zig also decreases, retaining d=3 and b_0=11. Complete-window membership of all 39 later critical neutral doubles is unchanged: the upper endpoints 96,95,94 remain A-absent through the actual full reset by the preserved extremal-ancestor argument.

For example t=99 imposes the finite necessary constraint

    11-lambda_E-lambda_P-lambda_F-3lambda_S <= 3beta+gamma

for BOTH versions. This is a finite control only, not a refutation of all finite constants. No original 97-key source, event ID, frozen selector or evidence status is rewritten.

## 6. Candidate classes tested in the required order

### 6.1 Class I: E and P only — both versions FAIL

Set lambda_F=lambda_S=0. Initial maximum accesses in H_(1,q) have n_0=2(q+1) unbounded. By Section 5.3, their strong left side is

    (1-lambda_E)n_0-1,

so a universal strong law NECESSARILY has lambda_E>=1. For the weak law u=0 there, so the necessary condition is lambda_E>=0.

At the next critical access, n_1-1=q and the strong AND weak left sides are

    (1+lambda_E)q-lambda_P.

Since d=2,k=1, either universal law NECESSARILY has lambda_E<=-1.

The strong requirements lambda_E>=1 and <=-1 contradict. The separate weak requirements lambda_E>=0 and <=-1 also contradict. No choice of lambda_P, beta or gamma repairs an unbounded linear coefficient. This covers EVERY signed rational Class-I choice, indeed every fixed finite real choice.

### 6.2 Class II: E, P and F — both versions FAIL

Set lambda_S=0. The same initial maximum accesses require

\[
1-\lambda_E+\lambda_F\le0
\quad\text{(strong)},\qquad
-\lambda_E+\lambda_F\le0
\quad\text{(weak)}.
\tag{6.1}
\]

The next wave still requires lambda_E<=-1; lambda_P and lambda_F contribute only constants to that row. These necessary halfspaces are NOT asserted sufficient.

Now use the EXISTING p=2 row-2 accesses: N=8(q+1)+1, target N-3, original t=N+3. Their exact vector from Section 5.3 is

\[
(b_0,u,d,k)=(q,q,2,1),\qquad
(\Delta E,\Delta P,\Delta F)=(1,0,0).
\tag{6.2}
\]

Thus either law would require

\[
q+\lambda_E\le2\beta+\gamma
\quad\text{for every positive integer }q.
\]

This is impossible for EVERY fixed signed coefficient triple and finite constants. It also covers all triples satisfying (6.1); no failed numerical guess or sampling claim is involved.

### 6.3 Class III: all four features — both versions FAIL

Here is a coefficient-independent physical-motif plateau in the preserved RG-02 F3 configuration.

Fix p=3, let q>=1 vary, and take the COMPLETE original H_(3,q). Then

\[
N=16(q+1)+1,\quad t=N+7,\quad x_3=N-7,\quad n_3=q+1.
\]

At that one original KEEP,

\[
\boxed{b_{0,t}=u_t=q,\quad d_t=2,\quad k_t=1,\quad
(\Delta E,\Delta P,\Delta F,\Delta S)=(0,0,0,-2).}
\tag{6.3}
\]

The source is reachable from its allowed complete diagonal with empty prefix, all physical keys remain, and both closing sweeps count. The neutrality/interior/full-window facts were proved in Section 4.1, and the four actual feature changes in Section 5. No indicator pattern was guessed.

For ANY fixed signed coefficients, the strong and separately verified weak left sides BOTH equal

\[
q-2\lambda_S.
\]

Either proposed universal inequality would force

\[
\boxed{q-2\lambda_S\le2\beta+\gamma\quad\text{for EVERY }q\ge1.}
\tag{6.4}
\]

Choose an integer q>max(0,2beta+gamma+2lambda_S). This gives a valid complete original source and an actual offending access. Equivalently the weak ratio is

\[
\frac{u_t+\Delta_B\Phi_\lambda}{d_t+k_t}
 =\frac{q-2\lambda_S}{3}\longrightarrow\infty.
\tag{6.5}
\]

The denominator is exactly three. This proves exclusion of ALL coefficient choices in Class III, including signed rationals and arbitrary fixed finite reals. It does not merely reject one displayed potential or one selection of beta,gamma.

The weak exclusion is independent of the strong exclusion: u_t=q was established from the complete cyclic A-absence history. No inference "strong failed, therefore weak failed" is used.

### 6.4 LL/RL and both zig orientations

Order reflection x->N+1-x, applied to a COMPLETE source and both trees, swaps LEFT/RIGHT, RR/LL and LR/RL. The path side pair is reflected in both motif sets; fork children exchange their ordered left/right roles consistently; SET labels and the two carrier extremes are reflected as actual key sets.

Thus every f_i and its full-access delta is invariant under that simultaneous bijection. Costs, neutral/decreasing counts, exact closure and complete-window membership are preserved. The primitive steps in Section 3.2 give the reflected LL/RL identities literally, and the necessary coefficient constraints above hold on those valid reflected sources too.

This symmetry does not edit or relabel an archived source or mix its physical credits with another period. It exhibits the opposite-orientation instances required by an all-source law. The separate terminal-zig constraints were computed in (5.6); no virtual bit is used.

No class has a feasible universal certificate. RG-05 therefore receives none.


## 7. RG-04 transfer packet and exact result scope

### 7.1 Principal all-coefficient failure configuration

This is a durable INPUT/HANDOFF packet for RG-04, not execution of that gate.

Use the unchanged COMPLETE H_(3,q), q>=1:

    X=S=M=[N], N=16(q+1)+1;
    common diagonal V+(1,N), reaching prefix empty;
    DELETE 2,...,N;
    descend EVERY key N,...,1, KEEP only at N,N-1,N-3,N-7;
    KEEP 1,...,N;
    KEEP N-1,...,1.

The period length is 4N-2 and its actual A cost is 4(N-1). At ORIGINAL t=N+7 the complete post-A tree is

    A=(N-7)(V-(1,N-8),V+(N-6,N)).

The old/new B trees are EXACTLY B_2 and B_3 of (4.3)–(4.4), with all physical blocks included. The original path has 2(q+1) actual edges, q RR doubles followed by one LR.

The full physical feature values before/after, at the SAME fixed A, are:

| Feature | Before | After | Delta |
| --- | ---: | ---: | ---: |
| f_E | 12q+11 | 12q+11 | 0 |
| f_P | 16q+14 | 16q+14 | 0 |
| f_F | 8q+8 | 8q+8 | 0 |
| f_S | original value s | s-2 | -2 |

The common physical edge count is 4q+5 on each side; shared two-edge paths and shared forks are zero. There are q COMPLETE-window interior neutral demands and two actual Psi-decreasing rotations.

Every last-generation neutral double k=1,...,q has the actual whole frame

\[
F_k=[N-16k-14,N-4],
\]

with original creator

\[
\Gamma_k=B(N+3,2k+1,1),
\]

and current-run removal

\[
\sigma_k=
\begin{cases}
B(N+7,k+1,1),&k<q,\\
B(N+7,q+1,0),&k=q.
\end{cases}
\tag{7.1}
\]

The preceding kappa is the previous cyclic sigma. To verify that run identity directly: these frames are absent in the initial right vine; their minimum size is 27, whereas first-SS outputs in this p=3 packet have at most 15 keys. Only the stated row-2 second outputs create them. All contain the final pivot N-7; the full B increasing reset preserves that pivot's ancestry of N through its hit and of 1 afterwards, so none is recreated there. Reverse-vine states also exclude them.

A is absent for each F_k at EVERY actual snapshot of the full H period. Thus membership holds on the COMPLETE cyclic Pi, with no prefix event or second physical copy counted. These are all q neutral doubles at that access, not a chosen residual.

For any fixed lambda,beta,gamma the exact offending expression is

    q-2lambda_S-(2beta+gamma).

An integer q>max(0,2beta+gamma+2lambda_S) makes it strictly positive. This is the all-coefficient certificate; no coefficient fit is required.

### 7.2 Additional preserved configurations

Transfer together with the principal packet:

* RG-02 F1 and (4.7): original E vector (q,q,q,2,1), enriched motif delta (q,-1,+1,-2). Keep every actual shared LEFT-edge deletion and the final LR correction.
* RG-02 F2: row 2, enriched delta (1,0,0,-2), b_0=u=n_2-1. Its fork and path counts do not grow across the transition despite actual changed occurrences.
* RG-02 F3 for every later row: delta (0,0,0,-2), b_0=u=n_j-1. The principal packet is its p=j=3 instance.
* RG-02 F4/F5 with their ORIGINAL smaller carrier and full low/gap subtrees: enriched deltas (+1,+1,-1,-2), (-1,-1,+1,-2), and their exact full-window run records. F5 independently defeats every fixed coefficient choice as r grows.
* The actual 97-key, 293-operation source and its four enriched critical vectors in Section 5.5. This remains finite control, not a substituted parametric source.
* The four A-side locality tables and constants (3,7,3,1); they remain valid even though the capacity classes fail.

The full literal transitions, physical IDs and source words remain in RG-02 and the explicit formulas here. No failed configuration is erased because a signed feature changes the outcome of a different individual test.

### 7.3 What has and has not been ruled out

All three EXACT frozen feature classes are eliminated for both proposed B-side laws, with arbitrary fixed signed rational coefficients. The proof also excludes fixed finite real coefficients in that span.

This is NOT a theorem that all state capacities are impossible. The three motif values coincide in the principal transition, but the full trees and their motif SETS do not coincide; many actual occurrences are replaced. A different permitted future state feature could distinguish them. No such feature is introduced or tested here.

This does NOT refute URCD or a whole-period source-work theorem. The original A preparations, private/hanging populations and actual restoration work are retained. The failure is of these specified local conservation certificates.

No larger motif radius is introduced. No candidate is sent to RG-05. RG-04 receives this report's exact failure packet only; its analysis is not begun.

## 8. Dependency, preservation and scope audit

The new universal locality proofs require only literal ordinary rotations, complete physical edges, actual path/fork tuples and SET duplicate suppression. The B-side counterexamples use the already explicit original complete source recurrences, whose all-tree construction is retained. Their motif counts are derived symbolically above, not inferred from passing or failing samples.

| Scope item | Exact treatment |
| --- | --- |
| Both primitive orientations | Separate edge/path/fork/SET tables |
| External parent and grandparent | c included for edges/forks; d included for two-edge paths |
| Empty L,H,R and root rotations | Conditional rows omitted, no empty-child/root-parent motif |
| Transported whole subtrees | Internal tuples unchanged; all attachment-crossing paths/forks checked |
| Arbitrary private A ancestors | All physical vertices retained; SET labels use eta(v) and duplicate suppression |
| LL,RR,LR,RL and real zig | Exact two-primitive substitution table and valid full-source reflection |
| Virtual accounting bits | No feature occurrence or physical transition |
| A fixed during B | Every match uses one explicit complete A_(x_j) |
| Path cardinality | Root-degree term retained explicitly; not treated as a fixed edge count |
| Original u_t domain | Every neutral demand at the cited access checked on its COMPLETE cyclic window |
| Source validity | Allowed diagonal/reaching prefix, all operations and complete A/B return |
| Repeated windows / cyclic seam | Original Gamma,kappa,sigma and IDs once per period |
| Coefficients | Fixed signed rationals; exclusion covers all finite real choices |
| Strong versus weak | Separate source-verified u values; neither failure inferred from the other alone |
| Quantifiers | A parameter grows against ALL fixed lambda,beta,gamma |
| Existing owners / scalar identities | Unchanged; no occupied bit is declared free |
| Evidence | Universal symbolic counting and parametric source proof, not numerical coefficient guesses |
| Stop boundary | No RG-04/RG-05 execution or unrelated strategy |

The static 97-key and warmed controls were not rerun. The new motif columns are manuscript deductions from their full physical recurrences. Symbolic author review is not separate-agent/external review or formal-kernel certification.

## 9. Sources and byte preservation

| ID | Current local source | Use |
| --- | --- | --- |
| S1 | [RG-01 primitive accounting](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md:1>) | PASS prerequisite, physical edges, original SET signs and actor/operation/real-bit conventions. |
| S2 | [RG-02 exact conservation failure](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG02_EDGE_CONSERVATION.md:1>) | All F1–F5 transitions, full B recurrences, complete cyclic windows, warmed support, saved 97-key control and exact occurrence IDs preserved. |
| S3 | [Original 97-key / W_(p,q) source reconstruction](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md:1>) | Literal physical perfect-block recurrence and source closure; selected last-generation frame creators/removals. |
| S4 | [H_(p,q) and warmed source definitions](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md:1>) | Original H word, all-adjacent A invariants, actual costs, warmed prefix and full return. |
| S5 | [Repository research rules](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md:1>) | Scope, source preservation, universal symbolic proof versus sampling, and stopping requirements. |

Current read-only SHA256 pins:

| ID | SHA256 |
| --- | --- |
| S1 | f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa |
| S2 | 16b93dbe5fa80a75da0591ad79765581ffc8a8c826b6f41758e985270de2253e |
| S3 | 1c31d4b5d8c97771640e5235e2015a95b584753d42ada4987600d071d8466176 |
| S4 | 4cf67ae246987f211997e18a5efb5b6d37ab9afbf800777769bbd2f56de5d42a |
| S5 | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |

Workspace:

    C:\Users\Saif malik\OneDrive\Documents\Desktop\Temp\splay-multiscale-transfer-liquidity-k6c2
    Branch: coarse-double-branch
    HEAD: 6d532b2c795c0778f57d8023b23b5fedfc48b010

Only this new RG03_CAPACITY_RECONSTRUCTION.md is written under DO_RESEARCH_REBOOT. RG-01, RG-02, all prior source artifacts, programs, physical event IDs, owners, resource records and Git state are preserved.

No source query, semantic replay, generated-tree experiment, enumeration, solver/coefficient search, proof-assistant run, external search or subagent was used. Static manuscript/hash checks establish preservation, not a computational universal proof.

## 10. Final verdict

**RG-03: FAIL — all three frozen feature classes are eliminated for BOTH the strong and complete-window weak B-side laws.**

The four A-side locality obligations PASS, with valid absolute constants

\[
(L_E,L_P,L_F,L_S)=(3,7,3,1).
\]

The decisive source-valid obstruction is

\[
b_{0,t}=u_t=q,\quad d_t=2,\quad k_t=1,\quad
(\Delta_B f_E,\Delta_B f_P,\Delta_B f_F,\Delta_B f_S)=(0,0,0,-2)
\]

on the complete original H_(3,q) for all q>=1. Every fixed coefficient choice would require q-2lambda_S<=2beta+gamma for every q. That is impossible.

BEFORE: E-only conservation failed; the four specified state features had to be tested without free indicator assignments or sampled coefficient fits.
RESULT: all four A-side change bounds are proved, the required primitive/full-source constraints are derived, and the nested feature classes are excluded in order by literal parametric source transitions.
AFTER: no accepted capacity certificate exists in this frozen span. The exact source configurations and locality proofs are the RG-04 input packet.
NET ADVANCEMENT: a complete decision of the authorized four-feature reconstruction gate. No general impossibility for state capacities or URCD is claimed.

**Stop. RG-04 and RG-05 have not been executed.**
