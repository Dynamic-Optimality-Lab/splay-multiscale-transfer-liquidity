# IAGS 1.2 — D2 residual A-unacquired regeneration cost

Date: 2026-11-09, Asia/Karachi.

## Scope fixed before the formal report

Execute D2 ONLY. Do not execute D3, P1, V1, P2 or RG-05. Preserve the complete original A/full-B model, physical keys, actual event IDs, paired closure, full cyclic windows, costs, owners and resource caps. Only this isolated report is written.

The complete current D1 proof and definitions, rather than a prose substitute, were read and audited. The imported residual is unchanged: ORIGINAL consecutive pairs in one complete first-hit cohort, both chosen output histories A-unacquired. No vertex is removed merely because it is inconvenient.

The principal mechanism to investigate is physical A-cover geometry. A possible smaller cost class is a residual gap containing an actual B subtree which becomes A-present during the shared output lifetime. Its first-hit disappearance may force a real A SET loss; any multiplicity claim must be proved across all source cohorts. A physical B enclosure alone is never a credit.

The proposed upward effect is strictly limited: if this class has a global cost bound AND nonempty source-realized coverage, remove it from R with an exact membership predicate for the complement. Otherwise report structural/blocked status. No bound on all R is assumed.

All constructions below are symbolic ordinary-tree proofs. There is no source-engine query, computational replay, experiment, enumeration, solver, new potential campaign, resource-cap change, Git mutation or independent/unapproved agent. Static current-byte reads and manuscript checks do not upgrade the inherited verification level.

## 1. D1 prerequisite audit

**Dependency audit: PASS, at the same-agent symbolic level.** Current D1 bytes were read in full, including Sections 3-6, 9, 11 and the complete source witnesses. Its definitions and claimed E=E_ctl+R, E_ctl<=2A are usable at that exact scope.

The checked proof is: selected outputs survive rigidly to their first hit; active chosen histories have unique nonempty B labels; one cohort is a strict physical-subtree chain. For each A-exposed chosen output, neutrality makes its label absent at birth and the first-hit A root makes it absent at the endpoint. Its actual acquisition and last loss are distinct real events. One rotation changes at most one SET label in each direction; simultaneous loss and creation of two B-common labels is excluded by B's rooted-subtree compatibility, including the disjoint/consecutive-S-key case. Thus acquisition and loss images are globally disjoint and injective.

D1 assigns a controlled edge to the outer output's acquisition if exposed, otherwise the inner output's loss. At most one lower edge and one upper edge use those two distinct events. This verifies the claimed load ONE per original real A rotation and E_ctl<=R_A=2A-V_A<=2A, over all cohorts. It is a cost count, not owner vacancy or independent certification.

The exact imported residual is

    rho=(h,d_i,d_(i+1)), ORIGINAL consecutive vertices
    of the FULL cohort C_h, with v(d_i)=v(d_(i+1))=0,

where v(d)=1 iff the CHOSEN output label J_d becomes A-present at any actual snapshot from its original birth through its common hit's post-A/pre-B state. No exposed vertex is deleted and its neighbors rejoined.

Whole-frame membership remains d in U_int, using F_d absent on the COMPLETE original Pi_d. Output nonacquisition is an additional, different predicate. No dependency defect or replacement residual is introduced.

Original Pair Access and ND35 specifications were read directly: physical keys remain present, A processes KEEP and DELETE, B processes KEEP only, each original double/zig is one A StepEv, both complete labelled trees close, and a causal lift does not create a resource. All older audit qualifications, owners and caps remain.

## 2. Exact residual-pair registry

For arbitrary rho in R write minus/plus for its inner/outer chosen outputs. Retain the following actual data:

| Item | Exact original object |
| --- | --- |
| Demands | d_-,d_+ in U_int, adjacent in their COMPLETE C_h |
| Chosen births | nu=B(t,k,0) for RR/LL; nu=B(t,k,1) for LR/RL |
| Physical outputs | O_-,O_+ with original physical roots g_-,g_+ and ALL their physical keys/hangers |
| S labels | J_-=V(O_-) intersect S strictly contained in J_+=V(O_+) intersect S |
| Whole-frame histories | F_-,F_+, Gamma_-,Gamma_+, kappa_-,kappa_+, COMPLETE Pi_-,Pi_+ |
| Chronology | nu_- before nu_+ before h on the one original cyclic causal timeline |
| A states | Actual fixed post-A tree at each B birth; every original real A bit between them and h |
| Common hit | First KEEP in BOTH labels, original ID h and actual target x_h in J_- |
| Nonacquisition | J_- absent at EVERY A snapshot on its OWN birth-to-hit interval; same for J_+ |

The outputs are both rigid throughout their SHARED interval from nu_+ just after birth through h's post-A/pre-B state. Their strict physical inclusion holds throughout that interval, not merely at its final snapshot. Before nu_+ the larger chosen subtree has not yet been born in this occurrence; no inclusion claim about that earlier nonexistent object is made.

At the inner birth, A has root its producer x_- outside J_-; no unwarranted relation of x_- to the future J_+ is imposed. At the outer birth A has root x_+ outside J_+, hence outside both labels. At h's post-A state A has root x_h inside both. DELETE helpers can access INSIDE either interval without being a B first hit or acquiring either label.

All real A accesses/bits in the shared interval are retained with their operation, StepEv, bit, pivot, promoted node and middle subtree. Prefix work and virtual companions are never substituted.

## 3. A-cover and exterior-obstruction theorem

### 3.1 Exact cover and equivalence — universal

For any nonempty original output S label J put a=min J,b=max J, and

    ell_A(J)=LCA_A(a,b);
    C_A(J)=lab_S^A(ell_A(J)).

This is the FULL physical rooted subtree at the original physical LCA, projected only by the ORIGINAL S-label convention. It is not the connecting path or a projected-tree LCA.

Then

\[
\boxed{J\subseteq C_A(J),\qquad
J\notin J_S(A)\ \Longleftrightarrow\ J\subsetneq C_A(J).}
\tag{3.1}
\]

Proof: a full physical BST subtree containing a and b contains every physical key between them, hence every key of J. If some physical A subtree has S label J, it contains a,b and their LCA; its S label therefore contains C_A(J). The reverse containment J subset C_A(J) gives equality. Conversely C_A(J)=J is itself a representative of J in the original SET.

An output J is an interval in S, although S may be sparse in physical order. Thus a key in C_A(J) minus J lies below min J or above max J in S order. Call such an ACTUAL S key an exterior A obstruction.

For a singleton J={a}, the LCA is the actual key a. Its physical subtree may contain private vertices; it is A-present exactly when that subtree has no OTHER S key. Private keys alone are not exterior S obstructions. Duplicate S labels on anonymous A chains count once and do not invalidate (3.1). The physical LCA can itself be private for larger J. Empty J is not used; degenerate empty R is handled separately.

### 3.2 Nested covers and the exhaustive obstruction relations

For J_- strictly inside J_+, physical ancestry gives ell_- at/below ell_+ and C_- subset C_+. For a residual pair both inclusions J_- strictly inside C_-, J_+ strictly inside C_+ hold at every relevant snapshot.

The complete set relations are

    inner ring obstructions = (C_- intersect J_+) minus J_-;
    shared exterior obstructions = C_- minus J_+;
    outer-only exterior obstructions = (C_+ minus J_+) minus C_-.

In particular the obstruction sets for the two labels have common elements exactly C_- minus J_+.

Either C_- has a key outside J_+, yielding a physical obstruction shared by both, or C_- subset J_+ and ALL inner obstructions lie in J_+ minus J_-. In the latter case C_- is actually a STRICT subset of J_+: equality would make J_+ an A label and violate residual membership. Outer obstructions still exist, and the two physical covering roots must then differ.

The ring and shared sets can both be nonempty. Different outside obstructions and changes of covering ancestor are permitted. No arbitrary choice of one canonical blocker, or assumption of a single persistent blocker, replaces these exact sets.

## 4. A-rotation obstruction transitions

### 4.1 Literal full rotation, not an abstract interval update

For a real A left rotation

    g(L,p(H,R)) -> p(g(L,H),R),

let F be its whole-frame S label, C the OLD p label, and D the NEW g label. Let D_phys be the new complete demoted-g subtree. The physical edge changes are exactly the original external c->g to c->p, pivot g->p to p->g, and nonempty middle p->rt(H) to g->rt(H), with the RG01 LEFT/RIGHT orientations. Internal/outer subtrees and ancestor key sets remain.

For EACH J independently, compute its actual old LCA ell. The exhaustive transition table is:

| Old physical LCA | Endpoint condition | New LCA | S-cover change | Exterior-set effect |
| --- | --- | --- | --- | --- |
| ell=g | Both endpoints belong to D_phys | g | F to D | Remove (F minus D) from C_A(J) minus J |
| ell=g | Otherwise | p | F to F | Same obstruction SET; physical covering root changes |
| ell=p | Necessarily the old LCA premise | p | C to F | Add F minus C to the exterior set |
| ell neither pivot | Endpoints in unchanged component or covering root above frame | Same ell | Unchanged | Unchanged |

For the SEPARATE right rotation

    g(p(L,H),R) -> p(L,g(H,R)),

take C=old p label and D=new g label, with D_phys=g(H,R). The SAME four rows, with these reflected components and actual endpoint test, hold. The changed middle is p->rt(H) to g->rt(H) with reflected orientations; private operands and empty H are allowed.

Proof: only g,p can change descendant key sets. If the old LCA is g and both endpoints remain under demoted g, their LCA stays g; otherwise the promoted p is their LCA and carries the whole old frame. An old LCA p stays p, now covering that whole frame. All other possible LCAs have unchanged rooted key sets. This is a physical-tree proof, including singleton endpoints.

Evaluate this table on BOTH labels with the SAME actual rotation; their indicators are not independent. Covers remain nested by physical ancestry.

The complete primitive changed-edge table is retained explicitly. Here h=rt(H); c-edges are absent at the root and h-edges absent for empty H.

| A primitive | Deleted physical edges | Inserted physical edges |
| --- | --- | --- |
| Left rotation | (c,g,sigma); (g,p,RIGHT); (p,h,LEFT) | (c,p,sigma); (p,g,LEFT); (g,h,RIGHT) |
| Right rotation | (c,g,sigma); (g,p,LEFT); (p,h,RIGHT) | (c,p,sigma); (p,g,RIGHT); (g,h,LEFT) |

All other edge runs persist in that primitive, with their actual component/ancestor distinction. These tables carry the original operation/StepEv/real-bit ID when instantiated on W.


### 4.2 Which changes are actual SET events

If F to D is a STRICT S-cover shrink, D is genuinely SET-created. If it already existed, its representative would contain the endpoints before the rotation and contradict minimality of the old larger cover F.

If C to F is a STRICT S-cover enlargement, C is genuinely SET-lost. Any surviving representative of C would contain the endpoints after the rotation and contradict their new minimal cover F.

Equal S labels under private-node movement do not trigger such SET changes. The root-transport row can change the LCA's physical name without changing any obstruction key. In a true residual history neither cover can ever shrink to its own J: that would invalidate the ORIGINAL whole-history R predicate, not merely change a temporary flag.

### 4.3 Mandatory real work, and its exact limitation

At nu_+ A has its S-key producer root outside J_+, so both covers are proper S subsets. At h's post-A state the actual A root x_h is between the endpoints of BOTH labels; their LCA is that global root and both covers are S.

Thus each cover has at least one strict enlargement during the shared lifetime, forced by original A dynamics. Each such enlargement has an actual SET-loss bit by Section 4.2. This proves real work exists; it does NOT prove distinct work per residual pair or per cover.

The global multiplicity of arbitrary cover changes/losses is NOT bounded by this local table. H_pq in Section 7 gives the exact unbounded sharing event.

## 5. Persistent versus changing obstruction cases

The cover sets in Section 3, not a freely renamed blocker, determine the cases.

* A covering root can change while its S-cover and all exterior keys persist.
* A strict cover shrink can remove some obstruction keys while others survive; R requires at least one obstruction left.
* A strict enlargement can add new exterior keys while retaining old ones.
* Two covers can merge or separate, changing whether they have a shared exterior obstruction.
* A fixed S key can remain in the covers of many nested outputs, even when their roots/covers change.

These are consequences of the literal table; none issues one credit per key. Selecting a canonical key such as the smallest obstruction is an audit convention only. Its change can represent many simultaneous label histories and must have its own multiplicity proof.

There is an additional physical possibility: while J_- and J_+ are BOTH A-unacquired, a rooted B subtree strictly BETWEEN them can be an A label. If such K exists then

    J_- strictly inside C_A(J_-) subset K strictly inside J_+.

Thus the inner obstruction is in the outer ring at that snapshot, whereas the outer label still has an obstruction outside J_+. This does not acquire either chosen output. Section 8 derives the actual loss forced by this intermediate common subtree, and Section 9 proves the global count.

Absence of such an intermediate common subtree is not inferred from the two endpoints' nonacquisition. Section 7.5 realizes the distinction in a complete source.

## 6. B regeneration and paired-closure requirements

Each chosen output is an original real B birth, survives outside-target accesses, and is removed as a proper label before its first-hit splay ends. The same label used later requires its actual recreation; matching endpoint names do not merge its occurrences.

On a residual pair's shared lifetime the ENTIRE O_+ is rigid. Every physical B subtree whose S label K satisfies J_- strictly inside K strictly inside J_+ is therefore a fixed internal subtree along the actual g_+-to-g_- path. Its rooted label and shape persist; only external attachments of O_+ can change. Its earlier creation/run history is recorded with its original B bit, not declared newly born at the moment A agrees with it.

At the common B hit h, x_h is in J_-, hence in every such K. All these proper labels are absent by the END of h's B phase. A later common intermediate occurrence requires actual B regeneration. This does not alone force an A event; the decisive additional fact is actual A presence of K BEFORE that hit and mandatory A absence at h's POST-A state.

Complete paired closure returns both full trees, not merely the two labels or root flags. It does not imply that an A-unacquired output itself ever has to become an A label. Nor does one restored B pattern prove one new A rotation per nested description. The W/H distinct spacer restoration injection retains its restricted source scope, not a universal regeneration law.

## 7. Parametric and repeated-source adversarial tests

### 7.1 H_pq: exact R membership and shared cover changes

Use the COMPLETE H_pq from its common right vine on X=M=S=[N]:

    N=2^(p+1)(q+1)+1, x_j=N+1-2^j;
    DELETE 2,...,N;
    descend EVERY key N,...,1, KEEP exactly x_0,...,x_p;
    KEEP 1,...,N; KEEP N-1,...,1.

Its length is 4N-2 and A=R_A=4(N-1). Every nonzero A access is an adjacent-key zig. Its complete A/B closure is the original sorted-sweep endpoint identity.

For each i=1,...,q let
a_i=N+2-2^(p+1)(i+1), k_ji=2^(p-j)(i+1)-1 and t_j=N-1+2^j. D1 proves the ENTIRE cohort at h_i=forward KEEP a_i consists of d_ji=(t_j,k_ji), j=1,...,p, with

    nu_ji=B(t_j,k_ji,0);
    J_ji=[a_i,b_ji], b_ji=a_i+2^(j+1)-2;
    O_ji=P_(j+1)(a_i+2^j-1);
    F_ji=[a_i,N-2^(j-1)].

The original Gamma/sigma/kappa histories are those in TF2/D1. The whole frames are absent on their COMPLETE Pi. A is globally interior-label-absent, so EVERY selected output is A-unacquired. All p-1 consecutive column pairs are genuinely in R. The larger root's left child is the smaller output root; no intermediate B label lies between these selected roots.

For the actual two-vine A with global root r and J=[a,b],

\[
C_A(J)=
\begin{cases}
[1,b],&r>b,\\
[a,N],&r<a,\\
S,&a\le r\le b.
\end{cases}
\tag{7.1}
\]

At output birth r=x_j>b_ji, and key 1 blocks its cover. At the single span-exit zig

    e_i=A(2N+1-a_i,1,0), root a_i -> a_i-1,

ALL column covers shrink from S to [a_i,N]. Key 1 disappears from all those covers; key N still obstructs every output. The smallest-obstruction convention changes from 1 to b_ji+1 for EVERY level at this one physical event.

At the final root entry/common hit

    r_i=A(2N-1+a_i,1,0), root a_i-1 -> a_i,

ALL covers enlarge from [a_i,N] to S. This is the LAST strict enlargement before the hit, for every column output. The same SET loss of C=[a_i,N] is B-common: immediately before the B phase B's old root is a_i-1, with that complete right-side S label.

Thus the candidate “charge a residual pair to its last cover enlargement/common-cover loss” has load p-1 at r_i. For any fixed bound choose larger p. Counting obstruction changes at e_i has the same unbounded pair load. These are complete-source parametric refutations of the specified selectors, NOT of R<=cA.

The crucial failure is that C CONTAINS J_+, rather than lying strictly between J_- and J_+. The one lost common cover can surround many collision gaps.

H also shows that a full-history fixed blocker is not automatic. For an outer J=[a,b], its birth cover is [1,b] and its post-exit cover is [a,N]; their intersection is exactly J. No exterior S key lies in both, so none can be a persistent obstruction throughout that whole history. Replacement is genuine, but it need not cost one event per pair.

Since all A labels in H are prefixes/suffixes, no interior B label between chosen outputs is ever A-present. The new class in Section 8 is EMPTY on H, including any other actual R pairs. This is an explicit limitation, not suppressed coverage.

### 7.2 Original W_pq and a complete persistent-obstruction control

Original W_pq stops its full adjacent descent at m=x_p and then uses the full increasing/reverse KEEP sweeps. Its critical whole-frame memberships and chosen-output chains are the original TF2/D1 ones. One must separately check output nonacquisition; whole-frame absence alone does not assert R.

A verified nonempty R control within original W is q=1, a_1=3. Before forward KEEP 3, A first splays 1 from its even two-vine root m, then splays 2. The first operation's nontrivial internal labels have minimum 2; at the second, nonsingleton proper labels with minimum 3 have upper endpoints 7,11,15,... or the boundary N (the singleton {3} is harmless). None equals [3,2^(j+1)+1], whose upper endpoint is 1 mod 4 and <N. The splay of actual target 3 cannot newly create a proper label containing 3. The critical prefix was two-vine. Thus all p selected chosen outputs are unacquired and their p-1 adjacent pairs belong to R. This is a symbolic path/parity check, not a replay.

For general q the complete critical restoration map still applies to every actual R subpair because it was proved for ALL critical demands, regardless of their later output visibility. No unverified forward A-output membership is promoted. The source theorem in Sections 8-9 is independent of the special family and covers any pairs satisfying the exact R predicate.

To test FULL-HISTORY persistent sharing directly, define a NEW complete word W_hit(p,q,i): insert KEEP a_i immediately AFTER W_pq's critical packet, before its full increasing KEEP sweep. All original W operations and both closing sweeps remain.

Its first hit for this selected column is now the actual added KEEP

    h=N+2^p.

The critical producers and nu/Gamma/F data are unchanged. A's vertex a_i is an ancestor of physical minimum 1 at every output birth. All intervening A targets are >=a_i, including the added target a_i, so that ancestry persists at EVERY rotation. Every cover of a chosen J_ji contains a_i, hence contains 1. Thus key 1 is a SINGLE persistent exterior obstruction for all p nested outputs on their ENTIRE birth-to-first-hit histories. None of them is A-acquired.

Whole-frame membership also survives. Their upper endpoints u_j=N-2^(j-1)>=m remain ancestors of N through the added access to a_i; during the full increasing sweep they retain N through their hit, then retain 1. The original other A phases are two-vine. Therefore F_ji is absent throughout the COMPLETE new period and every Pi. The p chosen outputs form the complete added-hit cohort, giving p-1 genuine R pairs.

The full increasing/reverse sweeps return BOTH complete trees to the original right vine from their new post-hit states. The source has empty prefix and length 3N+2^p-1. Its COMPLETE A cost is

    2(N-1)+(2^p-1)+ceil((m-a_i)/2)+C_new_forward,

where C_new_forward is the actual entire subsequent A increasing-sweep cost; it is included, not set to zero. The added jump has actual edge depth m-a_i. A finite direct upper bound C_new_forward<=N*ceil((N-1)/2) retains all that work. No bounded/unbounded R/A conclusion is inferred.

This realizes arbitrarily many residual pairs sharing one persistent physical obstruction, for arbitrary p. It refutes a constant load per obstruction KEY, not a cost theorem. Its large actual jump/reset work is preserved. The selected output roots are directly adjacent, so there is no intermediate B subtree in these selected gaps; these pairs remain outside the new controlled class.

### 7.3 Repeated 21-key source and the warmed-up repeat

Retain the complete original I^m Z construction:
T_10=19(-,20(-,21)), T_i=(2i)(2i-1,T_(i+1)), i=9,...,1. I is DELETE 4,6,...,18; descend 18,16,...,2 keeping only 18,16; KEEP 2,4,...,18; KEEP 16,14,...,2. Z is KEEP 1,...,21; KEEP 20,...,1; KEEP 19; then for k=1,...,9 KEEP 2k,2k-2,...,2. Both complete trees return to T. M=S=X=[21] and A=32m+A(Z), with all 87 closing operations counted.

For copy offset b=34(j-1), j>=2, d=(b+10,1) has F=[5,17], nu=B(b+10,1,0), chosen J=[5,11], and first hit KEEP 6 at b+20. D1 proves its complete cohort is a SINGLETON, so it supplies NO R pair. Neither its persistent leaf 7 nor its separately born companion [5,7] can be multiplied into collision obligations. New nonleaf births and different hit IDs are retained. Other actual R cohorts are subject to the universal theorem, not declared empty.

In the genuinely closed warmed repeat, original period A=2(2^p-1), KEEP support/carrier is {x_p,...,x_0}, and all unvisited physical low/gap subtrees remain intact. The period descends N,...,m keeping exactly those marks, then DELETE m+1,...,N. Its explicit legal prefix and complete B_p return are inherited from RG02; the excluded initial wide workload is NOT regenerated.

All A states are physical two-vines, so nonempty S labels are prefixes/suffixes. Hence every actual interior chosen output is A-unacquired, and all actual collision layers there are R. Intermediate labels strictly inside an interior J_+ are also absent from A; the new common-intermediate class is empty on this repeat. The old bound Q_B<=p(p+1)/2 and all actual fresh marked birth IDs remain. No q-sized workload is copied from the prefix.

### 7.4 CCR, AF, private ancestors and orientations

D1's exact current-domain check is retained: CCR's nine neutral whole frames leave only four possible interior demands, with chosen singleton labels {7},{11},{5},{9} and respective first-hit IDs 66,67,57,58 (last two cyclic). Distinct hits give E=R=0 even if all four pass their full Pi tests. AF's four fully neutral whole frames all contain min S=1; U_int=E=R=0. Their shared flag/blocker histories cannot be relabeled as residual pairs.

Those controls still refute arbitrary per-blocker/per-merger credit rules at their original scope. No new CCR/AF source run or full-window qualification is invented.

Private A vertices, duplicate SET representatives and S-free B hangers are included in (3.1) and the exact rotation table. The new necessity uses actual SET loss, not a private representative's movement. RR/LL/LR/RL only determine the inherited chosen B outputs; the subsequent A-cover and intermediate-label proof imposes no B-orientation restriction. No physical search edge is contracted.

### 7.5 A complete nonempty residual with an intermediate common subtree

The following NEW symbolic source W_star realizes the cost class of Section 8. It does not edit H or D1's witness. Start common A=B=V+(1,33), empty prefix, and use H_(3,1), whose critical KEEP targets are 33,32,30,26, with TWO A-only insertions:

1. Immediately after original KEEP 32 at t=34 insert P:
   DELETE 1,2; DELETE 1,2,...,33; DELETE 32.
2. Immediately after the original descending sweep reaches 1 insert Q:
   DELETE 11,10,1,2; DELETE 1,2,...,33; DELETE 32,31,...,1.
3. Retain every original H operation, including both full closing KEEP sweeps.

P has 36 operations and returns A to its complete two-vine state at root 32. Q has 69 operations and returns A to its complete right vine at 1. B is frozen during both. Thus all original KEEP post-A states and full B rotations agree with H, up to their explicit index offsets, and the COMPLETE pair closes to its common full right vine. X=M=S=[33]; all physical keys and costs remain.

The 235-operation original indexing is:

| Part | Exact original indices in W_star |
| --- | --- |
| H prefix through KEEP 32 | t<=34 unchanged |
| P DELETE 1,2 | t=35,36 |
| P ascending DELETE k | t=36+k, k=1,...,33 |
| P final DELETE 32 | t=70 |
| Original descending tail 31,...,1 | old t+36, ending t=101 |
| Q DELETE 11,10,1,2 | t=102,103,104,105 |
| Q ascending DELETE k | t=105+k |
| Q reverse DELETE k | t=171-k, k=32,...,1 |
| Original forward KEEP k | t=170+k |
| Original reverse KEEP k | t=236-k, k=32,...,1 |

#### The immutable R predicate, not a modified cohort

The critical chosen outputs are still

    d1=(34,7), nu1=B(34,7,0), O1=4(3,5), J1=[3,5];
    d2=(72,3), nu2=B(72,3,0), O2=P_3(6), J2=[3,9];
    d3=(76,1), nu3=B(76,1,0), O3=P_4(10), J3=[3,17].

Their whole frames are F1=[3,32], F2=[3,31], F3=[3,29].
Gamma1=B(33,15,1), Gamma2=B(34,7,1), Gamma3=B(72,3,1).

P intentionally makes F2 A-present at the actual rotation

    A(36,7,1).

It lies AFTER Gamma2 and BEFORE d2's producer-post-A state. Therefore d2 FAILS the original full Pi predicate and is NOT in U_int, although its producing double is still fully neutral. It was never a vertex of the current source's C_h.

Here is the exact A geometry. From the initial insertion state A32, DELETE 1 has depth 31; DELETE 2 then has depth 16, with seven internal LL doubles followed by a global RL. Its seventh LL bit 1 creates [3,31]. The resulting complete A is

    2(1,32(K28,33)),
    K4=4(3,6(5,7)),
    Kr=r(K_(r-4),(r+2)(r+1,r+3)), r=8,12,...,28.

No F1 or F3, and no J1 or J3, is created during these two accesses: first DELETE 1 gives singletons and labels with minimum 2; DELETE 2 gives first outputs [5+4s,7+4s], second outputs [3,7+4s], s=0,...,6, plus boundary labels containing 1 or 33. The forbidden upper endpoints 5,17,29,32 are not in that list with minimum 3.

Before reset DELETE 3, the only relevant nonsingleton labels with minimum 3 are those [3,7+4s] and [3,33]. A splay of target 3 creates no new proper label containing 3. Afterwards 3 is an ancestor of 1 through the remaining increasing scan, excluding all F1,F3,J1,J3. The final DELETE 32 returns the full original two-vine state. This proves the necessary absence at EVERY intermediate P rotation.

The original descending A tail is again two-vine. During Q's low accesses, the upper keys 29 and 32 retain N=33 below them; the subsequent increasing scan preserves that relation through their own hits, then preserves their ancestry of 1. Thus F1 and F3 remain absent at every Q snapshot. The original other phases were unchanged. Both F1 and F3 are therefore A-absent throughout the COMPLETE new period, hence their full Pi windows, while F2 has the explicit disqualifying presence. No new U_int demand can be added by extra A-only snapshots when all original phases agree; original memberships can only be removed.

D1's original complete three-output cohort at forward KEEP 3 thus becomes EXACTLY

    C_173={d1,d3}.

No exposed chosen vertex is deleted to form a new adjacency. The actual immutable U_int definition itself excludes d2.

#### Both chosen outputs stay A-unacquired

Q starts at the complete right vine. Its DELETE 11 has depth 10; DELETE 10 then has depth 5 and leaves

    A=10(4(2(1,3),8(6(5,7),9)),V+(11,33)).

At DELETE 1, t=104, its first LL rotation is RIGHT at g=4 promoting p=2, with middle subtree {3}. It deletes (10,4,LEFT),(4,2,LEFT),(2,3,RIGHT) and inserts (10,2,LEFT),(2,4,RIGHT),(4,3,LEFT). The inner cover shrinks from [1,9] to [3,9], while the outer cover stays S. It creates the ACTUAL A label

    K=[3,9], rooted in A at 4,
    r_create=A(104,1,0).

After DELETE 2 the complete A is

    2(1,10(4(3,8(6(5,7),9)),V+(11,33))).

None of Q's first four accesses creates J1=[3,5] or J3=[3,17]. Their displayed subtrees and direct RR/LL formulas show the relevant labels with minimum 3 are [3,10], {3}, [3,9] or [3,33], not those chosen endpoints. During the following reset splay of target 3, new proper labels exclude 3; afterwards its ancestry of 1 excludes J1,J3 through the increasing scan. The full reverse and original remaining A phases are two-vine. The P analysis already excluded J1 during the earlier inner-output history. Thus BOTH d1,d3 have v=0 over their OWN full birth-to-hit intervals.

At h=173 the full pre-B tree is

    2(1,26(18(P_4(10),P_3(22)),P_3(30))).

So rho=(h,d1,d3) is a genuine residual pair. The physical B root 6 has the strict intermediate label K=[3,9], with

    [3,5] strictly inside [3,9] strictly inside [3,17].

Its chosen birth B(72,3,0) belonged to the excluded d2, not an omitted U_int vertex. It stays physically rigid through the shared lifetime.

#### Actual A cover transition and compulsory common loss

At reset DELETE 3, t=108, the path is

    2 ->right 10 ->left 4 ->left 3.

Its first LL bit is the RIGHT rotation at 10 promoting 4, with the entire middle subtree 8(6(5,7),9). It SET-loses K at

    r_loss=A(108,1,0), Delta_A Psi=+1.

K was B-common at that moment (B root 6, A root 4). The deleted physical edges are (2,10,RIGHT),(10,4,LEFT),(4,8,RIGHT); the inserted ones are (2,4,RIGHT),(4,10,RIGHT),(10,8,LEFT).

For J1 the minimal A cover expands from K=[3,9] to [3,33]. For J3 its cover [3,33] is transported from root 10 to root 4 with the same S set. Both remain strictly larger than their chosen labels. Inner ring-only obstructions are replaced by a cover sharing exterior keys, including 33, with the outer cover.

K is never A-reacquired before h: after target 3, any A label containing 3 also contains 1 during the remainder of that increasing scan, and subsequent two-vines exclude K. Thus r_loss is the exact last loss used by Section 8.

#### Complete source cost

Every helper is counted. P's first two costs are 16 and 8. From its displayed K_r tree, its ascending DELETE scan has costs 9 on targets 1-4, 12 on 5-12, 12 on 13-20, 11 on 21-28, and 6 on 29-33: total 50. These follow by the literal LL/RL identities; its last DELETE 32 costs 1. Hence A(P)=75.

Q's first four costs are 5,3,2,1. Its ascending reset costs 5 on targets 1-4, 8 on 5-10, and 23 on 11-33: total 36. Its full reverse reset costs 32. Hence A(Q)=79.

For an additional cost check, in P's ascending reset the only targets with A cost greater than one are
3:5, 4:2, 5:3, 7:2, 9:2, 13:3, 15:2, 17:2, 21:2, 23:2, 25:2, 29:2.
Every other target costs one, giving 33+17=50. In Q's ascending reset only targets 3,5,7 cost two, giving 33+3=36. Their original operation IDs are t=36+k and t=105+k respectively; repeated target names do not identify events.


Therefore the COMPLETE admissible word has

    |W_star|=235, A(W_star)=128+75+79=282.

No critical access or helper interval is extracted as a closed source. These calculations are symbolic literal-tree identities, not an executed replay or a finite-sample argument for a universal claim.

## 8. A new actual A-work necessity theorem

### 8.1 Precisely defined source subcount

For rho=(h,d_-,d_+) in the ORIGINAL R, let I_rho be the shared interval from nu_+ just after birth to h's post-A/pre-B state. Define its actual intermediate B labels

    K_rho={K in J_S(B): J_- strictly inside K strictly inside J_+}.

Evaluate this list just after nu_+ in the ORIGINAL full B tree. These are the rooted labels of internal physical B vertices between g_+ and g_-. O_+ rigidity makes the list and complete shapes CONSTANT throughout I_rho; it is not recomputed on a projected tree. It can be empty, for example at a direct parent-child gap.

Put rho in R_sep iff SOME K in this list is A-present at SOME actual snapshot in I_rho. Put every other original residual pair in R_rem. Thus

\[
\boxed{R=R_{\rm sep}+R_{\rm rem}.}
\tag{8.1}
\]

The membership is independently testable from original source states; it is not one resource ticket per pair. W_star proves R_sep is NONEMPTY in the admissible model, while H and W_hit give arbitrarily long gaps outside it.

R_rem has an exact stronger obstruction: not only the two chosen labels, but EVERY physical B label strictly between them stays A-absent throughout their shared life. Its internal A covers may still have ring obstructions with incompatible/non-B label sets. Neither endpoints nor intervening B labels are permitted to acquire a common A representation there.

### 8.2 Source-forced loss, even if agreement predates the outer birth

For rho in R_sep choose the earliest actual shared-interval snapshot having such a common K; break ties by smallest K under the actual strict inclusion order (closest to J_-). Retain its original B rooted-label run and creation history. It is not newly issued at this witness.

K persists in B through h's A phase because all earlier KEEP targets are outside J_+. Its A representation exists at the witness. At h's post-A state the global A root x_h lies in J_- subset K, while K is proper, so K is A-absent.

Therefore there is a REAL original A SET loss of K after the witness and no later than that endpoint. Define b(rho) to be the LAST such actual SET loss in this original cyclic interval. This is a compulsory source event, not a conveniently postulated preparation. It remains valid when K was already common at nu_+ and no A acquisition occurred during this interval.

The current B label K is present at b(rho). D1/RG01's verified common-label sign law gives

    Delta_A Psi(b(rho))=+1.

Only one actual SET label can be lost by that rotation; duplicate private representatives are suppressed. No virtual bit, B transfer, release receipt or owner vacancy is counted.

W_star has its unique intermediate K=[3,9], first common at A(104,1,0), and exact b(rho)=A(108,1,0). Neither chosen output was A-acquired, so this cost is genuinely beyond the class discharged in D1.

## 9. Global overlap and quantitative calculation

### 9.1 One live intermediate label separates at most one active collision gap

Fix any actual A-rotation time s and a currently live B label K. Consider residual pairs active at s for which J_- strictly inside K strictly inside J_+.

For ANY such pair, the next as-yet-unperformed B phase with target inside K must be its common first hit h. An earlier such phase would already hit the containing J_+; its designated h itself targets J_- subset K, so it cannot precede that next K hit. The occurrence is unique.

This uses fine source chronology: if s is INSIDE h's A phase, its B phase is still upcoming and is included. Cyclic wrapping names one existing original KEEP/B phase, not another copy.

Thus all such pairs have the SAME h. At h they belong to one FULL strict chain of chosen outputs. A fixed strict intermediate label K can lie between only ONE consecutive pair of that chain. Two different gaps would require incompatible strict inclusions.

This proves the source-uniform active-gap uniqueness. It uses actual first hits and adjacency; abstract interval nesting alone would not suffice.

### 9.2 The original-event selector is globally injective

If b(rho)=b(rho')=r, the original real A rotation r loses just ONE actual SET label K. Both pairs' chosen outputs are still active at that time, and their chosen intermediate K is that same current B label. Section 9.1 makes the common hit and consecutive pair identical. Hence rho=rho'.

For EVERY original real A rotation r,

\[
\boxed{L(r)=\#\{\rho\in R_{\rm sep}:b(\rho)=r\}\le1.}
\tag{9.1}
\]

This is global over ALL cohorts, repeated labels, root epochs, helpers, sparse supports and cyclic seams. Temporal intervals need not be disjoint. The property is not a per-cohort congestion estimate.

Consequently, with P_A the count of original positive real A rotations,

\[
\boxed{
R_{\rm sep}\le P_A\le R_A=2A-V_A\le2A,\qquad
R_{\rm rem}\le R\le2A+R_{\rm rem}.
}
\tag{9.2}
\]

Every counted positive bit remains an original physical operation, possibly already g_1-owned. The statement counts cost and does not make it a vacant payment head.

### 9.3 Interface with D1's real-event association

There is also a concrete noncollision fact: a new b(rho) cannot equal a D1 acquisition a(d), since their signs differ. It cannot equal a D1 loss b(d) either. Such equality would make the lost K the label of a STILL-UNHIT chosen output d. Its first hit would be the same next K hit h, placing d strictly between rho's two allegedly consecutive cohort vertices, a contradiction.

This proves compatibility of these particular original-event images. It is retained as an interface, not an execution of D3, an ownership reallocation or a universal bound on the remaining gaps. Arbitrary existing g_1/raw payments and unrelated classes are not declared free.

The failed broad cover-loss selector from H remains refuted. The new theorem has the ESSENTIAL source restriction K strictly between the endpoints, which is exactly what makes the original gap unique.

## 10. Explicit proof-relevance verdict

The quantitative result is SOURCE-UNIFORM and strictly inside D1's unchanged R:

\[
R=R_{\rm sep}+R_{\rm rem},\qquad R_{\rm sep}\le2A,
\]

with L(r)<=1 for the actual positive A SET-loss selector. R_sep is realized by the ORIGINAL tuple

    rho=(173,(34,7),(76,1)) in W_star,
    intermediate K=[3,9], b(rho)=A(108,1,0).

Both chosen output labels are A-unacquired; this is not a reapplication of D1's exposed-output bound. The middle candidate d2=(72,3) is excluded by its ORIGINAL full whole-frame Pi test, not deleted from a fixed cohort after seeing the desired adjacency.

The paid subcount has a proved physical cost event, nonempty source-realized coverage, global multiplicity and uniform coefficient. The new complement has an exact stronger source predicate: every intermediate B rooted label in the rigid gap is also A-unacquired during shared life. W_star proves the two classes are a proper distinction. H/W_hit show the remaining domain is substantial.

No unrestricted R/A bound, contraction, or unbounded R/A family is obtained. No new B identity, fixed obstruction count or family-only restoration map is substituted for that missing theorem.

At the stated partial-result scope:

| Check | Result |
| --- | --- |
| Source validity | PASS: physical LCA/rotation identities, original SET semantics and actual full closed words |
| Membership/coverage | PASS: exact original R retained; R_sep and R_rem partition it; W_star supplies an actual pair |
| Quantitative effect | PASS: one mandatory positive real A loss per controlled pair, globally injective |
| Global overlap | PASS for R_sep over every original cohort and cyclic seam; no bound asserted for R_rem |
| Noncircularity | PASS: cost proof uses actual common K, forced loss and first-hit gap uniqueness, never a desired R/A bound |
| Known controls | H's shared cover loss remains an exact counterexample to broader rules; W_hit realizes persistent sharing; singleton/empty controls are not relabeled as R |
| Uniformity | PASS: load 1 and coefficient 2 are independent of size, support, depth, helpers and source length |
| Verification level | Same-agent symbolic only; no independent/formal certification or empirical all-tree inference |

## 11. First unsupported implication

The remaining gap is now precisely a R_rem pair whose TWO chosen output labels and EVERY B rooted label strictly between them remain A-absent during shared lifetime.

A can still have covering subtrees with exterior keys; such covers may surround the whole gap, or sit within the outer interval with S labels incompatible with the intermediate B labels. Their changes force real rotations, but the one common cover can serve arbitrarily many pairs. Direct parent-child gaps have no intermediate label at all, and therefore no internal common SET loss to select.

The first unproved source implication is that creation/reuse of these fully unacquired B gap segments forces additional ORIGINAL A preparation/restoration elsewhere, with a uniform multiplicity across all such gaps. It is NOT proved by:

* distinct B births or distinct enclosing roots;
* existence of a last A-cover enlargement;
* counting an exterior obstruction key;
* restoring B to an earlier full state without tracing A;
* the restricted dyadic spacer restoration injection.

H supplies the exact broad-loss collision, and W_hit supplies full-history persistent-key sharing. Those failures do not refute R_rem<=cA or R<=cA. Conversely the new controlled class does not prove either.

The unresolved burden is still a source-cost necessity for the stronger gap predicate, not merely adding already known budgets. A later authorized gate would need that additional theorem or a genuine complete unbounded-ratio family. No replacement potential, matching conjecture or automatic fallback is executed here.

## 12. Dependency and verification ledger

### 12.1 Proof dependencies

    original Pair Access/SET model + current D1 definitions/proof
        -> exact R and rigid shared B gap;

    physical endpoint LCA
        -> correct absence/cover characterization
        -> exhaustive literal A-cover transition table;

    actual intermediate B label K becomes A-present
        + first-hit A root inside K
        -> mandatory positive A SET loss before that B hit;

    K strictly between adjacent chosen outputs
        + same next inside-K B phase
        -> one active original gap per K
        -> global real-event injection and R_sep<=2A.

The last two arrows do not use the desired R/A bound, any resource inventory or a source-size-dependent parameter. H/W_hit and W_star are adversarial/nonvacuity checks, not evidence substituted for the universal proofs.

### 12.2 Required proof-debt fields

| Field | Exact D2 record |
| --- | --- |
| Proven inputs | D1 E=E_ctl+R, E_ctl<=2A and exact chosen-output/cohort histories; original full physical Pair Access/carrier/SET model; R_A=2A-V_A; original family closure facts |
| New theorem | A-cover equivalence and literal cover transitions; one active adjacent cohort gap per strict intermediate B label; actual common-intermediate loss injection |
| Quantitative effect | R_sep<=P_A<=R_A<=2A, with L(r)<=1 globally; exact R=R_sep+R_rem |
| Surviving residual | Original R pairs for which every B label strictly between the two chosen outputs is absent from A throughout shared life |
| Global overlap | PROVED for the new positive-loss image; its noncollision with D1 endpoint images is proved; unrelated historical owner vacancies are not claimed |
| Source counterexample | Complete H_pq gives p-1 uses of one common cover loss; complete W_hit gives p-1 pairs with one persistent obstruction; neither yields unbounded R/A |
| Source-realized coverage | Complete 235-operation W_star, A=282, with rho=(173,(34,7),(76,1)), K=[3,9], loss A(108,1,0) |
| Dependency status | D1 audit passed; D2 subcount discharged; no universal R_rem bound, no D3/P1/V1/P2/RG05 execution |
| Verification level | Same-agent symbolic proof and static manuscript/input checks; no independent agent, formal kernel or source replay |
| Main theorem effect | A new nonempty universally bounded portion of R is removed; unrestricted R/A, E/A and URCD remain OPEN |

### 12.3 Scope, boundary and negation audit

The cover theorem includes singletons, sparse S, private LCA vertices and duplicate labels. The rotation table includes roots, empty middle subtrees and unchanged ancestor/outer structure. The cost selector uses an ACTUAL SET loss, so representative motion or private-only changes create no false event.

R is empty when G0 gives no interior demands; in particular A=0 forces R=0 before ratios are considered. Identity KEEPs and DELETE helpers remain in source chronology. A selected loss can be in an intervening helper or in h's own A phase. The first upcoming INSIDE-K B phase is the precise operation boundary used by the overlap proof.

Cyclic lifts contain each original event once. Equal labels in later B runs do not share the current loss. A persistent B edge is not reissued at the seam; a proper K containing the eventual hit cannot persist unconsumed through that hit.

The new theorem's exact negation is a source with R_sep>2A (or two different eligible pairs assigned to one real loss under the fixed rule). Such a collision would require the same lost K to separate two different consecutive gaps with the same next inside-K B hit, contradicting the literal source-order argument. Known broad-loss counterexamples fail the strict-between eligibility, which is why they remain outside the proved class.

The broad selector's refutation is parametric: for every claimed finite load L choose p-1>L in H_pq. W_hit's persistent-key count likewise has arbitrary p. Full source costs/closing work were retained; neither finite example nor these bad selectors is called a refutation of the universal cost target.

### 12.4 Current input bytes and preservation

All sixteen read-only input hashes were rechecked after constructing the manuscript and matched their initial pins. These byte records identify inputs, not independent mathematical certification.

| Input | SHA-256 |
| --- | --- |
| [IAGS12_D1_COLLISION_PROVENANCE.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/IAGS12_D1_COLLISION_PROVENANCE.md>) | `0aa9cbf3e9cc036af5d4bbdf3ea3acdfcbef9341c856401b74247a615c4f814f` |
| [IAGS12_G0_QUANTITATIVE_BASELINE.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/IAGS12_G0_QUANTITATIVE_BASELINE.md>) | `09863af3277745f5ebef956e680feb43a3d1ad4e5c7bb57bb545918c4813523a` |
| [RG01_PRIMITIVE_ACCOUNTING.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG01_PRIMITIVE_ACCOUNTING.md>) | `f46c0ee4e549ee8223bd97e4e28b364e415566129ad09df32558f5819500d7fa` |
| [RG04_GLOBAL_REGENERATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG04_GLOBAL_REGENERATION.md>) | `52072e0c9a5214cf16b7bf44e3efb09df102e91e939bf3186b2e280b0763832b` |
| [RG02_EDGE_CONSERVATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RG02_EDGE_CONSERVATION.md>) | `16b93dbe5fa80a75da0591ad79765581ffc8a8c826b6f41758e985270de2253e` |
| [TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_TF2_AUDIT_AMPLIFICATION_20261109/TF2_INDEPENDENT_AUDIT_AND_PARAMETRIC_AMPLIFICATION.md>) | `1c31d4b5d8c97771640e5235e2015a95b584753d42ada4987600d071d8466176` |
| [UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_UNIVERSAL_SOURCE_WORK_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_PROOF_OR_REFUTATION.md>) | `4cf67ae246987f211997e18a5efb5b6d37ab9afbf800777769bbd2f56de5d42a` |
| [UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/ROUTE02_ROUTE04_REGENERATION_CONTINUATION_20261109/UNIVERSAL_INTERIOR_SOURCE_WORK_REGENERATION_CONTINUATION.md>) | `50e90e4471b1f794ba58f848f44522dc71ac74685ed9f81e09593cfb11e871d0` |
| [STEP3_1B_NECESSITY_CONTINUATION_02.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_02.md>) | `9b784193b5d68bc0fc358ca09204ff4ebacb69ba1db0fabce422cf97ff98a1e3` |
| [STEP3_1B_NECESSITY_CONTINUATION_03.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_03.md>) | `00a004ec6f55fbe3e4e7bc8c4866782f428edbcbc40f1eb7c4903e46769e2059` |
| [STEP3_1B_NECESSITY_CONTINUATION_04.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/STEP3_1B_NECESSITY_CONTINUATION_04.md>) | `e247f175606d377ee359d89fce487e4985ab885726ef126abb35ccfde5c6e08d` |
| [STEP01_ATTACHMENT_TRACE.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/PARALLEL_ROUTE02_ATTACHMENT_TRACE_20261108/STEP01_ATTACHMENT_TRACE.md>) | `fc07769642f6b08f35f6d6cfdd45290f740772556d7ad754757eb94a3a9949b4` |
| [RESEARCH_RULES.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/RESEARCH_RULES.md>) | `c6b35f746f107ad8a1c226aefdb2b43711a4982fd9717fe513d7080f25d299bc` |
| [Pasted text.txt](<C:/Users/Saif malik/.codex/attachments/51aa6fac-c023-4ac1-a193-4c30d9c4ac84/Pasted text.txt>) | `eed4e967c16fbbce25e42cee06c66e6be8bebbd4bfe8f2bf0b846e80f30b239d` |
| [U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/run_20261030_v001/U4_02_ORIGINAL_PAIR_ACCESS_SPEC.md>) | `8be55471edfdac31f59d552952c84f8d380bbfa3a7e46b7643d22af766757fd5` |
| [SOURCE_SPEC.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/SE03_STEP3_RECURSIVE_SOURCE_CLOSURE_35/ND35_COMPLEMENT_08/SOURCE_SPEC.md>) | `a52487cfe212aa562b91406bb6006d2f9a9469bebcfd4e039d9cd224fc6d677b` |

Verification used symbolic checks of the LCA-cover equivalence, all A-rotation cases, exact D1 membership and images, the upcoming-B-phase uniqueness at losses inside h's A phase, W_star's two excursions/full windows/costs, persistent-blocker W_hit, and all claimed source scopes. The new text was read back against the constructed manuscript; formula tags, table columns and stop conditions were checked. No source program was executed to establish any claim.

Tracked Git diff remains empty; HEAD is unchanged at 6d532b2c795c0778f57d8023b23b5fedfc48b010 on coarse-double-branch. All prior untracked entries remain as found, with only this new IAGS12_D2_RESIDUAL_REGENERATION_COST.md added. Source-engine query/replay/experiment/solver/independent-agent calls are ZERO. Original source artifacts, owners and cumulative resource caps were not modified.


## 13. Final D2 status

**D2: QUANTITATIVE PASS — partial source-uniform reduction, same-agent symbolic.**

Discharged: residual pairs with an A-present intermediate B subtree have distinct compulsory original positive A SET losses, giving R_sep<=2A with load ONE per real A rotation.

Remaining: pairs whose entire intervening B-label gap, as well as both chosen endpoints, remains A-unacquired during shared life. No absolute cost bound for that remaining class is certified.

This is a valid nonempty subcount theorem beyond D1. It is NOT a full R<=cA theorem, not a URCD proof and not independent certification. No D3, P1, V1, P2 or RG-05 is executed. Stop after this report.
