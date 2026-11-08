# Conflict counts and a maximum access profile also lose needed geometry

These rejections continue the investigation after the rotation-distance
obstruction. They do not refute original CD or exclude all richer potentials.
All n-variable families and gap substitutions are symbolic; no finite tests.

## 1. The count of unmatched subtree intervals has the same obstruction

For a full labeled BST let its clusters be the key sets of subtrees rooted
at every node, excluding the whole-tree root cluster. Let C(A,B) count B
clusters absent from A. All proper clusters inside the identical rigid
gap BSTs F_i are common and contribute0. Different distinguished-key sets
cannot be equal full clusters under any legal gap substitution.

In the rotation-distance family, at prepared state A_j versus R_n the
common distinguished proper clusters are precisely the suffix clusters
starting at k(j+1),...,kn. The unmatched count is j-1. At A=L_n versus R_n
it is n-1. After the starved KEEP, B' has left child k1 containing ALL
lower distinguished keys, giving exactly one shared proper prefix cluster.
Every other distinguished proper B' cluster omits k1, whereas all proper
distinguished L_n clusters contain k1. Thus C(L_n,B')=n-2.

Consequently the last DELETE and starved KEEP have BOTH coordinates

    (dist_rot,C): (n-2,n-2) -> (n-1,n-1) -> (n-2,n-2),

with total original weight2-q<0. No arbitrary function of this pair, even
with fixed ambient-size parameters, can certify all edges. Adding fixed
core size, support size or core deficiency does not distinguish these
three states; all are constant in the closed family. This is a projection
failure, not a closed original counterexample.

## 2. A plausible maximum over all prospective access deficits fails

Define independently of the current requested key

    Phi(A,B)=max(0,max_v[floor(d_B(v)/2)-d_A(v)]),           (1)

where the maximum ranges over present keys. DELETE has the desired safe
Lipschitz law: its actual d_A(x) primitive rotations change each other
depth by at most that many in total, so each expression in (1) increases
by at most d_A(x)<=2a. Taking a maximum preserves that upper bound.

However, use even n=2k with k>=4 and the reachable state (L_n,R_n). For
distinguished key ki its expression is floor((i-1)/2)-(n-i), maximized at
kn with value k-1=q. For a node of internal depth t in a gap hanger,
its expression is at most the expression at that hanger's root, since
floor((b+t)/2)-(a+t) is nonincreasing in t. For gap F_j, j<n, its source
root offsets give at most k-2; gap F_n gives at most k-1. Hence exactly
Phi_before=q, including arbitrary nonempty hangers.

After starved KEEP kn, the original RR-frame induction puts k(n-1) at
B' depth k. It remains at A depth1. Thus

    Phi_after >= floor(k/2)-1 >=1.

The KEEP has a=0 and weight -q, but Phi_after-Phi_before>=1-q>-q. Thus (1)
fails its required KEEP edge law, despite its valid DELETE law. A maximum
can store the largest prospective demand while another substantial demand
survives servicing that key. There is no single-coordinate reset invariant.

## 3. The updated proof obligation

A useful state must encode how oriented source paths share and transfer
credit. Multiplicity-sensitive sums need a source capacity proof; maxima,
rotation distance and interval counts erase needed service information.
The exact signed cross-key term and explicit removable-excursion capacity
remain valid. Neither supplies universal existence or repayment on its own.
The next attempt must connect actual A rotation ancestry to B-double
consumers without replacing that missing connection by the target inequality.
