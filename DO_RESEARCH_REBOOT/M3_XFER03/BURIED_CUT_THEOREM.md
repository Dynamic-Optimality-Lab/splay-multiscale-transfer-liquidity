# Repayment when a separating port drops below depth two

Analytic universal safe-operation theorem with restricted source coverage.
The independent symbolic audit is separate. No finite tests are used.

## 1. The shared state does not remember the missing port

Let a<b be the two SMALLEST marked keys. The excluded same-direction
access in Transfer02 has an actual source prefix

    b(p(a(A,B),C),P) -> a(A,p(B,b(C,P))),             (1)

where P=b.right is PORT. It becomes b.right at A depth3 on the right.
At the destination another source witness may replace the unobserved
branch by an actual marked node. We neither infer P from that state nor
carry the first witness into the next edge. Instead we explicitly support
the return after this replacement, using public B-depth/count information.

All predicates below use only frozen(mu,b_state,alpha7,sigma), valid core
B projection and A/B root synchronization. V is the prior SET of marked
nonroot kind0 labels; unused fields are ignored as in the original reader.
For the small-end predicates require b in{4,5}:

 S_minus: root b, a visible as a kind0 Score at LL, and coreB depth(a)<=3.
          Other marked keys MAY be visible; no port guard is used.
 T_minus: root a, b visible at RR, V={b}, and coreB depth(b)<=3.
          There is NO guard on the unobserved b.right branch.
 L_minus: root b, a visible at LL, V={a}, and b.right is PORT.

The order-duals use the two LARGEST marked keys a<b and a in{3,4}:

 S_plus: root a, b at RR, coreB depth(b)<=3.
 T_plus: root b, a at LL, V={a}, coreB depth(a)<=3.
 L_plus: root a, b at RR, V={b}, a.left is PORT.

Write S,T,L for the respective unions. Root's unused kind and all unused
nonreal S/index fields remain free. Real active a/b occurrences cannot
be fabricated by G: a same-side grandchild through a ghost root child
would report the root or its child, not this distinct actual LL/RR key.
The original active-path/Score-uniqueness proof supplies the actual paths.

For ANY explicit public Lambda<=D<=2 define the three operations IN ORDER:

    D1=max(D,1_S),
    D2=max(D1,2*1_T),
    D3=max(D2,2*1_L).                              (2)

Each operation preserves every original LOW inequality valid before that
operation. Apply to D=D_R from Transfer02, giving the explicit final debt

    D_cut=max(D_R,1_S,2*1_T,2*1_L).                 (3)

No global feasibility of D_R is assumed. No fixed point, private inventory
function, new graph coordinate or bounded sign-history is introduced.

## 2. Central B roots cannot have weight0 Gamma1 edges

Auxiliary universal lemma: for ANY original H2/Gamma1 LOW edge whose
source core B root r satisfies3<=r<=5, its terminal B depth is<=7,
so q<=3 and w2=4-q>=1. This includes Score-bearing helpers.

Reuse the complete Gamma1 normal form: one extreme gap0/9 access followed
by a core terminal, with actual original H=2 and terminal-only q. After
the extreme access, old root r has depth<=2. For minimum gap0, the original
r.right subtree, containing every core>r, is untouched and remains under r.
If the terminal y>r, its depth is<=2+(8-r). If y<=r, no core>r can be on
its path, so there are at most r+1 cores following the gap root, and its
depth is<=r+1. For maximum gap9, the corresponding bounds are r+2 for
y<r, and9-r for y>=r. Thus every terminal depth is at most

    max(r+2,10-r)<=7 for3<=r<=5.                   (4)

Other gap proxies remain leaves off the core path. Dirty NULL side fields
do not change the established genuine LOW core projection. We use no HIGH
root-termination hypothesis and no finite core-tree census. The same-side
untouched-subtree property follows from the original rotation writes.

## 3. A one-credit S rule allowing newly exposed marked keys

Work at S_minus. Its actual A prefix has the form

    b(p(a(A,B),C),Y),                             (5)

where p is unmarked or anonymous because a,b are the first two marks.
All other marked keys exceed b, and Y may contain any of them as actual
nodes. B depth(a)<=3 gives its H1 weight>=1. Every other marked target
c>b has coreB depth<=8-b<=4. No H1 exit from S is negative.

If its weight is at least1, newly raising the source to1 is range-safe.
Consider a weight0 exit. It must target c>b at B depth4. Counting the
upper cores forces b=4, and the four nodes of B.right are all on this
access path. The initial right direction and the following three binary
directions give eight universal spine schemas. With an arbitrary left
subtree at b and no off-path UPPER core, exact paired rotations show:

    after splay_c, every upper core has depth<=3;
    old b has depth<=2.                           (6)

The independent checker proves those eight symbolic identities and their
order-duals; it assigns no numerical labels/tree/population. Completeness
is by core count: the path already uses all four possible upper cores.

We must also exclude a from the destination shadow. Its actual source
position is LL. Any active c>b is at R/RL/RR, whose exact rotations put
a at depth3/3/4 respectively. No marked key below b other than a exists.
This ACTUAL-depth argument alone would miss the G aliases. The original
slot0 owner here is b; all right-branch accesses leave b.left equal to
the unmarked actual p. A depth-two fallback through b therefore reports
p or the modified upper branch, never a. Nonreal parents propagate their
kind and unused fields do not contribute. Thus every marked nonroot
label reported at the destination is b or an upper core. By(6) all have
B depth<=3. The actual full destination therefore belongs to E1.

The completed capacity theorem gives Lambda>=1 on E1. Hence for a
newly raised S source, D1(s)=1, and a zero exit has D1(t)>=1. All H1
inequalities from newly raised S sources hold. Unchanged sources gain
only a target increment. H2/Gamma1 has w>=1 by(4) since b=4/5, so it
is also safe for source debt1. Gamma0 uses the completed range/ACTUAL
preterminal-floor law, since D1>=Lambda>=psi. This proves that D1
preserves each previously valid LOW inequality.

More generally, in the FINAL function(3), every S source with D_cut<=1
has all its LOW inequalities: positive edges use range1, zero H1 edges
use the E1 destination, Gamma1 has w>=1, and Gamma0 uses its old law.
We DO NOT claim every debt2 S source is solved. No downward clamping of
old debts is performed, since that could break incoming inequalities.

## 4. Two credits on the buried state T

A genuine T_minus source has actual prefix

    a(A,p(B,b(C,Y))).                             (7)

The only visible marked target is b; Y is arbitrary and may have actual
marked nodes above b. Its H1 weight is>=1 by the public B-depth guard.
The exact return is

    a(A,p(B,b(C,Y))) -> b(p(a(A,B),C),Y).           (8)

In B, old root a has final depth<=2. Therefore the actual full endpoint
is in S_minus, even when Y reveals new marked targets. No singleton-V
guard is imposed on S. Previously established D1>=1_S supplies the
required credit. For a source raised to2,

    w1+D2(t)-D2(s) >= w1+1-2 >=0.                (9)

Unchanged source inequalities are preserved by target monotonicity.

For H2/Gamma1, an extreme helper at depth1/2 cannot be on the source
right chain: p is strictly between the two marked cores a,b; RR is the
Score b; RL is also between a,b. Gap9 is impossible in the remaining
left positions. A gap0 helper may occur at L,LL,LR. Its splay puts b at
depth3,4,3 respectively; every other marked key is below b.right and
therefore even deeper. The only possible marked terminal with A charge1
is ENTRY a. After the B helper its depth is<=2, giving q<=1,w2>=3.
Such edges are range-safe at source debt2, without an endpoint-class
claim. This includes any Score-bearing helper in the source left block.
Gamma0 again uses its completed floor/range proof. Thus adding2 on T
preserves all previously valid LOW inequalities and directly proves all
T-source LOW inequalities for D2 and for the final D_cut.

T is indeed inside E1, but the old E1 theorem only justified raising
to1. The two-credit conclusion is new and essential for an incoming
weight0 access from debt2. No completed E1 check is rerun or promoted.

## 5. Close the missing port-source LL transfers L

In L_minus the right port contains every other marked key, so the only
present marked Scores are a,b. Its H1 target is a and its A endpoint is(1).
The source core B path to a lies in b.left and has at most b<=5 edges.
Hence its original weight is>=0. At the endpoint b has B depth<=2;
the A shadow reports b at RR and no other distinct marked nonroot key.

The last claim includes G: source slot0 is b; after(1) its children are
the old block C, whose actual keys lie between the first two marks, and
PORT P. A ghost left child of new root a can therefore report only an
unmarked key, duplicate b, or nonreal P. It cannot fabricate another
marked key. The full endpoint consequently lies in T, independently of
every unused field and the unobserved port's future realization.

It already has D2(t)=2, so a newly raised L source satisfies

    w1+D3(t)-D3(s) >= w1+2-2 >=0.                (10)

No Gamma1 helper exists here at source depth1/2. At L the actual parent
p lies BETWEEN a,b and cannot be an extreme-gap helper; LL is Score a;
LR lies between p,b; R is PORT. The other positions propagate the port.
A gap0 helper deeper under a has charge at least2, incompatible with
the inherited Gamma1 two-charge normal form. Gap9 nodes are behind P.
Gamma0 is floor/range-safe. Therefore the last operation in(2) preserves
all previously valid LOW inequalities and supplies EVERY L-source LOW
inequality. These are not only H1 or conditional-on-cut-persistence rows.

Every missing small-end LL port source OUTSIDE E1 is included: its
only target a has B depth>=4, which forces b>=4; three further marked
keys exceed b, forcing b<=5. Its depth is4/5 and weight is0. Thus the
new theorem deletes the full named missing family, not a sampled support.

## 6. Order dual, combined coverage and signs

The largest-pair proof reverses the constructor directions and Score
order: the central root is a=3/4; its four possible lower cores replace
the upper four, and zero accesses hide the marked key b initially at RR.
G reads the old root a, whose right child stays unmarked. The visible
lower port is buried by RR, the LL return reaches S_plus, and T_plus's
only possible Gamma1 terminal is its entry b. All arguments apply to
actual source witnesses in this orientation; no original weak-LE rank
assignment, HIGH sentinel, or psi table is reflected.

The construction preserves range[0,2] and the psi floor, and EVERY valid
LOW inequality of the partial seed D_R remains valid after(2). It supplies
all LOW inequalities with source in L or T, and all S-source inequalities
when the final debt is<=1. Earlier Q/R source coverage is preserved.

Incoming LOW edges of weight0/+1 to L or T are safe because those
destinations have debt2. All incoming+1 LOW edges to S are safe because
S has debt>=1; incoming zero edges to S are safe from source debt<=1.
This does not assert the zero-edge implication from debt2 into a debt1 S.

Define the explicit covered source set

    C = Q union R union L union T union {s in S: D_cut(s)<=1}.

With the inherited HIGH law and corrected h0, put

    W(O)=-D_cut(O)-5chi8(O.b),   W(M)=-5chi8(M.b).

HIGH inequalities hold globally by range2; LOW inequalities hold for
sources in C. Thus every finite original walk whose LOW sources lie
in C has weight>=-7, and every fully closed such walk has weight>=0.
Within a fixed chi8 region the finite bound is-2. Multiplicity and
independent private witnesses do not affect telescoping on the SAME
full states/midpoints. Closure is all147-O/all127-M coordinates.

The source classes are proof predicates, not restrictions added to the
graph. Arbitrary masks/signatures in the original domain remain, with
weak LE, literal-slot0 aliases, raw unused fields, original q/weights,
free high v and h0(actual0,declared18,q9,w=-3) unchanged.

## 7. Nonvacuity and exact remaining frontier

Nonempty outside-E1/non-Q/non-R L sources follow from the symbolic
family b(p(a(A,B),C),P), with a=the smallest mark, b=the next and b>=4,
and a four-edge ordered B path below b. A can be a port/empty and p a
compatible unmarked Score or anonymous node. Other marked keys reside
in P. No new finite case/root is evaluated to construct this family.
Its output has the actual port below depth2. A new witness at the shared
T state may put an actual marked c>b in the previously unseen branch Y;
return(8) is still covered and may expose c. The S rule permits this,
including a subsequent upper weight0 access when the four-core path is
full. No persistent private completion or deterministic lost port is used.

Still OPEN: arbitrary buried states without the T B-depth guard, S debt2
sources not otherwise covered, other marked configurations and general
non-C LOW transfers. E1 is not declared solved for all possible debt2
sources; only the new T subclass is closed here. General M3 and Dynamic
Optimality remain OPEN. No negative cycle or new whole-signature
certificate is claimed.

BEFORE: the same-direction cut-burial family was explicitly excluded.
RESULT: explicit three-clause LOW-safe repayment, including fresh hidden-
branch witnesses and new marked exposure. AFTER: L/T source obligations
and one-credit S obligations are removed, preserving all old proven rows.
NET ADVANCEMENT is this precise original signed family, not a finite fit,
hidden observability claim or new global existence premise.
