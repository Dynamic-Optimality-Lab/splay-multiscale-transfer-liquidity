# Whole source B repayment fails at four keys

The second-crossing potential obeys DELETE uniformly, but a legal starved KEEP has no potential decrease despite q=1. Three fixed sources also refute every constant positive-integer crossing threshold. These results reject the specified candidates, not Coarse-Double.

## The principal actual source access

Write empty children as empty. On keys 1,2,3,4 let

    A=4(2(1,3),empty),
    B=1(empty,2(empty,3(empty,4))).

KEEP 4 has root(A)=4. The A phase is a no-op: a=0. In B, key 4 has depth three. The exact source events are RR on keys 2,3,4, followed by a right-oriented ZIG on keys 1,4. Hence q=1,z=1. The B destination is

    B'=4(1(empty,3(2,empty)),empty).

The proper intervals of B are [2,4],[3,4],{4}; those of B' are [1,3],{2},[2,3]. A is unchanged. The complete degrees are

| A interval | Crossing B intervals | Degree before | Crossing B' intervals | Degree after |
| --- | --- | --- | --- | --- |
| {1} | [2,4] | 1 | {2},[2,3] | 2 |
| [1,3] | [2,4],[3,4],{4} | 3 | none | 0 |
| {3} | {4} | 1 | {2} | 1 |

Thus H2=1 before and H2=1 after. The counted feature at [1,3] disappears, but a new counted feature at {1} replaces it. Precisely,

    Delta_KEEP H2 = 0 > -1 = 2a-q.

This is a failure of the requested whole-access source law with access-root alignment already present. It is not merely a failed per-double sufficient condition, nor a root-changing DELETE problem. The same operation reflected in key order gives the other orientation. The [certificate](crossing_certificate.json) contains every interval, crossing edge, physical endpoint and oriented event, independently verified in [audit](independent_audit.json).

## Reachability and exact closed paired replay

Start both trees at T0=R4, the right vine. The three DELETE accesses

    D4 D2 D4

transform A to the displayed A while B remains R4. The source four-key single-tree search visits all 14 shapes to locate this connector; it assigns no potential labels and builds no pair graph. The connector is also directly replayed by both source engines.

The complete closed word is

    D4 D2 D4 K4 K1 K2 K3 K4 K3 K2 K1.

The failed K4 is at zero-based position 3. Common ascending accesses 1,2,3,4 synchronize both trees at L4; descending accesses 3,2,1 return both to R4. Physical replay gives

    A_total=12, Q_B=2, Z_B=8.

The final actual A tree and actual B tree equal their initial trees. Summed H2 changes are exactly zero. This walk satisfies Q_B=2<=24=2A_total; it is explicitly not a Coarse-Double counterexample.

## Direct corollary for every fixed threshold

Consider the same formula Hk with one fixed positive integer k, independent of n. The principal witness handles k=2. The gate registered two further opposite-vine accesses, and no threshold was fitted or selected.

| Fixed threshold class | Registered actual source | A proper-interval crossing degrees before | Degrees after | Required change |
| --- | --- | --- | --- | --- |
| k=1 | A=L6,B=R6, KEEP 6 | 1,2,3,4,5 | 2,1,3,2,0 | <=-2 |
| k=2 | Principal four-key KEEP 4 | 1,3,1 | 2,0,1 | <=-1 |
| k>=3 | A=L3,B=R3, KEEP 3 | 1,2 | 0,0 | <=-1 |

For k=1 the value changes 5->4, underpaying q=2. For k=2 the value changes 1->1, underpaying q=1. For every k>=3 the three-key source and destination both have value zero, underpaying q=1. Every row has a=0 and satisfies root(A)=x. These three cases exhaust the fixed positive integers. The opposite-vine states are reachable from the diagonal R_n by DELETE 2,3,...,n; each is a root-child zig. Reflection preserves all values and costs.

Therefore no constant threshold Hk is a universal source potential. The k=1 result overlaps the already known exact-disagreement failure on this control; it is not presented as independent new full-proof progress. The second-crossing transfer and the class partition are the additional audit content.

The result does not exclude thresholds depending on n, weighted crossing profiles, globally coupled incidence functions, or other structural potentials. No such successor is constructed or assumed here. In particular the case partition must not be read as proving failure for an arbitrary sequence k_n: its three witnesses have different sizes.

## Verification scope

The producer compares both existing source engines. The independent verifier uses the pointer engine without importing the producer; reconstructs all proper intervals; checks crossings by strict endpoint membership with distinct endpoints; recomputes H1,H2,H3; verifies the all-k>=3 argument by the maximum source degree; and checks actual source-state sharing, present-key counts, reflection, the 11-access paired closure and totals. It verifies 17 source rows including reflected controls and 525 chord comparisons counted with repeated endpoint evaluations. Universal DELETE is an analytic proof in CT01, not inferred from those finite checks.
