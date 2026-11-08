# Source-exact last-event synchronization and the diagonal debt floor

This is a necessary source lemma, not a funding theorem or a proposed
normalization. It explains why the diagonal-zero route in proof84 failed.
It supplements, and does not replace, the already accepted Gamma_r range
obstruction in SE03_STEP2_REPAY01/UNIFORM_RANGE_OBSTRUCTION.md.

## Frozen IAGS Box

Target: determine the source-forced debt at a diagonal endpoint.
Conditions: N>=4 physical ordered keys; a genuine full-B transition
T --KEEP x--> U inside an already source-closed marked B cycle. Its
original B depth is d>=1 and q=floor(d/2). Any tested debt is nonnegative
and obeys the original natural-packet law with one A-event price2-q.
Inheritance: ordinary bottom-up source semantics and the independently
checked UNIFORM_A_REALIZATION_OVER_CLOSED_B theorem. Ambiguities excluded:
we do not assert that every abstract B transition is recurrent, that a
given history used the preparation below, or that its credits are free
under a frozen allocation. Bridge: realize the actual last-event prestate
as the synchronized A shadow, producing a genuine H1 packet ending A=B.

## Uniform source lemma

Run the mathematical ordinary bottom-up splay of x in T. Immediately
before its LAST StepEv, call the full physical tree T_star. Then:

    root(T_star)=root(T),
    depth_(T_star)(x) is1 or2,
    S_x(T_star)=U.

PROOF. Each earlier double acts at a grandparent strictly below the
original root, hence changes no root key. It reduces x's depth by two.
The last event is precisely the remaining root zig at depth one or root
double at depth two. Every arbitrary hanging BST stays in its exact
source position under the original rotation formulas. This argument is
inductive in d and has no bound on physical population. Root-repeat d=0
is excluded from a genuine transition. QED.

T_star is used as a specified TREE, not as a sequence of partially applied
B rotations in A. The source-realization theorem supplies an actual
A-only ordinary access preparation from the common initial tree to that
tree, outside the packet under study. A genuine KEEP of the old root
synchronizes the natural boundary. The next original KEEP x has ACTUAL
A cost H=1 and full B cost Q=q, and ends with A=B=U. Keep the complete
given B closing cycle and perform the actual A-only reset. Its recurrent
full/erased/chart period is legitimate by the inherited source theorem.
Every preparation/reset event is physically present and charged outside
the displayed packet. This construction proves existence of such an
original-source packet; it never forces these events in another history.

## Necessary debt inequality

On this actual occurrence any proposed nonnegative natural-packet debt
must satisfy

    D_new(U,U) >= D_old(T_star,T)+q-2 >= q-2.

Consequently any state-only debt has diagonal lower bound max(0,q-2) at
this destination. If the debt also depends on recent-key charts, this
assertion concerns the ACTUAL constructed destination chart, not a freely
chosen fixed-chart representative. Incoming-chart lemmas are not extended.

In particular q>=3 rules out a globally diagonal-zero debt on this natural
packet domain. A=B alone does not mean all state debt is zero. If D lies
in an interval[0,K], necessarily K>=q-2. The inherited Gamma_r source
already realizes q=r-1, giving the known K>=r-3 natural-packet obstruction.
This last consequence is reused, not a new support theorem. Pairing or
coarsening genuine source packets changes the priced obligation and is
not refuted by the single-packet statement.

The failed proof84 assumed D10(U,U)=0. That assumption was checked before
use and failed. Its attempted minimum-rule refutation was rejected, its
CPU charged and its artifacts retained. The later actual min-rule witness
is different: it is the independently replayed weight+1 packet in
interior_min_contraction_closed_source.json, not a repaired diagonal claim.

No floor is added to the old D10 or Hamiltonian normalized debt. This
necessary condition is not combined with a refuted changing-chart floor.
It creates no physical donor or ownership license and does not prove CD.
