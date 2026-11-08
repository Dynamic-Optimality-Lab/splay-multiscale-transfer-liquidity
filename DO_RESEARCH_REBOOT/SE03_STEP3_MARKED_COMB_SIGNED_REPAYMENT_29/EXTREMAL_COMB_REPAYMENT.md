# MC29-X — source-forced repayment for extremal marked combs

Status: complete symbolic comparison-level theorem for the proper
extremal source subclass below. Physical extension hypotheses are stated
separately; this is not principal MC29 closure on all comb/owner classes.

## Statement

Use the original seven-mark/core13/all-SS source and actual H1/Q3/beta3/z1
comb e. Let x be its accessed marked leaf and R=g3 its old marked root.
Assume x and R are opposite extreme KEEP keys. They need not be extreme
PHYSICAL keys; arbitrary private nodes may lie outside their interval.
Let p be the genuine predecessor and j the pre-predecessor.

With the intrinsic correction J_B=3-b(T), where b counts marked branch
vertices, the total potential D_leaf+J_B differs from E=L-b-1 only by3.
Thus every signed identity below is an identity for ORIGINAL rho plus
the ACTUAL state correction Delta J_B. No original weight is redefined.

There is a source-defined packet ending at e with

    sum rho + Delta J_B = sum sigma_E >=0:

* U or B predecessor: choose(p,e), for EVERY Hp>=1.
* P predecessor with Hp>=2: choose(p,e).
* P predecessor with Hp1: choose(j,p,e). In this case source forces Hj>=2.

All such packets for an arbitrary finite collection of actual extremal
combs have disjoint full macro inventories. Reflection is covered. Every
helper cost is an actual source H, including any DELETE/root repeat.

## Single-event order barrier

Lemma. For four distinct marked keys x<Y,Z<R, no actual A execution
starting at root Z can perform accesses Y,R,x with exactly ONE bottom-up
StepEv at EACH access. Arbitrary ordered hanging BSTs and anonymous
middle parents are allowed.

If Z<Y, x is in the old root Z's LEFT subtree, off Y's search path.
After splaying Y, Z remains an ancestor of x, so depth_Y(x)>=2. During
the next access R>Y the old LEFT subtree of Y remains attached to Y.
After the one R event, Y has depth>=1, hence depth_R(x)>=3, contradiction.

If Y<Z, R is in the old Z RIGHT subtree, off Y's search path. Thus after
splaying Y, Z is still an ancestor of R. A one-event R access requires
depth_R_before<=2, forcing Z at depth1 and R its direct right child.
The second event is RR through Y,Z,R and leaves Y at depth2. Since
x<Y, its unchanged subtree below Y puts x at depth>=3, contradiction.

These off-path invariances follow from the explicit zig/SS/zigzag
rotation stencils and hold for opaque arbitrary subtrees. They do not
assume that no anonymous physical nodes exist. A unique positive event
earlier in a macro may be a DELETE of its terminal target; all other
operations then have zero A cost. Root synchronization therefore reduces
three H1 macros to precisely these three actual single-event accesses.

## Why the barrier applies to the weak P predecessor

MC29-P shows the marked tree BEFORE a P predecessor has root either
Y=g2, of degree3 with children(g1,l2,l3) where g1 has children(x,l1)
and l3 has child R, or Y=l3 of degree1 with child g2. In the latter form
g2 has children(g1,l2,R). The root Z before the incoming j access is
one of the OLD ancestors which become children of Y. Thus Z is NOT x
or R, and neither is Y. For extremal x,R both Y,Z are strictly between
them. Hj=Hp=He=1 would violate the lemma; hence Hj>=2. No future-depth
claim and no manufactured helper is used: this is a bound on an actual
PAST source macro.

## Exact helper balances

On a comb sigma_E0. For the three predecessor profiles of MC29-P, the
actual marked degrees give

    sigma_E(p)=2cp-1  (U),
                2cp-2  (B),
                2cp-3  (P).

The first two are nonnegative at Hp1; P is nonnegative at Hp>=2.
For weak P, sigma_E(p)=-1. If the marked root after j has degree1,
its one child has degree3: Qj1 and sigma_E(j)=2cj-2>=2 at Hj>=2.
If that root has degree3, its children have degrees2,1,0. Consequently
Qj<=3, its old target degree is3-Qj, and at most ONE old ancestor has
degree>=3. Therefore sigma_E(j)>=2cj-3>=1. The triple pays the weak
P deficit including ALL helper debt. This is not mere pointwise comb
normalization: the negatively affected helper is part of the same packet.

MC29-P's two-step separation makes the chosen packets disjoint. All
physical events in them retain one absolute owner and are counted once.
Shared marked keys/private ancestors do not duplicate source occurrences.

## Physical and frozen-owner bridge

These packets have a separate natural-compatible physical comparison.
The comb has just ONE native h0 deficit, its third double. For a Qp1
predecessor, give it p's first unused natural unit (ordinal Qp+1=2).
For P with Hp>=2 use p ordinal3. For weak P use j ordinal Qj+1<=4,
which exists since Hj>=2,Qj<=3. Keep every h0 value. Each chosen unit is
an ACTUAL original bit unused by h0, and source packets are disjoint.
No claim that such a bit is unowned under f6/effective a is made.

On a whole source where all OTHER native h0 deficits are already covered
by disjoint source comparers, these packet maps form the required raw
component. If all native deficits are these combs, their union with h0
is directly a FULL independent injection. For any frozen a, total-H paths
then preserve every old value and give free endpoints under the original
eligibility license. At partial coverage paths may end at OTHER frontiers;
that is relocation, not full funding. The storage bridge is the ACTUAL
cut profile B_extended<=B_H+2B_a, or a separately proved source schedule.
No universal old-owner profile bound is assumed.

The pure signed packet correction spends no additional physical bit and
changes no old a value. If it is composed into a COMPLETE signed source
certificate, all uncovered sigma_E macros must also be proved nonnegative
or repaid. E in[0,4], selected packet units<=10 and actual legal cuts give
a raw budget within Bank25; fixed old cuts/maps still require their exact
transport/profile receipt. The explicit mixed-comb family supplies the
complete owner and Bank5 bridge at its declared raw-canonical scope.

Nonextremal x,R, further high-arity helper debt outside these packets,
arbitrary old nested-normalized receipts and unrestricted global MC29
composition remain OPEN. No unconditional Gate U claim follows.
