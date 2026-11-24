# Primitive proof and one-sided hit coupling

All letters below are arbitrary intact FULL physical components, including private hangers. The actual completed double identities are:

| Case | Before | After |
|---|---|---|
| RR | g(L,p(H,x(C,R))) | x(p(g(L,H),C),R) |
| LL | g(p(x(L,C),H),R) | x(L,p(C,g(H,R))) |
| LR | g(p(L,x(C,H)),R) | x(p(L,C),g(H,R)) |
| RL | g(L,p(x(C,H),R)) | x(g(L,C),p(H,R)) |

The notation is at the actual double boundary after lower doubles have been performed. Lower steps preserve the initial full ancestor frame. Higher steps transport the two completed outputs intact. Both non-target outputs exclude x, proving strictness even after restriction to original S. An LL/RR old-parent output is taken after bit1, never immediately after its bit0 promotion. A terminal zig is its one real rotation.

For a fixed g, a rotation at another key only transports its subtree unless g is the promoted child. Without promotion of g, only a pivot at g changes its full descendant set, always by loss. An inside right request can pivot g as the old grandparent (RR/RL), or as an old parent in an opposite LR/RL double. In every case g.right becomes a component consisting entirely of keys<x. Its left child and all its left internal edges remain unchanged. Reflect for a left request. An SS old-parent role would first promote g and is excluded on the ORIGINAL PF trajectory. A terminal zig at g cannot occur after post-B(u) without a prior promotion: g is not root just after its old-grandparent double. Other terminal zigs can transport its component and are retained normally.

## One-sided hit-shadow theorem

Start from the ACTUAL full B state immediately after u. Up to any PF-chain endpoint, keep only original KEEPs whose target lies in the actual pre-access B_g component and is >g. Omit left inside hits, outside hits and DELETEs. Replay ordinary splay from that exact initial full state. At every original operation boundary, the complete rooted subtree hanging from g.right in this shadow equals its original counterpart, including its root and all internal child pointers. Left-side reflection also holds.

Proof by induction over original accesses. An omitted outside request never enters the current g component, so preserves its internals. An omitted left request preserves g.right by the table. For a retained right request, the search suffix starting at g.right is identical in the two trees. All lower double steps are therefore identical. If the distance from g to the target is even, the final step involving g is the same old-grandparent double in both. If odd, g is the old parent of the target after the identical lower steps: its rotation transfers exactly the target's left child to g.right. This result is independent of the external grandparent, which can change the pairing to SS or opposite in the SHADOW. A possible shadow non-target promotion of g is followed by the target's rotation at g and has the same completed active-side output. If g is shadow root, the terminal zig gives that same transfer. Subsequent higher steps transport the completed g output and preserve the active side. This proves the induction without claiming equality of the other child or the full shadow tree.

Whenever an ORIGINAL retained target has g as its old grandparent, its even distance 2j from g is unchanged. The shadow thus has the same original j, g, p and orientation for that double. The full frame can differ on the omitted side; only the old-grandparent matching required by the inherited comparison argument is asserted. Different original parents cannot collide within one such shadow at the same operation/double. This is a physical coupling theorem, not new original U/Pi eligibility for shadow events.

Right retained targets strictly decrease, and left targets strictly increase, by the output rule above. Build each shadow's domain J as the ancestor closure of its retained targets in its ACTUAL initial B state, as in the pinned comparison theorem. The usual off-path component argument keeps every shadow access path in J; all other components remain intact. With no targets use no shadow and J=empty. This domain construction is neither a new original source nor a frozen F window. Its initialization and global reuse still require payment.

The general proof is by component identities and induction. ONE_SIDED_SHADOW_RESULTS/SCOPE audit selected complete original histories using an additional immutable shadow splay and complete active-side child pointers; finite checks are not a proof assistant or a universal test.
