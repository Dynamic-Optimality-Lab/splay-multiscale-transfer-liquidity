# Former-root orientation (PROVED from source cases; corroborated 52,362 configs)

**Claim.** Let T be rooted at y, z≠y present, T1=Sz(T). Then y is a child of z
(depth 1) or a same-side grandchild (depth 2, LL or RR). No other position.

**Proof.** Bottom-up splay consumes the y→z path innermost-first. Lower steps
restructure strictly below y (y's child pointer updates but y stays root until
the top step). The top step is determined by remaining path length and top-edge
geometry: length 1 → zig (y becomes child); length 2 with same-side edges →
zig-zig (y becomes same-side grandchild: LL gives y as right-right if z went
left, RR mirror); length 2 with opposite edges → zig-zag (y becomes child:
both rotations place g as child of z). Longer paths reduce to these by the same
top-step analysis after lower pairs are consumed (sites ascend by exactly 2,
rebuilt units root at z≠y). Zig-zag places g(=y) as direct child (verified in
rotation tables: g+1 with final depth 1). Hence depth ∈{1,2} (banked 26AJ Lemma 2)
with the stated geometry. ∎

**Consequence.** Sy in T1 is exactly one StepEv (single zig if depth 1, single
zig-zig if depth 2). The return tables (§4, R-zig/R-zigzig) are therefore the
complete return dynamics — no multi-step return analysis needed.

**Corroboration.** 52,362 (T,y,z) configs n≤9: 0 orientation failures, both
engines agree.
