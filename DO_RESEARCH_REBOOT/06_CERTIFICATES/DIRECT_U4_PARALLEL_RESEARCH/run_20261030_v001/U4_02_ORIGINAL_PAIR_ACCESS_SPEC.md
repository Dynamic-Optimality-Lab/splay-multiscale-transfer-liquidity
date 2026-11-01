# Exact original Pair Access specification

K is any finite totally ordered set, T0 any BST on K. A and B start at the SAME T0.
KEEP x splays both; DELETE x splays A and freezes B. All x are present. DELETE omits an
occurrence from the retained history; it never physically removes a key. The theorem domain
is every finite exactly closed pair walk reachable from some such diagonal, any length.

Depth d counts EDGES, root depth0. For each access a=ceil(dA/2); on KEEP q=floor(dB/2),
z=dB mod2, b=q+z=ceil(dB/2); on DELETE q=z=b=0. A=sum a, Q_B=sum q, Z_B=sum z,
B=Q_B+Z_B. A DOUBLE is one StepEv for two rotations; the final single ZIG is one StepEv.
LT cost is d+1, a different quantity. In legacy_embedding.replay_A/replay_B the variable a
actually stores that LT cost; wp6_overflow.replay recomputes the StepEv a. Names are not interchangeable.

Pointer source: [_depth_to / primitive rotations / splay_trace](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/python/liquidity/legacy_embedding.py:59>).
Both zig-zig cases rotate parent over grandparent first, then target over parent; zig-zag
rotates target over parent then target over grandparent. Events execute deepest first,
with a terminal zig if depth is odd. Independent source: [_rebuild](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/python/independent/splay.py:92>).
Pair graph source: [build](<C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/scripts/wp6_cycle_ratio.py:58>). Event counts and full
states were compared at every access of both new physical witnesses.

Root repeats are no-ops with zero event cost (but LT cost1); nongenuine KEEP is B identity,
possibly with positive A cost. If every KEEP is nongenuine, Q=0. Empty walks/key domains are
trivial. If some KEEP is genuine, every retained key on a B-closed period belongs to genuine
support: the cyclic B root is the latest genuine target. Both trees, not roots alone, must
close. Repeated accesses, zero operations, primitive/nonprimitive words, both orientations,
sparse order-preserving relabeling and a single copy of cyclic credits are included.

CD-U: Q_B<=2A for ALL such walks. U4-M is a sufficient stronger graph-matching claim,
now REFUTED. U4-S (R<=S) remains equivalent to CD-U by R-S=Q_B-2A.
