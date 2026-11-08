# Pre-proof correction; same principal saturation theorem

This supersedes the starting proof identity in PRE_EXECUTION.md, preserving
that file. No mathematical checker/root/population test has been executed.
Manual review caught an arithmetic error: B old-root depth2 has reverse
weight1, NOT2. Therefore destination c=2 cannot be inferred when that old
root is marked. The proposed saturation function itself is unchanged.

Correct mechanism: simultaneous saturation on the Q region. If old root r
is marked, its successor again has the same opaque two-core Q shape, with
the roles of r,x exchanged; its unique visible target r has B depth1/2,
so successor h=min(2,w_reverse+2)=2, since w_reverse>=1. If r is unmarked,
the successor has V empty, and the already proved Lambda=c=2 applies.
In BOTH cases max(D,h) at the successor is2. This proves the desired
source residual w+2-h>=0 and entails no recursive-existence premise.

The same exact public h and principal theorem remain within all four
written gates. In particular this is a finite, explicitly defined
simultaneous operation; no forward reachability/fixed-point is introduced.
Unchanged sources preserve old valid inequalities by monotonicity, raised
sources have the displayed direct residual. R1-R4/caps/provenance unchanged.

The audit must verify both mark branches, the corrected reverse weights,
and Q preservation under the two zig terms. It must NOT claim destination
c=2 in the marked-root branch. For D_Q=max(Lambda,h), all H1 edges leaving
Q are valid, even if Lambda has invalid inequalities elsewhere. No new
H1 failure type is introduced; any remaining failure is outside Q and
among the previous possible0/+1 types.

Direct original LOW corollary also registered before audit: a Q source
has exactly TWO present real A nodes, both Scores. Connectivity forces
this from its three nonreal child cuts. The present-node set is immutable
through all A events, so no actual anonymous Gamma1 helper exists.
Original H2/Gamma0 is already range/floor-safe. Reuse those completed
normal forms; no new H2 fusion is asserted. Thus EVERY original LOW edge
with source Q is covered by D_Q. The inherited HIGH/h0 glue then bounds
every finite walk whose LOW sources all satisfy Q by-7, and fully closed
walks by0, for arbitrary signatures. This is a restricted graph theorem,
not full M3. It is one direct corollary of the registered local mechanism.

All other exposing prefixes, general zero/+1 transfers, and Score-bearing
Gamma1 sources outside Q remain OPEN. No later pivot follows this audit.
