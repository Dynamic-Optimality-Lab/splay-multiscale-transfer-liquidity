# Explicit B-closure quantifier and seam clarification

This note makes explicit why AC02's theorem for every closed coupling with KEEP projection W^p uses the certified B profile without assuming a preferred initial B state. It is the same scan identity, not another proof campaign or an additional premise.

On any thirteen-key BST, splaying12 produces 12(U,13) for some left subtree U on keys1,...,11. The subsequent decreasing KEEP scan11,...,1 canonizes that tree to R13, independently of U. DELETEs do not change B. Thus one complete W sends EVERY possible B input to R13. In a closed walk whose KEEP projection is W^p, the B state before every hot K13 must therefore be R13. Its entire 26-request B profile is exactly the prior certified profile. There is no alternate recurrent B state with different q values hidden in the theorem's quantifiers.

The same decreasing scan identity for A is used only in a cell with no effective pure A work. It applies to arbitrary U, not just the left vine in the B certificate. When a cell does contain pure work, AC02 uses the right-spine budget instead; it does not assume A canonicalizes or stays aligned with B.

Cyclic rotation of the physical input does not change these statements. Immediately after a K12, A has root12 and right child13; continue through the actual descending blocks to the next hot K13 leader. That leader may be DELETE13 completed later by KEEP13, so the depth and grouped-cost lower bound are measured BEFORE its effective splay. Any earlier different-key source block with no KEEP is counted in C_D. A request-level cut through a constant-key block cannot hide its leader cost. One may rotate the whole closed source walk to a block boundary when applying the inherited minimum-cut theorem.

All p cells are distinct physical source occurrences. Their pure pools partition C_D once, including blocks crossing the originally displayed seam. No reachability-prefix state, alternative B state, later-lap credit or unproved all-size A construction is assumed. The requested reachable couplings are a subset of this broader source-valid closed class.
