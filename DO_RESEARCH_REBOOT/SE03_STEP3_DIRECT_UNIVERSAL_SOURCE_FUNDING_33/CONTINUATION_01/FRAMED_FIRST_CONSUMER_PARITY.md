# Exact first-consumer parity for the outside frame

Mathematical derivation complete. Independent free-term base check pending
at creation. This is an A-source comparison theorem, not a new donor,
eligibility, Bank25 or Gate U theorem. No fresh source search is used.

## IAGS Box

Target: determine exactly when a common later target in X rejoins the
two actual outside-frame trees, without a forced-depth assumption.
Conditions: ordinary bottom-up splay; ordered disjoint BST terms

    T0=R(G(A,p(J,X)),E),  T1=R(p(G(A,J),X),E),
    A<G<J<p<X<R<E.

Inequalities on terms mean every key of the term has the indicated
order. Terms may be empty except X contains the target y. All named
nodes are distinct. J may be an arbitrary BST, not just the earlier j.
The inequalities do not assert ancestor or chronological order.

Inheritance: original StepEv is ceil(edge-depth/2). The outside-frame
source construction and its independent receipt are in
FRAMED_RETURN_SOURCE_BRIDGE.md and
framed_return_and_core13_independent_audit.json. The local rejoin issue
also occurs in C23 A_FLIP_SOURCE_VALIDITY.md, whose manuscript controls
do not supply a new normalized owner receipt here.

Ambiguities: which dirty histories admit a useful comparison of these
two trees, their actual B/chart coupling, and the physical ownership
effect of the comparison remain unresolved.

Bridge: for an actual source instance satisfying these tree equations,
the following ordinary-splay identities apply to its genuine next
occurrence of y, retaining its original operation kind and all costs.

## Statement

Let d be y's edge-depth inside X before the common access. Write a0,a1
for the numbers of actual StepEv events in the two executions. Then

    a0=ceil((d+3)/2), a1=ceil((d+2)/2).

The final complete trees agree if and only if d is even. In that case
a0=a1+1. When d is odd their costs agree and their precise remaining
discrepancy is one of the two forms below. Reflection gives the entire
opposite orientation. The statement is uniform in arbitrary finite X,
all other BST payloads and the target's depth.

## Proof: common phase and exhaustive terminal forms

While y has depth at least two within X, its next bottom-up double uses
only nodes of X. Its path and rotations are identical in T0 and T1;
they replace the same X by the same new term and do not touch G,p,R.
After floor(d/2) such doubles the depth inside X is d mod 2. This is
an induction along the actual splay, not an enumeration of bounded trees.
It proves that the following three terminal forms are exhaustive.

If d=2k, the new X is y(L,U). The remaining two-event splay in T0
uses RR on G,p,y then a final zig at R. The one-event splay in T1
uses LR on R,p,y. Both yield

    y(p(G(A,J),L),R(U,E)).

Their total costs are k+2 and k+1. Each named payload occurs once in
the same final slot, so the equality includes the entire physical tree.

If d=2k+1, the new X has y as a child of its root z.

1. X=z(y(L,U),V). Both executions first use RL on p,z,y. T0 then
   uses LR on R,G,y, whereas T1 finishes with a zig at R. Their results:

       S_y(T0)=y(G(A,p(J,L)),R(z(U,V),E)),
       S_y(T1)=y(p(G(A,J),L),R(z(U,V),E)).

2. X=z(V,y(L,U)). Both executions first use RR on p,z,y, and the
   same respective LR/final-zig endings yield

       S_y(T0)=y(G(A,z(p(J,V),L)),R(U,E)),
       S_y(T1)=y(z(p(G(A,J),V),L),R(U,E)).

Both odd cases cost k+2 events in each execution. In case1 the left
roots of the final y are G and p; in case2 they are G and z. The named
keys are distinct, so the complete trees do not agree. This proves the
only-if direction as well, including arbitrary choices of the payloads.

Reflection reverses every key order, exchanges left and right, and
conjugates each ordinary splay. It preserves depth and event counts,
therefore proving the reflected statement without a new source premise.

## Consequences and exact limits

The earlier root-of-X lead is the d=0 case. There is a uniform extension
to every even-depth target; a general all-target rejoin assertion is
false already at either odd terminal form. This is an exact local
identity/inequality, not by itself a paired-closed countercertificate.

The difference a0-a1 is not a new free original bit. T0 and T1 are
different executions, and an auxiliary owner may already use every
original bit at the indicated occurrence. No B-double demand, auxiliary
demand, signed chart correction or original operation has been removed.
No future y access is asserted to occur, and no lower bound on future
target depth is assumed. A repeated/shared physical donor theorem
requires the still-open source/owner bridge.

This lemma does not change any accepted result or resource cap. Principal
C33, unconditional Gate U and Universal Coarse-Double remain OPEN.

## Dependency provenance

FRAMED_RETURN_SOURCE_BRIDGE.md SHA256:
1891b0a4405dcdce2bdbad54020b2faa051928ff53d1b5207fe64997d0b5920e.

C23/A_FLIP_SOURCE_VALIDITY.md SHA256:
7dc1023ef0c8bdada413e8ce0bbc1f4c4c5b30a2fca7c4d0d1fe63dbc0186c80.

Resource baseline is resources_checkpoint_960_01.json SHA256:
0122232ed4a53603ce02556faaa23b1b03e962a0c371f1f73c0f4807186f7efa.

No independent check is implied by this manuscript alone. Its possible
later check must be charged to the existing independent budget, not to
a renewed symbolic budget that has not been authorized.
