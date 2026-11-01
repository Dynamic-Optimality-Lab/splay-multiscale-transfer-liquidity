# A closure and reset funding are explicit before B is evaluated

Status: PROVED—UNIVERSAL for the root-position source identity, and PROVED—RESTRICTED DOMAIN for the displayed fixed A tour and all276 mode assignments. These positive component identities do not assert that the requested high-excess A/B witness exists.

For any n and r in {1,...,n}, let

    T_r=r(L_[1,r-1],R_[r+1,n]),

where L and R are left and right vines. Empty end vines are allowed. If x=r+1, x is the root's right child; one right zig gives T_x. If x=r+2, the source root frame is RR and the parent-first pair gives the new left vine ending at r+1, unchanged right vine, and root x. Thus it gives T_x in one grouped event. Reflect for x=r-1 and x=r-2. Consequently

    1<=|x-r|<=2  implies  S_x(T_r)=T_x and a=1.             (1)

This is an exact source identity with both orientations and all boundary cases; it is not a fitted all-n assertion. It follows directly from python/independent/splay.py's parent-first LL/RR and oriented zig formulas, independently checked here by python/liquidity/legacy_embedding.py.

At the existing thirteen-key size, start diagonally at T_1=R13 and fix

    C=(3,2,4,6,5,7,9,8,10,12,11,13,
       11,12,10,8,9,7,5,6,4,2,3,1).

Every successive step, including cyclic1->3, has magnitude one or two. Every A action therefore costs one StepEv, its output is T_key, and the last1 returns exactly to T_1. There are24 actions and24 grouped A events per lap. Frequent direction reversals avoid a full consecutive-key restoration sweep. Closure is furnished by (1), not an assumed scan result or a searched-for A state.

For each of the276 lexicographic pairs of positions 0<=d<e<=23, relabel those two actions DELETE and leave the other22 KEEP. The A trajectory is unchanged. Consecutive source action keys are distinct, so every action has its own positive-cost A-root leader. Both DELETEs are pure KEEP-less blocks with a=1, even if they are consecutive actions or two occurrences of the same key. No fallback or starved KEEP is needed. Hence

    A=24 and C_D=4 per A lap.                               (2)

After an exact p-lap pair recurrence, there are24p physical A events and2p reset occurrences, so C_D=4p. Only p=1 meets the exact-two-reset requirement; a two-lap cycle is not called a two-reset cycle.

Since every actual leader has a=1, every KEEP's positive excess is max(q_B-2,0), and a DELETE has zero positive excess. Therefore for every actual recurrent pair in this mode class,

    E=G_B exactly.                                          (3)

This removes the unknown A-cost compatibility premise within this class. It also makes the failed B-budget result in AT02 decisive. Formula (3) supplies no positive excess if all q_B<=2; it does not manufacture an A credit or borrow prefix work.

Some adjacent KEEP targets can coincide after DELETE actions are omitted. They still belong to different physical A-root blocks, because the intervening DELETE actions changed A's root and all A leaders cost one. J_B is evaluated by the same high/low formula on actual cyclic KEEP occurrences. Here every evaluated cycle has no high q>=3, so G_B=J_B=0 without needing any extension of the old helper theorem.

Every resulting source word and KEEP projection is checked for full consecutive ascending/descending twelve-key core sweeps, including the cyclic seam. All276 pass that check. This is the precise non-scanning property used here. The failure theorem is restricted to this fixed tour, seed and mode class; it is not a theorem about every small-rank walk or every all-one-StepEv A tour.
