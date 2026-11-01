# Route C root alignment repair audit

The explicit root-pinned repair of G preserves access-root alignment and proves the uniform B-repayment bound, but it fails DELETE. No complete uniform A/B potential was found in this repair family.

With r=1/8 and primitive rotation distance rho, the tested functions were

    G(A,B)=sum_y r^{d_A(y)} d_B(y),
    U(A,B)=max_T [G(T,B)-rho(A,T)],
    L(A,B)=max_{root(T)=root(A)} [G(T,B)-rho(A,T)].

For root(A)=x and d_B(x)>=1, every auxiliary term in L decreases by at least floor(d_B(x)/2)+1/3 under the B splay. This gives L the required root-conditioned B law on every size and arbitrary fringe configuration. See [the proof](AL01_ROOT_PINNED_B_LAW.md).

For A=1(empty,n(M,empty)) and B=2(1,right-vine3..n), DELETE n costs a=1 but forces

    Delta L >= (2n-7)/3 > 2, for every n>=7.

The exact n=6 control already gives Delta L=21/8. The same argument excludes normalized root envelopes with arbitrary nonnegative zero-self penalties. See [the DELETE obstruction](AL02_DELETE_BAND_OBSTRUCTION.md).

Blending with U cannot repair both laws, even if the coefficient is chosen separately for every n. KEEP 1 from the SAME source forces theta_n<=4/7, while DELETE n then gives

    Delta[(1-theta_n)L+theta_n U] >= (2n-11)/7 > 2, n>=13.

This is an analytic all-size contradiction, not a fit or extrapolation. It excludes this entire size-dependent convex family. See [the blend proof](AL03_SIZE_DEPENDENT_BLEND_NO_GO.md). Source reachability for these arbitrary-size pairs follows from [Levy and Tarjan, Theorem 3.4](https://arxiv.org/html/1907.06310v3#S3), as explained in the DELETE proof.

[Independent verification](independent_audit.json) passed on the existing six-key metric corpus and the complete eight-DELETE closed replay. The finite blend tests have a nonempty necessary interval; no finite infeasibility or sufficiency is claimed. The closed word has Q_B=0 and does not refute Coarse-Double. See [the exact control](AL04_EXACT_CONTROL_AND_REPLAY.md).

The [four-rule gate](AL00_FOUR_RULE_GATE.md) preceded this bounded audit. The [required strategy review](AL05_STRATEGY_REVIEW.md) records two consecutive envelope failures and stops automatic variants. Strategic elimination is established; no original Coarse-Double obligation is discharged. The uniform potential, Coarse-Double, and downstream Dynamic Optimality proof remain open or conditional as before.

All outputs are append-only here. No larger finite fits, new pair graphs, installs, commits, or Stage 11G edits were made. Preservation details are in final_integrity.json; reproducibility is in [AL07](AL07_REPRODUCIBILITY.md).
