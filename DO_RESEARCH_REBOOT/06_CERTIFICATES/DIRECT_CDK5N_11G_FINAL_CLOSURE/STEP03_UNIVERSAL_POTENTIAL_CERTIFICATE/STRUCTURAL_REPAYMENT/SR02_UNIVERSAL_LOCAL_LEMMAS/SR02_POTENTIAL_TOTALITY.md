# SR02 Potential Totality + Feature Semantics (Gate A)

R=b_rank_sum: total (windowed log2 sizes, sentinels excluded, unreachable
->eval None only on invalid states; total on all 246 stored valid endpoints).
D=b_depth_max: parent-walk depths, range 0..8 (9 core nodes; validity forces
connectivity; max 8 attained). M=a_marked_count: shadow S-positions (0..7;
DISTINCT from global 5-marked invariant — documented). R_M=b_rank_marked:
marked S-indices only (membership via mu bits). Guard g=1[D>=7]: pure vertex
predicate (no H/witness/edge data; code-inspected). Grounded/symbolic
agreement: grounded eval recomputed identically (S1 check); symbolic DAG
encoding of ranks/depths NOT constructed (solver-blocked; recorded, not
claimed). Phi total on valid U_O by composition of total features.
