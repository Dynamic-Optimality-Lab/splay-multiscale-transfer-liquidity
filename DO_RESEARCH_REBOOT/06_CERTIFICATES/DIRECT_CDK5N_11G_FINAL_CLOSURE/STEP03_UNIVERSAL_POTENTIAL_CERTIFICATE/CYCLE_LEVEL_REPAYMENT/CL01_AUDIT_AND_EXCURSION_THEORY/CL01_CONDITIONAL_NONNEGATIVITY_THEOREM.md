# CL-01 Conditional Nonnegativity Theorem (PROVED conditional)

Assume H1 (all 00 edges: w>=alpha-diff), H2 (all maximal deep excursions:
w(P)>=alpha(u1)-alpha(u0)), H3 (all deep-only closed walks: w>=0).
Then every closed walk has w>=0. Proof: TYPE L by H1 telescoping
(sum of alpha-diffs = 0). TYPE H by H3 directly. TYPE M: decompose
(decomposition theorem); each 00 edge contributes >= its alpha-diff (H1);
each excursion contributes >= its endpoint alpha-diff (H2); alpha-diffs
telescope around the closed walk (sum 0); hence w(C) >= 0. Covers all
lengths/masks/signatures/high edges (whatever H1-H3 quantify over).
STATUS: conditional — H1, H2, H3 all OPEN (H2 untested: no paired
excursion in stored data; H1/H3 unproved universally). Sufficient, not
necessary. No promotion.
