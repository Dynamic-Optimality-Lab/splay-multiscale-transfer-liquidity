# FE02: the parity channel in an approaching transfer

Status: the arithmetic classification below is PROVED—UNIVERSAL. The
source realization and its discharge have the explicit structural scope
in AD02. FE02-CD remains OPEN. No potential or additional capacity is
defined by this diagnostic.

For an unaccessed tracked key y, in the actual pair source put

    G_y = d_B(y)-2d_A(y),
    z_A = d_A(y) mod2, z_B = d_B(y) mod2,
    E_y = floor(d_B(y)/2)-2ceil(d_A(y)/2).

Direct integer arithmetic gives 2E_y=G_y-z_B-2z_A. Unlike G, E includes
the two rounding effects in the physical demand/capacity comparison.
It describes the excess of accessing y NEXT; it is not a debt already
incurred by an unaccessed key.

## Complete nonincreasing-G exposure classification

Suppose E_before<=0<E_after, and Delta G<=0. Write

    Delta G = 2t+Delta z_B,       Delta E = t-Delta z_A.

The integer t exists because G has B's parity. Nonincreasing G implies
t<=floor(-Delta z_B/2); exposure implies t>=1+Delta z_A.
Since each Delta z lies in {-1,0,1}, these inequalities require

    Delta z_A=-1, t=0,
    (Delta G,Delta z_B)=(0,0) or(-1,-1).

Conversely those parity transitions increase E by exactly1. Consequently
every such exposure has E_before=0,E_after=1. When Delta z_B=0 its
unchanged parity may be0 or1; thus there are three parity configurations,
not an unbounded set requiring a depth cutoff. This is an exhaustive
integer argument, not a finite depth fit. It does not assert that each
configuration has an original-source realization.

This classification DOES NOT contradict PC02A's necessary positive gap
creation somewhere on the entire return interval. It shows that the last
exposing helper need not itself increase G. Earlier history can already
have accumulated the requisite G.

## Exact source realization of one channel

Use original parent-first ordinary splay. T=k(L,R) denotes a BST node,
and a bare k a leaf. Let

    U=4(3(2,.),6(5,.)), R=11(9(.,10),12),
    A0=13(1(.,8(7(U,.),R)),.),
    B0=13(1(.,11(3(2,8(4(.,5(.,6(.,7))),9(.,10))),12)),.).

The source path to8 in A is13,1,8. One LR produces

    A'=8(1(.,7(U,.)),13(R,.)).

In B the path is13,1,11,3,8. The inner LR has grandparent11,parent3;
the outer LR has grandparent13,parent1. They produce

    B'=8(1(.,3(2,4(.,5(.,6(.,7))))),13(R,.)).

Thus KEEP8 has (a,q)=(1,2), exactly saturated. Tracked7 has

|State|d_A(7)|d_B(7)|G_7|z_A|z_B|E_7|
|---|---:|---:|---:|---:|---:|---:|
|Before KEEP8|3|8|2|1|0|0|
|After KEEP8|2|6|2|0|0|1|

The A target-left interior containing7 moves up once. The two B cross
frames move its containing interior up twice. No unit is available from
this helper: its own two B doubles consume both actual A bits.

The subsequent source paths to7 are

    A':8,1,7       (one LR),
    B':8,1,3,4,5,6,7   (RR,RR,LR).

Consequently KEEP7 has (a,q)=(1,3), and both FULL destination trees are

    C=7(1(.,U),8(.,13(R,.))).

Equality of destinations, rather than equality of accessed roots, is the
new source consequence used for discharge. The first two KEEP7 doubles
use its two A bits; its third requires one later genuine unit.

The exact diagonal prefix D8,D7,D1,D13 takes (B0,B0) to(A0,B0), keeping
B unchanged throughout. This is ordinary source reachability, not an
assumed one-zig transition. Two overwritten prefixes D8,D7,D4,D1,D13
and D8,D7,D2,D1,D13 have the SAME tracked7 exposure3/8->2/6 and the
same costs KEEP8=(1,2), KEEP7=(1,3). Their post-positive source geometry
is analyzed in AD02; they need not synchronize immediately.

All14 inorder external gaps may be replaced by arbitrary COMMON ordered
subtrees. Every displayed core access avoids their interiors. Therefore
the original rotation identities treat them as untouched variables.
The integer labels stand for arbitrary increasing core keys: nonempty
intermediate gaps are allowed by order-preserving relabeling. This is
not a claim about unequal A/B gap subtrees.

Source identities are in source_discharge_certificate.json and
overlap_discharge_certificate.json. Both original engines independently
replayed the opaque-variable identities. Their checks certify these
identities; the proof of the universal parity statement is the integer
argument above, not the number of checks.
