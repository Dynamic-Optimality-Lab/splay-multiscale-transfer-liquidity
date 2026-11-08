# Joint residual quotient theorem — exact scope

## Box JFR-Q

Target: compress ALL actual natural/frozen paths into one simultaneous repair
system, and characterize its physical feasibility without losing shared
owner bottlenecks. Conditions: the actual D,U,h0,a0,Gamma and original path
license, as frozen in the frontier definition. Inheritance: original finite
h/l exchange, natural h0 and accepted natural prior. Ambiguity: arbitrary
source-derived repair eligibility and its compatible working schedule.
Bridge: the theorem below characterizes a fixed seed-policy fiber; a
universal source license and schedule are still needed for the parent.

## Q1: actual component compression (no eligibility assumption)

Use R,S,B,rho,k from GENUINE_EXCESS_FRONTIER_DEFINITION.md. The compressed
graph for a proposed repair b has edges `r -> b(r)` and fixed edges
`s -> rho(s)`. Roots are B and actual free terminals are rho(S) intersect T.
Each compressed edge expands to its exact original path. No two expansions
share an interior vertex, original demand or bit. Owner-only natural cycles
are irrelevant to root feasibility and cannot be used as free credit.

For ANY injective partial b:V->S, V subset R, b augments h0 adequately for
all outstanding roots iff every B path in this compressed graph ends at
an actual free T bit instead of a hole. Thus compression is exact FOR
EACH proposed comparison, even if the policy is state-dependent. No claim
that independently allowed seed edges compose has been used.

Proof. Expand fixed rho chains and repair edges, obtaining exactly the
h0 union b / inverse-a0 walk. Each bit has at most one b predecessor, every
rho endpoint has one initial component, and B has no incoming rho edge.
Therefore paths cannot enter cycles or merge. Every finite path stops at
a missing comparison entry or a free T endpoint. The old exchange theorem
then applies, appending only root-to-terminal pairs. QED.

## Q2: exact STATIC-POLICY Hall criterion

Additional hypothesis F: one independently justified source policy gives
L subset R x S, and permits all injective partial seed choices from L
jointly at the physical/comparison layer in question. Extra Gamma
reservations are part of that justification. Source/block/Bank scheduling
is either separately supplied or left as a separate obligation. This
hypothesis is NOT proved for the entire original source domain here.

Let J be the bipartite relation

    J(r) = L(r) union {k(r) if r in R\B}.

Edges k are VIRTUAL FROZEN STAYS, not new comparison donors. Then the
following are equivalent:

1. Some injective partial b from L is adequate for all B.
2. The alternating directed graph `r -> s` from L and `k(r) -> r` has
   |B| disjoint augmenting paths from B to S\im k.
3. J has a matching covering ALL of R.
4. For every X subset R,

       |N_L(X) \ k(X\B)| >= |X intersect B|.                 (QH)

The formula includes paid intermediate holes, not only roots. It counts
net virtual neighbor capacity, NOT initially unowned physical bits.
Actual unowned terminal bits are obtained only by rho and the proven paths.

Proof 1<=>2: Q1, with rho(s)=r exactly when s=k(r); rho(s) is free otherwise.
Every adequate partial plan supplies the paths. Conversely retain only the
comparison edges on disjoint paths. They define one injective partial b.

Proof 2=>3: toggle k along the disjoint alternating paths. No k-covered left
vertex loses coverage; each root gains it. Since dom k=R\B, all R is covered.
These toggles are algebra on virtual pairs. The ACTUAL a0 is not modified.

Proof 3=>2: compare a covering matching M in J with k. In M symmetric-
difference k, the component starting at each B is an augmenting path to an
unused S vertex. Interior M edges different from k lie in L. No two such
components meet. Alternating cycles can be discarded. This produces 2.

Proof 3<=>4: the finite matching theorem follows by the elementary
augmenting-path argument: if a maximal matching leaves a left vertex
uncovered, its alternating reachable left set X has fewer neighbors than
vertices; otherwise augment to a free right vertex. Conversely a covering
matching injects X into its neighbors. Here
`N_J(X)=N_L(X) union k(X\B)` and |k(X\B)|=|X\B|. Subtract that term to obtain
exactly QH. This proves both directions, rather than assuming expansion.

## Q3: the stronger unchanged E_r2 criterion

For a factorable independent seed policy L, a FULL independent repair has
the stronger criterion

    for all X subset R: |N_L(X)| >= |X|.                    (FH)

This is the matching theorem applied WITHOUT virtual k edges. Given the
source policy/license and merged working trace, it constructs b on ALL R,
hence E_r2 by EASY_HARD_DECOMPOSITION.md. QH can hold while FH fails.
Virtual stays may justify retaining a paid physical owner, but are not
rotation-derived independent comparison receipts.

## What this DOES NOT prove

No union of incompatible source comparisons is declared to be L. A relation
defined by 'a seed occurs in some acceptable plan' need not satisfy F.
Likewise QH/FH does not prove source truth of its own inequalities or give
a Bank25 schedule. For a coupled policy, Q1 is exact planwise, while the
complete feasibility system remains the original source-license/selection/
schedule system. This is a proved quotient, not an all-route flow claim.

New mathematical status: Q1–Q3 proved at these stated quantifiers. The
new independent implementation check verifies the quotient of accepted
physical ledgers, without rerunning BSTs or asserting all-source eligibility.
