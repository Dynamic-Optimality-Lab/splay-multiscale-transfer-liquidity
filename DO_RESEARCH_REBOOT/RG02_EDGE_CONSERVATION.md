# RG-02 — Edge-disagreement conservation test

Date: 2026-11-09, Asia/Karachi.

## Scope freeze and acceptance protocol

RG-01 was read in full and has PASS status. Its physical edges, real/virtual rotation IDs, original SET-label classifications, complete cyclic windows, A-then-B order and paired closure are retained. RG-01 and all prior artifacts are read-only.

The one authorized test is the proposed B-phase law for the UNMODIFIED capacity

\[
\Phi_0(A,B)=|E(B)\setminus E(A)|.
\]

STRONG quantifiers:

\[
\exists\beta,\gamma\in[0,\infty)\text{ finite}\quad
\forall W\text{ admissible}\quad\forall t\text{ B-producing}:
\quad b_{0,t}+\Delta_{B,t}\Phi_0\le\beta d_t+\gamma k_t.
\tag{S}
\]

WEAK quantifiers, tested separately if necessary:

\[
\exists\beta,\gamma\in[0,\infty)\text{ finite}\quad
\forall W\text{ admissible}\quad\forall t\text{ B-producing}:
\quad u_t+\Delta_{B,t}\Phi_0\le\beta d_t+\gamma k_t.
\tag{W}
\]

Constants may differ between the two assertions. d_t counts decreasing REAL B rotations for Psi, not a residual deficit; k_t is the nontrivial-B-splay indicator. b_(0,t) counts every fully neutral double, and u_t uses the COMPLETE interior always-A-absent class, not a selected subset or unpaid demand set.

BEFORE the formal derivation:

* Strictly smaller: decide these two specific per-access conservation laws, not universal source-work counting or URCD itself.
* Concrete mechanism: RG-01's exact deleted/inserted physical edges and their shared-edge indicators, evaluated in ONE specified complete post-A BST; then telescope across the ENTIRE B access.
* One principal objective: a complete proof or a source-valid parametric refutation. No free edge indicators, modified capacity, independently closed access, sampled-tree argument or additional open theorem is permitted.
* Upward advancement: either send a genuine passing law to RG-05, or preserve the complete exact failure configurations as the RG-03 transfer packet in this report. No RG-03/RG-05 proof work is begun here.

The original reaching prefixes, complete source periods, all physical keys, helpers, owners and resource records remain intact. Only this new report is written. All computations below are symbolic manuscript derivations; no source query, semantic replay, generated-tree experiment, solver or enumeration is run.


## 1. Exact primitive B transition tables

### 1.1 One actual post-A BST, not independent indicators

Fix the COMPLETE physical post-A tree A=A_t, rooted at its actual target x, throughout the entire B phase. For an actual edge e put

\[
\chi(e)=\mathbf1[e\in E(A)].
\]

Use e^L_(ab)=(a,b,LEFT), e^R_(ab)=(a,b,RIGHT). An external edge e^sigma_(ca) is omitted if c is absent. An attachment to rt(empty) is omitted. chi(D) means sum_(e in D) chi(e), so D intersect E(A) is exactly the subset of its displayed edges with chi=1.

These indicators all come from this ONE complete labelled BST: every nonroot has one parent, each parent has at most one child per side, all edges satisfy BST order and acyclicity, and EVERY incoming edge to x has chi=0. They are not free Boolean variables. In the counterfamilies below A is explicitly specified and every shared-edge test is evaluated in that tree.

For any row with deleted set D and inserted set N, RG-01 gives EXACTLY

\[
\delta\Phi_0=\chi(D)-\chi(N).
\tag{1.1}
\]

All edges internal to the displayed hanging subtrees, and all edges outside the affected frame, are unchanged. Retained outer attachments are unchanged as specified in RG-01. Only the displayed boundary edges are deleted/inserted.

For SET classifications write J(U)=S intersect keys(U). If a row creates the demoted-pivot label K, then

\[
s(K)=\mathbf1[K\in J_S(A)],\qquad
\delta\Psi=-s(K).
\tag{1.2}
\]

The row decreases precisely when s(K)=1 and is neutral precisely when s(K)=0. This follows from RG-01: the old lost proper label contains target x and is A-absent. No edge sign is substituted for (1.2).

### 1.2 RR, both original real rotations

Literal complete transformation, with external parent c of g in slot sigma:

\[
g(L,p(H,x(C,R)))
 \longrightarrow p(g(L,H),x(C,R))
 \longrightarrow x(p(g(L,H),C),R).
\]

Let h=rt(H), v=rt(C) when nonempty.

| Bit / actual operands | Deleted physical edges D | Inserted physical edges N | New SET label K |
| --- | --- | --- | --- |
| 0: left rotation at g, promoting intermediate parent p | cg^sigma, gp^R, ph^L | cp^sigma, pg^L, gh^R | K_0=J(L) union {g} union J(H) |
| 1: left rotation at p, promoting target x | cp^sigma, px^R, xv^L | cx^sigma, xp^L, pv^R | K_1=K_0 union {p} union J(C) |

Here, for example, cg^sigma abbreviates e^sigma_(cg); ph^L is e^L_(ph). Only conditional external/middle edges are omitted.

The shared deleted/inserted counts are respectively the sums of chi over the entries of each D/N column. With incoming-x indicators zero, the exact deltas are

\[
\begin{aligned}
\delta_0&=\chi(cg^\sigma)+\chi(gp^R)+\chi(ph^L)
          -\chi(cp^\sigma)-\chi(pg^L)-\chi(gh^R),\\
\delta_1&=\chi(cp^\sigma)+\chi(xv^L)-\chi(xp^L)-\chi(pv^R).
\end{aligned}
\tag{1.3}
\]

Each bit's classification is (1.2) using its displayed K_i. The external edge cp^sigma inserted by bit 0 is deleted by bit 1; its shared contribution cancels in their sum.

### 1.3 LL, both original real rotations

\[
g(p(x(L,C),H),R)
 \longrightarrow p(x(L,C),g(H,R))
 \longrightarrow x(L,p(C,g(H,R))).
\]

| Bit / actual operands | Deleted D | Inserted N | New SET label K |
| --- | --- | --- | --- |
| 0: right rotation at g, promoting intermediate parent p | cg^sigma, gp^L, ph^R | cp^sigma, pg^R, gh^L | K_0=J(H) union {g} union J(R) |
| 1: right rotation at p, promoting target x | cp^sigma, px^L, xv^R | cx^sigma, xp^R, pv^L | K_1=J(C) union {p} union K_0 |

Again h=rt(H), v=rt(C), and

\[
\begin{aligned}
\delta_0&=\chi(cg^\sigma)+\chi(gp^L)+\chi(ph^R)
          -\chi(cp^\sigma)-\chi(pg^R)-\chi(gh^L),\\
\delta_1&=\chi(cp^\sigma)+\chi(xv^R)-\chi(xp^R)-\chi(pv^L).
\end{aligned}
\tag{1.4}
\]

The membership test for EACH K_i gives decreasing/neutral status exactly; the two nested labels are not assumed to have equal status.

### 1.4 LR, both original real rotations

\[
g(p(L,x(H,C)),R)
 \longrightarrow g(x(p(L,H),C),R)
 \longrightarrow x(p(L,H),g(C,R)).
\]

The FIRST external attachment is at actual parent g in its LEFT slot, even when the WHOLE double has no external c.

| Bit / actual operands | Deleted D | Inserted N | New SET label K |
| --- | --- | --- | --- |
| 0: left rotation at p, promoting target x under g | gp^L, px^R, xh^L | gx^L, xp^L, ph^R | K_0=J(L) union {p} union J(H) |
| 1: right rotation at g, promoting target x | cg^sigma, gx^L, xv^R | cx^sigma, xg^R, gv^L | K_1=J(C) union {g} union J(R) |

\[
\begin{aligned}
\delta_0&=\chi(gp^L)+\chi(xh^L)-\chi(xp^L)-\chi(ph^R),\\
\delta_1&=\chi(cg^\sigma)+\chi(xv^R)-\chi(xg^R)-\chi(gv^L).
\end{aligned}
\tag{1.5}
\]

K_0,K_1 are disjoint S labels, on opposite sides of x. Each still needs its own actual SET-membership test.

### 1.5 RL, both original real rotations

\[
g(L,p(x(C,H),R))
 \longrightarrow g(L,x(C,p(H,R)))
 \longrightarrow x(g(L,C),p(H,R)).
\]

The FIRST external attachment is at actual parent g in its RIGHT slot.

| Bit / actual operands | Deleted D | Inserted N | New SET label K |
| --- | --- | --- | --- |
| 0: right rotation at p, promoting target x under g | gp^R, px^L, xh^R | gx^R, xp^R, ph^L | K_0=J(H) union {p} union J(R) |
| 1: left rotation at g, promoting target x | cg^sigma, gx^R, xv^L | cx^sigma, xg^L, gv^R | K_1=J(L) union {g} union J(C) |

\[
\begin{aligned}
\delta_0&=\chi(gp^R)+\chi(xh^R)-\chi(xp^R)-\chi(ph^L),\\
\delta_1&=\chi(cg^\sigma)+\chi(xv^L)-\chi(xg^L)-\chi(gv^R).
\end{aligned}
\tag{1.6}
\]

These two K labels are disjoint as well. Neither disjointness nor nesting permits inventing an edge match with A.

### 1.6 Terminal zig, both orientations

A terminal zig occurs at the GLOBAL B root, so c is absent.

| Orientation and literal transition | Deleted D | Inserted N | Exact Delta Phi_0 | SET status |
| --- | --- | --- | --- | --- |
| Left: g(L,x(H,R)) -> x(g(L,H),R) | gx^R, xh^L | xg^L, gh^R | chi(xh^L)-chi(xg^L)-chi(gh^R) | K=J(L) union {g} union J(H)=S_<x, common in A; decreasing |
| Right: g(x(L,H),R) -> x(L,g(H,R)) | gx^L, xh^R | xg^R, gh^L | chi(xh^R)-chi(xg^R)-chi(gh^L) | K=J(H) union {g} union J(R)=S_>x, common in A; decreasing |

The incoming edge to x is not shared, hence its zero term is omitted from the delta column. Empty H omits its two attachments. A virtual companion creates neither an edge nor another B rotation/demand.

All tables use real physical parent-child edges and full hanging subtrees. They are universal literal identities, not samples of trees or freely assigned edge indicators.

## 2. Full-access accumulation

Let

\[
C_t(T)=|E(A_t)\cap E(T)|
\]

be shorthand for an actual shared-edge COUNT with A_t fixed; it does not replace or change the capacity. Since every physical B tree has |X|-1 edges,

\[
\Delta_{B,t}\Phi_0
  =\sum_{\rho\text{ in actual B phase}}\bigl[\chi(D_\rho)-\chi(N_\rho)\bigr]
  =C_t(B_{t-1})-C_t(B_t).
\tag{2.1}
\]

An edge inserted and later deleted in that same access cancels because its chi is evaluated against the SAME A_t. All intermediate roots, parent attachments and transported subtrees remain in the sum.

Thus the quantities to test are EXACTLY

\[
h_t^{(0)}=b_{0,t}+C_t(B_{t-1})-C_t(B_t),
\qquad
h_t^{(\mathrm{int})}=u_t+C_t(B_{t-1})-C_t(B_t).
\tag{2.2}
\]

For a nontrivial B splay k_t=1, so the proposed bounds are h<=beta d_t+gamma. On a root-repeat KEEP every B count and B difference is zero, and on DELETE the B phase is an identity. These degenerate accesses cannot provide a violation with a fabricated zero denominator.

The tests below evaluate (2.1) on actual COMPLETE B recurrences. No assertion about one neutral double is substituted for the full-access sum.


## 3. The complete source families and their literal B recurrences

### 3.1 W_(p,q) and H_(p,q), without an extracted access

Let p,q be positive integers and

\[
N=2^{p+1}(q+1)+1,\quad x_j=N+1-2^j,\quad
m=x_p,\quad n_j=(N-1)/2^{j+1}.
\tag{3.1}
\]

Start A=B at the complete physical right vine V+(1,N), prefix EMPTY, on X=[N].

The original amplified W_(p,q) word is:

1. DELETE 2,...,N.
2. Access EVERY integer k=N,N-1,...,m. KEEP precisely at x_0,...,x_p, DELETE elsewhere.
3. KEEP 1,...,N.
4. KEEP N-1,...,1.

Its length is 3N+2^p-2. H_(p,q) changes line 2 to descend ALL THE WAY to 1, with the same KEEP targets and DELETE at every other integer. Its length is 4N-2. These are the two already specified source families, not modifications of any archived word.

Every B history at its critical KEEPs is identical in the two families. Extra DELETEs freeze B. Both full scans are INSIDE each period. A complete increasing sweep produces the full physical left vine from any complete BST; the following decreasing sweep returns the full right vine. Therefore both A and B return EXACTLY to their common complete labelled starting tree. Every physical key is KEEP-visited, so the ORIGINAL M=S=X=[N], with no contraction or suppressed hanger.

At critical access x_j, in BOTH families the actual post-A tree is

\[
A_{x_j}=x_j(V^-(1,x_j-1),V^+(x_j+1,N)).
\tag{3.2}
\]

Thus every edge-presence test has the exact physical formula

\[
\chi_{x_j}(a,b,s)=1
\Longleftrightarrow
\begin{cases}
s=\mathrm{LEFT},\ b=a-1,\ 2\le a\le x_j; \text{ or}\\
s=\mathrm{RIGHT},\ b=a+1,\ x_j\le a<N.
\end{cases}
\tag{3.3}
\]

This specifies ONE actual complete BST, not independently selectable indicators.

### 3.2 Full B state, with all physical perfect blocks

Let P_1(c)=c and

\[
P_{h+1}(c)=c(P_h(c-2^{h-1}),P_h(c+2^{h-1})).
\]

After critical KEEP x_j, write

\[
B_j=x_j(C^{(j)}_0,H_j),
\]

\[
\begin{aligned}
r_i&=2+2^{j+1}i,\quad i=0,\ldots,n_j-1,\\
C^{(j)}_i&=r_i(T_i,C^{(j)}_{i+1}),\\
T_0&=1,\qquad T_i=P_{j+1}(r_i-2^j)\quad(i\ge1),\\
C^{(j)}_{n_j}&=R_j.
\end{aligned}
\tag{3.4}
\]

R_0=H_0=empty, and for j>=1,

\[
R_j=P_j(N+1-3\cdot2^{j-1}),\qquad
H_j=P_j(N+1-2^{j-1}).
\tag{3.5}
\]

Every vertex of these blocks is a physical key. The left part contains exactly keys 1,...,x_j-1; H_j contains x_j+1,...,N. The initial maximum access follows the literal full right vine and has n_0 RR doubles. For j>=1, the path begins LEFT from x_(j-1), then follows n_(j-1)=2n_j actual right-spine vertices to x_j. There are n_j-1 RR doubles followed by ONE LR, and no terminal zig.

RR merges the two actual perfect left blocks by the literal Section 1.2 transformation; the final LR gives H_j. This proves (3.4) recursively with the full outer leaf, right remainder and right subtree retained. It is the inherited complete recurrence, not an infinite-chain approximation.

### 3.3 Neutrality and COMPLETE-window membership

At j=0 all but the last RR are fully neutral; the last RR has two decreasing bits. Their whole frames end at N and hence are outside the interior class. Therefore

\[
b_{0,t_0}=n_0-1,\qquad u_{t_0}=0,\qquad d_{t_0}=2.
\tag{3.6}
\]

For j>=1, RR double k, 1<=k<=n_j-1, has WHOLE frame

\[
F_{j,k}=
[N+2-2^{j+1}(k+1),\,N-2^{j-1}].
\tag{3.7}
\]

Its lower endpoint is at least 3, and its upper endpoint is below N. Its created labels are

\[
[a,a+2^{j+1}-2],\qquad[a,x_j-1],
\quad a=N+2-2^{j+1}(k+1).
\tag{3.8}
\]

Both exclude 1,N and are absent from (3.2). The old lost labels contain the actual root x_j. Thus BOTH real bits are neutral. The final LR creates the full left/right S sides of x_j, both common in A; its two bits decrease.

Full-window A absence is proved on the ENTIRE source, not just at (3.2):

* In H_(p,q), every A real rotation is an adjacent zig and every A tree is a two-vine tree. Its proper physical labels are prefixes starting at 1 or suffixes ending at N. Every frame (3.7) is absent at every snapshot of the full period.
* In W_(p,q), preparation, critical descents (including all DELETEs) and reverse restoration have the same two-vine property. At the beginning of the full forward reset, put v=N-2^(j-1), the upper endpoint of (3.7). Since v>=m, vertex v is an actual ancestor of N in A's right vine. A splay to a target <=v preserves that ancestry at EVERY real rotation: only promotion of a key >v across v could remove N from v. This holds through KEEP v. At that access's end v is root and therefore an ancestor of 1. All later targets >=v preserve v's ancestry of 1 by the reflected argument. A label containing v and excluding BOTH 1,N is therefore absent at EVERY reset snapshot as well.

This global absence contains each original COMPLETE window (kappa_d,t_d^A], irrespective of its actual cyclic run placement. RG-01 supplies the original preceding creation/removal records; no window is shortened. Thus ALL n_j-1 neutral RR doubles, not only the selected K_(p,q) columns, belong to the original interior always-A-absent class:

\[
\boxed{b_{0,t_j}=u_{t_j}=n_j-1,\quad d_{t_j}=2,\quad k_{t_j}=1
       \quad(j\ge1).}
\tag{3.9}
\]

The critical operation IDs in BOTH words are t_j=N-1+2^j. No original occurrence ID is changed.

## 4. Exact full-access edge accumulation in W_(p,q) and H_(p,q)

A perfect P_h has zero adjacent left/right edges for h=1, and exactly 2^(h-2) of EACH orientation for h>=2. Only the bottom internal parents have consecutive physical-key children; every higher edge jumps at least two. By (3.3), below x_j only LEFT adjacent edges are shared, while above it only RIGHT adjacent edges are shared.

Counting these edges in the FULL decomposition (3.4)–(3.5) gives:

| Critical row | Shared BEFORE with the fixed post-A A_(x_j) | Shared AFTER with that SAME A_(x_j) | Exact Delta_(B,t_j) Phi_0 |
| --- | ---: | ---: | ---: |
| j=0 | 0 | n_0 | -n_0 |
| j=1 | 2n_1 | n_1+1 | n_1-1 |
| j=2, if present | 2n_2+2 | 2n_2+1 | +1 |
| j>=3 | 1+2^(j-1)n_j | 1+2^(j-1)n_j | 0 |

Here is the boundary audit behind the table.

* At row 0, the old B vine has only RIGHT edges, while A_N has only LEFT edges. Afterward the n_0 even-root-to-odd-leaf LEFT edges are shared.
* At row 1, BEFORE there are 2n_1 consecutive LEFT attachments. AFTER, root 2 contributes its left edge to 1, each of the n_1-1 physical P_2 blocks contributes one adjacent LEFT edge, and x_1->N contributes one adjacent RIGHT edge. The net change is +(n_1-1), not a matching decrease.
* At row 2, BEFORE the n_1-1=2n_2-1 P_2 blocks contribute that many LEFT edges, root 2 contributes one, and the two one-key high remainders give two adjacent RIGHT attachments. AFTER, the n_2-1 P_3 blocks contribute 2(n_2-1) LEFT edges, root 2 contributes one, R_2 contributes one LEFT edge, and H_2 one RIGHT edge.
* For j>=3, BEFORE the 2n_j-1 P_j blocks contribute (2n_j-1)2^(j-2) LEFT edges, root 2 one, and R_(j-1),H_(j-1) together 2^(j-2) RIGHT edges. AFTER, the n_j-1 P_(j+1) blocks contribute (n_j-1)2^(j-1) LEFT edges, root 2 one, and R_j,H_j together 2^(j-1) appropriately oriented edges. The totals agree.
* All remaining chain and boundary attachments jump more than one physical key, or have the wrong side of the fixed A root and orientation. They are not shared. They are still actual edges of B, not discarded vertices.

Combining all counts, the COMPLETE access vectors are

| Row | b_(0,t) | u_t | Delta_B Phi_0 | d_t | k_t | h^(0) | h^(int) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | n_0-1 | 0 | -n_0 | 2 | 1 | -1 | -n_0 |
| 1 | n_1-1 | n_1-1 | n_1-1 | 2 | 1 | 2(n_1-1) | 2(n_1-1) |
| 2 | n_2-1 | n_2-1 | +1 | 2 | 1 | n_2 | n_2 |
| j>=3 | n_j-1 | n_j-1 | 0 | 2 | 1 | n_j-1 | n_j-1 |

Thus the initial maximum access really does consume enough edge disagreement, while its later neutral waves need not do so.

## 5. A complete primitive-by-primitive parametric refutation

### 5.1 Freeze p=1, leave q arbitrary

Take EITHER full admissible source W_(1,q) or H_(1,q). Then

\[
N=4q+5,\quad x=N-1=4q+4,\quad t=N+1.
\]

At this original KEEP x,

\[
A=x(V^-(1,x-1),N),\qquad B_{\rm before}=B_0.
\]

B has exactly q neutral RR doubles followed by one decreasing LR double. The source recurrence, all physical keys, all original preparations and both full closing sweeps remain present.

For neutral RR k=1,...,q the actual operands and attachments are

\[
g=x-4k,\quad y=g+2,\quad c=g-2,\quad \sigma=\mathrm{RIGHT},
\]

\[
L=(g-1),\quad H=(g+1),\quad
\mathrm{rt}(C)=
\begin{cases}x-1,&k=1,\\g+6,&k\ge2.\end{cases}
\tag{5.1}
\]

Here y is the physical parent, filling the role named p in Section 1; the family parameter p remains fixed to 1. Target x has empty right subtree within its frame. For k>=2, C is the full left subtree accumulated by preceding doubles, NOT just its displayed root.

Evaluating EVERY affected edge of Section 1.2 by the actual BST formula (3.3):

| Actual rotation | Shared deleted edges | Shared inserted edges | Delta Phi_0 | Original SET class |
| --- | --- | --- | ---: | --- |
| RR k, bit 0 | ONLY (y,g+1,LEFT) | None | +1 | Neutral |
| RR k=1, bit 1 | ONLY (x,x-1,LEFT) | None | +1 | Neutral |
| RR k>=2, bit 1 | None | None | 0 | Neutral |
| Final LR, bit 0 | None | None | 0 | Decreasing |
| Final LR, bit 1 | None | ONLY (x,N,RIGHT) | -1 | Decreasing |

All other deleted/inserted edges in those rows are exactly the previously listed table edges; each has chi=0 in (3.3).

For the final LR the literal frame is N(2(1,x(C,empty)),empty), with rt(C)=6. Its first rotation creates [1,x-1], common in A, and its second creates {N}, also common. Neither creates a second neutral demand.

The q neutral doubles therefore contribute (q+1) to the SUM of the physical-edge changes, and the final LR contributes -1. The FULL B access has

\[
\boxed{b_{0,t}=q,\quad \Delta_{B,t}\Phi_0=q,\quad d_t=2,\quad k_t=1.}
\tag{5.2}
\]

This is the sum over the complete access, not a one-double estimate.

### 5.2 Actual run IDs and the weak membership check

For neutral double k the original whole frame is

\[
F_k=[x-4k-1,x],\quad k=1,\ldots,q.
\]

It excludes BOTH carrier extremes 1,N. Its actual creator and current-run removal are

\[
\Gamma_k=B(N,2k+1,1),
\]

\[
\sigma_k=
\begin{cases}
B(N+1,k+1,1),&k<q,\\
B(N+1,q+1,0),&k=q.
\end{cases}
\tag{5.3}
\]

Before KEEP N these labels are absent from the full right vine. During KEEP N only the stated second outputs create them; first outputs are singletons. After their current removal they are not recreated in the forward scan: each contains x, which remains an ancestor of N through KEEP x and then an ancestor of 1. Reverse-vine states also exclude them. Thus each has exactly one B run per period, and kappa_k is the PREVIOUS cyclic occurrence of sigma_k.

By Section 3.3, A is absent for every F_k at every snapshot of the FULL source period, including both closing sweeps. In H this follows from its literal two-vine states; in W it includes the full reset ancestor argument. Hence this absence holds on the actual complete window

\[
\Pi_k=(\text{previous cyclic }\sigma_k,\ t^A].
\]

Both real bits are neutral by the primitive table. Therefore the weak count is the exact FULL count

\[
\boxed{u_t=q,}
\tag{5.4}
\]

not merely an unverified local or selected interior subset.

### 5.3 Separate existential refutations

STRONG: for every q>=1, (5.2) would require

\[
2q\le2\beta+\gamma.
\]

No finite absolute beta,gamma satisfy this as q grows.

WEAK: the independently verified full-window equality (5.4) gives the SAME requirement

\[
u_t+\Delta_{B,t}\Phi_0=2q\le2\beta+\gamma.
\]

This refutes the weak existential assertion separately. It is not inferred solely from failure of the strong assertion.

Equivalently, on either COMPLETE source family,

\[
\boxed{\frac{u_t+\Delta_{B,t}\Phi_0}{d_t+k_t}
             =\frac{2q}{3}\longrightarrow\infty.}
\tag{5.5}
\]

The denominator is exactly three, never zero. For any proposed finite coefficients choose an integer q>beta+gamma/2. The complete legal period and its original operation t=N+1 then violate that version.

The primitive failure mechanism is explicit: many neutral RR first rotations DELETE physical A-shared consecutive LEFT edges and replace them with nonshared edges. Phi_0 INCREASES instead of consuming the neutral bill. SET neutrality of the new subtree labels does not imply physical-edge cancellation.


## 6. Saved actual 97-key source: separate finite control

The saved source is NOT W_(3,5). Its exact 293-operation word is

    DELETE 2,...,97;          t=1,...,96
    KEEP 97,96,95,94;         t=97,...,100
    KEEP 1,...,97;            t=101,...,197
    KEEP 96,...,1.            t=198,...,293

It starts at A=B=V+(1,97), with empty prefix and original X=S=M=[97]. The closing sweeps return BOTH full labelled trees to that vine. At critical target x, post-A is the actual two-vine A_x of (3.2).

The complete physical B states, including the irregular outer block, are:

    after 97:
      97(C_1,empty),
      C_i=(2i)(2i-1,C_(i+1)), i=1,...,48; C_49=empty.

    after 96:
      96(D_0,97),
      D_i=(4i+2)(T_i,D_(i+1)), i=0,...,23;
      T_0=1; T_i=P_2(4i) for i>=1; D_24=95.

    after 95:
      95(E_0,96(empty,97)),
      E_i=(8i+6)(L_i,E_(i+1)), i=0,...,11;
      L_0=2(1,4(3,5)); L_i=P_3(8i+2) for i>=1;
      E_12=empty.

    after 94:
      94(Q_0,95(empty,96(empty,97))),
      Q_i=(16i+6)(R_i,Q_(i+1)), i=0,...,5;
      R_0=2(1,4(3,5)); R_i=P_4(16i-2) for i>=1;
      Q_6=P_3(90).

These are the saved literal recurrences, not the dyadic-target formulas substituted at the same N.

| Original access | Actual B path pattern | b_(0,t) | u_t | Shared before with SAME post-A | Shared after | Delta_B Phi_0 | d_t | k_t |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| t=97, KEEP97 | 48 RR | 47 | 0 | 0 | 48 | -48 | 2 | 1 |
| t=98, KEEP96 | 23 RR, then LR | 23 | 23 | 48 | 25 | +23 | 2 | 1 |
| t=99, KEEP95 | 12 RR, then right zig | 11 | 11 | 25 | 26 | -1 | 3 | 1 |
| t=100, KEEP94 | 5 RR, then LR | 5 | 5 | 26 | 27 | -1 | 2 | 1 |

At t=99 the last RR is NOT neutral: it creates the common prefix and full left side. Together with the decreasing terminal right zig it gives d_t=3. Calling all twelve RR neutral would be a false classification.

The shared-edge counts follow from actual adjacent physical edges in the displayed blocks:

* At 96, before=48; after=1+23+1=25.
* At 95, before=1+23+1=25; after=2 outer-block LEFT edges + 22 P_3 LEFT edges + 2 right-tail edges=26.
* At 94, before=2+22+2=26; after=2 outer-block LEFT edges + 20 P_4 LEFT edges + 2 remainder P_3 LEFT edges + 3 right-tail edges=27.

The neutral frames at 98,99,100 have lower endpoints respectively

    95-4k, k=1,...,23;
    95-8k, k=1,...,11;
    87-16k, k=1,...,5,

and upper endpoints 96,95,94. All lower endpoints exceed 1. Their created labels exclude both extremes, so the RR bits are neutral at the actual post-A trees. At forward-reset start A has root 94 and its right vine; each of those upper endpoints is an ancestor of 97. The complete reset argument of Section 3.3 proves A absence at EVERY source snapshot. Thus all 39 later critical neutral doubles have complete-window interior membership, not just the fifteen selected graph-witness demands.

The corresponding h^(0) values are -1,46,10,4; the h^(int) values are -48,46,10,4. This finite source constrains proposed coefficients but BY ITSELF does not refute existence of all finite beta,gamma. Its access t=98 is the literal finite q=23 instance of the Section 5 B-transition geometry; the complete source histories are still kept distinct.

## 7. Cheap warmed-up repeat: original carrier and all physical edges

### 7.1 Source, reaching prefix and COMPLETE return

Use the same p,q,N,x_j,m and full B_p of Section 3. Reach

    A=V-(1,N), B=B_p

by the already specified legal prefix:

    DELETE 2,...,N;
    descend N,...,m, KEEP exactly at x_0,...,x_p;
    DELETE m+1,...,N.

The ORIGINAL repeated period is

    descend EVERY k=N,N-1,...,m,
       KEEP exactly at x_0,...,x_p and DELETE otherwise;
    DELETE m+1,...,N.

It has 2^(p+1)-1 operations and EXACT A cost 2(2^p-1). Its reaching prefix is excluded as permitted; no demand from that prefix is counted again in the period.

The full B_p decomposes as the actual RIGHT spine

    x_p -> x_(p-1) -> ... -> x_0,

with the entire physical low subtree C^(p)_0 left of x_p, and gap R_i left of x_i, i=0,...,p-1, where R_0 is empty and R_i is the full perfect tree in (3.5). In particular

    H_i=x_(i-1)(R_(i-1),H_(i-1)).

All these physical gap trees remain intact in the repeat. The KEEP paths consist of the displayed marked vertices linked by ACTUAL physical parent-child edges, not shortcuts. The decreasing scan of all p+1 such vertices returns their right-spine shape. In that shape every intact gap has its unique inorder attachment, and the low subtree remains left of x_p. Hence the COMPLETE physical B tree returns to B_p. A also returns to its full left vine through adjacent physical zigs.

Here the genuine support is M={x_p,...,x_0}. It is itself the union of root-to-M paths at the starting B_p, so the ORIGINAL canonical carrier S=C_M(B_p) is EXACTLY M, by the closed-core specification. This is not a convenient replacement of the original carrier. All other physical vertices remain S-free hangers, still included in Phi_0. The source-model reference for C_M is the union-of-original-paths statement in CD5_PROOF Section 2.

A is a full physical two-vine at EVERY snapshot of this period, including DELETEs at unmarked keys. Its J_S labels are therefore only S prefixes/suffixes (with duplicates suppressed). Every S interval excluding the two S extremes is A-absent throughout the COMPLETE period, hence on every original Pi window.

### 7.2 Full-access SET counts in this repeat

For the first KEEP x_0=N, the ACTUAL B depth is p.

| p | b_(0,t_0) | u_(t_0) | d_(t_0) | k_(t_0) |
| --- | ---: | ---: | ---: | ---: |
| even, p>=2 | p/2-1 | 0 | 2 | 1 |
| odd, p>=1 | (p-1)/2 | 0 | 1 | 1 |

For even p the final global RR has two decreasing bits; for odd p all RR doubles are neutral and the final left zig decreases. Every whole frame contains max S=x_0, so u_(t_0)=0 regardless of neutrality.

For each later KEEP x_j, j>=1, let h_j be its ACTUAL physical B depth. The already accessed larger support keys form a right suffix. The next target is the maximum SUPPORT key of the old root's left subtree, so its actual path is one LEFT edge followed by RIGHT edges. There is no S-free vertex on that path.

| Later actual depth h_j | b_(0,t_j) | u_(t_j) | d_(t_j) | k_(t_j) |
| --- | ---: | ---: | ---: | ---: |
| 1 | 0 | 0 | 1 | 1 |
| even >=2 | h_j/2-1 | h_j/2-1 | 2 | 1 |
| odd >=3 | (h_j-1)/2-1 | (h_j-1)/2-1 | 3 | 1 |

For even depth, the final LR creates the two full S sides, and all earlier RR doubles are neutral. For odd depth >=3 the outermost RR creates a common S prefix and full left side, followed by one decreasing terminal right zig. Other RR outputs exclude both S extremes and are neutral. A neutral whole frame is then interior; the global A-absence just proved establishes its COMPLETE-window membership, so u=b_0 in EVERY later row.

These formulas give exact counts, not population-asymptotic bounds. For completeness, the actual h_j can be generated by the following literal full-subtree recurrence, without a replay or contracted source.

Write the current root as g, its right subtree as V, and its path to the next target as

    g( a_0(L_0,a_1(L_1,...,a_(ell-1)(L_(ell-1),H)...)), V ).

Here ell=h_j, all a_i are actual path vertices, every L_i is its COMPLETE physical left subtree, and H is the complete S-free gap right of the target. No node of L_i,H,V is removed.

If ell=2s+1, initialize C=L_(2s), and for i=s-1,...,0 replace

    C <- a_(2i+1)(a_(2i)(L_(2i),L_(2i+1)),C).

Then the full resulting tree is

    a_(2s)(C,g(H,V)).

If ell=2s, initialize C=L_(2s-1), and for i=s-2,...,0 replace

    C <- a_(2i+2)(a_(2i+1)(L_(2i+1),L_(2i+2)),C).

The full resulting tree is

    a_(2s-1)(a_0(L_0,C),g(H,V)).

These are repeated RR identities followed by the actual terminal zig or final LR. They specify the next entire physical left subtree and hence its actual next path length. Empty loop ranges are empty; ell=1 is one right zig. This is an exact symbolic recurrence retaining every physical hanger.

In particular the first maximum splay leaves a right spine of ceil(p/2) vertices in its left subtree. Therefore

\[
h_1=\lceil p/2\rceil.
\tag{7.1}
\]

This counts actual physical path edges, as the next target is the last vertex on that spine.

### 7.3 Exact physical-edge deltas in the warmed repeat

Use the SAME complete physical A_(x_j) as in (3.2), not a tree obtained by making adjacent support keys physically consecutive.

All internal edges of every intact low/gap tree cancel in the B-phase difference. The low subtree is permanently attached left of minimum-support x_p, at physical root 2, which is not adjacent to x_p. For a gap R_i with i>=2, its physical root is at distance 2^(i-1)>=2 from either bordering support key. Such boundary edges cannot be shared with (3.3), whichever bordering key is its parent.

The only changing boundary candidates that can be shared are:

1. The physical adjacent support pair x_1=N-1, x_0=N.
2. If p>=2, the SINGLE physical gap vertex N-2 between x_2=N-3 and x_1=N-1.

Every other physical edge is either unchanged or a nonadjacent boundary edge.

Before the first maximum access, the singleton gap is attached LEFT of N-1 and is shared with A_N. That first splay puts it RIGHT of N-3, unshared with A_N. A final shared edge N->N-1 is present only for p=1 or p=2; for p>=3 N's final left child is a smaller support vertex. Thus

\[
\Delta_{B,t_0}\Phi_0=
\begin{cases}
-1,&p=1,\\
0,&p=2,\\
+1,&p\ge3.
\end{cases}
\tag{7.2}
\]

At the second KEEP x_1=N-1, the singleton gap (if any) remains right of N-3, unshared with the fixed A_(N-1) both before and after. The final new physical edge (N-1,N,RIGHT) becomes shared, and no other changing edge becomes shared or loses sharing. Hence

\[
\boxed{\Delta_{B,t_1}\Phi_0=-1\quad\text{for all }p\ge1.}
\tag{7.3}
\]

At KEEP x_2=N-3, when present, that gap moves from RIGHT of N-3, shared with A_(N-3), to LEFT of N-1, unshared. The edge (N-1,N,RIGHT) stays shared. Thus Delta_(B,t_2)Phi_0=+1.

At every later KEEP x_j, j>=3, both these high-key structures belong to the rigid already visited suffix and keep the same sharing status. All other changing boundaries are nonadjacent, so Delta_(B,t_j)Phi_0=0.

| Warmed access | Exact Delta_B Phi_0 |
| --- | ---: |
| j=0 | -1 if p=1; 0 if p=2; +1 if p>=3 |
| j=1 | -1 |
| j=2, if present | +1 |
| j>=3 | 0 |

This is PHYSICAL-edge counting with the complete low/gap populations retained. Replacing S-adjacent keys by consecutive physical keys would give different edge matches and is not permitted.

### 7.4 Independent parametric failures inside the cheap repeat

Fix q=1 if desired and take p=4r, r>=1. At the first KEEP,

    b_0=2r-1, u=0, Delta_B Phi_0=+1, d=2, k=1.

Its STRONG left side is 2r, unbounded with bounded right side. This first access alone does not refute the weak law.

At the SECOND KEEP, (7.1) gives the actual depth h_1=2r. Therefore

\[
\boxed{b_{0,t}=u_t=r-1,\quad
       \Delta_{B,t}\Phi_0=-1,\quad d_t=2,\quad k_t=1.}
\tag{7.4}
\]

The original period positions are t_0=1, t_1=2; in general the KEEP x_j is at position 2^j. A historical absolute prefix offset, if used, is retained. These are the existing period's positions, not newly borrowed events.

The weak AND strong left sides at the second access equal r-2. The exact weak ratio

\[
\frac{u_t+\Delta_{B,t}\Phi_0}{d_t+k_t}
   =\frac{r-2}{3}\longrightarrow\infty
\tag{7.5}
\]

is a SECOND source-valid refutation of both versions. Global A absence relative to this source's ORIGINAL carrier, rather than reuse of the old full-support frames, justifies u_t.

For the p=1 warmed control there are only two actual terminal zigs: both have b_0=u=0, Delta_B Phi_0=-1, d=k=1. Their counts do not depend on q. The first-wave q-sized low-key workload is not regenerated by that two-key repeat. For growing p, the new higher-support neutral work in (7.4) is real, but remains compatible with the full period's actual A cost 2(2^p-1).


## 8. Exact gate decision and RG-03 transfer packet

### 8.1 Gate status, with the quantifiers settled

**STRONG VERSION: FAIL — source-valid parametric refutation.**

Section 5 gives b_0+Delta_B Phi_0=2q with d=2,k=1 for every integer q>=1. Section 7.4 gives an independent strong failure in the warmed repeat.

**WEAK VERSION: FAIL — separately verified source-valid parametric refutation.**

Section 5 verifies ALL complete cyclic windows and gives u+Delta_B Phi_0=2q, again d=2,k=1. Section 7.4 independently gives the unbounded weak value r-2, with the warmed source's own canonical carrier and full physical edge set.

Thus the overall **RG-02 gate is FAIL for BOTH versions**. It is not BLOCKED, and no universal beta,gamma certificate exists for either exact proposed law. Allowing different finite constants for the two laws does not help.

There is no first unsupported source implication left in these refutations. The FALSE implication tested by RG-02 is that an entire neutral B burst must either consume enough of THIS physical-edge disagreement or incur proportionally many original Psi decreases. The actual first descendant wave instead increases Phi_0 linearly.

### 8.2 Failure configurations transferred to RG-03

This section is the durable RG-03 INPUT/HANDOFF packet. It preserves exact configurations and their failure mechanisms; it does not begin an RG-03 repair or change the capacity.

| Packet | Actual complete-source configuration and operation | Exact vector (b_0,u,Delta_B Phi_0,d,k) | Consequence |
| --- | --- | --- | --- |
| F1 | W_(1,q) OR H_(1,q), N=4q+5, original KEEP N-1 at t=N+1; full A/B states and bit-level shared edges in Section 5 | (q,q,q,2,1) | Strong and weak LHS 2q; ratio 2q/3 unbounded |
| F2 | W_(p,q) OR H_(p,q), p>=2, critical row 2, t=N+3 | (n_2-1,n_2-1,1,2,1) | Strong and weak LHS n_2; unbounded with q |
| F3 | Same full sources, any fixed row j>=3 with p>=j, t=N-1+2^j | (n_j-1,n_j-1,0,2,1) | Strong and weak LHS n_j-1; unbounded with q |
| F4 | Warmed period with p=4r, first KEEP N, period position 1 | (2r-1,0,1,2,1) | Strong LHS 2r unbounded; this row alone does NOT refute weak |
| F5 | Warmed period with p=4r, second KEEP N-1, period position 2 | (r-1,r-1,-1,2,1) | Strong and weak LHS r-2 unbounded; complete run certificate below |
| C97 | Saved 97-key source, exact original operations 97–100 | Full finite vectors in Section 6 | Finite control only; not an existential refutation alone |

For F1 retain original whole-frame histories (5.3), not just the q neutral bit patterns. Their previous cyclic removal, exact creators and current removals are part of the packet.

For F5 there is also an explicit original run certificate. Let v_0<...<v_p be the ACTUAL support keys, so v_i=x_(p-i), v_p=N, v_(p-1)=N-1, and p=4r. For k=1,...,r-1 the second access's neutral double k has whole S label

\[
F_k=\{v_{p-2-4k},v_{p-1-4k},\ldots,v_{p-1}\}.
\tag{8.1}
\]

The smallest lower support index is 2, so neither extreme v_0,v_p belongs to any F_k. Its creator in the FIRST access is

\[
\Gamma_k=B(t_0,2k+1,1).
\]

Its current removal in the SECOND access is

\[
\sigma_k=
\begin{cases}
B(t_1,k+1,1),&k<r-1,\\
B(t_1,r,0),&k=r-1.
\end{cases}
\tag{8.2}
\]

There are no such frames when r=1. These formulas refer to the warmed source's original operation positions, with any historical absolute offset preserved.

Initially the marked right vine has only S suffix labels, so F_k is absent. Only the displayed first-access second output creates it; first outputs are S singletons. After its second-access removal, v_(p-1) remains an ancestor of maximum N during ALL remaining lower-target KEEPs, so no F_k can be recreated. DELETEs freeze B. Thus the preceding kappa_k is exactly the previous cyclic sigma_k. The full period's A has only S-prefix/suffix labels, so F_k is absent throughout that ENTIRE window. This supplies actual full histories for F5, not an inference from local neutrality.

Handoff invariants to preserve:

* Phi_0 remains |E(B) minus E(A)| over ALL physical oriented edges.
* Psi neutrality is a SET-label condition, not an edge-match condition.
* F1 can lose one original A-shared LEFT edge at EACH neutral RR first bit.
* The additional first RR bit-1 loss and final LR gain are both retained; dropping either changes the exact full-access total.
* Warmed hangers are not physically deleted, made consecutive, or turned into path shortcuts.
* F1–F3 use S=X; F4–F5 use their original smaller canonical S=M. Mixing these supports would invalidate u.
* No original source access is independently closed; its entire period and actual reachability are given.
* No resource, historical owner, source operation, Gamma/kappa window or occurrence ID is changed.

No passing certificate is sent to RG-05. These exact failures are supplied to RG-03 ONLY as inputs in this report; no RG-03 analysis, alternative capacity, repair theorem or new source experiment is undertaken.

### 8.3 What the failure does NOT say

This FAIL rejects the TWO SPECIFIED local conservation laws for the FIXED Phi_0. It does not refute URCD, Universal Coarse-Double, a different source-derived argument, or a whole-period A-work comparison.

All preparations/restorations in W,H and the warmed period have their original real A costs. In particular H has A=4(N-1), and the warmed period has A=2(2^p-1). No argument here claims that their complete U_int/A ratios diverge.

The forward/reset accesses remain in each complete source and in the full-window tests. Their separate event vectors need not be enumerated to refute a law quantified over EVERY access: one original offending access suffices. No uncomputed reset-neutral count is silently declared zero.

## 9. Provenance and preservation

RG-01 was read in full, its PASS prerequisite checked, and its exact edge/event conventions retained. The named source words, full critical B recurrences, A invariants, original 97-key distinction and warmed-prefix/closure clauses were read from the existing local reports below.

| ID | Source | Exact use |
| --- | --- | --- |
| S1 | [RG-01 primitive accounting](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md:1>) | PASS prerequisite; exact physical edges, phase deltas, original event counts and complete-window definition. |
| S2 | [97-key audit and parametric W_(p,q) amplification](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md:1>) | Sections 3–5: complete saved 97-key source, literal full B recurrences, W word, neutrality and global A absence. New physical-edge counts are derived here. |
| S3 | [Modified H_(p,q) and cheap warmed repeat](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md:1>) | Section 8.2: H word and A invariant. Section 9.3: exact warmed source, reaching prefix, complete return and counted A work. |
| S4 | [Regeneration continuation](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md:1>) | Read-only context on regeneration versus counting; none of its partial work bounds is needed to refute the RG-02 laws. |
| S5 | [Saved original 97-key TF2 source certificate](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_STEP04_TF2_20261109/STEP04_TF2_BINARY_CERTIFICATION.md:1>) | Actual 293-operation source and original physical occurrence conventions; not silently replaced by dyadic W_(3,5). |
| S6 | [Original canonical closed-core definition](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/CD5_BASE01/CD5_PROOF.md:45>) | C_M is the union of original root-to-mark paths. Used to identify the warmed source's own S=M, without contracting physical hangers. |
| S7 | [Research rules](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md:1>) | Preserved scope, read-only historical artifacts, proof/refutation distinctions and symbolic evidence status. |
| S8 | [Maximal-core grammar](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/CONTINUATION_04/MAXIMAL_CORE_GRAMMAR.md:1>) | Static context only; no restricted maximal-core theorem is used as universal RG-02 coverage. |

Read-only SHA256 pins for the current input bytes:

| ID | SHA256 |
| --- | --- |
| S1 | f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa |
| S2 | 1c31d4b5d8c97771640e5235e2015a95b584753d42ada4987600d071d8466176 |
| S3 | 4cf67ae246987f211997e18a5efb5b6d37ab9afbf800777769bbd2f56de5d42a |
| S4 | 50e90e4471b1f794ba58f848f44522dc71ac74685ed9f81e09593cfb11e871d0 |
| S5 | 1a56e2f4eb3023642979fae4ca93f73e9ad794bb1d982c9de5a018fef8cdf0a7 |
| S6 | 6380c55270c8c52505e2726e27a8fee734cac9812f39271b608cc282b34e88be |
| S7 | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |
| S8 | 4f4cd296c353c6a30fd5b8ae100f79fd246907ff9848353c1cc37129817a7fa9 |

Workspace:

    C:\Users\Saif malik\OneDrive\Documents\Desktop\Temp\splay-multiscale-transfer-liquidity-k6c2
    Branch: coarse-double-branch
    HEAD: 6d532b2c795c0778f57d8023b23b5fedfc48b010

Only this new RG02_EDGE_CONSERVATION.md is written in DO_RESEARCH_REBOOT. RG-01, the source reports, programs, source periods, historical IDs, resource files, owners, Route 01/03/04 artifacts and Git state are preserved.

No source query, executable splay replay, generated-tree experiment, enumeration, solver, new capacity, proof-assistant or independent-verifier run, external search or subagent was used. Every shared-edge count is a symbolic derivation in an explicit complete labelled BST. Input hashes establish preservation, not independent or formal proof certification.

## 10. Final verdict

**RG-02: FAIL — BOTH STRONG AND WEAK VERSIONS ARE REFUTED.**

The main exact certificate is

\[
(b_{0,t},u_t,\Delta_{B,t}\Phi_0,d_t,k_t)=(q,q,q,2,1)
\]

on the COMPLETE original families W_(1,q) and H_(1,q), for arbitrary q>=1. Therefore either proposed law would force 2q<=2beta+gamma for every q. The weak count was verified on the complete cyclic windows independently of the strong failure.

The saved 97-key source is consistent with those exact physical-edge counts; it is not used alone as an existential refutation. The warmed source gives the independent full-window certificate (7.4)–(7.5) without reusing the initial low-key workload.

BEFORE: the candidate could fail by unconstrained indicator guesses or by overlooking full-access edge cancellation.
RESULT: all primitive orientations, actual post-A edge constraints, complete access accumulation and full original source windows were retained; the fixed candidate fails parametrically for both claims.
AFTER: no RG-05 certificate exists; the exact source configurations are recorded in the RG-03 handoff packet.
NET ADVANCEMENT: the precise edge-disagreement conservation candidate is decisively eliminated. URCD itself remains unrefuted.

**Stop point: this report. No subsequent gate is undertaken.**
