# The full directed-distance cone: DELETE proved, KEEP obstructed

Use the actual event-weighted preparation distance ell from
DIRECTED_SOURCE_DISTANCE_DELETE_LEMMA.md. For fixed alpha>=0, beta<=0,
alpha-beta<=2, put Phi=alpha*ell(A,B)+beta*ell(B,A). The two directed
triangle inequalities give, for an actual A-only access of cost a,

    Delta ell(A,B)>=-a,   Delta ell(B,A)<=a,
    2a+Delta Phi >= (2-alpha+beta)*a >= 0.

This is a uniform proof for all physical key sets of size>=4 and arbitrary
private populations. The zero-event identity has a=0 and DeltaPhi=0.
It imports no numeric external cost bound and allocates no hypothetical
preparation unit. The lambda family is alpha=2lambda,beta=-2(1-lambda).

The candidate source packet in directed_source_distance_closed_sources.json
has H1,Q3, so price-1. Its exact directed distances change

    ell(A,B):11->8;   ell(B,A):7->10.

Hence its margin is -1-3(alpha-beta)<0 for EVERY alpha>=0,beta<=0,
including the entire DELETE-safe cone above. For the lambda family the
margin is exactly-7, independently of lambda. This is a necessary KEEP /
natural-packet obstruction, not failure of the DELETE theorem.

A second original packet has H1,Q3 and keeps both directed distances
unchanged at(8,6). It rules out any fixed debt depending ONLY on those
two numbers. It does not rule out additional root/chart/geometry inputs.

These conclusions are promoted only by the separate independent receipt
checking the complete seven-key ordinary primitive graph, exact shortest-
path lower/upper labels and the original closed source histories. Existing
source proofs and owner maps are untouched. No actual negative full-state
cycle or Coarse-Double counterexample is asserted. Source grouping or a
different sufficient invariant remains possible; C33 remains OPEN.
