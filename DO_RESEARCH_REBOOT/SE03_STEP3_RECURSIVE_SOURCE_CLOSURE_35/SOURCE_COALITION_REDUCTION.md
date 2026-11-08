# Reduction rules with actual descent

## DELETE-LOOP35 — PROVED, source-level negative preservation

Target: eliminate a genuine class of source complexity from a hypothetical
negative countercut. Conditions: a nonempty contiguous subword J wholly
inside the actual period, consisting only of original DELETE operations,
whose initial and final FULL A trees are identical. The legal source cut
is outside J. Inheritance: DELETE is A-only, exact ordinary splaying and
C34 operation pools. Dual: a surviving state/birth/pool differs after the
reduction. Bridge: a negative cut survives on a strictly shorter source.

Construct a DIFFERENT source word W' by removing J; do not edit W or its
archived certificate. B/BE and charts were unchanged throughout J and
A returns exactly, so every remaining original operation has precisely
its old tree states and costs, under the order-preserving occurrence
bijection rho. Original closure and reachability from the same prefix
hold. All genuine KEEPs, support, maximal B core and genuine macro
boundaries survive. No physical BST key is deleted.

Last genuine g births are the same remaining occurrences. All endpoint
ancestry losses outside J are identical. Own inventories and retiring
operation pools therefore satisfy, for the corresponding coalition S',

    N_W'(S')=rho(N_W(S) \ union_{t in J} C_t),
    Q_W'(S')=Q_W(S),
    delta_W'(S')=delta_W(S)+|N_W(S) intersect union_{t in J}C_t|.

Consequently a positive deficit stays positive. Source length strictly
decreases, even for a zero-event DELETE identity. This is an explicit
new-source counterexample reduction, not dropping costs from a fixed
source or calling the deleted bits available to its donors. QED.

For a MOP/owner extension reduction, old a0/fE/Gamma identities must NOT
use a deleted bit or demand, and original retirement/transport licenses
must separately survive. No unconditional owner-preserving version is
claimed. ROOT35 is owner-independent, so the raw reduction is sufficient
at this layer. No existing map or source file is actually altered.

## Exact reconstruction into ROOT35

If any counterexample exists, choose one lexicographically minimal in
(|S|, number of original period operations), with either coordinate a
nonnegative integer. LPR/exterior/own-solvent inheritance excludes the
known classes; splitting disconnected neighborhoods selects a smaller
negative component. REM35 excludes a removable private-capacity macro.
DELETE-LOOP35 excludes every such DELETE loop. Each accepted reduction
strictly decreases the stated pair, so no infinite recursion is possible.

The remaining source must have a connected coalition, at least two
macros, an interior target, an excess macro, private capacities<Q for
EVERY selected macro, and no DELETE-only exact A return subword. These
are necessary source conditions, not an assertion that such a source
exists or that its deficit is positive.

The resulting irreducible-source compensation statement is still a
substantial unproved source theorem. Calling it a child does not prove
it. A reduction based only on negative-set minimality would be circular;
see PRIVATE_CAPACITY_RECURSION.md.
