# G03R Piecewise-Candidate Analysis

Guard `g(s) = [b_depth_max(s) >= 6]`: pure vertex function (no H, no witness).
Per-region fits all SAT, but region-pair evaluation breaks telescoping, so a
JOINT LP (theta_0, theta_1; edge uses piece of its own endpoints; single-valued
`Phi(s) = theta[g(s)].f(s)`) was fit: SAT with large coefficients. Grounded
falsification of the telescoping joint potential: 12/40 violations — REFUTED.
Min-plus `min_i Phi_i` was not promoted (no surviving pieces). Conclusion:
depth-guarded piecewise affine over the 16-feature language does not
generalize either; the failure localizes to deep-chain transitions. Universal
`V_w(Phi)` queries not run (no surviving candidate). (`G03R_POTENTIAL_CANDIDATE_RESULTS.json`,
`G03R_PIECEWISE_FALSIFY.json`, `G03R_UNIVERSAL_VERIFICATION_RESULTS.json`:
1.6M-node product compiles; family root present; probe UNKNOWN.)
