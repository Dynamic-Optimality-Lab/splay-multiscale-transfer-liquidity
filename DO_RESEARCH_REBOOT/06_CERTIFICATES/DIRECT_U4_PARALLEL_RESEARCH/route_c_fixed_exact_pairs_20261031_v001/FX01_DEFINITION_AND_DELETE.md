# Fixing exact common subtree pairs retains DELETE

There is an explicit repair of E that satisfies all three named acceptance requirements: universal DELETE, full q on opposite vines and both established arbitrary-fringe helper branches. It is not a universal source potential: FX04 gives a different valid B consumer where it fails.

## One function on every finite pair

Let C0(T) be the exact key sets of proper nonempty node-rooted subtrees of a finite ordered BST T. The full set is excluded and is matched to itself implicitly. For n>=1 each side has n-1 distinct sets. As in E, join I on the A side to J on the B side when

    min(I)=min(J) OR max(I)=max(J).

This compares minimum with minimum and maximum with maximum. Let

    S=C0(A) intersection C0(B), c=|S|.

Require every exact edge I--I for I in S to be in the matching. These edges are disjoint and always exist. Remove their vertices from both sides, and let mu be the maximum cardinality of a matching in the remaining endpoint graph. Define

    K(A,B)=c+mu,
    Ehat(A,B)=(n-1)-K(A,B).

K is the largest cardinality of a matching containing ALL exact common pairs. The residual maximum is a completely determined finite current-state operation, not an unknown potential label or future-excess oracle. For n=0 set Ehat=0. For n=1, C0 is empty and Ehat=0.

Writing nu for the unconstrained cardinality used by E, the inequalities c<=K<=nu give

    E<=Ehat<=F,
    Ehat-E>=0.

This is an explicit nonlinear repair to E. No transition law follows merely from those pointwise comparisons. Its source laws are proved below and in FX02-FX03. Equal subtree sets mean equal key sets, even if their root labels or internal shapes differ.

## A constrained rematching argument

A primitive A rotation replaces precisely one proper subtree set J by one different set K0, retaining all other sets and the full set. In the endpoint graph it replaces one left vertex. Let M be an old optimal matching with all old exact pairs fixed.

First delete M's edge at J, if present; at most one edge is lost. All old exact pairs except possibly J--J remain intact. If the added left set K0 is not present in C0(B), no new exact requirement arises, so this remaining matching is already feasible at the destination.

If K0 is present in C0(B), add the required edge K0--K0. If its right endpoint was already matched, remove that one old edge first. The removed edge cannot be an unchanged required exact pair: it would have had left vertex K0, which was not in the old A collection. Removing that edge and inserting K0--K0 has net cardinality at least zero. No other required exact edge is disturbed.

Thus K_new>=K_old-1. Apply the same construction to the inverse rotation to obtain K_old>=K_new-1. Therefore

    |Ehat(A_new,B)-Ehat(A_old,B)|<=1.                    (1)

This argument controls the changing exact-match constraints; it does not incorrectly treat them as a fixed feasible set.

An actual present-key source splay uses exactly d_A(x) primitive rotations: two per double and one for the optional final zig. Summing (1) proves

    Delta_DELETE Ehat<=d_A(x)<=2 ceil(d_A(x)/2)=2a.       (2)

The proof holds for every finite same-key pair, all fringe shapes and both orientations. If d_A=0 the tree and value are unchanged. DELETE here omits an occurrence from B, not a BST node.

Reversing key order and swapping children exchanges minima with maxima, preserves all forced exact pairs and preserves residual matchings. Thus Ehat is invariant under reflection. Relabeling any finite ordered key set by ranks also preserves the function and source operations.

## Scope of the successful repair

The old L-helper had E=1->2. Fixing exact pairs raises only its source among those two endpoints: Ehat=2->2. The correction Ehat-E therefore drops by one, restoring whole-helper compensation. FX03 proves this for arbitrary paired fringes, not merely the empty example.

The named whole-helper law must not be confused with universal B repayment after the A phase. Those are different source obligations. The function meets the three named tests but fails that larger obligation, as certified in FX04.
