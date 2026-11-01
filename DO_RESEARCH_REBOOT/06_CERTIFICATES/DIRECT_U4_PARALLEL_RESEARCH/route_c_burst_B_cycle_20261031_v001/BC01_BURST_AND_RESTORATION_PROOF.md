# An explicit primitive B cycle with protected surplus five

Status: PROVED—RESTRICTED DOMAIN for the displayed source construction and its arbitrary upper-fringe substitution. The fully enumerated thirteen-key replay is FINITE-EXACT. This is a B component, not a new settled CD subclass or an FI-only paired witness.

## Source convention and construction

KEEP x performs the repository's present-key bottom-up splay. Depth counts edges; q=floor(depth/2) counts LL/RR/LR/RL doubles and z=depth mod 2 counts the final zig. In particular a zig-only access changes B and counts as a later intervention even though q=0. The authoritative tuple source is python/independent/splay.py; its independent pointer counterpart is python/liquidity/legacy_embedding.py. Same-side double rotations are parent first.

Write k(L,R) for a node, a bare key for a leaf node, and . for the empty tree. Let R_[a,b] and L_[a,b] be right and left vines on consecutive keys a,...,b. The diagonal initial B is R_[1,13]. Use the single fixed all-KEEP word

    W=(13,11,9, 1,2,3,4,5,6,7,8,9,10,11,12, 11,10,9,8,7,6,5,4,3,2,1).

There are 26 accesses. There is no warmup, orbit cap, seed search, larger finite key size or repeated-period padding.

## Three source identities create the surplus

The source rotations give

    B1=13(2(1,4(3,6(5,8(7,10(9,12(11,.)))))),.),
    B2=11(4(2(1,3),8(6(5,7),10(9,.))),13(12,.)),
    B3=9(4(2(1,3),8(6(5,7),.)),11(10,13(12,.))).

The exact grouped event lists, in execution order, are:

| Access | Input depth | Double events (case, interval) | Final zig | q |
| --- | ---: | --- | --- | ---: |
| 13 | 12 | RR[11,13], RR[9,13], RR[7,13], RR[5,13], RR[3,13], RR[1,13] | none | 6 |
| 11 | 7 | RL[10,12], RR[6,11], RR[2,11] | left [11,13] | 3 |
| 9 | 4 | RL[8,10], LR[4,11] | none | 2 |

These follow by substitution into the source RR and mixed-double formulas, followed by the indicated final zig. The exact before/after trees and every event interval/orientation are in burst_B_cycle_certificate.json and were reproduced by the pointer engine and reflection.

Thus the first two contributions to G_B=sum max(q-2,0) are four and one. Their immediate successors have q=3 and q=2. Neither surplus-bearing access is followed by a return to its former root, or even to that former root's child collar:

| Anchor | Former root/children | Next request | Next q |
| --- | --- | ---: | ---: |
| K13 | {1,2} | 11 | 3 |
| K11 | {13,2} | 9 | 2 |

## Restoration is an identity

Successive-key scan lemma: after splaying 1,2,...,k in any BST on keys 1,...,13, the root is k and its left subtree is L_[1,k-1]. For k=1, minimum access has an empty left subtree. Inductively the next key k+1 is the minimum of the current right subtree. Its search path begins right from k and then consists only of left edges. Inner LL rebuilds do not touch the old left vine. At the outer site either a right zig or an RL double places the old root k directly below k+1, with the old left vine attached and no key between k and k+1. This establishes the new left vine. This proof uses the source formulas, including both possible path parities.

For k=12 only key 13 remains on the right, so the increasing scan produces

    T12=12(L_[1,11],13).

This conclusion holds in particular for B3 above. Starting at T12, each descending access k=11,...,1 is its root's left child. One left zig produces

    Tk=k(L_[1,k-1],R_[k+1,13]).

Induction gives T1=R_[1,13], exactly the initial tree. No reachability prefix, guessed stabilization period or assumed closure is used.

## Simplicity and boundary checks

After B3 the unrequested subtree 13(12,.) is a fringe. A search for any key <=11 never enters it, so source rebuilds preserve that subtree throughout the increasing scan up to key 11. Each increasing-scan state has its known left vine and retains the core left edge 13->12 in its right subtree. The descending state with the same root instead has a right vine on all larger core keys. The two states therefore differ.

The burst states with roots 11 and 9 have left-subtree root 4; the scan states with those roots have left-subtree roots 10 and 8. The burst root 13 appears nowhere else. The initial root-1 right vine differs from the increasing-scan root-1 state by the intact 13->12 edge. The final root-1 state is the closing endpoint and is counted once. All 26 source states are distinct, as the complete replay independently checks. This is a simple directed B-state cycle, hence a primitive recurrence; the success threshold has not been reached by multiplying a shorter period.

All 26 B depths are positive. Adjacent KEEP keys differ, including the cyclic seam 1->13. The sole syntactic turnaround ABA is 11,12,11; its middle access has q=1. We make no global ABA-free claim. What is absent is a surplus-bearing immediate guard return.

## Exact full cost profile

| Segment | B depths | B doubles q | B zigs z |
| --- | --- | --- | --- |
| 13,11,9 | 12,7,4 | 6,3,2 | 0,1,0 |
| 1,...,12 | 3,2,3,1,4,2,3,1,1,2,1,2 | 1,1,1,0,2,1,1,0,0,1,0,1 | 1,0,1,1,0,0,1,1,1,0,1,0 |
| 11,...,1 | eleven copies of 1 | eleven copies of 0 | eleven copies of 1 |

Therefore Q_B=20, Z_B=19, G_B=5, with 39 grouped B events and edge-depth sum 59. Only the first two positions have q>=3. The remaining word creates no additional raw surplus.

## Arbitrary fringe and reflection

Replace the empty right child of core key 13 in R_[1,13] by any finite BST F whose keys are all greater than 13. Every request is <=13, so no search or rotation enters F. Every source identity commutes with substituting F at that right fringe. The same 26 requests close exactly, and projection deleting F recovers the distinct thirteen-key states. Consequently simplicity, all requested depths/events, G_B and J_B, and the historical UD ceilings for requested keys remain unchanged. This is an analytic all-size fringe extension, not a larger finite replay; it does not assert unbounded genuine KEEP support.

Reflecting keys by x->14-x and swapping left/right proves the lower-fringe version. RR/LL and RL/LR swap, final zig directions swap, and an event interval [a,b] becomes [14-b,14-a]. The independent pointer audit explicitly checks all 26 reflected accesses.

## Direct graph connection and limit

This is an actual cycle in the B projection of the source transition graph, starting at a legal diagonal tree. Its diagonal all-KEEP lift has A=B throughout by determinism and is a trivial valid paired closed walk. That lift supplies no positive A-root block: its grouped A total is 39. The relevant prospective use is a different A trajectory obtained by permitted A-only insertions, which has not been constructed here. Source B surplus five is an upper bound on possible A-block excess, not actual five-unit debt or five available credits.

Matching-terminal remains FROZEN. No original Stage 11G graph, predicate, certificate or truth status changes.
