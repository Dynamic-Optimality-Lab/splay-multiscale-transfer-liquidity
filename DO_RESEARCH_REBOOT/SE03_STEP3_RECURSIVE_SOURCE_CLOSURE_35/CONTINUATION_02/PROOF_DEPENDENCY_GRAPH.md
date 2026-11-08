# Dependency graph

UCF35 <- SRC35 + COMPAT35 + OWNER35, with original legitimate E_r1 input.
SRC35 <- SC35 + SIMPLE35. SC35 reuses the support<=6 base and strictly
shorter closed children. SIMPLE35 is the covered-family intersection plus
OTHER_SIMPLE35. AF35 <- RC35 + DS35 + inherited exact B frame induction.
OWNER35 is inherited support-free full comparison exchange. FD35 gives
the precise all-license falsification burden, not source feasibility.

proof_boxes_v3.json is the executable dependency/status registry. Edges
marked reductions or conditional interfaces never promote an open child.
The old SI34 root remains separately REFUTED and has no negative edge
to UCF35. No circular dependence on CD(r), Step3, or Dynamic Optimality
is introduced. All new source proofs are independent of the supplied fE.
