# Exact positive extension: arbitrary marked support with core at most seven

Reuse the completed K4 certificate at precisely its proved scope: every BST U
on4..7 nodes, every four-element marked subset F and every x in F satisfy

    q-2c + eta_F(S_x U)-eta_F(U)<=0,
    q=floor(d_U(x)/2), c=1[x!=root(U)],
    eta_F(U)=1[max_{z in F} d_U(z)=6].

The saved certificate includes ALL such trees/subsets, even when F's own core
does not fill U. This is explicit in its proof and verifier source. We do not
replay any of its68876 accepted rows.

## Destination-witness subset argument

Let U have at most7 nodes, and let M be ANY marked subset with |M|>=4. Define
eta_M by the same formula. Since every node has depth<=6, eta_M is just the
existence of a marked depth-six node and is monotone in the marked set.

For an arbitrary x in M, write U'=S_x U. If eta_M(U')=1, choose a marked
depth-six witness z in U'. Pick a four-element F subset M containing x and z;
at most two required elements leave enough room to pad to four. If eta_M(U')=0,
pick any four-element F subset M containing x. In either case,

    eta_F(U')=eta_M(U'),  eta_F(U)<=eta_M(U).

The saved four-mark inequality applies to this SAME full U,U',x and gives

    q-2c+eta_M(U')-eta_M(U)
      <=q-2c+eta_F(U')-eta_F(U)<=0.

F may be chosen separately for each edge: it is a proof witness, not a state
coordinate. The global potential is the single well-defined eta_M, so the
edgewise choices cause no endpoint-sharing or compatibility burden.

## Original closed-walk consequence

Consider an original reachable fully closed Pair Access walk with nonempty
genuine support G. Reuse CD5's exact normalization M_KEEP=G and fixed labeled
B-core S=C_M(B_t). Suppose |S|<=7. Pruning mark-free hanging subtrees preserves
marked depths and commutes with marked splay. Core constancy ensures the
unpruned post-splay tree on S is already the next full core; no node drops on
this closed walk. Thus its KEEP steps meet the inequality above if |M|>=4.
DELETEs freeze B and eta_M. Telescoping gives Q_B<=2C_KEEP<=2C_full<=2A.
For |M|<=3, reuse RT2/CD5; G=empty has Q_B=0.

Therefore CD holds on the union

    |G|<=5  OR  (G nonempty and |C_G(B_t)|<=7 throughout).

This includes the six- and seven-genuine-key cases whose cores have at most7
nodes, uniformly in ambient tree size, DELETE support, length and fringe.
It does NOT prove all six-/seven-key walks: their cores may be larger. Nor
does it extend the K4 formula past7 core nodes, where max-depth=6 no longer
equals existence of a depth-six witness. No mask/population tests were run.

The additional cases are nonvacuous without a finite test: on a fixed6- or
7-key set, repeat the KEEP word visiting all keys in increasing order from a
diagonal. A finite-map recurrent period exists; all adjacent targets differ,
including the seam, so its genuine support is the full set, and its core has
exactly that many nodes. This establishes existence, not a claim of strict
novelty against every older packet class in the research bank.

Any original CD counterexample, if one exists, consequently has at least six
genuine keys AND core size at least eight. This is a proved restricted extension
and localization of the residual, not unrestricted CD or a support induction.

## The next core size: analytic failure of copying the same bit

The bound7 above is essential to this particular copied formula. Choose eight
ordered marked keys g0<g1<h1<h2<z<g2<g3<x. Let H=h1(empty,h2(empty,z)) and

    U=g0(empty,g1(empty,g2(H,g3(empty,x)))).

The path to x is g0,g1,g2,g3,x (depth4). Two original RR doubles give

    U'=x(g1(g0,g3(g2(H,empty),empty)),empty),

where bare key symbols denote leaves. This is obtained by RR on g2,g3,x,
then RR on g0,g1,x; all hanging subtrees are carried by the exact source rule.
Initially the greatest marked depth is5, attained by z. Afterwards z has
depth6 and all other marked depths are smaller. Thus the same copied bit
has eta(U)=0, eta(U')=1, while q=2 and c=1, giving

    q-2c+eta(U')-eta(U)=2-2+1=1>0.

Replacing any empty hanger by an arbitrary mark-free BST in its inorder gap
preserves all marked paths, the two doubles and these values. Thus this is a
source-term family for arbitrary ambient fringe, not a finite experiment.
With A=B=U the original KEEP has a=2,q=2 and actual CD weight2; there is no
CD counterexample. The statement rejects only the same height-six indicator
(also the threshold>=6 version on this family) as a per-edge core8 potential.
No claim is made that every core8 formula or every uniform joint formula fails.
