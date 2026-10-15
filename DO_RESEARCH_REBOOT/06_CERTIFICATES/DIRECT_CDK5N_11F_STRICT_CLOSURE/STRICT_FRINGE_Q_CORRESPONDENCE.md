# STRICT_FRINGE_Q_CORRESPONDENCE.md — Gate B consequence (q status per class)

## Proved: marked all-core paths give core q
If marked target x has all-core B-ancestors at genuine-KEEP time, then concrete `d_B(x)` equals the
skeleton core depth, so `q = floor(d/2)` is exactly the compiled representative q (path-verified,
depth-equality checked per edge; 138 grounded + 5 E3/E4 negatives; skeleton-vs-concrete depth
agreement asserted, mismatches skipped openly).

## Open: fringe-ancestor q
If marked x has fringe B-ancestors, concrete q (full depth) may exceed representative q
(core depth). The §9 projected representative preserves q under Control-F discipline (30,773
imported cases) but per-macro preservation is not re-proved here. No fallback observable is
introduced (R3); no alternative B-controller (frozen); no new coordinate. Status: OPEN.

## Accounting rule (A8, exact)
Macro `Q_B` = terminal genuine q only (intermediate genuine KEEPs prohibited by segmentation
discipline; nongenuine/zero-cost KEEPs contribute nothing: B-unchanged or unmarked). `w = 2H-q`
is used only with correctly derived source macro cost. No independently supplied q anywhere in
production predicates (high-cost q witnessed via terminal B-trace in STRICT_HIGH_COMPILER).

## Consequence for simulation
Items using representative-exact q are complete on the all-core class and conditional elsewhere
(G23 item 9 already conditional; SC24 cannot pass while this is OPEN — stated, not hidden).
