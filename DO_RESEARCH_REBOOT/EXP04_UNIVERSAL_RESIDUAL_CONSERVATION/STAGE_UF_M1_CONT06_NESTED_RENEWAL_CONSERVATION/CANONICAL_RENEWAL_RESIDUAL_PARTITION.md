# NR-A: exact original PF/PM residual partition

Use C5's ORIGINAL C_old predecessor map, not physical noncheap adjacency. For each rho in S_UU, let v=mu(rho), g=g(v), and u its unique preceding C_old parent in its actual A-demotion epoch; if g has no A demotion, take the unique cyclic preceding C_old parent, with a preceding-lap self-copy allowed. A C_old first parent in an actual epoch is E_old-selected, so it cannot be a survivor.

Let I(u,v) run AFTER the full B phase of u through the post-A/pre-B boundary of v, on its canonical lift. No A bit in I demotes g. A B promotion of g in I cannot target g: targeting g in A would force its demotion before the later different consumer. Thus every promotion there is a qualifying SS bit0 non-target promotion with old parent g.

Define S_PF to contain exactly the original S_UU rho whose interval has no such B promotion; S_PM contains the rest. The predecessor/interval and promotion Boolean are parent-defined, independent of which gap in v is retained. Therefore

    S_UU = S_PF disjoint-union S_PM.

No reset or seam exception is omitted. A preceding-lap ID is a lift for history only, never an additional measured event. In the epochless singleton case, PF is actually impossible: F_v subseteq J_v proper-subset F_v would contradict equality of the full labelled states on repeated laps. Such a possible singleton survivor must be PM.

For each actual D-tail parent v in Z_h retain its literal D-fiber weight d_h(v). Partition Z_h by the same PF/PM flag. Exactly

    |S_PF| = sum_h sum_(v in Z_h^PF) d_h(v),
    |S_PM| = sum_h sum_(v in Z_h^PM) d_h(v).

Each weight is1..3; the original full-cohort adjacency, beta, rho and parent never change. Broader C_old PF edges before H/quota are only an upper candidate class. Their nonzero count does not certify actual S_PF.
