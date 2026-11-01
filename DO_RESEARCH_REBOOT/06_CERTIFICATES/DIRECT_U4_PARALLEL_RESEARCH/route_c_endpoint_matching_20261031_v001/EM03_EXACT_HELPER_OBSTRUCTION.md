# The first six key helper refutes endpoint matching

The nonlinear endpoint repair pays full q on opposite vines and obeys DELETE universally, but it fails the required arbitrary-fringe helper law already at the permitted empty fringe. This is a whole source KEEP with zero budget, not an extra micro-step requirement.

## Full physical source operation

Use the L branch of the established six-core family, with no additional fringe keys. Omitted children and bare key children are empty and leaves respectively. The initial trees are

    A0=6(2(1,3(empty,4(empty,5))),empty),
    B0=6(5(4(1(empty,2(empty,3)),empty),empty),empty).

KEEP 2 gives

    A1=2(1,6(3(empty,4(empty,5)),empty)),
    B1=2(1,5(4(3,empty),6)).

The source A access has depth one and performs one left-oriented zig. B has depth four and performs LR then LL, so

    a=1, q=2, z=0, required upper bound 2a-q=0.

The actual grouped events are A: ZIG on keys 2,6 with orientation L; B: LR on 1,2,4 followed by LL on 2,5,6. Both the pointer and frame engines agree on every event and complete tree endpoint.

## Exact proper subtree vertices

Intervals denote exact key sets on these consecutive keys. They do not encode subtree shape.

| Tree | Proper subtree key intervals |
| --- | --- |
| A0 | [1,1], [1,5], [3,5], [4,5], [5,5] |
| B0 | [1,3], [1,4], [1,5], [2,3], [3,3] |
| A1 | [1,1], [3,5], [3,6], [4,5], [5,5] |
| B1 | [1,1], [3,3], [3,4], [3,6], [6,6] |

## A matching and equal size cover at the source

The following four disjoint graph edges form a matching in the A0,B0 endpoint graph:

    A[1,1] -- B[1,3],
    A[1,5] -- B[1,4],
    A[3,5] -- B[3,3],
    A[4,5] -- B[1,5].

The left vertices A[1,1], A[1,5], A[3,5], together with right vertex B[1,5], cover EVERY graph edge. This cover has size four. A matching cannot be larger than any vertex cover, so nu(A0,B0)=4 and

    E(A0,B0)=5-4=1.

## A matching and equal size cover at the destination

Three disjoint edges are

    A[1,1] -- B[1,1],
    A[3,5] -- B[3,3],
    A[3,6] -- B[6,6].

The only non-isolated left vertices are A[1,1], A[3,5] and A[3,6]. They cover all edges, so nu(A1,B1)=3 and

    E(A1,B1)=5-3=2,
    Delta_KEEP E=+1>0=2a-q.

These hand-readable matching/cover certificates are independently verified in addition to the algorithm-generated certificates. The arithmetic proves the violation without trusting an optimizer's assertion.

## Why the correction loses helper safety

After A alone moves, E(A1,B0)=2; during the B phase E remains two. The matching ranks along the whole source operation are 4 -> 3 -> 3. Thus the B phase creates no net matching augmentation to compensate for A motion, despite creating exact agreements.

The old F values are 4 -> 5 -> 3, so F's whole change is -1 and its B-phase drop is two. For H=E-F,

    H_source=-3, H_destination=-1, Delta H=+2.

The helper allowed H to increase by at most one, because Delta F=-1 and the whole budget is zero. The endpoint repair exceeds that allowance by one. E<=F at every state did not preserve F's transition inequality.

The arbitrary-fringe contract explicitly includes m=0. This in-domain empty-fringe witness therefore refutes preservation of the entire stated family. It does not claim that every nonempty fringe also fails. No larger fringe controls, alternative matching cost or hook-vine test were run after this first obstruction.
