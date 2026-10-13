# UFRL_REPRESENTATIVE_CONSTRUCTION.md (Steps 5-7: E1-E8 + L1-L8 proof)

## Construction (code: UFRL_extract.py)

E1: depth-6 prefix K retained exactly (|K|≤127 binary); frontier F =
nonempty subtrees below (|F|≤128). E2: frontier positions recorded.
E3: hidden S keys stay in their frontier (no moves). E4: S-less nonempty
frontier ⇒ min-key witness (deterministic). E5: E=K∪S∪witnesses;
|E|≤264; non-S ≤255. E6: V_i⊇E∩G_i, |V_i|=min(|G_i|,266) — feasible since
|E∩G_i|≤255≤266 (both cases verified in code; fill = lowest keys).
E7: prefix exact; per-hole balanced rebuild over retained keys of that
hole (S_h + witness + V_i∩hole); empty stays empty; attachments kept
⇒ rebuilt contents at depth ≥7. E8: |U*|=9+Σ|V_i|≤9+10·266=2669 (exact
set arithmetic; V_i disjoint from S by gap definition).

## Preservation L1-L8 (proof + fuzz: 2,305 general + 180 adversarial + 30,773 B-side, 0 mismatch)

L1: targets of H≤2 intervals have a≤2 ⇒ d≤4 <6 ⇒ in K ⇒ retained.
L2: pivots are ancestors of targets with current depth <d≤4; initial
depth ≤ current + prior rotations ≤ 2H + ... ≤ 4 <6 ⇒ in causal region
(prefix exact ⇒ pivot keys/positions exact).
L3: induction over effective accesses: descents agree (same prefix,
same keys, same comparisons; frontier never entered — targets at depth
≤4 < frontier depth ≥7); hence depths, a-costs, H agree exactly.
L4: same paths ⇒ same zig/zig-zig/zig-zag cases (path-shape-determined);
frontier blocks rigid in both (verified step-type sequences identical).
L5: displacement ≤4 total rotations (2H≤4); initial ≥7 ⇒ final ≥3 > 2;
rebuilt roots also at depth ≥7 (attachments kept) ⇒ same bound. Hence
final top-3 nodes were initially ≤6 in both; holes provably inert.
L6: initial shadows: prefix exact + frontier nonempty preserved (S or
witness ⇒ nonempty; empty stays) + hole S-subsets (E3: same subtree) +
root (u both) + inventory (L7). Final shadows: visible topology (L3-L5:
same retained trajectories) + S identities (S never dropped/moved
across blocks) + anonymous pattern (positions, canonical β) + holes
(S-content rides rigid blocks; emptiness as initial) + root v + inventory.
L7: min(|V_i|,266)=min(n_i,266) by E6 construction; ops fix universe.
L8: zero-DELETE removal sound (frames-empty identity, verified); terminal
KEEP present; B via §9 representative (depths/q/projected-successor
preserved: marked ancestors all core ⇒ retained; verified 30,773 cases);
actual splays/costs throughout.

## B-compatibility (§9)

Representative B* on U*: same S, projected core shape, fringe blocks on
retained gap keys (surgical/extraction rebuild). Marked B-depths preserved
(ancestors core ⇒ retained ⇒ identical chains); q preserved; projected
successor preserved (splay path = marked S-path in both; verified).
No prune-then-splay commutation assumed (Control F respected: only
projected outcomes compared, full-tree equality never claimed).
