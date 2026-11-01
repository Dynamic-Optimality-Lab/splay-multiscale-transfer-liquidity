# All A couplings of the fixed KEEP word are DELETE-budget covered

Status: PROVED—RESTRICTED DOMAIN. For every actual closed A/B source walk on keys 1,...,13 whose cyclic KEEP projection is a positive power of the displayed word W, arbitrary present-key A-only DELETE insertions satisfy E<=C_D. Reachability from a diagonal is unnecessary for the obstruction, so it applies in particular to every reachable coupling requested by the user. Universal CD on other KEEP words remains OPEN.

The fixed word is

    W=(13,11,9, 1,2,3,4,5,6,7,8,9,10,11,12, 11,10,9,8,7,6,5,4,3,2,1).

Its B recurrence and cost profile are the preceding BC certificate, rechecked here without alteration. DELETE leaves B unchanged. Each period has Q_B=20,Z_B=19 and G_B=5. Only the first, hot K13 and K11 can be positive: their q values are 6 and 3, respectively. All other q values are <=2.

## Correct block accounting, including starved KEEPs

Use cyclic maximal A-root blocks. A positive-cost leader splays key x with a>=1 grouped A events; all later requests in that block have the same key and zero A cost. Adjacent KEEP keys in W^p differ, including the period seam. Thus every KEEP belongs to a different A-root block and every KEEP-containing block has exactly one KEEP. A KEEP-less block contributes 2a to C_D and no B demand.

If a block begins with DELETE x and later has KEEP x, its leader cost remains the cost of that KEEP-containing block. The later zero-cost KEEP does not erase it, and the leader is not a pure reset. For the A-state argument, compress such a block to its single effective splay of x. Moving its B action within the constant-key block changes neither the boundary states nor its B cost; A/B trees are independent and the other A operations are no-ops. The compressed sequence consists exactly of the KEEP-key splay sequence, interspersed with effective KEEP-less A splays. No source action or unit is omitted from either a or C_D.

## Spine growth through the descending tail

Start immediately after any KEEP12 at the end of the increasing scan. A is rooted at 12. Its right subtree is the single key13, while its left subtree is an arbitrary valid BST on 1,...,11. Both 12 and 13 are on its right spine.

Next come the eleven descending KEEP blocks 11,10,...,1. Just before processing k, let P be the previously processed core keys {k+1,...,13}. Every currently counted vertex in P on A's right spine is larger than k. By AC01, splaying k retains all of them and adds the new root k to the counted set. Each effective KEEP-less A splay with a events can remove at most 2a counted vertices. Other source requests in its A-root block do nothing to A.

Let R be the sum of pure grouped A work between this KEEP12 and the next hot K13 block leader, stopping before that leader acts. Starting with two counted vertices, adding eleven, and subtracting at most 2R losses gives at least 13-2R counted vertices on the right spine. Since key13 is its largest core vertex,

    d_A_before_hot_13(13)>=12-2R.                            (1)

Negative lower bounds are simply vacuous. Each retained counted vertex before 13 is an ancestor of 13. No assertion about off-spine keys or matched subtrees is needed.

## Requested two-reset contradiction

In one closed 26-KEEP period with two PURE one-StepEv resets, all pure work totals two, so R<=2. Equation (1) gives

    d_A(13)>=8,   a_13>=4,   max(6-2a_13,0)=0.

The sole other possible positive block is hot K11. Every actual leader has a_11>=1, so its excess is at most 3-2=1. Hence

    E<=1<4=C_D.                                             (2)

The requested E>C_D coupling is impossible, regardless of reset gaps, keys, initial A shape or diagonal reachability. This is a source contradiction, not the failure of a selected reset policy. E=5 would require a_13=a_11=1; (1) further shows that a_13=1 alone requires at least five pure A StepEvs on the preceding tail interval, contributing capacity at least ten, already larger than G_B=5 for one period.

If either syntactic reset belongs to a starved KEEP block instead of being pure, C_D need not equal four. The broader theorem below still excludes E>C_D; the accounting does not silently turn every DELETE into a pure payer.

## All powers and arbitrary pure-reset budgets

Partition an actual closed walk with KEEP projection W^p into p cyclic cells, each immediately after one KEEP12 through the next KEEP12. Let T_l be the total grouped A cost of KEEP-less leaders in that cell. These physical pools are disjoint across cells, and

    C_D=2 sum_l T_l.

Each cell has one hot K13 and K11, and no other possible positive. Its tail interval work R_l is at most T_l. Since every KEEP block has a positive-cost leader, (1) implies

    a_13>=max(1,6-T_l),
    e_13<=max(6-2 max(1,6-T_l),0),
    e_11<=1.                                                (3)

The zero-work branch needs its own argument. If T_l=0, A has no effective pure splay anywhere in the cell. The descending scan from 12(U,13), for arbitrary U, sends A exactly to R13. This is the reflected successive-key scan induction: each next smaller key is the maximum of the left subtree, preserves the already processed right vine, and adds its root. Therefore hot K13 has depth12 and cost6; the next hot K11 has depth7 and cost4 by the exact source prefix. Starved KEEP leaders perform those same effective splays. Both excesses are zero, giving E_l=0.

For T_l>0, (3) gives the complete integer bound:

| T_l | Lower bound a_13 | Upper bound e_13 | Upper bound e_11 | Upper bound E_l | Cell pure capacity |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 0 | 6 | 0 | 0 | 0 | 0 |
| 1 | 5 | 0 | 1 | 1 | 2 |
| 2 | 4 | 0 | 1 | 1 | 4 |
| 3 | 3 | 0 | 1 | 1 | 6 |
| 4 | 2 | 2 | 1 | 3 | 8 |
| 5 | 1 | 4 | 1 | 5 | 10 |
| >=6 | 1 | 4 | 1 | 5 | >=12 |

The tail row is an exact consequence of the constant G_B=5 bound, not an extrapolation from tested values. Every row gives E_l<=2T_l, strictly when T_l>0. Summing over the actual closed walk proves

    E<=C_D,
    and E<C_D whenever C_D>0.                               (4)

No assumption of two resets in each B period is needed. Resets may have arbitrary costs, vary their keys and positions, or be concentrated across different B periods. The cell partition counts each once. Increasing the recurrent A period or adding more resets cannot recover E>C_D on this word.

## UD and no-reuse consequence

The inherited CW01 DELETE-budget lemma proves that E<=C_D supplies an old-UD accepted physical cut. It uses the cyclic values +excess at positive blocks, -2a at KEEP-less blocks and zero elsewhere, cut after a MINIMUM cumulative sum. The chronological reflected debt queue then clears within one period. Early unused units are retired. Positive local prefixes, KEEP-less outgoing pools and distinct B-demand tails are assigned once; monotone source occurrence/event/bit identities prevent reuse. No prefix, next-lap or alternative-cut capacity is pooled.

Combining that established lemma with (4), every actual closed coupling of W^p is already old-UD-covered. It therefore cannot witness FI acceptance with UD rejection at every cut. No FI/UD recognizer or allocation optimizer is needed to prove this obstruction.

## Scope, symmetry and what this does not prove

Reflect x->14-x and swap left/right. The entire proof uses the left spine and minimum core key1 in the reflected cycle; source cases and costs agree. Empty fringes, root no-ops, zig-only resets, starved KEEP leaders and blocks crossing the input seam are included above. Each repeated B period is a distinct physical cell, not the same credit pool reused.

The proof also survives substituting an arbitrary untouched upper fringe at the right child of core13, provided all KEEP and DELETE targets remain among the core keys and A/B trees are of that substituted form. The core projection, all requested depths, source rewrites and scan canonicalization remain unchanged. The reflected lower-fringe extension follows as well. Arbitrary extra-key DELETEs are outside that fringe corollary. No larger finite size is executed.

This refutes the fixed KEEP family as the requested coupling architecture. It does not refute strict FI-only existence on other words, or prove universal CD. In fact this particular family was already trivially CD-bounded by Q_B=20p and A>=26p from its distinct adjacent KEEP blocks. The new content is the structural E<=C_D obstruction and its resulting old-UD membership, not a newly solved original CD subclass. The earlier B-only G_B=5 construction remains correct; its budget is not jointly realizable as required A excess. Matching-terminal and Stage 11G are unchanged.
