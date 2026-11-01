# Established own-work coverage used by the uniform proof

UH01 uses the unchanged source-defined procedures from UD01(`route_c_unbounded_depth_charging_20261031_v001`) and FI01(`route_c_first_intervention_ceiling_20261031_v001`). Both are pinned inherited premises. In particular, the proof's statement that all non-residual demands pay in their own prefixes uses the already proved pointwise source-ceiling bound; it does not assume successful FI membership.

For a later KEEP payer j with key y, after a positive anchor i let h be y's depth and let k count strictly intervening genuine B changes. The established whole-splay displacement inequality increases any tracked depth by at most2 per genuine splay, including a single zero-double zig. Thus q_j<=floor(h/2)+k under UD.

For FI with k>=1, its first such change acts on the exact post-anchor tree T. The original-source-frame ceiling gives the first-post depth at most U_T(x,y). Bound each of the remaining k-1 changes by +2. Then

    q_j <= floor((U+2(k-1))/2) = floor(U/2)+k-1 = c_FI(i,j).

When k=0 the bound is floor(h/2). KEEP-less DELETE payers have q=0 and ceiling0. The source bound U<=h+2 also gives c_FI<=c_UD. These are source facts, valid regardless of whether the anchor has been repaid. Retaining paid facts changes neither their validity nor the physical unit set.

At a nonpositive pool C=2a, source nonpositivity gives q_j<=C. With nonempty history, q_j is at most every source ceiling and hence their minimum. Therefore q_j<=r=min(C,c_min). With empty history r=C and the same inequality holds. Its own q_j demands can always use the first q_j units of the reserved prefix; unused reserved units remain unavailable for loans. Only the suffix[r,C) is lendable and is retired after one visit.

UH01 specifies the additional facts needed for membership: at each delayed KEEP5 the minimum is exactly1, so the suffix contains a real unit and the debt induction clears every complete triple. It proves the uniform statements by source identities and induction, not by assuming a successful cut or by substituting the actual future q into a reservation. All passes start empty and use one period; no source fact or capacity from a startup or another lap is introduced.

The inherited inequalities are sound on arbitrary source spans but do not assert that every closed walk has a successful cut. The new theorem is restricted to H_m,m>=5; universal Coarse-Double remains OPEN.
