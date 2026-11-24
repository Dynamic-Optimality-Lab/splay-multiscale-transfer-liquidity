# Literal original residual partition

## Frozen sets and order

All sets here are sets of **original gap occurrences**, identified by the full original rho=(consumer h, inner producer ID, outer producer ID), source-scoped. Write R_* for the inherited original subset of R6 and F for the union of the frozen carrier and skipped-rank eligible classes. Let P_old contain original gaps whose original consuming double index j is at most 2a_h, where a_h=A(G_h) on the original incoming cyclic KEEP gap (previous KEEP excluded, current KEEP included, all DELETE helpers included).

The OLD selection pool is

\[
C_{\rm old}=\mathcal R_*\setminus(F\cup P_{\rm old}).
\]

E_old is selected **once on C_old**: for each physical g and each epoch starting at an actual A-demotion bit of g and ending at its next such bit, take the first original C_old parent in cyclic chronological order, and all its C_old gaps. There is no epoch/donor if g has no actual A demotion in the period. This is the pinned C03 `epoch_payment.py` rule, not a new selection on D.

H_all is the whole original noncheap hybrid class under the frozen single source case. If any full-period cut/variant has the old cyclic certificate <=10A, it pays all original noncheap eligible R_* occurrences. Otherwise use the existing eligible local raw/G/H intervals with threshold 5A(I). Do not add these source-case budgets or change guard thresholds.

The prescribed current pool and quota are

\[
D=\mathcal R_*\setminus(F\cup E_{\rm old}\cup H_{\rm all}),\qquad
\mathcal R_{\rm overflow}=D\setminus Q(D).
\]

At each h, Q(D) selects the first min(b_h(D),2a_h) distinct original D parents in increasing original double index, and every D gap of each selected parent. No selector is refilled. For disjoint budget assignment use carrier, skipped-rank after carrier, E_old after F, H_all after F and E_old, Q(D), residual. Overlap in eligibility does not duplicate an assigned occurrence.

## Total map to the all-double forest

An original R6 occurrence keeps its original full-cohort adjacency, endpoint producer IDs, first inside hit and beta: the first actual B primitive deleting an edge of its intact original gap path at that consuming hit. Its original consuming parent is the containing actual B double (h,j). Original R_* and all subsequent selectors only remove such occurrences; they do not change beta, reindex the B doubles, or form new adjacency across removed cohort members. R6's consuming-parent predicates already require the qualifying original neutral double; a terminal zig is not an eligible such parent. Thus

\[
\mu:\mathcal R_{\rm overflow}\longrightarrow V,\qquad
\rho\mapsto(h,j)_{\rm original}
\]

is defined uniquely everywhere. It is immaterial whether the forest predecessor or other vertices of that B access have zero residual weight. They remain in the global forest.

## Three slots, on the original event path

Use the historical all-source theorem `IAGS12_D4_NEUTRAL_RENEWAL.md`, section 8.1, pinned in INPUT_MANIFEST. Immediately before a double the current target path has c -> g -> p -> x, with c absent at the root. Still-intact original gap segments awaiting first change lie on this path, and original adjacent gaps in the **full** cohort have edge-disjoint segments.

LL/RR first deletes old slots c->g and g->p, then additionally p->x. LR/RL first deletes g->p and p->x, then additionally c->g. Reflection changes orientation but not the count. A second-bit external/pivot edge inserted in bit 0 was not an intact original gap's first old edge. Middle transfer edges are off the current target path. A later rebirth of the same edge tuple cannot furnish a second first change of the same original occurrence. Hence one original double consumes at most three original gaps, even counting both bits together. Restricting to any unchanged subset, including the prescribed overflow, cannot increase this number:

\[
w(v)=|\{\rho\in\mathcal R_{\rm overflow}:\mu(\rho)=v\}|\in\{0,1,2,3\}.
\]

Because mu is a total function and the finite fibers are disjoint,

\[
R_{\rm overflow}:=|\mathcal R_{\rm overflow}|=\sum_{v\in V}w(v).
\]

This is a literal gap count. It is not the number of nonzero-weight parents. In C04 notation e_h=(b_h(D)-2a_h)_+, Q(D) leaves exactly e_h whole parents. Each has 1–3 D gaps, so

\[
\sum_h e_h\le R_{\rm overflow}\le3\sum_h e_h.
\]

## Disjoint weighted classes and required interface

The already-proved vertex partition gives, by restricting the same fibers,

\[
R_{\rm overflow}=R_R+R_C+R_P,
\qquad R_i=\sum_{v\in V_i}w(v).
\]

Every original occurrence appears once, under the unique type of its original parent. The root injection and three slots yield R_R<=3|V_R|<=6A, and hence the requested inequality R_overflow<=6A+R_C+R_P for every admissible source.

## Stronger consequence for these exact selectors: R_R=0

Suppose rho survives in overflow with parent v=(h,j). Necessarily j>2a_h: if j<=2a_h there are at most j-1 earlier original doubles, hence fewer than 2a_h earlier D parents, and the quota selects v. Therefore rho belongs to the **original** C_old.

If v were a global R vertex, its chosen A donor alpha demotes g(v) after the full B phase of the previous **all-double** same-g use and before the current pre-B boundary. There is no original B double with old grandparent g between alpha and v: there is none between consecutive global uses, and g is used at most once in the current B splay. Alpha is the last A demotion before v, by the same interval definition. Consequently v is the first C_old parent in this actual A-demotion epoch. The frozen E_old rule selects all its C_old gaps, including rho. But D excludes E_old, a contradiction.

Thus every global root has w(v)=0. This proof uses E_old on its original pool, without recomputation, moving a selector, adding credit, or assuming that every later consumer has a reset. It does not apply to raw prehybrid R_* weights, which can and do occur on roots. It proves R_overflow=R_C+R_P, not that the two descendant weights vanish or are bounded by A.
