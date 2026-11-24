# Exact physical inventories; no completed transfer X

Two independently defined original-source inventories were investigated. Their identities are proved, but neither has the quantitative price required to close full M1. They are not renamed residual differences.

## B-ancestry lifetimes

For each physical g and marked key y!=g, the indicator that y is a B descendant of g is an original state variable. It can be gained only by a B primitive promoting g, and lost only by a primitive with pivot g. Because B closes exactly, its gain/loss events alternate cyclically whenever it changes. An ancestry lifetime is the original opening gain followed by its first closing loss, with IDs (opening bit,g,y,closing bit).

The retired-target map in CHAIN_LIFECYCLES assigns every C child v to the lifetime closed by its predecessor u's old-grandparent loss of x_u. Distinct children have distinct closers, and a lifetime cannot have two first closers. If a given opening bit e promotes g and gains the original S-key set G_e, at most |G_e| such tickets can use it, one for each gained key. Weighted original gaps have load at most3|G_e|. All three gap slots remain original occurrences consumed at v, not new demands at e.

Define independently of residuals

\[
M_{\rm tar}=\sum_{e:\ B\ {m promotes\ its\ target}}|G_e|,\quad
M_{\rm nt}=\sum_{e:\ B\ {m promotes\ a\ non\!target}}|G_e|.
\]

Then R_C<=3(M_tar+M_nt) is a valid volume envelope. It is **not** the accepted c_1 A+X result. Target promotions can gain many descendants per A access, and non-target gain mass already has a historical superlinear counterfamily. Neither mass is assumed O(A). The577-key repeated-grandparent case and W Hall obstructions do not disappear by assigning these new names.

## A/B mismatch state potential and exact primitive laws

Write A_g and B_g for complete rooted descendant key sets and keep the original S. Set

\[
\Phi(A,B)=\sum_g |(B_g\cap S)\setminus A_g|.
\]

This depends on the complete relevant state and fixed original S, so exact paired closure gives Phi_final=Phi_initial.

For a rotation with pivot u and promoted v, let L_u be the key set lost at u and G_v the key set gained at v in the rotating actor. Every other rooted set stays fixed. An A primitive has

\[
\Delta\Phi=|L_u\cap B_u\cap S|-|G_v\cap B_v\cap S|.
\]

A B primitive has

\[
\Delta\Phi=|G_v\cap S\setminus A_v|-|L_u\cap S\setminus A_u|.
\]

The formulas count physical descendants, not SET multiplicities, and do not alter any original SET/Pi sign. A B target promotion has zero positive term since A is rooted at that same target. Thus every positive B mismatch creation is at a real non-target promotion. Let F_A be the signed sum of A deltas, G_B the sum of B positive terms and L_B the sum of B negative terms. Then exactly

\[
L_B=G_B+F_A.
\]

Every B primitive loses its current marked target from its pivot, and that target is absent from the pivot's A subtree. Therefore L_B>=2Q_B+Z_B. This is an exact flux identity and inequality, not a constant payment. The independent edge updater checks every term against complete boundary states.

## The missing price and explicit rejection

The candidate F_A<=K A for an absolute K is false, even on a common-diagonal root-zig-only source: M1_POTENTIAL_TEMPLATE_OBSTRUCTION proves F_A/A=n/2. Replacing F_A by its positive part or sum of A-created atoms does not help on that example. A closed state potential can have arbitrarily large cross-actor flux while its net period change is zero.

The saturated-column potential counts each nonempty mismatch column once and has bounded change per A bit. But it is not discharged at the predecessor pivots that supply C tickets: the future C target is still below g in B and outside the same rigid A component, so the indicator is1 both before and after that pivot. The unbounded chain realizes repeated failures. No unit local payment follows.

There is no completed X here. To use these inventories downstream one must first prove a bounded-load localization of **relevant deep original unpaid** ancestry lifetimes, or an independently meaningful restorer property that prices them without assuming the same missing C law. Merely taking X=3M_nt while leaving F_A unpriced, or X equal to the deep residual, is not accepted.

IAGS box: target full R_C<=c_1 A+X; inheritance exact primitive/lifetime laws above; sufficient bridge a global bounded-load price for relevant A-origin tickets plus a genuinely distinct restoration obligation; ambiguity event capacity is volume, not a unit and not an A bit; bridge remains **OPEN**. No proof of R_P+X is asserted.
