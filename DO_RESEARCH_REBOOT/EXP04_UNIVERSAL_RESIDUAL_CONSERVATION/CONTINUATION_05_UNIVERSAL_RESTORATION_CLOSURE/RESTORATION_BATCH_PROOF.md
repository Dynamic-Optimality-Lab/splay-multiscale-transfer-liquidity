# Cyclic restoration intervals and the last-promotion forest

## R1. Source-defined intervals, with one donor per selected occurrence

Choose any set T of original B double parents, for example the fixed
overflow parents, or **all** B doubles. For each physical old-grandparent
key g, order its T occurrences cyclically. A B splay demotes each original
strict ancestor once, so g occurs at most once as old grandparent in one
KEEP. For p in this column let u be its predecessor in the same column
(its preceding-lap copy when it is alone). Its interval is after the full
B phase of u through the actual post-A, pre-B boundary of p. These
intervals are disjoint in each column and lift at most one lap. Endpoint
consumer B phases are excluded. No source occurrence is duplicated at the
seam.

If there is a real A demotion of g in the interval, mark p as a reset and
take the last such bit. A bit has one pivot, so reset donors are distinct
over all columns. Otherwise g cannot be targeted in the interval: that
access would leave A rooted at g and the first later non-g request (at
latest p's target) would demote it. A strict A ancestor would also be
demoted. Hence g's complete A subtree stays internally rigid and all
targets avoid it. Its outer attachment may move.

A B primitive changes rooted descendant sets only at its pivot and
promoted node. The pivot loses descendants; the promoted node gains
descendants. On a no-A-reset interval, there are two useful **different**
selectors.

* Last actual gain: for p's target y, select the last B gain of \(g\to y\)
  in the interval if one exists. If none exists, the relation was true
  throughout, since it is true just before p. This also detects destruction
  and recreation of a relation that was true just after u.
* Last promotion: select the last B primitive promoting g, whether or not
  that bit adds y. If none exists, g's descendant set only shrinks, so the
  relation was true throughout. This is the selector used for the forest
  and optional refined payments. It is not called a gain unless it is one.

Either selected promotion is non-target, because a B access to g would
also be an A access to g and force a reset. Only the first bit of a
same-side double promotes a non-target. Its old parent is g. Each
restoring B double can be selected by at most one interval: it names one
g and that column's intervals are disjoint. This rules out double use of
the restoring occurrence even if it gains many individual relations.

## R2. Strict frame descent

Write F(p) for the original S label of the old grandparent immediately
before its double. Lower steps in the same splay preserve that ancestor's
full frame, so F(p) equals its pre-B S-subtree. Write \(x(p)\) for its
access target, which belongs to F(p).

For no-A-reset p:

* If no B promotion of g occurs, take predecessor r=u. After r's full
  B phase g has its completed grandparent output \(J_g(r)\).
  No intervening promotion of g means \(F(p)\subseteq J_g(r)\).
* Otherwise let r be the double of the last B promotion. Its old parent
  is g. After the second bit g has its completed parent output \(P_g(r)\),
  which persists through the remainder of r's splay. No further
  promotion of g means \(F(p)\subseteq P_g(r)\).

Both completed outputs are subsets of F(r) and exclude \(x(r)\);
\(x(r)\in S\cap F(r)\). Consequently
\[
F(p)\subsetneq F(r),\qquad x(p)\ne x(r).
\]
This proves strictness on the unchanged S labels, not just on an
unmarked physical hanger. The argument also holds on the complete
physical descendant sets. Every edge points causally forward on a
lift, and strict inclusion forbids a cycle among original occurrence
IDs even across the printed seam.

## R3. Forest covering every original B double

Take T to be **all** original B doubles, including nonneutral ones.
Every nonreset vertex has the R2 predecessor in T. Each vertex can be
a predecessor at most twice: once as the previous use of its own
grandparent column, and once as the selected non-target promotion of
its old-parent column. Those are distinct roles. Terminal zigs are
not vertices, and cannot supply the non-target promotion role.

Thus there is a directed rooted forest with exactly \(Q_B\) vertices,
outdegree at most two, and at most \(R_A\le2A\) roots. Roots inject into
actual A demotion bits. This is a complete construction on arbitrary
admissible periods; no frame exposure assumption is used. The forest
may be empty. For a restricted class with a uniform height L, it proves
\[
Q_B\le 2(2^{L+1}-1)A.
\]
This bound pays actual original B doubles on the complete sources
satisfying the height restriction. The unrestricted implication is
open. An unbounded exact one-column family refutes a uniform height
bound for the all-double forest, and the 72-key control refutes
disjointness of sibling frames.

For a smaller T, a silent last-promotion predecessor may lie outside T.
It is an external original B occurrence, not a funded root. Retention
predecessors are in T by definition. Forgetting the external roots would
be an invalid proof for the fixed overflow subset.

## R4. Unpaid physical obligation after pruning

GLOBAL_A_WORK_ACCOUNTING prices reset vertices and selected restoring
doubles that are prefix-paid, protected comparison-paid, nonneutral,
whole-frame exposed, or completed-parent-output exposed. It proves a
global budget, even with multiple columns, shared historical owners and
arbitrarily nested epochs. It does not price no-promotion paths or the
remaining doubly silent restorations.

**Proof box.** Target: \(T\le KA\). Conditions sufficient: a uniform
aggregate bound on vertices of the remaining forest pieces, including
external silent restorers if working on a subset; or a joint count of
the two unpaid classes. Inheritance: R1–R3 and the signed/exposure
budget. Ambiguity: frame inclusion supplies neither disjoint child
budgets nor bounded depth; local causal-span congestion is unbounded
on physical parents. Bridge: add the bounded paid vertices and the
two bounded residual classes, then apply the three-slot theorem.
The uniform aggregate condition is **OPEN**, not defined as funded.
