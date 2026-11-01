# A source-exact primitive B cycle with G_B=9

Status: FINITE-EXACT for the explicit thirteen-key cycle and source prefix, with analytic derivation through GB01's exact recurrence. PROVED structurally for the arbitrary-fringe extension below. The requested B-only threshold G_B>=5 is achieved. No A reset or FI-only pair is asserted.

## Concrete construction

Use upper guard 13 and local query order

    L=(1,9,5,3,11,7,2,10,6,4,12,8).

Return to 13 after each query. The complete word is

    W=1,13,9,13,5,13,3,13,11,13,7,13,
      2,13,10,13,6,13,4,13,12,13,8,13,

with every operation a KEEP. Start with the valid tree T0=13(R_[1,12],empty). It can be the diagonal initial tree in the source model, whose T0 is arbitrary. If the same KEEP prefix is applied to A as well, it lifts to a diagonal A/B prefix by identical inputs and maps; the current audit executes B only.

The exact source identities are

    S_W(T0)=B*,
    S_W(B*)=B*,

where

    B*=13(12(8(6(4(2(1,3),5),7),10(9,11)),empty),empty).

A bare key is a leaf. Thus one W is a 24-request reachability prefix and the next W is the recurrent cycle. Substituting the left subtree of B* into the H_x recurrence of GB01 yields it again after the twelve local queries. The local root/depth/cost table specifies that source calculation; every intermediate raw tree is in the certificate.

## Exact recurrent profile

| Query x | Local root u | Local depth d | Query q_x | Return q_13 | Query surplus max(q_x-2,0) | Returned local root |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 12 | 5 | 3 | 1 | 1 | 12 |
| 9 | 12 | 5 | 3 | 1 | 1 | 12 |
| 5 | 12 | 6 | 3 | 0 | 1 | 5 |
| 3 | 5 | 4 | 2 | 0 | 0 | 3 |
| 11 | 3 | 5 | 3 | 0 | 1 | 11 |
| 7 | 11 | 6 | 3 | 0 | 1 | 7 |
| 2 | 7 | 3 | 2 | 1 | 0 | 7 |
| 10 | 7 | 3 | 2 | 0 | 0 | 10 |
| 6 | 10 | 5 | 3 | 1 | 1 | 10 |
| 4 | 10 | 5 | 3 | 1 | 1 | 10 |
| 12 | 10 | 2 | 1 | 0 | 0 | 12 |
| 8 | 12 | 7 | 4 | 1 | 2 | 12 |
| Total | | | 32 | 6 | 9 | |

Hence the cycle has

    length=24, Q_B=38, Z_B=10,
    G_B=sum max(q_B-2,0)=9>=5.                 (1)

The seven q_x=3 opportunities contribute seven and the one q_x=4 opportunity contributes two. Every return has q<=1 and contributes zero. The full q sequence is

    3,1,3,1,3,0,2,0,3,0,3,0,
    2,1,2,0,3,1,3,1,1,0,4,1.

All twenty-four source B trees in the recurrent cycle are distinct. The final destination equals its first source exactly. This is a simple cycle, so it is not a power of a shorter B cycle and does not reach the target by period multiplication. The predeclared chronological loop decomposition emits exactly ONE component: the entire W. No loop was removed, no alternative component was substituted, and no separate low-budget loops were concatenated to manufacture success.

## Source provenance and independent verification

The tuple audit records the whole two-lap B trajectory, all source/destination trees, exact depths and event cases/intervals/orientations. At every query/return pair it separately computes the full local splay and the omitted-zig partial result, then compares GB01's predicted returned shape and double counts with the global source.

The pointer verifier independently replays all global and local requests and reflects them under x->14-x, swapping event cases LL/RR and LR/RL, zig direction and interval endpoints. It checks first whole-boundary recurrence, direct diagonal reachability, every local law, source-edge multiplicity in the canonical decomposition, primitive closure and all G_B counts. Reflected states/costs form a second exact orientation with lower guard 1.

There are 48 global orbit rows and 24 local query checks per orientation: 96 global pointer source calls plus 48 local calls, 144 total, with 290 raw BST validation occurrences. Zero/even/odd-away/odd-toward source cases all occur. No larger finite key size, fit, A-reset search, FI/UD comparison or formal-assistant build is used.

## Arbitrary-fringe extension

Attach any BST F with keys >13 as the guard's right child in T0. Queries and guard returns never enter F. GB01 explicitly preserves its V fringe, so both source identities become

    S_W(13(R_[1,12],F))=B*(F),
    S_W(B*(F))=B*(F).

All core depths, source events, Q_B, Z_B and G_B are unchanged. Substitution is injective: deleting the distinguished larger-key fringe recovers the core tree, so simplicity and the exact first return are preserved. Reflection gives arbitrary unrequested left fringes. This is an analytic all-size family with fixed thirteen-key requested support, not a claim of unbounded genuine KEEP support and not a larger finite fit.

## Interpretation for two planned resets

Two one-StepEv PURE resets would supply four actual units in their KEEP-less blocks. The numerical necessary budget G_B>4 is therefore cleared by five units on this chosen primitive B cycle. That difference is headroom in an upper bound; it is not a spendable credit pool, an actual E value, a proved reset placement or FI-only coverage.

Moreover, GB03 proves an additional obstruction: the guards already pay most possible query excess under old UD, leaving source residual upper budget one. Two pure resets would pay four and make the coupled class old-UD-covered. The raw B target is achieved; a strict two-pure-reset coupling on THIS guarded order is not a remaining existence claim and must not be advertised as the next successful architecture.
