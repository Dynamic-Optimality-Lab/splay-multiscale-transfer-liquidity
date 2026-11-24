# Bank–Cap Regeneration Gate — 2026-11-23

**Verdict:** `SUBSTANTIVE PARTIAL; UNIVERSAL BOUND OPEN`. This checkpoint is an attempted proof, not a proof of Dynamic Optimality.

## 1. Frozen source domain and already proved budgets

Original A splays every KEEP/DELETE. Original B splays KEEP only. Every source is reachable from a common initial BST and exactly returns both complete labeled A/B trees. Original A StepEv count is `A`, original B double count `Q_B`, and the frozen five-credit selected policy gives

\[
Q_B=P_5+\Omega_5,\qquad P_5\le45A.
\]

Let `R_A=2A-Z_A` be the number of *real primitive A rotations*, with `Z_A` terminal A zigs. For fixed integer `c>=1` set

\[
\Psi_c(A,B)=\sum_{I\in J(A)}\min(c,\ell_B(I)),\quad
\ell_B(I)=\#\{v\in I:I_B(v)\not\subseteq I\}.
\]

A real A rotation increases `Psi_c` by at most `c`; each B rotation made after A has splayed the common KEEP target to the root does not increase `Psi_c`. Closed-state telescoping yields

\[
D_c(W):=\sum_{\text{primitive B rotations}}(-\Delta\Psi_c)\le cR_A\le2cA.
\]

## 2. Exact local visibility criterion (proved)

Fix a B primitive rotation during a KEEP of target `x`. At this moment A has root `x`. Let `p` be the demoted parent and let `J=I_{B^{\rm after}}(p)` be its new physical subtree interval. For every **proper** A-subtree interval `I`, the preceding promoted B-subtree interval contains `x`, hence cannot be contained in `I`. The B rotation replaces that old interval with `J` in the multiset of B-subtree intervals. Therefore,

\[
\ell_{B^{\rm after}}(I)=\ell_{B^{\rm before}}(I)-\mathbf{1}[J\subseteq I].
\]

Hence the exact capped decrease is

\[
-\Delta_B\Psi_c=
\#\{I\in J(A)\setminus\{K\}:J\subseteq I,\quad
1\le\ell_{B^{\rm before}}(I)\le c\}.
\]

Define the *minimal visibility cap* of a primitive B rotation by

\[
h(R)=\min_{I\in J(A)\setminus\{K\},\ J\subseteq I}
\ell_{B^{\rm before}}(I).
\]

For a B double `e=(R_1,R_2)` define `h(e)=min(h(R_1),h(R_2))`, evaluating the second rotation at the actual intervening B state. Then `e` is visible to `Psi_c` **if and only if** `h(e)<=c`.

This gives the proved budget

\[
\#\{e:\text{GSO-unpaid B double and } h(e)\le c\}
\le D_c(W)\le cR_A(W)\le2cA(W).
\]

This statement is entirely source-uniform; no finite-search assumption enters its proof.

## 3. Very short closing door (NOT proved)

**Candidate BC5.** Every unpaid original B double in the **greatest clipped cyclic H=5 bank** of an admissible exactly paired-closed original source satisfies `h(e)<=5`.

If BC5 holds, the preceding theorem yields

\[
\Omega_5\le D_5\le5R_A\le10A,
\qquad Q_B\le55A.
\]

Hence the established Universal Relaxed Coarse-Double / Levy–Tarjan implication would prove Dynamic Optimality. **BC5 is currently a conjecture, not an inherited result.**

For a more tolerant fallback, put `H_5(W)=#{e unpaid:h(e)>5}`. The exact decomposition gives

\[
\Omega_5\le10A+H_5.
\]

It is enough to prove `H_5<=theta*Omega_5+C*A` for some absolute `theta<1,C<infinity`. Nothing in this record establishes that either.

## 4. Actual original 257-key witness: exact replay

The `run_003/complete_00.json.gz` original source was recovered from GitHub and rewritten as its 173 raw operations plus 513 mandatory restoring KEEPs. Independently implemented rotation and bank routines reproduce every published aggregate:

| Physical statistic | Replayed value |
|---|---:|
| Full physical keys | 257 |
| Operations | 686 |
| Original A StepEv `A` | 989 |
| A terminal zigs `Z_A` | 498 |
| Real A rotations `R_A` | 1,480 |
| Original B doubles `Q_B` | 519 |
| H5-paid `P_5` | 517 |
| H5-unpaid `Omega_5` | 2 |

The only unpaid doubles are `B(99,14)` and `B(99,15)`, both RR:

| Unpaid ID | `h(R_1)` | `h(R_2)` | `h(e)` | `-Delta Psi_1` | `-Delta Psi_2` | `-Delta Psi_5` |
|---|---:|---:|---:|---:|---:|---:|
| B(99,14) | 2 | 3 | 2 | 0 | 1 | 4 |
| B(99,15) | 2 | 1 | 1 | 1 | 2 | 2 |

This is *support* for BC5 on one real physical source, not a proof.

### Near-witness adversary

A deterministic random perturbation of that 173-operation prefix (always appending the complete exact restoring scan) evaluated **890** valid paired-closed sources before the 30-second cut. **632** had nonzero Omega5; none had an unpaid event with minimal visibility cap above five. The largest Omega5 observed in this localized sample was two. This search is biased toward the same successful dry packet and is not an independent or exhaustive certification.

## 5. Sharp obstruction to any purely instantaneous proof (proved in the larger state class)

For every fixed `c`, let `N>c+12` be odd. Consider A the *left vine* rooted at `N`, B the *right vine* rooted at `1`, and all H5 bank block stocks initially zero. This is an abstract A/B/bank snapshot, **not asserted to be a valid greatest-cyclic-stock source state**. A already has `N` at its root, while B must splay `N` through `(N-1)/2` consecutive RR doubles.

A genuine KEEP voucher puts exactly five credits into the target's bank block. The first five B doubles consume them; all other blocks started empty, so the **sixth RR double is unpaid**. Its exact minimal visibility cap is

\[
\boxed{h(RR_6)=N-12>c.}
\]

For example, `N=65` gives `h(RR_6)=53`, and `N=257` gives `245`.

This refutes any proposed proof of BC5 that uses *only* the instantaneous BST geometry, the fact that A has the target at its root, and a locally legal bank transition. In the genuine original H-family preparation that creates the opposite spines, earlier A DELETE rotations refill the other block banks, making the corresponding long B access paid. That historical stock provenance is exactly what the local argument omitted.

The abstract configuration **does not refute BC5 on its original paired-closed source domain**, and it certainly does not refute Dynamic Optimality.

## 6. Precise unclosed bridge

Construct a whole-source invariant linking the *canonical cyclic bank stock provenance* to the *minimal cap threshold* `h(e)`. The strong form is BC5: no H5-unpaid event with `h(e)>5`; the weaker contraction form is a global bound on the count of those events.

Any valid invariant must account for:
1. New A rotations simultaneously changing subtree intervals and refilling their exact H5 bank footprints.
2. Paid B doubles transferring and consuming credits between blocks, not simply draining isolated local accounts.
3. Repeated destruction/recreation of ancestry and repeated group entry.
4. The greatest clipped **cyclic** bank seam and the absence of reaching-prefix financing.

**Next falsification gate:** Search entire paired-closed histories with the primary objective `max(h(e): e H5-unpaid)`, not merely `Omega5/A`. A certified event with `h(e)>5` refutes BC5 and leaves the weaker contraction route. Otherwise, one must still prove BC5 by a source-uniform inductive or global argument; finite tests cannot close it.

## Pinned references

- [GSO frozen bank policy and exact witness](https://github.com/Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity/tree/coarse-double-branch/DO_RESEARCH_REBOOT/GSO_OMEGA_CYCLE_SEARCH_20261122_V001)
- [Complete-period ancestry/capped-potential derivation](https://github.com/Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity/blob/coarse-double-branch/DO_RESEARCH_REBOOT/GSO_OMEGA5_COMPLETE_PERIOD_20261123.md)
- [Levy–Tarjan eventual monotonicity reduction](https://arxiv.org/abs/1907.06310)
