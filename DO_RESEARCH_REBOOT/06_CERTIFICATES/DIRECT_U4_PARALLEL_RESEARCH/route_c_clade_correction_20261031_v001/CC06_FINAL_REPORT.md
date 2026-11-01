# An unbounded correction to G and its remaining repayment failure

The subtree-set construction gives an explicit unbounded R that cancels the old root-changing DELETE drift, proves DELETE universally, and preserves the arbitrary-fringe zero-weight helpers. It does not preserve full B repayment; a six-key source witness refutes that remaining requirement.

Let C(T) be the exact key sets of T's nonempty node-rooted subtrees, including its full key set. Define

    F(A,B)=n-|C(A) intersection C(B)|,
    R(A,B)=F(A,B)-G(A,B),
    Psi(A,B)=G(A,B)+R(A,B)=F(A,B).

One primitive rotation replaces only one subtree key set. This proves Delta_DELETE Psi<=d_A<=2a. When A is rooted at the accessed key x, a B splay loses no common set and, if nontrivial, creates at least one. Thus Delta_B Psi<=-1. See [the source identity](CC01_SOURCE_ROTATION_IDENTITY.md).

On the old family A=1(empty,n(M,empty)), B=2(1,right-vine3..n), the one-rotation DELETE n has

    Delta G=7(n-3)/8, Delta R=-7(n-3)/8, Delta Psi=0,

for every middle tree M. KEEP 1 from the same pair also passes, with Delta Psi=-1. The correction is unbounded in n and cancels the drift exactly. It is not another root envelope.

The general whole-KEEP bound is

    Delta Psi<=d_A-indicator(d_B>0).

Consequently, the required inequality holds on all q<=1 edges and on q=2 edges with odd A depth, including every earlier arbitrary-fringe helper with d_A=1,q=2. See [the correction and partial laws](CC02_UNBOUNDED_CORRECTION_AND_PARTIAL_LAWS.md).

Full B repayment nevertheless fails. With A the six-key left vine, B the right vine, and KEEP 6, a=0 and q=2 but Psi falls only from 5 to 4; it must fall by at least 2. Analytically, opposite vines refute the formula for every n>=6. A diagonal DELETE also excludes every scalar rescaling c_n F, even with a different coefficient at each size. See [the all-size obstruction](CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md).

[Independent verification](independent_audit.json) passed on nine fixed controls and a complete seventeen-operation closed source replay. The replay has A=19,Q_B=4; it does not refute Coarse-Double. There were zero fits, new source graphs or larger finite corpora. [Exact control details](CC04_EXACT_SOURCE_CONTROL.md) and [reproducibility](CC07_REPRODUCIBILITY.md) are saved here.

The [four-rule gate](CC00_FOUR_RULE_GATE.md) preceded the audit; the [strategy and status record](CC05_STRATEGY_AND_PROOF_STATUS.md) stops this refuted construction. No complete potential or universal Coarse-Double proof was obtained. Stage 11G and all inherited sources remain read-only; delivery checks are in final_integrity.json.
