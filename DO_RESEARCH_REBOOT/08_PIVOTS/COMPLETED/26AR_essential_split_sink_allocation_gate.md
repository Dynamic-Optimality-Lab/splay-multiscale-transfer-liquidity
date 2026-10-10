# PIVOT-26AR gate: essential split-sink allocation — OUTCOME A

## A. Repository safety

Branch `coarse-double-branch`, HEAD `88d3007`, dirty only with
DO_RESEARCH_REBOOT artifacts. No reset/clean/stash/checkout/commit/push;
writes confined to DO_RESEARCH_REBOOT/; source semantics untouched; 26AJ–26AQ
records (incl. 26AM Outcome B) preserved. 14-key walk NOT used as witness.

## B. Banked inputs

AJ–AQ statuses verified; 26AJ Lemma 2, 26AL-L1, 26AP-P, 26AQ bridge, three
banked recognizers + hashes confirmed; premises valid; no silent repairs.

## C. Source model

KEEP/DELETE, a/q, 37 blocks (all a≥1), δ identity, zero-A banked ✓.

## D. AR-L1

d_B(r)≤2p, q_r≤p (witness: 4 ≤ 6, q=2 ≤ 3) ✓.

## E. AR-L2

d_B(s)≤4, q_s≤2, p-independent (witness: traj 2→4, q=2) ✓.

## F. AR-L3 and AR-P

u=v=2; dA 4/3 ≥ 3/3 ⟹ a≥2/2; p+(p−2u)+(2−2v)=0 (witness: −1) ✓.

## G. Global restricted theorem

C_ARmix partitions (D+B+S+singletons); disjoint; Q_B≤2A proved ✓.

## H. Recognizer

All-cuts × DP, O(m⁴); sound/complete/invariant; independent verifier; AP/AQ
preserved by imported validators; 15/15 self-tests ✓.

## I. New authoritative witness

Vine-16; 16-mixed prefix; 37-cycle; sweep vines at #21; closure; 37/37 table;
53/53 engines; 37 blocks; 3 positives; r=16, s=4; sinks −2,−2; essentiality
1,1→−1; A=70, Q=39, W=−101 ✓.

## J. Strict novelty

Three roots vs AJ–AM (accurate incl. local-compat honesty notes); 26AO/26AP/
26AQ actual REJECTs; ARmix ACCEPT; AP/AQ preserved; C_AQmix⊂neqC_ARmix;
union enlarged ✓.

## K. Four-rule verdict

```text
RULE 1 — STRICTLY SMALLER: PASS (one run, two sinks, AR-P8-gated)
RULE 2 — CONCRETE SOURCE-DERIVED INDEPENDENT MECHANISM: PASS (L1/L2/L3, no aggregate premise)
RULE 3 — BOUNDED PROOF OR STOP: PASS (witness-first, no hunt)
RULE 4 — NEW RESTRICTED UNIVERSAL THEOREM PLUS STRICT REACHABLE CLOSED-WALK COVERAGE: YES
```

## L. Final pipeline status

```text
26AR FIRST FORMER-ROOT BOUND: PROVED
26AR SECOND FORMER-ROOT BOUND: PROVED
INDEPENDENT A-DEPTH THRESHOLD LEMMA: PROVED
UNIVERSAL PARAMETERIZED SPLIT-SINK PACKET THEOREM: PROVED
GLOBAL ARmix COARSE-DOUBLE: PROVED
CYCLIC EXACT-COVER RECOGNIZER: SOUND AND COMPLETE FOR ITS DOMAIN
AQmix DOMAIN PRESERVATION: PROVED
NEW 16-KEY DIAGONAL REACHABILITY: VERIFIED
37-ACCESS A/B CLOSED CYCLE: VERIFIED
53/53 INDEPENDENT SOURCE AGREEMENT: VERIFIED
37 A-ROOT BLOCKS: VERIFIED
EXACTLY THREE POSITIVE BLOCKS: VERIFIED
FORMER ROOTS r=16, s=4: VERIFIED
FIRST RETURN ACTUAL DEFICIT: -2
SECOND RETURN ACTUAL DEFICIT: -2
FIRST RETURN ALONE: INSUFFICIENT
SECOND RETURN ALONE: INSUFFICIENT
BOTH RETURNS: SUFFICIENT
ESSENTIAL PACKET: (+1,+1,+1,-2,-2) = -1
A=70, Q_B=39, W=-101: VERIFIED
ACTUAL 26AO RECOGNIZER: REJECT
ACTUAL 26AP RECOGNIZER: REJECT
ACTUAL 26AQ RECOGNIZER: REJECT
NEW 26AR RECOGNIZER: ACCEPT
FULL PRIOR-DOMAIN EXCLUSION: VERIFIED
STRICT ORIGINAL COARSE-DOUBLE DOMAIN EXTENSION: PROVED
FOUR RULES: PASS / PASS / PASS / YES
FINAL VERDICT: 26AR OUTCOME A — PROVED
GENERAL STRUCTURAL CREDIT ALLOCATION: OPEN
UNIVERSAL COARSE-DOUBLE: OPEN
DYNAMIC OPTIMALITY: OPEN
26AS: NOT LAUNCHED
```

Stop.
