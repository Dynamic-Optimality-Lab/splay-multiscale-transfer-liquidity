# Repayment for marked grandchildren below two unmarked Score ancestors

This is a uniform original-LOW theorem on a restricted public class outside
S. It supplies a safe explicit capacity increase, closes all zero H1 rows
in that class, and leaves other marked-grandchild configurations open.
There are no finite tests or new saved-potential queries.

## 1 Public regions and statement

Reuse full ordinary states s=(mu,b,alpha7,sigma), set-valued V, psi,c,U,
Lambda, existing totalizations, and the completed D_interval. Source root
r is a Score synchronized with the valid ordered core-B root, and mu
does NOT mark r. Its child p is a kind0 Score, also UNMARKED. The marked
Score grandchild x has the indicated public position below p. Require
V={x}, and the following two nonreal cuts and marked-label barrier:

| Region | Order and grandchild | Opaque cuts | Public marked-label barrier |
|---|---|---|---|
| Z_LL | x<p<r; p at L, x at LL | LR,R | {k in mu:k<p}={x} |
| Z_LR | p<x<r; p at L, x at LR | LL,R | {k in mu:p<k<r}={x} |
| Z_RL | r<x<p; p at R, x at RL | L,RR | {k in mu:r<k<p}={x} |
| Z_RR | r<p<x; p at R, x at RR | L,RL | {k in mu:k>p}={x} |

Here nonreal/opaque means kind1(PORT) or kind2(EMPTY), with no constraints
on its unused isS/index fields. Scores at nonroot positions have kind0
and isS=true. Root's UNUSED kind is arbitrary. The four cases are disjoint
because the other grandchild or opposite child is nonreal. V={x} follows
from these observations and is retained explicitly in the public guard.
Let Z be their union.

The mark barriers use only mu and observed Score labels. They say nothing
about a private unmarked support, anonymous rank, gap, port label/bill or
completion. Arbitrarily many compatible anonymous and unmarked real nodes
may lie under x. Other marked Scores may be present or hidden in opaque
cuts; they are not forbidden from the inventory. The theorem quantifies
over EVERY actual edge of every admissible signature, not a claim that
every signature realizes every particular prefix.

Put

    w_x(s)=2-floor(depth_coreB(x)/2),
    h_Z(s)=min(2,w_x(s)+2) on Z; h_Z=0 elsewhere,
    F(s)=max(D(s),h_Z(s))                         (1)

for any explicit public Lambda<=D<=2. Since a nonroot core has depth<=8,
w_x>=-2 and 0<=h_Z<=2. No invalid core projection is newly assigned a
nonzero cap. Thus all old invalid-state totalizations are retained.

THEOREM.

1. Every original H1 edge s->t with source in Z has V(t) EMPTY and hence
   Lambda(t)=D(t)=F(t)=2, on the literal full target state.
2. F preserves EACH original LOW row previously valid for D, individually.
   Every nonnegative Z-source H1 row is directly valid for BOTH D and F;
   under F, a zero row has source/target values2 and residual exactly0.
3. Every Z-source H2 row is valid for F. If D already satisfies all negative
   H1 rows, every Z-source original LOW row is valid for F. This applies
   to the existing D_interval. Define the new public debt
       D_grand=max(D_interval,h_Z).              (2)
   For its actual Z-source H1 rows the residual is exactly max(w_x,0).
4. Every nonnegative incoming LOW row to Z2={s in Z:h_Z(s)=2} is valid
   for F. No general incoming claim is made for the smaller-cap part of Z.

No assumption of global LOW feasibility, continuing private inventory,
fixed point or new existence witness appears in this statement.

## 2 Exact original paired rotations

The two strict observed Score steps r,p,x must be actual present nodes.
An out-of-range kind0 ref would read immutable source slot0's label r;
it cannot supply distinct p, or marked x when r is unmarked. Source
connectivity, child bounds, uniqueness and the original verified active
paths therefore apply. Nonreal prefixes cannot be crossed by real paths.

Reuse the original H1 normal form with SAME full endpoints, H=1 and
terminal q. It includes the charged DELETE/zero terminal KEEP form.
The four actual depth-two paths have the exact identities

 LL: r(p(x(A,B),C),D) -> x(A,p(B,r(C,D))),        (3)
 LR: r(p(A,x(B,C)),D) -> x(p(A,B),r(C,D)),        (4)
 RL: r(A,p(x(B,C),D)) -> x(r(A,B),p(C,D)),        (5)
 RR: r(A,p(B,x(C,D))) -> x(p(r(A,B),C),D).        (6)

A,B,C,D are universally quantified child-pair/subtree blocks, not sampled
trees. In(3), C/D are opaque; in(4)-(5), A/D are opaque; in(6), A/B are
opaque. Primitive rotations carry these pairs without changing their kind,
payload or unused fields. The two right-side proofs use actual original
LOW operations, not reflected private weak-LE witnesses or psi labels.

## 3 Full endpoint has no nonroot visible mark

LL. Every present Score in A has label<x<p, and every present Score in B
has x<label<p. The public barrier says x is the only marked label below
p. Score uniqueness excludes a second actual x. Consequently neither
block contains a present marked Score. At the target, A is at L, p at R,
B at RL and r at RR; descendants of A may be seen at LL/LR. All actual
nodes seen through A and B are therefore unmarked/anonymous. Both p and
r are unmarked; C/D stay below r at depth3 and are not observed.

The boundary G case needs TWO levels of care. If the newly exposed
kind0 A reference is out of range, its target L observation reads the OLD
source slot0 label r, which is unmarked. Its target LL/LR observations
then read r's CURRENT children, namely the opaque C/D. Their kinds remain
nonzero. A proper real A node's bad child reference likewise reads the
unmarked r. Nonreal A prefixes propagate kind. Thus G cannot fabricate a
nonroot marked observation even at that second shadow level.

LR. Blocks B,C are strictly between the present Score labels p,r, with
x excluded by Score uniqueness. The barrier permits no other marked label
there. At the target p and r are unmarked children, A/D are opaque at
LL/RR, and B/C are at LR/RL. Their actual roots are unmarked/anonymous;
any G fallback is old unmarked r. No child below B/C is observed. Hence
there is no nonroot visible marked Score.

RL. Blocks B,C lie strictly between r,p, and their only possible marked
label x is the distinct target root. In(5) the unmarked r,p are children,
A/D remain opaque, and B/C are the two middle observations at depth2.
The identical interval exclusion and old-unmarked-root G rule prove the
same empty-V assertion without reflecting a private rank assignment.

RR. Blocks C,D lie above p, where x is the only marked label. Neither
contains another actual x or any other present mark. The target has p
at L, r at LL, C at LR and D at R; D's children can be observed at RL/RR.
All proper exposed nodes are unmarked/anonymous. If D is G, it reports
old unmarked r, then r's opaque children A/B. This explicitly handles the
second-level G reads, just as LL does in the opposite actual orientation.

Present rank inequalities here imply the stated Score-label inequalities
by the original strict order of present Scores. Weak-LE compatibility for
hidden ranks and port allocations is never strengthened. A marked Score
may be HIDDEN in a newly visible port, but that port is nonreal and its
unused labels do not enter V. No conclusion about private inventory is
drawn from such a port.

Therefore V(t) is the EMPTY SET for every actual H1 endpoint in all four
cases. The completed public law c(t)=Lambda(t)=2 for empty V proves
Theorem1. This is a pointwise public floor on the full typed target even
when it has no compatible fresh source witness; it is not a completion
or state-identification argument. All147 ordinary coordinates remain.

## 4 Signed max preservation and exact zero repayment

Every unchanged source only gains a nonnegative target increment. If a
source is raised, it belongs to Z, and every H1 target has value2 by the
new structural endpoint theorem. Its residual is then

    w_x+2-min(2,w_x+2)=max(w_x,0)>=0.             (7)

For w>=0 this is w+2-2=w. For w=-delta,0<delta<=2, it is
-delta+2-(2-delta)=0. These are signed identities in indeterminates, not
checks on selected depths. Thus every formerly valid H1 row is preserved.

For ANY nonnegative Z-source H1 row, even before augmentation, D(t)=2
and D(s)<=2 prove its inequality. After augmentation h_Z(s)=2, so both
F values are2. In particular every zero row (original core depth4/5)
has exact residual0. The newly proved empty-target structural preimage
is what discharges this original class; no old violated row is alleged.

If w<0, an arbitrary input D can exceed h_Z at a typed state. No downward
clamp or blanket typed-source cap is applied. For an ACTUAL negative edge
already valid for D, however,

    D(s)<=w+D(t)=w+2=h_Z(s).                     (8)

This gives F(s)=h_Z(s) and residual0. The completed negative H1 theorem
for D_interval supplies exactly this premise, without any global LOW
feasibility assumption. Hence all actual Z-source H1 rows of D_grand
have the residual in(7). Simultaneously raising a destination causes no
problem: its value was already2. No private information is accumulated.

For an incoming nonnegative row to Z2, target F=2 and source F<=2 give
residual>=w>=0. Smaller-cap Z destinations are not declared protected.

## 5 H2 and repeated mixed walks

Every real source position at depth1/2 is a Score: the ancestor p or
target x. All other observed nonroot positions have nonreal kind, since
the opposite source branch is opaque and propagates its kind. Root r is
also a Score. There is NO actual anonymous node at source depth1/2.
Invalid G refs cannot supply a missing active anonymous target; the actual
active paths and target cover are reused unchanged.

The complete original Gamma1 normal form requires a first changing
anonymous helper at source depth1/2. Thus no Gamma1 edge has a Z source,
independently of hidden Score support or anonymous populations. Anonymous
nodes may be present below x at source depth>=3; they are too deep for
this charge1 helper. They have not been erased from the source graph.

Gamma0 H2 edges CAN expose hidden marked descendants or use core-prefix
operations. The completed ACTUAL preterminal floor proves their signed
inequality for every public psi<=F<=2, with original terminal-only q.
No terminal-only-x assertion is used for H2. H0/other excluded forms and
full H1/H2 source coverage are the established dependencies. This proves
all Z-source H2 rows and, together with the unchanged-source argument,
preservation of every previously valid LOW row globally.

An H1 destination with V empty has no next genuine H1 target. It may
still have H2 or HIGH transitions and compatible fresh witnesses; it is
not a graph sink. Every future witness is independent. D_grand preserves
all completed rows, but this theorem does not declare those otherwise
uncovered H2 successors solved. No finite sign horizon is assumed.

Reuse HIGH/h0 glue with W(O)=-D_grand(O)-5chi8 and W(M)=-5chi8. Walks
whose LOW legs are previously proved rows, Z-source rows or nonnegative
incoming-Z2 rows have weight>=-7; fully closed such walks have weight>=0.
Full147-O/127-M closure, SAME actual midpoint, independent private scopes,
free high v, weak LE/G/raw unused fields, original H/q/prices and corrected
h0(actual0,declared18,q9,w=-3) are unchanged. The original graph is not
restricted to those walks and full M3 is not inferred.

## 6 Nonvacuity and strict new capacity without tests

For an analytic LL family use nine FORMAL ordered Score roles

    x<p<m1<u1<m2<u2<m3<m4<r,

mark x,m1,m2,m3,m4. Root r and parent p are unmarked, and x is the only
mark below p. Give A the proper prefix r(p(x(A,B),C),D), with C,D opaque
and the other Scores in compatible ordered ports. An arbitrary compatible
anonymous/unmarked prefix below x is allowed. Give core B the formal
prefix r,Lm3,Lm2,Lm1,Lx with the other roles in compatible side blocks.
Then x is at original A depth2 and B depth4, H=1,q=2,w=0, a genuine
original marked access. The source is outside S (root is unmarked),
outside Q/I (its only real child is unmarked) and outside old marked-root
capacity regions. This is a universal ordered family, not evaluated
numeric masks/populations/trees. Its LOW right-side counterpart follows
by the corresponding proper ordered construction, not psi reflection.

Strict capacity increase uses the immutable completed fact published in
Transfer01, from LDR01 helper_reset_2:

    B root8, target0, weight0, psi(source)=psi(destination)=0.

No saved bank, source root, psi label table or B operation is queried or
replayed. Apply that fact with marks{0,2,4,6,7} and proper A prefix

    8(1(0(A,B),C),D),                            (9)

with C a port containing2..7, D empty, and A/B empty for sigma0 (or
compatible unmarked/anonymous blocks in a compatible population). The
standard source port realization and the same legal core access provide
an original witness. The root8 and parent1 are UNMARKED; 0 is the sole
mark below1. Its V={0}. Thus c=Lambda=0 from the completed B fact.
Q and I fail because there is no marked child; the old R/S regions require
marked roots. The central second-mark/second-largest-mark release guards
also fail: these marks have second2 and second-largest6. Hence every
earlier augmentation vanishes there and

    D_interval(source)=0, D_grand(source)=2.      (10)

The original zero row was already valid once its empty target was proved;
it is not refuted. This strict source-capacity increase additionally
protects incoming nonnegative rows. The universal theorem uses(3)-(8),
not this reuse example. No whole-signature certificate count changes.

## 7 Before, result and remaining obligations

BEFORE: the complete S frontier and the interval-child class were proved,
but not this unmarked-ancestor grandchild structural preimage. RESULT:
the explicit max operation(1)-(2) preserves every old LOW row; all Z-source
zero H1 residuals are0, all current Z-source LOW rows are proved, and the
new public capacity can strictly exceed D_interval. AFTER: delete the four
Z-source zero H1 classes and the stated incoming-Z2 obligations. No new
open existence or independent compensation lemma is introduced.

Marked-ancestor grandchildren, anonymous-parent grandchildren, source
classes without these cuts/barriers, other unproved zero/+1 transfers
and global signed LOW remain OPEN. Some subcases there have previous
coverage; no exhaustive remaining-case count is asserted. Full zero LOW,
M3 and Dynamic Optimality are OPEN. No certified original negative cycle
or new whole-signature certificate is claimed. R1-R4 and current caps
are preserved; the independent audit is recorded separately.
