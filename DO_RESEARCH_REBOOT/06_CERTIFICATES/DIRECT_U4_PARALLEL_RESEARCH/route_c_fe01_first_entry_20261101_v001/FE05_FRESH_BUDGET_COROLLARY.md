# FE-fresh accepted-cut corollary and exact reservation loss

**PROVED—UNIVERSAL**, using FE02's safe source facts and the unchanged
RC01/PG01 cyclic minimum-prefix construction. This asserts a sufficient
source-budget class, not that Gamma_FE is nonpositive universally.

## 1. Single-cut exact identity

For a fixed physical cut let r_j be FE's actual frozen reservation, s_j=C_j-r_j
its suffix offer, and lambda_j=r_j-q_j>=0 at a nonpositive block; set
lambda_j=0 at positives. Put x_j=delta_j at positives and x_j=-s_j otherwise.
FE03's original FIFO/retirement rules give

    x_j=delta_j+lambda_j,
    D_t=max(0,D_(t-1)+x_t), D_0=0.

Let X_0=0, X_t=sum_(j<=t)x_j. Induction yields

    D_N=X_N-min_(0<=b<=N)X_b
       =max_(ending suffix I, including empty) sum_(j in I)x_j.    (1)

For a rejected cut select the LAST global prefix minimum. Its following
canonical busy suffix I has every nonempty prefix balance positive and

    D_N=sum_(j in I)(q_j-2a_j)+sum_(j in I)lambda_j.               (2)

Retain ALL original source facts before I, even paid anchors. No retired
unit before I is imported: a fact is not a pool. This is an OPEN-suffix
identity and is not a closed CD counterexample criterion. For the full cut
the unclipped signed balance is Q_B-2A+sum lambda; terminal debt additionally
has the prefix-minimum correction in (1). It cannot be discarded as banking.

## 2. Fresh source budgets

If positives exist, partition the physical cycle into runs, each a positive
anchor i followed by nonpositive payers up to the next positive. For each
payer j use ONLY this run anchor's FE fact and put

    rho_j=min(C_j,c_FE(i,j)),
    f_j=C_j-rho_j,
    lambda_fresh,j=rho_j-q_j>=0,
    T_i=sum_(j in run i, j!=i) f_j,
    g_i=delta_i-T_i.

Every physical payer is used once. A KEEP-less payer has q=0, rho=0, f=C
and lambda_fresh=0. Let L_FE,fresh sum f only over KEEP-containing payers.
Then exactly

    Gamma_FE := sum_i g_i
             = E-C_D-L_FE,fresh
             = Q_B-2A+Lambda_FE,fresh,                            (3)
    Lambda_FE,fresh=sum_nonpositive lambda_fresh,j.

Because c_FE<=c_PF, fresh reservations and losses decrease, offers increase,
and Gamma_FE<=Gamma_PF. This alone does not prove strict accepted coverage;
FE04 supplies the separate source witness for that claim.

## 3. Constructive cut proof

An auxiliary conservative queue uses the current run anchor's single fresh
reserve and lends its suffix to ANY oldest residual, including older runs.
Within a run only its first block adds debt. Its exact end-of-run recurrence is

    Dhat_next=max(0,Dhat+g_i).

Surplus is retired, not banked. Write G_0=0,G_t=sum_(i<t)g_i for the p
positive runs. If G_p=Gamma_FE<=0, choose q minimizing G_0,...,G_p and
cut at positive run q modulo p. Every ending suffix of that rotated order
has sum at most zero: for a suffix starting t<q use G_q-G_t<=0; for t>=q
use Gamma_FE+G_q-G_t<=0. If q=p, use cut0 and Gamma_FE-G_t<=0. By (1),
the auxiliary queue ends empty after exactly one period.

At this cut every payer's fresh anchor has already appeared in the pass.
Actual FE retains that anchor, even after payment; its minimum reservation
is no greater than rho and its suffix no smaller than f. Block induction
then gives D_FE<=Dhat, so FE ends empty at the SAME constructed cut. Thus

    Gamma_FE<=0 ==> a successful FE physical cut.                  (4)

No successful cut was assumed, and no private run ownership was required.
FE03 supplies distinct physical-unit accounting even with shared payers,
paid facts, repeated coordinates and wraparound. Empty/no-positive closed
walks pay locally; the inherited fixed-root closure handles A=0. Mixed
blocks, genuine zero-double zigs, arbitrary fringes and both orientations
keep their original definitions.

## 4. Designated witness and remaining boundary

The new FE fresh certificate for W has precisely one offered unit, at phase2,
and unused reserved-prefix loss28. Therefore

    Gamma_FE(W)=1-0-1=-28+28=0,
    Gamma_FE(W_m)=0,
    Gamma_PF(W_m)=m>0.

The all-m assertion follows from the exact returning source identities,
not replay. FE04 independently proves the actual FE pass and physical loan;
it does not merely cite (4). This explicitly supplies the necessary strictness
witness beyond PF.

For arbitrary source walks no universal Gamma_FE<=0 theorem is asserted.
Gamma_FE>0 need not imply FE rejection, because older retained facts may
improve on fresh ones. All-cut FE rejection implies Gamma_FE>0; every genuine
CD counterexample would also have to satisfy it. Nonemptiness, impossibility
and complete coverage of that remaining domain are NOT established here.
