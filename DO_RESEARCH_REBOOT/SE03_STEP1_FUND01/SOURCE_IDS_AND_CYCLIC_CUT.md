# Actual occurrence identities at the maximum-debt cut

The allocation is cyclic with a legal chosen source seam. It does not
claim zero-start online funding from an arbitrary fixed input timestamp.

Let the already recurrent aligned period be I=[a,a+T), T=LN. Macro
boundaries have offsets within this period. Choose the earliest boundary
with maximum actual ordinary debt and offset delta. Use the ACTUAL source
interval I'=[a+delta,a+delta+T). Both histories are periodic on this length:
the full history has period N dividing T, the erased history has period T,
and their A histories agree. Thus both full endpoint pairs close on I'.

For an occurrence at absolute time t in the original I, its unique
corresponding occurrence in I' is

    t'=t, if t>=a+delta;
    t'=t+T, if t<a+delta.                                  (1)

All source A trees, StepEv cases and local event indices agree at these
periodic copies. Give the selected ACTUAL occurrence in I' the ID
(absolute_time=t', local_StepEv_index, bit=0/1). If retaining original
word-copy labels, t' uniquely determines those labels and the original
occurrence index. Erasure preserves A, so the full and auxiliary A event
IDs in I' coincide. Auxiliary B-double IDs additionally include the
auxiliary history tag and actual local B-double index.

Equation(1) is a bijection of ONE period's source positions onto ONE
period's positions at the new seam. It is not permission to spend both
t and t+T, and no source unit outside I' enters the allocation. All
t'>=a are beyond the erased preperiod. The reaching prefix, including
the shift to the chosen seam, is never a funding pool. Every event
is selected at most once with its actual timestamp in I'.

Costs and signed marginal over I and I' agree, because they are cyclic
sums over a full common period. Divide all such totals by the SAME L
only after constructing the integer-unit allocation on I'. No fractional
physical unit or unmatched transient is introduced by normalization.

source_allocation.py accepts an ALREADY ROTATED actual source record
whose initial debt is maximal. It never silently reorders absolute IDs.
Its canonical_cut helper only identifies a boundary; preparing the actual
rotated record must use the source bijection above. This avoids treating
a numerical permutation of timestamps as a causal physical allocation.

The auxiliary prefix to I' remains a legal original Pair Access history
from its own diagonal. The full prefix to I' is legal in the full history.
Their beginning B trees need not agree. Reachability and source closure
are inherited actual properties, not inferred from equal debt values.
