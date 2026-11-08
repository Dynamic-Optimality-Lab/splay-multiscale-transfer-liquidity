# Simultaneous fixed-owner exchange

Input: actual D,U, original locked common l and partial h0/l map a;
independent source-certified complete injection h agreeing with h0 on
dom(h0). No previous value may be changed. The residual roots are Pstar.

Algorithm: for each p in Pstar against the SAME fixed a, repeat
u=h(d), then d=a^{-1}(u) if u already paid; otherwise save (p,u).
After ALL roots terminate, return a union all saved pairs.

In the demand-owner graph each vertex has at most one predecessor by
injectivity of h and a. Starting roots have no incoming edge because
they lie outside dom(a). Entered cycles and merging paths would force
predecessors back to a paid starting root or two equal roots, impossible.
Finite D and total h imply termination. Paths and their terminal units
are disjoint, so all saved units are different and outside im(a).
All previous a values, not just common owners, remain literally fixed.

Eligibility bridge: each old successful h0/l path avoids R and remains
IDENTICAL in complete h/l on the EXACT original common set C. Blocked
paths continue and previously missing noncommon R roots start. Complete
exchange disjointness forbids any new terminal equaling an old endpoint.
Thus licensed full h/l is exactly the old a plus these residual pairs.
The all-paid walks compute those same new terminals. This proves joint
source legality without enlarged auxiliary claims, guessed fE, altered
eligibility, assumed cardinality or any reassignment of old paid roots.

The algebraic path proof has no fixed two-root bound and is sufficient
for any finite residual set IF a complete independent source h is supplied.
It does not independently supply arbitrary-support h. Here the actual
two-slot predecessor theorem supplies it. The public allocator rejects
more than two residuals/slots so the executed campaign remains bounded.
