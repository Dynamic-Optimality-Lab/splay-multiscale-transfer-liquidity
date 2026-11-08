# Source-exact old-boundary restoration or transfer

PROVED—UNIVERSAL at the ordered-restoration scope explicitly below.
All A/B interiors and off-path subtrees can be arbitrary and unequal.
The hypothesis on intervening root motion is NOT automatic in FE02.
The theorem is a repayment-or-NAMED-TRANSFER theorem; unrestricted
eventual repayment and full FE02-CD remain OPEN.

## 1. Original source setup and quantified domain

At a common root g, take a complete nontrivial KEEP-containing A-root
block at r0!=g. Original mixed masks are permitted through the inherited
costed endpoint projection: A work remains at its actual leader, and
B work at its actual first KEEP. Let epsilon_A,0 and epsilon_B,0 be
the final depths of old root g in the two source splays. They belong
to{1,2} and are determined from the ORIGINAL source paths.

For definiteness g<r0. Before the FIRST return to g, suppose all intervening
common-root block targets satisfy

    r0<r1<...<rk,         k>=0.

Thus after departure each helper moves the common root strictly farther
away from g. All key support, gaps, helper access depths, interior BSTs
and number of helpers are arbitrary. There are no same-key root followers
in this list of nontrivial blocks, but any number of original zero-cost
followers may occur physically inside their respective blocks.

Let epsilon_A,i,epsilon_B,i be the ORIGINAL old-root source epsilons at
helper i,1<=i<=k. Reflection gives the case g>r0>r1>...>rk. No proof
below discards an approaching/crossing helper when it exists: a history
with such a helper is outside this ordered source theorem.

A KEEP-less nontrivial block already has negative excess and a spare
unit. In any hypothetical all-saturated FE02 candidate it cannot occur.
For the source proof assume the listed blocks contain KEEP; their
projected boundary tree pairs agree with the original blocks exactly.

## 2. Exact quantitative reserve identity

The inherited source far-side law is an EQUALITY: when roots move away
from g, every key in g's far-side subtree, including g, gains exactly
the old-root epsilon in each tree. It uses no equality of interiors.
Since g starts at depth0 before departure, its return source depths are

    d_A=sum_(i=0)^k epsilon_A,i,
    d_B=sum_(i=0)^k epsilon_B,i.

Define the source deficit

    D=sum_(i=0)^k (2epsilon_A,i-epsilon_B,i)=2d_A-d_B.

Each summand for(epsilon_A,epsilon_B)=(1,1),(1,2),(2,1),(2,2)
is respectively1,0,3,2. Hence D>=0. At g's actual returning block,
a=ceil(d_A/2), q=floor(d_B/2), z_A=d_A mod2. Therefore

    q=d_A-ceil(D/2),
    2a-q=z_A+ceil(D/2).                           (R)

This is the EXACT count of unused physical A units after own B-double
payment at the return. It is not a potential, an assumed reserve, a
count of hidden keys or a source of virtual capacity. B's terminal
zig is retained but is not a double demand.

Thus the return supplies at least one genuine spare unit unless

    D=0 and d_A is even.                          (Z)

If any departure/helper pair differs from(1,2), D>=1 and the return
has q<=2a-1. If all pairs equal(1,2), d_A=k+1 and d_B=2(k+1).
Then k even gives exactly ONE spare unit; k odd gives zero spare
capacity and a saturated return. In particular k=0 cannot be unpaid.
All noncritical initial departure types yield a spare unit regardless
of the later ordered helper count.

For the critical initial departure(1,2), uniform_reserve_algebra_certificate.json
records(R) symbolically using D=2v+p, with v an arbitrary nonnegative
integer and p in{0,1}. No k, depth or fringe-size sweep proves this
identity; it follows from the displayed source depths and integer algebra.

## 3. The surviving source inversion in the zero-reserve case

Assume(Z). Then EVERY pair is(1,2) and k is odd, so k>=1. In the
initial critical departure, A places g as r0's left CHILD. B's original
outer RR places g as r0's left GRANDCHILD under its original parent p0,
where g<p0<r0. This is the named odd-boundary inversion(g,p0).

At helper i let p_i be B's ORIGINAL source depth1 parent, from its
final outer RR. Since epsilon_B,i=2,

    r_(i-1)<p_i<r_i.

A has epsilon_A,i=1, so its old common root r_(i-1) is the LEFT CHILD
of r_i, even when A's last operation is a cross rather than a zig.
B has r_i->p_i->r_(i-1) down its left spine. All earlier g-facing
subtrees remain attached to the old root, with their internal source
structure unchanged. Induction gives the ACTUAL pre-return paths

    A: rk,r_(k-1),...,r0,g,
    B: rk,p_k,r_(k-1),p_(k-1),...,r0,p0,g.

Every displayed move is left; arbitrary inward and outward fringe
subtrees hang off these paths and need not match across A/B.

Since k is odd, A's depth k+1 is even and B's depth2(k+1) is even.
The original LAST outer LL at g's return uses the original A root rk
and parent r_(k-1); B's LAST outer LL uses root rk and parent p_k.
In the literal parent-first source identity

    g_old(p(x(L,R),Q),C) -> x(L,p(R,g_old(Q,C))),

the NEW root's right child is the ORIGINAL outer parent. Hence the
FULL returned trees have

    root=g in both,
    right-child_A=r_(k-1),
    right-child_B=p_k.                             (T)

The right children differ because r_(k-1)<p_k. BST order therefore
forces the actual surviving inversion

    r_(k-1) ancestor_A p_k,
    p_k ancestor_B r_(k-1).                       (I)

Before the last helper, r_(k-1) was the COMMON ROOT and ancestor of
p_k in both trees. That helper created this inversion; (T) proves
that restoring g does NOT erase it. Its keys are directly selected
from the original source parent/root, not chosen from later payer demand.
Its ordered interval lies strictly beyond the old boundary pair:

    g<p0<r0<=r_(k-1)<p_k<rk.

This is a source transfer of a particular disagreement, not |fringe|
new debts. It may or may not correspond to an evicted canonical
common key; no common-prefix count is used in this proof.

## 4. Repayment and closure corollaries at explicit source scopes

**Aligned returned-child class.** In this ordered source domain, if
g's returned child toward the helpers has the SAME key in A and B,
the zero-reserve branch(T) is impossible. The returning block has
q<=2a-1 and supplies a real spare unit. This allows arbitrary unequal
deeper interiors; full synchronization is not assumed. In an FE02
walk it settles the unique positive's one-unit deficit, or any
earlier negative block already does.

**Fresh-pair exact closure class.** Suppose the pair in(I) had agreeing
ancestry in the full source BEFORE departure, and the proposed history
claims exact paired closure at this first g return. Then zero reserve
would leave the inversion(I) contrary to that exact source agreement.
Thus the return supplies a spare unit or that proposed closure is
impossible. Agreement of this named pair before departure is an
EXPLICIT additional source condition, not assumed for arbitrary BSTs.

These corollaries delete their stated unpaid-restoration cases from
the FE02 obstruction. They do not prove that an arbitrary closed walk
contains an aligned return or a fresh-pair closure interval. No strict
new whole-walk coverage relative to FI/PF/FE is asserted.

## 5. Distinct physical payment when the return is negative

At the negative return, assign its own q B doubles to the first q of
its 2a actual A units in event-index/bit order. Formula(R)>=1 certifies
that its LAST A-event bit1 is outside that own-work prefix. Use that
single unused physical bit for the unique positive's third double.
The positive uses its own two bits for its first two demands; every
other nonpositive block pays its own q with its first q units.

Choose one traversal beginning at the positive. If g's first return
is in that traversal and qualifies for the source corollary, its
spare unit is later in that SAME traversal. No startup/future-period
capacity is imported and no unit is reused. For mixed blocks A's
unit stays at the original leader and B's demand at its first KEEP.
This is a direct injection, not a change to FI/PF/FE reservations.

The normal form does not promise payment in the zero-reserve branch.
There it proves a transferred source inversion that a further theorem
would have to handle. OR02 gives an actual closed FE02 history
realizing that unpaid restoration and later payment.

## 6. Why the ordered transfer cannot simply be iterated

Although the transferred ordered pair lies beyond the old pair WITHIN
this phase, the returned root is now g, not rk. The transferred pair
need not have the initial depth signature(1,2); in the fixed control
key7 has depths(1,3) after g=1 is restored. A next source episode can
approach, cross, reverse orientation or interact with another unrelated
interior. Neither the initial signature nor the strict ordering is
proved invariant under that continuation. Finite support alone does
not close this missing composition step. Unrestricted eventual
discharge remains OPEN, rather than assumed from the local transfer.
