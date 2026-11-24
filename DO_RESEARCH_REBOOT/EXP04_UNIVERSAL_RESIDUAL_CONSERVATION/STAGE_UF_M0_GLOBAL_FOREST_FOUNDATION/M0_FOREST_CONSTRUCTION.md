# Canonical construction on all original B doubles

## Physical inventory

Fix the original labelled source, its operation numbering and its original S. A vertex v=(h,j) is the jth actual B double of KEEP h. Write x(v), g(v), p(v) for its target, old grandparent and old parent, respectively. Write F(v) for the S label of the complete subtree at g(v) immediately before this double. Lower doubles in the same bottom-up splay stay inside this ancestor frame, so F(v) is also its original pre-B subtree label. Let J_g(v) be the completed old-grandparent output after both bits, and P_p(v) the completed old-parent output. Neither output is replaced by an endpoint of an older residual gap.

All these are physical quantities. A source's nontrivial KEEP targets belong to its genuine support and hence to S. The initial path union S is ancestor-closed and contains all B access paths. Splaying targets in S preserves this property: private off-path components move as intact components and no private key is traversed. Thus x(v) is in S and in F(v). If all KEEP targets coincide, exact B closure makes each KEEP a B identity, so V is empty. No KEEP, an empty word and zero B work are likewise harmless cases.

The evidence records retain original g,p,x, rotation case, S frame and outputs, real primitive edges and signs, complete pre/post step states, and complete A/B operation boundaries. The finite tests use dense ordered integer labels; the argument itself uses only order and labelled subtree membership and applies to arbitrary finite ordered key sets.

## Global columns and cyclic intervals

For each physical key g, list cyclically **all** vertices with g(v)=g. In a single B splay a key is an old grandparent at most once: after its double it lies in a completed subtree off the remaining target path. Let u(v) be the previous occurrence in this global column. For a singleton column take its preceding-lap copy.

Let I(v) contain the measured original operations from after the full B phase of u(v) through the post-A/pre-B boundary of v. The two endpoint B phases are excluded. This precise boundary convention matters: promotions inside the current B phase do not qualify. A demotion in the A phase at the consumer does qualify. Intervals lift at most one period. For fixed g their interiors are disjoint; if consecutive uses are adjacent KEEP operations, the interval still includes the intervening A phase.

## Deterministic priority, exactly as in C05

1. **R:** If I(v) contains a real A rotation whose pivot is g, declare v a root. Its donor is the last such primitive on the lift. It has no predecessor.
2. **P:** Otherwise, if I(v) contains a real B primitive promoting g, choose the last one. Let r be its containing original B double; set pred(v)=r.
3. **C:** Otherwise set pred(v)=u(v).

This is the historical reset-first rule in C05 `forest5.py`, independently recovered as a streaming two-lap rule in `independent0.py`. A raw geometric description could apply despite a reset; the canonical rule makes that history ineligible for P or C. Thus an R vertex has no **reset-free admissible** predecessor. We do not assert that no older vertex could contain its frame geometrically. No historical rule was repaired or silently changed.

## Why the P predecessor exists in V

Assume no A-demotion of g in I(v). There cannot be a B access targeting g in this interval. Its preceding original A access leaves A rooted at g. The first later request different from g, at latest the consumer target x(v) different from g, must demote g by a real A rotation before the current pre-B boundary. That would be a forbidden reset. Consecutive repeats of g do not evade the first later different request.

In ordinary bottom-up splay, a non-target is promoted only by bit 0 of an LL or RR double, and is that double's old parent. Both bits of LR/RL and the last bit of LL/RR promote the target; a terminal zig also promotes the target. The chosen primitive therefore lies in a genuine original double r, with p(r)=g. It is neither a virtual event nor a terminal zig. Its entire B phase precedes the current consumer's B phase on the lift.

The finite original event list makes each last-event choice unique. Exactly one of 'reset present', 'no reset but promotion present', and 'neither present' holds. C always has u(v) in V; P has r in V as just proved. Acyclicity below will also exclude a putative same-original-ID predecessor across the seam. Consequently every original B double is classified once and only once, before inspecting any residual or comparison payment.

Rotating a computational scan cut preserves these original IDs, S and all selector data; only the lifts change. A new research source with a different original cut must use its own original S and residual definitions. Cut checks here do not authorize recomputing those definitions on a changed shadow source.
