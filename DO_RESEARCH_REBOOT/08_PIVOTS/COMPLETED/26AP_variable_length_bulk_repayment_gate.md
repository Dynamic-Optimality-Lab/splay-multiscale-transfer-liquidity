# PIVOT-26AP gate: variable-length bulk repayment — OUTCOME A

## A. Safety

Branch `coarse-double-branch`, HEAD `88d3007`, dirty only with
DO_RESEARCH_REBOOT artifacts. No reset/clean/stash/checkout/commit/push;
writes confined to DO_RESEARCH_REBOOT/; source semantics untouched; 26AJ–26AO
records (incl. 26AM Outcome B) preserved.

## B. Foundations

26AJ Lemma 2, 26AL-L1, 26AM/26AN/26AO statements, exact 26AO recognizer
(sha256 `4f4b40e0…`), source KEEP/DELETE/block/deficit semantics re-verified;
premises valid; no silent repairs.

## C. Cost and block model

a=⌈dA/2⌉, KEEP q=⌊dB/2⌋, DELETE q=0; cyclic A-root blocks; δ=q−2a;
Q−2A=Σδ; zero-A banked. 29 accesses → 27 blocks (two no-ops grouped).

## D. Parameterized depth theorem

26AP-L1: d_B(r)≤2p for all p≥1 (induction via 26AL-L1 per genuine splay);
sharp form h_i+2(p−1); q_return≤p. Witness: 4 ≤ 6 ✓.

## E. Signed bulk repayment

26AP-L2: a_return≥p ⟹ δ_return≤−p. Witness: a=3=p, q=2, δ=−4 ≤−3 ✓.

## F. Universal local theorem

26AP-P: p unit positives + return ≤ p−p = 0, all p≥1. Witness: +1+1+1−4=−1.

## G. Global maximal-run theorem

R1–R6 class; disjoint run+return groups; m=1-positive and all-positive
correctly excluded; repetition certified. Q_B≤2A on C_26AP.

## H. Recognizer

Amended cut (min nonpositive j, j+1..j), O(m)/O(m); sound + complete for
R1–R6; cut-independence executed (24/24 agree) and proved; rotation-invariant;
self-tests 6/6.

## I. 16-key witness

Vine-16 start; 9-DELETE prefix (B vine); 29-access cycle; A/B + repetition
closure; 29/29 table; 38/38 engines; A=46, Q=27, W=−65; 27 blocks; positives
exactly 3; p=3 packet accepted.

## J. Strict novelty

Three roots (1/11/9) vs every domain — all excluded; 26AO banked REJECT + 2k
parity; 26AP ACCEPT; strict union extension proved.

## K. Four-rule audit

```text
RULE 1 — STRICTLY SMALLER: PASS (unit runs + immediate returns; no J4/globals)
RULE 2 — CONCRETE SOURCE-DERIVED MECHANISM: PASS (L1/L2 from depths+counts)
RULE 3 — BOUNDED DECISIVE PROOF OR STOP: PASS (witness-first, no hunt)
RULE 4 — NEW ORIGINAL COARSE-DOUBLE OBLIGATION DISCHARGED: YES
```

## L. Final pipeline status

```text
26AP PARAMETERIZED FORMER-ROOT DEPTH: PROVED
VARIABLE-LENGTH SIGNED BULK REPAYMENT: PROVED
GLOBAL MAXIMAL-RUN COARSE-DOUBLE: PROVED
DETERMINISTIC O(m) RECOGNIZER: SOUND AND COMPLETE FOR ITS DOMAIN
CYCLIC CUT INDEPENDENCE: PROVED (24/24 executed)
16-KEY REACHABILITY: VERIFIED
29-ACCESS A/B CLOSED CYCLE: VERIFIED (+ repetition)
38/38 ENGINE AGREEMENT: VERIFIED
THREE UNIT-POSITIVE BLOCKS: VERIFIED
p=3 BULK REPAYMENT: (+1,+1,+1,-4) = -1
ALL THREE FORMER-ROOT AUDITS: PASS
26AO RECOGNIZER: REJECT
26AP RECOGNIZER: ACCEPT
EXCLUSION FROM ALL PRIOR DOMAINS: VERIFIED
STRICT ORIGINAL COARSE-DOUBLE DOMAIN EXTENSION: PROVED
FOUR RULES: PASS / PASS / PASS / YES
FINAL VERDICT: 26AP OUTCOME A — PROVED
UNRESTRICTED COARSE-DOUBLE: OPEN
DYNAMIC OPTIMALITY: OPEN
```

No 26AQ launched. Stop.
