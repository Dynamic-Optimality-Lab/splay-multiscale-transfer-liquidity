# The guards create an additional old-UD coupling barrier

Status: PROVED—RESTRICTED DOMAIN for the guarded B order and arbitrary A-only insertions on a closed actual pair walk, with the stated KEEP-less funding condition. This scope audit prevents the successful B-only budget from being misrepresented as an FI-only reset construction. No A policy is executed here.

## Guaranteed physical guard capacity

Consider any actual closed A/B source word whose B KEEP sequence is GB02's query/guard cycle, or a positive power, with arbitrary A-only DELETE requests inserted. All query keys differ from the guard r=13. A query block and its following guard block are distinct A-root blocks, each with a positive-cost leader a>=1. If a KEEP is starved at the request level, its earlier DELETE leader supplies that same block's cost; it does not eliminate the leader pool.

B is rooted at r immediately before every query. Immediately after the query, r has depth one or two, and the following KEEP r has q_r<=1. Intervening DELETEs do not change B. For a POSITIVE query block, the old UD historical source fact for the former root r therefore gives the guard's exact own-work ceiling

    c_query(guard)=floor(h_query(r)/2)=q_r.

This fact remains retained even if earlier DELETE pools have already paid the query. Every other valid fact bounds the same q_r from above, so their minimum cannot invalidate it. The guard pool's capacity is at least two; after its one own-work reservation, its available suffix has at least

    s=2-q_r>=1                              (1)

distinct actual units. It can pay current or older pending demands without reusing a unit. Guard pools are distinct from query-local pools and from KEEP-less DELETE pools; the guard's block contains a KEEP and is never also counted in C_D.

## A total-debt cell argument

Partition cyclic A-root blocks into cells beginning at each query's positive-cost leader and ending just before the next query leader. Each cell has one query, its following guard, and any inserted KEEP-less blocks. Let

    e_i=max(q_x-2a_x,0),
    D_i=sum of actual KEEP-less capacities in cell i.

Every pending arrival in that cell occurs at its query; later source blocks in the cell are nonpositive. If e_i>0, the retained query fact guarantees guard service s_i=2-q_r by (1). If e_i=0, put s_i=0 in the comparison; we do not assume a fresh query fact exists. Pure DELETE service is D_i. Old UD may lend more from other pools, which only helps.

For incoming total debt X, its outgoing debt is at most

    max(0,X+e_i-s_i-D_i)
      <=max(0,X+rho_i-D_i),
    rho_i=max(e_i-s_i,0).                     (2)

The bound remains sound when early capacity is unused: all positive arrivals are already present before cell service, no later positive arrives inside the cell, and unused units are retired. No credit is banked for future cells. The old greedy algorithm can pay an older anchor rather than the current one; only total debt is compared, so no private-recipient assumption is needed.

When e_i>0, a_x>=1 gives

    rho_i<=max(q_x-2-(2-q_r),0)
          =max(q_x+q_r-4,0).

When e_i=0, rho_i=0 and the same upper bound holds. Define the source-only residual upper budget

    H_B=sum_(query/guard pairs) max(q_x+q_r-4,0). (3)

If C_D=sum D_i>=H_B, a minimum-cumulative-sum cut on the scalar cell values rho_i-D_i makes the comparison queue finish at zero, by the already established cyclic queue lemma. Choosing the actual block cut at that query leader is valid; every cell includes its own guard within the one-period proof. Induction in (2) then makes the actual old-UD debt zero as well. Thus

    C_D>=H_B implies an old-UD accepted cut.   (4)

All guaranteed capacity in this argument belongs to explicit actual source pools. Every residual cursor is monotone. Guard own-work prefixes, outgoing suffixes and separate DELETE pools are disjoint. The comparison quantities H_B and rho_i bound demand; neither creates a new physical credit. No reachability-prefix, second-lap or alternative-cut unit is used.

## Evaluation on the certified cycle

For GB02's twelve pairs, all q_x+q_r<=4 except the final query 8 and return 13, where q_x+q_r=4+1=5. Therefore

    H_B=1 per certified primitive B cycle.

The existing independently verified B rows supply these numbers; guard_repayment_profile.json records the calculation without any new source requests. Two pure one-StepEv resets would have C_D=4, so (4) guarantees old-UD membership. For p complete B cycles, H_B=p and two such resets PER cycle provide 4p, giving the same conclusion. More expensive or additional KEEP-less blocks cannot help strictness on this family.

This does not refute arbitrary guarded cycles, arbitrary B orders or couplings with less KEEP-less capacity. In particular, syntactic DELETEs completed by KEEP of the same key are not automatically pure C_D pools; the stated obstruction counts actual KEEP-less leader blocks. Nor does it refute FI-only existence elsewhere.

## Meaning for this turn

The requested primitive B cycle with G_B>=5 is genuinely constructed: G_B=9, no period padding and no larger finite fit. It removes the raw B-budget obstruction. Its guard architecture simultaneously gives old UD useful immediate payers, leaving only one unit of residual upper budget. Direct insertion of two pure resets on this same order cannot establish the ultimate strictness target.

The A-reset placement and FI-only source walk are not being silently assumed. No new A search or second open theorem was delegated. This is a direct no-reuse corollary of the same guard identity and existing cyclic queue proof, recorded to make the successful component's scope accurate. Universal Step 3/CD remains OPEN; matching-terminal work and Stage 11G are unchanged.
