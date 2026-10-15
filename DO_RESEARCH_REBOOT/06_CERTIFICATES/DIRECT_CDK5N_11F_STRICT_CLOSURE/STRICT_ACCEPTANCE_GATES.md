# STRICT_ACCEPTANCE_GATES.md — SC01-SC25 (no CONDITIONAL/PARTIAL passed as PASS)

| Gate | Status | Evidence or blocker |
|---|---|---|
| SC01 entry/sources | PASS | STRICT_SOURCE_AUDIT.md (HEAD 52778b8, 4/4, Bank25@25, freeze) |
| SC02 action grammar | PASS | PC_EFFECTIVE_MACRO_GRAMMAR (imported) + STRICT_ZERO_COST_NORMAL_FORM (corrected proof + 60/60) |
| SC03 same KEEP identity | PASS | STRICT_KEEP_IDENTITY_THEOREM + circuit binding + adversarial rejections |
| SC04 root-terminated paths | PASS | STRICT_ROOT_PATH_THEOREM + circuit + adversarial rejections |
| SC05 zero-cost normal form | PASS | corrected proof + executable + preservation fuzz |
| SC06 B-core validity | PASS | STRICT_B_CORE_VALIDITY + parent/connectivity + reconstruction + adversarial |
| SC07 boundary validity | PASS | 10-check predicate + realizability construction (STRICT_INVENTORY_SOUNDNESS A5) |
| SC08 authoritative alpha | PASS | STRICT_A_SHADOW_EQUIVALENCE (alpha-7 + beta-canonical; regression matching) |
| SC09 inventory/arithmetic | PASS | STRICT_INVENTORY_SOUNDNESS (cover/order/conservation/compat/widths; integer-room OPEN sub-point noted) |
| SC10 marked-core/q | FAIL | Universal monotonicity REFUTED (minimal admissible counterexample); C_M=S REFUTED (admissible boundary); fringe-q OPEN. Marked-splay monotonicity PROVED (partial, insufficient). HARD STOP. |
| SC11 cost accounting | PASS | terminal-genuine-only q (A8 discipline); D(q)=0; intermediate genuine prohibited+tested |
| SC12 high-cost midpoint | OPEN | WQ import stands; witnessed-q repair DESIGNED but UNBUILT (stopped at SC10) |
| SC13 port low relation | PASS | STRICT_LOW_COMPILER (repaired relation; 108 grounded; adversarial green) |
| SC14 T=266 | PASS | PC_266 audit imported + 13-ledger stands; per-edge/per-walk distinction kept |
| SC15 126 masks | PASS | imported 126/126 SAT+transitions (parametric var; no rebuild needed) |
| SC16 saturated sigs | PASS | sig 10x0..266 parametric; min-count construction imported |
| SC17 repaired product | PARTIAL | low relation recompiled+verified (1,400,302 nodes); FULL product (high+operators) NOT recompiled (stopped) |
| SC18 quantifier semantics | PASS | imported backend + binder/hygiene tests (no change; execution semantics intact) |
| SC19 free-witness SAT | OPEN | predecessor UNKNOWN stands; no new synthesis attempted (stopped) |
| SC20 full-domain decision | OPEN | depends on SC19 + SC10 |
| SC21 production Pre/Post | OPEN | predecessor constructed; NOT re-certified against repaired relation (stopped) |
| SC22 MinPre | OPEN | same as SC21 |
| SC23 DAG <=4M | PASS | repaired low 1,400,081 (STRICT_DAG_SIZE_CERTIFICATE.json); full product not rebuilt |
| SC24 simulation | OPEN | representative-level proof stands; item 9 conditional on OPEN fringe-q (unchanged) |
| SC25 verifier/repro | PASS | this campaign: repairs verified (grounded+adversarial+monotonicity); commands recorded |

First failing gate: SC10 (REFUTED premise + OPEN correspondence). Verdict: OUTCOME E. HARD STOP.
