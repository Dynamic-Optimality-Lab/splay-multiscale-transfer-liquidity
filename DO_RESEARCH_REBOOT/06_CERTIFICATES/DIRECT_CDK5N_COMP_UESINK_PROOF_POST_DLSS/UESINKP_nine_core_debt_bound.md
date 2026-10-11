# Marked nine-core debt bound, standalone (L2b, arbitrary ambient trees)

Definitions: marked set M (genuine KEEP keys are marked); marked B-ancestor
core = union over m∈M of root→m paths, ancestor-closed by construction;
H1: |core|=9 at every cyclic state.
Claim: every genuine KEEP access has d_B≤8 (hence q≤4).
Proof: the accessed key is marked, so its root-to-key path lies in the core
by definition of the union. The path has at most 9 nodes (core size), i.e.,
at most 8 edges. ∎ No assumption that the ambient tree has nine nodes —
unmarked nodes outside the core never lie on a marked root path.
Consequences: q_j≤4 for all KEEPs; c=0 ⇒ q=0 (B rooted + frozen, see L-doc);
w>0 ⇒ w∈{1,2}. (Corpus max dB=6, max q=3.)
