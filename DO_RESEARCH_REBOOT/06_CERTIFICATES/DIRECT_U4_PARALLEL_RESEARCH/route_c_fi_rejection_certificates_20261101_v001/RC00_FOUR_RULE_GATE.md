# Exact FI rejection certificates and a strict source-budget obstruction filter

2026-11-01, Asia/Karachi. This one bounded campaign is authorized by the request to derive exact FI rejection certificates and isolate a strictly smaller source obstruction class. No new source word, size, repetition count, splay engine, fit or allocation optimizer is used. All previous files, source, tests, configuration, Git and Stage11G are read-only. Matching-terminal stays FROZEN. Outputs are exclusive creations in this fresh directory.

## Principal theorem and predetermined proof mechanism

Work with the established cyclic maximal A-root blocks and the unchanged FI protocol. At block j let C_j=2a_j and delta_j=q_j-C_j. Positive blocks add e_j=delta_j debt and use all their own units. At nonpositive payers FI retains every encountered positive fact, including paid anchors, freezes reservation r_j and can lend s_j=C_j-r_j once. Empty history means r_j=C_j and s_j=0. Facts are not credits.

For a fixed one-period cut c set x_j=delta_j on positives and x_j=-s_j on payers. The queue obeys D_t=max(0,D_(t-1)+x_t),D_0=0. Prove

    D_N = X_N - min_(0<=t<=N) X_t
        = max_(suffix I, including empty) sum_(j in I) x_j,

where X_t is the prefix sum. When rejected, choose the LAST global minimum of X. The following terminal busy suffix starts at a positive block, has strictly positive balances at every nonempty prefix, and has terminal imbalance exactly D_N. Reservations use the ORIGINAL full cut history, including paid facts before the suffix. No prefix unit is imported. On a payer let lambda_j=r_j-q_j>=0, and set lambda=0 on positives. Then x_j=delta_j+lambda_j, so the exact certificate splits source cost imbalance and unused reserved own-work capacity. This identity alone is bookkeeping and is NOT counted as an advance of universal CD.

The substantive reduction uses a cyclic SOURCE-LOCAL budget. If positives exist, partition the physical cycle into runs: a positive anchor followed by every nonpositive block up to the next positive. For each payer j use only the current run anchor's established FI source ceiling c_fresh(i,j). Define

    f_j = C_j-min(C_j,c_fresh(i,j)),
    T_i = sum_(payers in run i) f_j,
    g_i = e_i-T_i,
    Gamma = sum_i g_i = E-C_D-L_fresh,

where L_fresh is the sum of f_j on KEEP-containing nonpositive blocks. Every KEEP-less block has source ceiling0 and is counted once in C_D. The source fact remains valid even after its anchor is paid. Actual FI retains that anchor, so its minimum reservation is no larger and its available suffix is at least f_j.

An auxiliary conservative FIFO queue, using these fixed suffixes and no private ownership, has run-boundary recurrence D'=max(0,D+g_i). If Gamma<=0, choose a positive-run cut after a minimum prefix sum of the cyclic g_i. Every ending suffix sum is nonpositive, so the auxiliary queue clears in one period; FI's total-debt domination gives a real successful FI cut. All pools are physical, visited once and retired; extra offers with empty debt are discarded. This is a constructive cut proof, not an assumed cut or aggregate-bank argument.

Therefore every all-cut FI rejection, and hence every genuine counterexample to universal Coarse-Double, must lie in the necessary source class

    O_fresh = {reachable closed source walks: E>C_D+L_fresh}.

It is a proper subclass of the older candidate class E>C_D: the proved H_m family,m>=5, has at least one fresh KEEP5 unit per positive, so L_fresh>=m and Gamma<=-4 while E=m>4=C_D. The theorem removes all E>C_D cases with Gamma<=0 without an accepted-cut existence assumption. It does NOT assert Gamma<=0 universally, Gamma>0 sufficient for FI rejection, or nonemptiness/impossibility of O_fresh. No matching-terminal object is involved.

As an algebraic source corollary, only bounded-fresh facts can release units: if k>=1 then c_fresh=floor(U/2)+k-1. Positive offer is equivalent to k<=C and U<=2(C-k)+1. For k=0 it is equivalent to h<=2C-1. These are exact integer conditions, with no constant-depth or fringe restriction. They supply the concrete geometric content of L_fresh.

## Fixed validation corpus, not a new fit

Validate only the twelve already source-verified ordinary/reflected witnesses in the old FI certificate(n=7 or13), plus the existing H5 ordinary/reflected walk. Their recorded FI outcomes provide432+204=636 existing cuts, including44 rejected cuts. Do not add witnesses if no residual-class example appears. Reconstruct source blocks/facts, the recurrence and every busy-suffix certificate; independently check the old outcomes, full-history reservations, terminal debt, reserved-loss split and source-frame provenance. For each source cycle compute fresh-run budgets and the explicit minimum-prefix cut when Gamma<=0, with distinct-unit verification of its actual FI pass. No additional m or n is constructed/replayed. The universal proof comes from the recurrence and cyclic cut argument, not these finite controls.

## Four rules before execution

1. **Strictly smaller — PASS.** One scalar-debt normal-form theorem with source ceilings already proved. It reduces full cut-history scheduling to exact suffix certificates and, for the substantive accepted class, nearest-positive run budgets and a determined minimum-prefix cut. The remaining source inequality is stronger than E>C_D and needs no cut quantifier.
2. **Concrete reason — PASS.** Unrolling the clipped queue gives the certificate directly. Source-fact min domination and the positive-run recurrence yield a complete cycle-minimum proof whenever Gamma<=0. The known H_m identity proves strictness of the remaining filter without a new source witness or numerical hope. Freshness bounds follow by exact floor arithmetic.
3. **One-prompt scope — PASS.** One cyclic deficit theorem and its source-local budget consequence, with one fixed old-corpus audit and independent checker. No second open return, universal budget bound, new witness search, frame repair or all-FI completeness premise is assumed. Stop after this theorem and audit.
4. **Exact obligation — PASS subject to proof.** The suffix identity alone earns no CD advancement. Success additionally deletes the accepted-cut burden for EVERY source walk with Gamma<=0, including the proper nonempty class E>C_D but E<=C_D+L_fresh. The source restriction Gamma>0 is proved NECESSARY for any remaining counterexample; it is not an optional extra premise or equivalent global-existence restatement. Universal CD on that stricter class remains OPEN and is not claimed solved.

Handle empty/no-positive/all-positive boundaries, mixed KEEP/DELETE root blocks, zero-double genuine zigs, repeated keys, arbitrary fringes, wraparound, retained paid facts and unit multiplicity. Record BEFORE/RESULT/AFTER, deleted obligations, assumptions and NET PROOF ADVANCEMENT, separating diagnostic normalization from genuine one-sided coverage. Pin all inherited files, prior inventory, all125 Stage11G files and unchanged HEAD/branch/tracked status before and after. Stop on a failed proof case; do not automatically pivot after OPEN. No larger finite fit or automatic successor follows.
