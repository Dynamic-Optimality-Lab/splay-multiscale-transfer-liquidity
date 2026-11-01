# A first-intervention frame ceiling that recovers payer capacity

Status: PROVED—UNIVERSAL for the local source-frame depth bound. PROVED—RESTRICTED DOMAIN for the constructive charging corollary and the earlier-repayment source spans. Every successful UD cut is preserved. A strict enlargement of UD's closed-walk class is NOT ESTABLISHED. Universal Step 3/CD remains OPEN; matching-terminal work stays FROZEN.

## Source convention and operation sites

S_x is ordinary source bottom-up splay on a finite BST with present keys x and y. Same-side LL/RR doubles rotate the parent over the grandparent first. Use edge depths. The source search path to x has depth d and directions e_0,...,e_(d-1). Its doubles consume pairs innermost first, at original site-top depths

    d-2, d-4, ..., 0 (even d), or ..., 1 (odd d).

If d is odd, a final zig consumes the root frame at depth zero. A double's case is the two consumed original directions, LL/RR/LR/RL. Its top and parent are the corresponding unconsumed original search-path nodes; the rebuilt inner unit is rooted at x. These are the actual source frames and case word, not a different rotation convention.

For y!=x, define its entry operation as the first consumed operation site whose key set contains y. Before entry, all operations lie in subtrees excluding y, so its depth remains h=d_T(y). Operation sites ascend. Their key sets equal the corresponding ORIGINAL rooted-subtree key sets, since earlier rotations inside them preserve key membership and do not consume their top nodes. Thus entry can be found either by original-site subtree membership or by choosing the first site-top depth <= the original LCA depth of x and y. This definition includes a y below x: it is present in the first operation site. If the first containing operation is a zig, it is final.

## Exact source shifts and conservative first gain

The source double shapes and shifts are those already used in DS/UD. At a double, the parent p has depth shift zero; the grandparent g gains at most two; any fringe key gains at most two. Thus the first-gain allowance is

    mu=0  if y is that entry double's parent;
    mu=2  for any other y!=x in an entry double;
    mu=1  if entry is the final zig.             (1)

This deliberately retains a conservative bound for a cross-case grandparent and many fringes. It does not read y's post-splay depth to select mu.

Immediately after entry, y is a proper descendant of the rebuilt root x, hence lies in its left fringe when y<x and its right fringe when y>x. At every later outer double those are the target node's two current child fringes. The actual global depth shifts for every key inside them are:

| Later source operation | Target left fringe y<x | Target right fringe y>x |
| --- | ---: | ---: |
| LL | -2 | -1 |
| RR | -1 | -2 |
| LR | -1 | -1 |
| RL | -1 | -1 |
| final left zig | -1 | 0 |
| final right zig | 0 | -1 |

For example, LL is g(p(x(A,B),C),D)->x(A,p(B,g(C,D))); the current target fringes A/B shift -2/-1. RR is g(A,p(B,x(C,D)))->x(p(g(A,B),C),D), giving -1/-2 on C/D. LR gives -1/-1 on B/C in g(p(A,x(B,C)),D)->x(p(A,B),g(C,D)). RL gives the same on B/C in g(A,p(x(B,C),D))->x(g(A,B),p(C,D)). These formulas act uniformly on arbitrary fringe trees; internal depths and multiplicities do not affect the shifts.

Let r count doubles strictly after entry. Let m count among them LL when y<x, or RR when y>x. Each later double decreases depth by exactly one plus this matching-side indicator. The later final zig has nonpositive shift and may safely be ignored. Summing after the first-gain allowance gives

    d_(S_x T)(y) <= h+mu-r-m.                   (2)

The expression bounds a nonnegative depth; clamping below at zero does not invalidate it. Combining it with the inherited whole-splay bound h+2 gives the explicit universal ceiling

    U_T(x,y)=min(h+2, max(0,h+mu-r-m)).          (3)

If x=y, set U=0 because splay places x at the root. If d=0, set U=h because the tree is unchanged. These special cases supersede entry parameters. Formula (3) and its proof hold for every finite tree, both orientations, every source path length and arbitrary fringes. No fitted constant or finite classification is used.

The bound is generally loose: mu overestimates many first shifts, and later zig decreases are ignored. No full exact-depth update is hidden in (3). The audit observes 1,958 loose bounds on its fixed corpus, supporting that distinction but not constituting the universal proof.

## Refine only one intervening B splay per anchor fact

Keep UD's cyclic A-root blocks and source quantities. A leader i has actual grouped cost a_i>=1, B doubles q_i, and delta_i=q_i-2a_i. DELETE splays A alone and freezes B; it never removes a key. A block contains at most one genuine B-changing KEEP. A genuine single B zig counts as a change even with q=0.

For each positive anchor i and each present key y, let h_i(y) be y's depth in the anchor's B destination. At a later payer block j with key y, let k_i(j) count genuine B changes in strictly intervening blocks. UD uses floor(h_i(y)/2)+k_i(j).

If k>=1, let the FIRST such change be S_x. Its pre-tree T equals the anchor's B destination: all earlier intervening DELETEs and B-root no-ops leave B unchanged. Compute U_T(x,y) using only this source pre-tree, x, y and its source frame word. Do not obtain U by looking up the first-post depth or future payer work. Bound every remaining k-1 intervening change by the inherited +2 rule. Therefore

    c_FI(i,j)=floor(h_i(y)/2),                   if k=0;
    c_FI(i,j)=floor(U_T(x,y)/2)+(k-1),           if k>=1, (4)

for a block with KEEP. For a KEEP-less block put c_FI(i,j)=0. As before, A-only requests before a block's first KEEP do not change its B source state. Thus

    q_j <= c_FI(i,j) <= c_UD(i,j).              (5)

The right inequality follows from U<=h+2 and floor((h+2)/2)=floor(h/2)+1. It also holds in the k=0 and KEEP-less cases. Zero h, a first intervener accessing y, a first single zig, root no-ops and intermediate returns to y are all covered. The refinement is made ONCE per anchor/payer fact; later interventions are not refreshed or exactly propagated.

## One reservation, one loan suffix, no reused credits

Retain every encountered positive source fact, including paid anchors. At each nonpositive payer j with capacity C=2a_j, take c_j as the minimum of (4) over all encountered positive anchors. With no history reserve the entire pool and lend nothing. Otherwise reserve r_j=min(C,c_j), once. Nonpositivity gives q_j<=C, while (5) gives q_j<=c_j, so q_j<=r_j.

Use the first q_j actual units of [0,r_j) for own B demands. Lend only [r_j,C), oldest unpaid anchor first, in disjoint consecutive unit slices; advance recipient residual-demand cursors. Retire the physical pool after this one visit. The extra capacity released by a smaller r_j belongs to this SAME suffix, not to an additional virtual pool. A source fact may tighten many later reservations without creating a credit itself.

Each A StepEv has distinguishable units (cycle occurrence,event index,bit), bit 0/1; each B double has demand identity (cycle occurrence,B-event index). Positive anchors use their own first 2a_i units for their first 2a_i demands. Monotone residual cursors ensure no later loan repeats a demand. A payer's reserved prefix and all loan slices are disjoint; different physical pools are distinct. The complete injection therefore contains no reused units or demands.

For an accepted one-period cut every B demand is paid, giving Q_B<=2A. Reject a cut if residual debt remains. Prefix, second-lap, future-anchor and alternative-cut budgets are never available to repair a rejection. Closed walks with A=0 have Q_B=0 by the established fixed-root closure argument; empty, one-key, all-nonpositive and all-positive boundaries behave as in UD. Membership defined by trying all physical block cuts is invariant under rotation; success at every cut is not asserted.

## Old successful cuts and complete-block spans are preserved

For a fixed order both old UD and FI retain the same source-positive history independently of payment. Equation (5) implies every refined reservation is no larger and every refined certified suffix S_F is at least S_U. All pending anchors are eligible under both procedures.

With D_F<=D_U before a block, a positive adds the same delta to each. A nonpositive updates

    D_F'=max(0,D_F-S_F),
    D_U'=max(0,D_U-S_U),

so D_F'<=D_U'. Starting at zero proves total-debt domination throughout every cut, and every previously accepted cut remains accepted. Individual recipient allocations need not coincide.

The same proof applies to a finite directed span of consecutive COMPLETE A-root blocks, beginning at a positive-cost leader and using only units in that span. If FI finishes with zero residual, it proves Q_B(span)<=2A(span) without endpoint credit. This is a restricted statement: an arbitrary open trace may start with an unfunded A-root no-op and positive B work. Such a leading fragment is not a complete positive-leader block and is not covered by this span theorem. No false A=0 assertion is made for open traces.

The three-block span in FI02 is accepted by FI and rejected by the old UD procedure in its fixed directed order. It proves strictly earlier repayment using only those ten physical units. It does not prove strict enlargement of the closed-walk class: its containing cycle was already accepted by UD. A supplied disjoint collection of such source spans composes by the same unit-identity argument, but no assertion that arbitrary cycles admit that collection or an accepted cut is added.

## Precise advancement and remaining boundary

The original over-reservation at KEEP12 is removed by a universal source-frame estimate. The outstanding unit is paid before any DELETE credit is spent. The all-size frame lemma, source-derived reservation refinement, old-cut preservation and strictly stronger directed-span repayment are complete.

Strict new closed-cycle coverage, universal cut success, exact-surplus allocation and universal CD remain unestablished. Those would require further work, not a reinterpretation of the already accepted source word. No further campaign follows this result automatically. All old research, proof statuses, Stage 11G and the matching-terminal freeze are preserved.
