# PIVOT-26AQ gate: cross-run credit transfer — OUTCOME A

## A. Repository safety

Branch `coarse-double-branch`, HEAD `88d3007`, dirty only with
DO_RESEARCH_REBOOT artifacts. No reset/clean/stash/checkout/commit/push;
writes confined to DO_RESEARCH_REBOOT/; source semantics untouched; 26AJ–26AP
records (incl. 26AM Outcome B, 26AP Outcome A) preserved.

## B. Banked mathematical foundations

Former-root ≤2, displacement +2/splay, shallow-credit −1, 26AP-P (P1–P6),
banked 26AP recognizer (`9abefb16…`), banked 26AO recognizer (`4f4b40e0…`)
re-verified; premises valid; no silent repairs.

## C. Original cost semantics

a/q/DELETE/blocks/δ identity as banked; 30 accesses → 28 blocks (no-ops
grouped, asserted); zero-A preserved.

## D. AQ-L1 — Shallow bridge

δ_bridge≤−1 from dB≤3 + a≥1 (witness: K10 dB=2, δ=−1) ✓.

## E. AQ-L2 — Cross-run former-root depth

d_B(r)≤2(p+1), q_return≤p+1, per genuine splay (witness: 5 ≤ 8) ✓.

## F. AQ-L3 and AQ-P

δ_return≤1−p (witness: −6 ≤ −2); packet p1−1+p2+(1−p)≤0 (witness: −4) ✓.

## G. Global restricted theorem

C_AQmix partitions (Direct + Bridge + singletons); disjoint; Q_B≤2A proved.

## H. Deterministic recognizer

All-cuts × DP exact cover, O(m³); soundness/completeness/rotation-invariance
proved; independent cert verifier; 26AP preserved (Direct p=3 ACCEPT);
self-tests pass (direct-p1, bridge-1+2, bridge-p2/all-positive rejects).

## I. Authoritative witness

Vine-16; 9-DELETE prefix (B vine); 30-access cycle; A/B closure; 30/30 table;
39/39 engines; 28 blocks; positives exactly 1,2,4 (1-based); packet
(+1,+1,−1,+1,−6)=−4; A=50, Q=23, W=−77 ✓.

## J. Strict novelty

Roots 1/11/10 vs AJ–AM (per-block table); 26AO REJECT (0 candidates, parity);
26AP REJECT (both runs); mixed ACCEPT; C_26AP⊂neqC_AQmix; union enlarged ✓.

## K. Four-rule verdict

```text
RULE 1 — STRICTLY SMALLER: PASS (one bridge, p>=3, no globals/J4)
RULE 2 — CONCRETE SOURCE-DERIVED MECHANISM: PASS (L1/L2/L3, tax cancellation)
RULE 3 — BOUNDED DECISIVE PROOF OR STOP: PASS (witness-first, no hunt)
RULE 4 — GENUINE NEW ORIGINAL COARSE-DOUBLE COVERAGE: YES
```

## L. Terminal pipeline status

```text
26AQ SHALLOW BRIDGE CREDIT: PROVED
CROSS-RUN FORMER-ROOT DEPTH: PROVED
CROSS-RUN SIGNED REPAYMENT: PROVED
UNIVERSAL RESTRICTED PACKET THEOREM: PROVED
MIXED 26AP/26AQ CYCLIC RECOGNIZER: SOUND AND COMPLETE FOR ITS DOMAIN
26AP DOMAIN PRESERVATION: PROVED
16-KEY DIAGONAL REACHABILITY: VERIFIED
30-ACCESS A/B CLOSED CYCLE: VERIFIED
39/39 ENGINE AGREEMENT: VERIFIED
28 CYCLIC A-ROOT BLOCKS: VERIFIED
THREE POSITIVE BLOCKS: VERIFIED
TWO POSITIVE RUNS: VERIFIED
SHALLOW BRIDGE: VERIFIED
SIGNED PACKET: (+1,+1,-1,+1,-6) = -4
A=50, Q_B=23, W=-77: VERIFIED
BANKED 26AO RECOGNIZER: REJECT
BANKED 26AP RECOGNIZER: REJECT
NEW 26AQ RECOGNIZER: ACCEPT
EXCLUSION FROM ALL PRIOR DOMAINS: VERIFIED
STRICT ORIGINAL COARSE-DOUBLE DOMAIN EXTENSION: PROVED
FOUR RULES: PASS / PASS / PASS / YES
FINAL VERDICT: 26AQ OUTCOME A — PROVED
GENERAL STRUCTURAL CREDIT ALLOCATION: OPEN
UNRESTRICTED COARSE-DOUBLE: OPEN
DYNAMIC OPTIMALITY: OPEN
```

No 26AR launched. Stop.
