# Exact old-root departure and a universal return-gap budget

**PROVED—UNIVERSAL source subtheorem.** These statements hold for every
finite ordered BST and, after FE02_01's proved timing reduction, every
candidate saturated return. They do not by themselves exclude the entire
arbitrary-support return class.

## 1. Old-root departure is exactly1 or2

Let T have root r, and splay present x!=r. Write d=d_T(x)>0. If d is odd,
the last operation is a root zig with old root r as its parent p. FE01's
exact zig table gives d_(S_xT)(r)=1. If d is even, the last double has r
as grandparent g. Its exact table gives depth2 for LL/RR and depth1 for
LR/RL. Earlier inner operations exclude r and leave its depth0 unchanged.

Define epsilon(T,x)=2 precisely when d is even and the LAST outer double
is LL or RR; otherwise epsilon=1. Then exactly

    d_(S_xT)(r)=epsilon(T,x) in {1,2}.                       (3)

The last outer case is read from the first TWO directions of the ORIGINAL
path when d is even, not from a post-tree. For odd d it is the final root
zig regardless of inner frames. This is a direct specialization of FE01's
first-containing-site theorem for y=r. All sizes, fringes, path lengths,
empty off-path subtrees and reflected orientations are included.

## 2. Return-gap bound, including its sharp one-unit improvement

Consider the exactly closed recurrent KEEP macro word with N nontrivial
blocks and cyclic keys x_j, adjacent keys different. For each block j let
p(j) be its preceding SAME-key occurrence in the periodic SOURCE extension
and let L_j=j-p(j)>0. This extension locates predecessors; it creates no
credits. If a key occurs once, its preceding occurrence is exactly one
physical period earlier and L_j=N. Every relevant source state is the
actual periodically repeated closed state.

After p(j) the tracked key x_j is B's root. Its departure is the block
p(j)+1, which accesses a different key. By (3) its depth just afterwards
is epsilon_j in {1,2}. Set eta_j=1-floor(epsilon_j/2): eta=1 for depth1,
eta=0 for depth2. There are exactly L_j-2 further genuine B changes before
the return at j. FE01's source theorem bounds EACH of those changes by +2
on this tracked key, including zero-double genuine zigs. Therefore

    d_B,j(x_j) <= epsilon_j+2(L_j-2),
    q_j <= L_j-2+floor(epsilon_j/2)
        = L_j-1-eta_j.                                     (4)

No future q, FE acceptance or donor is assumed. The stronger eta=1 bound
uses the actual ORIGINAL departure frames; forgetting eta loses a real
source unit. B-root no-ops inside a macro block neither alter the source
depth nor add to L. The mixed block's actual first KEEP is its departure/
return event; the A-only leader does not change B.

## 3. A source-forced donor criterion

For a nonpositive block j, if

    L_j <= 2a_j+eta_j,                                     (5)

then (4) proves q_j<=2a_j-1. Its last actual A unit is a safe donor by
FE02_01 section4. This is an all-size sufficient SOURCE criterion for direct
repayment of the unique positive unit, valid with arbitrary other keys,
fringes and closed histories. It does not require any positive-anchor FE
fact or FE cut. A KEEP-less nontrivial block is already an immediate donor
and does not need the recurrent-KEEP reduction.

Thus a saturated return must satisfy the stronger per-occurrence constraints

    L_j >= 2a_j+1+eta_j, j!=i,
    L_i >= 4+eta_i.                                      (6)

An immediate ABA root return has L=2 and q<=1, so it is necessarily
nonsaturated. A return after one intervening block with depth1 departure
has L=3,eta=1 and again q<=1. These are structural exclusions, not merely
assertions about aggregate total capacity.

## 4. Exact cyclic count and its limitation

Let s be the number of DISTINCT macro keys. For each fixed key its positive
cyclic gaps partition one period and sum to N. Summing over all keys gives

    sum_j L_j=sN.                                         (7)

The preceding-same-key map j->p(j) permutes physical occurrences within
each key class, and p(j)->p(j)+1 permutes all blocks. Therefore sum eta_j
is also exactly the number of macro splays whose old-root destination depth
is1 (odd-depth access or even outer cross). There is no multiplicity loss.
Summing (4) yields the universal recurrent-KEEP budget

    Q_B <= (s-1)N-sum_j eta_j.                             (8)

In the hypothesized single-positive saturated return Q_B=2A+1. Since
each a_j>=1, put R=A-N>=0. Combining (8) with its exact signature gives

    2R+1+sum_j eta_j <= (s-3)N.                            (9)

For s<=3 this is impossible. This independently excludes that support
subclass at arbitrary n and arbitrary fringe geometry. That CD support
class was already banked by DIRECT-NFKS-RT2; it is NOT counted as a new
Coarse-Double domain solved here. The exact eta-sensitive signature and
source-donor criterion are the present structural conclusions.

For general s>=4, (9) need not contradict nonnegative integers. The formal
signature N=s=4, a=(1,1,1,1), q=(3,2,2,2), L=(4,4,4,4), eta=(0,0,0,0)
satisfies (4),(6)-(9), yet has Q-2A=1. It is ONLY a numeric signature.
NO original A/B trees, source transitions, reachability or closure witness
is supplied for it. In fact the separate inherited four-KEEP theorem covers
that support size; it is not being refuted or reopened. The signature
shows exactly why THIS ROOT-GAP ARGUMENT ALONE does not give the source
compatibility contradiction, even in a case resolved by other machinery.

The general unresolved part includes larger support not discharged by the
applicable inherited small-support results. No finite search is substituted
for the missing joint-source proof; the principal all-size FE02 rigidity
theorem and FE02-CD remain OPEN.
