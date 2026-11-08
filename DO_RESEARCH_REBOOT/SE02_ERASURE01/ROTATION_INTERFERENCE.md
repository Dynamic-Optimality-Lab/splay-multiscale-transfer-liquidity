# Source-local production of the signed erasure terms

## Complete primitive depth table

Use source node notation k(L,R). For left rotation

    p(L,c(M,R)) -> c(p(L,M),R),

the depth changes are p:+1, c:-1, all keys of L:+1, M:0, R:-1. For right
rotation

    p(c(L,M),R) -> c(L,p(M,R)),

they are p:+1, c:-1, L:-1, M:0, R:+1. All keys outside the pivot subtree have
change0. The statements hold for arbitrary BST hangers in their inorder gaps.
Internal hanger topology is rigid, so every member has the same offset.
These tables compose over the actual bottom-up primitive rotation words;
same-side doubles use parent-first order exactly as in the frozen source.

For a tracked key v let delta_t(v)=d_F,t(v)-d_E,t(v) before the occurrence.
At DELETE, delta is unchanged. At erased Kz,

    delta_next(v)=delta_t(v)+sum_{rho in actual F splay z} gain_rho(v).

At retained Ky (y!=z),

    delta_next(v)=delta_t(v)
       +sum_{rho in actual F splay y} gain_rho(v)
       -sum_{sigma in actual E splay y} gain_sigma(v).

Each gain reads membership in ITS OWN current source frame. The two rotation
words and their memberships need not agree. A root splay has an empty word.
One cannot transport a full-history rotation word to the erased tree, or use
the single-splay +2 bound as a bound on all future interference.

## Exact per-occurrence sign classification

For a retained Ky let f=d_F,t(y), e=d_E,t(y) and eps_f=f mod2, eps_e=e mod2.
The indirect charge is exactly

    j_t=floor(f/2)-floor(e/2)
       =(f-e-eps_f+eps_e)/2.

It is positive exactly when f's double-depth band is higher than e's. More
explicitly: if f-e>=2 then j_t>=1; if f-e=1 then j_t=1 precisely when e is odd
and otherwise0; if f=e then0. If f-e=-1 then j_t=-1 precisely when f is odd,
otherwise0; if f-e<=-2 then j_t<=-1. Direct erased-key charge is positive
exactly when its original pre-depth is at least2. These cases include zero
charges and different genuine/nongenuine statuses in the two histories.

This classification plus the primitive update tables is source-exact for all
operations and all r>=6 periods. It is not an exhaustive favorable geometric
partition of six-key walks: the state-dependent signs and their total remain
unrestricted until an additional compensation mechanism is proved.

## Universal source-family stress identities

For y<p<z and arbitrary hangers A,B,C,D, the source RR double is

    T_R=y(A,p(B,z(C,D)))
       -> T_L=z(p(y(A,B),C),D).

The source LL return at y restores T_R exactly. If z's KEEP is erased, the
subsequent KEEP y has original pre-depth2 and erased pre-depth0, contributing
+1 to J; erased Kz contributes1 to D. This is the inherited positive-marginal
hanger family. Any rule J<=0 fails here.

Both signs really occur source-locally. Let D have root w>z. Immediately
after Kz, a retained Kw has original depth1 but erased depth3, so its indirect
contribution is0-1=-1. The whole subtree D moved up two levels under RR.
Starting from the diagonal T_R, these are legal full/erased prefixes with
identical A trajectories. No closure or CD counterexample is claimed for that
prefix. The symmetric family follows by reversing order and swapping children.

These are formal rotation identities with arbitrary hanger substitution,
not finite instance tests. They prohibit assigning a favorable sign to J.
Equal depth vectors also do not imply equality of full B trees; later proofs
of resynchronization must establish full labeled-tree identities.
