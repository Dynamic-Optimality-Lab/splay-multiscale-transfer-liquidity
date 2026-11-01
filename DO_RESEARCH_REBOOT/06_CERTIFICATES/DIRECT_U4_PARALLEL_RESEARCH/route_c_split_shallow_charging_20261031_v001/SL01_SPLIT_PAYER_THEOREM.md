# Split shallow payers with retained source facts

Status: PROVED—RESTRICTED DOMAIN. For every finite key set and every reachable closed actual A/B source walk accepted by the deterministic procedure below, Q_B<=2A. Every successful XR cross-run batch cut remains successful. SL02 gives a reachable strict witness and an analytic family with unbounded KEEP support.

This is a source-unit charging theorem. The matching-terminal line remains frozen. The successful-cut restriction is explicit and is not proved necessary for arbitrary reachable walks. Universal CD and Step 3 remain OPEN.

## Source quantities and boundary cases

KEEP x splays A and B. DELETE x splays A alone and freezes B; it does not remove x from the key set. All requests are present keys. A cost is the number of grouped source StepEvs, a=ceil(d_A(x)/2); B work q=floor(d_B(x)/2) counts doubles only. A B zig is a genuine tree change even though q=0.

Use cyclic maximal A-root blocks as in SC, DS, SP and XR. Each block i has one positive-cost leader a_i>=1, followed by zero-A-cost requests of that same key. There is at most one genuine B-changing KEEP in a block. Define q_i as the block's total B doubles and delta_i=q_i-2a_i. Thus

    sum_i delta_i = Q_B-2A.

A positive block has delta_i>0. Every nonpositive block can pay its own B doubles from its 2a_i units. One actual A event carries distinguishable units (cycle occurrence, A-event index, bit), bit in {0,1}. A B demand is (cycle occurrence, B-event index), with event case other than ZIG. Multiplicities and repeated keys are retained through occurrence identities.

If A=0, A has one fixed root and every request is that root. B can change at most once before staying there. Exact closure forces no change, so Q_B=0. Empty walks/key sets and one-key cases follow. Otherwise the cyclic block decomposition is valid, including a block crossing the input seam. An accepted pass uses one occurrence of every physical block, not a prefix or second lap.

## Source depth facts, inherited rather than fitted

For every whole source splay S_x and tracked present key y,

    d_(S_x T)(y) <= d_T(y)+2.                    (1)

This is the established 26AL/DS source displacement lemma. Its arbitrary-fringe proof uses the actual parent-first LL/RR formulas: the first rebuilt site containing y raises its depth by at most 2; subsequently y is in a fringe of the unit rooted at the accessed x, and every later outer rebuild gives that fringe a nonpositive shift. A final zig increases depth at most 1 and gives no subsequent increase. No bound on path length, fringe size or number of earlier splays is needed.

In particular, an old root ends at depth <=2 and an old child at depth <=3. For a positive anchor i, let C_i be the root and nonempty children of B immediately before i's genuine B splay. For y in C_i, record its actual post-splay depth h_i(y), between 1 and 3. It cannot be the accessed key: positivity and a_i>=1 imply q_i>=3, hence the accessed key was at depth >=6.

For a later block j whose key y lies in C_i, let k_i(j) count genuine B-changing KEEPs strictly between the two blocks in the selected one-period order. Count a zero-double zig; omit DELETE and B-root no-ops. Applying (1) repeatedly gives

    q_j <= c_i(j),
    c_i(j) = floor(h_i(y)/2)+k_i(j) if j has a KEEP,
    c_i(j) = 0                         otherwise. (2)

The floor identity floor((h+2k)/2)=floor(h/2)+k is exact. A block's B may wait through an initial DELETE, but no B change occurs before its first KEEP. If that KEEP is a root no-op, the ceiling remains sound. Intermediate splays may access y, which only improves (1); no avoidance premise is required. These statements hold across a seam because actual paired closure identifies the physical endpoint state.

Several bounds in (2) constrain the same physical q_j, so they combine by minimum. A source fact can stay valid after its anchor's demands are paid. Its validity never supplies a second A pool or an extra spendable unit.

## Deterministic one-period construction

Choose a block cut and scan exactly m blocks in cyclic order. Maintain:

- An append-only history H of every positive anchor encountered, with C_i and h_i.
- A residual cursor p_i for each such anchor, initially zero. Its unpaid amount is delta_i-p_i.

At a positive block i, pay the first 2a_i B doubles from its own units. Append its remaining delta_i demands, in source-event order, with cursor p_i=0. Append i to H. Positive pools lend nothing.

At a nonpositive block j, its key is y and capacity is C=2a_j. Let H_y contain every historical anchor i with y in C_i, including anchors whose cursor already equals delta_i. If H_y is nonempty, set

    c_j = min_(i in H_y) c_i(j),
    r_j = min(C,c_j),
    S_j = C-r_j.                                (3)

If H_y is empty, set r_j=C and S_j=0. Freeze this reservation once for this physical pool. By nonpositivity and (2), q_j<=C and, when a fact exists, q_j<=c_j; therefore q_j<=r_j in every case.

Number j's units 0,...,C-1 by A event then bit. Pay j's own q_j demands from the first q_j positions of the reserved prefix [0,r_j). The unoccupied part of that prefix stays reserved and is not lent.

Use the suffix [r_j,C) for loans. Inspect all unpaid eligible anchors in history order, oldest first. For each, lend the minimum of its remaining debt and the suffix's remaining capacity. Assign the next residual demands using the next consecutive suffix units; advance both cursors. Stop when the suffix is exhausted or all eligible debts are paid. Eligibility is individual: a payer may help one anchor even when its key is absent from another anchor's shallow set.

Retire the pool immediately. Do not bank unused capacity, revisit the pool, reserve it again for another anchor, or lend it to a future positive. Keep H unchanged even when an anchor is paid. Facts are retained; spent pools are not retained as resources.

Accept the cut exactly when every seen positive is fully paid at the end of this one period. Define the split shallow class SL by success of at least one physical block cut. This is a completely specified finite source-trace procedure; there is no allocation optimizer, backtracking or unknown compatibility witness.

## No reused unit or demand

Positive local assignments use distinct pools and exactly their first 2a_i B demands. No later loan touches that paid demand prefix. Each residual cursor only advances; a loan takes the half-open residual interval [p_i,p_i+t), then replaces p_i by p_i+t. Consequently two different payers cannot discharge the same residual demand, even when one anchor is split among arbitrarily many payers.

Each nonpositive pool is processed exactly once. Its own work is inside [0,r_j), and all outgoing loans occupy disjoint consecutive slices of [r_j,C). The reservation is computed once using all available facts about the same q_j. No separate budget is allocated for each fact or recipient. Positive-local, payer-local and outgoing assignments are disjoint both within and between physical pools.

At any completed pass, if U=sum_i(delta_i-p_i) over seen positives, then

    assigned B demands = Q_B-U,
    unused A units = 2A-(Q_B-U).                 (4)

Every nonpositive own demand is paid; all remaining uncovered demands are exactly the residual cursor tails. Every assignment uses one actual source unit. An accepted cut has U=0, so its injection of Q_B distinct B demands into 2A distinct A units proves Q_B<=2A. A rejected cut with U>0 supplies no full-cycle certificate. Alternative cuts are alternative proofs, and their budgets are never combined.

The proof is independent of tree size, delay, fringe shape, number or size of positive runs, number of payers per anchor, and number of recipients per payer. Those parameters are unbounded within the explicitly accepted class. This is scalar closed-walk charging; no online temporal service guarantee is claimed.

## Every successful XR cut is preserved

Fix an old XR successful cut and its sequence of closing payers. Induct that all anchors through each old closing payer have been paid by SL by that same point. The assertion is empty before the first batch.

At the next old closing payer j, let P be XR's pending batch, E=sum_(i in P)delta_i, and c_P=min_(i in P)c_i(j). XR's conditions give y_j in every C_i for i in P and

    E+c_P <= C=2a_j.                            (5)

By induction SL owes no earlier batch. Its current unpaid anchors form a subset of P; partial earlier loans may have reduced or eliminated their debts. Their total remaining debt D is at most E. SL's retained history still contains ALL of P, including any already paid member. Thus H_y contains P and c_j<=c_P. Equation (3) yields

    S_j=C-min(C,c_j) >= C-c_P >= E >= D.        (6)

All remaining anchors are eligible at j. This fresh, once-visited pool therefore clears every remaining debt, regardless of how earlier loans were distributed. The induction continues; the last old closure leaves no debt. Zero-positive cases agree. Hence every XR successful cut is SL successful, and XR is a subclass of SL.

Retaining paid facts is essential to THIS containment proof: deleting the paid member supplying the best ceiling could raise c_j and shrink the certified suffix. We make no unsupported assertion that every such truncation necessarily fails on some source walk. A historical fact's use in (6) costs no credit; only actual units in j's suffix pay demands.

## Cyclic semantics and scope

Rotating a source cycle permutes its physical block cuts. Membership, defined by trying all of them, is invariant under that rotation. A single selected pass may reject if it ends before sufficient eligible pools arrive. The method does not promise all cuts succeed or that every successful cut gives the same allocation.

No positive blocks means local success. An all-positive nonempty pass has no lender and rejects. Empty eligible sets, exhausted reservations and stranded residuals also reject. No resource from a prefix, a preceding period, a future positive or an alternative cut repairs a failed pass. Global source bounds remain true independently of whether the cut succeeds.

SL02's strict source witness is outside XR at every cut. Thus the precise new original CD case is the accepted SL complement SL\XR, now settled with a direct explicit charging injection. Neither arbitrary successful-cut availability nor unrestricted shared allocation is established. The matching-terminal line, the refuted setup graph, the old proof statuses and Stage 11G remain unchanged.
