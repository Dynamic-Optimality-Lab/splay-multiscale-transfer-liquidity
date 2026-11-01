# Reproducibility of the cross run source certificate

The [producer](audit_cross_run.py) uses the immutable tuple source. The [independent verifier](independent_verify.py) uses the pointer source, validates raw BST inputs and reconstructs every greedy trial and resource map. Neither imports a matching evaluator, allocation optimizer, old recognizer or Stage 11G code. Both disable bytecode and create outputs exclusively with mode x.

The original run used Python `-X utf8 -B`. To reproduce, copy the scripts and preexecution gate into a fresh versioned sibling directory, run the producer, then the verifier. Do not rerun over sealed outputs. The new entry will additionally pin this run as previous research.

The corpus is one fixed thirteen-key source word derived from SP by one DELETE insertion, plus reflection and all six prior SP/DS/SC controls. No key-size expansion, word hunt, finite fit, source-state graph or solver is used. The all-size source theorem and fringe/unbounded-support family are analytic arguments in XR01/XR02, not finite extrapolation.

The verifier checks 256 cycle rows, twelve diagonal-prefix rows, 1,096 strict BST tree occurrences and all 256 block-cut trials. There are 236 accepted alternative covers and 20 rejected trials with unpaid debt. Selected covers contain 186 actual unit assignments. The 6,286 assignment checks over alternative accepted passes are per-cover verifications, never a combined credit budget. The pointer source is called 510 times.

The certificate SHA-256 is `f5c94e4e0784dc6dc02f4240314f1980ed42c6746677e27813e1474d0bbe3448`. Every preserved source row and total is unchanged. The inserted DELETE lends no credit, the saturated KEEP pays locally, and the selected payer pool is reserved only once. Prefix and second-lap units are excluded.

Entry/final hashes preserve 576 inherited/source/previous-run files, all 125 Stage 11G files and their inventory, current HEAD/branch and tracked status. The matching-terminal freeze notice remains pinned and unchanged. All previous statuses and historical untracked material remain intact. The delivery manifest hashes every new artifact except itself.
