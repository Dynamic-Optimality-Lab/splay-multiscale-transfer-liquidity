# Exact nonlinear joint-depth certificate at seven keys

**Status: FINITE-EXACT. No all-size invariant is proved.**

For actual BST pairs on seven ordered keys define

    alpha(A,B) = (7, root(A), root(B), H),
    H[u,v] = number of keys x with d_A(x)=u and d_B(x)=v.

All depths count edges. H is the COMPLETE multiset of paired depths, not separate marginal histograms. The exact root key labels are retained. The stored code is [rootA,rootB] followed by the sorted seven values 7*d_A(x)+d_B(x). This is a lossless encoding of this fixed-n summary; no probabilistic hashes or cell truncation are used.

There are 429 BSTs, 184,041 physical paired states and 90,812 distinct summaries. Every physical pair lies in the explicitly computed recurrent component of the right-vine diagonal anchor: both a reachability path and a path back exist. The transition table has 2,576,574 KEEP/DELETE edges. The two physical engines agree on all 3,003 shape/access transitions, including whole final trees and ordered StepEv traces.

For each exact summary edge, use the MAXIMUM reward q-2a among its concrete representatives, and retain a source representative. There are 1,842,798 summary edges. Thus a potential satisfying this quotient's inequalities covers every concrete transition; this direction does not require lifting abstract cycles to physical ones.

Exact integer label correction completed in five passes, 9,213,990 edge scans. The result is the explicit table Phi7 in {-3,-2,-1,0} saved in finite_summary_potential.json. Every original seven-key transition satisfies

    q(e)-2a(e) <= Phi7(alpha(source))-Phi7(alpha(destination)).

An independent checker rebuilt all source transitions with the pointer engine, independently regenerated all features and checked EVERY one of the 2,576,574 concrete inequalities. Minimum residual0, maximum9. It imports neither the quotient generator nor its label-correction code. This finite certificate is exact; no floating solver or rounded value is involved.

Summing gives the finite theorem for ANY length and any seven-key physical path:

    Q_B(path)-2A(path) <= Phi7(start)-Phi7(end) <= 3.

For an exactly closed paired walk the potential boundary is zero, so Q_B<=2A. This holds for repeated/nonprimitive walks and arbitrary occurrence masks in that seven-key domain. Order-preserving relabeling transfers the finite theorem to any seven-element totally ordered set. It does not transfer it to a larger key count.

This is NOT new coverage of Coarse-Double: the repository already has finite seven-key certificates. The new finite observation is that a complete nonlinear joint-depth summary suffices here; full keyed tree state need not be retained at n7. Its all-size sufficiency remains unproved and unrefuted by this run.
