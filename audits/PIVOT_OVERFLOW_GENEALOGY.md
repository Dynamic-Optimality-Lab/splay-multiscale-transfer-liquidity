# PIVOT-13: Overflow Genealogy → Coarse-Double (finite charging via creator+setup matching)

Status: FINITE_EVIDENCE (strong) — universal `Q_B ≤ 2A` remains OPEN.
Target unchanged: `Q_B ≤ 2A` on reachable closed Pair-Access cycles.

## 1. What was built

StepEv-level charging machinery (`scripts/wp6_overflow.py`):

- **Objects.** LEFT = B-double StepEvs (the Q objects: zigzig/zigzag steps with
  ordered triple `(x=node, p=parent, g=grandparent)` + pattern LL/RR/LR/RL +
  transferred-subtree keys). RIGHT = 2 credits per A-StepEv (2A total).
  Count identities VERIFIED per access by assertion:
  `#A-steps = a`, `#B-doubles = q = floor(dB/2)`, `#B-zigs = z`.
- **Rotation log.** Every B-rotation logs its changed `(child→parent)` edges
  with `(acc, seq)` stamps (3 entries per rotation: risen node, pushed-down
  node, transferred subtree). A-rotations logged symmetrically (soup only).
- **ORIGIN / creator.** `ORIGIN(e)` = latest strictly-prior access establishing
  ancestor edge `e`, recursed transitively through same-splay steps to a
  strictly-prior access; `{GENESIS}` if never built in-history.
  `creator(D)` = latest (max acc id) of `ORIGIN((x→p)) ∪ ORIGIN((p→g))`.
  Canonical: previous-KEEP-root preference falls out (latest-builder wins).
- **Setup (E4 reborn).** `setup(t,x)` = latest access before `t` that splayed
  `x` in A from non-rooted (A-root-arrival). Eligibility: doubles of `(x,t)`
  ↔ setup access's A-credits. Needed because starved `a=0` overflows have
  starved (`a=0`) creators — the paying work is the setup access's A-splay
  (often a DELETE: pure slack, zero B-demand).
- **Matching.** Kuhn max-matching, adjacency local-first (local, creator,
  setup). On failure: König Hall-violator `(X, N(X))` with per-double detail.

## 2. Overflow canonical form (frozen)

Deepest-first: local `2a` credits pay the FIRST `2a` (deepest, earliest-executed)
doubles; overflow = the LAST `q−2a` (shallowest). **Empirically moot**: over
150 overflow cycles, overflow is overwhelmingly single-double `(a=0,q=1,eps=+1)`
(orientation coincides trivially); the only multi-double overflow seen is
`(a=0,q=2,eps=+2)` (4 cases) where `k=q` so both orientations coincide too.
Partial-overflow (`k<q`, `q≥2`) NEVER observed. No `(a=1,q=3)` anywhere.

## 3. Vignettes (real oracle output)

- **(a=0,q=1).** Word `[D3,K3,K2,D1,K1]`, lap2 acc6 `(K3)`: `dA=0, dB=2`,
  double `RR` over `(3,2,1)`. Local 0 credits. Creator = acc4 (lap1 `K1`,
  built the stack); setup = acc5 (`D3`, brought 3 to A-root with `dA=2`,
  2 credits). Textbook starved-overflow paid by setup/creator.
- **(a=0,q=2,+2).** Word `[K6,D4,K4]`, acc2 `(K4)`: `dA=0, dB=4`, doubles
  `RL(4,5,3)`, `LR(4,1,6)`. BOTH doubles → creator acc0 (`K6`) credits
  (full-history match 2 local + 2 creator). The KEEP that built the deep
  4-chain pays for its consumption — the §4 story verbatim.
- **5/3 cycle:** lap2 all 4 doubles have creators (acc−2/−3, different keys);
  match fully LOCAL (all eps ≤ 0). Genealogy engages exactly on overflow.

## 4. Matching results (all FINITE_EVIDENCE)

| corpus | lap2-steady full | full-history full |
|---|---|---|
| hunt n=6, 200 overflow cycles (2-lap) | 200/200 | 189/200 (11 = lap1 genesis-transient) |
| walk n=6, 61 cycles + 5/3 + n5-killer | 63/63 | 63/63 |
| walk n=7, 35 overflow cycles | 35/35 | 29/35 (6 transient) |

Steady-state (lap2) genesis rate = 0.000 everywhere (all edges churned;
full genealogy). Creator distances 1–9. Access-level creator chains ≤ 10
hops, all terminating (genesis/setup/none); no loops observed.

## 5. Hall autopsy (pre-setup failures → the setup rule)

With local+creator only: 7/200 lap2 failures. All one family: SHORT
alternating `D,K` cycles (`[D1,K1,D3,K3]`: eps `−2,+1,−2,+1`) whose `+1`
doubles are `(a=0,q=1)` with `a=0` creators — Hall set `X` = the starved
doubles with `N(X) = ∅`. Fix: setup edges (`K1`←`D1`-setup,
`K3`←`D3`-setup) → 200/200. The deficiencyPRODUCTIVELY identified the
missing rule (setup/DELETE-slack), now banked as §14.4 path.

## 6. Nonconsecution (§19)

40 overflow cycles, lap2 legs: overflow-run lengths = {1: 29} — ALL runs
length 1, ZERO consecutive overflow pairs. Overflow accesses are isolated
(single-step spikes, immediately repaid). No floor-minus argument needed;
reported as observed finite regularity (universalization: open).

## 7. Epsilon ladder (§6)

Overflow needs observed: `(a=0,q=1)` ~all; `(a=0,q=2)` 4/150 cycles; nothing
higher; `(a=1,q=3)` absent. Restated ladder `q ≥ 2a+1` stands (PIVOT-12);
the data says nature lives at its bottom rung (`a=0`).

## 8. rho_Q bounds (§4/§7/§9)

Upper = `rho_n` analytic (n=2..6: 1, 1, 3/2, 3/2, 5/3). Lower (best-found):
n=6: 2/3 (5/3-word Q/A=4/6); n≤5,7: 1.0 (random corpus); n=7 achiever words:
0.833 (5/3-word @diag 5), 0.857 (`K2,K1,K3,K4` @diag 400) — degrade
off-diagonal, random 1.0 stands. n=7 upper OPEN (`rho_7` unknown, no BF).
Exact-max (Dinkelbach/Howard) NOT pursued: scratch Howard had an off-by-one
depth-table bug caught by replay-verification; analytic `max W_Q = 0` (n≤6)
is stronger anyway. Howard निर्णायक dropped, no loss.

## 9. Vine-slack lemma (§20, AUTHOR)

On vine-pair-preserving accesses (n≥5): V1 ⇒ splayed depths ≤ 1 ⇒ `q=0`
(KEEP: B-depth ≤ 1; DELETE: B frozen, no StepEvs). n≤4 via global analytic
(mirror exceptions absorbed). So vine chambers contribute ZERO Q — the
matching only ever works the non-vine chamber. Universal, banked.

## 10. z-thread (§21)

Excursion re-census CONFIRMS caps: n=6 W₂ ∈ [−12,+2] (58 pos: 50×+1, 8×+2);
n=7 W₂ ∈ [−18,+2] (104 pos: 103×+1, 1×+2). Positives: short (len 3–4),
K-only, exit `K1/K6` with `dB ∈ {4,5}` vs `dA = 2` (B-deep/A-shallow
residuals, self-repaying per PIVOT-9-2). E4b (`B ≤ 3A`) 0 violations both.
z (zigs) ride along but never break the +2 residual cap; C.ZIG unchanged.

## 11. n=32 W_Q trace (§22)

Cited from `coarse_double/regressions.json`: A=31 Q=49 Z=22 WQ=−13; trajectory
peaks +23 mid-sweep, fully repaid by return. Old +9 was Z-noise. The
excursion-bit refutation (+9 W₂) is a Z phenomenon, not a Q phenomenon —
Q stays charged throughout (consistent with this pivot's matching).

## 12. Rotation soup (§24)

300-access walk (n=6): A = 198 doubles + 140 zigs; B = 136 doubles + 106
zigs. Zigzig (LL+RR) dominates zigzag (LR+RL): A 120 vs 78, B 86 vs 50.
Bottom-up execution is STRUCTURAL (capture loop starts at `path[-1]`,
deepest-first by construction). No soup anomaly; recorded for the
restoration-wall file.

## 13. Zig-first (§23)

Moot: capture order = execution order (bottom-up) by construction; the
orientation question collapsed empirically (§2). No zig-first variant built.

## 14. Minimal-counterexample framing (§25)

A minimal `Q_B > 2A` closed cycle must SIMULTANEOUSLY defeat: local credits
(`eps ≤ 0` everywhere fails first), creator genealogy (short, terminating
chains 1–9 back), AND setup/DELETE-slack — with a Hall set surviving all
three eligibility classes. Search criterion is now concrete: hunt for
`charge()` returning `full=False` on lap2-steady cycles. 296 cycles tested,
0 survive. The wall (if it exists) is NOT in short-cycle space n≤7.

## 15. Counting alternative (§18)

Not pursued: the matching superset already yields finite chargings; global
counting (`Q ≤ 2A` restated) is kept as a universalization path, not needed
for discovery. No work lost.

## 16. Universalization assessment (§14) — what remains OPEN

PROVEN (finite): local+creator+setup charging exists on 296 overflow cycles
(n≤7) + hard corpora. OPEN (universal): creator-existence lemma (every
overflow double HAS a strictly-prior builder on closed cycles — genesis
dies in steady state: needs proof that closed-cycle B-edges churn fully),
chain-termination (no creator loops on closed cycles), setup-availability
(every starved access has a setup access with unused credits IN THE CYCLE —
wraparound credit accounting), nonconsecution universally, and the entire
non-vine-only chamber characterization. VINE_VISITING_C2 stays OPEN (the
excursion-bit refutation is untouched by this pivot — different claim).
Global `Q_B ≤ 2A` (hence `B ≤ 2A`, hence DO): OPEN.

## 17. Files

- `scripts/wp6_overflow.py` — instrumented replay + ORIGIN + matching oracle.
- `scripts/wp6_hunt.py`, `scripts/wp6_walk.py`, `scripts/wp6_ovf_anal.py`.
- `artifacts/.../overflow/hunt_n6.json` (200/200), `walk_n6.json`,
  `walk_n7.json`, `analysis.json` (chains/orientation/soup/vignettes/rhoQ).
- Count identities assert-verified; 5/3 replay reproduces banked A6Q4Z6B10.
