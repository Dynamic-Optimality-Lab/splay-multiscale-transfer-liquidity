# Strict descent and the binary forest

Use the global construction in M0_FOREST_CONSTRUCTION. All subtree statements below hold on complete physical key sets, before restricting to the original S.

## Rotation monotonicity at one fixed key

For a primitive rotation with pivot a and promoted child b, only the rooted descendant sets at a and b change: a loses keys and b gains keys. Any middle component retains its complete internal subtree; only its attachment changes. Rotations below any other ancestor preserve that ancestor's total descendant set. Hence over an interval with no promotion of a fixed g, the descendant set rooted at g can only shrink. This assertion allows arbitrary intermediate destruction and recreation of other edges; it is not a monotone-ancestry assumption for the whole tree.

## Completed outputs

At a double r, the target x rises above its old grandparent g and old parent p. Both completed non-target outputs are contained in the pre-double frame and exclude x. For reference the complete local forms, with every letter a real intact component, are:

| Case | Before | After |
|---|---|---|
| RR | g(L,p(H,x(C,R))) | x(p(g(L,H),C),R) |
| LL | g(p(x(L,C),H),R) | x(L,p(C,g(H,R))) |
| LR | g(p(L,x(C,H)),R) | x(p(L,C),g(H,R)) |
| RL | g(L,p(x(C,H),R)) | x(g(L,C),p(H,R)) |

Later steps in the same access rotate x with ancestors above x. They may transport a completed output, but do not change it internally or insert x into it. Thus J_g(r) and P_p(r) are the same rooted output labels at the end of the full B phase. In LL/RR the old-grandparent chosen output is already completed at bit 0. For a P predecessor use the **old-parent output after bit 1**, not the intermediate subtree immediately after promoting the parent: that intermediate subtree still contains x and would not prove strictness.

## Edge proof

For a C child v, r=u(v). There is no promotion of g(v) in I(v). Immediately after r's B phase its subtree is J_g(r). Rotation monotonicity gives

\[
F(v)\subseteq J_g(r)\subsetneq F(r).
\]

For a P child v, the selected last promotion has g(v)=p(r), in bit 0 of r's LL/RR double. After bit 1 this key has subtree P_p(r). Higher steps preserve it, and by lastness there is no subsequent promotion of that key before v. Therefore

\[
F(v)\subseteq P_p(r)\subsetneq F(r).
\]

The strict containments remain strict on original S labels, since x(r) belongs to S and F(r), while both completed outputs exclude x(r). Thus this is not strictness supplied only by an unmarked hanger. Complete physical descendant sets satisfy the same inclusions. These arguments cover both orientations, opposite-side C predecessors, middle-subtree transport, and arbitrary intervening ancestry recreation.

## Well-foundedness across the seam

Each edge strictly decreases the finite positive integer |F|. A cycle on original vertex IDs, including one crossing the printed period seam, would give a strict inclusion of a finite labelled set into itself. This is impossible. In particular a singleton column with a preceding-lap copy of the same vertex cannot produce a C self-loop; its actual history must fall into another case. No chronological ordering of the printed word is being substituted for this argument.

Every nonroot has one predecessor, roots have none, and V is finite. A finite acyclic graph with this indegree rule is a disjoint union of rooted trees.

## Actual number of children

For a fixed vertex r, there is at most one C child: the next use of its own old-grandparent column in the **global all-double** cyclic list. It becomes a C child only if the reset and promotion tests both fail.

There is at most one P child: only bit 0 of r's LL/RR double can promote a non-target, namely its unique old parent. That one primitive belongs to at most one of the pairwise disjoint intervals for that physical key. If r is LR/RL it has no P role. A later promotion can prevent selection of r but cannot create a second recipient. This proves a bound on actual immediate children, not merely the existence of two names for roles.

The same child cannot occupy both roles because its class is unique. Hence outdegree is at most two. There is no resulting constant bound on height, total descendants, component size or weighted residual consumers. Sibling frames need not be disjoint. The pinned long-chain and overlapping-sibling examples remain valid obstructions to those stronger assertions.
