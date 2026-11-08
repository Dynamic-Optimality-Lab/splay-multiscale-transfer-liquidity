# Source-preserving numerical image memoization

An immutable profile p is the complete numerical debt function on ONE
fixed A-root class. For target key x define its exact LOW image

    T_(p,x)(t)=max {p(s)-2h : (s,t) is an actual H=h LOW row}, h=1,2.

The image depends on p,x and the already certified full A source relation;
it does not depend on which literal B tree currently points to p. For an
ACTUAL full B edge b--x-->bt of cost q, its numeric update is therefore

    D_bt(t) <- max(D_bt(t),T_(p,x)(t)+q).

Caching this image, or the result for an identical immutable source/target
profile pair and q, is exact evaluation reuse. It does not identify b or bt,
does not remove their original edge, and does not realize an abstract
profile cycle. Negative witnesses still require literal A/B state closure.

Cached result IDs refer ONLY to currently live immutable profiles. If an
ID has been released, recompute; profile IDs are never reused. Caches are
bounded and are derived values discarded at CPU checkpoints, not new
physical source evidence. Before parent tracing is activated they save
only numerical values. Above the tracing trigger8, use the uncoalesced
actual predecessor updates. The trigger is not a claimed debt bound.
Every genuine negative source cycle would eventually trigger tracing in
an unbounded fair relaxation; only a literal checked negative cycle is
reported. A cap/checkpoint is not evidence of absence.
