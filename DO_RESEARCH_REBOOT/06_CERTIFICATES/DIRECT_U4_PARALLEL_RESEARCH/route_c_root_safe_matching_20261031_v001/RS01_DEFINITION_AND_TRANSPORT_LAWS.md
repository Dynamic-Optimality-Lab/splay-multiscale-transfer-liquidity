# A global matching reserve restricted by the A root

The explicit reserve below gives a global transport rule for matching credit during a B splay. It pays the registered conflict-transfer consumers, but a root-changing DELETE has unbounded positive drift. It therefore does not solve Step 3.

## One function of the current pair

Let A,B be BSTs on the same finite ordered key set. For n>=1 put r=root(A). Let C0(T) be the distinct proper nonempty node-rooted subtree key sets. Equivalently use their rank intervals; the full set is excluded. As in [the protected matching definition](../route_c_fixed_exact_pairs_20261031_v001/FX01_DEFINITION_AND_DELETE.md), put

    S=C0(A) intersection C0(B), c=|S|, F=n-1-c.

Force each exact pair I--I for I in S. Remove those vertices from both sides. Retain every remaining A interval, but retain a remaining B interval J only if r is not in J. Join the remaining I,J when their minima agree or their maxima agree. Let mu_r be the maximum cardinality of one matching in this entire residual graph. Define

    P(A,B)=F(A,B)-mu_r(A,B).

Every proper A subtree excludes r, so every exact common interval excludes r. All forced pairs are eligible and disjoint. Thus the definition is always feasible and finite. This is a global optimum within the current pair; it does not optimize over histories or assume the existence of potential labels. Multiple features cannot use the same matched vertex. For n=0 set P=0, and for n=1 the collections are empty and P=0.

If mu is the unrestricted residual rank defining Ehat, deleting right vertices gives mu_r<=mu. Therefore

    Ehat<=P<=F.

The function is not covered merely by the old scalar monotonicity result: it uses which residual B intervals contain the actual A root. The two six-key starved sources previously forced incompatible scalar values, whereas P assigns the padded source value 4 and the opposite-vine destination value 2, meeting their necessary order. No general information-theoretic independence claim is needed.

## Root-depth lower bound and common-root equality

The proper B subtrees containing r are exactly the nodes on its ancestor chain starting at r and stopping before the global B root. There are d_B(r) of them. Hence there are n-1-d_B(r) eligible B vertices in total, including the forced exact pairs. If K_r=c+mu_r is the total protected rank, then K_r<=n-1-d_B(r). It follows that

    P=n-1-K_r >= d_B(r).

When root(B)=r, no proper B interval contains r. The restriction removes nothing, so

    root(A)=root(B) implies P(A,B)=Ehat(A,B).

These statements hold for all sizes and arbitrary internal shapes. Increasing relabeling preserves the function. Key-order reflection exchanges minima/maxima and preserves membership of r, all matchings and P.

## Transport during B splay

Freeze A with root r and splay r in B. The [source interval identity](../route_c_clade_correction_20261031_v001/CC01_SOURCE_ROTATION_IDENTITY.md) proves that every primitive source rotation removes a proper B interval J containing r and inserts one interval K excluding r. This includes the first parent-over-grandparent rotation of a same-side double; it is not modeled as two rotations both promoting r.

The removed J was ineligible and cannot have been an exact common pair. Every old eligible right vertex and every old forced pair persists. If new K is not an A interval, add its right vertex without removing any old feasible matching edge. The total protected rank cannot fall.

If K is an A interval, force the new K--K pair. Its right vertex is new. Its left vertex may have been used by at most one old residual edge. Remove that edge if present and insert K--K. The net cardinality change is nonnegative, and no old forced pair is disturbed: K was not an old B interval, so it could not have been an old exact pair. The remaining matching stays feasible.

Thus K_r never decreases and P never increases at any primitive B rotation. Composing the actual source rotations proves universally on the root-conditioned domain

    P(A,S_r B)-P(A,B)<=0.

This weak transport law controls reassignment without double-counting credit. It does not imply the required <=-floor(d_B(r)/2). The full-q B law is not proved or refuted universally in this run. For d_B(r)=0 the operation is a no-op.

## A rotations that preserve the root

For a primitive A rotation preserving r, eligibility of B intervals is fixed. The source interval identity replaces one left interval J by K. Remove the old edge at J, losing at most one. If K becomes an exact pair, its eligible right vertex may be occupied by at most one old unforced edge; replacing that edge by K--K does not lose an additional unit. Unchanged forced exact pairs cannot be displaced. Apply the same argument to the inverse rotation. Therefore

    |P(A_after,B)-P(A_before,B)|<=1

for root-preserving primitive A rotations. This is a restricted structural law, not a universal DELETE law. A complete splay usually changes the A root. Its final root change can change the eligibility of many retained B intervals, and the proof above does not cover that transition. RS03 gives a single-zig failure of the desired full bound.

Source implementations are [tuple source](../../../../python/independent/splay.py) and [pointer source](../../../../python/liquidity/legacy_embedding.py), pinned in entry_source_pins.json. No source file was edited or Stage 11G code run.
