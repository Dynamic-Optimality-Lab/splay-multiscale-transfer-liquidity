# Exact seven key root zig and closed source replay

The smallest member of the displayed odd family has

    M=3(leaf2,5(leaf4,leaf6)),
    A=1(empty,7(M,empty)), B=R7.

DELETE7 is the actual A-root right zig, producing A'=7(1(empty,M),empty), while B stays R7. The potential completes B at the new root7 to

    V7=7(2(leaf1,4(leaf3,6(leaf5,empty))),empty).

The exact evaluated data are

| Quantity | Before | After |
| --- | --- | --- |
| Terminal F | 5 | 5 |
| Terminal antichain discount alpha | 1 | 1 |
| Terminal K | 4 | 4 |
| Potential-completion doubles Q | 0 | 3 |
| Phi=K+Q | 4 | 7 |
| Actual raw P | 3 | 6 |
| Correction R=Phi-P | 1 | 1 |

The actual DELETE has a=1,q=z=0 and budget2, so its increment3 is a strict violation. The potential-completion count3 is not charged as actual B work. The reflected operation is a left zig with the same values and costs.

Start diagonally at R7. A fixed single-tree connector is

    D4 D7 D3 D5 D7 D1.

It reaches the displayed source pair. The next DELETE7 is the registered failed edge. One bounded n=7 single-tree BFS found this connector, visiting427 of the possible429 trees and evaluating no potential labels during search. The analytic family and its failure were fixed before this reachability computation; no fit or source-pair graph was built.

The complete closed word is

    D4 D7 D3 D5 D7 D1 D7 K1 K2 K3 K4 K5 K6 K7 K6 K5 K4 K3 K2 K1.

The failed DELETE7 is zero-based position6. The final common ascending and descending passes restore both actual trees to R7. Exact totals are A=27,Q_B=0,Z_B=12. The explicit Phi increments telescope to zero; the registered edge is the only failing edge in this recorded replay. This closed walk is not a Coarse-Double counterexample.

The producer loads the prior AT evaluator read-only and calls only its in-memory value/trace helpers. It never calls that module's main or save functions and writes exclusively into this new run. The old evaluator and mathematical definition are SHA256-pinned, so the candidate is unchanged. Both original tuple and pointer engines agree on all actual and completion endpoints and oriented events.

The [countercertificate](root_bound_countercertificate.json) contains every terminal graph, every maximal residual B antichain, matching/cover equalities, raw P graphs, actual source/completion traces and full replay. The [independent verifier](independent_verify.py) imports neither new nor old producer or matching algorithm. It regenerates the interval graphs and every maximal antichain, checks all dual equalities and global alpha optima, recomputes all potential and correction values with the pointer source, and checks the actual root depth, one-ZIG cost, reflection, reachability, sharing and closure.

The all-odd-size proof in RB01 is analytic, not inferred from finite evaluation. The n=7 computation certifies a reachable physical instance within the previously used key sizes. No formal-kernel compilation is claimed, and old AT files retain their historical OPEN disposition unchanged; the new status ledger records the subsequent refutation.
