# Completing the central marked-ancestor relay at B depths four and five

This is a restricted original-LOW theorem, not exhaustive Step4. It closes
the full central same-direction class from Transfer11, including depth5
and both exceptional endpoints. The separate coverage audit retains the
user's request to complete Step4 and identifies what is still unproved.
No finite tests or new saved-potential queries are used.

## 1 Main class, public construction and quantified input

Use full original states, valid nine-core projection, psi,Lambda and the
current D_marked. Start with ANY public D_marked<=D<=2; global feasibility
is not assumed. Existing invalid-core totalizations remain. Every named
Score occurrence is kind0/isS=true; root's unused kind, nonreal unused
fields, raw gap/NULL pairs and annotations retain original freedom.

At the smaller end let a<b be the TWO SMALLEST marks, b in{4,5}, and
let c>b be marked. Define main G45_minus by:

* synchronized marked root c; A L=b, LL=a, nonreal LR and R;
* core root c with immediate left child b;
* depth_B(a) is4 or5. There is NO c-b span restriction.

G45_plus is the ACTUAL opposite orientation: a>b are the TWO LARGEST
marks, b in{3,4}, marked c<b; root c, A R=b/RR=a, nonreal L/RL;
core c with immediate right child b and depth_B(a)4/5. All compatible
remaining core subtrees, original raw fields and admissible signatures
are universal. No claim says every signature realizes every guard.

Write E for CORE-empty and L for the four-core subtree0..3. The old
named direct cores are

 J5=5(4(L,E),8(6(E,7(E,E)),E));
 J6=6(4(L,5(E,E)),8(7(E,E),E));
 J7=7(4(L,6(5(E,E),E)),8(E,E)).                 (1)

Define the following new public classes in the smaller-end orientation;
all have synchronized marked roots and no V filter.

 Bdry: Transfer05 Z's Score4-at-LL predicate, or Transfer08 G_B's
       Score4-at-LL branch, dropping ONLY its V subset{4..8} condition.
       Every other old core/mark/depth guard is retained.
 Rsh: first two marks a<4; core J5/J6/J7, A L=4/LL=a,
      depth_B(a)<=2. The root is the named marked5/6/7.
 Q8: first two marks a<4, marked8; core8(4(L,U),E), U any core tree
     on5..7; A L=4/LL=a, depth_B(a)<=2.
 P8: mu={a,4,5,6,8}, a<4; core8(4(L,7(5(E,6(E,E)),E)),E);
     A L=5/LL=4 and depth_B(a)<=2.
 C5: first two marks a<4, marked5; core4(L,5(E,U)), U any tree on6..8,
     L rooted at a; A L=a/R=5.
 C8: first two marks a<4, marked8; core4(L,8(U,E)), U any tree on5..7,
     L rooted at a; A L=a/R=8.
 K: first two marks a<b, b4/5, marked c>b; root a; A R=b/RR=c;
    core a(L,c(b(M,N),P)), or
         a(L,c(q(M,b(N,P)),Q)) with a<q<b.
    q is a public unmarked Score, automatically unmarked by the pair order.
 J8: first two marks a<4, marked8; root a, A R=4/RR=8,
     core a(L,4(M,8(U,E))).                       (2)

All letters for side subtrees other than the explicitly specified bands
are arbitrary compatible CORE blocks. The shallow guards in Rsh/Q8/P8
mean that a is L's root, since 4 has core depth1. C5/C8 likewise require
that actual core child on the lower side. A fields not named are free;
in particular no opaque cut, port identity, private support or persistent
completion is imposed on any return class.

Include the actual upper-end classes, defined on original fields by
reversing constructor arguments and Score ORDINAL roles:4 fixed,
5/6/7/8 become3/2/1/0, smallest a becomes largest a>4, L becomes its
arbitrary upper four-core block. Directions exchange and first/last pairs
exchange. For K use c<b<a, b3/4, a>q>b in its three-level case. These
are actual predicates, not a map on weak-LE witnesses, psi or HIGH data.

Apply public cap2 operations IN ORDER:

    Bdry, Rsh, Q8, P8, C5 union C8, K, J8, G45. (3)

Each operation is Dnext=max(Dprevious,2*1_region), using its two actual
orientations. Let D45 be the resulting explicit maximum with D_marked.

THEOREM. Each operation preserves every original LOW row valid before
it, individually. Every source row in the new regions holds for D45.
Every G45 zero marked-grandchild H1 row has D45(s)=D45(t)=2 and exact
residual0. Every nonnegative incoming LOW row to these regions is valid.
No blanket repair of previously invalid negative incoming rows is claimed.

## 2 Boundary completion changes no actual LOW source

Consider a source with root c>4 and an actual Score4 at A LL, reached
through kind0 L. Both observations are actual: a ghost L reads root c,
and its LL reads that same root's left reference, not distinct4. Strict
present order puts every present marked a<4 under4.left at depth>=3.
All other marks are in U={4,5,6,7,8}. Actual source V therefore cannot
contain a. G also cannot fabricate it: slot0 reads c; a ghost right
parent reads root.left, the ancestor of4 and hence either anonymous or
a Score>4. Single ghost children read c. Nonreal prefixes propagate kind.
Thus V subset U holds at EVERY ACTUAL source satisfying these guards.

At such a source Bdry is exactly an old Z or old G_B source. The current
D_marked already equals2 there and already proves its outgoing LOW rows.
For any D>=D_marked with range2, that source stays2 and targets only gain.
Every extra Bdry point has no compatible original LOW source witness.
Consequently saturating Bdry changes NO actual LOW source value, only
possibly increases destinations. Every old valid LOW row is preserved;
all actual Bdry-source rows remain proved. No vertex or edge is deleted.

The ACTUAL upper-end proof uses Score4 at RR: largest mark a>4 must be
below4.right at depth>=3; a ghost left parent reads a node<4 or anonymous,
not a. V lies in0..4 at every actual source. The same old-cap argument
applies to its literal boundaries. HIGH remains governed by range/floor.

## 3 Shallow direct returns Rsh and the Q8 flank

At Rsh, a has core depth2 and actual A LL. Its weight1 access has the
exact pair c(4(a(A,B),C),D)->a(A,4(B,c(C,D))). The core pair is the same
because a is the lower core child of4. The full endpoint has root a,
Score4 at R, Score c at RR and B depths1,2. For c5 it is the completed
Transfer05 one-credit K; for c6/7 it is the completed Transfer08 K_B.
Those predicates have NO V filter. Their existing credit>=1 repays +1.

All other Rsh H1 targets are upper keys. Reuse the SIX completed +1
upper exits of J5/J6/J7; each has every upper core at depth<=3 and old4
at depth<=2. The newly imposed L-root-a condition puts a at<=3 too.
Thus every marked label in the actual full endpoint has depth<=3 and
the existing E1 floor is>=1, even if it is newly exposed or a G duplicate.
Weight2 exits are range-safe; no zero/negative H1 exit exists here.
The completed parametric helper barrier (Transfer07 Section3) applies
to every core c(4(L,T),R) with A Score4 at L, without an extra A guard:
every Gamma1 row has weight>=2. Gamma0 uses its actual-preterminal floor.
Therefore Rsh tolerates source2. Its upper-end proof uses the six actual
opposite exits, upper a at<=3 and the actual opposite helper barrier.

For Q8 the +1 a return uses the same old one-credit K_B with c8. Key4
has weight2. Every other marked target is in5..7. Let k be such a target.
If its source B depth is2, the exact top LR pair gives

    8(4(L,k(A,B)),E)->k(4(L,A),8(B,E)).          (4)

All remaining upper cores have depth<=3, and a has depth2. At B depth3
the two lower pair forms give

    k(4(L,A),8(u(B,C),E)), or
    k(u(4(L,A),B),8(C,E)),                      (5)

where u is one of the other5..7 roles and only ONE other upper role is
off path. It lies in a block at depth<=3; old4 has depth1/2 and a2/3.
All marked depths are<=3, so every +1 upper exit is E1-floor valid.

A zero upper target has B depth4. Its path within the THREE-core U uses
all three nodes, giving the four complete two-direction chain schemas.
After the bottom pair, (4) is also the endpoint of the actual RL top pair

    4(L,8(k(A,B),E))->k(4(L,A),8(B,E)).          (6)

The completed full-upper zero maps for (6) yield exactly J5/J6/J7.
We reuse those maps, not their checker executions. Equation(4) gives
the identical CORE output for Q8. The A zero target must be LR under4:
its pair leaves Score4 at L and actual a at LL. Old4 has B depth1, a2.
The literal full target is Rsh, already at2, regardless of extra G fields.
Thus every Q8 zero row has residual0 at source2. The old helper barrier
again covers Gamma1 with weight>=2, and Gamma0 retains its floor law.
Q8 is therefore safe to saturate after Rsh.

In the ACTUAL lower flank Q0, the core block on1..3 and maximum a>4
use the corresponding RL/LL identities, and zero targets are the actual
J3/J2/J1 returns. Present lower key counts and old4/a depths are the
same; the opposite helper barrier applies. No private witness is reflected.

## 4 The isolated P8 return

At an actual P8 source, Score5 is L and Score4 LL. Smallest a is hidden
below4.left at depth>=3. G through source slot0=8 reports8 or Score5,
never a. Its only possible marked H1 targets are4,5,6, with weights2,1,0.
The exact new core identities are

    P8 --5--> 5(4(L,E),8(7(6(E,E),E),E));
    P8 --6--> J6.                              (7)

After5, marked a/4/6/8 have depths<=3 by the shallow L-root-a guard.
The existing E1 floor repays +1. A genuine6 must be at LR under5; its
A zigzag leaves Score4 at LL. Its full J6 target belongs to Bdry, which
has no V filter. The zero6 row ends at2; key4's weight2 is range-safe.

Only MAXIMUM Gamma1 helpers at R/RR/RL are possible: LL4 is a Score,
LR lies between present5,8, and L5 is a Score. Such a helper pushes the
entire left5/4 block deeper. The only marked charge1 terminals are old8
or5; 4 and any6 at LR are now at depth>=3. In valid source B the maximum
proxy9 is the right child of Score8 (completed proxy-parent lemma). Its
first splay is a zig, leaving old8 at depth1 and old5 at depth4. Original
q is at most0/2, so H2 weight is at least4/2. Range2 proves all of them,
without an initial helper Score-emptiness assumption. Gamma0 is unchanged.

The ACTUAL P0 proof uses minimum helpers on the left, old0/3 as terminals,
proxy0 below Score0 and B depths1/4; its zero2 target is Bdry's J2.
This proves both orientations of the P stage.

## 5 Two band-root returns C5 and C8

Both classes have root4, smallest a as the actual A left child AND core
left child, and the named marked m5/8 as A right child and core right child.
Their a and m exits have weight2. A different marked upper k can only
be at RR under5 for C5, or RL under8 for C8.

For C8, the same complete zero maps in(6) give J5/J6/J7. Its A RL pair
leaves Score4 at L, a at LL; its core also leaves a at depth2. Every zero
target is Rsh, already at2. A +1 upper target has depth2/3; the exact
two depth3 forms are

    k(4(L,A),u(B,8(C,E))), or
    k(4(L,u(A,B)),8(C,E)).                       (8)

Only one other5..7 role remains off path. Its depth and every other
marked depth are<=3, including a2, so these +1 rows end at E1 credit>=1.

For C5, a zero upper path uses5 and all THREE cores6..8. Reuse the saved
RLL/RLR/RRL/RRR full-upper maps: their cores are B6/B7/B8. The A RR
pair leaves Score4 at LL. Old4 has B depth<=2, so its old left child a
has depth<=3, satisfying the old G_B cap5. The full target is Bdry, even
if G reveals a elsewhere. These zero rows end at2.

For a +1 C5 upper target at B depth2, old4/a end at depths2/3 and all
upper marked depths are<=3. At B depth3, let u be its parent among6..8.
If k<u, the lower RL pair and final zig give

    k(4(L,5(E,A)),u(B,C));                       (9)

the single off-path upper role is at depth<=3. If u<k, they give

    k(4(L,u(5(E,A),B)),C).                      (10)

The sole possible depth4 node is inside A, strictly between5 and u.
With only three upper roles, nonempty A forces their order6<7<8 and
forces u7,k8,A=6,B=C=E. This is exactly the P8 core. If6 is unmarked
all marked depths are still<=3. If6 is marked, source marks already
include a,4,5,8, so mu is exactly{a,4,5,6,8}; the A RR pair leaves
Score5 at L and Score4 at LL, and a has B depth2. Thus the full endpoint
is P8, already at2. These are symbolic count/interval alternatives,
not a finite tree census or label test. They exhaust every +1 C5 exit.

H2 in either C class is also range-safe at source2. Minimum helpers can
only be at LL below Score a; the other low middle interval(a,4) is interior.
That LL pair puts a at A depth1, old4 at2, and the whole right m block
at depth>=3. Only a/4 can be marked charge1 terminals. For B, a minimum
proxy access from a root with left child a puts old4 at<=2 and old a
at<=3. This last bound follows by last-step parity: an even proxy depth
ends with the same-direction top pair, giving old a depth1; an odd depth
finishes a's subtree first with its old root at<=2, then the final root4
zig can add only1. Arbitrary right blocks of a are allowed. Both terminal
prices have q<=1, hence H2 weight>=3.

Maximum helpers can only be at RR under Score m. Its A pair pushes a
to depth3 and excludes it as a marked charge1 terminal. All eligible
marked terminals are at least4. In B the entire lower0..3 block remains
below old4.left, off every such terminal path. There are only FIVE
relevant cores4..8 below the maximum proxy, so actual preterminal depth
is<=5 and ORIGINAL q<=2, weight>=2. This permits Score-bearing helper
support and newly exposed upper marks. Gamma0 uses the existing floor.

For the actual opposite C3/C0 classes, maximum helpers below the largest
A right child leave only it/4 eligible, with B depths<=3; minimum helpers
below the left m hide that largest mark and use only the FIVE cores0..4.
Thus the same original weight bounds apply in those actual orientations.
This closes C5/C8 and their opposite classes after Rsh/P8.

## 6 Odd successors K and the remaining even span

At an actual K source, the first-two-mark order and A R=b/RR=c make
b,c the only marked H1 targets. G source reads root a or b, not a new
marked key. In B, c has depth1 and weight2; b has depth2/3 and weight1.
The exact two b accesses are

    a(L,c(b(M,N),P)) -> b(a(L,M),c(N,P));
    a(L,c(q(M,b(N,P)),Q))
                  -> b(a(L,q(M,N)),c(P,Q)).     (11)

Old a and c are now direct children of b. All other marks exceed b.
If6<=c<=b+3, a marked k between b,c has depth<=c-b<=3, and one above
c has depth<=9-c<=3. All marked keys are therefore E1-shallow. Given
b4/5 and b<c<=8, the only ways either inequality can fail are b4,c5
or b4,c8. In those cases (11) has exactly the C5/C8 core and A guards:
root4, core left child a, right5/8 and A L=a/R=5/8. Those destinations
are already2. Thus every +1 b row repays a source2, with no span exception.

Only minimum Gamma1 helpers on the A left side can occur. As in the
saved Transfer11/05 helper identities, they leave only old a or b eligible;
c remains at A depth>=3. In B the old right block is untouched and old
root a ends at<=2. A b initially at depth<=3 can end at no more than5.
Original q<=2 gives H2 weight>=2, enough for source2. Other forms use
the actual-preterminal floor. The actual upper-end K proof uses maximum
helpers and the untouched left block, and the lower-band C3/C0 exceptions.

The only new even-depth successor beyond saved Transfer11 J is J8,
with b4,c8. Its b exit has weight2; its +1 c exit, by the actual RR pair,
lands in Q8, including A L=4/LL=a and a at B depth2. Its helper proof
from the saved J calculation did not use the span bound: only old a/4
are eligible, and their B depths after a minimum proxy are<=2/3, giving
weight>=3. The actual upper-end J0 uses the corresponding LL/minimum-band
count and maximum helper. Thus the exceptional even successor is safe.

## 7 Depth-five parity and the final source saturation

In G45_minus a,b,c are all marked, a at A LL, and the exact A pair is

    c(b(a(A,B),C),D)->a(A,b(B,c(C,D))), C,D nonreal. (12)

The only genuine H1 targets are a,b. They have original weights0,2.
The complete old H1 normal form retains SAME endpoints,H,q, including
charged DELETE/zero terminal KEEP. No edge is repriced or fused with H2.

At B depth4 the saved Transfer11 top pair gives root a with b,c at
depths1,2 in the chain a,Rb,Rc. If c-b<=3 it is the OLD J cap2; the
only other possible pair is b4,c8, which is the NEW J8 cap2.

At B depth5, consume the arbitrary lowest pair, leaving
c,Lb,Lq,epsilon a. For epsilon=L the remaining pair/final zig give

    a(L,c(q(M,b(N,P)),Q)), a<q<b;               (13)

for epsilon=R they give

    a(q(L,M),c(b(N,P),Q)).                     (14)

Both are K: old c is at depth1, b at depth3/2. All arbitrary processed
bottom blocks remain variables. These two universal parity cases exhaust
the odd path after the bottom pair; no population/tree sample is used.
The A target still has b at R and c at RR. No V filter or fresh source
completion is required at K/J8 or the old J. G aliases reporting old
marked c at other positions do not remove the literal endpoint.

Thus every zero a exit lands at already established2; every b exit has
weight2. G45 has no actual anonymous source node at depth1/2 because
its other cuts are nonreal. Gamma1 cannot start. Gamma0 retains its
actual-preterminal floor, even if it exposes different hidden marks.
All G45-source LOW rows therefore tolerate2. The actual upper-end RR
source has top RR and the two odd reverse pairs; it lands in the defined
upper K/J0 or saved J with the identical ORIGINAL weights.

For each operation in(3), a source unchanged by it only gains target
credit. A raised source belongs to a region whose complete outgoing
LOW rows have just been proved using earlier capacities. Bdry's argument
is even stronger: no actual source changes. Hence every operation
preserves each prior valid row; the order is acyclic and no global LOW
feasibility is assumed. All new source values are2, so every nonnegative
incoming LOW row is range-safe. This proves the theorem.

## 8 Original domain, nonvacuity and limits

Every main G45_minus root is c>b>=4 and differs from its second-smallest
b, so it is outside S_minus and above S_plus's root range3/4. Every
G45_plus root is c<b<=4 and differs from its second-largest b, so it
is outside S_plus and below S_minus's root range4/5. Both ancestors
are marked. Nonreal cuts may contain arbitrary compatible private counts;
they are not required to retain a private payload at the next edge.

For a formal new depth5 family use nine ordered roles
l0<l1<l2<l3<b<u<c<v<w, mark l0,b,c,v,w and a=l0. Root c and child b
are marked, b is ordinal4 and c6. Take actual A c(b(a(A,B),C),D), C/D
opaque; place the other Scores in ordered ports. Take the core path
c,Lb,Ll3,Ll2,Ll1,La, with other roles in compatible side blocks. This is
an original A-depth2/B-depth5 access with H=1,q=2,w=0. Standard source
port realization supplies full witnesses including sigma0. The actual
upper-end ordered family is also legal. No numeric tree, root, bank,
saved label, mask census or population experiment is evaluated.

Use HIGH/h0 with W(O)=-D45(O)-5chi8 and W(M)=-5chi8. Walks whose LOW
legs have prior coverage or the stated new coverage have weight>=-7;
fully closed such walks have weight>=0. All147-O/127-M fields, SAME
actual midpoint, independent scopes, high v free, weak LE/G/raw unused
fields, original H/q/prices and corrected h0(actual0,declared18,q9,w=-3)
remain. No shared state is identified or original graph edge removed.

BEFORE: the central aligned marked-ancestor relay excluded depth5 and
span4. RESULT: all its zero-depth4/5 cases, BOTH endpoint exceptions and
both actual orientations are proved with an explicit ordered cap formula.
AFTER: delete all G45 zero obligations, new source LOW rows and their
nonnegative incoming rows; every completed row remains. No new global
existence premise or strict numeric old-debt increase is claimed.

This DOES NOT prove that every original zero LOW source has one of
these guards. Non-extremal marked targets, absent B child alignment,
other A cuts/orientations and remaining shallow Gamma1 zeros are audited
in STEP4_COVERAGE_AUDIT.md. Full Step4, M3 and Dynamic Optimality remain
OPEN unless those original residual obligations are separately closed.
