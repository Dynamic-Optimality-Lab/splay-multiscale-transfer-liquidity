# U1-U3 and their exact limits

Authority: [audits/PIVOT_UNIVERSALIZE_U1U4.md](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/audits/PIVOT_UNIVERSALIZE_U1U4.md>) sections A-H;
[lean/WP6/GCStaticGenealogy.lean](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/lean/WP6/GCStaticGenealogy.lean>) is explicitly an ABSTRACT descent kernel.

U1: take consumed B edges (x,parent),(parent,grandparent) before a double. Follow latest
establishing rotations backwards, recursively through earlier steps of the same splay.
The previous KEEP x rooted x, so every queried x-parent edge was absent then. The x-line
therefore reaches a strictly previous KEEP inside that key epoch. Max over strictly prior
origin accesses remains in-epoch because that x-branch is inside it. Eternal/Genesis
alternatives on the other branch do not remove the x-branch. Periodic indexing locates
predecessors; it does not create more credits. Epochs may cross.

U2: for a zero-A-cost B-active access t to z, the last positive-cost A arrival s at z exists.
Otherwise a non-z access would dethrone z and force a later positive z arrival; an all-z
closed word has no B-active z access. Between s and t there are only z accesses. Thus s
has a>=1. This applies to starved B-double consumers and starved B-active creators, not
arbitrary A no-ops without B activity. L1 strengthens it: s is DELETE, because a KEEP s
would root B at z throughout the quiet block. L2: distinct starved B-active ACCESSES have
distinct setups; the first KEEP in a quiet block roots B and prevents a second active KEEP.

U3: D->creator(D), then if that creator is starved ->setup(creator). The latter has positive
A credit, so at most two hops suffice. This proves reachability of positive credit, neither
availability nor ELIGIBILITY: charge() does not add creator-setup edges.

U1's paper mechanism and U2/U3/quiet/L1/L2 arguments are reconstructed here. The Lean kernel
receives the real-splay latest-establishment/consumed-edge facts AS HYPOTHESES; it does not
implement all BST mechanics, cyclic matching or U4. No new Lean build/kernel promotion is claimed.

H1 epoch confinement and H2 quiet blocks are valid at access level. H3 gives one active
starved ACCESS per block, not one B-double: one access may have many doubles. The historical
sentence 'no two starved doubles share one setup' is false on our three-double K7.
H4's O(dB) fan-in narrative does not prove a capacity bound or a unit-level injection through
recursive origins; no such theorem is inherited in the counterexample proof.

Implementation scope: build_origin indexes logged edges by (access,StepEv); make_origin_fn
recurses over changed AND consumed edges and contains an origin-set >64 cutoff. It is not
an independently proved all-size canonical ancestry implementation. The new finite cyclic
checks stabilize at 2/3/4 laps. More importantly, the refutation is independent of exact
creator identity: every possible B-mutation creator is a KEEP with ZERO A credits.
