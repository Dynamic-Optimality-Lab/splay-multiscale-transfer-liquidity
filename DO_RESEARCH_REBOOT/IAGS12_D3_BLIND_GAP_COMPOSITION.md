# IAGS 1.2 — D3 blind-gap regeneration and global cost composition

Date: 2026-11-09, Asia/Karachi.

## Scope fixed before formalization

Execute D3 ONLY. P1, V1, P2, RG-05 and later gates are not executed. Only this isolated report is written. Current G0, D1, D2, RG04, original source specifications/rules, and the complete family descriptions were read from actual bytes.

First reconstruct the two inherited real-A maps and prove their JOINT disjointness, then freeze the unchanged blind-gap domain. The principal new mechanism to investigate is the FIRST actual B rotation modifying a gap's original physical path. If it decreases the ORIGINAL SET disagreement, its contribution can use the already proved global D_B cost identity only with an explicit all-cohort multiplicity.

The candidate smaller class is blind gaps with a decreasing first path modification. Success must give a universal numerical bound, nonempty full-source coverage and a precise complementary source predicate. Birth/survival/return identities alone do not count as quantitative progress.

The starting physical facts are literal rotations, disjoint path segments between consecutive cohort roots, and the original closed-source identity D_B=P_A-N_A<=R_A<=2A. This uses the EXISTING original SET accounting, not a new potential campaign or a conjectured payment matching. Joint use of the A budget must be explicit.

All source periods, historical reports, owners, IDs and resource caps remain read-only. New words below are symbolic source constructions, not modifications of saved source artifacts. No source-engine query, replay, experiment, solver, enumeration, external research, Git mutation or subagent is used. Verification is same-agent symbolic, not independent/formal certification.

## 1. D1/D2 proof-image disjointness audit

Let phi_1 be D1's fixed map on E_ctl: for an original consecutive cohort pair, choose the outer exposed output's first acquisition a(d), otherwise the inner exposed output's last loss b(d). Those events are ACTUAL SET changes during the output's live B history, with signs -1 and +1.

At any original snapshot there is at most one still-unhit chosen history with a given nonempty B label. One A rotation creates/loses at most one SET label. Common-label acquisition and loss cannot cancel in one A rotation: two simultaneously common candidate labels would violate physical B subtree compatibility, including the consecutive-S-key disjoint case. Thus all a images are distinct, all b images are distinct, and the two images have opposite signs. One chain vertex has only one lower and one upper incident pair, using its different a/b events. This reconstructs GLOBAL injectivity of phi_1, rather than assuming it.



For the sign assertion used above, a literal A left rotation u(L,p(H,R))->p(u(L,H),R) can SET-lose only C=lab_S(p(H,R)) and SET-create only D=lab_S(u(L,H)); the whole label C union D persists. Simultaneous actual loss/creation therefore requires C,D incomparable. If both were current B labels, overlapping incomparable sets would violate rooted-subtree laminarity. If disjoint, D lies left of C and their union is an S interval. The consecutive S endpoints a=max D,b=min C have a physical B LCA in S, by ancestor closure. Its key lies between a,b, so is a or b; its alleged B subtree must then contain the other endpoint, contradicting disjointness. Reflection proves the right-rotation case. Thus no lost common label can cancel a created common label in the same real A bit.

Live-history uniqueness also uses physical chronology: while a chosen label is unhit, its rooted B subtree is rigid. Another chosen birth of the same label would have to change that subtree using a target in it, which would already hit the older history. Different cyclic displays do not make two active copies of this same physical occurrence.


Let phi_2 be D2's fixed map on R_sep. Its chosen intermediate B label K is A-present during shared life, and absent at the common hit's post-A root. Choose its last actual SET loss. It has sign +1. If two pairs use the same loss, the lost label is the same current K. Their common hit is the next still-unperformed B phase inside K. They therefore belong to the SAME complete cohort, and K can strictly separate only ONE consecutive pair of that chain. This proves global injectivity of phi_2.

Now verify their CROSS-image intersection. A phi_1 acquisition has sign -1, so cannot equal phi_2. If a phi_1 loss b(d) equalled phi_2(rho), the one lost label would be BOTH the still-unhit chosen label J_d and the strict intermediate K of rho. The next B phase inside K is the first hit of d as well as rho's hit h. Thus d is a vertex of the SAME FULL C_h, strictly between rho's allegedly consecutive vertices. Contradiction.

Therefore, universally,

\[
\boxed{\operatorname{im}\phi_1\cap\operatorname{im}\phi_2=\varnothing.}
\tag{1.1}
\]

The argument uses original real A IDs and actual SET losses, not just two separate load-one bounds. It includes a loss inside h's A phase (its B phase is still upcoming), private duplicate representatives, and all cyclic seams. A causal lift never gives a second copy of an event. No historical g_1 owner or release allocation is changed.

## 2. Correct combined baseline and constants

The joint original real-event inventory gives

\[
\boxed{E_{\rm ctl}+R_{\rm sep}\le R_A=2A-V_A\le2A.}
\tag{2.1}
\]

Using the exact original partitions and G0,

    U_int=H+E_ctl+R_sep+R_rem, H<=A.

Consequently

\[
\boxed{U_{\rm int}\le A+R_A+R_{\rm rem}\le3A+R_{\rm rem},}
\quad
\boxed{Q_B\le9A+R_{\rm rem}.}
\tag{2.2}
\]

The last inequality imports the original Route 02/04 relation Q_B<=6A+U_int with its existing qualifications. Nothing is inferred from a standalone cardinality partition without the proved joint event injection.

A=0 implies U_int=0 by G0, so all residual counts vanish. The quantifiers remain every original finite reachable exactly paired-closed source, with arbitrary physical populations, support, helpers and hangers. This is a baseline with an unresolved term, not a universal coefficient.

## 3. Exact R_rem registry

Fix an ORIGINAL rho=(h,d_-,d_+) in R_rem. These are consecutive vertices of the COMPLETE first-hit cohort C_h, not of a filtered chain.

For each endpoint keep the original demand ID, chosen birth nu, physical root g, full physical subtree O, S label J, whole frame F, Gamma/kappa/Pi and A state. The chosen birth is bit 0 for RR/LL and bit 1 for LR/RL. The complete whole-frame U_int predicate is retained.

There is physical strict nesting O_- inside O_+, and J_- strictly inside J_+. Births satisfy nu_-<nu_+<h in original cyclic causal order. Both J labels stay A-absent on their OWN birth-to-first-hit histories. Every strict intermediate physical B rooted label remains A-absent on the SHARED interval from nu_+ just after birth to h's post-A/pre-B state.

At nu_+, A has its actual producer root outside J_+. At h's post-A endpoint its root x_h is in J_-. These facts do not prescribe a particular A parent or a common producer/token.

For the physical record retain:

| Field | Original data |
| --- | --- |
| Birth/survival | Actual nu_-/nu_+, full rooted shapes, every real incoming edge-run occurrence and transfer |
| Blind path | Actual g_+-to-g_- vertices and LEFT/RIGHT edges at nu_+ |
| A history | Every original A access and real bit, both physical LCA covers and SET changes |
| Consumption | Actual pre-B tree at h, x_h path, first path-modifying real B bit, all later deletions/recreations/label retirements |
| Return | Complete cyclic event word back to the identical pre-nu_+ full pair state, with original IDs counted once |

No new demand, artificial intermediate vertex or independently closed critical subword is introduced.

## 4. Type 0 and Type + physical paths

At B just after nu_+ define the UNIQUE physical ancestor path

    P_rho=(v_0=g_+,v_1,...,v_l=g_-), l>=1,

with actual edges e_j=(v_(j-1),v_j,LEFT/RIGHT). All v_j lie in S by ancestor closure. An intermediate vertex v_j, 0<j<l, has

\[
J_-\subsetneq K_j=\operatorname{lab}_S^B(v_j)\subsetneq J_+.
\tag{4.1}
\]

Strictness follows from the distinct S ancestor keys, not projected shortcut relations. These are complete physical rooted subtrees, with all their hangers.

O_+ is rigid throughout shared life, since earlier KEEP targets are outside J_+. Thus the whole internal path, all its edges, and these rooted physical subtrees remain UNCHANGED until h's B phase. Only the external incoming edge of O_+ may be middle-transferred. Internal incoming edges are not silently reissued.

Exactly two cases exist:

* Type 0: l=1, g_- is an actual physical child of g_+. There is NO intermediate K.
* Type +: l>=2; all actual K_j are absent from A at every shared-lifetime snapshot, by the unchanged R_rem predicate.

This is exhaustive and universal. The number of intermediate labels is not a payment or an A-cost bound.

## 5. Literal outer-output birth reconstruction

Use g=g_+, actual producer x, old parent p, and external c in slot sigma. H,C,L,R denote complete physical subtrees; h0=rt(H), c0=rt(C), with only genuinely empty edges omitted.

| Original double frame | Chosen birth | New outer output | How the older inner output is contained |
| --- | --- | --- | --- |
| RR: g(L,p(H,x(C,R))) | bit 0, left at g | g(L,H) | Entirely in unchanged L or transported H |
| LL: g(p(x(L,C),H),R) | bit 0, right at g | g(H,R) | Entirely in transported H or unchanged R |
| LR: g(p(L,x(C,H)),R) | bit 1, right at g | g(H,R) | Entirely in transported H or unchanged R |
| RL: g(L,p(x(C,H),R)) | bit 1, left at g | g(L,C) | Entirely in unchanged L or transported C |

It cannot straddle the new root and components: it was already a complete rooted subtree and the producer is outside it. The new enclosing S root g already existed. Its B subtree changes from one containing x to one excluding x, so this chosen output is genuinely newly born, not merely renamed. Its older inner output is not internally modified.

| Birth bit | Deleted physical edges | Inserted physical edges |
| --- | --- | --- |
| RR 0 | (c,g,sigma); (g,p,RIGHT); (p,h0,LEFT) | (c,p,sigma); (p,g,LEFT); (g,h0,RIGHT) |
| LL 0 | (c,g,sigma); (g,p,LEFT); (p,h0,RIGHT) | (c,p,sigma); (p,g,RIGHT); (g,h0,LEFT) |
| LR 1 | (c,g,sigma); (g,x,LEFT); (x,h0,RIGHT) | (c,x,sigma); (x,g,RIGHT); (g,h0,LEFT) |
| RL 1 | (c,g,sigma); (g,x,RIGHT); (x,c0,LEFT) | (c,x,sigma); (x,g,LEFT); (g,c0,RIGHT) |

For LR, bit 0 first changes
D={(g,p,LEFT),(p,x,RIGHT),(x,c0,LEFT)},
N={(g,x,LEFT),(x,p,LEFT),(p,c0,RIGHT)}.
For RL, bit 0 first changes
D={(g,p,RIGHT),(p,x,LEFT),(x,h0,RIGHT)},
N={(g,x,RIGHT),(x,p,RIGHT),(p,h0,LEFT)}.
SS's subsequent target promotion preserves the newly born g output.

All other internal/outer edges persist in the respective bit. If the inner output is the middle component itself its incoming edge is reattached; if deeper, its own incoming edge is unchanged. A Type 0 edge can therefore already exist before nu_+ (outer case), or be the newly attached middle edge at nu_+; it is not automatically a new seed in either case.

The actual A tree throughout this birth is the producer's fixed post-A tree, rooted at x outside J_+. Neutrality verifies absence of the chosen new label; it does not force an additional A rotation.

## 6. Literal first-hit consumption reconstruction

### 6.1 An original path-edge run must end

Read the complete B before h, with target x=x_h in O_-. The rigid path P_rho is part of the ACTUAL search path to x.

Every original edge e=(u,v,side) of P has an initial run containing the pre-hit snapshot. Until that run ends, v's complete descendant KEY SET stays fixed (the original RG04 edge-run lemma, including internal shape changes). It initially contains x. If it survived the entire splay, x would still lie below a proper incoming edge, contradicting that x becomes the global B root. This also covers v=x.

Hence EVERY initial path-edge run ends in a REAL B rotation of h. The original physical tuple may later reappear with a DIFFERENT run and child subtree.

Define

\[
\boxed{\beta(\rho)=\text{FIRST actual real B bit of h deleting
an original edge of }P_\rho.}
\tag{6.1}
\]

It always exists. Before it, all P edges still belong to their original runs and are on the current target path. No virtual companion, inferred projected edge or A operation defines beta.

### 6.2 Exact orientation/parity cases for the first bit

Let r be the original physical distance from g_- to x within O_-, and l the gap length.

| Case | Literal first modification |
| --- | --- |
| r=2s>=2 | After s-1 doubles strictly below g_-, the next double has grandparent g_-. If SS, its bit 0 changes the external edge into g_-; if opposite-side, bit 0 is below it and bit 1 changes that external edge. |
| r=2s+1>=1 | After s doubles below g_-, x is its child. The next double's first bit changes the lowest gap edge, as a pivot in SS or external edge in LR/RL. |
| r=0, opposite double | The first bit promotes the actual inner root x and changes its incoming gap edge. |
| r=0, SS, Type + | The first bit can change the gap edge ABOVE the lowest one before the second bit changes the lowest edge. |
| r=0, SS, Type 0 | The first bit acts above the gap, preserving its one edge; bit 1 is the first modification. |

The StepEv indices are respectively s, s+1, or 1 in h's actual bottom-up order. LEFT/RIGHT reflection preserves the statements.

The inner/outer roots are interior B subtrees, so g_+ has physical depth at least two before h. A first gap modification in the frozen domain therefore occurs in a double, not a terminal zig. For a general ancestor edge reaching the global root a terminal zig would simply delete its pivot edge. There is NO exceptional blind-gap orientation in which beta fails to exist.

The first modified edge need not be the lowest edge (r=0 SS Type +), and the first bit need not be bit 0. These exceptions matter for exact original IDs.

### 6.3 Every subsequent relevant bit, rooted output and SET retirement

For each original real bit b of h retain its complete before/after frame, deleted/inserted edge sets D_b,N_b, actual labels at all P vertices, and both predicates
1[g_+ ancestor g_-], 1[g_- ancestor g_+].
Tag whether it ends an initial P run, recreates an old tuple, changes either rooted output, changes either ancestor predicate, or merely transports an unchanged component. Keep unchanged bits as such; they are not excised.

For each J endpoint also record its FIRST actual SET removal sigma_J in h. It exists because the proper label contains x, whereas after the complete splay x is global root. A label containing x cannot be newly SET-created during its own splay, so this retirement is not confused with later creations excluding x.

The rooted output can change root/shape earlier while its S label is temporarily carried at another promoted root. Its incoming edge, physical root identity, SET-label retirement, and complete-state restoration are separate records.

## 7. Original A-cover evolution and mandatory work

Use the ORIGINAL physical endpoint cover
C_A(J)=lab_S^A(LCA_A(min J,max J)).
D2 proves J is A-absent iff J is a STRICT subset of that cover, including singleton J, private vertices and duplicated labels.

For every original real A bit between nu_+ and h record both physical covering roots, C_-,C_+, inner-ring obstructions (C_- intersect J_+) minus J_-, shared exterior obstructions C_- minus J_+, and actual SET changes.

The exact D2 table is applied to each label at the SAME actual rotation. For a primitive with old frame label F, old promoted-child label C and new demoted label D:

* old LCA at the demoted pivot, both endpoints staying below it: F to D;
* old LCA at that pivot, otherwise: physical root moves to promoted node, F to F;
* old LCA at the promoted node: C to F;
* any other LCA: rooted cover unchanged.

The reflected right rotation is included. Strict cover shrink creates D as an actual SET label; strict enlargement loses C as an actual SET label. Private-only/equal-label moves do not create false events.

At outer birth the producer root is outside J_+, so both covers are proper S subsets. At h's post-A state x_h is inside both intervals, so both covers are S. Each therefore has a genuine strict enlargement somewhere, but one physical event can serve many gaps. G0 already counts one root transition per occupied cohort.

For the blind gap, neither endpoint nor any old intermediate K is ever A-present during shared life. Thus no A acquisition/loss of THOSE labels is available in that interval. Cover events concern other labels, possibly enclosing many gaps. Their sign is computed from the actual SET and current B, not inferred from a cover-root change. Membership in phi_1/phi_2 requires their exact original selector conditions; sign alone proves neither vacancy nor membership.

The new quantitative mechanism below does not invent a second A-root-entry payment. It identifies cases where B's first gap modification CREATES a DIFFERENT A-present output and hence decreases the already controlled original B SET demand.

## 8. Complete cyclic return chronology

Start immediately BEFORE nu_+ and follow the ENTIRE original fine-event circle: its outer birth and remaining producer bits, all subsequent original accesses, h and its full splay, then every remaining operation back to the identical pre-birth phase. Exact full paired closure and deterministic original operations make BOTH complete A and B states return. This is all of W at a different fine cut, possibly splitting one operation, not an independently closed critical subword or a new budget period.

For each P edge retain its original run birth gamma_e, its first deletion delta_e in h, and every actual later recreation gamma'_e. Record full child subtrees and actual A states at each. Cases differ:

* An old P edge already present before nu_+ must be present on the cyclic return to that pre-birth full state, but can reappear much earlier, even within h.
* A middle-attachment edge NEW at nu_+ is absent at that pre-birth state. The next cyclic occurrence of nu_+ is the SAME original event ID, not another spendable resource.
* A persistent internal component can be transported through many attachments without rebirth.
* A recreated tuple is a new run with possibly DIFFERENT descendants, not the old rooted output restored.

The first-hit rooted labels disappear; any later identical rooted label has its actual new B creation. The complete-state return still includes every intermediate B/A event and every original DELETE/helper.

A genuinely forced A return fact is weaker than a per-gap payment: after h A is rooted inside J_+, while at the returned pre-nu_+ phase it has the producer root outside. Some original real A rotation must first move the global root outside that physical interval after h. Its current B context/sign and any existing owner must be recorded. It is not automatically negative, free, or distinct across gaps.

For W_hit with a_i=3, this first post-hit exit is the SAME right rotation A(h+1,1,0), root 3->2 in the next KEEP 1, for all p-1 selected gaps. Thus that extra-return selector has unbounded load even though the event genuinely exists.

Even more directly, assigning each gap the whole cyclic return's A budget gives every A event load equal to the number of gaps: each such return is the same full original circle with a different cut. These budgets cannot be added as disjoint work.

Section 9 supplies an original-source example where an old gap edge is recreated inside h itself, with no A between deletion and recreation. No full B restoration or per-gap independent A cost is inferred from tuple equality.

## 9. Source-valid adversarial families

### 9.1 H_pq and the dyadic restoration work

Use the complete original H source:
N=2^(p+1)(q+1)+1, x_j=N+1-2^j, m=x_p;
common full right vine, empty prefix; DELETE 2,...,N; descend EVERY N,...,1 with KEEP only x_0,...,x_p; KEEP 1,...,N; KEEP N-1,...,1.
Its length is 4N-2 and A=4(N-1). Both full labelled trees close.

For each selected column i, a_i=N+2-2^(p+1)(i+1), k_ji=2^(p-j)(i+1)-1, t_j=N-1+2^j. D1's ENTIRE cohort at forward KEEP a_i consists of

    d_ji=(t_j,k_ji), nu_ji=B(t_j,k_ji,0);
    J_ji=[a_i,a_i+2^(j+1)-2];
    O_ji=P_(j+1)(a_i+2^j-1);
    F_ji=[a_i,N-2^(j-1)].

Original Gamma/sigma/kappa records and complete Pi membership are retained. Global A two-vines make all interior J labels absent. Consecutive physical roots are direct LEFT parent-child pairs, so these are p-1 genuine Type 0 blind gaps per column.

The target a_i is the minimum of every selected output. Its path inside them is all LEFT. Each first modifying bit is a first LL bit whose new demoted label is a proper interior subset of O_pi. At post-A root a_i, H's actual A two-vine has no such label. Thus these first bits are NEUTRAL, not decreasing. These selected gaps survive in the remaining class of Section 10.

D2's shared transitions stay as recorded:
A(2N+1-a_i,1,0) exits below a_i for many histories, and A(2N-1+a_i,1,0) is their one cost-one common first hit. Arbitrarily many p-1 layers share them. No new rule may count them independently per gap.

The known distinct restoration zigs are genuine:
ell(j,k)=2^(j-1)(2k+1), seed a=N-2ell, and A(4N-a,1,0) in H (A(3N+2^p-a,1,0) in W).
They use the original seed/right-fringe provenance and maximum fiber one over the critical class. They are not promoted to a universal selector for arbitrary blind gaps.

### 9.2 W_pq and W_hit

For original W, all critical F/Pi memberships and physical outputs are the TF2/D1 ones. Output visibility must still be checked separately. D2 verifies the q=1, a_1=3 selected cohort is entirely output-unacquired; these direct-child pairs are Type 0 R_rem. For other columns no new output-absence claim is invented: any actual pair is tested with the frozen v predicates before using it. The restricted restoration map covers every critical demand, so applies to every eligible subpair without presuming all pairs eligible.

W_hit inserts KEEP a_i just after the W critical packet, before its complete closing sweeps. The selected cohort has p outputs, all A-unacquired because vertex a_i remains an ancestor of minimum 1 throughout their entire life; every cover contains that exterior key. Their whole F labels remain globally A-absent by the original upper-ancestor argument, and complete closure follows from both full sorted sweeps.

Full costs remain
2(N-1)+(2^p-1)+ceil((m-a_i)/2)+C_new_forward,
including the actual jump and ENTIRE reset. No prefix work or critical access is counted as a closed source.

For a_i=3 the first post-hit root exit is A(h+1,1,0) in KEEP 1, the physical right rotation 3->2; every selected outer interval starts at 3. Its load is p-1. A persistent obstruction never has to disappear before h, and the required post-hit root exit is not a bounded-load replacement.

### 9.3 Repeated 21-key I^mZ, warmed repeat and W_star

The full 21-key source and its exact original I/Z words are the current D2 Section 7.3. Its displayed critical output at copy offset b=34(j-1) has birth B(b+10,1,0), root 8, J=[5,11], first hit KEEP 6 at b+20. D1 proves that particular cohort is a SINGLETON. It gives no blind-gap pair, despite repeated physical fringe leaf 7 and distinct nonleaf births. Other actual cohorts are not declared empty. A=32m+A(Z) includes every fixed closing operation.

The warm source retains its excluded legal reaching prefix and complete B_p return, genuine marked carrier, full physical low/gap hangers, and A(period)=2(2^p-1). All original A S labels are prefixes/suffixes, so every actual interior collision pair is R; intermediate interior labels are also A-absent, hence actual collisions are R_rem. The first maximum's whole frames contain max S and are not U_int. Later marked births are real, but the q-sized initial wide wave is not recreated inside the period. The new counting argument applies only to actual consuming accesses and their original path-edge runs.

W_star remains the COMPLETE 235-operation source with A=282. Its pair
(h=173,d_-=(34,7),d_+=(76,1))
has intermediate B label [3,9] A-present and last lost at A(108,1,0). It belongs to R_sep, NOT R_rem. Its excluded middle candidate (72,3) fails the original whole-frame Pi predicate. No Type + blind gap is manufactured by forgetting that intermediate agreement.

### 9.4 A complete source realizing two decreasing first modifications

This NEW source H_dec supplies nonempty coverage for the quantitative class in Section 10, and attains the incidence constant TWO.

Start at the common full right vine on X=M=S=[33], empty prefix. Use H_(3,1), but insert DELETE 11, DELETE 10 AFTER its original forward KEEP 2 and BEFORE KEEP 3. The COMPLETE word is:

    DELETE 2,...,33;
    descend 33,...,1, KEEP only 33,32,30,26;
    KEEP 1; KEEP 2;
    DELETE 11; DELETE 10;
    KEEP 3,4,...,33;
    KEEP 32,31,...,1.

There are 132 original operations. The helpers are t=68,69; the common hit is h=70. Forward KEEP k for k>=3 is t=67+k; reverse KEEP k is t=133-k.

The original critical demands/births remain

    d1=(34,7), nu1=B(34,7,0), J1=[3,5], g1=4;
    d2=(36,3), nu2=B(36,3,0), J2=[3,9], g2=6;
    d3=(40,1), nu3=B(40,1,0), J3=[3,17], g3=10.

Their whole frames are [3,32],[3,31],[3,29] with the same original critical Gamma IDs as H. They remain absent at EVERY added/changed A snapshot: the upper keys 32,31,29 retain 33 below them through the low helpers and the subsequent increasing scan until their own hits; afterwards they retain 1. Original earlier A states and the closing reverse states are two-vine. This proves FULL Pi membership, including the cyclic seam.

Before the helpers A=2(1,V+(3,33)). DELETE 11 has depth 9, cost 5; DELETE 10 has depth 5, cost 3. The complete resulting A is

    10(4(2(1,3),8(6(5,7),9)),V+(11,33)).

The helper rotations create singletons, labels with upper endpoint 10, [5,7],[5,9], prefixes containing 1, or the suffix [11,33]; none is J1,J2,J3. The actual splay of target 3 cannot newly create a proper label containing 3. Thus all three chosen outputs stay A-unacquired until h. No extra B birth occurs in a helper. The old maximum frames are outside U_int, and KEEP 1's global double and KEEP 2's zig add no eligible earlier output. The COMPLETE cohort is exactly d1,d2,d3, both consecutive pairs being Type 0 R_rem.

The complete pre-B tree at h is

    2(1,26(18(P_4(10),P_3(22)),P_3(30))),

with path 2->26->18->10->6->4->3.


The complete helper-bit check is short enough to retain explicitly. Each listed D is the newly demoted physical subtree's label; all rotations of the helpers are present.

| Actual helper ID | Primitive pivot/promoted node | New demoted label D |
| --- | --- | --- |
| A(68,1,0), A(68,1,1) | left at 9 / left at 10, promote toward 11 | {9}; [9,10] |
| A(68,2,0), A(68,2,1) | left at 7 / left at 8 | {7}; [7,10] |
| A(68,3,0), A(68,3,1) | left at 5 / left at 6 | {5}; [5,10] |
| A(68,4,0), A(68,4,1) | left at 3 / left at 4 | {3}; [3,10] |
| A(68,5,0) | terminal left zig at 2, promote 11 | [1,10] |
| A(69,1,0), A(69,1,1) | left at 6 / left at 8, promote toward 10 | [5,7]; [5,9] |
| A(69,2,0), A(69,2,1) | left at 2 / left at 4 | [1,3]; [1,9] |
| A(69,3,0) | terminal right zig at 11, promote 10 | [11,33] |

None is [3,5], [3,9] or [3,17]. The suffix in the last row is included; it is not an omitted A event. All higher untouched u=29,31,32 still have 33 below them during both helpers. The two virtual zig companions have no physical rotation.


The actual post-A tree at h is

    3(2(1,-),10(4(-,8(6(5,7),9)),V+(11,33))).

The FIRST B bit B(70,1,0) is the right rotation at 6 promoting 4. It deletes

    (10,6,LEFT), (6,4,LEFT), (4,5,RIGHT)

and inserts

    (10,4,LEFT), (4,6,RIGHT), (6,5,LEFT).

Its new demoted label is [5,9], present in actual post-A at root 8. The removed promoted label contains actual target 3 and is A-missing. Thus Delta_B Psi=-1. The second bit creates [4,9], also A-present at root 4, so this double is decreasing in both bits.

The two blind paths are 6->4 and 10->6. Their FIRST modifications are BOTH this SAME B(70,1,0), respectively its pivot and external deletion. This realizes multiplicity two at one genuine decreasing bit, without acquiring any old gap label.

Complete A closure is explicit: after splaying 3 the visited prefix is 3(2(1,-),...), so the remaining increasing KEEPs end at the complete left vine, then the full reverse gives the original full right vine. B has the unchanged sorted-sweep endpoint. All physical keys remain present.

All costs are included. Relative to original H cost 128, the helpers cost 5+3=8. In KEEP 3,...,33 only targets 3,5,7 now cost two instead of one; every other such KEEP costs one. Their depths are respectively 3,4,3; all original reverse KEEPs remain zigs. Therefore

    A(H_dec)=128+8+3=139.

This is a complete admissible source, not a local abstract alignment. It proves the new class is nonempty and the incidence constant one would be false.

### 9.5 A blind-gap edge can return inside the SAME hit

Use W_(3,1) on [33], insert KEEP 5 immediately after its critical packet, then retain the ENTIRE increasing/reverse KEEP sweeps. Call this NEW word W_5. It has 106 operations and is fully paired-closed from the common right vine. Its added hit is h=41.

The actual selected critical cohort has the same d1,d2,d3 above, now first hit 5. Every output contains 3, and A's vertex 3 remains an ancestor of 1 under all intervening targets >=3, including the added 5. Thus all selected outputs are unacquired. The whole F labels remain absent on every complete Pi by the original upper-ancestor argument, preserved by the added low hit and full sweeps. The pairs are genuine Type 0 R_rem.

Take rho=(41,d2,d3), whose path is the physical LEFT edge 10->6. That initial run was born at B(36,3,0); it was an unchanged OUTER attachment at nu_+=B(40,1,0), not a fresh edge seed there.

The pre-B hit path is

    26 ->left 2 ->right 18 ->left 10 ->left 6 ->left 4 ->right 5.

The first double is LR on 6,4,5. Bit 0 changes 6->4 but preserves 10->6; bit 1 at 6 replaces (10,6,LEFT) by (10,5,LEFT), ending rho's run. It leaves 5's right subtree rooted at 6, now with S label [6,9].

The next double is LL on 18,10,5. Its bit 1 transports that rooted 6 subtree from 5's right to 10's left, RECREATING

    (10,6,LEFT) at B(41,2,1).

No A rotation occurs between B(41,1,1) and B(41,2,1). The old tuple returns, but its child label is now [6,9] rather than [3,9], and root 10's new label is [6,25] rather than [3,17]. The original outer label is SET-removed at B(41,2,0), and the original inner label at B(41,2,1). Physical tuple return is not restoration of either original output.

The added A jump has actual depth 26-5=21 and cost 11. The COMPLETE A cost is

    32 preparation + 7 descending + 11 jump
      + C_full_increasing + 32 reverse
      =82+C_full_increasing,

with the ENTIRE actual 33-key A scan included (in particular <=82+33*16=610). No numerical value for that scan is fabricated. The full sorted sweeps close both complete trees; the B hit is not independently closed.

This refutes the precise source implication “each reappearance of an old blind-gap edge requires an intervening A operation.” It does not refute an aggregate A bound. It also verifies a genuine opposite-side first modification: beta(rho)=B(41,1,1). Its new [6,9] label matches actual A at root 8 after the low jump, so that bit decreases. All other orientations remain governed by the universal literal tables.

### 9.6 Private A geometry, hangers and true mixed orientations

The helper witness uses different physical A/B roots for matching SET labels; no independent A-edge indicators are chosen. W_5 has a real LR consumption followed by LL; the original H reset has real RL boundary doubles; critical access construction has RR. The proof covers every RR/LL/LR/RL chosen birth and consumption without requiring any of these source shapes.

For arbitrary S, the path comprises ACTUAL physical vertices in the ancestor-closed carrier. S-free B hangers remain complete components. A can have private ancestors and duplicate S labels. The incidence bound concerns actual target-path edges, while the signs and aggregate budget use actual original SET changes. No unproved physical-neighbor or full-support simplification is imported.

## 10. New source-cost necessity theorem

### 10.1 A strictly smaller original-source complement

For each unchanged rho in R_rem use beta(rho) from (6.1), with A fixed at the actual post-A tree of its original first-hit access. Define

\[
\begin{aligned}
R_{\rm dec}&=\#\{\rho\in R_{\rm rem}:
                  \Delta_{B,\beta(\rho)}\Psi=-1\},\\
R_{\rm neu}&=\#\{\rho\in R_{\rm rem}:
                  \Delta_{B,\beta(\rho)}\Psi=0\}.
\end{aligned}
\tag{10.1}
\]

These are disjoint counts of ORIGINAL consecutive pairs. The original B sign theorem has no positive real B bit, so

\[
\boxed{R_{\rm rem}=R_{\rm dec}+R_{\rm neu}.}
\tag{10.2}
\]

This test refers to an actual specified source event, not to the success of a desired charging rule. R_neu has the additional source predicate “its FIRST consumption of the original physical path is neutral.” No gap is joined to a new neighbor, and no interior demand is reclassified.

H_dec gives two R_dec pairs; ordinary H_(3,1) gives two R_neu pairs. Thus the newly controlled class is nonempty, and the surviving predicate is demonstrably narrower than R_rem. Ordinary H_pq still has arbitrarily long selected chains in R_neu. Narrower does not mean bounded cardinality.

### 10.2 What is actually forced

If rho is counted in R_dec, its literal first path-changing B bit removes an A-missing proper label containing the hit target and creates an A-present label that excludes that target. The latter label is different from all old path labels, since all old path labels contain the target. Consequently there is no contradiction with the old blind labels' complete A absence.

The source has therefore supplied an actual decreasing B bit, not an additional A bit at the original neutral birth. Define the exact B selector

    tau(rho)=beta(rho), for rho in the R_dec subclass.

The selector is determined before any accounting association is sought. It uses one original B(operation,StepEv,bit) occurrence. Section 11 proves its load at most two.

No direct A selector sigma(rho) is asserted. The permitted aggregate alternative uses the ORIGINAL closed-source identity

\[
D_B=P_A-N_A,\qquad R_A=P_A+N_A+T_A=2A-V_A.
\tag{10.3}
\]

Here P_A,N_A,T_A count actual real A bits of signs +1,-1,0 for the inherited Psi. To rederive the bridge: the complete period has total A change P_A-N_A, total B change -D_B, and identical initial/final Psi by exact paired closure. DELETEs contribute their actual A signs and zero B change; virtual units contribute neither. This is the existing original source identity, independent of the new path classification.

Combining the load theorem with that identity gives the NEW universal cost consequence

\[
\boxed{R_{\rm dec}\le2D_B
       =2(P_A-N_A)\le2R_A\le4A.}
\tag{10.4}
\]

It controls original blind gaps through existing decrease surplus. It neither assumes an independent A event per gap nor reuses an excluded reaching-prefix wave.

## 11. Full cross-cohort multiplicity and the common physical budget

### 11.1 At most two gaps per actual first-change bit

Fix an ORIGINAL real B bit b. Every rho with beta(rho)=b has its consuming cohort at b's SAME original KEEP h. Different first-hit KEEP occurrences cannot use the same physical bit, including when their cyclic display intervals wrap.

List the full cohort roots from inner to outer. In the rigid pre-hit B tree they lie on the target's unique physical ancestor path. The path segments between CONSECUTIVE roots are edge-disjoint. They can share an endpoint vertex, but cannot share an edge. Rigidity proves these are exactly the segments recorded at their respective outer births.

Immediately before b, every edge of every segment awaiting its FIRST change is still in its original run, and still on the current target path. For a primitive rotation g(L,p(H,R))->p(g(L,H),R), the possible deleted edges are:

| Deleted edge | Relation to the current target path in its actual B splay |
| --- | --- |
| external c->g, if present | On the path |
| pivot g->p | On the path |
| middle p->rt(H), if present | OFF the path |

The reflected table has the same property. For an opposite-side first bit the pivot is the old parent and the promoted node is the target itself; for a same-side first bit the target remains in the promoted child's other component. In both cases the middle component excludes the actual target. The second bits and terminal zigs obey the same literal rule.

Thus b deletes at most TWO edges belonging to still-intact original gap segments. Since those segments are edge-disjoint, it can be the first change for at most two gaps. Counting two deleted edges from ONE gap still supplies only one preimage. Therefore

\[
\boxed{\#\{\rho\in R_{\rm rem}:\beta(\rho)=b\}\le2}
\quad\text{for EVERY original real B bit }b.
\tag{11.1}
\]

This is global across all cohorts, source periods, output-root epochs and path lengths. It requires consecutive roots of the FULL cohort; a filtered chain would invalidate the edge-disjointness argument. It counts original edge runs, so later recreation of the same tuple does not generate another first change.

Restricting (11.1) to decreasing bits proves R_dec<=2D_B. H_dec attains TWO with one external deletion and one pivot deletion, so replacing two by one in this selector would be false.

### 11.2 D1/D2 overlap is retained in one budget

Let F_old=E_ctl+R_sep. For each actual real A bit r let chi_old(r) be 1 if it is in the verified DISJOINT union of phi_1 and phi_2 images, otherwise 0. Section 1 proves chi_old<=1 and

    F_old=sum_r chi_old(r).

Every such image has sign +1 or -1, never zero. Write s_A(r) for the actual sign of r. Equations (10.3) and (11.1) give the common signed inventory

\[
F_{\rm old}+R_{\rm dec}
 \le\sum_{r\in\mathcal R_A}
       \bigl(\chi_{\rm old}(r)+2s_A(r)\bigr).
\tag{11.2}
\]

No disjointness between new aggregate work and old payment images is assumed. The right-hand side is exactly F_old+2D_B. Its coefficients, on the SAME original real A occurrences, are:

| Actual A sign | chi_old | Coefficient chi_old+2s_A |
| --- | --- | --- |
| +1 | 0 or 1 | 2 or 3 |
| -1 | 0 or 1 | -2 or -1 |
| 0 | 0 | 0 |

In particular,

\[
\boxed{F_{\rm old}+R_{\rm dec}
       \le3P_A-N_A\le3R_A\le6A.}
\tag{11.3}
\]

One can instead keep the weaker but transparent bound
F_old+R_dec<=R_A+2D_B<=3R_A.
Both use one original A inventory. Negative terms are original signed cancellation, not extra spendable tickets. There is no claim that each rho has been matched to its own real A bit. Equation (11.2) is an aggregate inequality with proved multiplicity, as authorized by Stage G.

The signs and virtual-unit conversion are the actual source ones. Two real bits in one A double are each counted at most with the displayed weight; a terminal zig has one real bit and an unused virtual accounting unit. No physical unit is declared vacant, no g_1 owner is reassigned, and no historical raw-payment allocation is duplicated.

### 11.3 Residual quantitative consequences, with their limits

Retaining the exact partition gives

\[
U_{\rm int}=H+F_{\rm old}+R_{\rm dec}+R_{\rm neu}
            \le7A+R_{\rm neu},
\]
\[
\boxed{Q_B\le13A+R_{\rm neu}.}
\tag{11.4}
\]

These are PARTIAL residual bounds, with the inherited Route 04 qualifications. They accompany the sharper-cost original-domain bound Q_B<=9A+R_rem. Equation (11.4) pays a larger coefficient to remove a nonempty source-defined subclass. Neither residual inequality is a bound on all of Q_B by a fixed multiple of A.

The theorem does not add a third independent budget for restoration. All A restoration events, whether D1/D2 images or not, are already included in P_A,N_A,T_A in (11.2). Other chains can share them without violating the displayed weights. This is exactly why a bounded B-first-change incidence can be composed although a per-gap “new A restoration” assertion fails.

## 12. Quantitative result and the first remaining obstruction

The new universal theorem is R_dec<=4A, with the exact global original-B multiplicity two and an explicit common-A budget. It applies to BOTH Type 0 and Type + gaps. Path length and intermediate-label count never enter its constant.

The unresolved class R_neu consists exactly of original blind gaps whose first actual path-changing bit is NEUTRAL. The original H_pq selected cohorts are an arbitrary-length control in this class: one cannot dispose of it by a bounded-depth exception or a per-hit constant. Their distinct later dyadic A restoration zigs are real complete-period work, but their family-specific selector has not been proved for arbitrary original sources.

The first unsupported universal implication would be:

    The neutral-first-change gaps force, elsewhere in the SAME
    complete original period, additional real A work or original
    decreasing B work with an ABSOLUTE globally bounded incidence.

No such statement is proved here. Later path changes cannot be substituted for beta without a new incidence argument: after first deletion, the original segments cease to be simultaneously intact; labels can be transported and edge tuples can be recreated with different descendants. W_5 gives an actual within-hit recreation with NO intervening A. Shared A root entry/exit events have unbounded load in H/W_hit.

The exact missing relationship is therefore between those neutral first-consumption occurrences and distinct or bounded-multiplicity later regeneration/restoration work. Merely noting an eventual cyclic return, or assigning the whole original period's A cost to each gap, supplies no bound.

In particular this report establishes neither R_neu<=cA nor a contractive inequality with coefficient below one, and does not establish an unbounded R_neu/A or R_rem/A family. It refutes only the specific “every old-edge return needs an intervening A” implication and any load-one claim for beta. URCD is not refuted.

No complete R_rem certificate exists in this report, so Stage 10's complete U_int, Q_B and B coefficients are NOT assembled. Near-side and other Route 04/outside-domain cases retain their inherited status; removing a blind-gap subclass supplies no new certificate for them.

## 13. Proof-relevance verification

| Required test | Discharged result and actual scope |
| --- | --- |
| New quantity controlled | Original strict subclass R_dec of the frozen R_rem |
| Independent membership | Exact sign at the first real B bit changing the original path; no matching-based definition |
| Universal necessity | Initial path run must end during its original first hit; beta exists for every rho |
| Global multiplicity | At most two gaps per original B bit, using full-cohort consecutive path segments |
| Original A cost | R_dec<=2D_B=2(P_A-N_A)<=4A on the COMPLETE paired-closed source |
| Old/new overlap | Equation (11.2), maximum positive coefficient three on the same original A inventory |
| Nonempty coverage | Complete symbolic H_dec source, 132 operations, A=139, two R_dec gaps at one decreasing bit |
| Strict residual | Unmodified H_(3,1) has the same selected gap locations with neutral first changes; H_pq retains arbitrary chain length |
| Literal regeneration test | W_5 recreates (10,6,LEFT) during one hit with changed subtree labels and no intervening A |
| Helpers/private geometry | Actual helper A rotations construct the agreement; no independent A-edge indicators |
| Sparse support/hangers | General incidence uses actual carrier path edges; aggregate signs use original duplicate-suppressed SET labels |
| Historical cost integrity | All original DELETEs, jumps, full resets and reverse scans retained; reaching prefixes remain excluded |
| No equivalent restatement | A local path-deletion theorem proves a finite cost bound for a nonempty strict source subclass |
| No overclaim | No bound on R_neu, complete URCD or DO; no P1/V1/P2/RG-05 execution |

All universal statements are same-agent symbolic derivations. The new finite words are exact manuscript witnesses and have not been source-replayed, experimentally sampled, independently certified or checked by a formal kernel. The finite witnesses establish nonemptiness/sharpness or refute precise local implications; the universal inequality comes from the all-source proof in Sections 10–11.

## 14. Dependency ledger

### 14.1 Mathematical dependencies and proof debt

| Dependency | Current use | Status retained |
| --- | --- | --- |
| Original Pair Access / SET specifications | Complete physical keys, KEEP/DELETE, A-then-B order, actual rotations, carrier and SET semantics | Frozen model |
| RG01 primitive and original SET signs | Two possible target-path deletions; A real/virtual cost; D_B=P_A-N_A | Universal symbolic input, identity rederived here |
| RG04 edge-run invariance | An intact incoming-edge run preserves its complete child key set | Used only until the FIRST deletion |
| G0 | H<=A; U_int=H+E; Q_B<=6A+U_int | Inherited precise scopes |
| D1 | Full cohort, strict chosen-output nesting/rigidity, phi_1 | Reconstructed and audited in Section 1 |
| D2 | Original R_sep/R_rem partition, phi_2, physical covers | Reconstructed and audited; joint-image proof supplied |
| TF2 / W / H / W_hit / W_star / I^mZ / warm reports | Complete original words and scoped symbolic recurrences | Not upgraded to universal selectors |
| New D3 beta theorem | Every original path initially lies on hit path; first-modification incidence <=2 | Universal symbolic proof |
| New D3 aggregate theorem | R_dec<=4A and joint common-budget coefficient | Universal symbolic proof |
| Neutral-first consumption | R_neu versus bounded later A/B work | UNRESOLVED |
| Unrestricted Universal CD / DO | No complete certificate from these partial results | OPEN; no later gate executed |

The source statements imported from G0/D1/D2/Route 04 keep their actual symbolic or audit-pending verification level. D3 does not upgrade all their historical prerequisites to independent certification. This report supplies explicit author-level all-source proofs of its new incidence/cost claims and of the requested D1/D2 image compatibility.

### 14.2 Current source references and read-only pins

The following are the actual inputs read for this D3 task. Hashes identify current working bytes, rather than assuming old reports were committed or unchanged from their own historical HEAD. The pre-execution branch/HEAD was coarse-double-branch at 6d532b2c795c0778f57d8023b23b5fedfc48b010.

| ID | Current input | Use | SHA256 |
| --- | --- | --- | --- |
| D0 | [G0 quantitative baseline](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/IAGS12_G0_QUANTITATIVE_BASELINE.md:1>) | H and U/Q baseline | 09863af3277745f5ebef956e680feb43a3d1ad4e5c7bb57bb545918c4813523a |
| D1 | [D1 collision provenance](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/IAGS12_D1_COLLISION_PROVENANCE.md:1>) | Complete cohorts, chosen outputs, phi_1 | 0aa9cbf3e9cc036af5d4bbdf3ea3acdfcbef9341c856401b74247a615c4f814f |
| D2 | [D2 residual regeneration cost](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/IAGS12_D2_RESIDUAL_REGENERATION_COST.md:1>) | R partition, phi_2, covers and adversarial controls | 4b1623da997a7c1dbd40073809d198cfd8c850b48edc1db6b42b5655b1808b0e |
| D3 | [RG04 global regeneration](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG04_GLOBAL_REGENERATION.md:1>) | Physical edge-run and full chronology facts | 52072e0c9a5214cf16b7bf44e3efb09df102e91e939bf3186b2e280b0763832b |
| D4 | [RG01 primitive accounting](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md:1>) | Literal rotations, real/virtual costs and SET telescoping | f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa |
| D5 | [RG02 edge conservation](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG02_EDGE_CONSERVATION.md:1>) | Prior failures retained; no Phi_0 certificate assumed | 16b93dbe5fa80a75da0591ad79765581ffc8a8c826b6f41758e985270de2253e |
| D6 | [TF2 audit and parametric amplification](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md:1>) | W/H full physical source recurrences | 1c31d4b5d8c97771640e5235e2015a95b584753d42ada4987600d071d8466176 |
| D7 | [Universal interior source-work report](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md:1>) | Full-window source obligations and I^mZ | 4cf67ae246987f211997e18a5efb5b6d37ab9afbf800777769bbd2f56de5d42a |
| D8 | [Regeneration continuation / warmed source](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md:1>) | W_hit / W_star / warm complete source scopes | 50e90e4471b1f794ba58f848f44522dc71ac74685ed9f81e09593cfb11e871d0 |
| D9 | [Original Pair Access specification](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md:1>) | Original labelled paired closure and KEEP/DELETE | 8be55471edfdac31f59d552952c84f8d380bbfa3a7e46b7643d22af766757fd5 |
| D10 | [Original source / SET specification](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md:1>) | Carrier and duplicate-suppressed J_S | a52487cfe212aa562b91406bb6006d2f9a9469bebcfd4e039d9cd224fc6d677b |
| D11 | [Repository research rules](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md:1>) | Proof level, resource and authorization gates | c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc |
| D12 | [Current D3 user directive](<C:/Users/Saif malik/.codex/attachments/d05519e4-e1f1-4d6e-8a60-170b76fa4964/Pasted text.txt:1>) | D3-only scope and acceptance standard | 4fbb2223ecfb26ce0f5155a2e80e26c9d5b16444aeeddde9096f10a218a03fba |

### 14.3 Preservation and verification record

All THIRTEEN pinned inputs were rehashed after writing the proof sections and matched their pre-execution hashes exactly. The tracked diff is empty. The branch and HEAD remain coarse-double-branch / 6d532b2c795c0778f57d8023b23b5fedfc48b010. The untracked pre-existing reports/directories remain in place; the only new task artifact is this D3 report.

Verification consists of static readback, author-level literal rotation/SET reasoning, exact event-count algebra and read-only file/Git checks. No source-engine query, source replay, tree sample, enumeration, solver, external research or subagent was run. No original artifact, route artifact, source code, physical-key population, owner map, historical period, event ID or resource cap was modified.

The source work is repository-recoverable and the user explicitly requested this repository Markdown deliverable; no duplicate project-memory page is created.

## 15. Final gate verdict and authorized stopping point

**D3: QUANTITATIVE PASS — PARTIAL, at same-agent universal symbolic proof level.**

1. The independent D1/D2 audit proves global injectivity AND disjoint images, so E_ctl+R_sep<=R_A<=2A and the inherited baseline Q_B<=9A+R_rem hold at their stated scopes.
2. The first physical path modification exists for every original blind gap. At most TWO such gaps use one original B bit, globally.
3. The nonempty strict subclass with DECREASING first modification has the universal original-source cost bound R_dec<=2D_B<=4A. Its overlap with D1/D2 is retained explicitly in one signed A inventory.
4. The exact narrower residual is R_neu: blind gaps with NEUTRAL first modification. Its full universal regeneration/restoration bound remains OPEN. Ordinary H supplies arbitrary chain length in this class, while H_dec proves the removed class is nonempty.
5. The precise implication “every recreation of an old blind-gap physical edge requires an intervening A operation” is REFUTED by the complete W_5 source. This does not refute URCD or an aggregate A bound.

No complete R_rem, URCD or DO theorem is claimed. This report stops after D3. P1, V1, P2, RG-05 and every later gate remain unexecuted.
