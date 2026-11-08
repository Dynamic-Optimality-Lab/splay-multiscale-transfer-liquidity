# Zero release coverage with a direct central barrier

The explicit operation below closes the new J7 successor and preserves
every previously valid LOW inequality. Together with completed J5/J6
theorems it covers all four direct-B-barrier words in the complete eight-
spine S-family zero frontier. Four buried-barrier words remain. This is
not exhaustive zero-weight LOW coverage on the whole graph.

## 1 The complete frontier being classified

Reuse Transfer03's S-family and its already proved counting argument.
At the smaller end a<4 are the first two marks. The source A root is4,
a is at LL, depth_B(a)<=3, and a zero H1 upper target c>4 has B depth4.
Every one of the four upper cores is on that path. The source B consists
of root4 with an arbitrary lower subtree L on0..3 and an upper path.
Write E for core-empty, and u1<u2<u3<u4 for the four formal upper roles.
They occupy ordinals5,6,7,8; these are theorem roles, not sampled keys.

After the initial right edge from4 there are three path directions. All
eight words are possible schemas; the inorder determines the ordered
upper labels uniquely. The exact successor classification is:

| Tail word | Upper path roles | Successor core | Status after this theorem |
|---|---|---|---|
| LLL | u4,u3,u2,u1 | J5 | Completed proof reused |
| LLR | u4,u3,u1,u2 | J6 | Completed proof reused |
| LRL | u4,u1,u3,u2 | J6 | Same existing certified successor |
| LRR | u4,u1,u2,u3 | J7 | New capacity proved below |
| RLL | u1,u4,u3,u2 | B6 | OPEN buried barrier |
| RLR | u1,u4,u2,u3 | B7 | OPEN buried barrier |
| RRL | u1,u2,u4,u3 | B7 | OPEN buried barrier |
| RRR | u1,u2,u3,u4 | B8 | OPEN buried barrier |

Here the complete six successor shapes are

    J5=5(4(L,E),8(6(E,7(E,E)),E));
    J6=6(4(L,5(E,E)),8(7(E,E),E));
    J7=7(4(L,6(5(E,E),E)),8(E,E));
    B6=6(5(4(L,E),E),7(E,8(E,E)));
    B7=7(5(4(L,E),6(E,E)),8(E,E));
    B8=8(5(4(L,E),7(6(E,E),E)),E).                (1)

The last three have4 at B depth2; J5/J6/J7 have4 at depth1. In every
row the exact active target is the last path role. Both paired rotations
are determined by the word. The two old P5/P6 identities and the old
complete upper-height bound are reused. Only the six remaining source
identities need new algebra. No tree/population bank or psi label is read.

Completeness is structural: depth4 consumes the four available upper
cores, leaving no off-path upper core. Every next left/right step fixes
the current extreme of the remaining ordered labels. This yields exactly
the eight words, rather than a finite test of a candidate classification.
The original source normal forms retain all full endpoints,H and q.

The LRL identification is reuse of existing J6 capacity, not a new sign
certificate. The actual dual gives the largest-pair frontier, reversing
directions and ordinal order in the LOW proof. No private assignment,
HIGH sentinel, interval or psi label is reflected.

## 2 Explicit public credit regions

All predicates require a valid core projection and root synchronization.
Use the existing full state, V, Lambda, psi and D_anon. At the smaller end
the two first marks are a<4. Define G7_minus by synchronized marked root7,
core J7, V subset U={4,5,6,7,8}, and either:

* Score4 at A L, with a kind0 separator at LL that is anonymous, OR is
  an unmarked Score k with a<k<4; or
* a kind0 node at L and Score4 at LL.

All stated Scores have kind0/isS=true. Anonymous index fields and root's
unused kind remain free. No separator gap, inventory or private identity
is read. Define the intermediate regions C_x, x=5/6, by root x marked,
7 marked, Score4 at A L, and the corresponding core

    C5=5(4(L,E),7(6(E,E),8(E,E)));
    C6=6(4(L,5(E,E)),7(E,8(E,E))).                (2)

Define K_x, x=5/6, by smallest marked root a, x and7 marked, Score4 at
R and Score x at RR, and core depths(4),depth(x)<=3. C and K have NO V
filter. This is essential for incoming full boundary states whose G
observations read through an old owner. Other A/B fields remain free.

Include the actual reverse LOW regions: middle4 fixed;7,6,5 become1,2,3;
directions exchange; root a becomes the largest mark d>4, with4 the
second-largest. Let G7,C,K be the unions of their two actual orientations.

For any explicit public Lambda<=D<=2 apply IN ORDER

    D1=max(D,1_K), D2=max(D1,1_C), F=max(D2,2*1_G7). (3)

THEOREM. Each operation preserves every original LOW inequality valid
before it. Every G7-source LOW inequality holds for F. In particular
every nonnegative LOW edge ending in G7 is valid. Apply (3) to D_anon:

    D_direct=max(D_anon,1_K,1_C,2*1_G7).          (4)

No global feasibility of D_anon is assumed. Predicates use current shared
coordinates and remain valid under independently changing private witnesses.

## 3 Parametric helper barrier lemma

Let c>4 be a marked synchronized root. Suppose actual A has Score4 at L
and core B has form

    c(4(L,T),R),                                (5)

where L contains the four lower cores, T has keys strictly between4,c,
and R keys above c. No other A guard or separator type is imposed.
Then every original H2/Gamma1 edge from this source has weight>=2.

For a maximum helper, A's lower marked a is below4.left, at depth>=2.
The helper is at R/RL/RR and pushes that entire block down, making a
ineligible for the charge1 terminal. Every eligible marked terminal is
in U. All lower B cores remain under4.left during this maximum proxy
access, so a terminal path uses at most the five upper cores. Its actual
preterminal depth is<=5, hence q<=2 and w2=4-q>=2.

A minimum helper can be only the actual anonymous LL node. The other
left positions are Score4 or above4; all right positions exceed c.
Its A splay has only4,c, or a as possible marked charge1 terminals.
Reuse the parametric parity identities of Transfer06. In B they are

    even helper depth: f(E,4(Q,c(T,R)));
    odd helper depth:  f(E,c(p(Q,4(S,T)),R)),       (6)

where p is a lower core. T and R are retained as arbitrary subtrees;
their sizes and shapes do not enter that proof. Terminals4/c have depth
at most3. For a<4, T and R are off the path. There are at most six relevant
cores{0,1,2,3,4,c}; even parity uses at most five.

The sole possible +1 price is terminal depth6 in the odd form. It uses
all six cores and forces path f,Rc,Lp,R4,Lv,epsilon u,eta a. After the
bottom pair, the two remaining RL pairs give

    a(f(E,p(Q,A)),c(4(B,T),R)).                  (7)

The final gap proxy has a real core child p, forbidden by ORIGINAL final
b_valid. Therefore every final-valid such terminal has depth<=5 and
weight>=2. This argument permits arbitrary Score-bearing helper support.
It imposes no leaf condition on the helper-rooted intermediate state.

This is Transfer06's same parity/count/leaf proof with unrestricted upper
T,R, not a new population test. In particular T may contain both5 and6
in J7, and the upper R may have the C5/C6 shape in(2). Hidden weak-LE rank
ties are not strengthened: the minimum gap argument uses only present
Score ranks, which are distinct. The actual reverse orientation uses
maximum helper9 and the corresponding final nonempty LEFT child.

## 4 One credit on K and C

K5 is a subclass of the completed Transfer05 K theorem. For K6 the actual
A prefix is

    a(A,4(B,6(C,Y))).                            (8)

All other marked Scores are either5 inside C or above6 inside Y, beyond
depth2. No mark besides a is below4. Thus H1 targets are only4/6, with
B depths<=3 and price>=1. The original source G reader reports root a
or one of its children, and cannot create another active target.

Minimum-helper L/LL/LR have the same three source identities as the
completed K5 proof with its final Score5 replaced by6. Only entry a or4
can be a charge1 terminal;6 is at depth>=3 and any5 is below it. A maximum
helper is hidden below6.right at depth>=3. In B the minimum access puts
old a at depth<=2 and leaves its right subtree untouched. Thus4 has
preterminal depth<=2+3=5, giving w2>=2; entry a gives w2>=3. This uses
no helper Score-emptiness assumption. K therefore tolerates a newly
raised debt1. Gamma0 retains its completed actual-preterminal floor law.

For C5/C6 every upper core has depth<=2 and a has depth<=5, since the
four lower cores begin under4.left at depth2. There is no negative H1
exit. Every positive exit tolerates source debt1 by range. The sole
possible zero target is a at actual A LL, with exact rewrite

    x(4(a(A,B),C),Y) -> a(A,4(B,x(C,Y))).          (9)

The old-child lemma extends with an arbitrary off-path T in(5). If a's
internal depth below4 is even, finish its internal splay with old4 at
depth<=2, then the remaining x/a zig increases that depth by at most1.
If it is odd, the final x,L4,La pair puts4 at depth1 and x at depth2.
Thus depth(4)<=3 and depth(x)<=2 in both cases. The full endpoint of(9)
belongs to K, including any extra observations through old owner slot0=x.
No V filter is imposed on that boundary. D1 already supplies at least1.

The helper lemma of section3 applies to C5/C6: actual A Score4 at L and
B form(5) hold, so every Gamma1 price is>=2. Gamma0 is floor/range-safe.
Consequently raising C to1 after K preserves every previously valid LOW
row. It does not assert that arbitrary already-debt2 C or K sources are
solved; unchanged sources retain their old valid rows by target monotonicity.

## 5 Two credits on the new J7 region

J7's complete H1 upper target list is4/8 at depth1, price2, and5/6 at
depth3/2, price1. A lower mark a is hidden by either source G7 guard.
If Score4 is at L, the unmarked separator at LL blocks an actual a at
depth2. If Score4 is at LL, its actual parent is between4 and7, and a
is below4.left at depth>=3. Source G cannot fabricate those distinct
Score observations or an anonymous label from slot0=7. V retains the
full-boundary target-cover condition. Thus no zero or negative H1 exit
from G7 exists.

For a +1 target x=5/6 the exact core outputs are C5/C6 in(2). If the A
source has Score4 at L, the target must be at LR and the separator stays
at LL after the access. Hence a remains hidden, including G observations,
and every marked visible label lies in U. All upper cores now have depth
at most2, so this actual full endpoint is E1 with Lambda>=1.

If Score4 is at LL, a target x=5/6 can be at L or LR. Their exact forms are

    7(x(4(K,D),E),Y) -> x(4(K,D),7(E,Y));
    7(q(4(K,D),x(E,F)),Y)
       -> x(q(4(K,D),E),7(F,Y)).                (10)

The first endpoint is C_x: a might be exposed at its LL, so E1 is not
assumed. The second retains Score4 at LL and a below depth2; old owner7
has children above x and cannot report a through G. It is E1. Both cases
have at least one credit under D2. Unmarked x gives no genuine edge.

For helpers, the A-L guard satisfies section3, so Gamma1 costs>=2.
With Score4 at LL, its parent q has4<q<7. No minimum helper can be at
depth1/2. A maximum helper is at R/RL/RR, moves the entire q/4 block down,
and has only U terminals in the five-upper-core bound, again costing>=2.
Gamma0 retains its actual-preterminal floor theorem. Original H0/Gamma>1
exclusions and H1/H2 normal forms are reused without repricing.

This proves every G7-source LOW row at F(s)=2. For the three operations
the new-source residuals are respectively: K positive w+F(t)-1>=0;
C zero to K gives F(t)-1>=0; G7 +1 gives1+F(t)-2>=0. Paid/helper edges
are range-safe. Unchanged sources only gain a target increment. Thus
every previously valid original LOW row is preserved by(3).

All arguments are also proved on the actual reversed LOW witnesses:
root1 replaces7, marked3/2 replace5/6, helper directions reverse, the
unchanged extreme subtree is left instead of right, and the forbidden
final gap child is LEFT. No psi symmetry or private rank reflection is used.

## 6 Original zero edges and advancement

In an S zero release the actual source is4(p(a(A,B),C),Y). The separator
p is an unmarked Score or anonymous because a,4 are the first two marks.
Use the already proved R/RL/RR A identities. For R/RL the endpoint has
Score4 at L and the same separator at LL; for RR it has Score4 at LL.
Old owner4 has unmarked child p and an upper block, so G cannot expose a.
These full endpoints satisfy the corresponding public guards.

For tail LRL the core is existing J6, so completed Score/anonymous and
RR guards already give two credits. This is reuse, not a new certificate.
For LRR the core is J7, so(4) gives two credits at every such endpoint,
in all three A positions and both separator types. The original H1 price
is0 and the signed residual is2-D_direct(source)>=0, with equality if
the source carries2. No claim that the old candidate actually failed or
that a particular saved psi label equals2 is required.

The newly saturated J7 region is nonempty: take a genuine prefix
7(q(4(K,D),E),Y) with marked q=5/6 and marked first pair a,4, complete
the five marks with7 and one remaining upper key, and place the other
Scores in proper ordered ports. J7 with any compatible lower block gives
an actual +1 exit to C_x, and D_direct assigns source2. A counterpart
with an unmarked/anonymous separator gives the L guard. Proper S prefixes
also realize the LRR zero access with any required symbolically positive
gap population. This is analytic construction, not numerical testing or
an asserted old-debt2 lookup.

Retain every D_anon valid row. Together with the earlier results, all four
smaller-end tail words beginning L and their actual duals are now covered.
The four words beginning R reduce to exactly B6/B7/B8, which remain OPEN.
The table is exhaustive ONLY for the S-family upper zero frontier. It is
not a claim for zero H1 edges in other marked configurations, general
debt transfers, or all Score-bearing H2 zero edges outside the proved
helper barriers and other inherited source classes.

With the inherited HIGH/h0 law, W(O)=-D_direct-5chi8 and W(M)=-5chi8
give finite weight>=-7 and full closed weight>=0 for walks whose LOW legs
are previous valid rows, G7-source rows or nonnegative incoming-to-G7 rows.
All147 ordinary/all127 midpoint fields, SAME actual midpoint, independent
witnesses, free high v, weak LE/G/unused fields and original H/q/prices
remain. The graph and target are unchanged.

BEFORE: six source spine arrangements were not explicitly mapped; J7
capacity and its C6/K6 transfers were unproved. RESULT: complete eight-to-
six frontier map, one reuse identification, and the explicit LOW-safe J7
capacity with its helper bound. AFTER: the direct-B-barrier half is closed;
three buried-B successor arrangements and global zero/+1 completeness
remain OPEN. Full M3/Dynamic Optimality remain OPEN. No new whole-signature
certificate, original negative cycle or global zero theorem is claimed.
