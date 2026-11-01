# The root restricted matching reserve pays the named consumers

The same P pays all four registered starved KEEP consumers. It also inherits the established arbitrary-fringe whole-helper law and full opposite-vine repayment at every size. These partial results do not repair its universal DELETE failure.

## Four fixed actual source consumers

Every row has root(A)=x and a=0. Whole source repayment is therefore the B law on that row.

| Consumer | n | x | q | z | P before | P after | Required upper bound on change |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Old hook with A=1(empty,L_[2,6]), B=L6 | 6 | 1 | 2 | 1 | 5 | 2 | -2 |
| Padded hook from CR02 | 6 | 1 | 2 | 0 | 4 | 2 | -2 |
| Four-key crossing-transfer source from CT02 | 4 | 4 | 1 | 1 | 3 | 1 | -1 |
| A=L6, B=R6 | 6 | 6 | 2 | 1 | 5 | 2 | -2 |

These are the frozen source states, not newly enlarged tests. Their complete interval graphs, eligibility decisions, matchings and equal-size vertex covers are in [the certificate](root_matching_certificate.json). The independent verifier reconstructs every vertex and edge and checks the dual certificates without running a matching algorithm.

For the padded source, the three misleading nested endpoint matches all use B intervals containing root(A)=1. They are now ineligible. P_source=F_source=4. At the destination the common root makes P=Ehat=2. This pays q=2 exactly and avoids that consumer's earlier cap obstruction. For the four-key crossing-transfer source, P drops 3->1 even though the independent second-crossing count had stayed 1->1. Thus the new mechanism passes the specific conflict-transfer failure, rather than inheriting its local counting argument.

The source states and earlier failures are documented in [CR02](../route_c_capped_residual_20261031_v001/CR02_MONOTONE_AGGREGATION_OBSTRUCTION.md) and [CT02](../route_c_crossing_threshold_20261031_v001/CT02_EXACT_REPAYMENT_OBSTRUCTION.md). Reflections of all four rows were checked with the same costs and values.

## Opposite vines for every size

Use A=L_n,B=R_n and KEEP n. At the source, every proper B interval contains n, so no right vertex is eligible and P_source=n-1. At the destination both roots are n, so P_destination=Ehat(L_n,S_n R_n). The pinned [all-size protected matching proof](../route_c_fixed_exact_pairs_20261031_v001/FX02_OPPOSITE_VINE_PROOF.md) gives

    P_destination=floor(n/2)-1,
    Delta P=-(q+1)<=-q, n>=2.

For n=1 the value and q are zero; empty trees have no present-key accesses. Reflection gives the opposite orientation. This is a uniform identity inherited through common-root equality, not an inference from the six-key row.

## Both established arbitrary-fringe helpers

In the helper family of [FX03](../route_c_fixed_exact_pairs_20261031_v001/FX03_ARBITRARY_FRINGE_HELPER_PROOF.md), the input roots of both trees are c6. After the whole KEEP c2, both roots are c2. The paired fringes U,V have arbitrary same-key shapes and arbitrary size, including size zero. Common-root equality gives P=Ehat at BOTH whole-access endpoints.

Consequently the exact Ehat helper calculation transfers directly to this same P:

    branch L: Delta P=0,
    branch R: Delta P in {-2,-1}.

These whole accesses have a=1,q=2 and budget 2a-q=0, so both are paid, uniformly in the fringe and after reflection. This does not prove a bound for the separate A phase, nor the full B q-law on arbitrary source pairs. No additional helper samples or fringe-size fits were run.

All formulas above concern one function P. They do not splice different potentials across edge classes. A closed walk using only proved whole-edge classes telescopes for P, but no claim is made that these classes cover original CD. The original full obligation remains open because RS03 refutes the missing DELETE condition.
