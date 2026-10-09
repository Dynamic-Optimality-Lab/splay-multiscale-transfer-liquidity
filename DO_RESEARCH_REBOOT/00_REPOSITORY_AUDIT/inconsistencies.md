# Conflicts, bugs, and proposed repairs (not applied)

1. **Finite UG imposed vs universally mandatory.** wp6_gapcompat.py adds gap equalities; wp6_ugar.py builds a finite map from six overlaps plus two extensions. No all-offset proof found. Repair: label these as added finite constraints and prove any claimed universal necessity separately; do not enlarge the map by assumption.
2. **Empty-sibling orientation.** wp6_funcmp.py:108 onward, wp6_redimpl.py:174 onward, and analogous leveled probes use [0,None,T] for s=0 but [p,T,S] for s>0. This changes the path side. Proposed patch: keep root p and the same child slot in both cases. Do not edit source here. The new checker uses [p,T,None] (or its mirror) exactly.
3. **Unseen-coordinate omission.** vec/Pform builders skip keys absent from finite rvmap. Proposed patch: keep a separate symbolic coefficient dictionary for unknown coordinates or refuse a universal interpretation. Unseen coordinates are not zero-valued mathematical variables.
4. **Root correction.** Raw diameter2 for every node is not the source DIAM statement. Use adjusted H−2b; root/nonroot raw range[0,4].
5. **Counts vs key sets.** Equality of atom key sets does not establish equality of coefficients. Genuine fixed-child nonrotating insertion freezes each old occurrence, while the new leaf can increase an already-present atom's aggregate count. Missing 26AB logs prevent identifying the cause of any purported changed old occurrence.
6. **Paper pins.** prereg/bridge_manifest.yaml records v1 SHAe23ea8b5..., local 29-page L3 v3 has SHAf7aa7901.... Do not silently update the original bridge gate. This reboot has an explicit independent v3 reference.
7. **Finite interface labels.** The 970x79 C0 narrative block is the xclean added-row restriction to old touched columns. It is not the full A0/A1/A2 arrays in j4_levelblocks.npz (250/550/970 rows by142 common columns). Compare matrices and coordinate domains before comparing ranks.
8. **Rank/nullity confusion.** Source kernel dimension is source_dim−rank; target image deficit is target_dim−rank. See permanent correction. Supplied corrected dimensions are retained but their missing actual matrices are not certified here.
9. **Stale report states.** “Only GC-STATIC open” in an older conditional route and later “Coarse-Double open” refer to different sufficient programs. The normative MSTL registry does not reflect every untracked J4 exploration. Preserve source distinctions.

All repair proposals remain documentation inside the authorized workspace. No source fix was applied.
