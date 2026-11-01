# B normalization loses full repayment on a starved helper

The normalized correction fails an existing six-key full-q B access. Exact upper and lower bounds suffice: the destination potential is at least -2, but the source law requires at most -3. No exact value of the destination envelope or B maximum is asserted.

## Fixed actual source pair

Write omitted children as empty. On keys 1 through 6 use

    A*=2(leaf1,6(3(empty,4(empty,leaf5)),empty)),
    B =6(5(4(1(empty,2(empty,leaf3)),empty),empty),empty).

This B is a six-node path; its final leaf is key3 at depth5. The actual access is KEEP2. A* is already rooted at2, so a=0. Key2 has depth4 in B, giving q=2,z=0. The source B operations are LR on keys 1,2,4 and LL on keys 2,5,6. The destination is

    C=2(leaf1,5(4(leaf3,empty),leaf6)).

A* stays fixed. This is the root-conditioned B phase of the previously established L-helper, reached by doing its A splay first as a DELETE. It is a whole source KEEP with an empty A phase, not an extra micro-step demand.

## Two exact local P values

The proper A* intervals are {1},[3,6],[3,5],[4,5],{5}. B has {3},[2,3],[1,3],[1,4],[1,5]. There are no exact pairs. With root(A*)=2 the only eligible B interval is {3}. It has endpoint neighbors [3,6] and [3,5]. A one-edge matching and the one-vertex right cover prove mu=1, hence

    P(A*,B)=5-1=4.

The proper C intervals are {1},[3,6],[3,4],{3},{6}. Fix the two exact pairs {1} and [3,6]. In the residual graph only the A interval [3,5] has edges, to B intervals {3} and [3,4]. One such edge and the one-vertex LEFT cover {[3,5]} prove residual rank one. Thus

    P(A*,C)=(5-2)-1=2.

All fourteen local graphs in the certificate, including these two and their reflections, have complete matching/cover equalities. The all-auxiliary extrema below do not come from enumerating those graphs.

## Exact source maximum and envelope

Every proper B interval contains key3, because B is a path ending at3. For any auxiliary tree U rooted at3, every proper B interval is ineligible and no exact common interval can contain that root. Therefore P(U,B)=5. For example take U=3(R_[1,2],R_[4,6]). The general range P<=5 supplies the matching global upper bound, so

    M(B)=5.

For the self auxiliary tree A*, the envelope has score P(A*,B)=4. Any different auxiliary tree has integer rotation distance at least one and raw P at most five, hence score at most4. Thus

    J(A*,B)=4, Phi(A*,B)=4-5=-1.

This upper bound covers every auxiliary tree regardless of its root or shape. It requires neither a metric graph nor an attaining one-rotation neighbor.

## A structural upper bound at the destination

Both extreme keys 1 and6 are leaves of C. For ANY auxiliary tree U the total protected root-eligible matching rank at (U,C) is at least one. If there is an exact common interval, the forced pair already proves this. Otherwise:

* If root(U)!=1, the proper U subtree containing key1 has minimum1, and C's leaf interval {1} is eligible. With no exact pairs, these give a residual endpoint edge.
* If root(U)=1, the proper U subtree containing key6 has maximum6, and C's leaf interval {6} is eligible. These again give a residual endpoint edge.

Consequently P(U,C)<=5-1=4 for all U, and M(C)<=4. More generally the same argument proves M(C)<=n-2 whenever both extreme keys of an n-key B tree are leaves; this is a structural conditional bound, not a formula for arbitrary B.

The self term in the envelope gives J(A*,C)>=P(A*,C)=2. Combining the independently proved bounds,

    Phi(A*,C)=J(A*,C)-M(C)>=2-4=-2.

The full q law requires

    Phi(A*,C)<=Phi(A*,B)-2=-3,

which is impossible. Equivalently Delta Phi>=-1>-2. The correction R itself has source value -5 and destination value at least -4: it increases by at least one while raw P spends exactly q=2. The reflection gives the opposite orientation. The argument uses bounds; it makes no claim that M(C)=4, J(A*,C)=2 or Phi(A*,C)=-2.

## Direct obstruction to every scalar normalization of this B maximum

Consider Phi_c=J-c_n M(B), with any finite real scalar chosen separately for each n. The old PE zero-double B edge at n=6 has Delta J=Delta M=1. Its required nonincrease gives

    1-c_6<=0, hence c_6>=1.

On the starved helper, the exact source values and destination bounds give Delta J>=-2 and Delta M<=-1. Since c_6>=1 is nonnegative,

    Delta Phi_c=Delta J-c_6 Delta M>=-2+c_6.

Full q=2 would require Delta Phi_c<=-2, forcing c_6<=0. Thus c_6>=1 and c_6<=0 are incompatible. No scalar multiplier of this M(B) normalization fixes both operations, even with size-dependent coefficients. This is the same two frozen witnesses, not a coefficient fit.

This excludes the stated family J-c_n max_T P(T,B), not arbitrary B-only gauges, different penalties, nonminimal majorants or all unbounded structural corrections. Generic Step 3 and Coarse-Double remain open.
