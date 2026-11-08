# PF-fresh source budget and exact reservation loss

Status: **PROVED—UNIVERSAL**, on the admissible finite closed Pair Access
source domain, conditional only on the already proved source facts of RC01
and PF01. This changes neither algorithm. It asserts no strict FI/PF
closed-walk inclusion and no universal sign for Gamma_PF.

Use RC01's cyclic maximal A-root blocks. Each nontrivial leader has actual
A StepEv cost a_j>=1 and physical capacity C_j=2a_j. Its at most one genuinely
B-changing KEEP has B-double demand q_j; put delta_j=q_j-C_j. Root no-op
followers create no new pool. DELETE freezes B and retains the key. A mixed
DELETE/KEEP root block is KEEP-containing and is counted once. C_D counts
only KEEP-less blocks. Genuine B zigs count in the intervention clock even
when they have zero double demand.

## 1. Exact unchanged source ceilings

For a positive anchor i let T_i be its B destination and h_i(y)=d_T_i(y).
For a later KEEP-containing payer j with root key y let k_i(j) count genuine
B changes strictly between i and j. If k>=1 let z be the first such access.
The unchanged PF ceiling is

    c_PF(i,j) = floor(h_i(y)/2),                  k=0;
             = floor(U_PF(T_i,z,y)/2)+k-1,        k>=1.

For KEEP-less payers it is zero. U_PF is precisely PF01's source-entry
formula: only the specified parent-outer fringe LR/RL entries replace
allowance 2 by 0. No further role is changed here. Its source proof gives
q_j<=c_PF(i,j)<=c_FI(i,j), with arbitrary fringes and both orientations.
The ceiling is determined before future payer demand is evaluated; neither
observed q_j nor observed first-post depth chooses it.

## 2. Exact one-cut reservation-loss decomposition

Fix one physical cut, start with empty source history and no residual debt,
and traverse exactly one period. PF retains every encountered positive fact,
including paid ones. At a nonpositive payer its reservation is

    r_j = min(C_j, min_encountered_i c_PF(i,j)),

or C_j if there is no fact. Soundness and nonpositivity give q_j<=r_j.
The own demands use [0,q_j), and only [r_j,C_j) is offered once under FIFO.
Define s_j=C_j-r_j and lambda_j=r_j-q_j>=0 at such payers; lambda_j=0 at
positive blocks. Put x_j=delta_j on positives and x_j=-s_j on payers. Then

    x_j = delta_j+lambda_j
    D_t = max(0,D_(t-1)+x_t),                 D_0=0.

With X_0=0 and X_t=sum_(j<=t)x_j, direct induction gives

    D_t = X_t-min_(0<=b<=t)X_b,
    D_N = max_(0<=b<=N) sum_(j=b+1)^N x_j.

If D_N>0, choose b as the LAST minimum of X_0,...,X_N. The busy suffix
I=(b+1,...,N) starts at a positive block, every nonempty prefix has positive
balance, and

    D_N = sum_(j in I)(q_j-2a_j) + sum_(j in I)lambda_j.       (1)

All source facts before b stay in the reservation calculation. Those facts
are not credits: no retired pool before b is imported into I. Each offered
suffix inside I is fully spent because debt remains positive. This is an
exact OPEN-suffix identity, not a closed-walk violation criterion. Individual
cut rejection says nothing about other cuts.

For the full fixed cut the signed, unclipped balance is likewise exactly

    sum_j x_j = Q_B-2A + Lambda_actual(c),
    Lambda_actual(c)=sum_nonpositive(r_j-q_j).

The clipped terminal debt additionally includes the negative-prefix correction
-min X. Omitting it would incorrectly bank discarded capacity.

## 3. PF-fresh run decomposition

If positives exist, partition the physical cycle into runs: a positive anchor
i, followed by all nonpositive blocks up to the next positive. At each payer
j in that run use only this nearest cyclic positive source fact and define

    rho_j = min(C_j,c_PF(i,j)),
    f_j = C_j-rho_j,
    lambda_fresh,j = rho_j-q_j >= 0,
    T_i = sum_(payers in run i) f_j,
    g_i = delta_i-T_i.

Let L_PF,fresh sum f_j only over KEEP-containing nonpositive blocks. Every
KEEP-less block has q=0, rho=0, f=C and lambda_fresh=0. Every physical payer
belongs to exactly one run. Therefore

    Gamma_PF := sum_i g_i = E-C_D-L_PF,fresh
             = Q_B-2A + Lambda_PF,fresh,                    (2)
    Lambda_PF,fresh := sum_nonpositive lambda_fresh,j.

Equation (2) is the requested exact reservation-loss decomposition. In
particular Gamma_PF>0 can be caused entirely by protected unused prefixes on
a walk with ample actual source capacity. It is not a CD counterexample.

The inherited ceiling comparison gives rho_PF<=rho_FI, hence
L_PF,fresh>=L_FI,fresh and Gamma_PF<=Gamma_FI. Strict inequality for a directed
span does not prove strict closed-walk coverage.

## 4. Constructing the successful cut

Consider an auxiliary FIFO queue using only these fresh reservations. It
offers each payer's suffix to the oldest residual, including debt from an
earlier run, and discards surplus when the queue is empty. Within run i the
only positive input is its first delta_i. Hence the exact run-boundary update is

    Dhat_next = max(0,Dhat_current+g_i).

Index the p runs 0,...,p-1. Let G_0=0 and G_t=sum_(i<t)g_i. Suppose
Gamma_PF=G_p<=0. Choose q minimizing G_0,...,G_p and cut at positive run
q modulo p. Every ending suffix of the rotated run order has nonpositive sum:
for a suffix starting at t<q the sum is G_q-G_t<=0; for t>=q it is
Gamma_PF+G_q-G_t<=0. If q=p, identify it with run 0 and use
Gamma_PF-G_t<=0. The empty suffix contributes zero. The clipped-queue
identity thus gives Dhat_end=0 after this one period.

At that cut every payer is preceded by its run anchor in this same pass.
Actual PF retains that anchor even when it is already paid. Its reservation
is no larger than rho_j, and its offer is no smaller than f_j. Positives add
the same debt. Block induction yields D_PF<=Dhat. Consequently

    Gamma_PF<=0  ==>  PF has a successful physical cut.       (3)

No successful cut was assumed. The minimum-prefix construction supplies it.
No startup, other-cut or second-period credit was used. Each A unit has
identity (period occurrence, block occurrence, A-event index, bit); demand
identities include physical B-event occurrences. Own prefixes, offered
suffixes and different pools are disjoint, and recipient cursors advance
once. This proves an actual distinct-unit injection at the constructed cut,
including interactions between successive positives and shared FIFO payers.

## 5. Boundaries and the remaining class

No-positive walks pay all doubles locally. Empty and A=0 closed walks have
Q_B=0 by the inherited fixed-root closure argument; arbitrary open fragments
with unfunded root no-ops are not being asserted to have that property.
One-positive, all-positive and wraparound runs obey the same formulas. Mixed
blocks, repeated coordinates, B-root no-ops, zero-double genuine zigs,
arbitrary finite lengths and all ordered key sets retain the inherited
source semantics. No fixed n or maximum fringe depth enters this proof.

The contrapositive is only

    all-cut PF rejection ==> Gamma_PF>0.

Every genuine CD counterexample lies in that necessary domain as well,
since PF success supplies an injection. There is no converse assertion and
no proof that this domain is empty. The companion fixed-source certificate
in this campaign tests that boundary without changing PF. Universal
Coarse-Double and the arbitrary-history one-unit closure theorem remain open
unless separately proved. Matching-terminal and Stage 11G stay frozen.
