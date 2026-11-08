# A two-credit relay for marked-ancestor grandchild zeros outside S

This theorem covers a restricted same-direction class with BOTH ancestors
marked. It preserves every completed LOW row and proves a new uniform
original zero-H1 class outside S. It is not complete marked-ancestor
coverage, a numerical fit, or a finite test.

## 1 Public classes and explicit debt

Reuse full states s=(mu,b_state,alpha7,sigma), the valid nine-core
projection, set-valued V, psi,Lambda, all old totalizations and D_grand.
All roots below are A/B synchronized Scores and all a,b,c are marked.
Every nonroot specified Score position has kind0,isS=true. Root's UNUSED
kind, all other unused fields, raw gap/NULL side pairs and annotations
are unconstrained except by original typed validity.

Smaller-end orientation: a<b are the TWO SMALLEST marked labels,
b in{4,5}, c>b is marked, and c-b<=3. Define:

 J_minus: root a; Score b at A R and Score c at RR;
          core B has root a, right child b, and b.right child c.
          NO V filter, opacity guard or other A restriction.

 G_minus: root c; Score b at A L and Score a at LL;
          alpha LR and R are nonreal(kind1 PORT or kind2 EMPTY);
          core B has root c, left child b, and depth_B(a)=4.

Larger-end actual orientation: a>b are the TWO LARGEST marked labels,
b in{3,4}, c<b is marked, and b-c<=3. Define:

 J_plus: root a; Score b at A L and Score c at LL;
         core B has root a, left child b, and b.left child c.
         NO V filter or further A guard.

 G_plus: root c; Score b at A R and Score a at RR;
         alpha L and RL are nonreal;
         core B has root c, right child b, and depth_B(a)=4.

Let J,G be the respective unions. These are predicates on FULL original
states; neither private inventories nor their ranks, gaps, port labels,
support or anonymous identities are read. Every arbitrary remaining
compatible core subtree and every admissible signature is included.
No claim says every signature realizes every guard.

For ANY public Lambda<=D<=2 apply IN ORDER:

    D1=max(D,2*1_J),
    F =max(D1,2*1_G).                            (1)

THEOREM. Each operation preserves EVERY original LOW inequality valid
before it, individually, without assuming global feasibility. Every
J-source and G-source LOW row is valid for final F. Every G-source zero
marked-grandchild H1 edge has F(s)=F(t)=2 and residual exactly0. All
nonnegative incoming LOW rows to J union G are valid by range.

For the current input set

    D_marked=max(D_grand,2*1_J,2*1_G).            (2)

All previous S, child, unmarked-ancestor, negative H1 and other completed
LOW rows remain valid. Invalid-core totalizations stay unchanged because
both new predicates require a valid core projection. All new caps are
literal public values even at boundaries without a fresh source witness.

## 2 Two credits on J: every H1 exit

Start with an ACTUAL J_minus source. The strict distinct Score observations
give actual present a,b,c. A G fallback reports source slot0=a and cannot
fabricate b or c. The source A prefix is

    a(A,b(B,c(C,D))).                            (3)

Every other mark exceeds b, since a,b are the first two. Thus the left
subtree A and the middle block B contain no other PRESENT marked Score.
All other marks, if present, are below c at source depth>=3. A fresh source
G reads a, or under a ghost left child reads b; these introduce only a
or duplicate b. Actual active paths and target cover therefore make b,c
the only genuine marked H1 targets. This is proved on each fresh source,
not inferred from a preceding edge's private completion.

The core B has the independent exact prefix

    a(L,b(M,c(N,P))).                            (4)

Their original prices are w_b=2 and w_c=1. The b exit is range-safe
from debt2 regardless of its endpoint. For c, the exact paired identity is

    a(L,b(M,c(N,P))) -> c(b(a(L,M),N),P).         (5)

Old a,b have depths2,1. Every other marked label exceeds b. For a key k
strictly between b,c, its entire core subtree N has c-b-1 keys and is
attached at depth2; hence

    depth_after_c(k)<=c-b<=3.                    (6)

For a key k>c, the right subtree P contains8-c cores and starts at depth1,
so depth_after_c(k)<=8-c<=3 because c>=5. Empty intervals have no such
key, so there is no empty-subtree off-by-one premise. All marked keys,
including a,b, consequently have final core depth<=3.

This is a count bound on arbitrary subtrees, not a census of core shapes.
The bound applies to EVERY marked label in the full target, including
newly exposed marked nodes or G duplicates. The target belongs to E1,
so its already completed Lambda floor is>=1. Therefore the actual +1 row
has residual 1+D1(t)-2>=0. This proves all J_minus H1 rows at source2.

The ACTUAL J_plus source has core and A prefix a(b(c(...),...),...),
with c<b<a. Its c access gives

    a(b(c(L,M),N),P) -> c(L,b(M,a(N,P))).         (7)

All other marks are below b. Keys below c have final depth<=c<=3,
and keys strictly between c,b have depth<=b-c<=3. Old a,b again have
depths2,1. Thus every marked key has depth<=3 and the same E1 credit
repays the +1 c exit. The b exit has weight2. This is a separate actual
LOW orientation proof; no psi labels, hidden weak-LE ranks, HIGH data
or endpoint annotations are reflected.

## 3 J Gamma1 helpers, including Score-bearing support

In(3), an anonymous source node at RL lies strictly between present
Scores a,b, so it is in an interior gap and cannot be an extreme Gamma1
helper. The R/RR positions are Scores b,c. Any anonymous L/LL/LR target
lies below present Score a and cannot be a maximum-gap helper. Therefore
the original complete Gamma1 form, if it occurs, starts with a MINIMUM
helper f at L/LL/LR, of source A charge1.

That left-side helper leaves the ENTIRE old right b/c block attached to
old a.right, moving it deeper. Old a has actual A depth1/2 after this
first charge1 splay; b has depth2/3 and c has depth3/4. Every other present
mark was below c and stays deeper still. Thus the only possible marked
terminal of A charge1 is old a or b. If b has depth3 it is ineligible,
which merely removes that possibility. No other terminal is invented by
a port or shadow alias; verified original active paths remain required.

In B, reuse the completed minimum-proxy last-step lemma: after the
minimum-gap access, old root a has depth<=2. Its old right child b and
the whole attached block are untouched except for that increase, so
depth_B(b)<=3. This holds for EVERY initial minimum-proxy path length
and every private Score support, not only an initially Score-empty helper.
For terminal a or b the ORIGINAL terminal-only price obeys

    q=floor(depth_preterminal/2)<=1,
    w_H2=4-q>=3.                                (8)

Range2 alone proves its inequality even after raising the source to2.
No helper-plus-terminal charge sum replaces q. Final gap-leaf validity
may exclude some witnesses; the bound applies to every witness that
survives. No new final-gap property is assumed here.

For J_plus the available extreme helper is a MAXIMUM in R/RR/RL.
The entire old LEFT b/c block moves deeper; terminal choices are again
old a or b. The completed maximum-proxy root bound puts old a at<=2
and old left child b at<=3. Equation(8) applies in this actual orientation.
The other anonymous middle interval is strictly between present Scores
b,a and cannot be either extreme. No private assignment is reflected.

All Gamma0 H2 rows retain the completed ACTUAL preterminal psi-floor
proof for any public psi<=D1<=2, even if DELETE/core-prefix operations
expose hidden marked nodes. No terminal-only-b/c assertion is made for
Gamma0. Original H0/other-form exclusions and H1/H2 coverage are reused.
Thus EVERY J-source LOW row holds at source2.

For a previously valid row whose source is not raised, only a nonnegative
target increment is added. A raised source is in J and all its original
LOW rows were just proved. Hence the FIRST operation in(1) preserves
every formerly valid original LOW inequality, individually.

## 4 The marked-grandchild zero lands in J

At an ACTUAL G_minus source the A prefix is

    c(b(a(A,B),C),D), C,D nonreal.              (9)

Distinct marked a,b,c are all genuine Scores, so both ancestors are
marked. Its only nonroot observed marked targets are a,b. All other
positions are opaque or under an opaque prefix. H1 normal form retains
the SAME full endpoints,H and terminal q, including charged DELETE/zero
terminal KEEP. Its a price is0 because depth_coreB(a)=4, and its b price
is2 because b is the immediate B child.

The exact A pair is

    c(b(a(A,B),C),D) -> a(A,b(B,c(C,D))).         (10)

The core path starts c,Lb,L... because a<b<c and b is immediate. The
target a is at depth4. Consume its arbitrary bottom pair: a replaces the
old depth2 subtree root, with arbitrary processed left/right blocks. The
remaining top path is EXACTLY c,Lb,La, so its final pair is

    c(b(a(L,M),N),P) -> a(L,b(M,c(N,P))).         (11)

Thus b,c have B depths1,2 and the root is a. Combining(10)-(11), the
literal full destination satisfies J_minus. No endpoint is replaced by
a shadow quotient and no fresh completion is required at that target.
All original raw children/annotations and the source/target sigma remain.

NO V filter is imposed on J. A newly exposed A or B G may report old
marked c at target L or RL; this could be incompatible with a fresh
source prefix rooted at a. It still is a full target and receives the
public cap2. The fixed Score observations b at R and c at RR remain true,
and every other field is free in J. No boundary is silently discarded.

Therefore the weight0 a exit ends at D1=2. Raising its source to2 leaves
residual0. The b exit has weight2 and is range-safe.

For G_plus the actual source A pair is

    c(A,b(B,a(C,D))) -> a(b(c(A,B),C),D),        (12)

with A,B nonreal. Its depth4 core access has top pair c,Rb,Ra after the
arbitrary bottom pair, giving the same mirrored CORE topology as(12)
with arbitrary blocks. It lands in J_plus with b,c depths1,2. The weight0
a exit again has source/target2; the weight2 b exit is range-safe.

These two exact zero relays are valid for arbitrary compatible original
core subtrees and signatures. The depth4 guard is essential to this
proof: depth5 leaves a different final step and is NOT declared covered.

## 5 G H2 and the second safe operation

At a G source every ACTUAL real node at source depth1/2 is Score a or b;
all other observations have nonreal kind. There is no actual anonymous
source target for the first charge1 step of Gamma1. Consequently Gamma1
cannot start in either orientation, irrespective of anonymous payload
below a or in the opaque cuts. Anonymous source nodes below a at depth3
remain allowed and are not erased from the original graph.

Gamma0 retains its original actual-preterminal-floor proof, which applies
to any public psi<=F<=2 even if other H2 operations expose new marks.
Together with the two H1 exits this proves EVERY G-source LOW row at
source2, once J was saturated first. A source unchanged by the G operation
only gains a target increment. Thus the SECOND operation also preserves
every previously valid row. In particular it preserves all newly proved
J-source rows as well as the original completed rows.

No assumption that the input D was globally feasible has been used.
No new unproved compensation object was selected. For final F every
J/G source has value2, so every nonnegative incoming original LOW row is
range-safe. Negative incoming rows receive no new blanket claim, but all
previously valid ones are preserved by the preceding argument.

## 6 Outside S, nonvacuity and upward connection

In G_minus the root is c>b>=4, so c>=5. It is not second-smallest b,
as required by S_minus; it cannot be S_plus's central second-largest
root in{3,4}. G_plus has c<b<=4, so c<=3; it is not second-largest b
and cannot be S_minus's central root in{4,5}. Thus ALL new main G rows
are outside S. J roots are the minimum/maximum mark, also outside S.

For analytic nonvacuity use nine formal ordered Score roles

    l0<l1<l2<l3<b<c<u<v<w,

with marks l0,b,c,u,w and a=l0. The roles fix b at ordinal4 and c5;
they are theorem variables, not sampled numeric trees. Give A proper
prefix c(b(a(A,B),C),D), where B hides l1,l2,l3 in its ordered port,
C is a compatible nonreal cut and D hides u,v,w in a port. The core B
has path c,Lb,Ll3,Ll2,La; l1 lies in a compatible side block and upper
u,v,w have arbitrary compatible topology. This is an original A depth2
and B depth4 marked access, H=1,q=2,w=0, with marked root and parent.
Standard source-port realization supplies compatible full witnesses,
including sigma0; no source root or potential label is evaluated.
The actual upper-end ordered construction proves nonvacuity there too.

No strict numerical increase over old D_grand is alleged without a
completed psi fact. The advance is the uniform original-row theorem and
the explicit safe two-credit relay; the old rows were not claimed invalid.
The proof never queries a saved label or fits a new finite certificate.

Use inherited HIGH/h0 glue with W(O)=-D_marked(O)-5chi8 and W(M)=-5chi8.
Walks whose LOW rows have prior coverage, J/G sources or nonnegative
incoming J/G targets have weight>=-7; fully closed such walks have
weight>=0. Full147-O/127-M closure, SAME actual midpoint, independent
private scopes, high v free, weak LE/G/raw unused fields, original H/q/
prices and h0(actual0,declared18,q9,w=-3) remain. The graph itself is
not restricted to those walks and global M3 is not inferred.

BEFORE: S, child and unmarked-ancestor grandchild classes were complete
only on their own domains. RESULT: the ordered J/G saturation proves the
new marked-root/marked-parent depth4 grandchild zero family outside S,
and all its J/G-source LOW rows, preserving every completed row. AFTER:
delete precisely those G zero obligations and the stated incoming
nonnegative obligations. No new global existence premise is introduced.

Depth5, larger marked spans, zigzag marked ancestors, other unprotected
grandchildren/children and remaining cheap helper transfers outside prior
coverage remain OPEN. No exhaustive remaining-case count is asserted.
Full zero LOW, M3 and Dynamic Optimality are OPEN. No whole-signature
certificate or original negative cycle is newly certified. R1-R4 and
current caps are retained; the separate audit is recorded independently.
