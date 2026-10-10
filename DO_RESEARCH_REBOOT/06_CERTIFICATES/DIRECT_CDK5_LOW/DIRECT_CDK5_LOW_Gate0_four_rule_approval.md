# DIRECT-CDK5-LOW Gate 0: four-rule approval — FOUR PASS, AUTHORIZED

**HEAD:** `9ec277c0ff4078ff80dee44cd680400f0bf3603f` verified; worktree clean at
start. Frozen: |M|=5, core ≤8, w(U,x)=⌊d/2⌋−2·1[x≠root], inventory counts
210/3960/45045/400400 = 449,615 raw. No post-hoc boundary changes (nine-node
class stays excluded even if convenient).

## R1 — STRICTLY SMALLER: PASS

Five-KEEP-key + eight-core restriction of universal Coarse-Double; source
semantics unchanged. Nonempty complement demonstrated: the nine-node witness
(M={1,3,5,7,9}, T0 as specified, word K3,K7,K1,K9,K5,K7,K1,K9) replays
authoritatively with depths 6,4,4,4,6,4,4,4 exact, A/B closure PASS/PASS,
engines agree, Q=18, C_K=8, A=18, **core size 9 at all 8 states** —
a real source instance outside the ≤8 class. The restriction is load-bearing:
Q_B−2C_K=+2 there, so no B-only certificate can cover it (regression control).

## R2 — SOLVABILITY MECHANISM: PASS

Exact finite weighted-core cycle certification: graph vertices = valid BST
marked cores (5 marks, 5–8 nodes); edges = source-exact marked splays with
weight w above; longest-path potentials (exact integers) or a positive
countercycle. Reduction obligations: K4-L1 (banked, arbitrary M), pruning
(banked, marked x), nine-node upper bound + closed-core conservation (Phase 2
proofs, same induction as the banked four-key case). Small-n screening is
corroboration only.

## R3 — ONE-PROMPT SCOPE: PASS

One theorem (CDK5-LOW). Supporting lemmas (nine-bound, conservation, pruning
correctness, graph construction, one certificate, novelty) feed it directly.
No packet families, no cardinality induction, no nine-node campaign, no
replacement potentials on failure (STOP instead).

## R4 — UPWARD PROGRESS: PASS

Five-key witness `ins1-1-K2` (vine-7, prefix D7,D6, word
K7,K2,D2,D4,D6,K1,K3,K5,K3,K1,D2,D4,D7,D6): A=19, Q=9, W=−29, exact closure,
engines agree, all five KEEP keys {1,2,3,5,7} genuine, max core 7 ≤8. Sole
positive K7 (δ=+1, r=1; successors 2,2,4): AJ/AK/AL-G/AM-G fail positionally;
single positive bars AN/AO/AP/AQ/AR/AS packet covers (all five recognizers
REJECT authoritatively); RT2-A/CDK4-A inapplicable (5 keys); baselines excluded
(n=7, dB=6, A=19). Fifth key K2 genuinely splays (not attached). Strictly new
coverage, W<0 (coverage, not counterexample).
