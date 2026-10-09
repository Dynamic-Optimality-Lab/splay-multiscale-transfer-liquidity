# PIVOT-25R: constraint-guided dual — L2 loop executed (GREEN n=7, wall n=8/9)

No new pivot, no E0 return, no candidate ranking. Twin-only kept ONLY as
baseline with FREE class values; every constraint below covers ALL concrete
edges of its size (repair-can't-break-satisfied enforced by max-per-class).

## 1. L1 decode (canonical replay: fresh ptr + splay_cap, cross-checked vs trans)

Stored root-pair cycle [(7,7),(1,1)], w=+1 each way (twin 1->1 throughout):
- e1 `(28,0)K7`: dA=2 dB=6 a=1 q=3. Pre roots (1,1), BOTH vine, md 6/6.
  Post (339,345) roots (7,7), BOTH non-vine, md 5/4.
- e2 `(297,428)K1`: dA=1 dB=6 a=1 q=3. Pre roots (7,7), BOTH vine, md 6/6.
  Post (90,83) roots (1,1), vineA kept, vineB destroyed, md 6/4.
- Stitch1 `(339,345)` vs `(297,428)`: same root-pair (7,7), differ in
  vineB (F vs T), vineA, maxdepth. Stitch2 `(90,83)` vs `(28,0)`: same
  (1,1), differ in vineB (F vs T). Smallest separator: ONE bit isVine(B).
  Artifact: `dual_mine/l2_decode.json`. Script: `scripts/wp6_l2decode.py`.

## 2. L2: alpha=(rootA,rootB,isVineB), Phi=-2*twin+P_alpha, P FREE

Constraint per concrete edge: P[U]-P[V] >= c(e),
c = w-2*(twin'-twin), w_KEEP=floor(dB/2)-2*ceil(dA/2), w_DEL=-2*ceil(dA/2).
Max-c per abstract edge over ALL edges (both modes), BF on costs -c.
- n=7: concrete=2576574, classes 63/98, abstract edges 875,
  FEASIBLE (3 passes). Artifact `dual_mine/l2_refine7.json`.
- Independent verifier (fresh trans derivation + stored-table match +
  all-inequality check): 2576574/2576574, 0 bad. GREEN.
  Script: `scripts/wp6_l2verify.py`.
- Methodology fix found by the verifier (RED caught it): pot extraction
  used P=-dist; correct is P=dist (dist[v]<=dist[u]+cost, cost=-c).
  Feasibility booleans (L0/L1/L2/L3) are sign-independent, unaffected;
  `cegar.json` stores no pots. Old `wp6_cegar.py` pot line has the same
  latent sign issue — unused, noted, not rewritten.

## 3. Compact evaluator + update-proof attempt

P_7 depends ONLY on vineB (all 63 classes): P=0 if B-vine, -1 else.
Compact, total, n-independent: Phi(s) = -2*[rA==rB] - [B non-vine].
- DELETE (B frozen): drop = 2*DT. a=0 => x is A-root => twin fixed
  (DT=0, drop 0 >= 0). a>=1 => drop >= -2 >= -2a. PROVED universal (AUTHOR;
  kernelization needs Lean tree-model alignment — open, minor).
- KEEP reduces to: 2*DT + DNV >= q-2a (DT=twin'-twin, DNV=nvB'-nvB).
  Twin pays <=+2, vine <=+1; q unbounded with n. Universal KEEP is the
  whole remaining obligation (see 5).

## 4. Loop continuation (INFEASIBLE branches with decoded stitches)

- Compact @ n=8 (ALL 32.7M edges): RED, 72252 bad, all KEEP q=3:
  (a=1,q=3,w=1,drop=0,twin kept,B non-vine kept) x35496;
  (a=0,q=3,w=3,drop=2,twin 0->1,B non-vine kept) x36756.
  Ex: (ia=0,ib=89,x=3): A-vine root1, B non-vine dB>=6, (1,1)->(3,3).
  Artifact: `dual_mine/l2_transfer8.json`.
- L2 FREE-P @ n=8 (128 classes, 80 present, 1264 abs edges, 32.7M conc):
  INFEASIBLE, cycle [(2,2,0),(7,7,0),(8,8,0)] (+3), witnesses
  (457,429,x8) (1091,1003,x7) (869,910,x2), all a=1 q=3 w=+1 twin-kept
  B-non-vine-kept. Stitches all incompatible; stitch0 end (1189,1195)
  vs start (1091,1003) share (8,8,0), differ in vineA (F vs T).
  Artifact: `dual_mine/l2_refine8.json`.
- L3 (+vineA bit, 256 classes, 100 present, 1756 abs edges): INFEASIBLE,
  cycle [(8,8,0,0),(2,2,0,0),(7,7,0,0)] (+3); witnesses (457,429,x8),
  (869,910,x2), (1093,1003,x7, sibling of L2's) — all pre md 6/6, post
  md 5/{4,5}, vineA=vineB=False throughout. The vineA split did not touch
  the cycle. Artifact: `dual_mine/l3_refine8.json`.
- L4 identified, NOT executed: B-maxdepth>=6 bit separates L3 stitch0
  (end mdB 4 vs start mdB 6). Withheld deliberately: L2->L3 already shows
  the bit-chase (each split preserves the cycle in the all-False classes);
  bounded payments vs growing q (5) makes further finite-bit iterations
  moot for universality. This is reported, not hidden.

## 5. n=9 probe (compact vs q>=4 KEEP edges; targeted, lower bound, 200/200
shape-ordering replays + 43K a-asserts green): 256 qualifying B-moves,
1244672 pair-edges, RED 126836 in exactly 2 classes:
(a=1,q=4,w=2,drop=1,twin kept,vine 1->0) x65088;
(a=0,q=4,w=4,drop=3,twin 0->1,vine 1->0) x61748.
Every q>=4 edge starts B-vine and destroys it, twin pays maximally — still
short by exactly 1. At n=9, (a=0,q=4) needs drop 4; twin+vine ceiling is 3.
Each +1 of max-q demands another payment bit (~1 bit per 2 sizes);
unbounded q needs depth-proportional (unbounded-range) payment without
recharge side-effects = the E0/setup-era wall in quantitative form.
Artifact: `dual_mine/l2_probe9.json`. Full-425M census NOT run (probe is a
refutation, honestly scoped; q<=3 at n=9 unchecked for the compact form).

## N. Verdict + exact remaining obligation (honest OPEN)
- Finite: L2 dual certificate EXISTS at n=7 (twin + 63-class P, GREEN).
  No universal Phi. No `Q_B>2A` witness (900+ tests green; all CEGAR
  positive cycles died in stitching/detours).
- ONE obstruction (executed, not conjectured): bounded-payment vs growing
  q — twin(+2 max) + finite summary bits(+1 each) cannot cover q-2a for
  unbounded q; n=8 (72K) and n=9 (127K) give exact failing edges.
- Exact remaining obligation: a dual term with depth-proportional drop on
  (a<=1, large-q, twin-maxed, vine-destroyed-or-kept) KEEP edges that does
  not recharge elsewhere (max-terms fail: recharge-cancel/over-recharge
  net-negative, banked). DELETE lemma for the compact form is proved
  (AUTHOR); KEEP is the wall. DO conditional throughout.
- Lean: no new file (L2-7 table is finite-n data, not a universal theorem;
  DELETE lemma needs tree-model alignment before kernelization).

======================================================================
PIVOT-25R CONTINUATION (pair-sensitive campaign)
======================================================================

## C0. Domain/reward/sign freeze (§2)

State = all valid same-key BST pairs on ordered keys 1..n (no reachability
restriction): splay maps BST->BST (preserved), diagonals initialize,
every closed Pair-Access cycle is a closed walk here (covered); strong
connectivity not needed for telescoping. a=ceil(dA/2); KEEP q,w as
specified (w=q-2a), DELETE w=-2a; need Phi(s)-Phi(s')>=w. BF costs c=-w,
potentials P[u]-P[v]>=w, extraction P=dist (sign bug banked §2 above).

## C4. root_A-plus-B impossibility: VERIFIED (all-pairs domain, n>=64)

Checked all 7 steps: (1) depths 0..5 hold <=63<64 nodes; (2) deepest key
at depth>=6; (3) explicit A (root r, x child: interval BSTs rooted at any
prescribed key exist by recursion); (4) KEEP x gives a=1,q>=3,w>=1;
(5) twin (r,r)->(x,x), F(r,B)-F(x,B')>=1; (6) G(B)=F(root(B),B) drops >=1
per deepest-splay step (fresh A_k keeps each pair valid); (7) finite
shapes => cycle contradicts strict descent. Illustration at n=7:
B=right-vine, x=7, constructed A root-1/child-7: replay gives a=1,q=3,w=1,
twin->twin. SCOPE: abstraction-impossibility (fresh A per step), NOT a
Coarse-Double witness. Consequence: L2-family Phi=F(root_A,T_B) (incl.
unbounded tables over rootA/rootB/vineB) is impossible on all-pairs;
A-shape beyond root is genuinely necessary. L3+ escapes scope (vineA).

## C5. Stitch autopsies (scripts/wp6_l3stitch.py; l3_stitch.json/l4_stitch.json)

L3-8 stitches: required source always holds next key at B-depth 6
(fuel loaded; S mdB=6, S_Apath depth 2); actual destination discharged
(B-depth 2-3, mdB<=5). S1 has IDENTICAL next-key A-path in E and S
([7,1,2]). L4-8 stitches (+2 cycle, connectors c=0): S1/S3 agree on ALL
coarse features (roots, vines, maxdepths [6,6]/[7,6]); E vs S differ only
in deep-chain placement (S: key 8 at B-depth 6 via right-spine len 6;
E: depth 2, spine len 2). L5 candidate (B root-spine>=6) identified from
S1/S3, WITHHELD: witness-chasing (maxdepth already fails to separate S1),
same threshold wall family. No L5 run.

## C6. Refinement results

L4 = L3 + [maxdepth_B>=6] (q-fuel bit; stitch-justified, not arbitrary):
n=8, 140/512 classes, 2796 abs edges, 32.7M conc: INFEASIBLE, 4-cycle
(8,8,0,0,0)-(1,1,0,1,1)-(8,8,0,1,0)-(1,1,0,0,1) (+2); +1 KEEPs (90,2,x8),
(255,2,x8) + c=0 connectors (1001/1003,1359,x1). Artifact l4_refine8.json.
L2->L3->L4: each split preserves a positive cycle (bit-chase demonstrated).

## C7. Grammar battery (scripts/wp6_c1battery.py; c1_battery.json; 18 edges)

Phi=-2*twin+Psi. C1 Psi=D_B-2D_A: 14 FAIL (zig-recharge L4d/e w=0/drop=-1;
A-dividend toxicity S4a3). C3 Psi=-D_A: 14 FAIL. C4 Psi=+D_B: 3 FAIL only
(recharge, L4d, L4e — all D_B-rise cases). C5 Psi=-Agree(paths): 5 FAIL
(L1e2/S4a1/L4c drop 0<1 — agreement breaks elsewhere; PR914 needs 2 gets 1).
ACTIVE: C4 (fewest fails, exact witnesses). DEAD: C1/C3; wounded: C5.
Analytic kill: subtree-size weighting collapses (Sum|sub| = D+n identically
=> C6 == C4; rotation-invariance misread — recorded against repeats).
§4 A-variants in battery (S4a1 w=1 vs S4a3 w=-3, same rootA+B): direct
A-necessity illustration. n=32 excursion NOT covered (no replayable word
stored; per §9 instantiation rule, unclaimed).

## C8. Micro-annotation / update-proof status

Blocked on live candidate (annotation can't save false Phi: C1/C3/C5 false
on battery edges; C4 false on 3). Banked for future work: twin flips only
at root-touching steps (DT boundary-determined); A/B step counts exact
(replay asserts); zig can raise total depth (+1 measured L4d) — no depth-sum
J satisfies reward<=ΔJ per micro-step with boundary-matching Phi. No J built.

## C10-C11. Universal theorems / telescoping

DELETE (compact form): PROVED AUTHOR (§3 above). KEEP: OPEN (obstruction:
bounded-payment vs growing q, now + C4/C5 battery + §4 analytic scope).
No dual => no telescoping (§11 not triggered). C.ZIG/DO: unchanged,
conditional, not claimed.

======================================================================
REPAIR ROUND (pair-sensitive representation)
======================================================================

## R0. Status corrections (visible, historical claims retained above)

1. C4 (Phi=-2twin+D_B) is REFUTED AS A COMPLETE POTENTIAL: replayed
   violation w=0, drop=-1 on L4d (1001,1359,x1) [also L4e, recharge].
   Retained ONLY as ingredient/term; never a surviving candidate by
   failure-count comparison. Battery: c1_battery.json (21 edges).
2. L2/L3/L4 infeasibility refutes those summaries on tested constraints
   only. Recursive structural summaries (paired intervals) NOT exhausted
   (untested). No "finite summaries exhausted" claim.
3. Micro-annotation cannot rescue false boundary Phi (interior telescopes
   to endpoints). No J built (blocked on live candidate, not on effort).
4. BF-label mismatch never rejected a representation; only infeasible dual
   constraints (L2-8/L3-8/L4-8 cycles) and replayed edge violations did.

## R2. Stronger exclusion F(rootA,vineA,T_B): PROVED (all-pairs, n>=64)

All steps verified + illustration (A=[1,None,[7,M,None]] M branching:
vine_before=False, single zig a=1, q=3, w=1, roots (1,1)->(7,7),
vine_after=False). 62 keys/3 intervals => >=3-key interval exists (empties
allowed); median-rooted subtree branches; rotation preserves it rigidly
in L/M/R; x<r by reflection. G(B)=F(root(B),false,B) strictly descends
along deepest-splay (fresh A_k keeps pairs valid); finite shapes force a
cycle: contradiction. Scope: abstraction-impossibility, not CD witness.

## R3. Exclusion applied

Universally rejected: every architecture factoring through
(root_A,isVine_A,entire_B) — incl. L2/L3/L4 summaries and unbounded tables
over them, and any B-only addition (maxdepth, spine, orientation, full B).
Not identified: WHICH A-feature suffices. One arbitrary A statistic does
not automatically escape. L5-spine (B root-spine>=6, separates L4 S1/S3)
universally VOID by this theorem; finite n=8 run withheld (bit-chase x3 +
voidness; script support exists for revisit).

## R5. L4 full-tree decode (all 4 stitches, E/S trees printed in session)

Binding +1 stitches (S1 y=8, S3 y=8): A-cost identical (a=1 both sides);
differ ONLY in B-depth(8) (6 vs 2). S1 A-paths differ ([1,8] vs [1,7,8]);
S3 A-paths differ ([1,8] vs [1,2,8], parent flips 1->2; LCA_A(2,8) flips
8<->2). S0/S2 connectors (c=0, y=1): A-paths differ ([8,2,1] vs [8,1]).
NO stitch has coinciding A-paths. E rootkids show created structure
(S0: A=[2,None] B=[2,None]; S1: A=[None,8] B=[None,7]).

## R6. A-feature panel (9 stats: n,md,leaves,branch,root,Lsz,Rsz,prof...)

Only `prof` differs, only on stitches 0/1 (mirrored); stitches 2/3 agree on
ALL coarse A-features (S3 A-trees agree on root/md/leaves/branch/sizes/
profile/vine). Missing info is keyed fuel-placement (which key hangs
where + its B-depth) — no finite coarse summary captures it short of
lookup tables (§6 forbids calling that compression). Loop diagnosed-stopped
with evidence (NOT abandoned after one failure: L2->L3->L4 executed).

## R7-R10. Battery 21 edges (S2nv/ACTL/PR904 added, all replay-instantiated)

Tallies: C1 14, C3 16, C4 3, C5 7 FAIL. C4 passes S2nv/ACTL/PR904(+14);
its 3 failures are EXACTLY D_B-rise (recharge +4, L4d/e +1). C5 fails
PR904 (+3<4). Repair spec (open): zig-monotone B-payment (drops-or-holds
on every splay step kind) without -D_B contradiction; unbuilt, unclaimed.
Update analysis for retained terms: twin DT boundary-determined (roots
change only at root-touching steps); D_B per-double dividends vary in sign
(C1 data); zig raises D_B (measured +1). n=32 excursion still uncovered
(no replayable word). DELETE AUTHOR stands; KEEP/TELESCOPE open; C.ZIG/DO
unchanged conditional.

======================================================================
POSITIONAL ROUND (executed, not withheld)
======================================================================

## P3. Additive separability exclusion: PROVED (all-pairs, n>=64)

Phi=-2t+F(T_A)+G(T_B) impossible. Checked: A x-rooted always exists
(interval BSTs); KEEP x is 0-step no-op (a=0, replay-asserted); x deep =>
x!=root(B) => twin 0->1; F(A) cancels literally (A identical);
2+G(B)-G(B')>=q>=3 per deepest step; finite shapes => cycle contradiction.
Illustrated n=7 (A-root 7, B-vine, x=7: a=0,q=3,w=3,twin 0->1). Scope:
representation-impossibility (fresh A per step); joint/recursive open;
joint evaluator over separate measurements allowed. C4 (F=0,G=D_B) lies in
the excluded family (consistent with its 3 replayed failures).

## P4. Positional summary + splitting table (n>=2; n=1 trivial base)

alpha_pos = (alpha_L4, dA(n), dB(n), rank(LCA_A(2,n))); k_max=n/k_2=2 are
order ranks (reversal-asymmetric, documented; state-computable, never
anticipatory). lca() root-first bug caught+fixed (returned root always);
true deepest-first LCA used everywhere. Splitting table on L4 stitches:
S1 E=(1,2,8)vS=(2,6,7), S3 E=(1,2,8)vS=(2,6,2) separated on all 3 coords
(LCA claim confirmed: 8v7, 8v2); S0/S2 stay (0,0,8)v(0,0,8) (connectors).

## P5-P6. FREE-P feasibility (max-c over ALL edges, P=dist, BF costs -c)

POS-7: FEASIBLE (1064 classes, 27121 abs edges) — refinement monotonicity
holds. POS-8: 2448/262144 classes, 82851 abs edges, 32.7M conc —
INFEASIBLE, 5-cycle (+1) with B-vine class + c=-1 slack edge
(lpos_refine8.json; stitches lpos_stitch.json). POSA (+[mdA>=4], first
A-quantity bit; S1-mdA 3v5 recurring basis): 3168/524288 classes, 127190
abs edges — INFEASIBLE, 6-cycle (+1): +1s (1175,1429,1) vine-destroyed +
(496,560,3) nonvine-kept (A-sibling of POS witness), c=-1/0 connectors
(lposa_refine8.json). Saturation test: all 6 POSA merges differ in >=1
coord (0/6 agree) — splits separate, +1 archetypes re-route. Five
infeasible refinements (L2/L3/L4/POS/POSA), pattern stable.

## P7-P9. Evaluator / updates (no speculative formulas)

No live complete candidate (C4 term-only; C5 wounded). Grammar space
defined (affine+cases+minmax+recursion) with no active claimant. Micro-reward accounting
(q B-doubles x+1, zigs x0, A-steps x-2; replay-asserted per access) is the
only proved micro-lemma; J induction needs live Phi (blocked, not failed).
§10: full-graph scans dominate any subset (all 32.7M edges constrained);
battery regressions stand (21 edges); n=32 uncovered; no n=10 brute force.
§11: no dual => no telescoping (conditional chain preserved).

======================================================================
UNIFORM JOINT SUBTREE-CONTEXT ROUND
======================================================================

## U2. Countercertificate verified twice, banked with scope

Attachment joint_depth_template_countercertificate.zip (root folder,
extracted to temp opencode/jointcert; files inspected BEFORE executing).
Standalone verifier: PASS (42 transitions, 64/64 cancel, surplus
10971177). Repository replay (scripts/wp6_jointcert.py, keys 0..7 +1
translated): 42/42 exact (BST validity, post-trees, StepEv counts,
q/twin/rewards all match stored fields) => NO semantic mismatch.
Recorded: ADDITIVE JOINT-DEPTH TEMPLATE (-2twin+sum f(dA,dB)) REFUTED.
Scope: this template only (fixed twin -2; per-key additive; real-valued
f). NOT excluded: nonlinear histogram functions, max/min/recursion,
positional info, joint structural potentials, Coarse-Double. The 42 need
not form a closed cycle (they don't claim to).

## U4-U5. Richer context + screening

eta_s(x)=(d_A,d_B,n_A,n_B,omega), n=subtree size (=interval length,
BST property asserted per key), omega=weak-order code of the 4 interval
endpoints (order ranks = keys; both intervals contain x by construction).
417 distinct contexts on cert support; M_eta nonzero on 415 => old
multipliers do NOT refute the richer template (NOT feasibility).
Artifact: dual_mine/joint_screen.json. Script: wp6_jointscreen.py.

## U6. Free-g feasibility: FEASIBLE, exact, tiny ternary coefficients

Sparse set 67 edges (42-cert + POS/POSA/L4 witnesses + battery A-variants
+ PR904) x 580 vars, max-slack LP unbounded (huge nullspace) => probed
min-max magnitude: optimum 1/9. Rounded rationals verify EXACTLY 0/67
violated; every g in {-1/9,0,+1/9} (joint_g_minmax.json; first max-slack
assignment had wild solver-artifact magnitudes up to 5M -- meaningless,
superseded). Template ALIVE on hard constraints; NOT universal (67 edges
only). Next per loop: grow constraints, then compact G_theta (§9 unbuilt).

## U7-U11. Status

No refinement executed (no real cancellation obstruction yet -- nothing to
refine FROM). No evaluator (ternary pattern suggestive, no rule extracted;
rule extraction = §9 next step). Updates: eta coords need per-splay
derivations (retained-subtree symbolic discipline noted, unexecuted).
Micro-accounting stands (per-access asserts). DELETE AUTHOR; KEEP open;
no telescoping. C.ZIG/DO unchanged conditional.

======================================================================
GROWTH + COMPACT-RULE ROUND
======================================================================

## W4. n=11 range obstruction: replayed; ternary-range dead universally

A=root-1 right chain, B=root-11 left chain, KEEP 1: a=0,q=5,w=5,twin 0->1,
b_e=3 (canonical replay). Global |g|<=1/9 caps Phi-drop at 2+22/9=40/9<5.
Necessary range law verified: 2+n(U-L)>=floor((n-1)/2) => U-L>=1/2 limit,
symmetric M>=1/4 (necessary only). Bounded per-key g NOT ruled out
(n terms grow). Old ternary (U-L=2/9) provably non-universal -- was already
scoped finite-only; now mechanical. Added to constraints (A-rng11).

## W6. Growth batches (joint_grow.json, 66 rows; E already in 67, skipped
visibly): B-deep x=1 n=7..64 (b=q-2: 1,1,2,3,5,13,29) + x=n mirror n=11;
twin-to-twin a=1 x=7 n=9,11,16; 15 DELETE twins (B frozen, A-intervals +
twin-flips stressed); F: 40 n=7 same-(dA,dB,nA,nB) different-omega pairs
(small-w biased, documented). Every tree inorder-validated; every row
replay-instantiated.

## W6b. Re-solve: FEASIBLE exact on 133 edges x 1121 vars (joint_lp.json)

Max-slack t*~0 (boundary) => minmax probe: optimum 29/128 (|g|<=0.2266),
exact 0/133 violated, values in {+5/22 x546, -5/22 x436, 0 x137, -3/32 x2}
(joint_g_minmax.json OVERWRITTEN by grown solution; stale /67 print fixed).
Range 10/22 hugs the n=64 requirement 29/64 exactly (29.09>=29): §4 law
bites precisely as predicted. Min-max optimality uncertified (witness only).

## W7. TOTAL evaluator R1 (majority-list, 44 margin-x-omega cases + default
0; total/state-based): REFUTED 27/133, first failure cert edge (a=1,q=3,
w=1, drop 5/11). Candidate failure (sums need joint pattern, not per-cell
votes), NOT template failure. No second guess (one consequential attempt
per spec economy). Artifact joint_cand_r1.json.

## W9. Rotation-level eta-updates: DERIVED + ENGINE-CHECKED (new)

60 trials/95 steps: outside step-subtree 115 keys 0 viol (depths+sets
fixed); non-pivot-inside 387 keys sets IDENTICAL 0 viol (only pivots
change children); pivot 258 events; inside depth deltas in [-2,+2]
(+1:76,+2:16 -- blocks pushed down: the recharge mechanism measured).
Full-splay composition NOT claimed affine. Artifact joint_updates.json.

## W10-W13. DELETE audit: old compact theorem does NOT transfer (different
Phi; DELETE moves many eta contexts). Finite DELETE: 28 rows (14 cert +
14 new) exact-OK under grown assignment. Universal DELETE for Phi_g OPEN
(no total g). Micro-reward sum banked (replay asserts). No telescoping.
C.ZIG/DO unchanged conditional.

======================================================================
FULL-GRAPH CUTTING-PLANE ROUND (n=7 verdict)
======================================================================

## X3. Loop as executed (scripts/wp6_jointcut.py -> wp6_jointexact.py)

Init 133 rows (all replay-instantiated). Per iter: LP (sparse HiGHS) +
complete scan (trans tables + precomputed per-shape per-key static info;
2,576,574 edges asserted) + top-K distinct-signature cuts + state save.
Sign/shape bugs caught en route (sparse t-column, lca root-first,
re-rooting snapshots, duplicate e1). Eta-construction cross-checked
0/300 vs edge_row.

## X3b. Float milestone + exact wall

Float cutting-plane CONVERGED iter 11 (viol=0 tol 1e-4, 4515 rows).
Exact finalize FAILED: 101,603/2.5M bad under rounded minmax (caught
pipeline bug: final assignment never scanned; fixed by exact loop).
Exact loop 21 iters / 41,036 genuine rows: bad oscillates 101K->57K->
31K->28K->17K->1K->8.5K->32K->7K->25K (minmax vertex whack-a-mole);
LP feasible at EVERY iteration (no Farkas trigger). Deficit split at
S=2^30: 1.5K rounding grazes (2^-30) vs 27K real (>1e-3).
Big-batch test (18.5K cuts at once): no collapse (7K->25K).
Cause analysis: t*~=0 marginal throughout (margin-delta LP infeasible);
3880/13588 active rows break under /1024 rounding; U pinned 29/128.
CONCLUSION: float-FEASIBLE on complete n=7; EXACT status UNRESOLVED --
marginality defeats every fixed-denominator rounding; exact rational LP
unavailable (method limit, not template verdict, not compute).

## X5-X7. No Farkas (LP never infeasible); no synthesis (rightly withheld
per §6: representation viability undecided); n=8 NOT attempted (blocked
behind n=7 exact verdict; scale 32.7M-edge exact scans x oscillation =
resource-deferred with bottleneck stated, not a verdict).

## X8. Rotation identities banked with scope (joint_updates.json): outside
step-subtree fixed (115 keys, 0 viol); non-pivot key-sets identical (387,
0 viol); inside deltas in [-2,+2] (down-push measured). StepEv-kind
breakdown + full-splay composition OPEN. No J (no live total Phi).

======================================================================
EXACTIFICATION ROUND (rational polyhedron)
======================================================================

## Y1. Frozen system: 41,036/41,036 replay-verified EXACTLY (wp6_jointfreeze)

Zero-cell canonicalization RESOLVED a false alarm: 7,693 apparent
mismatches were Counter-vs-scan bookkeeping (unchanged keys counted vs
skipped), mathematically void; zero-stripped comparison gives 0 REAL
mismatches. Canonical form strips zero cells. Result: 41,024 distinct
rows, gcd=1 everywhere (all primitive), 12 cross-format dupes merged.
Artifact joint_frozen7.json. LP numerics unaffected (0.0 coefficients).

## Y2/Y6. Face + gauge (partial; LP-cost wall documented)

GAUGE PROVED: M*1=0 exactly (each row sums C_pre-C_post = n-n); uniform
shift g->g+c preserves every difference (same n) => fixing ONE value
preserves feasibility (justified normalization available, unapplied).
Pairwise EXACT analysis COMPLETE on frozen set: 0 proportional dupes
(all primitive), 0 negation pairs => no free forced equalities.
Persistent-tight/diverse-vertex BLOCKED: random/coordinate float LPs stall
>=20 min each (HiGHS degeneracy; maxslack-structured solves run ~6 s).
max-t re-confirmed t*~=0; margin-delta infeasibility carries to the full
set by superset (no rerun needed).

## Y3-Y5/Y7. RESOURCE-UNRESOLVED (exact verdict not reached)

Face parameterization, basis reconstruction, exact rational LP: BLOCKED
(no persistent set without diverse vertices; sympy dense exact methods
infeasible at 2132-dim; sparse exact simplex unimplemented; 41Kx2.1K
degenerate LP solves >=20 min each). t*=0 structural proof (forced
equalities) needs 2 LPs per candidate row: same wall. This is the §11-D
third option: NOT infeasible (LP status 0 throughout; 41K-row float
feasibility stands), NOT a compute timeout on a running solver, but a
missing exact-LP capability at this scale. Self-caught discard: one
throwaway probe printed bogus t*=1e6 from a mid-growth len(var) indexing
bug; all banked scripts use the safe two-pass/post-insert pattern
(grep-verified); no artifact impact.

## Y8-Y10. No new cuts (per §8 rule: exact g required first). n=8
untouched. No G_theta. No eta change. Micro/DELETE/KEEP/C.ZIG/DO statuses
unchanged (DELETE finite-OK with rounding caveat; universal proofs open).

======================================================================
B-DOUBLE PAYMENT ROUND (structural D campaign)
======================================================================

## R-A. ROTATION DISTANCE REFUTED (824 @n6; scripts/wp6_rotdist.py)

Rotation graph 132 shapes connected (diameter 7); single-step emulation
200/200 consistent. Triples: 8592 doubles, 4712 zigs. RD violations 824;
RZ 0/4712 (zigs safe for rho AND D2). Smallest: A=right-vine,
B=[4,[3,[2,[1]]],[5,_,6]], x=1, LL zigzig d=3, rho 3->3 (need <=2).
Exchange anatomy: B has exactly ONE geodesic move (to shape 61: rotate
ROOT 4 right, FAR from x=1); canonical first rotation goes to shape 70
(rho stays 3); full double lands 66 (rho 3). Canonical x-local moves are
never geodesic: splay fixes x's neighborhood (1 reaches depth 1) while
rho meters global disagreement including rehung regions. Exchange lemma
FALSE. Artifact dual_mine/rotdist6.json.

## R-B. INTERVAL D2 REFUTED (1318 @n6; scripts/wp6_interval.py)

D2=|I(A) triangle I(B)|/2. Lipschitz-1 PROVED structurally (Ix_new ==
Ip_old as sets: net one removal + one addition) + asserted (max exactly
1 over all rotations). Double-descent fails 1318. Same smallest triple:
I(A)={(k,6)} right-anchored; double destroys {(1,1),(1,2),(1,3)} but
creates {(1,3),(2,3),(3,3)}: trade -3/+3 nets 0. Predicted failure mode
(trade, not progress). Root-bonus recursion R=D2+K[twin] impossible for
ALL K: K>=3 needed (aligning double, worst Lipschitz displacement -2)
vs K<=0 (twin-destroy A-step); both witnesses real. Sharper: R inherits
D2's twin-kept double failures for EVERY K (K-term vanishes there).
Artifact dual_mine/interval6.json.

## R-C. E1 REFUTED (n=2 single A-zig; minimal possible)

E1=-2twin+depth_B(rA)+depth_A(rB): J2 holds exactly (B-double drops 2 via
depth_B(x); twin never destroyed in B-phase, measured DT in {0,+2}).
(A) fails: twin n=2, zig out of twin (1,1)->A'=[2,[1]]: twin +2 rise,
depth_B 0->1, depth_A 0->1 = total rise 4 > 2 (mechanically replayed,
single rotation). Twin-destroy + dual depth jumps. Whole-access E1 also
unexamined (irrelevant to step-level kill).

## R-D. E_del REFUTED (11/20 battery; scripts/wp6_recur.py)

Deletion-normalized root alignment (well-founded via n-1 deletion,
successor-splice, deterministic): E alone 11 fails, with twin 10 fails;
restructuring RAISES alignment cost (L1e1 1->2, PR904 1->4). Symmetric
agreement meters die by restructuring, same family as D2-trade.

## R-E. Symbolic StepEv tables EXACT (scripts/wp6_symtable.py, 346/346)

DbDrop with arbitrary sizes (pivots net 0 in doubles!):
LL: +2s1+s2-s3-2s4, recharge <=> outer-right heavy (min: s4=1 rest 0 -> -2).
RR: mirror. LR: +1+s1+s2-s4, pays iff s4<=s1+s2 (min fail s4=1: 0<1).
RL: mirror. ZigR: s1-s3 (total w/ twin+2: 2+s1-s3; recharge <=> s3>=s1+3).
Fail-to-pay rates: LL 51/85, RR 43/70, LR 18/63, RL 16/66, Z 19/62.
Recharge = outer-subtree descent (T4 down 2 in zigzig; T4 down 1 in
zigzag). Per-double twin+Db audit (400 trials): twin never destroyed
(DT in {0,+2}); 54/153 twin-kept doubles violate twin+Db>=1 (need joint).

## R-F. Fuel token: NONE ALIVE (required properties now precise)

Burned: geodesic progress (rho: canonical moves aren't geodesic);
shared intervals (D2: trade); A-root depths+twin (E1: twin-destroy);
total-depth dividend (C4: T4-descent); agreement count (C5: trade);
deletion-alignment (E_del: restructuring). Live requirement: survive
T4-descent AND twin-destroy AND disagreement-trade AND restructuring.
Disjunctive lead (recorded, untested): C4 pays L4c-family (Db +7),
C5 pays L4d-family (drop 0); twin pays neither (kept); max-combination
untested, NOT claimed.

## R-G/H. B-double consumption + zig: OPEN (no live D)

Twin facts banked: never destroyed in B-phase (DT in {0,+2}); zig always
creates twin in B-phase (+2). Zig needs JOINT>=-2; 19/62 zigs overwhelm
even twin+2 via Db (s3-s1>=3). No live JOINT.

## R-I/J/K. Conditional derivation PROVED (premises open)

IF some D satisfies (A)<=+2 per A-StepEv, (B)<=-1 per B-double,
(Z)<=0 per zig, THEN: DELETE gives -2a<=drop (a steps x<=+2); KEEP gives
drop>=q-2a (A-phase rise<=2a, q doubles drop>=q, zig holds); closed-cycle
telescoping gives Q_B<=2A. Implication proved; all three premises OPEN.
C.ZIG/DO unchanged conditional.

## R-14. Charging/bank: NOT pursued (two gates)

Needs scalar-impossibility meta-proof (3 dead candidates != proof: gate
unmet) AND collides with standing E0/Hall ban (global injective
assignment is Hall-flavored). Documented, not hidden.

## R-15. Missing local inequality (three minimal obstructions)

Primary: twin-kept B-double, Db stagnant: D-drop>=1 (Phi=D form);
smallest L4c (255,2,x8,K): ledger twin:0, Db:+7, Agree:0, E_del:-1, D2:0.
Mechanism witnesses: n=2 E1-killer (A-step rise 4; twin-destroy class);
L4d (Db-rise double, kills depth family). Obstacle class: candidate
(four refuted with exact minima) + universal proof (no live D).

======================================================================
REALITY-DISCOVERY ROUND (transport + lineage, no synthesis)
======================================================================

## T-A. Decomposition: B double = transport of 4 ordered intervals

Per orientation (LL/RR/LR/RL): pivots x,p,g + hanging blocks
(xL,xR,pO,gO) with keys/endpoints/sizes/attach-depths/deltas, A-side
(depth_A ends, LCA_A, LCA depth/size, is-A-subtree, cover count + ordered
pieces), pivot A-relations. Scripts wp6_transport.py (role-correct
pO/gO siblings; earlier self-caught pO/pivot mixup fixed + bank rebuilt).

## T-B/C/D. Bank 650 doubles (178 hard; transport_bank.json) + collisions

Hard accesses decomposed per-double + random harvest, pay=twinDrop+DbDrop
(hard iff <1). D0 (orientation+sizes): 286 classes, 2 ambiguous.
D1/D2: 1 ambiguous (twin pair RR(0,1,3,0): same geometry, twin 0v+2).
D3/D4: ZERO ambiguous (600/619 classes). All 5 D0 collisions explained
by TWIN alone (identical DbDrop within class; pay differs only by +2).
Residual ambiguity after (D0+twin): ZERO on 650 events.

## T-E/F. Naked-arrival signature (the answer)

DbDrop == size-formula on ALL 650 (role-mapped; rigid-block motion =>
shape-independent RIGOROUSLY, not just empirically). twinDrop in {0,+2}
by roots. Hence per-double pay is FULLY determined by (sizes, roots):
nothing else missing at double level. Hard-double statistics: inner
(xL+xR) mean 0.40 (118/178 exactly zero) vs easy 2.60; outer mean 2.17
vs 0.74. HARD = x arrives naked (nothing absorbed yet) + outer mass
present + twin kept. L4c sequence: xL 0->3->5 across doubles (absorption
inverts debt: -1,+3,+7; first double is the hard one).

## T-G/H. Lineage (lineage_bank.json; refine_motion.json)

Debt PERSISTS in B-depths until re-splayed; MIGRATES toward/away from
access paths (L4c inversion); SPLITS (cover rises 1->2+); MERGE
unobserved. A-cover flickers (1->0->1: placement churn, not monotonic
fixing) -- placement is volatile, sizes evolve monotonically-ish
(absorption). Per-double pivots net ZERO (x:-2,g:+2 / LR:-1); ALL dividend
from hanging blocks. Verdict: multiset-of-interval-debts with migration,
closest to (not exactly) token/stack.

## T-I/J/K. Shape, recursion, refinement, missing info, next object

Shape: PROVABLY irrelevant to per-double pay (rigid motion => sizes
only; twin => roots only). Recursion: same coarse descriptor + different
internal A structure was never needed -- D3 already separates; no
evidence forcing recursion (stated, not claimed sufficient). Common
refinement: COLLAPSES to singletons on hard states (no coarsening benefit
here); informative aggregation is by ROLE (pivot vs hanging position),
not refinement pieces (negative result, honest). MISSING INFO (plain):
double level CLOSED (twin+sizes); access level needs size-EVOLUTION
across steps (outer-heaviness dynamics + twin timing) -- lineage bank is
the dataset. NEXT OBJECT (proposed, unbuilt): sequence-aware meter over
hanging-block size evolution (absorption profile), NOT another static
bit vector.

======================================================================
DISCOVERY-EXPERIMENT ROUND (access-level unpaid + first-hardness)
======================================================================

## X-A. Design: exhaustive KEEP census (n=5: 8,820 accesses; n=6 sample:
6,000) with per-double (pat,sizes,twinDrop,DbDrop) sequences (harvest),
prefix-surplus profiles vs (+1/double, 0/zig) quotas, and access UNPAID
= w - (2Dt_total + R_B_total) under banked twin+depth terms. Scripts
wp6_trprofile.py (+D-census), wp6_trcollide2.py (ladders).

## X-B/C. Census: n=5 unpaid 518/8,820 (5.9%, max 3); profiles q0 4116 /
clean 3202 / borrower 1502. n=6 sample: 413/6,000 (6.9%, max 5). L4c:
UNPAID -6 (OVERPAYS; hardship purely local); L4d: +1 (genuine via Db-1).

## X-D/E. Ladder: P0->P2 keep 78-230 ambiguous classes (spread to 8);
T4 (orientation+sizes, no twin-word) still 95 ambiguous (twin timing is
the gap); binary borrower label stays ambiguous to P2 (78 classes).
Scale answer: coarse pre-state NEVER collapses ambiguity (determinism
needs fine geometry); full-trajectory+twin-word collapses trivially;
cross-access UNNECESSARY (0/7 persistence; 10/10 de-novo).

## X-F/G. FIRST-HARDNESS THEOREM (exhaustive, falsifiable):

borrower ==> first-hard 95-97.5% (n5 1428/1502, n6 1268/1300);
first-easy ==> NEVER borrower (0 cases both sizes);
UNPAID ==> first-hard 100% (n5 328/328, n6 276/276).
Recovery: 77% of hard-first accesses still pay (later overpayment via
absorption + twin creation). Unpaid lives in q=1 zigzig-hard-first
(n5 exclusively; n6 mostly + rare zigzag/a=2 outliers documented).
Residual: zig-state geometry (5%).

## X-H. Hypotheses: H1 first-hardness (necessary screen, state, finite);
H2 recovery capacity (remainder trajectory, finite); H3 prefix-debt
profile (measurement needing state predictor); H4 twin-timing
(early/never/late); H5 outer-heaviness evolution (mechanism).
Held-out (§8): n=6 fresh confirms necessity 100%, borrower rule 97.5%;
sufficiency broadens slightly (rare outliers) -- pattern survives
adversarially in the necessary direction.

## X-J/K. MISSING: pre-state predictor of RECOVERY (which hard-first
recovers: sizes-evolution + zig-state rule unbuilt). NEXT QUESTION: for
a hard first double with deficit d, which remainder classes
(orientation-word, size-evolution, twin-word) supply >= -d + (w - first_pay),
stated as pre-state features. Narratives NOT falsified (absorption, prefixes,
lineage all confirmed); simplest screen (H1) preferred where it rules.

======================================================================
HIGH-NEED RECOVERY ROUND (mass-flow recurrence discovered)
======================================================================

## H-A. Data: 55 high-need accesses (needs 3..15), full double sequences

Vine families n=9..16,32 (zigzig), twin x=7 n=9..12, random n=10..12
filtered, mirrors decided post-hoc in analysis. Artifact highneed_bank.

## H-B/C. Residual traces (r_1=need, per-double supply, zig residual)

Range: need=15 clears; R10-29 3->6 RISES; R11-9 need=11 clears to -12;
overshoot to -26 common (late overpayment via absorption + twin).
41/55 cleared by doubles; 14 need zig; 6 traces rise mid-access then
mostly recover. Non-monotone confirmed.

## H-D/E. Ladder + determinism: X4 (fringe) EXACT on scale data

Random n=9..11 (16K accesses, ~50K doubles): X3 1061 amb, V1/V2 (turns
or sizes alone) 1515/1853 amb, X4 (full fringe) 3247 multi-occ states
with ZERO ambiguity. Turns alone and sizes alone both insufficient;
fringe-as-whole is the deterministic carrier. (Sparse-data caveat from
55-access round resolved by scale.)

## H-F/G. Recurrence VERIFIED (61/61 discovery + 41/41 held-out)

LL:(L,2+R+U+V); RR:(2+L+U+V,R); LR:(1+U+L,1+R+V); RL:(1+L+V,1+R+U)
[RL mirror-argument was WRONG; held-out caught it; re-derived by hand].
Fringe:[new0]+old[3:] via side-persistence (keys never needed);
twin':1 iff remdepth==1 else kept (A-rooted phase). Supply: formula +
twin timing. Held-out (mirrors, PR904, RL-comb, delayed-twin,
unbalanced, fresh random): 41/41 after RL fix.

## H-H/I. Big questions + invariants + World

A (one more double clears): NO (R10-29 3->6 minimal). B (strict
decrease): NO (6 rises). C/D (simple bound/component): NO single
scalar survives collision elimination (need/remdepth/outer-inner all
ambiguous). E (recharge): YES then recovery. Invariants: none single;
joint state required. WORLD B (bounded terminal residual: unpaid<=5
n<=6; high-need clears; cross-access echo 0/7; access-local).

## H-J/K/L/M. Adversarial + held-out + compressed object + next

Adversarial built: alternating RL-comb (need 4), delayed-twin pair
(zig vs double creation), unbalanced fringe, mirrors, 12 fresh random.
Held-out: supply + full next-state 41/41 (one real bug found+fixed).
COMPRESSED: X*=(pat,L,R,U,V,tw,fringe,remdepth) + G_LL/RR/LR/RL +
F=formula+twin; residual relation observed (absorption+twin cover),
unproved. NEXT: prove G/F maps for arbitrary attached subtrees
(symbolic update-lemma foundation); zig-state rule for need>=3
zig-only remainders.


======================================================================
RECOVERY CHARACTERIZATION ROUND (the next question, answered)
======================================================================

## Y-A. Remainder-uniformity: second double => recovery 100%

n=5: 56/56 (needs<=2 observed); n=6 fresh: 428/428. Single remainder
(zig only): recovery <=> zigpay >= need; zigpay = f(first config, twin,
top-outer-mass) EXACT (n5: 108 groups 0 amb/1092 ev; n6: 256 groups 0
amb/840 ev). need=w-first_pay is pre-state computable (first sizes +
twin timing from depths). need<=0 auto-pays except later-loss 5%
(48/918: later steps can lose via Db-rise). need>=3 zig-only ~89%
unpaid (zig capped). Artifact recovery_rules.json.

## Y-B. Boundary + mechanism (honest)

Verified n<=6 (needs<=2 range). DATA GAP: need>=3 WITH remaining doubles
unobserved (n=7+, PR904 territory: needs to 4). Mechanism: absorption
(x accumulates inner mass 0->3->5, later dividends + twin creation at
end) + zig root-region dividend. Twin-timing from depths (root-touch <=>
dB<=2 or zig). No universal claim beyond evidence range.



## T-I/J/K. Shape, recursion, refinement, missing info, next object

Shape: PROVABLY irrelevant to per-double pay (rigid motion => sizes
only; twin => roots only). Recursion: same coarse descriptor + different
internal A structure was never needed -- D3 already separates; no
evidence forcing recursion (stated, not claimed sufficient). Common
refinement: COLLAPSES to singletons on hard states (no coarsening benefit
here); informative aggregation is by ROLE (pivot vs hanging position),
not refinement pieces (negative result, honest). MISSING INFO (plain):
double level CLOSED (twin+sizes); access level needs size-EVOLUTION
across steps (outer-heaviness dynamics + twin timing) -- lineage bank is
the dataset. NEXT OBJECT (proposed, unbuilt): sequence-aware meter over
hanging-block size evolution (absorption profile), NOT another static
bit vector.









======================================================================
RECOVERY-MACHINE PROOF ROUND (symbolic X*, residual dynamics)
======================================================================

Conventions: B search path to x: v_0=root,...,v_m=x (m=depth), turns
t_i in {L,R}. Hanging blocks at a double (x,p,g): xL,xR (x's children),
pO (p's non-x child), gO (g's non-p child); s.=sizes. Twin t=[rA==rB].
DbDrop = D_B(pre)-D_B(post) (positive = collapse). All claims over
arbitrary finite BSTs / arbitrary attached subtrees; engine = canonical
bottom-up splay (splay_cap/PE rotations).

## M2. Symbolic path/fringe model

State at a B-double: path-turn word (t_0..t_{m-1}) + ordered hanging
block (interval,size) at every level + arbitrary internals. Fringe
above x: per level (side-of-path-child, off-path size, turn pair).
X* = (pat,L,R,U,V,tw,fringe,remdepth) extracts computably from this
model. Internal shapes never enter X* (proved irrelevant §M3).

## M3. Rigid-block motion (PROVED)

A rotation relinks only the two pivot nodes + transferred subtree root;
every other node keeps its children (hence key set AND internal shape);
depths shift only by ancestor displacement, uniform per rigid block.
Per double (two rotations): same, composed. Only x,p,g change children.
Therefore: block sizes persist as sets; internal arrangement never
affects any depth-sum; no key-specific info enters updates. (Pointer
mechanics of PE._rot_left/_rot_right + splay_cap LL/RR/LR/RL/Z cases.)

## M4. G maps (PROVED from rotation diagrams, arbitrary blocks)

Post-step x-children (L',R') with pivot masses counted:
LL: x.left kept (T1): L'=L. x.right'=p-node(p+T2+g(T3+T4)):
  R'=2+R+U+V (+2 = pivots p,g absorbed).
RR: R'=R; L'=2+L+U+V (mirror).
LR: x.left'=p(T3,T1): L'=1+U+L (+1 = p); x.right'=g(T2,T4):
  R'=1+R+V (+1 = g).
RL: x.left'=g(T4,T1): L'=1+L+V (+1 = g); x.right'=p(T2,T3):
  R'=1+R+U (+1 = p). [Earlier mirror-formula was WRONG; held-out caught
  it; hand re-derivation above is authoritative.]
Shape-independence: only sizes enter (rigid §M3). Verified 61/61 + 41/41.

## M5. Fringe shift / side-persistence (PROVED)

Rotation preserves subtree key sets: x stays in the same child-subtree
of every ancestor at/above G2 (old great-grandparent) => sides persist;
off-sizes persist (rigid blocks); turns recompute from persisted sides
(order-determined, no key values needed). Post fringe = [new0] + old[3:],
new0 = (old[2].side, old[2].off, (old[3].side,old[2].side)) with None at
top boundary; length drops d->d-2. Lookahead of exactly 2 levels (old[2],
old[3]) suffices; boundaries: d==2 -> empty fringe (x rooted); d==3 ->
length-1 None-turn. No missing case. Next U,V = new fringe[0..1].

## M6. Twin timing (PROVED)

A rooted at x throughout B-phase (A-phase splayed x; B-phase touches
only B). rB changes iff rotation at B-root: double with g=root (d==2)
or final zig (d==1); new root is always x. Else rB fixed. Hence with
rA==x: twin_post-double = 1 iff d==2 else twin_pre; twin_post-zig = 1
always; twin NEVER destroyed in B-phase (rB only ever becomes x).
d==0: no steps. DELETE has no B-phase (out of machine scope, noted).

## M7. Supply F (PROVED per orientation + zig)

Per-step depth deltas (g at depth t):
LL pivots (x:-2,p:0,g:+2) net 0; T1:-2,T2:-1,T3:+1,T4:+2:
  DbDrop = 2s1+s2-s3-2s4.
RR mirror: -2s1-s2+s3+2s4 (slots (gO,pO,xL,xR)).
LR pivots (x:-2,p:0,g:+1) net -1; T1:-1,T2:-1,T3:0,T4:+1:
  DbDrop = 1+s1+s2-s4.
RL: pivots net -1; DbDrop = 1+s1+s2-s4 with slots (xL,xR,pO,gO)
  (verified against hand derivation above, NOT by mirror).
ZigR (x=p.left, p root): x:-1,p:+1 (net 0); T1:-1,T2:0,T3:+1:
  DbDrop = s1-s3; mirror analog. Total zig supply = 2 (twin, always
  created in B-phase) + DbDrop.
Per-double twin+Db verified 346/346 engine-side; supply s_i =
DbDrop + 2*DTwin exactly. Determinism: (X_i -> s_i, X_{i+1}) computable.

## M8. Recovery-machine theorem (from §M2-M7)

For every B phase (A pre-rooted at x), with X* as defined, for every
double i: X_{i+1} = G_{pat(i)}(X_i) [§M4-M6] and r_{i+1} = r_i -
F_{pat(i)}(X_i) [§M7], with exact zig finale. Holds for arbitrary n,
arbitrary BSTs, arbitrary attached shapes. The original tree problem is
now an integer mass-flow recurrence (empirically exact: 3247 multi-occ
X4 states 0 ambiguity; 41/41 held-out incl. RL fix).

## M9-M16. Recurrence analysis: absorption, zig family, verdicts

Absorption (PROVED from rotation mechanics): x-subtree as key SET
strictly grows per double (ancestors come under x; nothing leaves);
fringe depletes (finite path). Same-direction-run telescoping template
(exact integer algebra, LL-run): fringe mass V* seen at step i with
m total steps remaining nets (m-3)|V*| (pays -2 now, +1 per later
step); strictly negative iff m<=2 (fewer than 3 steps total) -- late
fringe never amortizes. Mixed-run full induction OPEN
(orientation-transition bookkeeping = exact next step).

High-need recovery (§10) attempted via pairing/absorption: same-run
algebra supports eventual domination by absorbed mass, but late fringe
+ zig tails break uniformity (R10-29 3->6 rises). No clean two-step or
inductive closure obtained; smallest counterexample stands (R10-29).

ZIG-OUTER FAMILY (instantiated + replayed n=9: r_final=5, n=16: 12;
matches s3-2 exactly; mirror symmetric): B=[2,[1],chain(3..n)], A
rooted at 1, KEEP 1: single zig, w=0, twin +2, DbDrop=-(n-2),
r_final=n-4 -> UNBOUNDED. w=0 edges (NOT CD counterexamples): refute
twin+Db AS DUAL. Settles §14 (NO uniform bound) + §15 (r<=2a FALSE:
a=0, r=12).

Classification (§13): r_final>0 as (i) zig-outer-heavy (unbounded,
proved) or (ii) double-remainder shortfall with thin absorption
(per-fixed-n bounded by late fringe; L4-type). §16 BLOCKED on zig
family (no double demand; needs non-twinDb payment terms; shortfall
quantified as s3-s1-2 per zig).

## M17. Regression (this round): symtable 346/346 (LL85 RR70 LR63 RL66
Z62; recharge LL51 RR43 LR18 RL16 Z19); hnadvers 41/41 held-out (RL
fix included); hnseq X-collisions; bank 650 doubles. Artifacts:
rotdist6.json, interval6.json, recur_battery.json, refine_motion.json,
transport_bank.json, hnseqs.pkl, hnadversarial.json.

======================================================================
MACHINE-SOLUTION ROUND (exact R algebra + verdicts)
======================================================================

Conventions: R(X) = remaining-B-doubles demand minus DbDrop supply
(twin EXCLUDED; handled separately as exact +2 at creation). For edge
with suffix doubles: R(X) = 1 - DbDrop(X) + R(X'). Terminal no-zig:
R = 0. Terminal zig: R = -DbDrop_zig. Twin overlay: r_final =
R_entry - 2 (B-steps exist; twin 0->1 exactly once) else 0.
Verified end-to-end (scripts/wp6_machinecheck.py): L4c -4, PR904 -8,
V19 -8, R10-29 +8, R11-9 -10, zig n=9/16 +7/+14 -- ALL MATCH.

## S2-S3. Absorption identity (from G maps, all orientations)

S=L+R: LL: L+(2+R+U+V) = S+2+U+V. RR: (2+L+U+V)+R. LR: (1+U+L)+(1+R+V).
RL: (1+L+V)+(1+R+U). UNIVERSAL FORM: S' = S+2+U+V in all four cases
(proved by substitution; no new argument needed). x-subtree as SET
grows strictly per double (ancestors come under x). Fringe depletes.
Interpretation: bookkeeping identity only (not a potential).

## S4-S5. Backward coefficient maps (derived by substitution)

R = c + aL L + aR R + sum_j f_j m_j (m_0=U, m_1=V, m_j fringe masses):
T_LL: (aL-2,aR-1,[1+aR,2+aR,f0,f1,..],c+1+2aR).
T_RR: (aL-1,aR-2,[1+aL,2+aL,f0,f1,..],c+1+2aL).
T_LR: (aL-1,aR-1,[aL,1+aR,f0,f1,..],c+aL+aR).
T_RL: (aL-1,aR-1,[aR,1+aL,f0,f1,..],c+aL+aR).
LR/RL asymmetry (aL vs aR injection order) mirrors the verified G
asymmetry. f-vector shifts outward +2/step (length grows with depth);
(aL,aR) decrement per step. Reachable set: INFINITE but STRUCTURED
(deterministic fold over turn suffix from terminal (0,0,[],0) or zig
(-1,0,[+1],0)/(0,-1,[+1],0)); not finite, not periodic in general;
closed form = the fold itself (recursive evaluator over the word, O(q)
tiny ints, no tree simulation).

## S6-S8. Families from one formula (all verified above)

L4c R=-4; R10-29 R=+8 (rise reproduced); PR904/V19 R=-8; zig-outer
R=m_0-xL=n-2 (twin overlay gives r=n-4). Zig coefficient (+1 on top
fringe) marches outward under T (f_j -> f_{j+2}), never cancelled --
only dominated when inner (negative aL/aR) mass wins (absorption).
Suffixes exposing it: top-heavy fringe at zig time; neutralized by
same-direction absorption runs (inner growth outpaces).

## S9-S13. Whole-access formula, null transport, A-phase

R_entry = fold over reversed suffix from terminal (explicit recursive
H over turn word + fringe masses + twin case; arbitrary n; derived).
Null-transport verdict: zig-outer R is GENUINE demand (fringe REALLY
descends; nothing lifts it back; twin+Db can't pay; w=0 so no CD
impact, but any dual must cover it). Not null, not telescoping.
A-phase: B frozen so Db terms frozen; twin only (±2). A pairs via twin
alone (bounded); fringe terms (unbounded) have no A-counterpart in
twin+Db. No K boundary emerges (fringe demand is real).

## S13'. EXACT ACCESS IDENTITY (derived, twin+Db accounting)

drop_total = 2(1-t_pre) + q - R_entry (t_mid cancels exactly).
Hence w <= droptotal IFF R_entry <= 2a + 2(1-t_pre).
Surplus = 2a [A-budget] + 2(1-t_pre) [twin-budget 0/2] - R_entry
[B-fringe demand, exact formula above].
DELETE proved universally (a=0: twin fixed, drop 0; a>=1: drop
2DT>=-2>=-2a). KEEP reduces to the displayed R-inequality.
Zig family violates it (n-2 <= 2 iff n<=4). Telescope: none (no K).
M (remaining theorem): construct recharge-free fringe-mass payment
terms covering shortfall max(0, R-2a-2(1-t_pre)) -- i.e., universal-dual
synthesis with exact specification (out of twin+Db scope).

======================================================================
COMPILATION ROUND (deficit profile -> transport law verdicts)
======================================================================

## P-A. R_T static fold + D_s (scripts/wp6_staticR.py; 0/300 mismatches)

R_T(x) = backward coefficient fold over reversed double word from
terminal (zero even-depth; zig-form with key-order side odd-depth),
evaluated on X_0 fringe; no tree simulation. D_s(x) = R_B(x) -
2a_A(x) - 2(1-t(s)). KEEP equivalence (D_s(x)<=0 iff twin+Db pays)
holds by the banked §13 identity (surplus = 2a+2(1-t)-R).

## P-B/C/D/E. Transport census: ALL deficit-mass aggregations REFUTED

n=5 exhaustive (8820 acc): K_+ dpos 518/518 but uniform 8542/278 FAIL
(K_+ spikes on d<=0); K_max uniform fails; majorization 0/518 dpos.
n=6 (104544 acc): K_+ dpos 6434/536 FAIL, uniform 7244 fail;
K_max/K_sum fail; majorization 888/6970 FAIL; ledger appear 520 +
grow 116 (n=5 pure-disappear was small-n artifact).
Smallest dpos failure (9,83,1) n=6: Ds=[1,-3,-7,-5,-8,0] ->
Dp=[0,-2,-7,-5,-7,+2]: accessed +1 destroyed, key 6 APPEARS at +2
(moved AND amplified 1->2). Twin terms bounded (+-2) cannot cover
spikes (plus excess to 7, sum to 45, max to 11).

## P-F/G/H. Lambda exact + K_1/K_abs REFUTED (scripts/wp6_lambda.py)

R_T(x) = c + sum_y lambda(x,y) via fringe-block key sums (verified vs
fold values). K_1: 8320/500 FAIL n=5; K_abs: 8592/228 FAIL. Worst k1:
(21,19,1) d=0 with K_1 rise +8 (coefficient reshuffle on no-demand
access); worst kabs: (19,21,1) d=3 short 9. K_1/K_abs spike on
reshuffling without demand: raw coefficient movement is not demand.
Transfer law found: mass/coefficients MOVE and AMPLIFY (1 destroyed,
2 created); no conservation, no bounded ratio established.

## P-I/J. No M; A-budget rewritten, unpaired

M: NONE (six aggregations dead: K_+,K_sum,K_max,majorization,K_1,K_abs).
A-budget exact: 2ceil(d/2) = d + (d mod 2) (per-ancestor unit + parity
unit) -- verified algebraically. Pairing B-fringe coefficients to
A-ancestor units: OPEN (no valid ownership assigned; joint
fringe-comparison proposed UNTESTED as next object, not claimed).
DELETE for M: OPEN (no M). KEEP: OPEN.

## P-K/L. No telescope (no M). DO chain preserved unchecked

C.ZIG (Z_B<=A), B<=3A, E_B<=3S_A+g, LT 7x+2g, Levy-Tarjan hypotheses,
final DO: all preserved exactly as banked, no new claims (M open).
Max-mean-D = 0 n=5 (Karp exact): NO positive-D closed walk, so the
profile approach is NOT cycle-ruled-out; aggregations fail on EDGE
creation, a strictly harder obstruction.

======================================================================
CANONICAL INTEGRATOR ROUND (V exact + tight anatomy)
======================================================================

## V-A. Graph: n=5 (1764 states, 17640 trans) + n=6 (17424 states,
209088 trans), KEEP (D=R_B-2a-2(1-t), int) + DELETE (D^DEL=-2a-2dt'
PROVED <=0 everywhere: a=0 forces dt=0; else -2a-2dt<=0; base covers
all DELETEs, but they still constrain V). Karp (dmaxmean5) + Howard
max-mean 0/1 BOTH sizes (no positive-D cycle). Scripts
wp6_vintegrator.py (Howard/Fractions + bias shift), wp6_dmaxmean.py.

## V-B/C. V = longest-path (0-init) = Howard-bias minus min (proved:
V=h-min(h) satisfies sigma>=0 + fixed point + least-nonneg; all
verified exactly). n=5: V in {0..3}, 1206 zeros; sigma 0/17640,
fixed-point 0/1764. n=6: V in {0..5}, 8684 zeros; sigma 0/209088,
fixed-point 0/17424. Artifacts vfull5/6.json.

## V-D. Tight graphs ACYCLIC (all-singleton SCCs) both sizes; every
state has >=1 tight successor. n5: 4102 tight (488+/264-/3350z).
n6: 44968 (5734+/8582-/30652z). Unique/multi: 672/1092 (n5),
4934/12490 (n6).

## V-E/F. Trajectories + (9,83,1) decoded (u=1271 V=3, Ds listed,
v=1204 V=2, D=+1 tight; succs: self-loops D=0, (13829,K,6,+2)->V=0,
(13744,D,6,0); continuation 1+2=3=V(s); amplified key 6 selected by
tight K6 YES). Chain lengths: n5 all 1 (488 direct to V=0); n6
1/2/3/4 = 4350/1055/284/45. V-nonmonotone travel exists (1->5 via
D=-4 tight). Lambda rows pre/post recorded for (9,83,1).

## V-G. Collisions S0-S3 (n=5): ZERO ambiguity all levels (960/960/
960/981 classes). V-vs-maxdeficit: 1682/1764 match; 82 gateway states
(V>maxdef) are 93% non-twin + 100% non-vine-B. n=6 ladder deferred.

## V-H. Propagation (n6 5734 tight-pos edges): 99.5% deterministic
(14 amb / 2966 classes); post-counts 0/1/2 = 4858/856/20; direction
ALL strictly UP (Bpost-ancestors of x, depths 1/2/3 = 280/132/484;
x itself always D'=0 post-access); Lambda overlap 91%. Merge observed
(2 keys); split-to-2 rare (20).

## V-J/K. Units: Mmax 1682 match but 86 Bellman fails (worst
(-2,-1,19,16,3)); MpathB identical fails; Mdep 360 fails. Failure =
edge-integration (same edges), not just values. Gateway-conditioned
max-deficit untested (candidate, not claim).

## V-I. Zero-D tight SCCs trivial (singletons); zero-D tight edges move
B-shapes/roots (81/279) + twin flips (67) freely, A rarely (17): V
ignores B-root motion + twin flips at zero demand.

## V-L/M. NO M emerges (closest: max-deficit, refuted 86; gateway flag
untested). Missing relation: structural payer of the 82 gateway
lookahead demands + what covers post-creation spikes (mass move+amplify
+ coefficient reshuffle on d<=0). No universal verdict manufactured.

======================================================================
BELLMAN-CLOSURE ROUND (profile sufficiency + horizons)
======================================================================

## W-A. Tight-graph correction: DAG + D=0 self-loops ONLY

Self-loops all D=0 (n5: 458K+1764D; n6: 4120K+17424D; DELETE-at-A-root
always self-loop+tight). Zero nontrivial SCCs both sizes. Corrected:
acyclic after deleting self-loops; every state has >=1 tight successor
(min outdegree 1); maximal tight paths end in self-loops.

## W-B/C/D. Profile->V: clean n=5 (960 classes, 0 amb), 328 ambiguous
n=6 (8895 classes, 5403 multi). (P,twin): 296 amb. (P,twin,Broot): 250
amb. Smallest: P=(0,-3,-5,-7,-4,-6), (0,33)V=0 vs (47,115)V=1 (twin
differs). Smallest same-twin: (0,56)V=1 vs (0,75)V=2, same A/D/twin:
Lambda_B rows differ while R_B VALUES agree everywhere (key1: c=0/n4
vs c=1/n2). FIRST DATUM: (c,lambda-support) decomposition of
positive-D rows, not R values. Constant-vs-support split open.

## W-E/F/G/H. Horizons h_5=2 ({0:1206,1:476,2:82}), h_6=5
({0:8684,1:4348,2:2962,3:1236,4:190,5:4}); V_k-limit == canonical V
(0 mismatches both). Gateway 82 (n5) / 4392 (n6). C-vectors n=5: only
3 patterns ((0,1,0)x72, (1,1,0)x2, (0,2,0)x8): ALL gateway value from
C_2 (one-step lookahead); C_3+ never contributes. D-words: 3 (n5),
37 (n6) distinct tight residual words.

## W-I/J. Profile transitions: (P,x)->P' ambiguous 1254 (n5);
value-det also fails (210 amb). Smallest: P=(0,-5,-5,-6,-4),x=3 ->
(3,-1,0,-1,3) vs (3,-1,0,0,0) (keys 4,5 differ). Ideal profile machine
DEAD (both forms). Classification: n=5 outcome B (profile fixes V,
not transitions); n=6 outcome C (profile does not fix V).

## W-K/L/M. No M (max-deficit closest, refuted; gateway-flag untested).
Missing: payer of gateway lookahead (82-pattern: non-twin/non-vine-B
futures) + post-creation spike cover (move+amplify/reshape on d<=0).
Next object: Lambda-row (c,support) structure, NOT values.

======================================================================
A-CARRIER ISOLATION ROUND (location first)
======================================================================

## C-A/B/C. Gateway-event dataset (carrier5.json 31K C>0 events n=5;
carrier6 sample 35K) with B-tracer + A-transport partition + support
mapping + y-location. Dpost>0 genuine subset: 5.6K/31K (rest are
twin-driven bumps staying non-positive).

## C-D/E/F/G/H. Elimination table (counterfactual collisions):

H1 path/pivots: NECESSARY (path fixes hangs/sizes/attachments;
determinism sketch; twin needs roots).
H2/H3 mass/position: MOOT-SUBSUMED (zero independent variation:
hanging intervals+sizes+attachments are path-determined at n=5;
neither necessary nor eliminable separately).
H4 y-relation: UNRESOLVED (confounded with path; y indexes the question).
H5 support->blocks: UNRESOLVED (correlates; 341 ambiguous with it;
necessity untested cleanly).
H6 boundaries/LCA: UNRESOLVED (tracked, never isolated).
H7 internal shapes: NECESSARY-SOMETIMES (268 groups vary C; mechanism
= per-key A-depths via C_A; adversarial mirror pair below).
H8 remote: ELIMINATED (empty set: path+hangings partition all keys).
H9 global: UNRESOLVED residual.
Support-pre-placement alone: 341 ambiguous (needs post/crossing info).

## C-I/J. Adversarial exhibits: (1) H7 mirror pair (ia=19 vs 20, same
B/x/y/path/hangs, mirrored 2-chain: C=5 vs 3; tracked: dA(4) 1->2 vs
2->3, twin 0->1 both, CB identical, CA differs by exactly 2). (2) Twin
pair RR (same geometry, twin 0v+2, pay -1v+1). (3) Spine-bit separation
noted. Carrier tracking on (1): y=4 depth trajectory + twin flip
recorded; mirror block rides rigidly (depths shift uniformly).

## C-K/L/M. Minimal family H* = full path-neighborhood (path, pivots,
hang intervals/sizes/attachments, shapes-as-depths) + y-relation +
support placement + twin/roots + FULL B-side. Only H8 eliminated.
Transport law: component-exact (DbDrop formula, twin timing, depth
shifts); NO compressed C_before->C_after law (needs full state).
M: none (D<=M-drop open). Next theorem: single-crossing payer rule
for H4/H5/H6, or proof none exists below full state.


======================================================================
GATEWAY-CREATION KERNEL ROUND (exact answers)
======================================================================

## Y-A/B. V=V2: HOLDS n=5 (82/82 gateways), FAILS n=6 (1430/4392
mismatches). Finite theorem at n=5 only. Smallest n=6 mismatch u=18
(V=1,V2=0): A=vine, B=[1,[3,[2],[6,[5,[4]]]]], D=[0,-2,-5,-5,-5,-6];
tight K1(D=0)->V=1, K2(D=-2)->V=3 (V RISES along tight edge; value
funded by path via V=3 then discharge). Extra horizon required: 2.

## Y-C/D. Identity C=CB+CA+Ctwin EXACT on 671,364 KEEP transitions
(n=5+n=6), 0 mismatches. Positive-C drivers: twin creation (+2 to all
coords) dominates jointly (B+T 187K biggest bucket); A-only rare (6.8K).

## Y-E/F/G/H. Smallest collision pair fully decoded ((0,56)V=1 vs
(0,75)V=2: same A/D/twin/R-values; Lambda key-1 rows (c=0/n4 vs c=1/n2);
successors differ (Vpost 0 vs 1); post key-1 rows BOTH discharged --
demand lives in other rows' migrating fringe mass). Exposure E with
masses+deltas: 238 classes, 43 ambiguous (vs 21/21 without). Residual
ambiguity = fresh post-coefficients (case (0,0,x4)y=1: pre row EMPTY,
post gains +1 on key 5 (CB=1) vs +1 on {3,4,5} (CB=3)). Affected
region Q = path/fringe blocks (rigid motion); post-coefficient creation
is the irreducible remainder.

## Y-I/J/K. 328-class chain: 328 -> +twin 296 -> +Broot 250 ->
+argmax-row 237 -> +full-B-rows 114 -> +A-depths 0-VACUOUS (all
singletons). No compact sufficient Z (diminishing + specificity
explosion). Transition sufficiency fails at profile level already
(1254 amb; value-det 210 amb). C* one-step formula REFUTED at n=6
(V!=V2 there); valid n=5 only.

## Y-L/M/N. No M; no static C* (needs post-coefficient prediction =
trees). Next theorem: coefficient-transport rule for Lambda rows
(post-creation from pre-state exposure), then gateway payer.





======================================================================
SINGLE-CROSSING ROUND: REFUTED (exact smallest witness)
======================================================================

## X-A/B. Cut system: X_i nested VERIFIED on all events (subtree
deletion monotonicity). Sep_A interval property holds by nesting.
Gamma vectors + Delta sign-split per cut. Scripts wp6_cutcarrier.py.

## X-C/D/E/F. |CAND|: d0 4798 (no cuts exist: structural vacuity) +
delta-empty 6246 (no B-support: A/twin channels) + no-relevance 1398
(colocated support, vacuous) + NO-CONTACT 110 + MIXED 1332. In-scope
(delta-nonempty, d>=1, must-cross): 1442 without qualifying cut.
Contact fix (attachment-aware) rescued 1510; remainder stands.

## X-G/H/I/J/K. SMALLEST WITNESS (18,12,5,1), d=1, single support key:
A=[2,[1],[5,[4,[3]]]], B=[1,_,[5,[4,[2,[3]]],_]], x=5, y=2. C=+1
(Dpre=-5, Dpost=-4); B-coeff -2->-1 on key 3 STATIC in A (depth 3,
parent 4 unchanged); twin 0->1 (+2); A-cost -2. Single cut e_1:
rel T, act T, con F, nonvac T. No A-cut sees static-key creation.
Supporting: (9,0,5,1) (support {3,4} static, twin kept, A opposes -2).
Artifact singlexing_refute.json. R1-R4/I_common/L_i MOOT post-refute
(not executed: verdict forced at §7/§17.1-.3). B-only detail cannot
see A-static creation either (same wall, noted).

## X-L/M/N. VERDICT: SINGLE-CROSSING REFUTED. Minimum richer carrier
forced: B-coefficient creation visible on A-static regions (cut +
static-region B-coefficient claims, or full B-row with A-placement).
NOT launched (spec §17). Twin channel: bounded +-2, present in 96%
of creations, insufficient alone (spikes need B-terms); Delta_c travels
with support (no independent channel). D=-2 V:1->3 witness
(14,17,3)->904 recorded: any M must allow +2 rises (consistent with
A-step recharge bounds). No M; no telescope; DO chain preserved.

======================================================================
A-STATIC GATEWAY CARRIER ROUND (STATIC-A: latent B transport proved)
======================================================================

## S-A. A-static definition + C_A=0 (scripts/wp6_astatic.py)

Event (x,y) A-static iff across A->A': depth/parent/LCA/ancestor-relations
unchanged for y AND every z with Delta_lambda(y,z)!=0 (full §2 list;
hanging-identity interpreted as key-interval/attachment relation).
C_A=-2[ceil(dA'/2)-ceil(dA/2)]=0 follows from frozen depths (verified per
event; 0 violations). Redundancy NOT claimed (all checks enforced).

## S-B. Counts: 5214/31234 (16.7%) A-static, n=5; C in 1..8
(704/1834/876/918/650/160/64/8). Artifacts astatic5.json/staticB.json.

## S-C. Witness (18,12,5,1) decoded (NOT A-static: y depth 0->1, CA=-2)

A=[2,[1],[5,[4,[3]]]], B=[1,_,[5,[4,[2,[3]]],_]], x=5, y=2.
B path(x)=[1,5]; y-path [1,5,4,2]->[5,1,4,2]. Lambda_y: (-1,{3:-2}) ->
(-1,{3:-1}); Delta_c=0; C_B=+1; C_A=-2; C_twin=+2; net +1. B object
changed: y-fringe slot of key 3 (F_0, coeff -2->-1) as x's RL double
rebalances y's fringe. Smallest TRUE A-static witness: (0,19,1,4):
A vine fixed (x=1 root, Ap=A), y=4 depth 3 static, B zig 3->[1,[3..]];
Lambda (0,{5:-1,1:1,2:1})->(1,{5:-2,2:1}); C_B=-1, C_A=0, C_twin=+2,
net +1 (twin-driven creation).

## S-D/E. B partition: path pivots/hanging/unchanged/root-twin regions
with (interval,size,attachment,side,depths pre/post) per block (rigid
motion). y-support slots from proved fold: L/R/F_j/SELF/NONE; Slot_B
defined by key-membership in y's L/R/fringe sets (no guessing).

## S-F. T-classes (per-z over 5214 events): T1 1974, T2 644, T3 3876,
T4 3014; event-level T5-merge 1402, T6-split 1804. No impossible
category (all occur).

## S-G/H/I. Fresh (T3) 3876/3876 have pre-state latent block source
(100%: every fresh z sits in a pre-existing P_B(x) hanging block or
pivot; rigid motion preserves key sets). Latent claim L_B(y) =
(H, dest-slot, future coeff, activation-on-x) from current B + fold
geometry (no post lookup). Transport: ClaimSet_y(B)->ClaimSet_y(B')
via P_B(x)/P_B(y) overlap + hanging transport + fringe shift +
orientation (operator implemented in analysis; full-claim determinism
0 amb over 1008 pre-row classes). G-split: G1 838, G2 2056, G3 1720,
G4 600, G5 0 (G1-G4 exhaustive, no G5 needed).

## S-J/K. Exhaustive Delta prediction: full pre-row -> Delta vector
0 ambiguity (1008 classes). Coarse (slot,G) alone 17/21 ambiguous
(minimal key (F1,G4): -2 vs -1) -- fringe detail required, included
in latent claims. Delta_c dist (-2:28,-1:800,0:2984,1:1332,2:70)
travels with support (zero-lambda-rows: dc!=0 cases exist but track
root/twin/support events, no independent channel).

## S-L. Twin: 0->1 in 5186/5214 (99.5%), kept 28; synchronized root
arrival (twin flips exactly when B roots x: d==1 zig or d==2 double
per proved timing). Twin = independent bounded (+2) root charge
(board-wide, y-independent) PLUS coincides with fringe activation;
resolved as (A)-plus-(C) combination: bounded charge, not a substitute
for claim transport (spikes need B-terms).

## S-M/N. StaticClaims = latent/current B coefficient claims with
A-static relation; M_static naive pos-lambda-mass covers C_B only
2280/5214 (43.7%, worst -18 vs +6) -- summation needs multiplicity
(merges/splits), NOT forced. Static residual inequality therefore
OPEN as integrator; transport law itself exact.

## S-O. Negative-edge recharge EXISTS in static subsystem: 6972
static-y D<0 edges with V-rise, e.g. (0,0,3,2) D=-5 V:0->3 (dormant
claim activation funded by slack). Mandatory witness class recorded.

## S-P/Q. VERDICT: STATIC-A (no killer among §17.1-5: fresh 100%
sourced; full-claim determinism 0 amb; no shape-only counterexample
under frozen depths; splits representable per-z; Delta_c tracked).
REMAINING THEOREM (§19): weighted/multiplicity-correct M_static
integrator + coupling to moving-A carrier; then base accounting gives
w<=Phi-Phi' and Q_B<=2A. DO chain preserved, untouched.

======================================================================
ROOT-SELECTED ROUND: GATE I PROVED (kappa_*=4); GATE II FINITE-GREEN
======================================================================

## R-A/B. Authoritative residuals (verified, signs frozen)

D_KEEP=R_B(x)-2a_A(x)-2(1-t_pre), a=ceil(d_A/2), t=[rA==rB].
D_DELETE=-2a_A(x)-2(t_post-t_pre). Both replay-verified (sample +
exhaustive identity below). D0_y(B)=R_B(y)-2(1-b_y), b_y=[rB==y].
D_KEEP(A,B,y)=D0_y(B) when y=root(A) (a=0, t=b_y; exact).

## R-C. da=0 = pointed-B (proved)

y=root(A) => Splay_y(A)=A (root splay no-op). KEEP becomes
(A,B)->(A,Splay_y(B)). All da=0 A-static rows have x=y=A-root
(verified: 1764/1764 n=5). Domain: finite BST + distinguished key,
order-equivariant, no A-state. G1-only transport (x=y in-fiber).

## R-D/E. Finite cone: one-dimensional, stable

da=0 fiber LP (twin-blind root): unique optimum (tilt distance 0.0)
at n=5 AND n=6. Sign patterns agree on all shown common types
(+-1 box vertices identical). Scale grows with rows (10K->130K).
Truncation-of-one-rule supported; full-vector audit open (minor).

## R-F/G/H. G1 recurrence + compact g* + admissibility

Absorbed-mass gauge: g*=1[z outside y-subtree]; G_y(B)=n-|sub_B(y)|.
Monotone: y-subtree grows monotonically as SET under Splay_y (rigid
absorption; pivots net in) so claims only exit (1->0), never enter.
Transport-effective (strict on absorbing rows). Total, explicit,
order-equivariant, A-independent. (Supersedes LP vertex table.)

## R-I/J/K/L/M. H_y + row theorem + kappa_*=4 (PROVED universal)

H_y(B)=-R_B(y)+4*G_y(B), C_n=0. R_{Splay_y(B)}(y)=0 (y root => d=q=0).
DA0-ROW reduces to 4*absorbed >= 2R-2(1-b), i.e. R<=2*abs+(1-b).
LEMMA (universal, proved by fold induction): fold outputs satisfy
aL,aR<=0, f_j<=2, c<=q (#doubles); absorbed=fringe+d; chain gives
R<=q/2... precisely R<=d/2+2*fringe<=2*abs+(1-b). Absorbed=0 => y root
=> R=D0=drop=0. Hence kappa_*=4 sufficient (necessary >3.33 by
witness; sharp value in (3.33,4] open-minor). No per-key offsets.

## R-N. DA0-ROW THEOREM: PROVED (universal, mathematical)

Regression: 0 violations on 1764+17424 da=0 rows (n=5,6), tight
458/4120 (self-loops). Mechanization OPEN (Lean tree-model gap).

## R-O/P/Q. M + decomposition + row-switch target

M(A,B)=H_{root(A)}(B). KEEP: M-M'=[H_x(B)-H_x(B')]+[H_r(B)-H_x(B)]
(transport+switch; root(A')=x used). D_KEEP=D0_x+D_DELETE verified
0/8820 (mandatory identity HOLDS). D_DEL=-2a-2(b_x-b_r)<=0 always
(a=0=>x=r; else -2a+2<=0; proved). ROW-SWITCH:
H_r-H_x>=-2a+2(b_r-b_x) (upper form bounds H_x growth by A-budget).

## R-R/S/T. Finite row-switch: absorbed-H REFUTED, joint ALIVE

Absorbed-H (kappa=4): 3338/8820 fail n=5; witness class fails for ALL
kappa>=0 (LHS decreasing in kappa via G(r)-G(x)<0; fails already at
kappa=0). Pair graph strongly connected from diagonal (1764/1764) so
RS2 moot (failures reachable). JOINT fiber cone (DA0+RS, B-types +
c-root): FEASIBLE with strict drops (58K n=5; 893K n=6). Verdict:
SCALE (fix gauge via joint cone, not architecture). Kappa-interval
for absorbed family EMPTY; joint cone is full-dimensional object
(dimension analysis open-minor).

## R-U/V/W/X/Y. Universal row-switch OPEN (A-path proof not attempted);
KEEP/DELETE/residual theorems CONDITIONAL on universal joint gauge
(implications proved, premise open). No full residual integrator yet.

## R-Z/AA/AB. Coarse-Double OPEN (conditional chain recorded, not
closed). Math: Gate I closed, Gate II finite-green/universal-open.
Mechanization open (tree-model gap; no Lean this round). Remaining
theorem: universal joint-gauge admissibility (all-n A-root rows +
fringe induction for B-deep splays) + A-path row-switch proof.


======================================================================
GAUGE-RIGIDITY ROUND (finite R1 proved; fiber R2-direction found)
======================================================================

## G-A. Gauge reduction (exact, symbolic)

h(tau)=C-lambda(tau)+g(tau): atom req lambda'-lambda<=h-h' IFF
g(tau)>=g(tau') (ATOMIC GAUGE EQUATION; verified identity
hdrop==qsum+gdrop 0/300). Root: q_root=Delta_c (from r=C_B with
q_z=Delta_z), b(rho)=c_B(y), h_root=C_root-c+g_root reduces cleanly
to g_root>=g_root'. Twin NEVER destroyed under KEEP (both roots->x,
proved from splay rooting); DELETE destruction rows exist (356
A-static at n=5, e.g. (7,0,4,3)) and pin twin gauge.

## G-B/C/D. Root/twin + Tau + coordinates

Root token rho=(c,twin); KEEP twin only 0->1/1->1 (never destroyed);
DELETE adds destruction (1->0) + creation. Delta_c in -2..2 travels
with support (no independent channel). Tau=(slot,lambda) coarse;
refined +(fringe-idx, turn-pair, ancestor-distance). Normal form.
NECESSARY: slot (transport), lambda (payment unit), fringe-idx/turns
(shift dynamics). DERIVED: lambda from fold; latent-dest from
geometry. REDUNDANT: block masses (per-key coefficients
mass-independent; rows sum over keys), y-depth beyond turns.

## G-E/F/G. G1-G4 families + padding + completeness

G1 x=y; G2 y on P(x); G3 x on P(y); G4 shared-prefix-diverge (staticB
counts 838/2056/1720/600; G5 provably empty by tree path combinatorics
+ 0 events). Padding lemma: finite local geometry embeds at arbitrary
n (extra mass parked off both paths, turns preserved) so all 102
observed coarse edges + 17 forced edges are universal. Completeness:
G1-G4 exhaust all path relations (proved).

## G-H. ISOLATION REFUTED (aggregate necessary)

Single-change rows 5208/44100 cover only 27/102 edge types;
+root-fixed only 17 (4 forced SCCs); swap-augmentation adds 0
(17/102); 85 types uncovered. Vine parametric search: 0 fringe-shift
isolations in tested configs. Universal parametric isolation not
found. Aggregate DeltaN_e formulation authoritative:
<g,DeltaN_e>+Delta g_root(e)>=0 per universal row.

## G-I/J/K/L. SCCs + condensation + gauge family

Observed type graph single SCC (16 nodes); forced subgraph 4 SCCs
({F0,0/F1,1/F1,0/F2,1},{R0/L0/NONE0/F1,2},{L-2/L-1},{R-1/R-2}).
Hub (NONE,0): every claim reaches it in ONE step (splay z, A z-rooted;
verified 0/256 bad n=5..7) and it reaches 10 types directly; NONE=>lambda
0 structurally (ancestors never in fold support; verified 0 violations).
Condensation DAG on forced blocks (order, not equality, between blocks).
Finite gauge family: ONLY zero-drop gauges (LP-max=0; see below).

## G-M/N/O. Finite R1 THEOREM (LP + circulation)

n=5 AND n=6, coarse AND refined (49 vars), KEEP+DELETE (19K/235K rows):
max total gauge drop = 0 EXACTLY (all four probes). Positive
circulation y>0 with y^TA=0 EXISTS (dual certificate, status 0) so all
finite drops vanish structurally. Twin harvest dies via DELETE
destruction (KEEP-only max was 13983). No transport-effective B-only
(+root) gauge at n<=6. Row-config mutuality 46.7% (partial reversibility);
pair-level 26%; deep rows unbalanced (no Eulerian rescue: 25344 vs 0).

## G-P/Q/R. Fiber analysis (the frontier moves)

Fiber (da_y) gauges: da=0 harvests (9760 n=5; 130904 n=6; twin-blind
10384/130904 genuine B-drops); da=1,2 were twin artifacts (die
twin-blind); da=3 rigid always (0 at n=5 AND n=6 with 56K rows);
da=4 died n=5->n=6 (under-constraint artifact); da=5 modest (needs n=7+).
da=0 fiber PROVED = x=y=A-root rows (A-noop full B-splays; n-independent
family). da=0 gauge atomwise-valid (0 violations), strict drops
(mean +6.3 over CB, only 26% tight) -- genuine R2-shaped direction,
NOT tautology. Universal fiber verification OPEN.

## G-S/T/U. Fringe: hub-1 universal PROVED; index-shift isolations exist
at low indices (forced SCC spans F0/F1/F2); parametric deep-index
locking OPEN. lambda<=2 universal (fold induction) so tautology
normalizes C=2 globally. Regression green (reduction 0/300, hub 0/256,
identities 0 mismatches).

## G-V/W/X/Y/Z. Recharge (0,0,3,2) via dormant activation within slack
(tautological part; no independent reservoir needed). VERDICT R4:
finite R1 PROVED (B-only+root, n<=6) but universal classification OPEN;
missing relation = universal da=0-fiber admissibility (all-n A-root rows)
+ compaction to explicit g* + row theorem. R2 needs that program; R3
premise fails (atomwise HOLDS on fiber gauge: 0 violations); R1 false
once fiber allowed (finite fiber gauge transport-effective). Minimum
surviving structure: y=A-root-fiber-sensitive (deep-B) or cross-row
coupling; finite-depth-blind B-only objects all dead. Next theorem:
da=0-fiber row payment theorem at arbitrary n.


======================================================================
ATOMIC INTEGRATOR ROUND (weight solved: exactly the tautology)
======================================================================

## W-A. r_static frozen: access-level D_s(x); row-level C_B(x,y)

C=C_B+C_A+C_twin verified 0 mism/5214 (C_A=0 by A-static filter);
C_B=Delta_c+sumDelta_lambda verified 0 mism. Row target r=C_B;
root covers Delta_c, atoms cover sumDelta. Scripts wp6_atomic.py,
wp6_atomic2.py, wp6_hsolve.py, wp6_hdump.py.

## W-B/C/D. Claim(y,z) persistent (keys persist; dormant=lambda 0
included). tau=(slot,lambda) minimal (slot L/R/F_j/NONE/SELF from
proved fold membership; fringe index/orientation/block-size tested as
refinements). ell(tau)=lambda by construction, verified 0 bad/20856
atoms. G1-G4 transport context (G5 0).

## W-E/F/G. Transport: full-claim 0 amb (1008 classes); coarse
(slot,lambda,G) 37 amb/58 (fringe detail required, banked). Per-(y,z)
single deterministic successor (splay deterministic; no branching
ever). Merge/split RESOLVED as slot-level artifacts (T5 1402/T6 1804
events all per-z exact). Root token rho=(c,twin): 16 pre-states,
9 amb coarse; Delta_c in -2..2 travels with support; twin 0->1 99.5%
synchronized root arrival (bounded +2 charge, spikes need B).

## W-H/I/J. Decomposition r=q_root+sum q_z with q_z=Delta_z EXACT
(0 mism). Single-atom Bellman (longest paths, §13 procedure): 16
nodes/109 edges, converged 1 iter, 0 residual, h in {0..5}, row
coverage 5214/5214. BUT h(slot,lambda)=2-lambda EXACTLY
(slot-independent; per-lambda singletons {-3:5,-2:4,-1:3,0:2,1:1,2:0}).
This is §9's FORBIDDEN TAUTOLOGY (H_y=const-R_B(y); integrates by
definition). NO non-tautological margin is forced (Bellman least
solution collapses; extra weight would be arbitrary choice).
Recharge witness (0,0,3,2) decoded: z=1 (NONE,0)->(L,-1) weight 2->3
(gain funded by slack); z=3,4,5 discharge exactly; all tautological.

## W-K/L/M/N. Exhaustive: tautological cover 100%; naive
pos-lambda-mass 43.7% (prior). §17: NO coverage witness exists
(tautology covers all) -- obstruction is VACUITY not coverage; no
bundle forced (atoms already exact; bundles inherit tautology).
Classification: COHOMOLOGY (no ADMISSIBLE non-tautological weight;
transport deterministic, decomposition exact). Universal: n=5 types
finite; fringe-indexed h_k recurrence OPEN (tautology extends
trivially, doesn't count). Aggregation (§21) OPEN. Remaining theorem:
genuine (non-tautological) dormant-margin reservoir or proof none
exists below full fringe state.


