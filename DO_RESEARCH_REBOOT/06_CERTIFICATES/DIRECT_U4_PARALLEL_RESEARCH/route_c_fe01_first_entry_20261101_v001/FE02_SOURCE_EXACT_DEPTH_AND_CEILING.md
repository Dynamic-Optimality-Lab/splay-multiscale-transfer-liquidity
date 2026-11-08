# Exact source-only final depth and the FE ceiling

**Theorem B — PROVED—UNIVERSAL.** For every finite valid ordered BST T and
present x,y, the formula below computes d_(S_x T)(y) from the original
source tree, path, first-entry role and unconsumed outer frames alone.
No output tree is an input to its definition.

## 1. Definition and exact equality

If y=x, define H(T,x,y)=0. If x is the root and y!=x, define H=d_T(y).
Otherwise let h=d_T(y), let e be FE01's first containing source operation,
and let Delta_entry be its exact role-table value. Define

    H(T,x,y) = h+Delta_entry
                 + sum_(doubles strictly after e) Delta_outer
                 + zeta.                                            (1)

Here zeta is the exact proper-target-fringe shift of a terminal zig STRICTLY
AFTER entry, if present; otherwise it is0. In particular, if entry itself
is the final zig its full role shift is already Delta_entry and zeta=0.
The zig is never counted twice. For a later ZIG_L, zeta=-1 for y<x and0
for y>x; for a later ZIG_R, zeta=0 for y<x and-1 for y>x.

FE01 proves y's depth is h before entry, its entry shift is exact, and each
later shift in (1) applies by the persistent target-fringe invariant. Adding
the equalities through the final operation therefore gives

    d_(S_x T)(y) = H(T,x,y).                                        (2)

This proves (2), not just an upper bound. Internal subtree depths and site
offsets have cancelled locally; arbitrary source size/path length enters
only a finite, determined sum. Nonnegativity follows from (2), so no clamp,
fit or inferred correction is needed. Special cases were defined directly
from their source operation lists. Original subtree membership (or original
LCA depth) selects entry before any rotations are executed.

## 2. Comparison to unchanged PF

For y!=x, d>0, let r be the number of later doubles and t the number of
those doubles equal to LL when y<x or RR when y>x. The later-double sum
is exactly -r-t. The later zig is nonpositive. FE01's exact entry table
satisfies Delta_entry<=mu_PF for EVERY role: parent p gives0; LR parent
outer A and RL parent outer D give0; other double roles are at most2;
zig-entry roles are at most1. These are precisely unchanged PF's allowances.
Hence

    H <= h+mu_PF-r-t.

Also every entry shift is at most2 and every later shift is nonpositive,
so H<=h+2. This proves the whole-splay +2 displacement bound directly from
the source identities, including root no-ops and access to y itself.
Since H>=0, the historical PF clamping/minimum is safe and

    0 <= H <= min(h+2,max(0,h+mu_PF-r-t)) = U_PF.                    (3)

The special accessed-key and root-no-op definitions agree with PF and
satisfy (3). No old PF allowance, special case or algorithm is changed.

## 3. Refine only the first intervening B change

Keep the exact inherited A-root blocks and costs: C_j=2a_j, q_j B doubles,
and delta_j=q_j-C_j. For a source-positive anchor i, let T_i be its B
destination, h_i(y)=d_T_i(y), and k_i(j) the number of genuine B changes
STRICTLY between i and a later payer j. A terminal B zig is a genuine change
even with q=0; B-root no-ops and DELETEs leave B unchanged.

Define the separate FE source fact:

    c_FE(i,j) = 0,                              if j has no KEEP;
              = floor(h_i(y)/2),                if k=0;
              = floor(H(T_i,x_i',y)/2)+k-1,      if k>=1.            (4)

x_i' is the first genuine intervening changing access. Its pre-tree is
exactly T_i, since every earlier intervening operation froze B. H is
computed once from this ORIGINAL first pre-tree and frames. No later B
change is exactly propagated or used to refresh it.

If k=0, the payer's B source is T_i and q_j=floor(h_i(y)/2). If k>=1,
(2) gives the exact depth immediately after the first change. Each of the
remaining k-1 changes increases y's depth by at most2 by section2. Therefore

    q_j <= floor((H+2(k-1))/2)
         = floor(H/2)+k-1 = c_FE(i,j).

For KEEP-less blocks q=0. Mixed DELETE/KEEP blocks still have only their
one B-changing KEEP; preceding A-only requests do not affect its B source.
Repeated keys and a first intervention accessing y are covered by H=0.
The original future q is used only to VERIFY this bound, never to choose it.
Equation (3), floor monotonicity and the unchanged k=0 case give

    q_j <= c_FE(i,j) <= c_PF(i,j).                                (5)

Thus FE's first-intervention refinement is universally sound on arbitrary
admissible histories, not just the designated witness. Its global
completeness is a different, unproved claim.
