# RG-01 — Primitive rotation and edge accounting

Date: 2026-11-09, Asia/Karachi.

## Scope freeze and proof plan

Authorized task: RG-01 ONLY. Output: this new RG01_PRIMITIVE_ACCOUNTING.md. RG-02 is outside scope and will not be started.

BEFORE the formal derivation:

1. Strictly smaller obligation: prove a primitive physical-edge identity, its A-access Lipschitz consequence, and exact event/telescoping conventions. No universal interior-count, restoration-selection, matching or Coarse-Double theorem is attempted.
2. Concrete mechanism: list every changed physical parent-child edge of a literal rotation, retain the external attachment and middle subtree, and apply finite-set indicator identities. Reconstruct the inherited SET signs separately using the two changed subtree-label candidates.
3. One principal objective: an exact all-tree accounting model. The proof uses symbolic arbitrary subtrees and finite-sum telescoping; it needs no source generation, sampling, enumeration, solver, replay or additional open theorem.
4. Upward advancement: discharge RG-01's edge-change and accounting acceptance tests. Passing this foundational step does not discharge a later edge/label comparison or any global source-work inequality.

Keep the original finite present-key Pair Access model, KEEP/DELETE semantics, full physical populations, physical occurrence IDs, complete paired closure, carrier/SET conventions and historical owners. Only the user-prescribed Phi_0 and the inherited Psi are used. The requested Markdown artifact stays in the repository and is not duplicated into Notion.


## 1. Original physical source and frozen edge set

Let X be any finite totally ordered set of distinct PHYSICAL keys. A complete labelled BST here contains every key of X exactly once; "complete" does not impose a balanced or full-binary shape. Empty child slots contain no vertex. The original model permits any valid diagonal (T_0,T_0), followed by a legal reaching prefix and then the period under study. [S1, S6–S8]

A KEEP x splays present key x in A and then in B. A DELETE x splays x in A and freezes B: it omits a retained occurrence, never a physical key. All helpers, private A ancestors, B hangers and root repetitions remain. A period is exactly paired-closed when each COMPLETE labelled tree returns to its own initial tree; the two trees need not equal each other at that boundary. The reaching prefix supplies no period cost or event.

For any such tree T define exactly

\[
E(T)=\{(p,c,s)\in X\times X\times\{\mathrm{LEFT},\mathrm{RIGHT}\}:
       \mathrm{child}_s^T(p)=c\}.
\tag{1.1}
\]

This counts actual directed parent-child edges, with their actual child orientation. It includes edges at private/unmarked physical vertices. It excludes null slots, a fictitious parent of the root, ancestor shortcuts, projected S-subtree relations and virtual accounting bits. Updating a stored reciprocal parent pointer is not a second edge. For nonempty X, |E(T)|=|X|-1; for empty X it is zero.

Define the USER-PRESCRIBED physical-edge quantity

\[
\Phi_0(A,B)=|E(B)\setminus E(A)|.
\tag{1.2}
\]

It uses all physical X, independently of S or any subtree-label projection.

For fixed B and one A rotation A->A',

\[
\Delta_A\Phi_0=\Phi_0(A',B)-\Phi_0(A,B).
\tag{1.3}
\]

For fixed POST-A A and one B rotation B->B',

\[
\Delta_B\Phi_0=\Phi_0(A,B')-\Phi_0(A,B).
\tag{1.4}
\]

These are different phases. The A in (1.4) is the already processed target-rooted tree.

## 2. Exact primitive physical-edge changes

Write rt(U) for the physical root of a nonempty subtree U. L,H,R below are arbitrary pairwise disjoint actual subtrees, possibly empty. Every internal edge of each subtree is retained. If g has an external parent c, write sigma for the original LEFT/RIGHT slot of g at c.

### 2.1 Left rotation, including the external attachment

Start with the literal transformation

\[
g(L,p(H,R))\longrightarrow p(g(L,H),R).
\tag{2.1}
\]

Here g<p, and the inorder blocks are L,g,H,p,R. The entire rotated frame occupies the same position and key interval at c. Therefore the replacement root p uses the SAME external slot sigma, whether sigma is LEFT or RIGHT.

| Physical relation | Before | After | Exact edge status |
| --- | --- | --- | --- |
| External attachment, if c exists | (c,g,sigma) | (c,p,sigma) | Delete old; add new, with sigma preserved |
| Pivot relation | (g,p,RIGHT) | (p,g,LEFT) | Delete old; add new; direction and child orientation change |
| Middle-subtree attachment, if H is nonempty, h=rt(H) | (p,h,LEFT) | (g,h,RIGHT) | Delete old; add new; the boundary edge changes |
| Left outer attachment, if L is nonempty, l=rt(L) | (g,l,LEFT) | (g,l,LEFT) | Transported UNCHANGED; zero deletions/additions |
| Right outer attachment, if R is nonempty, v=rt(R) | (p,v,RIGHT) | (p,v,RIGHT) | Transported UNCHANGED; zero deletions/additions |
| Every internal edge of L | Same tuple | Same tuple | UNCHANGED |
| Every internal edge of H | Same tuple | Same tuple | UNCHANGED, despite H's changed external parent |
| Every internal edge of R | Same tuple | Same tuple | UNCHANGED |
| Every other edge outside the frame, including c's other child and c's own incoming edge, if present | Same tuple | Same tuple | UNCHANGED |

When c is absent, the global root changes g->p, but there is NO root-parent edge to delete or add. When H is empty, its two listed boundary edges are both absent, not empty-child edges. The same omission convention applies to the unchanged L/R attachments.

The exact deleted/added sets are

\[
\begin{aligned}
\mathcal E^-_\rho
 &=\{(g,p,\mathrm{RIGHT})\}
   \cup\{(c,g,\sigma):c\text{ exists}\}
   \cup\{(p,h,\mathrm{LEFT}):H\ne\varnothing\},\\
\mathcal E^+_\rho
 &=\{(p,g,\mathrm{LEFT})\}
   \cup\{(c,p,\sigma):c\text{ exists}\}
   \cup\{(g,h,\mathrm{RIGHT}):H\ne\varnothing\}.
\end{aligned}
\tag{2.2}
\]

Conditional singleton sets in this notation are omitted when their condition is false.

### 2.2 Right rotation, derived separately

Now start with

\[
g(p(L,H),R)\longrightarrow p(L,g(H,R)).
\tag{2.3}
\]

Here p<g, with inorder blocks L,p,H,g,R. Again the whole frame keeps its interval and external slot sigma.

| Physical relation | Before | After | Exact edge status |
| --- | --- | --- | --- |
| External attachment, if c exists | (c,g,sigma) | (c,p,sigma) | Delete old; add new, with sigma preserved |
| Pivot relation | (g,p,LEFT) | (p,g,RIGHT) | Delete old; add new; direction and child orientation change |
| Middle-subtree attachment, if H is nonempty, h=rt(H) | (p,h,RIGHT) | (g,h,LEFT) | Delete old; add new; the boundary edge changes |
| Left outer attachment, if L is nonempty, l=rt(L) | (p,l,LEFT) | (p,l,LEFT) | Transported UNCHANGED; zero deletions/additions |
| Right outer attachment, if R is nonempty, v=rt(R) | (g,v,RIGHT) | (g,v,RIGHT) | Transported UNCHANGED; zero deletions/additions |
| Every internal edge of L | Same tuple | Same tuple | UNCHANGED |
| Every internal edge of H | Same tuple | Same tuple | UNCHANGED |
| Every internal edge of R | Same tuple | Same tuple | UNCHANGED |
| Every other edge outside the frame, including c's other child and c's own incoming edge, if present | Same tuple | Same tuple | UNCHANGED |

Thus, for THIS right rotation,

\[
\begin{aligned}
\mathcal E^-_\rho
 &=\{(g,p,\mathrm{LEFT})\}
   \cup\{(c,g,\sigma):c\text{ exists}\}
   \cup\{(p,h,\mathrm{RIGHT}):H\ne\varnothing\},\\
\mathcal E^+_\rho
 &=\{(p,g,\mathrm{RIGHT})\}
   \cup\{(c,p,\sigma):c\text{ exists}\}
   \cup\{(g,h,\mathrm{LEFT}):H\ne\varnothing\}.
\end{aligned}
\tag{2.4}
\]

If c is absent, p becomes the global root without creating a root-parent edge. If H is empty its boundary row is omitted. Empty L/R have no attachment or internal edges.

### 2.3 Completeness and exact cardinality of both tables

All nonempty frame roots g,p,c,h,l,v are the indicated distinct physical vertices. An edge in an unchanged row remains the same ordered triple, even if its depth or ancestors change.

For either orientation each newly listed edge was absent before rotation: p formerly had parent g, g formerly had parent c or no parent, and h formerly had parent p. Their new parents differ. The corresponding deleted edges are absent afterwards. Consequently

\[
E(T')=(E(T)\setminus\mathcal E^-_\rho)\cup\mathcal E^+_\rho,
\quad
\mathcal E^-_\rho=E(T)\setminus E(T'),
\quad
\mathcal E^+_\rho=E(T')\setminus E(T).
\tag{2.5}
\]

There are no further changed edges: every physical edge is either one of the three changed boundary relations, one of the retained outer attachments, an internal subtree edge, or an outside edge.

In particular the deletion/addition sets are disjoint and

\[
|\mathcal E^-_\rho|=|\mathcal E^+_\rho|
 =m_\rho=1+\mathbf1[c\text{ exists}]+\mathbf1[H\ne\varnothing]\le3.
\tag{2.6}
\]

| External c | Middle H | Deleted edges | Added edges |
| --- | --- | ---: | ---: |
| Absent | Empty | 1 | 1 |
| Absent | Nonempty | 2 | 2 |
| Present | Empty | 2 | 2 |
| Present | Nonempty | 3 | 3 |

This is a symbolic exhaustion of the two optional boundary relations, not sampled-tree evidence. The direct pointer updates in the original primitive implementation agree with the tables; the all-tree proof is (2.1)–(2.6), not an execution of that code. [S9]

## 3. Exact physical-edge effects and the A-side bound

### 3.1 A rotation with B fixed

Let F=E(B) be any fixed complete physical B edge set. Changed old edges in F cease to be common and increase Phi_0; changed new edges in F become common and decrease it. All other contributions cancel. Therefore EXACTLY

\[
\Delta_A\Phi_0
 =|\mathcal E^-_\rho\cap E(B)|
  -|\mathcal E^+_\rho\cap E(B)|.
\tag{3.1}
\]

For example, the external row of the left table contributes

\[
\mathbf1[(c,g,\sigma)\in E(B)]
-\mathbf1[(c,p,\sigma)\in E(B)]
\]

when present; the pivot and H rows contribute their corresponding old-minus-new indicators. Every unchanged row contributes zero. The right table uses exactly its separately specified orientations.

Both counts in (3.1) lie in [0,m_rho]. Their DIFFERENCE, rather than the sum of their individual upper bounds, therefore satisfies

\[
\boxed{|\Delta_A\Phi_0|\le m_\rho\le3.}
\tag{3.2}
\]

This proves the requested universal constant THREE. No smaller uniform constant is asserted, and deleting plus adding three edges does not justify replacing this difference by a six-unit count.

### 3.2 B rotation with the post-A tree fixed

For fixed post-A A, an added edge contributes if it is missing from E(A), and a removed edge ceases to contribute if it was missing from E(A). Thus EXACTLY

\[
\Delta_B\Phi_0
 =|\mathcal E^+_\rho\setminus E(A)|
  -|\mathcal E^-_\rho\setminus E(A)|.
\tag{3.3}
\]

Because the two edge sets have equal cardinality, the same expression is also

\[
\Delta_B\Phi_0
 =|\mathcal E^-_\rho\cap E(A)|
  -|\mathcal E^+_\rho\cap E(A)|.
\tag{3.4}
\]

These are physical-edge identities. They do not classify a B rotation as decreasing or neutral for Psi. No correspondence between the signs of Phi_0 and Psi is assumed.

### 3.3 One full A access

Let A^(0),...,A^(r_t) be the actual consecutive trees in access t, so A^(0)=A_(t-1) and A^(r_t)=A_t. B stays B_(t-1) throughout. Applying (3.1) to each ACTUAL real rotation and telescoping within the A phase gives

\[
\begin{aligned}
\Delta_{A,t}\Phi_0
 &=\Phi_0(A_t,B_{t-1})-\Phi_0(A_{t-1},B_{t-1})\\
 &=\sum_{i=1}^{r_t}
   [\Phi_0(A^{(i)},B_{t-1})-\Phi_0(A^{(i-1)},B_{t-1})].
\end{aligned}
\]

Hence

\[
\boxed{|\Delta_{A,t}\Phi_0|
       \le\sum_{i=1}^{r_t}m_{\rho_i}
       \le3r_t.}
\tag{3.5}
\]

The bound does not require closure, a diagonal start, a carrier population bound, or any relation between the shapes of A and B.

* Root rotations: c is absent; (2.6) automatically omits its row.
* Empty L/H/R: only actual nonempty attachments are counted.
* Terminal zig: there is one real rotation. Its virtual companion has no tree transition and no edge.
* LL/RR double: first rotate the intermediate parent over the grandparent, then the target over that parent. Apply a fresh primitive table with the CURRENT c,H at each bit.
* LR/RL double: first rotate the target over its parent, then over its grandparent. Again apply the two current primitive tables. A double has two real rotations and contributes at most six to the sum of absolute primitive changes.
* Private A ancestors and arbitrary physical populations: all of their actual edges are included; nothing is contracted into a carrier shortcut.
* A root request: r_t=0, so the sum is empty and Delta_(A,t)Phi_0=0.
* Empty X admits no access; a one-key tree admits only root requests. The claims are then vacuous or zero.


## 4. Reconstructing the original SET signs, separately from Phi_0

### 4.1 Original label convention and source assumptions

For the nontrivial original closed B source, retain its fixed labelled carrier S. All KEEP targets and B path operands lie in S; S is ancestor-closed in B, and every off-S physical B hanger is S-free. These properties persist through the fine B rotations. A has no corresponding carrier restriction. [S2, S3, S6–S8]

For a physical vertex v write

\[
\operatorname{lab}_S^T(v)=S\cap\{\text{physical descendants of }v
                            \text{ in }T,\text{ including }v\}.
\]

The original convention is

\[
J_S(T)=\{\operatorname{lab}_S^T(v):v\in X,\ \operatorname{lab}_S^T(v)\ne\varnothing\},
\qquad
\Psi(A,B)=|J_S(B)\setminus J_S(A)|.
\tag{4.1}
\]

J_S is a SET, not a multiset. It includes the full S label when S is nonempty. Private A vertices may give duplicate labels, counted once. This is not E(T): it records descendant KEY SETS, not parent-child triples.

When genuine B support is empty, B has no real rotations. All B event counts below are zero, and their global bounds are direct. No nontrivial-carrier theorem is needed for that case. Empty S, if used by the original degenerate convention, has J_S(T)=empty and Psi=0.

### 4.2 Exact A SET changes, including duplicate suppression

For an arbitrary real A rotation let

\[
\mathcal L^- =J_S(A)\setminus J_S(A'),
\qquad
\mathcal L^+ =J_S(A')\setminus J_S(A).
\]

The whole rotated frame's label persists at its new root. Labels internal to L,H,R and labels outside the frame, including ancestor labels, are unchanged. Only the promoted child's OLD proper-subtree label is a possible loss; only the demoted pivot's NEW proper-subtree label is a possible creation.

Each of L^- and L^+ therefore has cardinality at most one. An empty candidate is ignored. A candidate still represented at another vertex is NOT SET-lost, and an already represented candidate is NOT SET-created.

With B fixed,

\[
\Delta_A\Psi
 =|\mathcal L^-\cap J_S(B)|
  -|\mathcal L^+\cap J_S(B)|
 \in\{-1,0,1\}.
\tag{4.2}
\]

This proves the original real-A classification: positive means +1, negative means -1, and zero means 0, computed from ACTUAL SET differences. It does not classify by a representative's disappearance alone. [S3, S4, S8]

### 4.3 Exact B SET changes at the post-A target-rooted tree

Fix a KEEP target x and the post-A tree rooted at actual physical key x.

In every ordinary B primitive rotation the promoted node is either:

* x itself; or
* its intermediate parent in the first rotation of an LL/RR double.

In both cases the promoted child's OLD proper-subtree label I contains x. The demoted pivot's NEW proper-subtree label J excludes x.

Both operands belong to S. I contains the promoted S vertex and excludes the demoted S pivot; J contains that pivot and excludes the promoted vertex. Thus I,J are proper and nonempty. They are different because I contains x and J excludes x. Distinct nonempty B labels have unique representatives: S-free vertices have empty labels, while strict ancestor S vertices contribute an additional S key. Thus the ACTUAL B SET differences are exactly loss of I and creation of J; the whole-frame label is transported unchanged.

Because A is rooted at x, its only subtree containing physical x is the whole tree, whose S label is S. The proper label I is therefore absent from J_S(A). It follows that

\[
\Delta_B\Psi
 =-1+\mathbf1[J\notin J_S(A)]
 =
 \begin{cases}
 -1,&J\in J_S(A),\\
 0,&J\notin J_S(A).
 \end{cases}
\tag{4.3}
\]

A DECREASING real B rotation means the first case of (4.3). A NEUTRAL real B rotation means the second. These words refer to Psi throughout the event counts; the sign of Delta_B Phi_0 is not substituted.

For a terminal B zig the old pivot is the global B root, and x becomes its root. The new demoted label J is exactly the nonempty full S side of x containing that pivot: S_<x for a left rotation, S_>x for a right rotation. The actual corresponding side subtree of target-rooted A has that same S label, irrespective of private physical vertices. Hence EVERY original terminal B zig is decreasing. It is one real B rotation, not a double demand.

No equality of A and B shapes is used. The essential assumptions are target-rooted post-A order, complete presence of all physical keys, and the original S-path/SET properties. The proof would not license using an arbitrary projected label collection in place of J_S.

## 5. Exact per-access event conventions

### 5.1 Costs, physical rotations and original IDs

Let delta^A_t be the original A edge depth of the present target x_t before its splay. Let delta^B_t be its original B edge depth on KEEP. The source costs are

\[
a_t=\lceil\delta^A_t/2\rceil,\qquad
q_t=\begin{cases}\lfloor\delta^B_t/2\rfloor&\mathrm{KEEP},\\0&\mathrm{DELETE},\end{cases}
\quad
A(W)=\sum_t a_t,\quad Q_B(W)=\sum_tq_t.
\tag{5.1}
\]

For A put v_(A,t)=delta^A_t mod 2. Ordinary bottom-up splay has floor(delta^A_t/2) doubles, then one terminal zig if v_(A,t)=1. Each double raises the target two levels using two actual rotations; a zig raises it one using one. Therefore define

\[
\boxed{r_t=\#\{\text{ACTUAL real A rotations at }t\}
          =\delta^A_t=2a_t-v_{A,t}.}
\tag{5.2}
\]

A double at original StepEv j has two real IDs A(t,j,0), A(t,j,1), in actual execution order. A terminal zig has one real ID A(t,j,0) and one distinct VIRTUAL accounting bit (t,j,1). The latter is not a rotation, an edge, or a new tree snapshot.

On KEEP let z_t=delta^B_t mod 2; on DELETE set z_t=0. B has q_t actual double IDs (t,j), j=1,...,q_t, with real rotations B(t,j,0), B(t,j,1). If z_t=1 its terminal real rotation is B(t,q_t+1,0). That terminal rotation supplies no extra double demand. The actual B real-rotation count is 2q_t+z_t.

Every actor, operation, StepEv and bit retains its original occurrence ID. Displaying chronological positions or a cyclic lift does not allocate or rename physical events. A reaching-prefix event is not counted in W.

### 5.2 Required B counts

For EVERY original access define

\[
\boxed{d_t=\#\{\text{real B rotations at }t
                          \text{ with }\Delta_B\Psi=-1\},}
\tag{5.3}
\]

\[
\boxed{k_t=\mathbf1[\text{B performs a nontrivial splay at }t]
          =\mathbf1[\mathrm{KEEP}\text{ and }\delta^B_t>0],}
\tag{5.4}
\]

\[
\boxed{b_{0,t}=\#\{\text{B doubles at }t
           \text{ whose TWO individual }\Delta_B\Psi\text{ equal }0\}.}
\tag{5.5}
\]

The two signs in (5.5) are evaluated at the double's two successive ACTUAL B snapshots, with the SAME post-A A_t fixed. Fully neutral means BOTH real rotations are neutral, not merely an edge-potential test.

For i=1,2 also let b_(i,t) count doubles with exactly i decreasing real bits. These are exhaustive because (4.3) excludes B-positive bits. By the terminal-zig proof,

\[
q_t=b_{0,t}+b_{1,t}+b_{2,t},\qquad
d_t=b_{1,t}+2b_{2,t}+z_t.
\tag{5.6}
\]

On DELETE all q_t,z_t,d_t,k_t,b_(i,t) are zero, even if A has positive cost. On a B-root-repeat KEEP they are also zero, even if DELETE helpers made the A access nontrivial. Conversely r_t=0 at one KEEP does NOT force k_t=0: prior A work may already have brought x_t to A's root.

Notation audit: RG-01's r_t is a real A-rotation count and its d_t is a B-decrease count. PC35 uses those same letters for a release budget and a deficit in a DIFFERENT displayed convention. Those legacy variables are not imported here. Also D_B below is a COUNT of decreasing real B rotations; it is not the legacy calligraphic set of all B-double demands, whose cardinality is Q_B. [S2, S5]

### 5.3 Complete interior always-A-absent class and u_t

For each fully neutral double d=(t,j), let F_d be its ORIGINAL whole grandparent-frame S label just before its first primitive rotation, not either designated output label.

A fully neutral whole frame is proper. Indeed a double whose grandparent is the global B root makes x the global root at its end. In SS its second new label is the full corresponding S side of x; in LR/RL the created side labels are full S sides. At least one such nonempty label is A-present at the target-rooted post-A tree, giving a decreasing bit. Thus a fully neutral double cannot have whole frame S.

Retain the original historical records of that frame:

* Gamma_d: its last B SET creation before the producing access;
* kappa_d: the B SET removal of the same label preceding Gamma_d;
* t^A_d: the producer's post-A/pre-B snapshot;
* Pi_d=(kappa_d,t^A_d], in actual cyclic order.

These are original label runs, as specified in Route 04 Section 5 and Route 02 Step 4 A2. A newly created proper B label always excludes that access's target, by Section 4.3. Therefore the whole frame containing x_t existed before this producer access, rather than being newly born in its earlier double. The first B access inside a live proper label removes it before that access ends, since its target becomes the global root. Outside accesses preserve that subtree. Paired closure supplies the corresponding preceding creation/removal records. These facts justify retaining the run records; no creator-forest counting theorem is needed here.

For nonempty S, the COMPLETE interior class is

\[
\mathcal U_{\mathrm{int}}(W)=
\{d:\ d\text{ fully neutral},\
 \min S,\max S\notin F_d,\
 F_d\notin J_S(A_\tau)\ \text{at EVERY actual snapshot }\tau\in\Pi_d\}.
\tag{5.7}
\]

Define EXACTLY

\[
\boxed{u_t=|\{d\in\mathcal U_{\mathrm{int}}(W):
                         \text{producer operation of }d\text{ is }t\}|.}
\tag{5.8}
\]

Then sum_t u_t=U_int(W) and 0<=u_t<=b_(0,t). When there is no possible B double, the class is empty. On DELETE, u_t=0.

This includes ALL eligible original demands, whether already paid or not, silent or not, SS or LR/RL, attached or unattached, and regardless of historical owner. It is the complete Route 04 always-absent class with the Route 02 Step 4 carrier-extreme partition, not a selected residual. [S6–S8]

u_t is HISTORY-DEPENDENT. Besides two current B signs and the whole-frame carrier endpoints, it requires the actual preceding B run and A membership at every snapshot since kappa_d. One local B rotation and its Delta_B Psi supply neither those historical records nor the full A-absence predicate. A-absence only at the current producer or at Gamma_d is insufficient to establish membership. No local rotation test is substituted for (5.7).

## 6. Verification of the inherited global bounds

Put

\[
R_A=\sum_t r_t,\quad V_A=\sum_t v_{A,t},\quad
D_B=\sum_t d_t,\quad K_B=\sum_t k_t,\quad
B_i=\sum_t b_{i,t},\quad Z_1=\sum_tz_t.
\tag{6.1}
\]

Z_1 counts actual decreasing terminal B zigs; it equals Z_B here by Section 4.3.

### 6.1 R_A <= 2A: cost identity, no closure needed

Summing (5.2),

\[
\boxed{R_A+V_A=2A,\qquad R_A=2A-V_A\le2A.}
\tag{6.2}
\]

Assumptions: present-key ordinary bottom-up A splay and the original ceil(depth/2) StepEv cost. KEEP and DELETE are both counted. Neither S nor closure is required. Virtual units contribute to 2A but never to R_A or E(T).

### 6.2 D_B <= 2A: original SET signs and paired closure

Let P,N,T_A count ALL real A rotations whose actual Delta_A Psi is +1,-1,0. Section 4.2 gives the exhaustive partition

\[
R_A=P+N+T_A.
\tag{6.3}
\]

For exactly paired-closed W, with the SAME fixed S and A-then-B phase order, Psi has the same initial and final value. The total A change is P-N; the total B change is -D_B by (4.3). Hence

\[
0=P-N-D_B,\qquad
D_B=P-N=B_1+2B_2+Z_1.
\tag{6.4}
\]

Consequently

\[
\boxed{D_B=P-N\le P\le R_A\le2A.}
\tag{6.5}
\]

The assumptions behind this bound are important: original fixed S and SET convention, target-rooted post-A B phases, all original A rotations/helpers, and EXACT closure of both complete trees. The bound is not inferred from Phi_0. Without closure the corresponding SET-potential endpoint term must be retained; it cannot be discarded.

If B has no real rotations, D_B=0 directly. No nontrivial carrier assertion is needed for that degenerate case.

As a source-identity cross-check, (5.6), (6.2)–(6.4) give exactly

\[
Q_B=B_0+B_1+B_2,\qquad
2A=P+N+T_A+V_A,
\]

\[
\boxed{2A-Q_B=2N+T_A+V_A+B_2+Z_1-B_0.}
\tag{6.6}
\]

This is the original scalar identity [S4, S5, S8]. No sign of its right-hand side, matching availability or Universal CD conclusion is inferred.

### 6.3 K_B <= A: distinct actual cyclic KEEP-gap work

If there are no KEEPs, K_B=0. Otherwise, for each nontrivial B KEEP t let t^- be the immediately preceding KEEP in cyclic source order, including identity KEEPs.

Let y be its target. B's root before t is y, since B ended t^- rooted at y and freezes on every intervening DELETE. Nontriviality at t is therefore exactly x_t!=y.

A is rooted at y after the A phase of t^- and at x_t after the A phase of t. The ORIGINAL gap from those post-A boundaries must contain at least one nonzero A StepEv. It may be in a DELETE/helper access rather than in the receiving KEEP.

Choose the first such original StepEv f(t). Consecutive KEEP gaps partition the actual A event occurrences cyclically, so different nontrivial B KEEPs have DISTINCT f(t). Each f(t) has cost one; no virtual companion supplies another StepEv. Thus

\[
\boxed{K_B\le A.}
\tag{6.7}
\]

Assumptions: A processes every KEEP, each splay ends at its actual target root, B processes only KEEP, and exact paired closure licenses the cyclic seam. No S population bound, owner vacancy, nonzero A cost at the current KEEP, or double at that KEEP is assumed.

For a word with just one KEEP occurrence, closure makes its B access a root repeat, so k_t=0. A seam that passes through DELETEs includes their actual A events ONCE. Empty words and zero-event gaps cause no exception.


## 7. Operation-level and paired-closed telescoping conventions

Use the exact original phase order

\[
(A_{t-1},B_{t-1})
 \longrightarrow(A_t,B_{t-1})
 \longrightarrow(A_t,B_t).
\tag{7.1}
\]

A_t denotes the post-A tree, which stays fixed throughout B's phase. Define

\[
\begin{aligned}
\Delta_{A,t}\Phi_0
 &=\Phi_0(A_t,B_{t-1})-\Phi_0(A_{t-1},B_{t-1}),\\
\Delta_{B,t}\Phi_0
 &=\Phi_0(A_t,B_t)-\Phi_0(A_t,B_{t-1}),\\
\Delta_t\Phi_0
 &=\Phi_0(A_t,B_t)-\Phi_0(A_{t-1},B_{t-1}).
\end{aligned}
\tag{7.2}
\]

Add the first two equalities. Their intermediate value cancels, giving the EXACT identity

\[
\boxed{\Delta_t\Phi_0
       =\Delta_{A,t}\Phi_0+\Delta_{B,t}\Phi_0.}
\tag{7.3}
\]

Each phase difference also equals the sum of its primitive real-rotation differences, using (3.1) for A and (3.3) for B. This is cancellation along the actual intermediate physical trees, with no sign or independence assumption.

Display a period by chronological positions 1,...,m, without changing its original occurrence IDs. Summing (7.3) gives, for ANY original finite history,

\[
\sum_{t=1}^m\Delta_{A,t}\Phi_0+
\sum_{t=1}^m\Delta_{B,t}\Phi_0
 =\Phi_0(A_m,B_m)-\Phi_0(A_0,B_0).
\tag{7.4}
\]

For an EXACTLY PAIRED-CLOSED source, A_m=A_0 and B_m=B_0 as COMPLETE labelled physical trees. Therefore

\[
\boxed{\sum_t\Delta_{A,t}\Phi_0+
       \sum_t\Delta_{B,t}\Phi_0=0.}
\tag{7.5}
\]

Equality of the two endpoint roots alone is not the closure assumption; the full edge sets must return. Nor does (7.5) require A_0=B_0: both individual trees return to their own starting values.

### 7.1 DELETE operations

B_t=B_(t-1), so Delta_(B,t)Phi_0=0. All actual A rotations still contribute by (3.1). Equation (7.3) holds with its B term zero. DELETE creates no physical deletion of a key or any new edge type.

### 7.2 Zero-cost and root-repeat accesses

If r_t=0, A_t=A_(t-1) and its A phase difference is zero. B may still move on KEEP, so its actual B term remains.

If B is a root repeat, B_t=B_(t-1) and its B difference is zero, regardless of A's cost. If both phases are identities, all three differences are zero. Such original operation occurrences remain in the history; none needs to be removed to telescope.

### 7.3 Terminal zigs and doubles

A real terminal zig contributes once, with its actual primitive table. Its virtual accounting companion supplies no physical transition. A double contributes its two successive real differences. The same cancellation holds if a hypothetical bookkeeping snapshot is inserted for a virtual unit only as an IDENTITY, but no such snapshot or edge is needed or counted.

B's real terminal zig also contributes once. Its Psi-decreasing classification does not replace its actual physical-edge Delta_B Phi_0 in (7.2).

### 7.4 The cyclic seam and the reaching prefix

The last complete pair equals the first complete pair, so a cut at any original operation boundary merely changes the first displayed summand. Every primitive real rotation keeps its ONE original actor/operation/StepEv/bit ID. A causal lift can express a gap crossing the seam but supplies no second physical copy or additional work.

The reaching prefix establishes legal reachability; it is not in (7.4) for W and is not borrowed to make (7.5) vanish. Empty periods have empty sums. With empty X, only the empty present-key history is legal; with one key every legal access is a root request and all edge changes are zero.

The same finite-state cancellation for the SEPARATE function Psi is exactly what was used in (6.4). This does not identify Psi with Phi_0.

## 8. Universal scope and acceptance audit

| Required scope / convention | Reason the proof covers it |
| --- | --- |
| Every finite complete labelled BST, arbitrary unbalanced shape | L,H,R and the external context are arbitrary; the changed-edge classification is exhaustive by location |
| LEFT and RIGHT primitive rotations | Separate tables and explicit orientations in (2.2), (2.4) |
| External parent in either child slot | Whole-frame interval stays fixed, so sigma is preserved |
| Rotation at global root | External row is omitted; root pointer is not an edge |
| Empty middle subtree | Both H boundary edges are absent; no null edge is invented |
| Empty outer subtrees | Their unchanged attachments and internal edges are omitted |
| Transported subtrees | Internal edges and retained outer attachments are unchanged even when depths/ancestors change |
| LL, RR, LR, RL | Ordinary doubles are two current primitive rotations, in original execution order |
| Terminal zig | One real bit; virtual companion excluded from edges and real-rotation counts |
| Private A ancestors and arbitrarily many physical vertices | Physical-edge proof uses all X; SET proof handles empty/duplicate labels at actual vertices |
| Present-key semantics | All requests target existing keys; absent-key API branches are not imported |
| KEEP and DELETE | Exact A-then-B order retained; DELETE has an identity B phase |
| Zero A cost at a nontrivial B KEEP | Allowed; K_B work may be in an earlier DELETE/helper in that actual KEEP gap |
| Zero B cost with positive A work | Allowed; B counts and B differences vanish independently |
| No KEEPs / empty genuine B support | All B event counts vanish directly |
| Arbitrary reachable paired states | Edge identities do not require A=B; closure is individual complete-tree return |
| Full Pi windows and ALL interior always-absent demands | Exact history predicate (5.7), not silence, owner status, local absence or a selected residual |
| Cyclic seam | Original IDs and disjoint actual KEEP gaps; no extra copy counted |
| Original SET and scalar identities | Re-derived independently of Phi_0; no scalar sign assumed |
| Owners, lambda, g_1 and historical payments | Not changed or needed for these identities |
| Evidence | Universal symbolic proof, not finite sampled trees, generated traces or computational enumeration |

The local edge identities and A-side bound require no carrier theorem or paired closure. The inherited D_B bound requires the original carrier/SET properties and paired closure; the K_B bound requires the original cyclic root-gap semantics and paired closure. These assumptions are stated where used and are not replaced by a projected physical model.

No bound connecting Delta_B Phi_0 to d_t, k_t, b_(0,t) or u_t is attempted here. Establishing such a further comparison is outside RG-01.

## 9. Source references and preservation

The three requested current reports were read in full. The original Pair Access, ND35 source/SET-sign specification, scalar-identity and residual-identity portions were read directly, as were the literal primitive functions. Only local static inspection and manuscript reasoning were used.

References use the actual current working bytes. Historical HEADs and unproved conclusions inside prior reports are not upgraded by RG-01's verdict.

| ID | Local source | Exact use |
| --- | --- | --- |
| S1 | [Original Pair Access specification](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md:1>) | Physical keys; diagonal reachability; complete closure; KEEP/DELETE; costs; ordinary rotation order. |
| S2 | [Original ND35 frozen source / SET model](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md:1>) | Original carrier, all physical subtrees, SET duplicates, original actor/operation/bit inventory. |
| S3 | [ND35 primitive SET-sign and closure reconstruction](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/ND35_UNIVERSAL_AUDIT.md:1>) | At-most-one SET loss/creation, post-A B signs, scalar closure conventions; reconstructed directly in Sections 4 and 6. |
| S4 | [Original scalar identity, Step 01 A2](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01_20261108/PARALLEL_SCALAR_INTERNAL_NEUTRAL_STEP01.md:42>) | Real/virtual partition and exact scalar identity, not a sign theorem. |
| S5 | [PC35 exact residual identity](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/PC35_RELEASE_COMPLETION_09/STEP1_EXACT_RESIDUAL_IDENTITY.md:43>) | Independent scalar reconciliation and the legacy per-access notation that RG-01 must not confuse. |
| S6 | [Current Route 02 Step 3](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_ALWAYS_ABSENT_20261108/STEP03_ALWAYS_ABSENT_FRAME_BOUND.md:1>) | Whole-frame Pi windows; real IDs; cyclic KEEP-gap injection; no linear closure imported. |
| S7 | [Current Route 02 Step 4 linear incidence](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_STEP04_LINEAR_INCIDENCE_20261108/STEP04_LINEAR_INCIDENCE_SOURCE_GEOMETRY.md:27>) | Original scope and all-U definition; carrier-extreme/interior partition. |
| S8 | [Current Route 04 relaxed-CD report](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md:1>) | Original physical model, costs, scalar identities, complete preceding-removal windows. |
| S9 | [Original primitive implementation, read only](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/python/liquidity/legacy_embedding.py:77>) | Literal _rot_right, _rot_left and bottom-up splay_trace. Code is corroborating provenance, not sampled proof. |
| S10 | [Repository research rules](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md:1>) | Scope gate, source preservation, symbolic/universal versus finite and independent-certification distinctions. |

Current read-only input SHA256 pins:

| ID | SHA256 |
| --- | --- |
| S1 | 8be55471edfdac31f59d552952c84f8d380bbfa3a7e46b7643d22af766757fd5 |
| S2 | a52487cfe212aa562b91406bb6006d2f9a9469bebcfd4e039d9cd224fc6d677b |
| S3 | fcd7ffc824cdfac51612d41421e59295c350d2a1ba2377d9d6b9cd33445f535d |
| S4 | 2304e5c6f9f030bba07f593fd7d3cb35eac742b4220a848d64bcb44f48dd37d0 |
| S5 | 7479a533f41cf2933f00409fafbad16f76678fee2f5a0161d22103ab316c238c |
| S6 | a06eff982f350aff51d4004b6ea1739e62e254b13455d3f872c66c2d5ec2c837 |
| S7 | 77702f3cb914d36a62adb5ba7511c141d92068b52680138997aefc845349e11a |
| S8 | f85354f04eed727e3bdc4c0ddca72c1a6f706885c35721ced525ee52fa26e712 |
| S9 | 20284bbc810a2c64c1b4f66f431b5479795b6d6658d258bb5d4a4f4b543e1cb2 |
| S10 | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |

Workspace:

    C:\Users\Saif malik\OneDrive\Documents\Desktop\Temp\splay-multiscale-transfer-liquidity-k6c2
    Branch: coarse-double-branch
    HEAD: 6d532b2c795c0778f57d8023b23b5fedfc48b010

Only this new RG01_PRIMITIVE_ACCOUNTING.md is written, under DO_RESEARCH_REBOOT. No source program, old report, source period, owner map, certificate, resource record, Route 01/03/04 artifact or Git state is modified.

No source query, replay, sampled-tree experiment, enumeration, solver search, proof-assistant run, external search or subagent is used. Static file/hash checks establish preservation, not a finite empirical substitute for proof. Symbolic author review is not separate-agent, external or formal-kernel certification.

## 10. Verdict

**RG-01: PASS — universal symbolic proof on the original physical-key source model.**

The acceptance obligations are discharged:

1. Exact left/right deletion/addition tables, including the external parent, correct child orientations, empty boundaries and transported unchanged edges: Section 2.
2. For ANY fixed complete B, one real A rotation has |Delta_A Phi_0|<=3, and one A access has |Delta_(A,t)Phi_0|<=3r_t: Section 3.
3. Actual real-event conventions, SET-based B decrease/neutral classifications, the complete history-dependent u_t predicate, and the inherited R_A<=2A, D_B<=2A, K_B<=A: Sections 4–6.
4. Exact A-then-B operation cancellation and paired-closed telescoping, with DELETE, zero-cost, terminal-zig and cyclic-seam cases: Section 7.

No claimed RG-01 identity fails under the stated assumptions, so no counterexample branch is invoked. No universal Coarse-Double or interior source-work inequality is claimed.

BEFORE: physical-edge changes and their relation to source event conventions had to be established without substituting SET labels or virtual bits.
RESULT: the universal tables, Lipschitz bound and telescoping identities are proved, and the two accounting systems are explicitly separated.
AFTER: RG-01 is complete. Historical open research remains at its existing status.
NET ADVANCEMENT: exactly the authorized primitive-accounting foundation; no additional global theorem or unproved premise is introduced.

**RG-02 has not been started.**
