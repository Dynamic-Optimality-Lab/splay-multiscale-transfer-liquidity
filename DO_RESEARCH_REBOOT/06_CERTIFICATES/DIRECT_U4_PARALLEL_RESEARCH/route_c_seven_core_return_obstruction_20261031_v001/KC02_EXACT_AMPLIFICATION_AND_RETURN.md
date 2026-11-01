# An exact below-threshold amplification-and-return identity

Status: PROVED—RESTRICTED DOMAIN by composition of the complete independently verified source table; the literal thirteen-key composition is FINITE-EXACT. This is a closed control with two genuine one-StepEv resets, but it does not meet the requested G/J/excess thresholds or the historical nowhere-diagonal condition.

Starting diagonally at R13, the exact literal word is

    D3,D5,K7,
    K6,K5,K3,K7,K1,K4,
    K2,K6,K4,K1,K3,K2,K5,K4,K2,K1.

It has19 source actions, of which exactly two are DELETE. Every source action has a positive-cost A leader, adjacent source keys differ including the cyclic seam, and each DELETE costs exactly one RR event. Both DELETE blocks are pure KEEP-less blocks. The complete pair returns exactly to(R13,R13).

## Amplification from one to two

The first three actions have the already derived costs:

    D3: a_A=1, q_B=0;
    D5: a_A=1, q_B=0;
    K7: a_A=1, q_B=3, positive excess1.

The selected shared-KEEP extension has these actual source costs:

| KEEP | a_A | q_B | q_B-2a_A |
| ---: | ---: | ---: | ---: |
| 6 | 1 | 1 | -1 |
| 5 | 1 | 1 | -1 |
| 3 | 1 | 1 | -1 |
| 7 | 2 | 1 | -3 |
| 1 | 2 | 1 | -3 |
| 4 | 1 | 3 | 1 |

This creates a second genuine positive block without another DELETE. It is a shortest extension yielding ANY further positive block from the seed, as verified by all reachable predecessor distances. It is not a maximum-excess calculation.

Immediately before the final K4, the source trees are

    A=1(.,4(2(.,3),7(6(5,.),F))),
    B=1(.,7(2(.,3(.,6(5(4,.),.))),F)),

with F=R_[8,13]. The target4 has A depth2 and B depth6. Its outputs are

    A=4(1(.,2(.,3)),7(6(5,.),F)),
    B=4(1(.,3(2,.)),7(5(.,6),F)).

Those are distinct and do not return to the input. They split the remaining structural differences between the1..3 and5..7 subtrees.

## Explicit shared return

The single predetermined return word is

    U=(2,6,4,1,3,2,5,4,2,1), all KEEP.

Composing the same verified table transitions shows that its first three queries2,6,4 synchronize the pair at

    4(2(1,3),6(5,7(.,F))).

The remaining1,3,2,5,4,2,1 return that common tree to the right chain1,...,7 with the original F at7.right, hence to R13 for the fixed fringe. No new reset or setup state is inserted. The source word and its KEEP projection contain no full consecutive ascending/descending seven-key core pass, including cyclic seams. In particular no larger twelve/thirteen-key scan tail is present.

The literal composition has19 distinct source pairs before its closing endpoint. It is a simple directed paired-state cycle. It contains diagonal states: the initial pair and the common-state suffix after synchronization. Therefore it is not a nowhere-diagonal witness.

## Actual cycle budgets and why this is below target

The exact totals are

    A=24, Q_B=21, Z_B=8,
    E=2, C_D=4, G_B=2, J_B=0.

Only source occurrences2(K7) and8(K4) are positive, with excess one each. Both q_B=3 accesses are immediately followed by a q_B=1 KEEP. Their high/low helper pairs each contribute max(3+1-4,0)=0 to J_B. Thus the return completes the pair identity but supplies no surviving adjacent-helper budget. Existing DELETE-budget and helper theorems already give old-UD membership; no strict FI-only coverage is claimed.

The four source units from the two DELETE occurrences are counted once each as capacity; no prefix, alternate path or later repetition is pooled. E counts actual positive blocks with their actual leader costs, rather than raw G_B alone. Repeating this whole closed word m times would produce2m resets, E=2m,C_D=4m,G_B=2m,J_B=0. It cannot meet the exact-two-reset or E>C_D requirement by period padding.

The requested identity would need E>4 and G_B,J_B>=5 with only two physical resets. This control satisfies none of those inequalities. It is banked as a source-exact weak amplification-and-return identity, not promoted to the desired result. No assertion is made that two is the maximum possible amplification on the complete graph.

## Verification attribute and all-size fringe scope

The full prefix and selected amplification extension were directly replayed in the independent pointer source and reflection. The return composition uses the already independently checked complete429-tree/3,003-transition source table; each required core context is an existing verified row. verify_literal_return.py composes this one explicit formula, checks exact pair equality, all costs/units, source simplicity, diagonal flags and the cyclic scan test. It imports neither source engine and makes zero additional engine calls. No new word class or search is introduced after the graph audit.

The independent audit's earlier field “actual_cycle_or_return: NOT ESTABLISHED” is its immutable pre-composition snapshot. The later literal_return_certificate.json establishes this BELOW-THRESHOLD control only. The high-threshold requested identity remains OPEN in the final ledger.

Every target is <=7, so the entire19-action identity commutes with substituting any finite fringe F>7, including empty. The same costs, budgets and pair return therefore hold for arbitrary total size. Reflect the source trees and queries for the lower-fringe orientation. This is algebraic source substitution, not a larger finite fit or unbounded genuine-KEEP-support claim.
