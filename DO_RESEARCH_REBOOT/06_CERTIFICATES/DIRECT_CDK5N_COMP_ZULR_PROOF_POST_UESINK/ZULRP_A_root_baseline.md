# A-root-change baseline, standalone (L2a)

For any cyclic KEEP interval I with change bit c and A-sum H: H≥c.
Proof: c=0 is trivial (H≥0). Suppose c=1 and H=0. Then every access in I
has a=0, i.e., d_A=0, i.e., targets the current A-root. Splaying the root
is a structural no-op, so the A-tree (hence its root) never changes during
I. The root at I's start is x_{prev} (the preceding KEEP splayed it there).
The terminal KEEP therefore targets x_{prev}, so x_j=x_{j-1}, contradicting
c=1. ∎ Hence R=2(H−c)≥0 for every interval, with no-ops and arbitrary
DELETEs allowed. (IN: all 16 intervals satisfy H≥c; OUT: all 16 satisfy it.)
