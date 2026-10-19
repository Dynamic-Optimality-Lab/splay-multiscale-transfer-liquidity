# CORE-01 Source Semantics (read from frozen code, not summaries)

B-controller: 19 slots (0..8 core S-indexed, 9..18 gap); kl/kr kinds,
rl/rr refs, root ref; parent muxed over all slots. Splay = bottom-up
zig/zigzig/zagzag via single_rot (rotation of child x, parent p, grandparent
gp; middle subtree S moves to p; rest rigid). DELETE/isK=False/inactive:
b_blend identity (verified). Terminal low KEEP: genuine + marked-target
(tisS + mu-membership + B-change on terminal event; build_slow lines
172-197). Intermediate KEEPs: A8 forbids (marked AND B-changing); unmarked-
target B-changing intermediates ADMITTED. nev=len(word) in ssertify envs
(single-KEEP => single active event + identities). OM high: ONE marked-
target splay (build_shigh ev=0) + bs1==g.b; terminal marked (mv2, core).
MO: t.b == g.b carried (b_equal), zero weight.
