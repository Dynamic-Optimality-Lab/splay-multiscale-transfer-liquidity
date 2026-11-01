# Exact pair constraints preserve both arbitrary fringe helpers

For the established helper family, the repaired potential Ehat has exact whole-access change zero on branch L and change either -2 or -1 on branch R. These bounds hold for every fringe cardinality and arbitrary same-key internal shapes U,V, including the empty fringe and reflections. Both branches have a=1,q=2 and budget zero.

## Source family and unchanged fringe data

Use ordered core keys c1<...<c6 and arbitrary BSTs U,V on the same m keys strictly between c4 and c5. The source A is

    A=c6(c2(c1,c3(empty,c4(empty,c5(U,empty)))),empty).

B has outer skeleton c6.left=c5, c5.left=c4 and c4.right=V. On branch L, c4.left=c1(empty,c2(empty,c3)); on branch R, c4.left=c3(c2(c1,empty),empty). All omitted children are empty. KEEP c2 uses one A zig and two B doubles. The exact outputs are

    A'=c2(c1,c6(c3(empty,c4(empty,c5(U,empty))),empty)),
    B'_L=c2(c1,c5(c4(c3,V),c6)),
    B'_R=c2(c1,c5(c3(empty,c4(empty,V)),c6)).

These source shapes and costs are inherited from RA02_ZERO_HELPER_ARBITRARY_FRINGE_PROOF.md and checked directly here for the core endpoint tables. No access enters U or V. Every internal subtree key set of U or V is retained, even if its absolute depth changes.

Let c_int be the number of exact common sets in C(U) intersection C(V), using ALL nonempty fringe subtrees. The entire fringe set, when nonempty, is among them. All c_int pairs are fixed at both endpoints and can be removed. Let D be the unchanged endpoint graph on the remaining k=m-c_int vertices per side. This is an explicitly determined graph for the present U,V, not an unknown label or a new assumption.

For m>0 put l=min(fringe), h=max(fringe). Define two extra vertices:

* L is a LEFT vertex adjacent to interior RIGHT vertices whose minimum is l.
* H is a RIGHT vertex adjacent to interior LEFT vertices whose maximum is h.

There is no L--H edge. Let mu_L be the maximum matching rank of D+L and mu_LH that of D+L+H. For m=0, D is empty and both boundary vertices are isolated, so both ranks are zero. These definitions also handle l=h.

## Two elementary matching facts

If one endpoint of an edge has degree one, some maximum matching contains that edge. If it is absent, that endpoint is unmatched; swap the edge at its neighbor for this edge, or add it if the neighbor is unmatched. Cardinality does not fall. Therefore such private edges may be fixed and removed when computing rank.

Adding one right vertex cannot lower matching rank, and can raise it by at most one: remove the added vertex's matched edge from any new maximum to obtain an old matching. Thus, for EVERY finite graph D and these arbitrary boundary neighborhoods,

    0<=mu_LH-mu_L<=1.                                  (7)

No feasibility theorem, compatibility assumption or fringe-size estimate enters (7).

## Core reduction table

Intervals mean complete key sets between their endpoints in the common ordered key set, including fringe keys when applicable. The exact common CORE sets fixed at the endpoints are:

| State | Forced common core sets | Additional private matching edges | Remaining kernel | Total protected rank K |
| --- | --- | --- | --- | --- |
| L before | [c1,c5] | 2 | D+L+H | c_int+3+mu_LH |
| L after | {c1}, [c3,c6] | 1 | D+L+H | c_int+3+mu_LH |
| R before | {c1}, [c1,c5] | 0 | D+L+H | c_int+2+mu_LH |
| R after | {c1}, [c3,c6] | 2 | D+L | c_int+4+mu_L |

No common set is counted twice: any core subtree contains a core key outside the fringe, so it cannot equal a fringe-only set. The full global key set is excluded throughout. There are m+5 proper vertices on each side, before and after.

Here is the explicit graph cancellation behind the table. After the forced core pairs are removed:

* L before has private edges A{c1}--B[c1,c3] and A[c3,c5]--B{c3}. In each case the B endpoint has no other neighbor, including in the fringe. Fixing them leaves only isolated core vertices and the boundary vertices A[l,c5] and B[c1,h], with the L and H neighborhoods above.
* L after has private edge A[c3,c5]--B{c3}, again with a private B endpoint. The remaining boundary vertices are A[l,c5] and B[c3,h], with exactly the SAME L and H neighborhoods. Other residual core vertices are isolated.
* R before has no residual core-core edges. A[l,c5] and B[c1,h] are the only vertices meeting the interior, giving D+L+H.
* R after has private edges A[c3,c5]--B[c3,h] and A[c4,c5]--B[c4,h]. The two A endpoints each have exactly one neighbor and no fringe neighbor. Both can be fixed without loss of maximum rank. This removes the two H-type B vertices; only A[l,c5], the L port, remains attached to D. The last core B vertex is isolated.

When the fringe is empty, replace l by c5 and h by c4 in the core intervals, and regard the two boundary vertices as isolated. The listed private edges and common pairs remain valid. When l=h, minimum and maximum are still compared in their own coordinates; no extra core edge arises. Thus the same reductions cover every permitted fringe.

helper_boundary_certificate.json lists all five proper core vertices per side, forced pairs, private endpoints and boundary neighborhoods. The independent verifier checks these symbolic reductions for distinct extrema, coincident extrema and the empty substitution. Actual source controls verify the endpoint tables. This is a finite symbolic core identity valid for arbitrary D, not a fit over finite U,V.

## Whole access compensation

The first two table rows have equal K and the same total node count. Therefore

    Delta_KEEP Ehat_L=0.                                (8)

For branch R, (7) and the last two rows give

    Delta_KEEP Ehat_R=-(2+mu_L-mu_LH)
                    =-2+(mu_LH-mu_L) in {-2,-1}.        (9)

Both are at most the original budget 2a-q=0. No assumption that U=V, no bound on m and no particular internal fringe shape was used. Reflection preserves source splays, exact pairs and the min/max endpoint graph, so the reflected family has the same values.

The fixed empty and singleton controls have L:2->2 and R:3->1. Those numbers check the wiring; equations (7)-(9) prove the arbitrary-fringe assertion.

## Scope of the compensation

This is a WHOLE helper law. It does not say that its B phase alone pays q. Indeed the L control has Ehat=2 after A and still 2 after B. If A has already been moved to that accessed root by a separate DELETE, the resulting starved KEEP is a different source obligation. Universal B repayment is not inherited from (8). FX04 gives an independently registered, fully closed safeguard counterexample to that universal claim.
