# GC-C: exact scan incidence; an A price remains open

Within each PF path, every right inside hit removes all remaining active descendants >=its target from g's right child; left reflection holds. Thus right targets decrease and left targets increase. Component-rooted one-sided shadows preserve the full active child and match old-g doubles. Their total rotation cost, including linear initialization, is bounded by C_seq M_loc. There is no additional cost-free concatenation theorem for mixed two-side words.

## Source-wide original B-bit injection

For each original inside hit of a path at old g, select the unique actual B primitive with pivot g in that access. It exists because the target is strictly inside g's component. Original g cannot be promoted in the block. Thus it is either an old-grandparent demotion or an opposite old-parent demotion, never the non-target old parent of SS. A terminal zig at g is impossible: just after the path's initial old-g double it is not the B root, and it cannot become root without a promotion.

Different paths of the same g have disjoint lifted hit intervals; different g select different pivot bits. Left/right targets are disjoint at any hit. Therefore this is a global injection from retained path/side hit occurrences into original NONTERMINAL B bits:

    M_hit <=2 Q_B.

This counts all physical inside hits in the canonical path family, not only demands, and preserves original modulo-period IDs at a seam. It is a proved scan incidence relation, not an A-work budget. Substituting the target Q_B back into a larger-coefficient inequality cannot close the target. No B bit is relabelled A credit.

The remaining support-padding mass is M_padding=sum(|I|-|H|). It represents actual initial internal search-path nodes, not an invented debt. A shadow's linear domain bound already includes scan accesses because |H|<=|I|; charging both again would double count. Strict monotonicity does not bound the number of initial non-target path keys by actual A work.

## A-funded exceptional scan class

Partition hit occurrences by the ORIGINAL double containing their B pivot bit. Each double has two actual bits, hence at most two such inside-hit occurrences globally. Let M_hit,nonU and M_hit,U count containers outside/inside original U. The inherited C1 theorem |V minus U|<=12A gives

    M_hit=M_hit,nonU+M_hit,U,
    M_hit,nonU<=2|V minus U|<=24A.

This is a genuine GLOBAL scan-class budget, also valid after hard selection. It counts original hit/access occurrences, not residual gap payments. The proof uses the bit injection and original single-extreme/SET non-U theorem, not finite loads. U hits and support-padding remain unpriced. Activating this subclass in the comparison inequality costs an explicit additional72 C_seq A (three gap slots times C_seq times24A), on top of the optional12 C_seq root budget.

The protected merge counterexample's opposite creator is original U and its sibling is unacquired, so that broader merging defect cannot always be routed to this non-U exception class. It still lacks a deep R6/C_old residual and does not refute a survivor-restricted repair.

## Paid-hit elision is false

On the exact39-key canonical original C_old PF path (3,4)->(7,4), h5 is an original frozen-F-paid inside use of old g2. The full one-sided sequence retains h5(target20),h7(target11). If h5 is deleted, the actual post-h3 initial tree gives a g2-to-target11 distance9, whereas the original consuming old-g double (7,4) has distance8. The shadow has g2 as an old parent, not an old grandparent. Its old-g match disappears.

This refutes ELIDE-FE on its stated pre-H scope. It does not create an actual survivor: the source has a positive periodic certificate. Paying an original gap does not erase the physical effect of its access. Safe hard-family trimming retains ALL intervening same-side inside hits after its chosen initialization, as proved in RESIDUAL_SENSITIVE_PATH_SELECTION.

The global A-price question is still the cost/reuse of initial interior domains and PM boundary roots. Neither an observed finite maximum nor this B-bit injection solves that question.
