# 26AR: essential split-sink allocation (PROVED + OUTCOME A)

**Status: PROVED** — two independent sink bounds, independent A-threshold
lemma, parameterized split-sink theorem, ARmix global theorem with exact-cover
recognizer, certified 16-key essential witness (neither sink alone suffices),
strict extension beyond the full AJ–AQ union. No J4, ROW-DIAMETER, J-SELF,
DTQ, UG, potentials, LP, or compactness. One run + two sinks only; no general
allocation claim.

## AR-L1 — first-sink B bound (PROVED)

After first splay d_B(r)≤2 (26AJ Lemma 2); p−1 further splays avoiding r
(AR-P4), 26AL-L1 each: d_B(r)≤2p, q_r≤p. All p≥3, no geometry.

## AR-L2 — second-sink B bound, p-independent (PROVED)

After last positive splay d_B(s)≤2 (s = its former root); next B-changing
block is KEEP r with r≠s (AR-P3/P5): one 26AL-L1 step gives d_B(s)≤4 at KEEP
s, so q_s≤2 regardless of p. This asymmetry is the structural basis of 26AR.

## AR-L3 — independent A thresholds (PROVED)

u=⌈(p+1)/2⌉, v=⌊(p+1)/2⌋, u+v=p+1 (derived, never assumed — AR-P10).
d_A(r)≥2u−1 ⟹ a_r≥u; d_A(s)≥2v−1 ⟹ a_s≥v. For p≥3: δ_r≤p−2u≤−1,
δ_s≤2−2v≤−2 — both independently negative.

## 26AR-P — split-sink packet (PROVED)

p+2 distinct consecutive blocks (AR-P1–P10: unit run, r≠s, noninterference,
consecutive KEEP(r)/KEEP(s) returns, separate dA thresholds, a_r,a_s<p,
no aggregate premise): p+(p−2u)+(2−2v)=2(p+1−u−v)=0.

## ARmix global theorem (PROVED)

C_ARmix: disjoint partitions into exact banked Type D (26AP-P verbatim),
Type B (26AQ bridge verbatim), Type S (26AR-P), nonpositive singletons; all
positives covered; no reuse. Each packet ≤0 by its theorem; Σδ≤0 ⟹ Q_B≤2A.
C_AQmix⊆C_ARmix (D/B matchers imported from the banked 26AQ module —
preservation by construction; executed: 26AP witness Direct p=3, 26AQ witness
Bridge p1=2/p2=1) and strict (split witness below; §14 executed).

## Recognizer (PROVED sound/complete, O(m⁴))

All m cuts × memoized DP (singleton/Direct/Bridge/Split, fixed priority);
Split tries p≥3 with all 13 AR-P checks (incl. dA thresholds from leader
pre-depths, a_r,a_s<p, keeps-noninterference). Independent `verify_cert`
re-checks every piece incl. derived bound cross-checks. Sound, complete for
C_ARmix (cut enumeration handles internal-nonpositive packets), rotation-
invariant, O(m⁴) packet tests. 15/15 self-tests (witness, preservation ×2,
rotations incl. boundary crossing, wrong-r/s, r==s, threshold fails ×2,
old-deep-sink no-S, overlap caught, uncovered/all-positive rejects, 14-key
control fails essentiality).

## Witness + novelty (OUTCOME A)

16-key vine; 16-mixed prefix (B changes — no vine assumption); 37-cycle;
sweep restores both vines at #21; exact closure; 37/37 table; 53/53 engines;
A=70,Q=39,W=−101; 37 blocks, positives exactly 0,1,2; packet
(+1,+1,+1,−2,−2)=−1; r=16,s=4; dA 4/3 ≥ thresholds 3/3; a=q=2/2 both sinks;
essentiality 3−2=1>0 each, −1 jointly; trajectories 2,4,4 and 2,4 (AR-L1/L2 ✓).
26AO banked (4f4b40e0…) REJECT (0 candidates; parity); 26AP banked
(9abefb16…) REJECT (bad-return a_r=2<3); 26AQ banked (9dc40634…) REJECT.
Accurate local returns reported, not hidden: K7→s=4 one-intervening triple is
locally 26AL-G-compatible but K11/K4 uncoverable (no GLOBAL old cover); K11→
r=16 two-intervening return exists but intermediates (+1,+1) violate 26AM-G
G3. n=16, depths 6, A=70. ⟹ γ*∈C_ARmix∖C_old; C_AQmix⊂neqC_ARmix;
C_old⊂neqC_old∪C_ARmix. 14-key walk retained only as N20 control. 26AM-B kept.

## Scope

p≥3 runs, two consecutive sinks, AR-P8-gated. NOT covered: deeper/multi sinks,
non-unit deficits, inter-packet credit, general allocation, unrestricted
Coarse-Double. Downstream unchanged.
