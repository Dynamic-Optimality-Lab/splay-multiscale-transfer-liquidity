# PIVOT-14: Universalizing the PIVOT-13 charging (U1–U4)

Verdict: **U1 PROVED. U2 PROVED. U3 PROVED. U4 OPEN (precisely located).**
`Q_B ≤ 2A` unrefuted on 550+ adversarial tests, still not universally proved.
No laps as objects: everything below lives on `Z/mZ` (periodic extension is
only a predecessor-locating device).

## 0. Cyclic setup (all Ui share this)

Closed cycle `γ = e_0..e_{m-1}`, states `s_m = s_0`, indices mod m.
Periodic extension `...γγγ...` for locating strictly-prior events.
Credit model: each A-StepEv yields 2 credits; exactly `2A` credits indexed
once by `Z/mZ`. Creator/setup point to mod-m indices (same orbit, same
budget, no duplication by construction — there is only one copy of each
access). `charge()` on second-copy replay approximates this (context copy
= same orbit).

Splay facts used (all banked/mechanical):
- (R) After KEEP x, x is B-root (and A-root). Rotations are the only
  B-mutations (DELETEs don't touch B). Every access splays A.
- (D) Dethrone: splaying `w ≠ z` in A ends with `z` non-root (root is
  unique, taken by `w`).

## A. Cyclic creator definition

For B-double `D` at access `j` (KEEP x, triple `(x,p,g)` at step start),
define the consumed edges `e_1 = (x→p)`, `e_2 = (p→g)`. The
**consumed-descent** of an edge `e` present at a step bound: take its latest
establishing rotation strictly before the bound (exists in periodic
extension unless the edge is ETERNAL — never rotated in any period);
if that rotation lies in the same splay at an earlier step, replace `e`
by that step's consumed pre-step ancestor edges and repeat (step index
strictly decreases; then a strictly-prior access). `ORIGIN(e)` = the set
of strictly-prior accesses so reached. `creator(D)` = max of
`ORIGIN(e_1) ∪ ORIGIN(e_2)` in periodic linear order.

## B. U1 cyclic_creator_exists: PROVED

Let `i` = prev KEEP-x occurrence (`i < j` in periodic extension).
**Epoch lemma:** if the x-epoch `(i,j)` is empty (adjacent), x is still
B-root at `j` (nothing moved B), so `q_j = 0` — no double exists. Hence
every B-double has nonempty epoch. (`m = 1` is vacuous: single-KEEP-x
steady state has `d_B = 0`; single-DELETE has no B-work.)

**Core:** the `(x→·)`-following descent always terminates strictly inside
`(i,j)`. Proof: at `i`-end x is B-root, so every `(x→·)` edge is absent;
every queried `(x→·)` edge exists at its bound (pre-step mid-splay state,
x non-root throughout access `j` since `d_B ≥ 2`), so its latest
establishment is a real logged rotation after `i`-end (if strictly-prior:
in `(i,j)` by the absent-at-`i`-end argument — an establishment at
`≤ i` would have been destroyed by `i`-end rooting and re-established
later, contradicting latestness; if same-splay: descend). At step 0 the
pre-step edge `(x→p_0)` exists at `j`-start (x non-root) and is absent at
`i`-end, so its builder is in `(i,j)`. Genesis is impossible on this
branch (every step exhibits a post-`i` establishment). The `(p→g)`-branch
may escape pre-`i` or hit an ETERNAL (never-rotated) edge — harmless: the
max over the union is still `> i` (via the x-branch) and `< j`
(all outputs strictly prior). Mod-`m` well-defined and `≠ j` (epoch
nonempty ⇒ the linear interval `(i,j) ⊂ [j-m,j)` contains no index
`≡ j` except `j` itself, excluded).

So: **every B-double (not just overflow) has a cyclic creator strictly
inside its key epoch.** Genesis eliminated structurally, not by fiat.

## C. Structural setup definition

For access `t` to key `z` with `a_t = 0` (z A-rooted) that either performs
B-double work or built B-structure consumed later: `setup(t,z)` = the
latest `z`-occurrence strictly before `t` (cyclically) with `d_A > 0`
(an A-root-arrival; it did `a ≥ 1` A-work, so `≥ 2` credits EXIST).
Not "whatever the matcher used" — a structural last-arrival.

## D. U2 cyclic_setup_available: PROVED

**Dethrone + quiet lemma:** `setup(t,z)`'s interval `(s,t)` contains NO
non-`z` access. Proof: any non-`z` access splays A (KEEP and DELETE both),
dethroning `z` (rooted at `s`-end) by (D), so the next `z`-occurrence
would have `d_A > 0`, contradicting maximality of `s`. Hence the interval
holds only `z`-accesses, all with `d_A = 0` (z never dethroned), i.e. the
starved block is quiet with all middle credits zero.

**Existence:** scan `z`-occurrences backward from `t`. If none has
`d_A > 0`, every gap has no non-`z` access (else dethrone ⇒ `d_A > 0`),
so the cycle is all-`z`-accesses. Then B is frozen between `z`-KEEPs
(KEEP roots, DELETE noops): at `t` (KEEP z) `z` is B-root — contradicting
`q_t ≥ 1` (overflow case) or contradicting "`t` rotated B" (builder case:
a builder rotated, so `d_B ≥ 1`, so `z` was non-root, so B moved, so a
non-`z` KEEP exists). Hence a `d_A > 0` arrival always exists for every
starved link (overflow or builder) on a cycle containing a genuine
double. It carries `≥ 2` A-credits by construction.

**Scope note (honest):** U2 is proved for starved links (`a = 0` with real
B-content). Non-starved accesses (`a ≥ 1`) may have `setup = None` (their
own A-work suffices structurally); they use local + creator.

## E. Wraparound one-cycle accounting: PROVED (definitional)

The setup/creator found by backward periodic scan is reduced mod `m` to
the same structural access on the closed orbit (periodic copies are the
same orbit). Credits are indexed once per cyclic access (`2A` total);
no copy is duplicated because there are no copies — the second-copy
replay in `charge()`/`cyclic_test` is an approximation whose context copy
is the same orbit. Any U4 injection built on mod-`m` indices spends each
credit at most once by construction. The remaining work is purely U4's
(global existence of the injection), not accounting hygiene.

## F. Creator-chain definition

`D → c_0 = creator(D)` (always a KEEP — only KEEPs rotate B). If
`a_{c_0} ≥ 1`: terminal. Else (`a = 0` starved builder): `→ s_1 =
setup(c_0)` (exists by §D generalized argument). Stop (setup has `a ≥ 1`).

## G. U3 creator_chain_terminates: PROVED (≤ 2 hops)

Every genealogy reaches a positive-credit event in at most two hops:
creator (terminal if `a ≥ 1`, carrying `2a ≥ 2` credits) or creator's
setup (terminal, `a ≥ 1` by arrival construction). No loop is possible
at the REACHABILITY level (loops would need a third hop, which never
occurs — every path bottoms at an `a ≥ 1` event). Whether the terminal
credit is FREE is U4's question, correctly separated.

## H. Genealogy interval/epoch structure (proved lemmas)

- **H1 (epoch confinement, from U1):** every double's creator lies
  strictly inside its key epoch. Epochs CROSS in general (alternating
  `D,K` family) — laminar epochs are FALSE, not used.
- **H2 (starved blocks pairwise disjoint):** the closed block
  `[s_j, t_j]` (setup..starved-overflow-KEEP, one key) contains only
  own-key accesses (quiet lemma). Different keys' blocks are disjoint
  (each key's accesses are other-key to the other, hence outside its
  open quiet interval and distinct from its endpoints). Same key's
  blocks are disjoint and ordered: two starved `t < t'` sharing setup
  `s` is impossible (the earlier KEEP roots B, quiet forces the later
  rooted, `q = 0`, contradiction); hence setups strictly interleave
  (`t < s'`, disjoint).
- **H3 (exactly one starved overflow per block):** the starved KEEP is
  necessarily the first in-block KEEP (a middle KEEP would root B and
  clean all later KEEPs); the setup itself has `d_A > 0` (non-starved).
  Corollary: no two starved doubles share one setup.
- **H4 (fan-in bound):** doubles naming one creator consume distinct
  edges it built (a consumed edge is destroyed; re-consumption names the
  rebuilder), so fan-in ≤ edges built ≤ `3 × rotations` = `O(d_B)`.
  Observed max fan-in 2 (45×1, 4×2 over 19 pool cycles); setup-KEEPs
  with own doubles are common (26/53 setups) — self-competition is real.

## I. Capacity model

`2A` cyclic credits; each double eligible to local pool (`2a_t`),
creator pool (`2a_c` or empty), consumer-setup pool (`2a_s` or empty).
Goal: simultaneous injection (equivalently
`total_overflow ≤ total_slack`).

## J. U4 overflow_capacity: OPEN (first unproved statement)

Attempted: Hall over local/creator/setup eligibility; minimal-deficient-X
characterization using H1–H4; two-tier (starved→own-setup via disjoint
blocks H2–H3; non-starved→local-first + creator chains). **Sticking
point (exact):** sharing of one terminal pool by (i) same-creator fan-in
(H4 bounds the degree but `O(d_B)` can exceed `2a_c` plus the creator's
own `q_c` demand), and (ii) setup-KEEP self-competition (H4: common —
the setup's own doubles plus the block's starved double plus outside
namers can exceed `2a_s`). No universal per-terminal demand ≤ capacity
lemma was found; crossing epochs (H1) rule out laminar counting. The
finite solver succeeds because global slack EXISTS on every tested
cycle; certifying it universally is exactly the missing
**closed-component capacity lemma**: every creator/setup-closed demand
component carries enough credits. Status: OPEN, not refuted (550+
adversarial cycles match; §K–L confirm the mechanism, not the theorem).

## K. Seven old Hall failures under the universal theorem

All seven are `[D,K]`-alternating short cycles whose `+1` doubles are
`(a,q) = (0,1)` with `a = 0` creators: under creator-only eligibility
`N(X) = ∅` (both pools empty). U2 locates each starved double's setup
(the preceding DELETE, `d_A > 0`, 2 credits, same cycle mod m — §E);
U3 terminates there (1 hop past the starved creator); H2–H3 give each
its own disjoint setup pool. They are now the canonical U2/U3 unit
tests, all passing in `charge()`.

## L. Vignette derivations

- **(0,1)** (`[D3,K3,K2,D1,K1]`, acc6): U1 gives creator acc4 (in-epoch
  builder of the `(3→2)` stack); U2 gives setup acc5 (`D3`, `d_A = 2`,
  2 credits); U3 stops (setup has capacity); matching assigns one of
  the two pools' credits. Fully inside the cyclic theorem.
- **(0,2,+2)** (`[K6,D4,K4]`, acc2): U1 routes both doubles to builder
  acc0 (`K6`); U2 provides setup acc1 (`D4`) as alternate pool. This is
  the minimal capacity->1 case (two units, one terminal with `2a ≥ 2`
  if `a_K6 ≥ 1`): covered by U4's per-terminal accounting — i.e. exactly
  where U4's open lemma sits. Not special-cased.

## M. total_overflow ≤ total_slack: OPEN (equivalent to U4)

Holds on all 550+ tested cycles (many with dense overflow: bred mean
2.2, maxlen 52). Unguarded universal claim NOT made.

## N. COARSE-DOUBLE Q_B ≤ 2A: OPEN (conditional composition ready)

`Q_B − 2A = total_overflow − total_slack ≤ 0` follows the moment U4's
closed-component capacity lemma lands. U1–U3 + H1–H4 are banked toward
it. `Q_B ≤ 2A` itself is UNREFUTED (no `Q_B > 2A` cycle found anywhere).

## O. B ≤ 3A after C.ZIG: conditional

`B = Q_B + Z_B ≤ 2A + A = 3A` needs U4 plus C.ZIG (`Z_B ≤ A`, banked
AUTHOR with V1–V3 mechanical assembly still open — unchanged status).

## P. Exact remaining path to Dynamic Optimality

1. Closed-component capacity lemma (U4 core) ⇒ `Q_B ≤ 2A` (all cycles).
2. C.ZIG mechanical assembly (V1–V3) ⇒ `B ≤ 3A`.
3. Banked chain takes over: `E_B ≤ 3S_A + g` (PIVOT-2) ⇒ `LT ≤ 7LT + 2g`
   (parametric translation) ⇒ DO via Levy–Tarjan (eventual approximate
   monotonicity + repeatability + coercibility — banked conditional).
No other obstacle is known; no constants need optimizing.

## Forensic appendix (falsification campaign)

- v2 ORIGIN (consumed pre-step edges in recursion set = U1 proof form):
  parity confirmed (hunt 100/100 lap2, identical profile).
- Siege: 255/255 full BUT long-walk/keep/cross batteries were vacuous
  (0 steady-state overflow — long random closed walks go shallow);
  cannon 60/60 meaningful (overflow-dense by construction).
- Breeder (spliced shared-state overflow cycles): n=6 60/60 (maxlen 52,
  mean ovf 2.2), n=7 80/80 — the strongest adversarial evidence.
- Per §26: no mechanism failure found, so mechanism-vs-theorem
  classification never triggered; `Q_B − 2A ≤ 0` on every tested cycle.
