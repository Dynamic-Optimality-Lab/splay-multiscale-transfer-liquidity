# Exact six key control and source replay

The saved certificate verifies a source-level DELETE failure for L and independently checks the finite arithmetic used to distinguish it from the all-size blend obstruction. It reuses the previous 132-tree, 660-directed-arc primitive rotation corpus. No larger tree corpus, pair graph, or fitted potential is involved.

## Exact endpoint evaluations

Set n=6 and M=4(3(2,empty),5). Then

    A = 1(empty,6(M,empty)),
    B = 2(1,3(empty,4(empty,5(empty,6)))).

Trees are represented completely in root_aligned_countercertificate.json. The two operations are DELETE 6 and KEEP 1, each from this same A,B. Exact maxima over all candidate trees are:

| Function | Source | After DELETE 6 | After KEEP 1 |
| --- | --- | --- | --- |
| L | 197/128 | 533/128 | 2801/4096 |
| U | 405/128 | 533/128 | 16625/4096 |

Thus Delta_DELETE L=21/8>2, Delta_DELETE U=1, Delta_KEEP L=-3503/4096 and Delta_KEEP U=3665/4096. DELETE has (a,q,z)=(1,0,0); KEEP has (0,0,1).

The two necessary blend tests at this size give

    5/13 <= theta_6 <= 3503/7168.

This interval is NONEMPTY. It establishes neither a feasible six-key potential nor a six-key refutation of all blends. No coefficient was chosen. The all-size impossibility in AL03 follows instead from its scalar inequalities for n>=13.

## A complete closed source walk containing the failed DELETE

Start from the diagonal (B,B) and execute

    D1 D4 D6 D1 D6 D5 D1 D2.

Every operation is DELETE; B remains fixed. After the first four operations the actual pair is exactly (A,B). The fifth operation is the failed DELETE 6. The last three restore A to B. The full oriented StepEv lists and both complete trees at every endpoint are saved. Both engines agree, and the actual paired endpoint equals the initial diagonal.

The closed totals are A=12 and Q_B=0, so Coarse-Double holds on this walk. Only L's proposed edge inequality is refuted.

## Independent checks

verify_root_aligned_repair.py produces the certificate from the frozen source engines and the prior metric corpus. It adds one metric BFS from A_d on the SAME 132 vertices. independent_verify.py imports neither the producer nor its formulas for the exact endpoint values. It independently recomputes all 396 integer candidate scores using a depth DFS and scale 8^5, restricts the maxima to the correct root at each endpoint, and validates all six displayed values.

The verifier also regenerates the 660 primitive rotation arcs directly from immutable raw tree tuples. For each of the two metric rows, predecessor paths attain every claimed distance, and the inequality |d(u)-d(v)|<=1 on every primitive arc proves the matching lower bound. Together they certify exact rotation distances. All 132 distinct ordered trees are valid, and the Catalan count 132 proves completeness of the fixed six-key corpus.

Full replay uses the pointer engine, independently of the frame-based producer records. All oriented event lists, source costs, source and destination trees, and exact closure agree. independent_audit.json reports PASS. A rational substitution at n=13 checks 15/7>2; it is scalar arithmetic, not an n=13 graph or finite fit.
