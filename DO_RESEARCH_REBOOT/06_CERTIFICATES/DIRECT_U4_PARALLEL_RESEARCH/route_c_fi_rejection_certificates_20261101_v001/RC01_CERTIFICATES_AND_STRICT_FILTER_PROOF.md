# Exact FI rejection certificates and a strictly smaller source obstruction domain

2026-11-01, Asia/Karachi. The exact debt identities and the source-budget coverage theorem below hold for every finite admissible closed Pair Access source walk, with the established FI rules. They impose no fixed depth, fringe, key-count or sharing bound.

The substantive result is

\[
\boxed{\Gamma(W):=E(W)-C_D(W)-L_{\rm fresh}(W)\le0
\quad\Longrightarrow\quad W\in FI.}
\]

The proof constructs a positive-block cut; it does not assume one exists. Consequently any remaining all-cut FI rejection, and any genuine Coarse-Double counterexample, must belong to

\[
\mathcal O_{\rm fresh}
=\{W\text{ admissible reachable closed}: E(W)>C_D(W)+L_{\rm fresh}(W)\}.
\]

This is a **proper subclass** of the earlier candidate domain E>C_D. The known H_m family,m>=5, has E=m>C_D=4 but L_fresh>=m, so Gamma<=-4. No new m or larger finite fit is needed for strictness.

This is a necessary residual source filter, not a claim that Gamma>0 suffices for FI rejection or that a walk in that residual class has been found. Coarse-Double on that class remains OPEN. The suffix identity alone is diagnostic normalization; the additional accepted-cut theorem is the one-sided coverage advance.

## 1. Source blocks, pools and established FI facts

Use cyclic maximal A-root blocks, each beginning at a positive-cost A leader. Let a_j be its actual A StepEv count,C_j=2a_j its capacity,q_j its B-double count and delta_j=q_j-C_j. A block has at most one genuine B-changing KEEP. B zigs contribute no double demand but count as genuine changes. A DELETE splays A, retains the key and freezes B.

A block containing DELETE followed by KEEP at the same root is a KEEP-containing block: its A capacity is counted once, and it is not part of C_D. Here C_D is the sum of capacities of KEEP-less blocks only.

Let E=sum_(delta_j>0)delta_j. At a positive block, FI pays C_j own demands from its own units and appends delta_j residual demands. Positive pools do not lend. At a nonpositive payer, every encountered positive fact is retained, including paid anchors. FI reserves

\[
r_j=\min(C_j,\min_{i\in H_j}c_{FI}(i,j)),
\qquad s_j=C_j-r_j,
\]

with r_j=C_j,s_j=0 if history is empty. Each source fact protects own work,q_j<=c_FI(i,j), so q_j<=r_j. Own work uses the prefix[0,q_j); unused reserved positions stay unavailable. Only[r_j,C_j) may lend, oldest residual first. The physical pool is retired after one visit.

For an anchor i and later payer key y, the unchanged source ceiling is

\[
c_{FI}(i,j)=
\begin{cases}
0,&j\text{ has no KEEP},\\
\lfloor h_i(y)/2\rfloor,&k_i(j)=0,\\
\lfloor U_{T_i}(x_i',y)/2\rfloor+k_i(j)-1,&k_i(j)\ge1.
\end{cases}
\]

h_i(y) is the depth in the anchor's B destination T_i; k counts genuine B changes strictly between the blocks; x_i' is the first such changing access. U is the established original-source-frame bound, computed from that first pre-tree, entry role and outer frames. Actual future q or observed first-post depth never chooses this ceiling. The source-bound proof covers arbitrary fringes and repeated keys.

## 2. An exact certificate for one rejected cut

Fix one physical block cut and scan its N blocks in order t=1,...,N, starting with empty history and zero debt. Once the source cut is fixed, every reservation and available suffix is determined by the source-positive history independently of whether those anchors have been paid. Define

\[
x_t=\begin{cases}
\delta_t,&\delta_t>0,\\
-s_t,&\delta_t\le0.
\end{cases}
\]

Because every pending anchor is eligible and the queue uses the offered suffix until it or the debt is exhausted,

\[
D_t=\max(0,D_{t-1}+x_t),\qquad D_0=0.
\]

Let X_0=0 and X_t=sum_(u=1)^t x_u. Induction gives

\[
D_t=X_t-\min_{0\le u\le t}X_u.
\]

Equivalently,

\[
\boxed{D_N=\max_{0\le b\le N}\sum_{t=b+1}^{N}x_t.}
\]

The empty suffix contributes0. This gives an exact certificate: a cut rejects iff some ending suffix has strictly positive signed certified balance. It does not say that a closed walk is outside FI merely because this one cut rejects.

For a canonical rejected-cut certificate choose b as the LAST global minimum of X_0,...,X_N. Since D_N>0,b<N. Then D_b=0 and every nonempty prefix of I=(b+1,...,N) has strictly positive balance. Its first block must be positive, since a nonpositive x cannot rise above the minimum. Every subsequent debt remains positive, so every available suffix unit of a payer inside I is actually used. The certificate records those source pools, reservations, demands, prefix balances and the exact terminal defect.

History is **not reset at b**. Positive facts encountered before b are all paid because D_b=0, but FI still retains them and may use them to lower later reservations. The certificate keeps their provenance. Their retired physical pools supply no new units to I; source facts are not credits.

## 3. Exact source-cost/reservation-loss split

At a nonpositive block define lambda_j=r_j-q_j>=0, the unused part of the protected own-work prefix. At positive blocks set lambda_j=0. Then in both cases

\[
x_j=\delta_j+\lambda_j.
\]

Thus the canonical busy suffix satisfies the exact identity

\[
\boxed{D_N=\sum_{j\in I}(q_j-2a_j)+\sum_{j\in I}\lambda_j.}
\]

This distinguishes source cost imbalance on that OPEN suffix from capacity withheld by the reservation ceiling. If its source sum is nonpositive, reserved loss must overcome the available source margin. If its source sum is positive, this is still not a counterexample on a CLOSED walk: the suffix has different source endpoints and can require capacity elsewhere in the period.

No sign conclusion is imposed on either source component beyond these exact identities. In particular, not every rejected cut must exhibit positive reservation loss; an unfortunate one-period boundary can strand a genuine last positive even on a walk accepted at another cut.

## 4. A source-local fresh-run budget

Assume the cycle has at least one positive block. Partition it into cyclic runs, each consisting of a positive anchor i followed by every nonpositive block until the next positive. Each nonpositive physical pool belongs to exactly one run.

For a payer j in run i, compute only that run anchor's established source fact and set

\[
\rho_j=\min(C_j,c_{FI}(i,j)),\qquad f_j=C_j-\rho_j.
\]

This is the fresh-run offer. It uses the nearest cyclic positive source fact, never actual own q as a reservation oracle. Define

\[
T_i=\sum_{j\text{ payer in run }i}f_j,
\quad g_i=\delta_i-T_i,
\quad L_{\rm fresh}=\sum_{\substack{j\text{ nonpositive}\\j\text{ contains KEEP}}}f_j.
\]

Each KEEP-less payer has ceiling0 and hence f_j=C_j. Partitioning the pools exactly once gives

\[
\Gamma=\sum_i g_i=E-C_D-L_{\rm fresh}.
\]

A run may have g_i>0. The theorem does not require private repayment of every anchor before the next one. A later run's physical payers may pay an older residual debt under FIFO. The current anchor determines a safe reservation, not ownership of that pool.

## 5. Constructing a valid cut when Gamma<=0

Consider an auxiliary conservative queue that uses only the current run anchor's ceiling at each payer, but lends its suffix to ANY oldest pending residual. Cut at a positive-run boundary and start with empty history/debt. The current run's anchor has then been encountered before every payer in that run, even if its own debt has been paid. Its source fact is valid without any earlier-lap information.

Within a run, one positive adds delta_i and all later steps only subtract fixed nonnegative offers, retiring unused units when debt is empty. Therefore its end-of-run debt is exactly

\[
\widehat D_{i+1}=\max(0,\widehat D_i+g_i).
\]

This clipping is essential: surplus at an early pool is discarded, not banked for a future anchor.

Index the p positive runs0,...,p-1 and let G_0=0,G_t=sum_(i=0)^(t-1)g_i. Suppose Gamma=G_p<=0. Choose q at a minimum of G_0,...,G_p and start at run q modulo p. Every ending suffix in that rotated order has nonpositive sum:

- For a start t<q its sum is G_q-G_t<=0.
- For a start t>=q its sum is Gamma+G_q-G_t<=0.
- If q=p, identify the cut with run0; the same minimum inequality gives Gamma-G_t<=0 for all ending suffixes.

The clipped-queue identity therefore gives zero auxiliary debt after one period. This explicitly constructs the cut from the source budgets.

At that same cut, actual FI retains the current run anchor among its facts. Its minimum ceiling is no greater than this single fresh ceiling, so its reservation is no larger and its offered suffix is at least f_j. Positives add the same debts to both queues. Induction on every physical block yields D_FI<=D_aux. Thus actual FI also accepts the constructed cut.

Every pool is used once, own prefixes and loan suffixes are disjoint, recipient residual cursors only advance, and every request/demand identity includes its physical occurrence. No pool from an alternative cut or another period is added to this injection. Hence this is a genuine source cut theorem, not total-capacity pooling.

## 6. The strictly smaller necessary source obstruction class

The contrapositive of the proved theorem is

\[
W\notin FI\quad\Longrightarrow\quad E>C_D+L_{\rm fresh}.
\]

Since FI acceptance proves Q_B<=2A, any actual Coarse-Double counterexample must satisfy this same necessary condition. Since L_fresh>=0,

\[
\mathcal O_{\rm fresh}\subseteq\{W:E>C_D\}.
\]

The inclusion is proper on admissible reachable source walks. In every H_m,m>=5, the newest anchor's source frame releases one fresh KEEP5 unit in each copy, giving L_fresh>=m. Its two reset pools contribute C_D=4 and E=m. Hence

\[
\Gamma(H_m)\le m-4-m=-4,
\]

although E>C_D. This uses the already proved source identity and unit donor; it is not an additional finite-m experiment. It eliminates the entire nonempty source class E>C_D with E<=C_D+L_fresh without assuming an accepted cut.

No converse is established: Gamma>0 may still permit FI to benefit from older retained facts. There is no claim that every source walk has Gamma<=0, that the residual domain is nonempty, or that source geometry makes its inequality impossible. Coarse-Double on O_fresh remains open. The reduction is one-sided and necessary, not a new equivalent global-existence premise.

## 7. The concrete source geometry of an offer

For a KEEP-containing payer let C=2a. If k=0,

\[
f>0\quad\Longleftrightarrow\quad h\le2C-1.
\]

If k>=1, the established source frame bound U>=0 gives

\[
\begin{aligned}
f>0
&\Longleftrightarrow \lfloor U/2\rfloor+k-1<C\\
&\Longleftrightarrow k\le C\ \text{ and }\ U\le2(C-k)+1.
\end{aligned}
\]

Thus a fresh offer requires a capacity-relative short-lag/source-frame condition. In particular k>=C+1 forces f=0 regardless of fringe depth. This bounds the relevant freshness per physical payer by its actual A work, with no fixed-size or constant-depth assumption. Inside the remaining class, the total capacity released by all these source-qualified KEEP pools, plus all KEEP-less capacity, is strictly smaller than E. Older-anchor improvements and other arguments remain available; the theorem does not discard them as invalid.

## 8. Boundaries, source audit and proof status

No-positive walks pay every demand locally, so every cut succeeds. Empty and A=0 closed walks have Q_B=0 under the established fixed-root closure argument. All-positive nonempty block cycles have no payer and reject each FI pass; the certificate identity still applies, while the fresh coverage hypothesis Gamma<=0 is false. A single positive has one cyclic run and the minimum-prefix argument is valid. Mixed DELETE/KEEP root blocks, B-root no-ops, zero-double genuine zigs, repeated coordinates, arbitrary fringes and reflected orientation are covered by the unchanged source-fact theorem and one-time pool accounting.

The fixed validation corpus contains only twelve previously verified FI controls and the ordinary/reflected H5 records:636 existing cuts. All recorded outcomes are reproduced;44 rejected cuts have canonical exact certificates and592 have zero terminal debt. Every control has Gamma<0, and the constructed positive-run cut is independently verified with full distinct-unit accounting. These controls are NOT examples of all-cut FI failure. No new source word, n, m or larger fit is introduced.

The proof of the universal statements is the debt unrolling, run partition and cyclic minimum argument above. Fixed-source validation checks the definitions, provenance, reservations, multiplicities and actual certificates; it does not replace the all-size proof. The certificate identity itself is bookkeeping. The additional theorem supplies unconditional accepted cuts on a proper source-defined subclass and a strictly stronger necessary domain for the remaining Step3 obligation.

Matching-terminal remains FROZEN. All prior source/research files and all125 Stage11G files are preserved. Universal Coarse-Double remains OPEN, now with the necessary residual source domain O_fresh explicitly isolated. No automatic successor follows.
