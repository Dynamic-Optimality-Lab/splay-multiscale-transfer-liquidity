# PIVOT-12: COARSE-DOUBLE Q_B <= 2A (n<=6 proved; n>=7 program)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Target: Q_B<=2A on every
reachable closed Pair-Access cycle (deliberately weaker than DOUBLE-FLEX
Q_B<=2A-Z_B; C.ZIG stays separate, giving B<=3A afterwards for DO with C=3).

## 1. n<=6 ANALYTIC CLOSURE (PROVED, no computation beyond banked certs)
For a closed cycle let A=sum a, Q=sum q, B=sum b (nonneg ints;
q=floor(dB/2)<=ceil(dB/2)=b per KEEP; DELETE has q=b=0).
- A=0: banked zero-A theorem (no A=0,B>0 closed cycle: theorem + finite
  0/14,0/42,0/132) gives B=0; since 0<=q<=b termwise, Q=0. So Q=0<=0=2A.
  (Independently provable directly: A-free access means key==A-root, so
  A never splays and root stays fixed; B changes at most once (first
  KEEP at root), hence a closed A-free walk never changes B at all and
  has Q=B=0. Universal, all n.)
- A>0: Q<=B (termwise) and B/A<=rho_n (banked exact max cycle ratio:
  rho = 1,1,3/2,3/2,5/3) gives B<=(5/3)A<2A, so Q<2A, i.e. Q<=2A-1.
Hence max W_Q = 0 exactly n<=6 (attained by (0,0) self-loops; every A>=1
cycle has W_Q<=-1). No Howard/BF needed (an earlier Howard +1/+2 reading
was traced to an off-by-one depth-table bug in scratch scripts; analytic
proof + fixed-Howard (0/1, 1-12 iters) + replay checks all agree).
Consequence: COARSE-DOUBLE needs new mathematics only at n>=7 (rho
uncertified there). Finite n<=7 evidence below guides it.

## 2. Regression witnesses (§3; q/z/epsilon exact)
- n=5 B.DOUBLE killer (banked A=4,Q_B=6,Z_B=0): W_Q=6-8=-2 SAFE (old
  +2 excess was pure Q under old lens too, but covered 2x by A=4).
- n=6 5/3 cycle, TRUE achiever start (1,5) (closed verified): A=6,Q=4,
  Z=6,B=10. W_Q=4-12=-8, rho_Q=2/3. Epsilon sequence all <=0:
  [-1,-1,-2,-1,-1,-2] (zero overflow; B-excess is zig-driven: Z=6 of 10).
- 3,620 old +1 run-local blocks (a=1,q=2,z=1): epsilon=q-2a=0 EXACTLY.
  Old obstruction disappears definitionally (no computation needed).
- n=32 EXCURSION-BIT killer (K1+K1..K32, (inc,dec)->twin): A=31,Q=49,
  Z=22,B=71. W_Q=49-62=-13 (old W_2=+9 was Z=22 zig-noise; stripping zigs
  kills it with margin 13). W_Q trajectory peaks +23 (exit eps +15, then
  +6,+2) and repays to -13 via steady -1/-2 slack. So zigs, not doubles,
  drove every prior refutation.
- Residue +2 patterns: n=6 (A,B)=(2,6) word K1,K5,K6 has (A,Q,Z)=(2,3,3),
  W_Q=3-4=-1, eps [+2,-1,-2] (overflow repaid inside the excursion);
  n=7 (4,10) word has Q=8 (3+1+1+2+1), A=4, W_Q=0 TIGHT.
- Periodic/two-key/sweep families: random closed-walk sampling to n=7
  gives max W_Q=0 throughout (no positive closed walk found anywhere).

## 3. rho_Q table (§4) + max W_Q (§4)
Upper: rho_Q(n)<=rho(n) via Q<=B: 1,1,3/2,3/2,5/3 (banked integer-BF
certs + achievers). Lower (replay-verified closed): n=6: 2/3 (5/3 word);
n<=5: 1.0 (random closed walks (2,2)); n=2: 0.0; n=7: 1.0 (random,
estimate). max W_Q = 0 EXACT n<=6 (analytic §1; self-loops attain).
n=7 max open (no positive found).

## 4. Zero-A (§5)
A=0 ==> B=0 (banked theorem; also direct: §1) ==> Q=0 (0<=q<=b).
Dependency exact; no computation. (Lean: needs walk model; recorded
as dependency, not kernelized.)

## 5. Epsilon classification (§6/7)
epsilon=q-2a. n=6 exact (209,088 accesses): 4 bad types, ALL a=0
(A-rooted KEEP, B-depth 2-5): (0,1,0)x4008, (0,1,1)x2744, (0,2,0)x1416,
(0,2,1)x424; worst +2. n=7 (2,576,574): 6 types (5x a=0 q<=3 + NEW
(1,3,0)x9716 (B-depth 6, A-depth<=2), worst +3). Universal ladder:
(a,q>=2a+1) i.e. B-depth>=4a+2. Finitely many STRUCTURAL types per level
(A-rooted vs shallow-A-deep-B); values unbounded with n.
Nonconsecution (§19): same-key KEEP-then-KEEP always (0,0) (both rooted
after first: universal, all n). So same-key bad runs have length<=1
(only DELETE-then-KEEP at frozen-deep-B key can follow bad with bad;
then rooted: safe). Cross-key consecutive-bad needs B-depth>=6 (n>=7+);
n<=6 bad accesses are ISOLATED (a=0 everywhere: next same-key is (0,0);
next elsewhere has a>=1 hence q<=2<=2a, safe).

## 6. Vine slack, universal (n>=5) (§20)
Vine-preserving access (stays vine-pair): V1 (n>=5) forces depths<=1 in
splayed trees, so B-depth<=1 and q=floor(d/2)=0; epsilon=-2a<=0 PURE
SLACK (much stronger than old DOUBLE-FLEX accounting where zigs muddied
it). n<=4 covered by global rho (no vine-specific argument needed).

## 7. Matching on 5/3 (§17)
All six accesses have eps<=0, so every B-double pays locally from same-
access A-credits (2a>=q each): matched Q=4/4, unused A-credits 8/12,
unmatched 0. No Hall deficiency (zero overflow: nothing to route).
Nontrivial matching (with overflow) untested: no finite overflow cycle
exists to test on (all n<=6 cycles repay internally per §1).

## 8. Per-excursion-Q program (universal route for vine-visiting walks)
Finite: n=6 all 9,600 excursions have W_Q<=0 (max exactly 0, TIGHT);
n=7 all 46,592 have W_Q<=0; n=32 excursion -13; +2 patterns tight (-1,0).
Vine segments have Q=0 (§6, n>=5). Hence IF per-excursion Q<=2A held
universally, vine-visiting closed walks would satisfy Q<=2A with NO
charging (Q_total = SUM_E Q(E) <= SUM_E 2A(E) <= 2A_total, using
A(V)>=0). n<=4 by rho-global. OPEN universally (restoration wall: return
must repay exit Q-surplus via A-drains; branch-creation/elimination cost
lemmas = C.ZIG-adjacent machinery, unbuilt). E4b-analog (B<=3A finite)
is insufficient (gives Q<=3A, need Q<=2A).
Creator genealogy (§§12-14) defined but not needed if per-excursion-Q
closes; §14B proved universally as §4 above (A-free closed => B=Q=0, so
creator chains terminate at A-costing events on closed cycles).
Minimal-counterexample mode (§25): n<=6 vacuous (analytic closure);
n>=7 open framing recorded (vine-safe regions have eps<=0 (n>=5), so any
minimal violator's surplus sits entirely in non-vine excursions).
Rotation form (§23): 2a=R_A+Z_A banked; Q_B<=R_A+Z_A reading noted, not
pursued (finite matching shows local payment suffices where tested).
Two-edge blocks (§24): q counts B root-path two-edge blocks; capacity
reading banked as interpretation.

## 9. Status + DO chain
n<=6: COARSE-DOUBLE PROVED (analytic §1). n>=7: OPEN (program: per-
excursion-Q universal (finite-exact to n=7) or full matching/genealogy;
non-vine-only needs the same (no vine slack there)). Non-vine-only
universal open everywhere >=7 (n<=6 via analytic). C.ZIG untouched
(separate; combine only on success: B<=3A => E_B<=3S_A+g => LT<=7LT+2g
=> Levy-Tarjan => DO; translation formula already parametric in C per
PIVOT-1 (2C+1 with C=3 gives 7), mechanical substitution queued).
Lean (§29): no new kernels (nothing cleanly kernelizable without walk/
splay models; epsilon identities definitional; V1 formalization queued
since PIVOT-9). GC/Hall/R3 unvisited. Zero kills (no counterexample to
Q_B<=2A found anywhere; only proof-route/obstruction refinements).
