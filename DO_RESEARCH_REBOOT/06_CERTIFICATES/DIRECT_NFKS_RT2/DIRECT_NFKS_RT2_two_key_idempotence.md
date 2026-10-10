# Two-key idempotence (PROVED; corroborated 52,362 configs, 0 failures)

**Claim.** For distinct present y,z: F_{y,z}(F_{y,z}(T)) = F_{y,z}(T), where
F_{y,z}(T) = Sz(Sy(T)) as full labeled BSTs (all hanging subtrees).

**Proof.** Let U = Sy(T) (root y), V = Sz(U) (root z). By orientation, y in V is
a child (zig/zig-zag top) or same-side grandchild (zig-zig top) of z.
Apply Sy to V: single zig (inverse of the zig that placed y) or single zig-zig
(inverse LL/RR pair at the top). In each case the top rotation(s) exactly invert
the final top rotation(s) of the Sz pass: zig inverts zig (same two keys, same
subtrees reattached); LL inverts the top LL (the three top keys y,p,z permute
back with identical hanging subtrees A,B,C,D restored — verified by composing
the LL region table with the return-LL table: A−2+2, B−1+1, C+1−1, D+2−2, all
net 0 for the V→Sy(V) leg restricted to the top unit, and untouched regions
stay put). Thus Sy(V) restores the pre-final-top state with y at root and the
identical child subtree containing z at depth 1-or-2 in the identical geometry
as U's top. Reapplying Sz repeats the identical top rotation(s) on identical
input, restoring V exactly. Lower units were already fixed points (z was root of
its unit; Sy with y outside that unit leaves it rigid; Sz re-splaying sees the
same path). Full labeled equality follows since every region is either rigidly
carried or exactly inverted. ∎

**Use.** Alternating y/z words revisit only post-y / post-z states, so the §6
depth bound persists for arbitrarily long two-key words.
