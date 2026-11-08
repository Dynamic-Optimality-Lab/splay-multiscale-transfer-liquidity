# Repayment for all three buried central barrier cores

The explicit public operation below closes B6/B7/B8 on the depth guard
inherited from every remaining S-zero release. Together with prior results,
it proves the entire eight-word S-family zero frontier and its actual LOW
dual. Other zero LOW source classes remain open. The same helper parent
lemma also excludes all original Gamma1 zero/+1 edges with initial B
helper depth>=3, without any assumption on private Score support.

## 1 Public regions and exact theorem

Reuse the full original shared state, V, Lambda, psi, D_direct and all
source normal forms/totalizations. At the smaller end let a<4 be the first
two marked keys; U={4,5,6,7,8}. L is any ordered lower core tree on0..3.
All predicates below require a valid projection and synchronized marked
root. They inspect only the current shared fields, not private inventories.

The main cores and one auxiliary core are

    B6 =6(5(4(L,E),E),7(E,8(E,E)));
    B7 =7(5(4(L,E),6(E,E)),8(E,E));
    B8 =8(5(4(L,E),7(6(E,E),E)),E);
    B6p=6(5(4(L,E),E),8(7(E,E),E)).              (1)

Define G_B by core B_c, c=6/7/8, depth_B(a)<=5, V subset U, and either

* Score4 at A L, with kind0 LL anonymous or unmarked Score k, a<k<4; or
* kind0 at L and Score4 at LL.

The cap5 is part of the theorem, not a graph restriction. Every actual
S-zero incoming edge satisfies it: old4 has B depth2 and its previous
distance to a was<=3. Arbitrary same-shaped sources exceeding that cap
are not claimed covered here.

Four one-credit regions support the main capacity:

* K_B: root a, marked c in{6,7,8}, Score4 at R, Score c at RR, and
  depth_B(4),depth_B(c)<=3. No V filter.
* R_B: one of the four cores in(1), marked root c, depth_B(a)<=5, and
  either Score4 at L with Score a at LL, or kind0 at L with Score4 at LL.
  No V filter.
* C_B: root4, depth_B(a)<=3, no extra A guard, and either core
      F6=4(L,5(E,6(E,7(E,8(E,E))))), or
      F8=4(L,5(E,8(7(6(E,E),E),E))).
* T_B: root8, depth_B(a)<=7, V subset U, no further A guard, and core
      H8=8(7(6(5(4(L,E),E),E),E),E).

The other key4 return

    F7=4(L,5(E,7(6(E,E),8(E,E))))                (2)

has every marked core at depth<=3 when depth(a)<=3, so its existing E1
floor already supplies one credit. It needs no new augmentation clause.

Every Score position is kind0/isS=true. Root's unused kind, anonymous
unused index, all nonreal unused fields, raw gap/NULL side pairs and
annotations keep their original freedom. Include the actual reverse
LOW predicates:4 fixed, largest marked d>4 replacing a, and5/6/7/8
replaced by3/2/1/0 with directions exchanged. No private weak-LE rank,
HIGH sentinel, annotation or psi table is reflected.

For any public Lambda<=D<=2 apply IN ORDER:

    D1=max(D,1_KB);
    D2=max(D1,1_RB);
    D3=max(D2,1_CB);
    D4=max(D3,1_TB);
    F =max(D4,2*1_GB).                           (3)

THEOREM. Every operation preserves every original LOW inequality valid
before it, individually. Every G_B-source LOW inequality holds for F.
Thus every nonnegative LOW edge ending in G_B is valid. Applying (3) to
D_direct gives the explicit debt

    D_buried=max(D_direct,1_KB,1_RB,1_CB,1_TB,2*1_GB). (4)

No global feasibility of D_direct, fixed point, selected private completion
or continuing port bill is assumed.

## 2 The extreme proxy parent lemma

In any original FINAL valid B tree, the minimum-gap proxy f has parent
Score0. Indeed it is a leaf and the smallest B key. A parent core p>0
would need Score0 in its left subtree, but that subtree is exactly the
single leaf f. All nine cores are present and the ordered tree is connected,
so this is impossible. Its parent cannot be another gap leaf either.
The actual maximum-gap dual has parent Score8.

Now start a terminal core splay from an intermediate minimum proxy root
f, whose current right child is z. After arbitrary bottom pairs, the last
step is one of these three universal forms:

    f(E,x(A,B)) -> x(f(E,A),B);
    f(E,z(A,x(B,C))) -> x(z(f(E,A),B),C);
    f(E,z(x(A,B),C)) -> x(f(E,A),z(B,C)).          (5)

Consequently f's final parent is either terminal x or that original
post-helper right child z. In the second form it is z; otherwise it is x.
For an even-depth terminal the first two original path edges f,Rz remain
until that last pair. For odd depth the remaining zig places f directly
under the terminal. The ordinary last-step proof works for a proxy root
as well as a core root; it is a statement about the same primitive rotations.

If the first minimum access has true depth h, its post-helper right child
is the old source root r for odd h, or the old source left child p for
even h. This follows by consuming the all-left bottom pairs: an odd h
ends with a zig of f/r; an even h ends with the r,Lp,Lf pair.

For B6/B7/B8, r is6/7/8 and p=5. For H8, r=8 and p=7. Neither possible
z is0. Combining(5) with final parent0 therefore forces terminal x=0.
The completed minimum-path lemma puts Score0 at depth ceil(h/2)<=5,
since h<=9. Its ORIGINAL terminal price is then q<=2,w2=4-q>=2.
No initial Score-emptiness assumption is used. Only final gap-leaf validity
is imposed; the intermediate proxy root may have children.

COROLLARY ON THE FULL ORIGINAL LOW RELATION. Any Gamma1 edge of weight0
or+1 has its initial helper B depth<=2. For a minimum helper at depth>=3,
the source root and its left child both differ from0; otherwise f would
already be at depth1/2. Thus the preceding proof forces terminal0 and
weight>=2. For a maximum helper, use source root/right child differing
from8 and final parent8. This excludes all deep-helper cheap edges
globally without sampling signatures or trees. It does not settle the
remaining shallow-helper zero/+1 edges.

## 3 One credit on K_B and R_B

At a genuine K_B source the actual A prefix is

    a(A,4(B,c(C,Y))), c in{6,7,8}.               (6)

The only marked H1 targets are4/c. All other marks are between4,c below
c.left, or above c below c.right, beyond depth2. Their guarded B depths
are<=3, giving price>=1. A fresh source G read uses slot0=a and cannot
create another active target. Minimum-helper L/LL/LR leaves only entry a
or4 eligible at charge1; c and its subtrees remain deeper. A maximum
helper is below c.right at depth>=3 and cannot fit Gamma1.

The completed unchanged-subtree argument puts old a at B depth<=2 after
the minimum proxy access and leaves a.right intact. Hence4 has depth<=5,
price>=2; terminal a has price>=3. Gamma0 uses the actual-preterminal floor.
This extends the already completed K5/K6 proof by the same ordered prefix,
not by assuming a new private symmetry. A newly raised K_B source has
debt1 and all its LOW rows are therefore valid.

For R_B every upper core has depth<=3 and a has depth<=5. With A Score4
at LL the lower a cannot be a charge1 H1 target. With Score4 at L and
a at LL, its only possible zero H1 target is a at B depth4/5. The exact
A return is

    c(4(a(A,B),C),Y) -> a(A,4(B,c(C,Y))).          (7)

Every R_B core has prefix c,L5,L4. If depth(a)=4, the core path is
c,L5,L4,Lp,epsilon a. The bottom pair places old4 at depth<=2 inside
the accessed subtree; the final c,L5,La pair increases that by at most1
and places old c at depth2. If depth(a)=5, consume the bottom pair below4,
then the 5,L4,La pair and final c/a zig. Old4 ends at depth2 and c at1.
Thus the actual B endpoint always satisfies depths(4),depth(c)<=3 and
the full A endpoint(7) is in K_B. D1 already gives it one credit.

There is no minimum Gamma1 helper in either R_B A guard: L/LL are Scores
or are forced above present4. A maximum helper pushes a deeper and has
only the five upper cores as eligible terminals. The lower block stays
under4.left, giving terminal depth<=5, price>=2. These statements include
Score-bearing support and actual source G behavior. Gamma0 is floor-safe.
All other H1 prices are>=1, so raising R_B to1 after K_B is LOW-safe.

K_B/R_B deliberately have no V filter. Old-owner G observations at an
incoming boundary may differ from a fresh source's slot0. Such boundaries
must receive credit even when they have no compatible next LOW source.
No boundary vertex or raw field is removed or identified.

## 4 One credit on root4 returns C_B

At C_B the lower marked a has B depth<=3. All upper cores have depth<=4,
so no H1 edge is negative. The only possible H1 zeros are8 in F6 and6
in F8; F7 has none and already lies in E1. Those two zero accesses give
B8 and B6 respectively, by the completed spine identities. The lower
subtree is unchanged and old4 ends at depth2, so a's new depth is<=5.

The full A endpoint receives one credit without retaining a hidden source
separator. If a is the actual source L child, an R/RL upper access leaves
Score4 at L and a at LL, satisfying R_B. An RR upper access leaves4 at
LL and again satisfies R_B, regardless of old-owner G observations.

If a is not the source L child, an R/RL upper access moves every actual
a beyond depth2. Source slot0=4 has left child different from a and a
modified upper right child; one-step G reads cannot expose a either.
All marked observed nonroot labels are then in U. The completed upper
height bound puts them at depth<=3, so the ACTUAL full endpoint is E1.
RR endpoints satisfy R_B directly. These cases cover arbitrary actual
source A prefixes, ports/anonymous blocks, and unused fields.

Thus every zero C_B row goes to R_B>=1 or the E1 floor>=1. Positive H1
rows are range-safe at debt1. Every Gamma1 edge from root4 has weight>=1
by the completed central-root theorem; Gamma0 retains its floor proof.
Raising C_B to1 after R_B therefore preserves every previous LOW row.

## 5 One credit on the long upper chain T_B

T_B has upper path8,L7,L6,L5,L4 and all lower cores below4. V subset U
excludes a as an H1 target. The only zero H1 target is4, at depth4;
the other upper targets have positive price. Splaying4 gives core

    Q4=4(L,7(5(E,6(E,E)),8(E,E))).               (8)

Every upper core has depth<=3. The cap depth_H8(a)<=7 says that the
unchanged distance from4 to a is<=3, so a's new depth is<=3 too.
EVERY marked core is therefore at depth<=3, irrespective of A/G/raw
observations. The full endpoint is E1 and already has Lambda>=1.

The minimum-helper parent lemma applies since root8 and left child7 are
nonzero, giving weight>=2. A maximum helper is a single B zig at8.right;
each upper core has preterminal depth<=5. The lower a is not an eligible
post-helper A terminal: source target-cover excludes it at depth1/2,
and a right-side maximum access pushes its old left branch still deeper.
Thus all such helper prices are>=2. Gamma0 is floor-safe. This proves
the one-credit T_B operation, including its zero return to E1.

## 6 Every cheap exit of B6 B7 B8

In a G_B source, either the LL separator hides a or the actual Score4
at LL hides it below4.left. Source G aliases cannot fabricate those
distinct Scores or an anonymous label from slot0=c. V supplies the full
boundary target cover. Every H1 target is in U, whose depths are<=3.
There are no zero or negative H1 exits from G_B.

The complete +1 core exit table is

| Source | Target | Exact core result | Credit supplied |
|---|---|---|---|
| B6 | 4 | F6 | C_B >=1 |
| B7 | 4 | F7 | E1 >=1 |
| B8 | 4 | F8 | C_B >=1 |
| B6 | 8 | H8 | T_B >=1 |
| B7 | 6 | B6 | E1 or R_B >=1 |
| B8 | 7 | B7 | E1 or R_B >=1 |
| B8 | 6 | B6p | E1 or R_B >=1 |

Other upper targets cost2. A key4 exit from either public A guard may
expose a directly at the new root's L child; C_B deliberately imposes
no extra A guard. Its lower depth is<=3 because source4 was at B depth2
and source a at depth<=5. F7 is E1 for all A observations.

For B6->8, the actual lower a remains unobserved: the upper access moves
the entire left block deeper, and old slot0=6 retains a child>=4, not a.
Its full endpoint has V subset U. Key4's B depth changes from2 to4, so
a's depth changes by2 and is<=7. Hence the endpoint satisfies T_B.

For the lower targets6/7, a source with Score4 at A L reaches an E1
endpoint: the separator stays at LL and a is hidden. With Score4 at LL,
the target is at L or LR. LR keeps4 at LL and a hidden, yielding E1.
At L, the target's A endpoint is

    x(4(K,D),c(E,Y)).                            (9)

If K's root is a, R_B supplies1. Otherwise a stays unobserved, including
G reads through old owner c whose children are now above x>4; the full
endpoint is E1. All three output cores have upper depths<=3, and their
lower a depth remains<=5. The R_B core B6p is auxiliary only, not a new
unproved two-credit frontier. These cases cover every private replacement.

Minimum helpers have price>=2 by section2: every main source root c
and left child5 differ from0, forcing terminal0. Maximum helpers push
the hidden a deeper; their eligible upper terminals use at most the five
upper cores, hence price>=2. No Score-empty helper assumption is made.
Gamma0 uses its actual-preterminal floor. Original H0/Gamma>1 exclusions
and source H1/H2 normal forms retain all full endpoints, H and terminal q.

Thus each +1 row ends at debt>=1 and every other H1/Gamma1 price is>=2.
All G_B-source LOW rows hold at debt2. Every previous valid row outside
a newly raised source only gains a target increment. For new sources in
K_B,R_B,C_B,T_B the value is1, with their zero rows explicitly supported
in the earlier order. This proves every operation in(3) individually.
Already-debt2 auxiliary sources are not claimed solved merely by a
one-credit operation; their previously valid rows are preserved.

All proofs also hold on actual reversed LOW witnesses. The helper-parent
lemma uses maximum gap9 and parent8; the opposite helper preserves the
other extreme subtree. K_B/R_B/C_B/T_B guards reverse constructors and
Score order. Their numeric prices and depth counts are the same, without
assuming reflection of private weak-LE ranks, B annotations or psi.

## 7 Complete S zero coverage and remaining scope

Reuse Transfer07's complete eight-spine map. Every remaining S-zero upper
edge has target core B6/B7/B8. Its old root4 ends at depth2 and its source
distance from4 to a was<=3, so the target has depth(a)<=5. R/RL actual
A endpoints keep4 at L and the unmarked/anonymous separator at LL;
RR puts4 at LL. Old owner4 has unmarked child p and an upper child, so
G does not expose a. Every full endpoint therefore satisfies G_B.

The original weight is0; (4) supplies target2 and gives residual

    0+D_buried(t)-D_buried(s)=2-D_buried(s)>=0.   (10)

This closes RLL/RLR/RRL/RRR, both separator types, all three actual A
target positions and both LOW orientations. The four previously completed
words remain valid under the safe operations. Thus ALL eight S upper-zero
words are now certified. S root5 (or dual3) has no upper H1 zero by count;
S's lower guarded target has positive H1 price. Central-root Gamma1 has
no zero and Gamma0 zero rows are already floor-valid. Consequently every
zero-weight LOW edge with an S source is covered, for all original masks,
admissible signatures and independently chosen compatible private witnesses.

The source guards and new capacity are nonempty: proper B_c cores with
a lower block of internal a-depth<=2 and proper A barrier prefixes realize
them. Marked child targets give real +1 key4 exits; C_B prefixes with a
as actual L child give zero upper returns to R_B; R_B with a at B depth4/5
gives its real zero return to K_B. H8 with a hidden in A has a real zero4
access. These are ordered-symbol constructions with arbitrary compatible
ports and symbolically positive populations when needed, not finite tests
or assertions about particular saved psi labels. D_buried itself gives
each genuine main source two credits.

Full-state closure is all147 ordinary/all127 midpoint coordinates, with
SAME actual midpoint, independent witnesses, free high v, weak LE/G/raw
unused fields, original H/q/prices and corrected h0 retained. Using the
inherited HIGH law with W(O)=-D_buried-5chi8 and W(M)=-5chi8 gives finite
weight>=-7 and fully closed weight>=0 for the stated covered LOW rows,
including the newly completed S zero rows. The graph/target are unchanged.

BEFORE: B6/B7/B8 S-zero capacity was open. RESULT: explicit five-stage
LOW-safe construction and the extreme-proxy parent lemma. AFTER: the
entire S-family zero frontier is closed and all deep-helper Gamma1 cheap
edges are excluded. Zero H1 sources outside S, shallow-helper zero/+1
Gamma1 edges not otherwise covered, global LOW validity, full M3 and
Dynamic Optimality remain OPEN. No new whole-signature certificate or
original negative-cycle claim is made.
