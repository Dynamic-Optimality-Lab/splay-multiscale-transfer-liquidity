# 26AQ: shallow-bridge cross-run repayment (PROVED + OUTCOME A)

**Status: PROVED** — universal bridge lemmas, two-run signed packet theorem,
mixed 26AP/26AQ global theorem with exact-cover recognizer, certified 16-key
witness (p1=2,p2=1), strict extension beyond 26AP and all prior domains. No J4,
ROW-DIAMETER, J-SELF, DTQ, UG, potentials, LP, or compactness. Exactly ONE
bridge per packet; no general allocation claim.

## AQ-L1 — bridge credit (PROVED, source arithmetic)

Genuine KEEP at 1≤d_B(z)≤3 with a≥1: q≤1, δ≤−1. (Same defs as 26AN-L1/AO-L1.)

## AQ-L2 — cross-run former-root depth (PROVED)

After first splay d_B(r)≤2 (26AJ Lemma 2). Intervening B-changing splays:
(p1−1) + 1 (bridge) + p2 = p total (AQ-P4: all avoid r, so 26AL-L1 applies per
splay): d_B(r)≤2+2p=2(p+1); q_return≤p+1. Universal in p1,p2≥1.

## AQ-L3 — final return (PROVED)

a_return≥p (source-tested, ⟺ d_A(r)≥2p−1) gives δ≤(p+1)−2p=1−p. The bridge's
−1 cancels the one extra B-double allowance — depth-tax cancellation.

## 26AQ-P — two-run bridge packet (PROVED)

p+2 distinct consecutive blocks (AQ-P1–P7): p1+p2=p≥3 unit positives, one
genuine shallow bridge (z≠r), return led by KEEP of r with a≥p, interveners
avoiding r, no geometry: p1−1+p2+(1−p)≤0.

## Mixed global theorem (PROVED)

C_AQmix: cyclic partitions into banked-exact 26AP direct packets (P1–P6
verbatim), 26AQ bridge packets (p≥3), nonpositive singletons; every positive
in exactly one packet; packets contiguous, disjoint, unreused. Each packet ≤0
(26AP-P / 26AQ-P); Σδ≤0 ⟹ Q_B≤2A. C_26AP⊆C_AQmix (direct transition exact;
cut enumeration finds a boundary; DP reconstructs old decomposition —
executed: banked 26AP witness ACCEPTED with Direct p=3) and the inclusion is
strict (bridge witness below).

## Recognizer (PROVED sound/complete, O(m³))

All m cyclic cuts × memoized DP (singleton-iff-nonpositive / maximal-run
Direct / maximal-run Bridge with p≥3, fixed priority); emits cut + pieces +
singles. Sound (pieces re-validated by independent verifier); complete for
C_AQmix (some cut aligns with a piece boundary — bridges internal nonpositives
handled by enumeration, not by a nonpositive-cut assumption); rotation-
invariant; no double credit; no total-sign shortcut; O(m³) packet tests.

## Witness + novelty (OUTCOME A)

16-key vine; 9-DELETE prefix (B vine); 30-access cycle, exact A/B closure;
30/30 table; A=50,Q=23,W=−77; 28 blocks (two no-ops grouped); positives
exactly blocks 0,1,3; bridge packet (+1,+1,−1,+1,−6)=−4 (p1=2,p2=1,p=3);
roots 1/11/10; r-trajectory 2,2,3,5 (≤8 ✓); K10 dB=2 genuine, z≠r; interveners
{9,10,16}∌1; return a=4≥3; engines 39/39. Mixed recognizer ACCEPTS (bridge);
26AO banked (4f4b40e0…) REJECTS (0 Type I/II candidates; 2k-parity bars odd-3);
26AP banked (9abefb16…) REJECTS (two runs, successors K10≠1 and K1≠10).
AJ/AK/AL (successor keys), AM-G (next-+1 / third-succ K15≠10), AM-S,
bounded classes (n=16, depths 10/6/6, A=50) all excluded per-block. ⟹
γ*∈C_AQmix∖C_old; C_26AP⊂neqC_AQmix; C_old⊂neqC_old∪C_AQmix. 26AM-B preserved.

## Scope

One bridge, unit positives, p≥3 bridge packets. NOT covered: multi-bridge,
non-unit deficits, inter-packet credit, general allocation, unrestricted
Coarse-Double. Downstream unchanged.
