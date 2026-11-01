# The correction failure is reachable in a closed source walk

The n=6 KEEP failure is reached from an actual diagonal and embedded in a closed paired walk. Only its frozen P values and envelope witnesses are evaluated; no potential fit or rotation graph is constructed.

Let T0=B_6=2(leaf1,R_[3,6]). As already certified in the prior root-matching audit, the prefix

    D4 D6 D3 D6 D1

transforms A to A_6=1(empty,6(R_[2,5],empty)) while B stays T0. The following KEEP1 is the failed operation. Its data are

    a=0, q=0, z=1,
    P=1->1, R=2->3, J=3->4, required Delta J<=0.

From the same source, DELETE6 instead has

    a=1, q=z=0,
    P=1->4, R=2->0, J=3->4, required Delta J<=2.

Thus the explicit correction repairs the old DELETE counteredge but creates the registered B failure. A single root zig is also the exact rho=1 witness used in the envelope calculation. Distinct trees give the lower bound, so no metric graph is needed.

The full closed word for the B failure is

    D4 D6 D3 D6 D1 K1 K1 K2 K3 K4 K5 K6 K5 K4 K3 K2 K1 K2.

The first K1 is the failed edge at zero-based position 5. The repeated K1 is a harmless common root access. Common ascending requests 1,...,6 then descending requests 5,...,1 synchronize both trees at R6; KEEP2 restores both to T0. Complete source replay gives

    A_total=18, Q_B=0, Z_B=12.

The final actual A and actual B trees equal their initial trees. This is not a Coarse-Double counterexample. No numerical J labels or summed J changes are claimed for the other replay states. J is a defined function on all states, so physical closure would imply its telescoping identity mathematically; that fact does not repair its failed edge bound.

The [certificate](p_envelope_certificate.json) supplies eight hand matching/cover certificates: the four P evaluations in PE02 and their reflections. It includes four full source controls (DELETE and KEEP, each orientation), the distance witness and all 18 replay steps. The producer compares the immutable tuple source and pointer source, including every oriented grouped event. It uses no matching solver, BFS, auxiliary-tree enumeration, metric graph, pair graph or fit.

The [independent verifier](independent_verify.py) imports neither producer nor tuple source. It reconstructs every proper interval and root-eligibility decision, verifies all residual edges and exact matching/cover equalities, recomputes P and R, checks the envelope arithmetic using PE02's analytic global upper bounds and the attaining one-zig witness, and independently replays all physical endpoints, costs and closure with the pointer source. The global auxiliary upper bounds themselves are the written all-size argument in PE02, not an exhaustive finite verification or formal-kernel proof.
