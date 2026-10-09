# PIVOT-10B: Excursion-Bit Law (finite-exact + partial universal + obstruction)

Branch `wp5x-k6c2-specialized`, HEAD `88f344d`. Target inequality:
  r(E) <= d(s)-d(t)   [d = differ-bit: 1 differ, 0 twin]
i.e. DT: W<=+2; DD: W<=0; TT: W<=0; TD: W<=-2. Equivalent (residuals
integral) to D1+F1+F2+R0 jointly (mechanical both directions, §1).
r(E) = W_2(E)-(tau(s)-tau(t)) UNCHANGED from PIVOT-9-2/10A.

## 1. Equivalence (mechanical, no splay)
r<=d(s)-d(t) with d in {0,1}: (a) values <= +1 max give D1 (r<=1);
(b) r=+1 forces d(s)-d(t)>=+1, i.e. (1,0) = DIFFER->TWIN (F1+F2);
(c) r=0 forces d(s)-d(t)>=0, i.e. forbids (0,1) = TWIN->DIFFER (R0:
twin-start r=0 ends twin); (d) negative r automatic (r<=-1 <= c since
c>=-1). Conversely D1+F1+F2+R0 imply the bit law per endpoint class
(DT by D1; DD/TT by D1+never-+1-there; TD by D1+R0+integrality).
One four-case endpoint theorem, as claimed.

## 2. Finite verification: EXCURSION-BIT HOLDS EXACTLY (n=6, n=7)
n=6 (9,600 shortest first-returns, complete): per-class max W =
TT:0 (bound 0, TIGHT); TD:-3 (bound -2); DT:+2 (bound +2, TIGHT);
DD:-2 (bound 0). Zero violations. Counts: TT 3,530 / TD 1,206 /
DT 3,216 / DD 1,648.
n=7 (46,592 shortest, complete): positives all DT (103 x +1, 1 x +2);
twin-start r=0 all end twin (72/72, no TD-r0); Wmax +2 (DT); hence all
four cases hold (DD/TT: no W>=+1 outside DT; TD: no r>=0). Zero violations.
Length-2 subledger (n=6, 3,722): DD max -4, TD max -3, DT/TT max 0.

## 3. Universal results proved this run
(a) §10 vine bit-change law (ALL n, no V1): d(v)-d(u) <= A(V) on every
vine-confined path. Per-edge: a_e=0 ==> diff<=0 (x A-rooted: post-A-root
x; twin-source stays twin since B splays x to root or freezes rooted B;
differ-source diff<=0 trivially); a_e>=1 ==> diff<=+1<=a_e. Telescope.
Kernel: Lean `vine_bit_le_A` (+`vine_step_le`) green.
(b) Re-entry A-forcing (ALL n): landing-DIFFER re-entry is DELETE with
a_r>=1 (KEEP always twin-roots; a_r=0 ==> pre vine-pair, contradicting
first-return interior). Hence DD/TD re-entries contribute w_re<=-2a_r<=-2.
(c) No-A-zero excursions (ALL n): A(E)>=1 always (B-root/frozen argument:
A-frozen B-moves root-then-stick; return to vine impossible).
(d) Length-2 DD/TD (n>=5): W<=-3. Proof: re-entry DELETE (a_r>=1, B-pre
must be vine since B frozen) forces exit A-only-branching (B stays vine);
V1 (n>=5) gives exit a_e>=1 (A dA>=2) with b_e<=1-or-0; total
(b_e-2a_e)+(-2a_r) <= -3. Data: DD max -4, TD max -3 (exact).
(e) T1 (banked, Lean `twin_exit_A`): non-trivial vine from twin has A>=1.

## 4. Precise obstruction (why DT/TT/longer resist)
Restoration capacity: B-deep-restore-to-vine per StepEv type is unbounded
in principle (deep splays) but empirically capped (single zig fixes <=2
branches; deep exits create more than any single re-entry removes; the
+1 family needs exactly its 1-3 neutral middles + (1,1) closer).
Proving any universal restoration bound needs per-StepEv
branch-creation/elimination lemmas (how many branch-nodes each
zig/zigzig/zigzag creates/destroys and at what depths) = C.ZIG-ownership
branch mechanics = the NEXT campaign. Interior B-work vs A-work tradeoff
during restoration has no bound in the current toolkit (V1 is one-way:
vine->vine only; restoration is non-vine->vine). No counterexample found:
steered n=8..32 (deep-B/shallow-A exits, long/all-KEEP/DELETE-poor words,
lifts/mutations, ~15k trials) max r=-8; four thresholds
(DT r>=2, DD/TT r>=1, TD r>=0) never breached.

## 5. Summation (§§9-11, given EXCURSION-BIT + §10)
V_i:t_{i-1}->s_i, E_i:s_i->t_i. sum r(E_i) <= SUM[d(s_i)-d(t_i)]
= SUM[d(s_i)-d(t_{i-1})] (cyclic reindex) <= SUM A(V_i) = A_vine by §10.
Then W_2 = sum r_E - A_vine <= 0 (banked residual identity). B<=2A on
vine-visiting closed walks. CONDITIONAL on EXCURSION-BIT (open).

## 6. Status (SUPERSEDED by §7 refutation below; preserved as record)
EXCURSION-BIT: TRUE on all finite evidence (n<=7 complete shortest:
56,192 excursions, 0 violations, tight DT/TT), partially proved
universally (DD/TD length-2 with margin; §10 all-n; re-entry forcing;
no-A-zero), OPEN in general (restoration-capacity gap above).
VINE_VISITING_C2: CONDITIONAL (unchanged from PIVOT-10A; debt-machine
needs D1/F1/F2/R0 = EXCURSION-BIT content). NO upgrade to unconditional.
NO universal claim (per §8). DO chain unassembled. GC/Hall/R3 unvisited.
Next: NONVINE_C2 via C.ZIG ownership + persistent-branch + mandatory-A-work.
Zero kills (exact witnesses + partial universal theorems banked).

## 7. REFUTATION: EXCURSION-BIT is FALSE (sweep-return family)
Primary witness (`vine_excursion/refutation_n32.json`, replay-verified,
sha256 c7d01179...): n=32, start (inc-vine, dec-vine) differ-pair (roots
1 vs 32); word K1 + K1..K32 (33 all-KEEP); interior 32 states ALL
non-vine; end twin-vine-pair (roots 32,32). Totals A=31, B=71, W=+9.
DT class (differ->twin): requires W<=+2, have +9. Residual r = +8
(requires <=+1). Mechanics: exit (0,16) [B-depth-31 splay] + sweep phase
(32 steps, per-step ~(1,1.7): B/A ratio ~2.29 sustained, net -7) = +9.
The sweep return repays (-7) but cannot cover the deep exit (+16).
Smaller witness: n=20, same family, L=21, A=19, B=42, W=+4, r=+3.
Onset <= 20 in sweep family (n<=18 clean on probed words).
Growth across n=8..32 best-W: 0,0,1,2,4,5,9 (~n/4, residue growth for
excursions, matching open-walk pattern).
KILLED: EXCURSION-BIT universal (DT violated); D1 (r<=+1, have +8);
E3 as universal; PIVOT-10A debt-machine hypotheses (conditional
collapses: non-+1 no longer implies r<=0). NOT killed: Lean kernels
(vine_cycle_nonpos, vine_path_bound, twin_exit_A, vine_bit_le_A all
remain true proved theorems about classified walks); PIVOT-9 vine B<=A;
n<=6 global rho certs; C.ZIG; E4b (witness has B=71<=93=3A, holds);
global B<=2A itself (witness is OPEN; closing it adds return work).
Consequence: VINE_VISITING_C2 loses its debt-machine route (not merely
conditional-open). The obstruction is now quantitative and structural:
deep-B exits (b~n/2) with sweep returns that sustain B/A>2. Next routes
must bound exit-minus-return jointly (excursion as a whole), not per-edge
or via fixed residuals.
