# Safe LOW augmentation with a visible cut separating the marked keys

Analytic theorem on the precisely defined region R. Independent symbolic
audit is recorded separately. No finite tests or proposed numerical fit.
The augmentation statement is universal; its source/walk coverage is
restricted to the named region. Full M3 is not claimed.

## 1. Observable region and explicit debt

Use the original full ordinary state(mu,b,alpha7,sigma), valid core B
projection, and public V,c,U,Lambda,D_Q from the completed E1/Transfer01
proofs. All old definitions, raw fields and totalizations are unchanged.

Let a<b be the TWO SMALLEST marked Score labels. Define R_minus by:

* root b, its right child has kind1(PORT), and a is a kind0 Score at
  L or LR; OR
* root a, b is its kind0 Score right child, and b.right (alpha RR) is PORT.

In each case the A-root label equals the B core root and V is exactly
the other member x of{a,b}. Root's unused kind and nonreal isS/index
fields are free. No other visible/unobserved subtree is restricted.
The PORT guard reads only its kind, not its reference or private payload.

Define R_plus dually for the TWO LARGEST marked labels a<b:

* root a, its left child is PORT, and b is at R or RL; OR
* root b, a is its Score left child, and a.left (alpha LL) is PORT.

Set R=R_minus union R_plus, and

    w_x(s)=2-floor(depth_coreB(x)/2),
    h_R(s)=min(2,w_x(s)+2) on R, and0 elsewhere,
    D_R(s)=max(D_Q(s),h_R(s)).

The marked pairs at the two ends are disjoint for the original five-bit
mask; V supplies a unique x. Since core depth<=8,0<=h_R<=2. On R, V={x}
gives h_R=U. Lambda<=U and the old Q clause either vanishes or equals
the same U, so D_Q<=h_R and D_R=h_R on R. Globally psi<=D_R<=2.
These are current shared-state formulas independent of private inventories.

In the small-end region the observed port b.right contains every other
marked Score, all of whose labels exceed b. Proper source connectivity
and strict ordering of PRESENT real Scores imply that none of those
other marked nodes is present anywhere in the actual prefix. The only
present marked Scores are a,b. Arbitrarily many anonymous and UNMARKED
Score nodes may still be present, and the port may hide arbitrary
compatible payload. This proves only a marked-support separation;
it does not determine a private unmarked-Score split or strengthen weak LE.
The large-end assertion uses the observed port a.left instead.

## 2. H1 preservation including anonymous exposure

Work at the small end. A genuine H1 target must be the other marked key.
The marked source roots/targets and the visible port make these the
complete allowed A shapes, with arbitrary compatible blocks A,B,C:

    b(a(A,B),P)       -> a(A,b(B,P));
    b(p(A,a(B,C)),P)  -> a(p(A,B),b(C,P));
    a(A,b(B,P))       -> b(a(A,B),P).                 (1)

P is the original PORT, moved as one side pair. The middle shape uses
a zigzag. A genuine source's p is real and unmarked/anonymous; a slot0
alias could not supply the nonroot target at LR through the port b.right.
The old H1 normalization retains the SAME original endpoints/H/terminal q,
including charged DELETE followed by zero terminal KEEP.

Each result again satisfies R_minus: the separating port remains visible
at depth<=2, and only the other member of{a,b} can be a marked nonroot
target. Newly exposed B/C may be anonymous or unmarked, even if their
private support differs across successive witnesses. They cannot contain
another PRESENT marked key. G lookups report the old source slot0 label,
which is a or b, and therefore introduce at most a duplicate of that pair.
No raw unused field is fixed and no projected endpoint equality is assumed.

After a B core access, the old root has core depth1/2 by the completed
last-step lemma. Hence the successor's h_R=2 (reverse weight>=1).

For any public0<=D<=2 let F=max(D,h_R). An H1 inequality whose source
was unchanged only gains the target increment. If its source was raised,
it lies in R and F(s)=h_R(s), F(t)=2, giving

    w_x+F(t)-F(s)=w_x+2-min(2,w_x+2)>=0.            (2)

For w_x>=0 this is w_x; for -2<=w_x<0 it is0. Thus augmentation
preserves each valid H1 inequality individually. For D_R every R-source
H1 inequality holds directly because D_R(s)=h_R(s).

The order-dual versions of(1) prove R_plus. This is a proof using both
actual LOW orientations, not reflection of weak-LE private witnesses or
HIGH sentinel fields. No symmetry of psi is needed.

## 3. A B spine lemma for a Score-bearing fringe helper

Lemma. Let f be an extreme gap proxy. Splay it from a source core-rooted
B tree, and then splay a DIFFERENT core x from the old core root r.
After the two accesses, r has core depth<=3. Other gap leaves and NULL
side pairs are carried unchanged; intermediate stale bounds are irrelevant.

Proof for minimum f. Its initial path is all LEFT. After the first splay,
old root r is either the right child of f, or the right child of p=f.right.
This is the completed depth/parity fact for the extreme fringe access.
All core keys exceed f. Analyze the terminal core access by its depth
inside the subtree containing it. An even internal depth is consumed by
pairs; an odd depth leaves one final edge. This is the actual bottom-up
pair decoder, not a new splay algorithm.

(i) r=f.right. If the internal x-depth in r is even, its paired splay
leaves old r at depth<=2 below x, then the outer x/f zig moves either
old x side subtree down by at most1. Thus r depth<=3. If internal depth
is odd, the remaining path f,r,x is a final pair; parent r becomes a
child of x, so its final depth is1.

(ii) r=p.right at source depth2. If x lies in r's subtree, an even
internal depth leaves old r at depth<=2 below x, followed by the outer
f,p,x same-direction pair. Each existing child subtree of x moves down
by at most1, so r depth<=3. An odd internal depth leaves f,p,r,x. Pair
x/r/p, then zig x/f; r has depth<=2. If x=p it ends at depth1. Otherwise
x<p and lies in p.left. The entire old r=p.right is off the access path
and stays a child of p. For even internal depth, after splaying within p,
p is at depth<=2 in x.right because p>x; the final x/f zig changes only
x.left, so p's depth stays<=2 and r's stays<=3. For odd internal depth,
the final f,p,x zigzag puts p at depth1, and r at depth2.

These cases exhaust all core x!=r. Every arbitrary lower paired suffix
fits the same tree-variable substitutions; induction by removing pairs
covers all path lengths. The maximum-proxy proof reverses constructors
and inequalities. No private rank reflection or finite topology census
establishes this lemma.

The bound concerns the ACTUAL final core tree. All gap slots must be
childless at an original final endpoint; deleting those leaves does not
change a core path depth. Therefore old r has reverse H1 weight>=1 and,
if the A endpoint is in R with other visible key r, its h_R equals2.

## 4. Complete Gamma1 helper check at the small end

Reuse the original source normal form: H2/Gamma1 is one outer-gap helper
f followed by a marked terminal key, both A charges1, with original full
endpoints, H=2 and ACTUAL terminal q. No assumption that f is Score-empty.
Interior gaps cannot be Gamma1 final-valid outcomes by the completed
opposite-side child proof. No H2 edge is fused or repriced as H1.

In R_minus, a/b are the only PRESENT marked Scores. All present real
nodes lie below the opaque upper barrier b.right or at b. In particular
no actual gap9 node is present; the Gamma1 helper must be gap0, so f<a<b.
Terminals are either the entry core r or the other member x of{a,b}.

If the terminal equals entry r, its B depth after the helper is<=2 and
q<=1. Hence w2=4-q>=3 and range alone gives the signed inequality.
No endpoint-region claim is needed for this case.

For the other terminal, these are the FOUR possible complete A schemas.
Apply splay_f and then splay of the indicated marked key:

 (A) b(a(f(A,B),C),P) -> a(f(A,B),b(C,P));
 (B) b(f(A,a(B,C)),P) -> a(f(A,B),b(C,P));
 (C) a(f(A,B),b(C,P)) -> b(a(f(A,B),C),P);
 (D) a(p(A,f(B,C)),b(D,P)) -> b(a(f(p(A,B),C),D),P). (3)

They correspond respectively to helper LL, L, L, LR. Each terminal
has A depth1/2 after the helper. The PORT P is unchanged and visible;
the two marked keys are now parent/child. Thus every result is in R_minus,
even when it exposes arbitrary new anonymous or unmarked nodes.

Exhaustiveness is an order/charge argument. With root b and a at L,
the gap0 helper can only be at LL; LR below Score a would exceed a,
and the other branch is PORT. With root b and a at LR under p, helper
L is case(B); helper LL instead gives a post-helper terminal a at
depth3, which has A charge2 and is impossible in this H2 normal form.
LR is Score a itself. With root a and b at R, helper L or LR gives
(C)/(D); helper LL gives terminal b at depth3 and is excluded likewise.
RL is between a,b and cannot be gap0; RR is PORT. A nonreal parent
cannot provide an active real helper. These are all six depth1/2 slots.

The B lemma gives the entry core r final depth<=3 when terminal x!=r.
Since the A endpoint of(3) belongs to R, F(t)>=h_R(t)=2. The completed
LOW credit bound gives q<=4, so w2>=0. Therefore, for any source debt<=2,

    w2+F(t)-F(s)>=w2+2-2>=0.                        (4)

This proves the signed inequality for Score-bearing helpers as well as
Score-empty ones, without private erasure or inventory invariance.

The R_plus proof is the explicit order-dual: only gap9 may occur,
the four mirrored schemas preserve the lower port a.left, and the
mirrored B spine lemma gives the same bound. Both outer directions,
anonymous identity changes and arbitrary compatible counts are covered.

## 5. Full LOW augmentation theorem and combined debt

Theorem. If psi<=D<=2 is a public ordinary-state function, then
F=max(D,h_R) preserves EACH previously valid original LOW inequality.
For H1 use(2). For H2/Gamma0 the completed actual-preterminal-floor
proof applies to every function in this range/floor class, including F.
For H2/Gamma1 a raised source lies in R and section4 proves the result;
an unchanged source only gains a nonnegative target increment. The
established genuine-H0/Gamma>1 exclusions finish the original coverage.

This is a constructed safe operation. It assumes no globally feasible
potential, chooses no private extremizer, and invokes no unbounded closure.
Unlike the previous general H1 normalization, this PARTICULAR R operation
has now been proved safe for the Score-bearing Gamma1 source cases too.
Nothing here promotes E1/c augmentation to full LOW-safe operations.

Apply the theorem to the existing partial seed D_Q. The resulting D_R
has every original LOW inequality with source in R, by sections2/4 plus
Gamma0. Every Q-source LOW inequality stays valid by preservation, even
if its target lies in R. Other previously valid D_Q LOW inequalities
remain valid. Therefore R adds genuine non-Q coverage without invalidating
the completed reductions. Whole signature certificates are not added.

Outside E1, any R state with its other marked target at B depth4/5 has
D_R=2 and a weight0 H1 exit to debt2. ALL incoming LOW edges of weight0
or+1 are safe by range. At depth6/7, D_R=1: its -1 H1 exit ends at2;
all incoming+1 LOW edges are safe, and incoming zero edges are safe from
source debt<=1. At depth8, D_R=0; no incoming0/+1 safety is claimed.

Any remaining H1 failure of D_R is outside Q union R and was already a
D_Q failure: w0 with psi(source)1/2, or w1 with psi(source)2, always
c(source)<psi(source). This does NOT classify every unsolved H2 source.

## 6. Restricted original signed-walk theorem

Use the completed HIGH/h0/chi8 glue, unchanged:

    W(O)=-D_R(O)-5chi8(O.b),       W(M)=-5chi8(M.b).

The HIGH proof requires only range2 and the original absorbing/entry laws,
so it holds globally. LOW conserves chi8. Thus every original finite walk
whose LOW sources all lie in Q union R has weight>=-7; every full-state
closed such walk has nonnegative weight. Within one fixed chi8 region the
finite bound is-2. Repeated/nonprimitive walks telescope with multiplicity.

Closure is all147 ordinary/all127 midpoint coordinates. Each OM/MO leg
keeps its independent private witness and the SAME actual midpoint; high
v is free. All original q/weights and h0(actual0,declared18,q9,w=-3),
raw annotations, weak LE and G aliases remain. No graph edge is removed.

## 7. Nonvacuity and remaining gap

The new region permits genuinely exposing non-Q sources. For example the
SYMBOLIC family b(p(A,a(B,C)),P), p<a anonymous and a<b the two smallest
marks, exposes the arbitrary B/C roots under its core zigzag. P hides all
other marked keys. If b-a>=4, a source core B can have a four-edge path
to a below b, so the genuine access has w0 and is outside E1. This is a
constructive ordered family in the frozen domain, not an evaluated test.
Anonymous counts stay within the original caps; no stronger integer-room
assumption is made. Variants with a above Score0 also admit Score-bearing
gap0 helpers whose support includes unmarked Scores or marked a itself.
The proofs never require them to be empty, nor fit labels to such examples.

The restriction excluding a at LL is essential to this proof: splaying
that target can put b at A depth2 and push its port below the observed
depth. A fresh witness could then change the unseen branch. Neither the
barrier-below-depth2 cases nor multiple exposed marked targets are solved.
The full non-Q/non-R coupled transfer problem and general Score-bearing
helper cases remain OPEN. M3/Dynamic Optimality remain OPEN; no negative
cycle or new full-signature certificate is claimed.

BEFORE: anonymous-exposing0/+1 transfers and Score-bearing Gamma1 sources
had no such safe augmentation. RESULT: explicit LOW-safe cut-pair operation
and a complete R-source proof, plus a restricted original signed-walk law.
AFTER: the remaining original obligations include all unproved non-Q/non-R
sources. NET ADVANCEMENT is this concrete deletion, not a global feasibility
restatement, new history coordinate, sampled agreement or private quotient.
