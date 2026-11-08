# Two credit repayment with an anonymous separator

An explicit public augmentation closes the anonymous-separator P5/P6 zero
releases at R and RL. Their RR counterparts use the completed Z theorem.
The extension permits every compatible private gap and Score inventory
at each edge. Its scope is the stated two core patterns, not all anonymous
separators in the full graph.

## 1 Public definition and theorem

Reuse the original full state, LOW normal forms, V, Lambda, psi, D_RR,
and the established P5/P6 and J5/J6 core patterns. At the smaller end let
a<4 be the first two marked keys. All other marks exceed4. For an arbitrary
lower core subtree L on0..3, the relevant successors are

    J5=5(4(L,E),8(6(E,7(E,E)),E));
    J6=6(4(L,5(E,E)),8(7(E,E),E)).                 (1)

Define N_minus by these public conditions:

* A root and B core root are the same marked c=5 or6;
* core B is J5 or J6 respectively;
* alpha L is kind0 Score4;
* alpha LL is kind0 and isS=false, hence anonymous;
* V is a subset of U={4,5,6,7,8}.

The anonymous slot's unused index is free. No predicate assigns its gap,
rank, identity or private Score support. Root's unused kind, nonreal unused
fields, B gap leaves, annotations and off-path raw side pairs remain free.
Reuse the existing invalid-core totalization; N requires a valid projection.

N_plus is the actual reverse orientation: the two largest marks are4<d,
root c is3 or2, the core is the constructor/order-dual of (1), Score4 is
at R, anonymous kind0 is at RR, and V is a subset of{0,1,2,3,4}. This is
a definition on actual states, not a reflection of private weak-LE ranks,
HIGH sentinels, interval fields or psi values. Set N=N_minus union N_plus.

THEOREM. For any explicit public Lambda<=D<=2,

    F=max(D,2*1_N)                               (2)

preserves every original LOW inequality valid for D, individually.
Every original LOW edge with source in N is valid for F. Apply to D_RR:

    D_anon=max(D_RR,2*1_N).                       (3)

All nonnegative incoming LOW edges to N are then valid. No feasibility
of D_RR outside its proved domain is assumed.

## 2 Visibility without learning the anonymous gap

At a genuine N_minus source the actual A prefix is

    c(4(p(A,B),C),Y),                            (4)

where p is anonymous. The two observed nonroot positions are actual:
a source G alias reports source slot0=c, which is a Score, and so cannot
produce the anonymous isS=false observation at LL. Score4 at L likewise
cannot be a fabricated copy of c. Port/empty prefixes propagate nonzero
kind and do not yield an active slot at LL.

Any PRESENT marked a<4 must occur under4.left, whose actual root p is
anonymous. It is therefore at depth>=3, whether it is below p.left or
p.right. A hidden marked a is not an active target. This depth statement
needs no comparison between p and a and holds in every fresh source
witness; no earlier private allocation is retained.

This replaces the old observed-Score separator argument. It does NOT
exclude p as a possible minimum-gap helper. That extra case is handled
below using final B validity, not an inferred private color.

## 3 All H1 exits from N tolerate two credits

H1 target cover and V restrict genuine marked targets to U. Reuse the
completed upper-core identities:4 and8 have weight2; the only weight1
targets are6/7 in J5 and5/7 in J6. Each of the four weight1 core successors
places every core of U at depth<=3. No core identity or psi label is queried.

For an upper target x>c at R/RL/RR, the entire left4/p block moves deeper.
The marked a stays unobserved. Old slot0=c keeps child4 on its left, and
its modified right child is above4. Thus a cannot be exposed through a
one-step G observation either. All marked labels observed at the full
endpoint are in U. The endpoint belongs to E1 and has Lambda>=1.

For J6's lower weight1 target5, actual order forces it to LR:

    6(4(p(A,B),5(C,D)),Y)
       -> 5(4(p(A,B),C),6(D,Y)).                 (5)

The anonymous p remains at LL and a stays at depth>=3 on either side
of p. Old owner6 has children above5, which cannot report a through G.
The full endpoint again belongs to E1. These are all weight1 exits.

Consequently weight1 exits satisfy1+F(t)-2>=0. Weight2 exits are range-safe;
there is no weight0 or negative H1 exit from N. This includes charged
DELETE/zero-KEEP forms via the inherited SAME-endpoint H1 normalization.

## 4 The extra minimum helper and its exact B bound

Use the completed Gamma1 normal form: an anonymous extreme-gap helper
followed by a marked terminal, each with A charge1, with H=2 and original
terminal-only q. No Score-empty helper assumption is made.

At N_minus a minimum-gap helper can be only p at LL. L is Score4; LR is
above that present Score; every right position is above present root c.
An active gap0 fringe precedes every PRESENT Score: inv._gapof counts
strictly smaller full Score ranks, and present ranks are distinct. This
argument requires no strict inequalities for hidden ranks or port bills,
and preserves the original weak-LE compatibility constraints.

Splaying this helper has A identity

    c(4(f(A,B),C),Y) -> f(A,4(B,c(C,Y))).          (6)

The only charge1 marked terminals are4 at R, c at RR, or a as the actual
root of B at RL. Other marks exceed4 and are below c, beyond depth2.
If a is the terminal, the exact second rewrite is

    f(A,4(a(B,C),c(D,Y)))
       -> a(f(A,B),4(C,c(D,Y))).                 (7)

The following bound avoids any need for an extra credit at (7).

LEMMA. Starting from either B core in (1), every original final-valid
Gamma1 edge using the minimum proxy has terminal B depth<=5. Hence
q<=2 and w2=4-q>=2.

Proof. Write b=4 and c=5/6. The source core is c(b(L,T),R), where T is
core-empty or the singleton5, respectively. The minimum proxy f hangs
below Score0. Its true path starts c,Lb,L..., and has only left directions.
Other gap proxies remain off-path leaves. Put h=depth(f).

If h is even, consume the bottom pairs below b. The last pair is
c,Lb,Lf and the intermediate tree is

    f(E,b(Q,c(T,R))).                            (8)

If h is odd, the last pair inside b is b,Lp,Lf, with p a lower core,
followed by the final c/f zig. The intermediate tree is

    f(E,c(p(Q,b(S,T)),R)).                       (9)

Q,S are arbitrary lower-core blocks; all other leaf side pairs travel
unchanged. The source has four lower cores, so h>=3, making both forms
exhaustive. These are parity normal forms of the actual bottom-up decoder,
not a catalog of sampled trees.

The terminal4 has intermediate depth1 or3 and terminal c has depth2 or1,
so both have q<=1 and w2>=3. Consider the only remaining terminal a<4.
In (8), c and T are off its path. At most five cores can occur after f:
the four lower cores plus4. Therefore its depth is<=5.

In (9), T is off every path to a<4, including T=Score5 in J6. The only
possible core ancestors/terminal are{0,1,2,3,4,c}, six cores in total.
Thus depth(a)<=6. If it is at most5 we are done. Suppose it is6, the
only possible weight1 case. The path must use all six cores. It must
therefore pass through p and b in (9), and a>p. Its path is exactly

    f,Rc,Lp,Rb,Lv,epsilon u,eta a.               (10)

Here p,v,u,a are the four distinct lower cores and epsilon,eta are the
two directions of the final lower pair. If a were in p.left, b would
be absent from its path and depth6 would be impossible.

The first bottom pair replaces the v/u/a subtree by a(A,B). The two
remaining pairs are then p,Rb,La followed by f,Rc,La. Their exact result is

    f(E,c(p(Q,b(a(A,B),T)),R))
       -> a(f(E,p(Q,A)),c(b(B,T),R)).             (11)

The final proxy f has a real core right child p. Original FINAL b_valid
requires BOTH child kinds of EVERY gap slot to be EMPTY. Equation (11)
violates that requirement. Depth6 is therefore impossible for an original
final-valid edge. The contradiction is at the final endpoint only; no
leaf condition was imposed on the helper-rooted intermediate state.
This proves the lemma, including arbitrary Score-bearing helper support.

## 5 Remaining LOW cases and safe augmentation

A maximum-gap helper may be at R/RL/RR. Its A splay moves the whole4/p
block down; a cannot become a charge1 terminal. Every eligible terminal
lies in U. Reuse Transfer04's five-upper-core B bound, giving terminal
depth<=5 and w2>=2. The separator's private gap is irrelevant to this
maximum-helper argument. Helpers absent under a particular sigma are
not invented. The minimum and maximum cases cover Gamma1 completely.

Gamma0 uses the completed ACTUAL preterminal floor theorem, since
F>=D>=Lambda>=psi and F<=2. The original H0/Gamma>1 exclusions and the
complete H1/H2 normal forms are reused with unchanged endpoints/prices.

On N every H1 weight1 exit reaches E1, and every other H1 or Gamma1
exit has weight>=2. Together with Gamma0 this proves all N-source LOW
inequalities at F(s)=2. If s is outside N its debt is unchanged and only
F(t) can increase, preserving each previously valid inequality. Hence
(2) is LOW-safe without a global feasibility premise.

At N_plus, the anonymous RR node may instead be a maximum-gap9 helper.
Reverse the constructors in (6)-(11) on the actual ordered LOW witness.
The possible cores are{4,5,6,7,8,c}; terminal depth6 leaves f with a real
LEFT core child, again forbidden by final b_valid. The opposite minimum
helper uses the five-lower-core bound. The same signed result follows
without reflecting weak-LE inventories, original annotations or psi.

## 6 Anonymous P5 and P6 source releases at every target position

An anonymous-separator source has actual prefix4(p(a(A,B),C),Y), where
p is anonymous and a<p<4 in that source. Do not carry this ordering into
a subsequent witness. Put K=p(a(A,B),C). Its three target-c identities are

    4(K,c(D,E)) -> c(4(K,D),E);
    4(K,q(c(D,E),F)) -> c(4(K,D),q(E,F));
    4(K,q(D,c(E,F))) -> c(q(4(K,D),E),F).         (12)

In R/RL, Score4 is at L and the anonymous p is at LL. Actual a is at
depth3; old owner4 has children p and a block above4, so G cannot report a.
The full endpoint satisfies N. In RR, Score4 is at LL and a at depth4;
old owner4 still has anonymous child p and an upper block. The endpoint
satisfies Transfer05's Z, whose public guard never required Score k.
Its already proved two-credit capacity applies directly.

Reuse the completed core identities P5->J5 and P6->J6 and their original
H=1,q=2,weight0. Under (3) all three actual target positions end at debt2,
so each zero release has residual2-D_anon(source)>=0. Source debt2 gives
residual0. Every previously valid D_RR row remains valid. No old potential
evaluation at these targets is needed or asserted to have failed.

Nonvacuity reuses the two formal depth8 predecessor identities forcing
psi(P5/P6)=2. Their lower blocks are the completed ones. Select a as the
smallest lower core and choose an actual anonymous p with a<p<4, using
an arbitrary symbolically positive intervening gap population. Proper
ordered ports hold all other Scores. R/RL/RR c=5/6 prefixes in (12) realize
original debt2 zero sources within the inherited caps. No population is
sampled, no original source root evaluated, and no saved psi label queried.

## 7 Exact graph advancement

D_anon retains all previously valid D_RR LOW rows and adds all N-source
rows and all nonnegative incoming-to-N rows. The named anonymous P5/P6
zero releases are now closed in all three A positions and both actual
LOW orientations. The proof covers all original admissible signatures
and independently changing compatible private completions in this domain.

Reuse HIGH/h0 with W(O)=-D_anon-5chi8 and W(M)=-5chi8. Finite walks have
weight>=-7 and fully closed walks have weight>=0 when their LOW legs are
previously covered rows, N-source rows, or nonnegative incoming-to-N rows.
Closure is all147 ordinary/all127 midpoint coordinates, with SAME actual
midpoint, independent witnesses, free high v, weak LE, literal-slot0 G,
raw unused fields, original H/q/prices and corrected h0 retained.

BEFORE: anonymous P5/P6 R/RL releases lacked a proved two-credit capacity;
RR's anonymous incoming case was not stated. RESULT: (2)-(3), including
the final-leaf exclusion of the only possible +1 minimum-helper exit.
AFTER: those original releases are deleted without introducing unpaid
new source rows. Other core arrangements, general zero/+1 coverage, full
M3 and Dynamic Optimality remain OPEN. No whole-signature certificate or
original negative cycle is claimed.
