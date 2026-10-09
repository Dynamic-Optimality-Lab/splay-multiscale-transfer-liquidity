# PIVOT-11: Unbounded Vine-Disagreement Credit (negative endpoint)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Target was structural D with
W_2(e) <= D(s)-D(t) on all vine-boundary macro edges (unbounded-in-n
allowed). RESULT: no such D found across ~40 principled variants; bias
microscope shows exact credit is flat/uncorrelated; fundamental tensions
documented below. Per §29 this is the negative endpoint (not abandonment:
precise obstruction + closest correct fragments banked).

## A. Canonical vine encoding (PROVED finite + verified)
Endpoint-choice words (L=take min, R=take max over remaining interval):
bijection between BST vines and {L,R}^(n-1) (2^(n-1) shapes; roundtrip
exact n<=8, 0 bad). Vine roots are always global endpoints (1 or n):
interior root would need 2 nonempty children. Hence pos0-disagreement
<=> roots differ <=> twin-bit tau (verified 0 mismatches, all vine-pairs).
Macrograph M_n built exactly (n<=7); n=32 witness representable (W=+9).
Scripts: temp vexenc.py (encoding), scripts/wp6_vine_excursion{,_n7}.py.

## B/C. n=32 family anatomy (design oracle)
Word K1+K1..K32 from (inc-vine, dec-vine) differ-pair; 32 interior states
ALL non-vine; end twin-vine (32,32). A=31=n-1 EXACT (exit a=0 + noop +
31x a=1: sweep does unit A-work per new key). B=71 (exit 16 + sweep 55,
per-step ~(1,1.7)). W=+9. Full 33-step trace banked (temp vextrace.py):
exit (0,16) jumps W to +16; steps 2-5 add +10 more (B-bursts 8,5,2,3);
then steady repayment (-17) to +9, never enough. ALL sweep states are
TWIN-rooted (k,k) but branched (twin != vine). End: both left-vine H=0.
Mechanism: monotone sweep flips one vine end-to-end (A: L^31->R^31) while
the other takes a branched detour back to itself; B-work (~2.3x A-work)
accumulates because the detour needs deep splays. Growth best-W n=8..32:
0,0,1,2,4,5,9 (~n/4). A(n)=n-1 exact (n=20,32); B(n) measured (42,71).

## D. Finite bias h (microscope result: NEGATIVE)
Least fixpoint Q>=0 with W<=Q(u)-Q(v) on n=6 fine pair graph (209k
edges): converged 2 rounds, maxQ=3. On vine-pairs Q-(H+tau) ranges -5..+1
(mostly negative: H+tau overestimates); (H,tau)->residual nonfunctional
(14 collisions); H=1..4 all map to all Q values; H=0->Q={0}. Exact credit
is FLAT (0..3) and UNCORRELATED with Hamming/spine structure. h is
Bellman-value (forbidden as theorem per §6); recorded only to show no
Hamming-like D resembles it. Temp vexbias.py.

## E/F. Candidates falsified (exact minimal counterexamples banked)
- H: vine 128x (0,1)-swap (u=90->28,K1: RLLLL->LRLLL vs LLLLL, pos0->pos1,
  H conserved, W=+1, gap 1); exc 41 (worst gap 2: W=0 twin->twin H+2).
- H+tau: vine 128x (1,0)-twin->differ H+2 (gap 1: -2 vs -3); exc 28
  (16 growers + 8 (0,3,6) + 4 +2s with H-drop 0).
- Weighted PL/PR/PD: worse (128-256 vine, 502-1771 exc; growth x weight).
- Directed root-depths (5 combos H+T±dArooB/dBrooA): 92-326 viol
  (DELETE re-rooting jumps + same residues).
- Positional subsets (9 rules): best R0-rule ({0}+tau) 0+0 BUT witness
  capped +2 (needs +9); EVEN 0+23; others 128+14-30.
- Rank (first/last-diff): 64+8 / 240+211.
- Deep-mass grid (9: shallow x uniform-deep): best 12-20 (mild growers
  creating deep with W~0); interval-deep 175-238.
- Pair/top2/sum/counts (prior campaign): worse.
- Twin-indicator coefficients: PROVEN impossible (entries need c<=-1,
  exits need c>=+1; also =1-tau redundant).
- B-depth caps: PROVEN tradeoff (cap<=1 kills witness-scale; uncap breaks
  on A-moving DELETE jumps).
R0-rule (D=2tau, i.e. positions-{0}+tau since pos0=tau): 0 vine + 0
excursion violations (n=6 explicit; n=7 derived from posW/posT + twin-start
lists). Closest correct fragment (see G).

## G. What actually holds (banked true fragments)
- R0-rule D=2tau: W<=2*Dtau on ALL vine-internal edges, UNIVERSAL (n>=5:
  V1-costs {(0,0),(1,0),(0,1),(1,1)} + root-tracking flips; (0,1) always
  differ->twin; (1,0) always W=-2>=-2; (1,1) lands twin; (0,0) loops;
  n<=4 finite: 2/16/64/210 edges, 0 viol). Kernel: existing Lean
  `vine_W2_twin_bound` (+`vine_W2_step_le`), green. Telescopes to vine
  paths. Tight on +2s (+2<=+2) and (1,0)-exits (-2<=-2). Range-capped +2:
  insufficient for witness (+9). No new Lean needed (already green).
- Deep-frozen (n>=5): vine-internal moves change endpoint-letters only at
  positions {0,1} (verified max=1 over 2,688 edges n=6; follows from
  zig/noop-only (V1) + rotation tables). Hence deep mass never affects
  vine-edge inequalities (free variable there).
- Vine-edge combos collapse to 8 (W,d1,dtau) patterns (verified).
- Positional creation/destruction overlap: growers create at {2,3,4}
  (all of them: pairs (2,4),(3,4),(2,3) all occur); +2s destroy {0}(+{4}).
  Any deep mass >0 at grower-create positions breaks mild (W=0/−1)
  growers; mass 0 there starves witness-scale. Proven tension (not just
  bad luck): same positions must both pay (destroy, need high) and forgive
  (create, need low).

## H-L. Remaining spec items (brief, mostly negative)
- H. Disagreement-creation cost: rebuilding (twin->differ) via (1,0)
  costs exactly W=-2 = R0-bound (tight); deeper transitions unmeasured
  systematically (R0 covers all: any twin->differ edge has W<=-2? NO:
  only (1,0) has W=-2; (1,b>=1)? twin->differ with b>=1: (1,1) lands twin
  (not differ); (1,0) only (DELETE, b=0). So twin->differ vine-edges are
  EXACTLY (1,0)-DELETEs with W=-2 = bound (tight, universal n>=5). Clean.)
- I. C.ZIG integration: not attempted (no D to integrate into; banked
  separately, preserved).
- J. Universal macro-edge inequality: NOT proved (see §29).
- K. VINE_VISITING_C2: still OPEN (R0-rule proves B<=2A only where its
  +2 range suffices; witness excursions exceed it).
- L. Lean: no additions (R0 kernel exists green; encoding is Python-
  verified infra; no D to formalize per §27).
- M. Extension to non-vine-only: D was never found, so nothing to extend;
  non-vine chamber untouched (5/3 extremal banked as-is).

## §29 NEGATIVE ENDPOINT (formal)
No tested principled D (list in E/F above: ~40 variants across Hamming,
weighted, directed, subset, rank, deep-mass, twin-augmented families)
satisfies W_2(e)<=D(s)-D(t) on all n=6 macro edges (2,688 vine + 9,600
excursions) AND the n=32 witness (needs +9). Closest: R0-rule (perfect
locally, range-capped +2) and Hamming (pays witness +31, leaks 128+41
with gaps 1-2). Structural reasons (not bad luck): (i) swap/growth need
opposite twin-signs (proven coefficient contradiction); (ii) creation/
destruction overlap at every deep position (measured); (iii) scale-vs-
tightness (witness needs +9 mass; mild growers forbid mass where they
create); (iv) bias microscope shows exact credit is flat/uncorrelated
with spine structure. Vine disagreement as sole boundary credit is
insufficient in additive positional form. Recommended next: joint
exit-return bounding per excursion (residue grows ~n/4; fixed-residual
charging dead per PIVOT-10B) and/or C.ZIG-ownership branch mechanics
for restoration capacity. DO NOT revive EXCURSION-BIT. GC/Hall/R3
unvisited. Zero global kills (all refutations are of proof routes and
candidate laws, on open-walk/macro objects).
