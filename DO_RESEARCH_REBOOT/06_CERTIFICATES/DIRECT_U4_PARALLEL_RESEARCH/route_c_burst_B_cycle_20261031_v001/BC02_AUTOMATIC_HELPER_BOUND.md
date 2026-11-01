# The automatic immediate-helper bound and its limitation

Status: PROVED—RESTRICTED DOMAIN. The domain is an actual finite closed A/B source walk whose adjacent cyclic KEEP keys differ, with arbitrary A-only DELETE insertions. This is a sufficient old-UD coverage bound, not a characterization of UD coverage. It generalizes the already proved guard-pair argument without introducing an allocation optimizer or a new potential.

## Actual pools and source facts

Use the established maximal cyclic A-root blocks. Each leader has a>=1 actual grouped A events, hence C=2a distinct physical units. A block has at most one genuine B-changing KEEP. The differing adjacent KEEP keys ensure the KEEP occurrences here belong to distinct A-root blocks. A KEEP syntactically following DELETE of the same key still belongs to that DELETE leader's pool; starvation does not remove the pool.

At a positive block q>C, pay its own first C B doubles locally and create excess e=q-C. Such a block requires q>=3. UD retains its post-B depth fact for every key even after that anchor is paid. For a later KEEP block with no intervening B change, the fresh fact is the exact ceiling c=q_later. At a nonpositive block UD reserves min(C,c_min) once, then lends its one unreserved suffix to pending demand. Facts combine by minimum, never by adding capacities. A KEEP-less block has c=0 and can lend its whole C if history and debt are present.

## Disjoint high/low pairs

From the cyclic B word form every adjacent pair (i,j=i+1) with q_i>=3 and q_j<=1. Such pairs cannot overlap: a low endpoint cannot be another high start, and each cyclic position has one predecessor. Intervening DELETEs leave B fixed.

If i is actually positive, its fresh fact gives c_i(j)=q_j. The helper has C_j>=2 and q_j<=1, so is nonpositive and guarantees at least s=2-q_j units of service. This holds even if the anchor was paid before the helper, because its fact remains retained. Allocation to older debt instead of i does not reduce total service. If i is nonpositive, this cell has no positive arrival, and we require no helper service.

Treat each paired occurrence as one cell; every unpaired KEEP is a singleton cell. A cell begins at its first KEEP block's positive-cost leader and ends just before the next cell leader, including all KEEP-less blocks in between. Its only possible positive arrival is at its first KEEP block. No pure service in the cell precedes that leader. Let D be its actual KEEP-less capacity, X its incoming debt, and e its possible positive excess. For a paired cell set s=2-q_j if e>0, and s=0 otherwise. The actual outgoing UD debt is at most

    max(0,X+e-s-D) <= max(0,X+rho-D),
    rho=max(e-s,0) <= max(q_i+q_j-4,0).

For a singleton, ignore all service from its KEEP pool and use rho=e<=max(q_i-2,0). For e=0 the corresponding rho is zero. No capacity is saved for future cells; unused suffix units are retired. The displayed recurrence is a comparison of total outstanding debt, not a promise to pay a named anchor from a private helper.

Define the source-only budget

    J_B = sum_(high/low pairs) max(q_i+q_j-4,0)
          + sum_(unpaired i) max(q_i-2,0).

It satisfies 0<=J_B<=G_B. Let C_D be total actual capacity of KEEP-less A-root blocks. If C_D>=J_B then the actual cell values v=rho-D have nonpositive sum. Cut after a minimum cumulative sum of these values. For the rotated list the final cumulative sum is a minimum, so every suffix sum is nonpositive and the reflected queue recurrence finishes at zero. The physical cut is at the following cell's A-root leader. A debt induction using the displayed bound gives an old-UD accepted cut within this one period.

Thus

    C_D>=J_B  implies  an old-UD accepted cut.

The cut direction is MINIMUM, as corrected in the earlier CW audit. This proof uses each physical pool once. Local own-work prefixes, helper suffixes and KEEP-less pools are pairwise disjoint; loan cursors and demand cursors only advance. It borrows no prefix unit, later-lap unit or alternative-cut unit. Empty positive sets pay locally; q=0 helpers still count as B changes in other history bounds. Source reflection preserves every count.

## Applying it to the explicit cycle

The only q>=3 positions have costs 6 and 3, followed by 3 and 2. There are no high/low pairs. Hence

    J_B=G_B=(6-2)+(3-2)=5.

The earlier guarded word had G_B=9 but guard residual budget H_B=1. The present word leaves five in this immediate-helper comparison. A proposed two-PURE-one-StepEv reset budget is C_D=4, so C_D>=J_B is false here. This automatic sufficient proof no longer forces UD membership.

Failure of a sufficient condition is not proof of rejection. J_B bounds possible residual demand; it is not an actual debt count, a new pool or an exact optimized repayment value. Extra A capacity, additional positive facts, delayed service or forced A geometry may still establish UD membership. BC03 audits the delayed source facts without assuming a realizable low-cost A trajectory. The actual reset placement, E>C_D and all-cut UD rejection remain OPEN.
