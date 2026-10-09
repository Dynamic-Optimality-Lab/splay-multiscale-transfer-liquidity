# Implementation semantics

Tree terms are [key,left,right], with None for empty. Keys are distinct and totally ordered. Present-key ordinary bottom-up splay uses oriented zig, LL/RR zig-zig, LR/RL zig-zag and preserves the key set. All old-tree mutations are prohibited during this reboot.

Depth in scripts is edge-depth. e(d)=floor((d+1)/2) counts StepEvs: root access0, double1, terminal zig1. The legacy API splay_cost uses depth+1, including its broader absent path. The present route uses only keys in the fixed universe. DELETE masks the B occurrence and leaves B unchanged; it is not a BST deletion. Dense key ranks are an order-isomorphic encoding.

J4 slots: SELF for y (excluded from the per-other-node sum), L/R for descendant child subtrees, F_j for the off-path child of the ancestor j+1 steps above y, NONE for strict ancestors. lambda comes from the path fold. tau4=(slot,lambda,d(z)−d(y),d(y)). The root atom is separately indexed by the fold constant c. Shared variables span all tree sizes.

H_y=−R_static+4(n−subsize(y))+sum_(z!=y)j(tau_yz)+rho(c_y). Hence D_J=R_static(v)−R_static(u)+4(subsize(v)−subsize(u))+J_u−J_v; 4n cancels. Individual H growth gives no row-difference growth theorem.

Reduced H=4G+sum_non-NONE(j−lambda)+K_d additionally requires rho=c and NONE(tau)=N_d for all ancestors at depth d, with K_d=dN_d. These restrictions are not Python default values or established universal consequences. Finite maps may omit coordinates; the mathematical domain does not.

The DIAM generator bounds H−2b, b=[y=root(B)]. For nonroots raw width2; for root/nonroot the raw difference lies in [0,4]. J-SELF is a separate same-row splay inequality. A complete proof needs one assignment satisfying both, not separate pointwise selections.
