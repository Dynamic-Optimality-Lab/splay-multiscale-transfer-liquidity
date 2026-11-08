# Two credit repayment for the P5 and P6 RR releases

The construction below gives a LOW-safe public two-credit successor for
both P5/P6 zero accesses at A position RR, including the case where the
intervening Score5 is marked. Its scope is these core patterns and their
actual LOW order-duals. It does not assert exhaustive debt-transfer coverage.

## 1 Public regions and theorem

Reuse the exact original LOW normal forms, V, Lambda, psi, D_release and
all their totalizations. Write E for core-empty and L for an arbitrary
ordered core subtree containing the four cores below Score4. Let a<4 be
the two smallest marked keys, so a is the only marked key below4.
Other fields, gaps, annotations and private realizations remain free.

The established core source and successor patterns are

    P5=4(L,8(7(6(5(E,E),E),E),E));
    P6=4(L,8(7(5(E,6(E,E)),E),E));
    J5=5(4(L,E),8(6(E,7(E,E)),E));
    J6=6(4(L,5(E,E)),8(7(E,E),E)).                 (1)

An access to5/6 in P5/P6 has B depth4, H=1, q=2 and weight0.
These completed identities and prices are reused, not recomputed.

Define Z_minus using only the full shared state:

* A root and core B root are the same marked c=5 or6;
* core B is J5 or J6 respectively;
* alpha L has kind0, and alpha LL is kind0 Score4;
* V is a subset of U={4,5,6,7,8}.

Define C_minus by root synchronization at marked5, second-smallest mark4,
kind0 Score4 at alpha L, and core

    C5=5(4(L,E),6(E,8(7(E,E),E))).                (2)

Define K_minus by root synchronization at the smallest mark a<4,
second-smallest mark4, marked5, Score4 at R, Score5 at RR, and

    depth_B(4)<=3, depth_B(5)<=3.                 (3)

All stated Score positions have kind0 and isS=true. Root's UNUSED kind
is free. C and K have NO V filter. In particular a target boundary state
with extra observations through an old G owner must not be excluded.

Include Z_plus,C_plus,K_plus in the actual reverse Score order:4 stays4,
5/6 become3/2, 7/8 become1/0, L/R exchange, and the two largest marks
are4<d. Thus Z_plus has Score4 at RR, C_plus has Score4 at R and root3,
and K_plus has root d, Score4 at L and Score3 at LL, with both depths<=3.
This defines actual predicates in both orientations; it does not reflect
private weak-LE ranks, HIGH sentinels or psi labels.

Put Z=Z_minus union Z_plus, and similarly C,K. For any public function
Lambda<=D<=2 apply these operations IN ORDER:

    D1=max(D,1_K), D2=max(D1,1_C), F=max(D2,2*1_Z). (4)

THEOREM. Each operation preserves every original LOW inequality valid
before that operation. Every Z-source LOW inequality holds for F.
Consequently every nonnegative LOW edge ending in Z holds for F.

Apply (4) to the prior D_release, defining explicitly

    D_RR=max(D_release,1_K,1_C,2*1_Z).             (5)

No global feasibility assumption on D_release is used. No private witness,
inventory, port bill, hidden separator identity or history enters (5).

## 2 A depth bound for an access below the left child

Let a<b<u, and consider an ordered core tree u(b(L,E),R), with a in L.
After splaying a, old b has depth<=3 and old u has depth<=2.

Let d be a's depth within the subtree rooted at b. If d is even, all
bottom pairs lie inside b's subtree. They finish its splay at a, with
old b at depth<=2 by the completed old-root last-step lemma. The one
remaining zig between u and a moves that right-side b down by at most1.
Thus b has final depth<=3 and u has depth1.

If d is odd, consume the bottom pairs inside b until a is its left
child. The final path u,Lb,La is a same-direction pair:

    u(b(a(A,B),C),R) -> a(A,b(B,u(C,R))).          (6)

Hence b has depth1 and u has depth2. This proves the bound for arbitrary
path length and arbitrary side subtrees; no path or topology census is
needed. The reversed argument gives the corresponding right-child bound.

## 3 The one credit return region K is LOW safe

At any genuine K_minus source the A prefix has the actual form

    a(A,4(B,5(C,Y))).                            (7)

The nonroot distinct Scores4/5 cannot be G fabrications: a source G read
reports source slot0=a, and propagating through it cannot report those
two distinct labels at R/RR. All other marked keys exceed5. A depth-two
actual marked terminal is therefore4 or5; each has B depth<=3 by (3),
so its H1 weight is>=1. This proves H1 safety when a source is raised to1.

Only a minimum-gap helper can have A charge1. A maximum-gap helper must
lie below5.right at depth>=3. The three possible minimum-helper positions
are L,LL,LR; their exact first-access outcomes, with arbitrary blocks, are

    a(f(A,B),4(C,5(D,Y)))
       -> f(A,a(B,4(C,5(D,Y))));
    a(p(f(A,B),C),4(D,5(E,Y)))
       -> f(A,p(B,a(C,4(D,5(E,Y)))));
    a(p(A,f(B,C)),4(D,5(E,Y)))
       -> f(p(A,B),a(C,4(D,5(E,Y)))).             (8)

Thus the only possible charge1 marked terminals after that helper are
the entry a and, in the first/third case,4. Score5 stays at depth>=3.
This overapproximation is enough; original final-validity conditions may
exclude some of these edges and are never weakened.

In B, a minimum proxy access leaves the old root a at depth<=2 and
does not change its original right subtree. Since4 was a descendant
there at depth<=3, its post-helper depth is<=2+3=5. The terminal prices
are therefore q<=1,w2>=3 for a and q<=2,w2>=2 for4. Both tolerate source
debt1. No helper Score-support assumption is used. Gamma0 uses the
completed ACTUAL preterminal floor law, since all functions remain>=psi.

If D1(s)>D(s), D1(s)=1 and the preceding H1/Gamma1 bounds prove the
inequality directly; Gamma0 is already valid by range/floor. Otherwise
the source is unchanged and the target can only increase. Hence the
first operation in (4) preserves each previously valid LOW row.
This is a one-credit operation, not a claim for arbitrary debt2 K sources.

## 4 The one credit intermediate region C is LOW safe

In C5 every upper-group core has depth<=3:4/6 have depth1,8 depth2,
7 depth3. The only possible marked lower terminal is a. It has depth<=5:
the four-node arbitrary lower subtree L starts at depth2 and has internal
depth<=3. Hence no H1 edge is negative. Every positive H1 edge tolerates
a newly raised source debt1 by range.

A zero H1 edge must target a. Because Score4 is at A L, its only possible
charge1 A location is LL. The exact rewrite is

    5(4(a(A,B),C),Y) -> a(A,4(B,5(C,Y))).          (9)

Lemma (6) gives B depths(4)<=3 and(5)<=2. The ACTUAL full endpoint lies
in K, even if a G observation through old slot0=5 adds another marked
label elsewhere in its shadow. K has no V restriction. D1 already gives
every such endpoint at least1, so the zero residual is>=1-1=0.

For Gamma1 use the completed central-root theorem: any source core root
in[3,5], including5 here and3 in the dual, has w2>=1. This includes
Score-bearing helpers and is enough at source debt1. Gamma0 again uses
its completed actual-preterminal floor proof. Unchanged sources gain
only a target increment. This proves the second safe operation in (4).

## 5 All two credit exits from Z

In a genuine Z_minus source, the observed Score4 at LL forces both
its own node and its L parent q to be present and actual. If L were an
out-of-range kind0 ref, shadow7 would read source slot0=c at LL, not4.
If LL itself were such a ref it would also report c, not4. Proper Score
order therefore gives 4<q<c. Every present lower marked key a lies below
4.left, at actual depth>=3. This applies separately to every fresh source
witness with this shared guard. No hidden separator is inferred.

V restricts all H1 targets to U. Reuse the complete Transfer04 upper-core
depth/price identities:4 and8 have weight2; the only weight1 targets are
6/7 in J5 and5/7 in J6. All four successor core trees put U at depth<=3.
These completed identities are not rerun.

For a larger target x>c, its A location is R/RL/RR. The entire left q/4
block moves deeper, so a stays below depth2. Source slot0=c retains left
child q>4; its modified right child is also upper. A one-step G observation
cannot reveal a. Thus the full endpoint has V subset U and lies in E1,
with Lambda>=1.

For the lower target5 in J6 there are exactly two active A possibilities:

    6(5(4(K,D),E),Y) -> 5(4(K,D),6(E,Y));          (10)
    6(q(4(K,D),5(E,F)),Y)
       -> 5(q(4(K,D),E),6(F,Y)).                  (11)

They are target positions L and LR respectively. In (11), q is between4
and5;4 stays at LL and a remains below depth2. Old slot0=6 has children
above5 after the rewrite, so G cannot expose a. Its endpoint is E1.
In (10) the lower block K may have a at its root in a fresh witness.
The successor is therefore NOT asserted to lie in E1. Its core is C5 by
the reused J6->5 identity and its A child is Score4. It lies in C, and
D2 supplies at least1. This is the exceptional +1 transfer closed here.

Every weight1 Z exit consequently has F(t)>=1, and every weight2 exit
is range-safe. There are no weight0 or negative H1 exits from Z.

For Gamma1 no minimum helper is at depth1/2: L is q>4, LL is Score4,
LR is above q, and every right position is above c. A maximum helper
is at R/RL/RR. Its splay moves the entire q/4 block down, so a cannot be
a charge1 terminal. Reuse the five-upper-core B helper bound of
Transfer04: all eligible terminals lie in U, the lower block remains
under4.left, their actual preterminal depth is<=5, and w2>=2. This is
range-safe at debt2, including Score-bearing helpers. Gamma0 is floor-safe.

These arguments prove ALL Z-source LOW inequalities at debt2. Outside Z
the third operation changes only targets of previously valid rows. This
completes the safe-augmentation theorem, with residuals

    weight1 to E1/C: 1+F(t)-2 >=0;
    weight>=2:       w+F(t)-2 >=0;
    C zero to K:     0+D2(t)-1 >=0.              (12)

All proofs also hold in the actual reversed LOW orientation. In K_plus
the sole possible helper is maximum-gap9, its eligible terminals are d/4,
and old d.left is untouched. C_plus has source core root3. Z_plus admits
only minimum-gap0 helpers, and its terminal paths use the five lower cores.
No psi symmetry or private rank reflection enters any proof.

## 6 The original RR zero releases

Let k be the observed unmarked Score separator at the P5/P6 source,
with a<k<4, and K=k(a(A,B),C). Let c=5/6 be a marked RR target. The exact
A identity, with all blocks free and 4<q<c, is

    4(K,q(D,c(E,F))) -> c(q(4(K,D),E),F).          (13)

It puts Score4 at LL. The source owner slot0=4 has new children K and D.
K's root k is unmarked and D lies above4, so no endpoint G observation
can fabricate a. The actual a is at depth>=4. Every visible marked
nonroot label is in U. The full endpoint therefore satisfies Z, for
every compatible original realization. Score5 as a marked q is allowed.

The already proved P5/P6 core access and original H1 normalization give
weight0 and core J5/J6 without changing endpoints, H or terminal q.
Consequently its new signed residual is

    0+D_RR(t)-D_RR(s) = 2-D_RR(s) >=0.           (14)

When the source has debt2 this is0. Nonnegative incoming-to-Z edges also
follow immediately from range. This deletes the whole named A-RR family,
not only sources whose lower marked key was already shallow at the target.

Nonvacuity reuses Transfer04's two formal depth8 predecessors and its
negative-core/range proof forcing psi(P5/P6)=2 on the stated lower blocks.
Choose the already specified smallest marked a and unmarked Score k.
In P5 an arbitrary actual anonymous q between4 and5 realizes RR (its
gap population is symbolically positive). In P6 Score5 can be q, and
can be marked, with4,6,a and one larger core completing the mask.
Proper ordered ports contain all remaining Scores. This realizes debt2
RR sources analytically within the inherited limits, without querying
psi labels, assigning numerical populations or evaluating a compiler root.

## 7 Original graph consequence and remaining obligations

Equation (5) retains every completed D_release LOW row and adds every
Z-source row plus every nonnegative incoming-to-Z row. The inherited
HIGH/h0 law with W(O)=-D_RR-5chi8 and W(M)=-5chi8 gives finite weight>=-7
and full closed weight>=0 on walks whose LOW legs are prior covered legs,
the new Z-source legs or nonnegative incoming-to-Z legs.

All147 ordinary/all127 midpoint coordinates, SAME actual midpoint,
independent private witnesses, free high v, weak LE, G, raw unused fields,
original H/q/prices and corrected h0 are retained. These are predicates
for a proof function, not graph restrictions or vertex identifications.

BEFORE: the P5/P6 A-RR zero-release family was open. RESULT: the explicit
three-region operation (4) proves its signed repayment and retains all
previous valid LOW rows. AFTER: this named family is deleted. General
anonymous-separator releases in other A positions, other core patterns,
global weight0/+1 coverage, full M3 and Dynamic Optimality remain OPEN.
No new whole-signature certificate or original negative cycle is claimed.
