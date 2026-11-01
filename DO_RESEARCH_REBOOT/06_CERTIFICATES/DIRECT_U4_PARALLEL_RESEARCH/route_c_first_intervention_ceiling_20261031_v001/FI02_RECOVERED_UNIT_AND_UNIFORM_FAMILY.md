# Recovering one reserved unit before either DELETE

Status: FINITE-EXACT for the unchanged 13-key source word and reflection; PROVED analytically for its fringe and unbounded-support extensions. The strict comparison concerns a directed three-block repayment span. Its containing closed cycle was already UD-covered and is not counted as a new CD cycle case.

Use the existing UD diagonal R13, prefix D13,D12 and unchanged cycle:

    K13 K11 K12 K2 D3 D2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K1 K2 K3 K4 K5 K6 K7 K8 K9 K10 K11 K12 K13
    K12 K11 K10 K9 K8 K7 K6 K5 K4 K3 K2 K1 D13 D12.

No new source word or key size was evaluated. Totals remain A=68,Q_B=35,Z_B=30,weight=101. The actual paired cycle, all diagonal prefixes and all source events/states agree with UD's certificate. Reflection x->14-x has the same costs and mirrored states.

## The three-block source packet

| Occurrence | Request | A depth / grouped a | B depth / doubles q | delta |
| --- | --- | --- | --- | ---: |
| 0 | K13 | 1 / 1 | 12 / 6 | 4 |
| 1 | K11 | 5 / 3 | 7 / 3 | -3 |
| 2 | K12 | 2 / 1 | 2 / 1 | -1 |

The anchor pays two of its six doubles locally and leaves four residual demands. KEEP11 has six actual units, reserves three for its three own doubles and lends three. The final residual is unpaid under UD after KEEP12, because UD's ceiling four exhausts that payer's two-unit reservation.

Immediately after K13, B is

    13(2(1,4(3,6(5,8(7,10(9,12(11,.)))))),.).

Tracked key 12 has depth h=6. The first intervening B splay is K11 on path

    13,2,4,6,8,10,12,11,

with source cases RL,RR,RR,ZIG. At entry, key 12 is the first double's parent and has first shift zero. It lies to the right of accessed key 11. Each of the two later RR doubles lowers that target-right fringe by two. The final left zig raises neither target fringe. Thus

    mu=0, r=2, m=2,
    U=6+0-2-2=2,
    c_FI=floor(2/2)=1,
    c_UD=floor(6/2)+1=4.

The actual source destination after K11 is

    11(4(2(1,3),8(6(5,7),10(9,.))),13(12,.)).

Its tracked depth two corroborates the bound; the bound was computed from the pre-tree and source frames, not this lookup. KEEP12's actual q=1 fits the new reservation one. Its second unit is released to the anchor.

## Exact physical-unit ownership

| Pool | Own B work | Loan to anchor 0 |
| --- | --- | --- |
| K13, occurrence 0, capacity 2 | two local demands | none |
| K11, occurrence 1, capacity 6 | unit prefix [0,3) | suffix [3,6), residuals [0,3) |
| K12, occurrence 2, capacity 2 | unit prefix [0,1) | suffix [1,2), residual [3,4) |

The recovered loan is actual unit (2,0,1). KEEP12's own demand uses (2,0,0). Earlier loan credits are (1,1,1),(1,2,0),(1,2,1). All identities differ. The anchor's residual cursor moves 0->3->4. Every B demand of occurrences 0,1,2 has one distinct unit from those same occurrences, and every one of their ten A units is used. Therefore

    Q_B(span)=10=2A(span),  A(span)=5.

No DELETE pool, prefix unit, second lap or external endpoint credit pays the span. Compared with UD, the recovered capacity is one A unit, although the ceiling improves by three. This distinction matters because reservation is min(capacity,ceiling).

KEEP2 remains conservative: its ceiling and reservation are two despite actual q=1. After the first-intervention refinement, its remaining intervening B change is still bounded coarsely. The procedure does not simply read exact own surplus.

## Cut comparison and the exact scope of strictness

On each orientation, UD accepted 40 of 44 cycle cuts. FI accepts 42: cuts {0,3,4,...,43}. The two failures, cuts 1 and 2, retain explicit unpaid debt. All old cuts and all old per-cut transfer records under UD are unchanged. The new successes are alternative single-period proofs, not budgets to combine.

The strict new local fact is that the ordered span [0,1,2] clears its four-unit excess internally. The old directed-span procedure leaves one unit after the same endpoint. More successful cuts of an already accepted cycle do not establish a strict enlargement of the set of accepted closed walks. No such class-strictness claim is made.

## Uniformity without larger finite fits

Graft an arbitrary unrequested BST F with keys >13 at key 13's right child in the diagonal R13. The fixed word never descends into F; rotations carry it as an unchanged off-path fringe. The tracked depths, consumed source frames, entry-parent identity and two later matching doubles are unchanged. The same reservation 2->1, recovered unit and three-block equality hold for arbitrary fringe size and shape.

For every n>=13 the existing UD full-support family is

    prefix D13,D12 on R_n;
    K13 K11 K12 K2 D3 D2 K3 ... Kn;
    K1 ... Kn;
    K(n-1) ... K1; D13 D12.

The first three requests and their source frames commute with the right fringe R_[14,n], so the earlier-repayment improvement is identical for every n. Increasing accesses through 13 synchronize A and B with that right fringe; continuing through n produces L_n. The common scans produce L_n then R_n, and final D13,D12 restore A's prefix state while B stays R_n. Every key 1,...,n is KEPT. This is the already-established source family with a stronger local repayment certificate, not a newly discovered closed-cycle family. No additional finite n was evaluated.

FI01 proves the general source estimate independently of this family. The fixed-corpus matrix of 4,708 actual B-access/tracked-key rows corroborates all four double orientations, final-zig entry and every non-noop entry role. Of those bounds, 1,958 remain loose and 3,808 improve the uniform +2 estimate. Root no-ops are not present among these actual B accesses; their identity case is proved analytically. These counts are not a finite proof or a parameter fit.
