# Historical ancestry / paid-bank provenance: direct closure attempt

**2026-11-23 — Verdict: two source-uniform accounting lemmas proved; universal bridge OPEN.**

This note is an independent deduction and limited computational check based on the attached `BANK_CAP_REGENERATION_GATE_20261123.md`, its reproduction scripts, and the repository's original GSO H5 bank rules. It is **not** a proof of BC5, Relaxed Universal Coarse-Double, or Dynamic Optimality. No source is mutated and no restricted theorem is promoted.

## 0. Frozen domain and notation

Use the original present-key Pair Access model: A splays every KEEP or DELETE, B splays KEEP only, both full labeled BSTs start from a common-tree-reachable pair and return exactly to themselves. DELETE never removes a physical key. A StepEv count is `A`; original B double count is `Q_B`. The canonical **greatest clipped cyclic H5 stock**, with five-rank capacity-five blocks and target-first B pooling, gives

\[
 Q_B=P_5+\Omega_5,\qquad P_5\le45A.
\]

Fix the cap `c=5`. By the existing interval visibility/potential theorem, write

\[
 \Omega_5=V_5+H_5,\quad
 V_5=\#\{\text{unpaid doubles }e:h(e)\le5\},\quad
 H_5=\#\{\text{unpaid doubles }e:h(e)>5\},
 \qquad V_5\le D_5\le10A.
\]

A **bad** double is an unpaid, cap-five-invisible B double. All other B doubles are **anchors** (paid or cap-five-visible unpaid).

## 1. Proved historical target-block invariant

Consider any genuine KEEP access to `x`. Let `b_x` be its target's rank-five bank block and `s_j` its stock immediately before the j-th original B double. The genuine KEEP issues a voucher resetting `s_1=5` (A's subsequent phase can only reset bank blocks to five). Every B double's footprint contains `b_x` and the redistribution gives it first priority. If `M_j` is the total footprint stock before its payment, the target stock after the event is

\[
 s_{j+1}=\min(5,M_j-\mathbf1[M_j>0]),\qquad M_j\ge s_j.
\]

Thus `s_{j+1} >= s_j-1`. It follows inductively that the first **five** B doubles in this genuine KEEP are paid, if they exist. Every unpaid double is preceded by at least five distinct paid B doubles **within that same KEEP**. A terminal zero-demand zig does not create a new double or defeat the statement.

This holds for the frozen stock policy on *any* legal history; it does not invoke canonical maximality or paired closure.

## 2. Proved packet-anchor injection (the first entry is already controlled)

Partition each genuine KEEP's B-double list into maximal consecutive **bad packets**. Every packet begins after a nonbad B double, since the access begins with at least one paid double. Map the packet to its immediately preceding nonbad B double within the same access. These predecessor doubles are distinct between packets, including across different accesses. Hence, writing `M_5` for the number of bad packets and `L_i` for their lengths,

\[
 \boxed{M_5\le P_5+V_5\le55A},\qquad
 H_5=\sum_{i=1}^{M_5}L_i
     =M_5+\sum_{i=1}^{M_5}(L_i-1).
\]

Even without distinguishing visibility, maximal packets of *all* unpaid B doubles inject into preceding paid B doubles. Thus their number is at most `P5 <=45A`.

### Explicit sufficient continuation lemma (OPEN)

Define `C_5=\sum_i(L_i-1)`: the count of **continuations** after the first high-cap unpaid double of each bad packet. The packet-anchor theorem gives

\[
 \boxed{Q_B=P_5+V_5+H_5\le110A+C_5.}
\]

Therefore **a source-uniform bound `C_5<=K A` is sufficient**: it gives `Q_B<=(110+K)A` and closes the established Relaxed CD -> Dynamic Optimality implication. Stronger but potentially simpler: if every bad packet has length at most an absolute `L`, then `Q_B<=55(1+L)A`.

**The continuation lemma is not proved here.** It is a sharper work target than demanding a separate A-rotation for every bad event: packet *entrances* already have an injective paid/visible predecessor. The remaining difficulty is renewal of successive bad pairings without new paid/visible anchors.

## 3. Proved cyclic ancestry-lifetime inventory

For a proper physical A-subtree interval `I`, let `ell_B(I)` count its B straddlers. While `I` remains a proper A interval (between its birth and removal), A rotations elsewhere leave `ell_B(I)` unchanged because B freezes, and each primitive B rotation changes `ell_B(I)` by `-1` or `0`, never upward, since A is rooted at the KEEP target. Hence its **excess** `e_I=(ell_B(I)-5)_+` is monotonically nonincreasing during that lifetime.

A real A rotation replaces precisely one proper A-subtree interval by one new proper interval; thus it creates precisely one new proper interval lifetime. On a paired-closed cyclic history, an interval present throughout the cycle has periodic endpoint straddler count and can have **no** B decreases. All B decreases must belong to an interval lifetime born at an A rotation in the cyclic period (interpreted periodically across the seam).

For every primitive B rotation `R` in a bad double, let `J` be the new subtree interval of its demoted B parent. Choose the **smallest proper A interval containing `J`**, breaking no ties because A intervals containing a fixed interval form an ancestor chain. Since `h(R)>5`, its straddler count is at least six before the B rotation, and this rotation spends one unit of its positive excess `e_I`. The two primitive rotations in each bad double spend two distinct excess units (not necessarily from the same interval lifetime).

Assign the spent unit to the unique most recent A rotation that *birthed that interval*, modulo the cyclic period. This is an explicit causal injection from bad **primitive** B rotations into labeled excess units at A-interval births. Let `e_rho` be the number of excess units at birth `rho`. Then

\[
 \boxed{2H_5\le\sum_{\rho\in\mathrm{Rot}_A(W)} e_\rho.}
\]

This is a genuine ancestry-history invariant, but **not yet a uniform A-work charge**: each A rotation may birth arbitrarily many excess straddler units.

### Why naive constant capacity per interval birth fails

The existing `GSO_OMEGA5_COMPLETE_PERIOD_20261123.md` records the opposite-spine original `H_{3,q}` family with `N=2m+1`, `A=8m`, and full-uncapped straddler potential `F=sum_I ell_B(I)` satisfying `sum_A Delta F >= m(m+2)`. Since `F=Psi_5+Theta_5`, where `Theta_5=sum_I(ell_B(I)-5)_+`, and `sum_A Delta Psi_5 <=10A=80m`, we obtain

\[
 \sum_A\Delta\Theta_5\ge m(m-78).
\]

Thus **raw senior straddler regeneration / A** can grow without bound. The original H sources in the finite exact checks are fully paid. Any correct universal historical invariant must explicitly offset senior regeneration already served by paid B work; it cannot simply claim `e_rho=O(1)`.

## 4. The sharper paid-offset historical invariant (UNPROVED)

Use the same deterministic **minimal-A-containing-interval** assignment for *all* primitive rotations of relevant B doubles, so an individual B primitive rotation can never be counted against multiple nested A intervals. For each A-born interval lifetime `L`, define:

- `u_L`: number of primitive rotations in **bad** B doubles assigned to `L` (each rotation has `ell>5`);
- `p_L`: number of primitive rotations in **paid** B doubles assigned to `L` when they also decrease `ell` above five (no rotation is assigned to more than one lifetime).

A concrete proposed historical invariant is: there are absolute constants `C,lambda<infinity` such that **for every original exactly paired-closed source and every A-born interval lifetime**,

\[
 \tag{HI-PAID-01}\boxed{u_L\le C+\lambda p_L.}
\]

If it were true, summing over at most `R_A<=2A` births and using `sum_L p_L<=2P_5<=90A` yields

\[
 2H_5=\sum_Lu_L\le CR_A+2\lambda P_5
 \le(2C+90\lambda)A,
\]

and therefore

\[
 \boxed{Q_B\le(55+C+45\lambda)A.}
\]

This is a mathematically valid **conditional** route to Dynamic Optimality. Its importance is that paid B rotations have a **single canonical A-lifetime owner** here, preventing the earlier full-uncapped potential's unbounded multiple charging of one paid rotation to many nested intervals. It is **not** claimed proved, true, or necessary. It may be false for individual lifetimes even if a global inequality holds. Testing should optimize `u_L-C-lambda*p_L` and not just `Omega5/A`.

## 5. Sharp abstract obstruction to packet-length arguments without history

Let `N` be odd, A a descending left vine rooted at `N`, B an ascending right vine rooted at `1`, and all H5 blocks empty before the KEEP voucher targeting `N`. The voucher supplies exactly five credits to the target block. In the ensuing B splay, all other blocks remain empty; the first five RR doubles pay and every later RR double is unpaid. The recorded exact rotation computation gives, for the j-th RR double, `h(RR_j)=N-2j`.

Thus the consecutive high-cap unpaid packet consists of j=6,...,(N-7)/2, of length

\[
 \boxed{L_N=(N-17)/2}\quad (N\ge19,\ N\text{ odd}).
\]

For `N=65`, `L_N=24`; for `N=257`, `L_N=120`. These are **abstract local states with an artificially empty initial stock**, not certified original paired-closed cyclic sources. They refute any fixed bad-packet bound proved from the local voucher and rotation geometry *alone* and show exactly why global stock provenance matters.

## 6. Exact finite checks and targeted falsification

Executed the attached independent physical engine with cyclic stock recomputation. `historical_packet_audit.py` checks the preceding packet inequalities; `HISTORICAL_PACKET_CHECKS.json` records results. In the certified 257-key original source, A=989, Q_B=519, paid=517, visible-unpaid=2, bad=0. Its two unpaid doubles are one all-unpaid packet of length two, both cap-visible.

Additional original H family runs at N=33,65,129,257 were paired-closed and fully paid. A deterministic 240-iteration local adversary mutation run (`search_blind5.py`, 179 retained positive-Omega sources) found no BC5 counterexample. The best zero-stock unpaid threshold was 3; a paid double at one remaining credit had threshold 5, and at two remaining credits there was a threshold-7 event. The mutations are highly correlated and are **not** an exhaustive search or a universal argument.

For the 257-key archived KEEP operation 99, exact (footprint total stock, h) transitions included `(2,7)`, `(1,5)`, `(0,2)`, `(0,1)`. These observations suggest a possible paid-to-visible boundary phenomenon; the abstract opposite-vine construction shows it cannot be deduced without source history.

## 7. Verdict and precise next gate

**PROVED here at the mathematical argument level:** target-bank voucher monotonicity; at least five earlier paid doubles before first unpaid; injective paid/visible predecessor per bad packet; `M5<=55A`; ancestry interval lifetimes and causal excess-unit assignment `2H5 <= sum_birth e`; rigorous conditional implications of a continuation or paid-offset invariant.

**NOT PROVED:** `C5=O(A)`, `HI-PAID-01`, a bound on per-birth net senior excess after paid offset, BC5, Universal Relaxed Coarse-Double, or Dynamic Optimality.

**Most discriminating falsification task:** search genuine paired-closed cyclic sources with `u_L> C+lambda*p_L` for progressively smaller fixed trial constants, and optimize the **maximum bad-packet continuation length** rather than just `Omega5/A`. A counterexample to a chosen `C,lambda` or packet length bound does not refute Relaxed CD or DO. If those strong invariants fail, the next relaxation should charge *cohorts* of overlapping A lifetimes jointly while preserving single-ownership of paid B rotations.

## Source pins

- User's `BANK_CAP_REGENERATION_GATE_20261123.md`, uploaded in this chat.
- `DO_RESEARCH_REBOOT/GSO_OMEGA5_COMPLETE_PERIOD_20261123.md` in branch `coarse-double-branch`.
- `DO_RESEARCH_REBOOT/GSO_OMEGA_CYCLE_SEARCH_20261122_V001/{README.md,core.py,credit.py,verify.py}` in the same branch.
- `DO_RESEARCH_REBOOT/ROUTE04_RELAXED_UNIVERSAL_CD_20261108/RELAXED_UNIVERSAL_CD_DISCOVERY_STEP01.md` (the established conditional reduction).

### Reproduction commands

From the directory containing the supplied engine and these scripts:

```bash
python -B replay_257.py
python -B historical_packet_audit.py
python -B local_cap_adversary.py
python -B search_blind5.py
```

The local mutation search is seeded and finite; no generated candidate is evidence for an all-source bound without independent exact validation.
