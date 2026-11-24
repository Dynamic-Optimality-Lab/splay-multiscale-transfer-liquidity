# Proved bounded-fringe payment; full M1 OPEN

This document proves a scoped payment on arbitrary sources. It does not assert the full required R_C<=c_1 A+X interface.

## Theorem and exact eligible class

Fix r>=1 and s_r=2^r-1. For each original C vertex v at KEEP h, measure ell(v) along actual pre-A parent pointers to the original target path P_A(h), as in THEOREM_TARGET. Let V_C^{<=r} contain all such physical vertices with ell<=r, before inspecting gap weights. Then

\[
|V_C^{\le r}|\le4s_r A,\qquad R_{C,\le r}\le12s_r A.
\]

All real keys and fringe components are counted. The result is independent of their population, source length and chain height.

## Part1: attachment at a strict path ancestor

For v, let z be the first path vertex reached while following A parents from g(v). Suppose z is a strict ancestor of x_h. Its path-following child is fixed by the search, leaving at most one off-path child. Within distance r of z in that off-path branch there are at most

\[
1+2+\cdots+2^{r-1}=s_r
\]

physical nodes. Distinct old grandparents within a B access are distinct, so at most s_r eligible C parents have this attachment z. An ordinary A splay demotes each original strict ancestor exactly once; select that actual primitive pivot z in operation h. It receives at most s_r parents, hence at most3s_r original residual gaps. Different z/operations have different actual bit IDs. A StepEv has at most two real bits, so this part costs at most6s_r A in gap weight. A terminal zig supplies its one real bit; no companion is supplied.

## Part2: attachment at the target

If z=x_h, there are at most two off-path child branches and hence2s_r eligible grandparent keys within distance r. Pay their gaps with the first actual cost-one A StepEv in the **original incoming cyclic KEEP gap G_h**.

That StepEv exists whenever such a C vertex exists: B is nonidentity at h, so its target differs from the previous KEEP root. A was rooted at that previous target just after the previous KEEP and ends at x_h. The intervening KEEP/DELETE original requests therefore contain positive measured A work. The argument also handles a zero-cost A access at h itself, using its real DELETE helpers. Root repeats with no B double make no demand. With no KEEP there is no demand; a single repeated KEEP target in a closed B period is a B identity.

The G_h partition original operation positions and actual A StepEv cyclically. Each selected StepEv belongs to just one such gap and receives at most2s_r parents or6s_r gap occurrences from this part. No reaching prefix is used. This part therefore costs at most6s_r A.

## Global composition

Every eligible C parent has exactly one nearest attachment and falls in exactly one part. A StepEv may receive both parts: at most two real pivot bits times s_r parents in Part1, and at most2s_r parents in Part2. Its total parent load is at most4s_r, or12s_r gap slots. This explicitly counts all possible reuse rather than assuming chains or components disjoint.

The map applies to every physical C vertex, not just the tested or Pi-qualified ones. Restricting its demands to literal original overflow gaps cannot increase load. Each such gap stays with its unique original consuming parent; at most three per parent by the original theorem. Thus the gap bound follows with no reclassification, new adjacency or quota refill.

## Radius2 and literal complement

With r=2, s_r=3. The original near class has a36A budget. Let R_{C,>2} be the exact original complement by ell>2. Then

\[
R_C=R_{C,\le2}+R_{C,>2}\le36A+R_{C,>2}.
\]

This is a scoped decomposition, **not a completed M1 theorem with X:=R_{C,>2}**. No physical restoration transfer or absolute price for that complement is proved. If every positive-weight C parent in a source has ell<=2, the direct full same-column bound R_C<=36A holds on that precisely named source class. Deep physical C vertices and deep prehybrid R_* consumers exist; they are not excluded by the theorem.

## IAGS proof box

Target: pay literal C gaps at physical fringe distance<=r. Conditions: one original C old grandparent per key per KEEP, actual strict-ancestor demotions, positive real incoming A gap for a B double. Inheritance: M0's source/IDs, C no-reset geometry and original three slots. Ambiguity resolved: multiple chains can share A work; the combined bound is4s_r parents per actual StepEv, not injectivity. Bridge: sum the explicit original-StepEv load and multiply by the three-slot bound. This closes the scoped branch only.
