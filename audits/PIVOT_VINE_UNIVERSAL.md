# PIVOT-9: Universal vine-pair B<=A (all n)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Status: PROVED for n>=5
(human proof below) + FINITE base n<=5 (pair-graph integer BF, no positive
B-A cycle on vine-pair subgraphs). Overlap at n=5, no gap.

## Theorem
Every closed walk confined to vine-pair states (both BSTs chains) satisfies
B <= A, for every n. (C=1, strictly stronger than DOUBLE-FLEX on this region.)

Costs: a = ceil(dA/2), b = ceil(dB/2) per access (StepEv counts agree with
depth formulas: C181 formula-vs-replay 0 mismatches; violator/blockdist
0-mismatch checks). Splay roots the accessed key (noop iff already root);
DELETE freezes B. Splay implementation: `scripts/wp6_eventflow.py`
(`splay_A`/`splay_B_push`, grandparent-first doubles, standard `_rot_*`).

## Lemma V1 (n>=5): vine-preserving splay has depth <= 1
Contrapositive: splaying at depth >= 2 on a vine (n>=5) yields a non-vine.
Bottom-up: the first step is a double rotation on the deepest triple.
Cases on the accessed key x (code rotation order throughout):

- x non-leaf (has a tree-child; it sits on the outer side, away from the
  parent, since the child is a descendant): zigzag gives x two non-leaf
  children (p-side + g-side, both real .nodes) => branched. Same-side
  zigzig keeps x's outer child and gains the p-side (real) => x ends with
  two non-leaf children (outer kept + p gained); if x's child is inner-only,
  the middle node instead keeps g-side (real) and gains x's inner (real)
  => branched there. Kernel: `vine_LR_branch`, `vine_RL_branch`,
  `vine_LL_branch`, `vine_RR_branch` (GCStaticVine.lean, green).
- x leaf: mixed path => zigzag => branched (same kernel lemmas, no
  hypotheses needed). Straight path => zigzig-leaf mirrors locally
  (chain preserved at this step); the splay continues iff depth > 2.
  Depth exactly 2 with x leaf on a vine forces n = 3 (path has 3 nodes;
  off-path attachments would already break vine-ness): excluded for n>=4.
  Depth exactly 3 with x leaf straight forces n = 4 (4 path nodes; a 5th
  node has nowhere vine-legal to attach): excluded for n>=5.
  Depth >= 4: step 2 is a double rotation with x now carrying exactly one
  child => branches by the non-leaf case above.
Hence for n>=5, depth >= 2 always branches. The n=3 (extreme depth-2
mirror) and n=4 (extreme depth-3 zigzig+zig) exceptions are REAL and
measured (`isvine` probe: n=3 x=3 True, n=4 x=4 True, n>=5 extreme False);
they are the reason for the n>=5 threshold, handled by finite check.

Persistence (branches survive to end of splay):
(P1) x doubly-branched (two real children) stays so through every rise:
  each rise keeps one real child (far side) and gains a real parent-side
  subtree => two non-leaf children by induction; x ends as root with two
  children => final non-vine.
(P2) descendant-branch persists: rotations rebuild only the matched triple
  (SplayRotate per-region tables); a branched node strictly below the rising
  key rides rigidly as a side-subterm (its interior never rebuilt, since
  triple nodes are always the key and its ancestors) => stays branched;
  a branched subterm makes the whole tree non-vine (iterate `vine_sub_l/r`
  along its root-path).

## Classification (n>=5; vine-internal edges have depths <= 1 by V1)
Costs per edge: (a,b) in {(0,0),(1,0),(0,1),(1,1)}. Differ bit
t = [A-root != B-root] (1 = roots differ, 0 = twin). Every KEEP twin-roots
its key (both trees splayed at x); DELETE freezes B. Flip table, in
differ-bits (all claims by root-tracking only):
- (0,1): KEEP x with x A-rooted (a=0) and dB=1 (b=1; vine forces exactly 1):
  source has B-root != x = A-root (differ, t=1); post has A-root x
  (unchanged) and B-root x (zigged) => twin (t=0). Always flips 1->0,
  weight +1. From-twin impossible (would need y = A-root = B-root with
  dB(y) = 1).
- (0,0): both trees unchanged (A noop on rooted key; B frozen or B-noop)
  => self-loop, no flip, weight 0.
- (1,0): KEEP variant has y = B-root with dA(y) = 1 (source non-twin,
  lands twin: flips 1->0, weight -1). DELETE variant splays A to y
  (B frozen): lands twin iff y = B-root (flips 1->0, -1) else stays
  differ-or-enters (0->1 entry, 0->0/1->1 neutral, all -1). From-twin only
  via DELETE y != x (KEEP-(1,0) impossible by the same contradiction as
  above): always a twin->differ exit (weight -1). Unrestricted flips;
  weight -1 throughout.
- (1,1): KEEP with dA = dB = 1, lands twin always: flips 1->0 (from differ)
  or 0->0 (from twin), weight 0. Never flips 0->1.
Counting (kernel `vine_cycle_nonpos`, green; Lean bits are twin-bits, i.e.
the negation of t, under which the table reads (0,1):F->T, (1,1):never
T->F): W' = N01 - N10 with N01 <= F10 = F01 <= N10, where F10/F01 are
1->0/0->1 flip counts (bit-telescope on closed walks; every (0,1) flips
1->0; only (1,0) flips 0->1). Hence total B-A <= 0 on every vine-confined
closed walk. QED (n>=5).

## Finite base (n<=5, covers the n<=4 mirror exceptions)
Integer Bellman-Ford positive-(B-A)-cycle detection on vine-pair induced
subgraphs: n=1 (1 pair), 2 (4), 3 (16), 4 (64), 5 (256): all clean.
n=6 (1024 pairs), n=7 (4096 pairs): clean (re-confirmed). Scripts:
temp `vinebase.py`, `vine7.py`, `vinetest.py`.

## Lean kernel (green, exit 0, no sorry/admit/axioms)
`lean/WP6/GCStaticVine.lean`: `isVine` + `vine_sub_l/r`, `vine_either`;
`vine_LL_branch`, `vine_RR_branch` (child-carrying zigzig), `vine_LR_branch`,
`vine_RL_branch` (unconditional zigzag); `scan`/`endBit`/`scan_telescope`/
`scan_closed`/`count01_le`/`count10_le`/`scan_weight`/`vine_cycle_nonpos`
(twin-bit counting for closed classified walks). Human audit assembles V1
(multi-step), persistence, classification application, n<=4 base.

## Standing and leverage
Vine-confined B<=A is PROVED universally (first universal C=1 region).
It does NOT imply general B<=2A (extremal 5/3 walks visit non-vines;
vines are the tame region for cycles even though vine-vs-vine hosts the
worst single-edge residue). Next: excursion decomposition (vine segments
B<=A + non-vine excursion bound) or per-n fixpoint certificates. DO OPEN.
GC-STATIC OPEN/NO_WITNESS. Zero kills (proof, not refutation).
