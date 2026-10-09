# PIVOT-2 — RECURRENT EXCESS (maximum cycle ratio)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d` + C181–C193/PIVOT-1 tree
(preserved; nothing reset/committed). Oracle: `scripts/wp6_cycle_ratio.py`
(graph+SCC), exact ratio via Dinkelbach + integer Bellman-Ford
(`C:/Users/SAIFMA~1/AppData/Local/Temp/opencode/ratelib.py`;
float-free; worst case honest-uncertified, never wrong).
Periodic hunt: `scripts/wp6_periodic.py`.

## A. Exact graph theorem

W_C(H) = B(H) - C*A(H) definitional (kernel `reward_identity`,
`reward_add`, `reward_pump_step`, all green). Equivalence
(bounded-W ⟺ no positive cycle): (A=>B) pump argument; (B=>A)
cycle-excision to simple paths + finite max = g_C(T0). Standard;
AUTHOR-recorded (list-excision machinery not kernelized; arithmetic
closure is green).

## B. Zero-A cycles: NONE (theorem + finite)

AUTHOR proof (universal, no reachability needed): A-cost 0 forces every
access A-noop (ecount_eq: 0 events ⟺ depth 0), so A is constant and every
accessed key is its root r; B moves only on KEEP r; first KEEP r roots B
at r forever after (DELETEs freeze), so a closed walk has B-cost 0
(either B never changes, or start already r-rooted and all noops).
Oracle verification: T0s with zeroA-posB cycle = 0/14 (n=4), 0/42 (n=5),
0/132 (n=6). Periodic hunt to n=256: none (would have saved
zeroA_kill.json).

## C. rho_n (exact rational table)

| n | shapes | pair nodes | reach/T0 | SCCs | recurrent | rho_n | extremal (A,B) |
|---|--------|-----------|----------|------|-----------|-------|----------------|
| 2 | 2 | 4 | 4 | 1 | 1 | 1 | [K2,K1] (2,2) |
| 3 | 5 | 25 | 25 | 1 | 1 | 1 | [K1,K3] (2,2) |
| 4 | 14 | 196 | 196 | 1 | 1 | 3/2 | [K2,K1,K3,K4] (4,6) |
| 5 | 42 | 1764 | 1764 | 1 | 1 | 3/2 | [K5,K4,K5,K2] (4,6) |
| 6 | 132 | 17424 | 17424 | 1 | 1 | pending (graph built; Howard+cert pending) |

All CERTIFIED (exact integer BF: no positive (qB-pA) cycle at rho +
explicit achiever). Every T0 reaches every pair (single SCC throughout):
per-T0 distinction vanishes; one rho per n. Extremals are all-KEEP
(DELETEs dilute); n=4 uses all 4 keys, n=5 uses 3 keys {5,4,2} with a
repeat (K5 twice).

## D. Extremal anatomy

- n=4 max-single-edge: (K3, a=1, b=2, ratio 2) + min-A BFS return
  [(K1,1,1),(K2,1,2),(K4,1,1)] (A=3,B=4) → closed A=4,B=6 = 3/2.
  Local monster (2×) + recovery tax (3 A-cost) = recurrent 1.5×.
- Twin-locked periodic cycles (sweeps [K1..Kk]) always ratio exactly 1.
- Two-key exhaustive (n=16) max 1.0; descending runs max 1.0;
  extremal-pattern seeding (oracle shapes lifted) max 1.0 to n=64.

## E. Recovery tax

- Small-n exact (BFS/Dijkstra on oracle graphs): above.
- PIVOT-1 steered n=64/128 bad epochs (local 15/15.5): return paths
  NOT computable (state space; BFS infeasible; no reliable heuristic).
  Open measurement. (Their pre-states are twin-adjacent per 8AC-TWIN0;
  post-states double-rooted.)
- Checkpoint graph (post-KEEP nodes, Dijkstra A-distances, epoch
  weights): rho = 3/2 CERTIFIED at n=4, agreeing with primitive graph.
  Semantics cross-validated both ways.

## F. Large-n cycle hunt

Deterministic replay + exact hash-equality cycle detection (tails
allowed), n=16..256, random/structured words × diagonal/diverged starts:
max ratio 1.0 everywhere (2048 two-key exhaustive at n=16; sweeps;
extremal patterns). No zero-A kill. No ratio >1 beyond oracle 1.5.

## G. Structural mechanism

- Dual bias (exact BF longest-path potentials at C*=3/2, n=4):
  corr(h, Σ|dA−dB|) = 0.734, corr(h, positive part) = 0.61.
  High-bias recurrent states = high depth-disagreement. Microscope only.
- Working conjecture (unproved): rho ≤ 3/2 universally. Support: exact
  n≤5, periodic ≤1.0 to n=256, extremal patterns ≤1.0 to n=64.
  KEEP-side mechanism open (recovery conservation law not yet isolated).

## H. Scientific status

Outcome 3: FINITE RECURRENT CONSTANT STRONGLY BOUNDED (≤1.5 everywhere
measured, certified n≤5), UNIVERSAL MECHANISM NOT YET PROVED. No new
theorem tree. Next: SAME extremal cycles ([K2,K1,K3,K4],
[K5,K4,K5,K2]) — why 3/2, what breaks the pattern, n=6 Howard+cert,
recovery-tax at scale. LT repeater mapping: cycle γ with (A,B) gives
histories Pγ^k with E_B/S_A → B(γ)/A(γ); startup prefix washes out as
k→∞; matches LT repeater shape (exact state restoration is stronger
than LT's tree restoration).

- rho_6 = 5/3 EXACT (integer-BF cert upper + replay-verified
  achiever [K3,K6,K3,K4,K2,K1] A=6 B=10). Universal 3/2 DEAD.
- 3/2 motif interval-lifts to ALL n>=4 (gap-block opacity; verified
  n=12,16,24,104): sup rho >= 3/2 universal floor. 5/3 lifts to
  n=12,36 verified: sup rho >= 5/3.
- Pattern rho_{2k}=(2k-1)/k suggests sup 2; n=8 motif hunt open.
- No growing (unbounded) family: periodic/two-key/sweep caps 1.0.

## PIVOT-4 append: two-lane verdicts + defect floor + B=R_A pattern
[SUPERSEDED on DOUBLE by PIVOT-5 below: DOUBLE is FALSE (n=5 witness).
ZIG claims stand.]

- Lane identities kernel green (`lane_split`, `lane_sum`).
- DOUBLE (Q_B<=A) + ZIG (Z_B<=A) hold on: oracle extremals n=2..6
  (n=6: QB=4<=6, ZB=6<=6 tight), 32 mixed closed walks, periodic,
  twin, steered. NO failures anywhere. Suspected sharp anatomy
  CONFIRMED on both maximizers: Z_B=A, Q_B=A-2, B=2A-2, defect=2.
- ROT dead (min n=3); R-invariance twin-trivial only; lip_compose green.
- Matching saturates wherever counts allow (tautological); per-access
  lane bounds hold on extremals (a=1 everywhere there) but fail
  generally (A-free KEEPs). No proof leverage beyond inequalities.
- Defect_2 = 2A-B: min 2 over sampled nontrivial cycles (never 0/1);
  extremals exactly 2. New exact pattern: extremals satisfy B = R_A
  (B-events = A-rotations) and defect = Z_A = 2. Origin unexplained.
- n=8 hunt (motif extension + beam): max 1.0 (twin-locked); 7/4 open.
- B<=2A unproved universally (needs DOUBLE+ZIG proofs); no lane-crossing
  witness (would need Q_B+Z_B>2A: none found).

## PIVOT-5: DOUBLE REFUTED, ZIG PROVED (formalization: V1-V3 open)

- DOUBLE (Q_B <= A universally on closed cycles) is FALSE. Exact
  replay-verified witness, n=5: [(K,5),(K,1),(K,5),(K,3)], closed,
  QA=2 ZA=2 QB=6 ZB=0 A=4 B=6. So Q_B=6 > A=4 (all B-doubles, zero
  zigs). Onset n=5 (n<=4 DOUBLE holds exact). ZIG holds there
  (0<=4, slack 4 covering excess 2); B=6<=8 holds. (Mission §21
  followed: minimality open (len 4 witness; shorter unchecked).)
- ZIG (Z_B <= A on closed pair-walks) PROVED by run-structure.
  Full AUTHOR proof: partition cycle into maximal A-noop runs (A-noop
  <=> accessed key is current A-root, present-domain; root constant
  across run since noops preserve tree; runs are same-key repeats).
  Cyclically every run has a preceding nontrivial access (else all-noop
  case: A=0 total => B=0 by zero-A argument below => Z_B=0).
  In a run (key r): at most ONE B-zig (first KEEP r iff B-depth odd;
  after it B rooted r; rest noops/frozen). Leading access L (nontrivial,
  key r by delivery, a_L>=1): if KEEP r, B rooted after L so run has
  zero B-zigs and L's own B-zig (<=1) pairs same-access (a_L>=1);
  if DELETE r, L has no B-events and run's <=1 B-zig pairs to L's
  A-StepEvs (all free). Pairings use disjoint access sets (KEEP-StepEvs
  vs DELETE-StepEvs), at most one claim each: injective. Hence Z_B<=A.
  Zero-A case: A=0 => all accesses A-noop => A constant, all keys=root r;
  B moves only on KEEP r; first such roots B forever (DELETEs freeze);
  closure forces B-cost 0 (else end-B != start-B), so Z_B=0<=0.
  Consumed premises, exact status (verified this run): deliver (+copy),
  splay_at_root, ecount_root, mem_splay, delete_step (History),
  ecount_eq (StepCount), valid_rotR/L — ALL KERNEL-GREEN. Open
  mechanical only: (V1) validity for doubles/fixups + splay-induction
  composition; (V2) mem->sdepth-some link in ecount-zero chain;
  (V3) history-fold + run-partition + matching formalization.
  The mathematics has no gaps; what remains is formalization labor.
  No reachability used: holds on ALL closed pair-walks, not just
  reachable. No finiteness invoked.
- Consequence: B<=2A needs Q_B <= 2A-Z_B (excess<=slack); no mechanism
  (all reformulations tautological; counting arguments provably
  insufficient since closed identity-words have unbounded cost ratios
  in general; geometry = bystander wall). OPEN.
- Prior PIVOT-3/4 records (ROT refutation, R-invariance verdict,
  lip_compose, rho_6=5/3 exact, 5/3 anatomy, motif lifts, pattern,
  growing-family status) consolidated in §H below; not repeated.

## PIVOT-6 REPLACEMENT: DOUBLE-FLEX (Q_B <= 2A-Z_B)

- B.DOUBLE kept dead (n=5 [(K5),(K1),(K5),(K3)], QB=6>A=4,
  replay-verified; all six B-doubles zig-zig; ZB=0). No resurrection.
- C.ZIG (Z_B<=A) via run-structure AUTHOR proof: partition into maximal
  A-noop runs; <=1 B-zig per run (first KEEP); leading nontrivial access
  funds (KEEP self-pairs, DELETE funds run); disjoint KEEP/DELETE
  capacity => injective => Z_B<=A. Zero-A subcase via first-KEEP-roots
  argument. Consumed premises: deliver (kernel), ecount-zero/root/noop
  chain (assemblable from banked ecount_eq/steps_nil_root/splay_at_root),
  DELETE-freezes-B (engine), absent vacuous (present-domain),
  validity-full-splay (PARTIAL: single rotations banked valid_rotR/L;
  doubles + splay-induction composition OPEN mechanical). Holds all
  closed walks incl n=5 exact BF (no positive (ZB-A) cycle). No
  reachability needed, no finiteness invoked.
- V-max (B-2A): max -2 sampled, never positive; V=0 ATTAINED (tightness
  confirmed: B=2A reachable). So bound would be tight, not strict.
- Run-local q_r<=2a_r-z_r: tight/0/-1 on extremals; random Floyd yields
  only trivial cycles (untestable there); steered deep-B runs would need
  window borrowing (= global form).
- n=5 regression full matching (canonical owner_Z EMPTY since ZB=0;
  greedy PRIMARY-same then free-FLEX with DISTINCT slot namespaces):
  6/6 saturate; the 2 overflow doubles are 2nd doubles of B-depth-4
  accesses (1 A-StepEv each); FLEX absorbs (all 4 free). PRIMARY/FLEX
  are distinct (2 slots per A-StepEv).
- StepEv-type parse (bottom-up turns) validated 360/360 vs engine sets.
- ZIG-saturated (ZB=A>0): absent in walks (only oracle extremals, where
  Q_B=A-2 fits PRIMARY). Vacuous there.
- Per-A-StepEv books: PRIMARY 1 + FLEX 1 each; ZIG takes FLEX only;
  DOUBLE takes PRIMARY + free FLEX. B<=2A still needs excess<=slack
  (open; all reformulations tautological; counting provably insufficient
  via identity-word cost ratios).

## PIVOT-7 DOUBLE-FLEX ASSAULT (Q_B <= 2A-Z_B): NOT PROVED

- ZIG stands proved (run-structure AUTHOR + premise audit; holds all
  closed walks incl n=5 exact BF; no reachability needed).
- DOUBLE-FLEX (equiv B<=2A) OPEN. Exhausted: excess-slack has no
  mechanism (all reformulations tautological); counting provably
  insufficient (identity-words); divergence-telescoping DEAD
  (V-C*dd to +1798, anti-correlated); run-local needs window borrowing
  (= global form); per-access forms false (A-free KEEPs).
- Corpora clean (V-max -2; V=0 UNATTAINED — corrects earlier tightness
  claim: max V observed -2, equality B=2A never observed; tightness OPEN).
  True on all evidence, unproved: B-doubles vs A-StepEvs across
  arbitrary-B/A accesses.
- Run-local (q_r<=2a_r-z_r per block) SUMS to DOUBLE-FLEX exactly, so it
  is the sharp sufficient form; holds tight on extremals/killer
  (0/-1/0); fails on open steered deep-B runs (q=5-16 vs 2);
  closed-only status open (needs diverged-closed test).
