# Safe saturation of an opaque two-core prefix

Status: analytic universal theorem on the explicitly restricted source
class Q below; independent symbolic audit is recorded separately. This is
not a universal M3 certificate. No finite tests are used.

## Public predicate and explicit construction

Retain original full ordinary states s=(mu,b,alpha7,sigma). Assume b has a
valid ordered core projection with root r. Q(s) means:

* alpha's root is Score r (root's UNUSED kind remains arbitrary);
* at exactly one of L/R the kind is0 and the label is a marked Score
  x!=r;
* all OTHER nonroot alpha positions have nonzero kind, that is port or
  empty in the frozen typed domain. Their unused isS/index values are
  irrelevant and may be arbitrary independently at the two endpoints.

Thus V(s)={x}. On a genuine source this is exactly an actual core root r
and one actual marked core child x, with three port/empty side blocks.
No assumption is made about the Scores/counts hidden in those ports.
An invalid kind0 reference would report literal slot0's root label r,
so cannot fabricate this child x. Propagated port/empty grandchildren
have nonzero kinds and cannot fabricate additional targets.

Reuse psi,c,U,Lambda and their exact totalizations from M3_E1_01. Write

    w_x=2-floor(depth_coreB(x)/2),
    h(s)=min(2,w_x+2) if Q(s), and h(s)=0 otherwise,
    D_Q(s)=max(Lambda(s),h(s)).

These are public current-state functions. They do not read private
inventories, enlarge the frozen tuple, select a completion, or use history.
Core depth<=8 gives w_x>=-2 and hence0<=h<=2. Since V={x}, h=U on Q;
the completed bound Lambda<=U gives D_Q=h on Q. Globally psi<=D_Q<=2
on valid projections, with the existing invalid-state totalization.

## Destination credit lemma

Take ANY original H1 edge s->t with source Q. The original H1 normal form
and its SAME full endpoints give a core access to x. Since its actual A
position is a child, the A rewrite is a single zig. For a left child,

    r(x(A,B),C) -> x(A,r(B,C)).                         (1)

A,B,C are arbitrary opaque/empty cuts, not completed private trees chosen
by the potential. The right-child identity is the left/right dual. No
node inside a port is an active operand. Actual terminal q, original H
and weight are unchanged, including charged DELETE/zero terminal KEEP.

The destination's only possible marked nonroot visible core is r. All
three side cuts stay nonreal. If mu marks r, t again belongs to Q, now
with root x and marked child r. If r is unmarked, V(t) is empty.

In B, after splaying a nonroot core x, the old root r ends at depth1 or2.
This follows from the last access step after arbitrary lower pairs:
a final zig places r at depth1; a final same-direction pair places it
at depth2; a final opposite-direction pair places it at depth1. All
interior side terms are arbitrary, so the fact covers every original B
core path. The reverse weight is2 at depth1 and1 at depth2.

Therefore, for ANY public Lambda<=D<=2 and F=max(D,h):

* if r is marked, h(t)=min(2,w_reverse+2)=2, so F(t)=2;
* if r is unmarked, V(t) empty gives c(t)=Lambda(t)=2, so F(t)=2.

The first branch uses SIMULTANEOUS saturation, not the false inference
that reverse weight is always2 or that c(t) is necessarily2. This is
the correction recorded in PRE_EXECUTION_v2.md. No unproved recursive
closure is involved: Q and h are explicit depth-two formulas.

## Augmentation theorem

For every public function Lambda<=D<=2, F=max(D,h) preserves EACH original
H1 inequality that D previously satisfied, individually. If its source
is unchanged, its residual only increases by F(t)-D(t)>=0. If the source
is raised, it lies in Q and F(s)=h(s). The lemma gives F(t)=2, so

    w_x+F(t)-F(s)=w_x+2-min(2,w_x+2)>=0.              (2)

For w_x>=0 the expression is w_x; for -2<=w_x<0 it is0. The proof
holds simultaneously at both endpoints and for all compatible witnesses
and signatures. The range/floor are preserved. It is stronger than
preservation for a globally feasible D: no global feasibility is assumed.

For the explicit seed D_Q, every H1 edge with source Q is valid even if
Lambda has invalid inequalities elsewhere. Indeed D_Q(s)=h(s) and
D_Q(t)=2 give(2) directly. The same augmentation theorem preserves all
other H1 inequalities already proved for Lambda. Thus no new negative
edge failure or new debt-transfer type is introduced by this operation.

## Weight0/+1 transfers outside E1

On Q the only visible target has B depth d. The following exact cases
are depth/charge deductions, not numerical experiments:

* d=4/5: outside E1, D_Q(s)=2 and its outgoing H1 edge has w=0 and
  D_Q(t)=2. Its residual is0. ALL incoming H1 edges of weight0 or+1
  are safe as well, because their source debt is at most2.
* d=6/7: outside E1, D_Q(s)=1 and the outgoing H1 edge has w=-1 and
  D_Q(t)=2. Its residual is0. ALL incoming+1 edges are safe; an incoming
  weight0 edge is safe whenever its source debt is at most1.
* d=8: outside E1, D_Q(s)=0 and its outgoing w=-2 edge ends at debt2.
  Its residual is0. No general incoming0/+1 claim is made here.

After the first H1 access in a run whose sources remain Q, the marked
pair is exchanged and the next B target is at depth1/2. Every later
H1 edge therefore has weight at least1. If the old root is unmarked,
the successor has no H1 target and such a run ends instead. No hidden
private history is assumed: each subsequent witness sees the same full
shared Q state, so exactly the same two marked labels must be used.
This handles arbitrarily repeated signed transfers WITHIN this class,
not only a fixed two-edge pattern.

Every D_Q failure remaining in the H1 system must have source outside Q,
be a previous Lambda failure, and belong to the old possible classes:
weight0 with psi(source)1/2 or weight1 with psi(source)2, always
c(source)<psi(source). Protected destination cases above are additionally
excluded. This is a proved restriction, not evidence that failures exist.

## Original LOW and signed-walk corollary

The AER01 source connectivity proof makes a Q source an actual proper
prefix after erasing invalid refs. Here every observed real child is
the distinct core x, and all other cut kinds are nonreal, so there is
no remaining invalid real pair at an active position. There can be no
other present real node: its real ancestor path would have to cross
one of those nonreal cuts. Exactly two real nodes are present, both
Scores. Wit.p/isS are immutable through the original A replay.

Consequently a normalized H2/Gamma1 edge cannot have a Q source: its
required actual anonymous helper is not present. This excludes BOTH
Score-bearing and Score-empty helpers LOCALLY by source semantics; it
does not prove augmentation safe for their non-Q sources. Original H2
Gamma0 retains its completed actual-preterminal-debt proof, since D_Q
has range[0,2] and the psi floor. Genuine H0/Gamma>1 exclusions and
H1/H2 coverage are the established source normal forms, reused unchanged.
It follows that EVERY original LOW edge whose source lies in Q obeys

    w+D_Q(t)-D_Q(s)>=0.

Use the already proved HIGH law and corrected h0 with

    W(O)=-D_Q(O)-5*chi8(O.b),       W(M)=-5*chi8(M.b).

HIGH inequalities require only the range and the unchanged absorbing
chi8/high-entry law; they hold globally for this W. LOW conserves chi8.
Therefore every finite original walk whose LOW sources all satisfy Q
has weight>=W(end)-W(start)>=-7. Every fully closed such walk has
nonnegative weight. Within a single chi8 region the bound is-2.
This is a PROVED--RESTRICTED DOMAIN signed theorem, not full M3.

Full closure uses all147 ordinary and127 midpoint coordinates. OM/MO
witnesses remain independent and share the SAME actual midpoint; free
high v, original q/weights and h0(actual0,declared18,q9,w=-3) are intact.
No low-source restriction is imposed on the original graph: Q merely
names the subclass this theorem discharges. Other cycles remain there.

## Strictness, dependency reuse, and boundary of progress

This saturation can strictly increase the prior public seed outside E1.
Reuse the ALREADY PROVED B facts in LDR01/full_run_controls.json,
helper_reset_2: r=8,x=0,w=0,psi(source)=psi(destination)=0. Do not rerun
its source/root evaluation or replay any B operation. Choose the ordered
source A prefix8(0(A,B),C), with all seven intermediate Scores hidden in
the port B, A and C empty or compatible opaque cuts. The standard source
port realization supplies a legal sigma0 completion; unused fields stay
free. Its V={0}, so c=Lambda=0, while h=D_Q=2. This is an analytic use
of a pinned completed B result, not a new evaluated finite case. Compatible
anonymous populations can remain opaque; the universal theorem itself
requires no new population realization or finite basis.

The existing original zero-reset control (psi2->0,w0) likewise can use
such a two-core prefix at its named root/target. This proof covers that
whole structural family without asserting what the old Lambda destination
label was. No claim is made that the old completed sector tables required
this particular normalization or that the new seed is globally valid.

Reused dependencies: original H1 normal form, AER01 real paths and source
connectivity, the original static port/inventory law, completed psi and
c/U/Lambda proof, Gamma0/range repayment and the universal HIGH glue.
No circular appeal to M3 or unproved arbitrary-signature feasibility occurs.

BEFORE: weight0/+1 possible failures of Lambda were not structurally
resolved on Q. RESULT: an explicit safe simultaneous saturation and a
source-complete restricted LOW/walk theorem for arbitrary signatures.
AFTER: delete Q-source LOW checks and the listed protected incoming0/+1
checks. General exposing prefixes and non-Q coupled transfers remain
OPEN; no full public debt/M3 proof and no negative cycle are claimed.
No signature certificate count changes and no finite tests are run.
