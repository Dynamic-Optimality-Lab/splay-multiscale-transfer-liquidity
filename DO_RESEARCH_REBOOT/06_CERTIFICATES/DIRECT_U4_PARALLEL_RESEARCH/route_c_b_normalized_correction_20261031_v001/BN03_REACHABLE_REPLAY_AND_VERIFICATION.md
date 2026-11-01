# The normalized correction failure occurs in an actual closed walk

Start diagonally at the B path displayed in BN02. The existing L-helper closed word is D1 D3 D6 D2 D6 K2 D5 D2 K1 K4 K6. Replace its K2 by D2 K2, splitting the original A-then-B execution without changing its combined endpoint or cost totals. The new full word is

    D1 D3 D6 D2 D6 D2 K2 D5 D2 K1 K4 K6.

The six DELETE prefix reaches (A*,B) from BN02. The KEEP2 at zero-based position6 is the failed starved B access. Both actual trees return to the initial trees after the final KEEP6. The source totals are

    A_total=16, Q_B=4, Z_B=2.

This walk satisfies Q_B<=2A_total and is not a Coarse-Double counterexample. The exact source costs and physical closure establish the counteredge's original-domain reachability. No new connector search is needed.

The [certificate](b_normalization_certificate.json) has fourteen local P graphs: eight inherited PE graphs and six helper/witness graphs including reflections. Each graph has every proper interval, forced exact pair, eligibility decision, endpoint edge, matching and equal-size vertex cover. The new source maximum M(B)=5 is witnessed by an auxiliary tree rooted at3 (at4 after reflection) whose eligible B side is empty. The destination upper bound M(C)<=4 is the written extremal-leaf argument in BN02, not exhaustive auxiliary-tree evaluation.

The producer compares both immutable source engines for six source controls and the twelve-step replay. The [independent verifier](independent_verify.py) imports neither producer nor tuple source nor a matching algorithm. It reconstructs all graph data, checks matching/cover equalities, verifies the source's depth-five maximizing witness, checks the two extreme leaves at the destination, derives the normalized-potential lower bound, recomputes the scalar-normalization contradiction, and replays all actual endpoints, costs and oriented events with the pointer source.

The new helper control deliberately has bounded values only. No exact J, M or Phi value is assigned to its destination, and no potential labels are claimed on other closed-replay states. The analytic all-size DELETE and old-family repair proofs are written in BN01; finite checks do not establish those quantifiers. No formal-kernel compilation, fit, BFS, matching solver, auxiliary-tree enumeration, metric graph or pair graph was run.
