# Delayed shallow charging without credit reuse

Status: PROVED—RESTRICTED DOMAIN. The theorem below extends SC's immediate shallow-successor class to a canonical delayed private-payer class. Tree size, KEEP support, delay, number of positive blocks and fringe shape are unbounded. The payer conditions are restrictions on the covered walks, not claimed universal facts.

No terminal potential or matching construction is used. The matching-terminal line remains frozen. Universal CD and all Stage 11G statuses remain OPEN and unchanged.

## Source blocks and demands

Use the established cyclic maximal A-root blocks. A block i has one positive-cost A leader, cost a_i>=1, followed by root no-ops of the same key. It has at most one nontrivial B splay, at its first effective KEEP. Let q_i be its total B-double count, and set

    delta_i=q_i-2a_i,
    sum_i delta_i=Q_B-2A.

DELETE accesses do not change B. A B-root KEEP no-op does not change B. A genuine B-changing KEEP has positive B depth; it may have q=0 and consist solely of a final zig. Those are different cases for the delay count.

The A=0 closed-walk case has Q_B=0: all A requests use one fixed root, and B could change at most once before remaining fixed, so exact B closure forces no B change. Empty walks, empty key sets and one-key trees are included. Otherwise the A-root block decomposition is well defined cyclically, including seam-crossing blocks.

## Source displacement bound, independent of access depth

For any BST T, present target x and tracked key y,

    d_(S_x T)(y)<=d_T(y)+2.                        (1)

This is the banked 26AL-L1 statement. The source proof is restated explicitly because the unit of the delay tax is one whole B splay, not one primitive rotation or double.

Write the four source double shapes using target x, parent p, grandparent g and fringe trees A,B,C,D. The following shifts apply to every key inside each indicated fringe; internal fringe depths and multiplicities are unchanged.

| Case and source shape | g | p | x | A | B | C | D |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| LL: g(p(x(A,B),C),D) -> x(A,p(B,g(C,D))) | +2 | 0 | -2 | -2 | -1 | +1 | +2 |
| RR: g(A,p(B,x(C,D))) -> x(p(g(A,B),C),D) | +2 | 0 | -2 | +2 | +1 | -1 | -2 |
| LR: g(p(A,x(B,C)),D) -> x(p(A,B),g(C,D)) | +1 | 0 | -2 | 0 | -1 | -1 | +1 |
| RL: g(A,p(x(B,C),D)) -> x(g(A,B),p(C,D)) | +1 | 0 | -2 | +1 | -1 | -1 | 0 |

These are the actual parent-first same-side formulas. A final zig has maximal increase +1. For a left zig g(x(A,B),C)->x(A,g(B,C)), the fringe shifts are A:-1,B:0,C:+1; the right zig is its reflection.

Before the first operation whose site contains y, y is outside the rebuilt site and its depth is unchanged. That first operation increases its depth by at most 2. If y is not the accessed key x, it then lies in a child fringe of the rebuilt unit rooted at x. At every subsequent outer double, x remains the target and these inner fringes have nonpositive shifts: LL uses A/B, RR uses C/D, and LR/RL use B/C. A final zig likewise shifts those target fringes by at most zero. Thus no later increase accumulates. If y=x its final depth is zero. This proves (1) for every finite path and arbitrary fringes.

A root no-op leaves the whole tree fixed and contributes zero displacement. Consequently only genuine B-changing KEEPs need the +2 allowance. The literal three-key controls confirm both the zero-double zig (+1 depth change with q=0) and the +2 double case; the universal proof is the frame argument, not those controls.

## Initial shallow set and delayed ceiling

Fix a positive block i. Let T_i be B immediately before its unique nontrivial B splay of x_i. Its candidate payer set C_i consists of T_i's root and nonempty original children. For y in C_i let

    h_i(y)=d_(S_x_i T_i)(y).

SC's source root/child transport proof gives h_i(y)<=3. Since x_i has positive deficit and therefore q_i>=3, it cannot itself have pre-splay depth at most 1; candidate keys differ from x_i, so their post-splay depths are positive.

For a later block j with leader key y in C_i, let k_i(j) count genuine B-changing KEEPs in the strictly intervening blocks. Each block has at most one. Count zero-double zigs; omit DELETEs and B-root no-ops. Repeated application of (1) gives, immediately before j's first KEEP of y,

    d_B(y)<=h_i(y)+2k_i(j),
    q_j<=floor(h_i(y)/2)+k_i(j).                   (2)

The intervening accesses need not avoid y. An intervening splay of y resets its depth to zero and still satisfies (1). Define the source ceiling

    c_i(j)=floor(h_i(y)/2)+k_i(j) if j has a KEEP;
    c_i(j)=0                              otherwise.

For a KEEP-less block q_j=0, so this special case is exact. For a block whose KEEP happens to be a B-root no-op, the first expression may overestimate zero and remains sound.

The parity identity floor((h+2k)/2)=floor(h/2)+k is exact. Replacing actual h by the coarse upper bound 3 would lose useful source information. The new fixed delayed witness uses h=1 and k=1, giving c=1 rather than the coarse bound 2.

## Canonical restricted class

For every positive block i, scan forward in cyclic order, stopping before the next positive block or a return to i. A candidate j qualifies exactly when its leader key y belongs to C_i and

    delta_i+c_i(j)<=2a_j.                         (D)

Choose the FIRST qualifying block as i's private payer. If any positive block has no such payer in its gap, reject the walk from this restricted class. With no positive blocks, accept trivially. A positive block cannot be its own payer, and no full-lap credit is introduced.

This is an explicit source-trace test. It uses only the pre-positive root and children, their actual post-positive depths, intervening B activity, and the payer leader's actual A cost. It is not an assumed aggregate repayment inequality or a general unknown allocation witness. Membership is not asserted for all reachable walks.

The payer's negativity is derived. By (2) and (D),

    delta_j=q_j-2a_j<=c_i(j)-2a_j<=-delta_i<0.      (3)

Every intermediate block is nonpositive because the scan does not cross another positive. Therefore each selected interval from i through its payer has nonpositive total deficit.

## No overlap and no reused credit

Positive blocks divide the cycle into disjoint forward gaps: one anchor followed by nonpositive blocks, ending just before the next positive anchor. Every selected interval lies entirely in its own gap. Thus intervals belonging to different positive anchors are disjoint, including their endpoints. The single-positive case uses at most the remaining m-1 distinct blocks; zero-positive and short-cycle cases are covered without duplicating positions across a seam.

Give every actual A StepEv two distinct units. For anchor i, pay its first 2a_i B doubles locally. Its remaining delta_i demands use the first delta_i units of payer j's leader pool. Pay payer j's own q_j demands from subsequent units. This fits because

    delta_i+q_j<=delta_i+c_i(j)<=2a_j.

All intermediate blocks pay their own demands locally, using q_l<=2a_l. Their unused credits are not borrowed. All other unassigned blocks are nonpositive and also pay locally. Disjoint intervals give each anchor and payer unique ownership; local leaders and event identities are distinct. Every B double is paid once and every A unit is used at most once.

Summing the completed charges proves Q_B<=2A on the stated class. This is cyclic scalar charging, not an online claim and not a claim about the refuted creator/setup eligibility graph. No allocation optimizer is needed.

The first-payer choice is intrinsic to the cyclic source trace. Rotating the cut changes labels, not the physical anchor, payer, intervening B events or unit identities. A scan encounters all candidate blocks in order before the next positive, so it is sound and complete for this explicitly defined class. Cut changes do not create new copies of any credit budget.

## Containment and precise advancement

Every SC walk is admitted. Its immediate payer has k=0 and h<=3, so c<=1 (or zero if KEEP-less); SC's delta_i<=2a_j-1 implies (D). That first block qualifies before any other positive, and no delay is needed.

DS02 gives a reachable witness admitted here but rejected by SC: it has a genuine B-changing intervener, h=1,k=1,c=1 and a delayed leader with a=1. Its immediate successor key had pre-positive B depth 2. Thus containment of SC is strict, beyond the already banked displacement component. The new witness also fails the named older former-root and multi-positive packet predicates.

The complement remains open: consecutive positives, gaps without a qualifying shallow key, inadequate A cost, or repayment requiring shared/intermediate reserves are not covered. No claim is made that all walks admit the scan. Universal Step 3, CD, and Stage 11G remain unchanged.
