# Rotation distance alone cannot be a uniform CD potential

Status: universal source obstruction to a proposed proof architecture. It
is NOT a counterexample to CD. No finite tree, word or population is run.
The family is parameterized by every even n>=8 and arbitrary rigid gap BSTs.

## 1. Exact distance to a comb with the same gap hangers

Distinguish ordered keys k1<...<kn. Let F0,...,Fn be arbitrary fixed BSTs
strictly in their inorder gaps, containing no distinguished key. A skeleton
BST is any BST on the distinguished keys with these gap BSTs substituted
at its external leaves. Its distinguished left-spine length ell is the
number of distinguished keys on its absolute leftmost path. Below that
spine the path may enter F0, containing no distinguished key.

Let L_n be the skeleton left comb with these hangers. Every primitive
rotation changes ell by at most1. Indeed only a rotation on the absolute
leftmost path can change that path: a left rotation inserts its former
right-child root, a right rotation deletes its former parent, and off-path
rotations do not alter it. At most one distinguished key is inserted or
deleted, even if the rotated key belongs to an arbitrary F_i.

Consequently the FULL ordinary rotation distance satisfies

    dist_rot(U,L_n) >= n-ell(U).

Conversely, while some distinguished node is absent from the left spine,
some spine node has a right child containing distinguished keys. In a
skeleton tree that right child is itself distinguished; a pure gap hanger
cannot contain a distinguished descendant. Left rotation there increases
ell by1, rotates only distinguished keys, and preserves every F_i rigidly.
Repeat until all n distinguished nodes are on the left spine. The resulting
tree is exactly L_n with the same hangers. This supplies n-ell(U) rotations,
so the lower bound is attained:

    dist_rot(U,L_n) = n-ell(U).                              (1)

The upper construction is a mathematical induction, not an executed search.

## 2. Reachable A preparation with one-StepEv DELETEs

Start at diagonal R_n, the skeleton right comb with the same hangers.
Execute DELETE k2, DELETE k3,...,DELETE kn. Each next target is the current
A root's right child, so each is ONE right ZIG. After DELETE kj, A is the
j-rooted skeleton with left comb on k1,...,k(j-1) and a right comb on the
larger keys. B remains R_n. Its distinguished left spine has length j.
There is a path of j-1 rotations from B to A, and the left-spine lower
bound from ell(B)=1 to ell(A)=j gives the matching lower bound. Therefore

    dist_rot(A_j,R_n)=j-1.                                 (2)

In particular, just before DELETE kn the distance is n-2; afterwards A=L_n
and the distance is n-1. That last DELETE has a=1,q=0, original CD weight2.

## 3. A starved KEEP returns the scalar but not the full state

Next KEEP kn has A at its root, hence a=0. In B the target has depth n-1.
For even n this is odd. Its original bottom-up word consumes only RR
doubles until the old root k1 is the single remaining frame, followed by
one right ZIG. Therefore B' has root kn, left child k1, and k1's left
child is still the rigid hanger F0. Its distinguished left spine has
length exactly2. Equation (1) now gives

    dist_rot(L_n,B')=n-2,
    q=floor((n-1)/2)=(n-2)/2,
    original CD weight=-q.                                (3)

The consecutive two edges thus have rotation-distance coordinates

    n-2 -> n-1 -> n-2

and total original weight2-q<0 for every even n>=8. Their full paired
states DO NOT close. This is a negative closed walk only in the proposed
one-coordinate projection, not an original negative CD cycle and not a
cycle in the frozen nine-core graph.

## 4. Every function of this scalar fails, even at a fixed ambient size

Suppose Phi(A,B)=f(dist_rot(A,B)), allowing f to depend on the chosen
ambient ordered key set, distinguished support or fixed hangers. The same
f is used for both edges. The desired edge law w>=Phi_next-Phi_before
would require from the DELETE

    f(n-1)-f(n-2)<=2,

and from the starved KEEP

    f(n-1)-f(n-2)>=q>2.

Contradiction. No arbitrary nonlinear choice of f repairs the information
lost by this coordinate. A fixed multiple of rotation distance is a
special rejected case. The proof concerns that candidate class only;
potentials using additional ordered source information are not excluded.

## 5. Embedding in a genuine original fully closed family

After the starved KEEP, append Kk1,Kk2,...,Kk(n-1), followed by
Kk(n-2),...,Kk1. On any skeleton tree, scanning consecutive distinguished
keys increasingly leaves the visited keys in a left comb. Inductively the
next distinguished key is the minimum distinguished key in the right
subtree: the original zig or outer RL formula attaches the old visited
comb as its left subtree. Internal double parity does not change it.
At k(n-1), only kn remains on the distinguished right. The descending
scan is then a sequence of left child ZIGs, returning exactly R_n with
every hanger in its original inorder gap.

Thus the complete original period from diagonal R_n is

    Dk2,...,Dkn, Kkn, Kk1,...,Kk(n-1), Kk(n-2),...,Kk1.

Both full trees close at R_n. All n distinguished KEEP keys are genuine;
their full B-core consists of those n nodes throughout. The negative two-
edge scalar projection lies inside this reachable closed original walk.
The remaining edges are not discarded when assessing CD. This argument
does not assert that the full period has negative weight; it supplies a
source-valid obstruction to the projected potential, with arbitrary fringes.

## 6. Revised candidate after the obstruction

Retain an oriented description of which ancestors were moved and which
actual A events created capacity. Two states with the same rotation
distance can have very different immediately available B-double demand.
The excursion reservation lemma supplies one legitimate capacity source;
the signed transport identities retain the missing source geometry. A
uniform transition law linking them, and its exhaustive coverage, remain
OPEN. This failure does not justify terminating the requested campaign.
