# A reachable old child successor gives strict restricted coverage

The fixed witness satisfies SC01 and lies outside the named banked immediate/delayed former-root and packet classes. A direct analytic extension has arbitrarily many genuine KEEP keys. No larger finite instance or graph was fitted.

## Fixed diagonal prefix and exact cycle

Start diagonally at R7 and execute D7,D6. B stays R7; A becomes

    6(4(2(1,3),5),7),

with omitted leaf children empty. From this pair execute the predeclared cycle

    K7 K2 K3 K4 K5 K6 K7
    K1 K2 K3 K4 K5 K6 K7
    K6 K5 K4 K3 K2 K1 D7 D6.

Both full trees close exactly. Independent pointer replay gives

    A=31, Q_B=11, Z_B=16, 2A-Q_B=51.

All 22 accesses are A-root block leaders in this witness. Its sole positive block is the first KEEP7, with (a,q,delta)=(1,3,1). Immediately before its B splay the B root is 1 and its right child is 2. The successor KEEP2 therefore qualifies at pre-splay depth 1; its post-splay B depth is 1 as well. Its source values are (a,q,delta)=(2,0,-4). The pair sum is -3, against the required nonpositive bound.

The exact first-two-KEEP trees explain synchronization. After KEEP7,

    A=7(6(4(2(1,3),5),empty),empty),
    B=7(2(1,4(3,6(5,empty))),empty).

KEEP2 splays A by an LL double followed by a left zig and B by one left zig. Both become

    2(1,7(4(3,6(5,empty)),empty)).

Subsequent common KEEPs stay diagonal and are termwise nonpositive: with d_A=d_B=d, q=floor(d/2)<=2ceil(d/2)=2a. The full ascending/descending passes restore R7, and final D7,D6 restore the cycle's initial A while B remains R7.

The explicit credit certificate assigns all 11 B doubles to distinct units among the 62 A-credit units. The first positive uses its two local units and one unit from the successor's four-unit pool. No pool or unit is duplicated. All 22 cyclic cuts, and all cuts of the reflected witness, preserve the class conditions and the same physical assignment after reindexing. Reflection gives the old-left-child version with former root 7 and successor 6.

## Named old-domain exclusions

The positive's former B root is 1, while its first three successor keys are 2,3,4. The first return to 1 is at offset 7.

| Named banked class | Necessary condition that fails |
| --- | --- |
| 26AJ | Immediate successor is former root 1 |
| 26AK / 26AL | Second successor is former root 1 |
| 26AM | Third successor is former root 1 |
| 26AN / 26AO | A packet needs two distinct positive blocks; this cycle has one |
| 26AP direct packet | The sole unit-positive run has length 1, but its next key is 2 rather than former root 1 |
| 26AQ / 26AR / 26AS components | Their bridge/split/shared components require additional positive blocks or groups; the direct AP alternative also fails |
| KEEP-support <=3/4/5 classes | All seven keys are genuine KEEP targets |

These are checked necessary-condition exclusions from the pinned theorem definitions. The old recognizer programs were not executed or modified. The source transport bound is a known consequence of 26AL; novelty is the admitted charging class and source-return geometry, not a new claim about one-splay displacement.

## Arbitrary rigid fringes

Graft any finite BST H with keys greater than 7 as the right child of 7 in both initial R7 trees. Every request in the fixed prefix and cycle is at most 7. H is never entered by a search and remains attached to 7. Each source rotation commutes with the graft: when 7 is an operand its right fringe is untouched, and all other operands are below or outside that attachment. Hence every requested depth, event, pair condition and credit count is unchanged, and full closure includes the identical H. This proves arbitrary fringe size and shape for this family without any finite size sweep.

## A family with genuinely unbounded KEEP support

For every n>=7 start diagonally at R_n, retain prefix D7,D6, and use

    K7 K2 K3 ... Kn
    K1 K2 ... Kn
    K(n-1) ... K1 D7 D6.                          (F_n)

This is 3n+1 cycle accesses after the two-access prefix. Before and through KEEP2, the extra right vine 8,...,n is the untouched fringe just described. Thus the same source calculation gives the sole positive KEEP7 and the qualifying KEEP2 with delta=-4; the trees synchronize after that second cycle access. All remaining KEEPs are on identical trees and cannot be positive. Final DELETEs also cannot be positive.

For completeness, a full ascending pass always yields L_n. After accessing k, the keys 1,...,k form the entire left spine under root k. The next target k+1 is the minimum of the right subtree. The source's internal LL operations retain its empty left fringe; the final right zig or RL double attaches the old prefix as its left spine. Inducting on k gives L_n at k=n. Reflection gives R_n from a descending pass. Therefore the ascending and descending blocks in (F_n) restore R_n; final D7,D6 restore its initial A exactly.

Every key 1,...,n is a KEEP target. The only positive still has successor 2 rather than former root 1; the first former-root return now occurs at offset n>3. The named old-class exclusions remain true for every n>=7. Taking n beyond any fixed finite corpus also prevents a claim that this is only another checked small-tree walk. This conclusion is analytic; only n=7 and reflection were replayed numerically.

The restricted theorem itself does not require this witness shape, synchronization, one positive, unit deficit, or these scan connectors. It applies to every reachable closed walk meeting S1-S2, including arbitrary support and any number of disjoint positive/successor pairs. The witness family establishes nonvacuity and strict named coverage; it is not the proof of the universal restricted theorem.
