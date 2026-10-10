# DIRECT-CDK5-LOW gate report — CDK5L-A (PROVED)

## A. Repository identity and preservation

Branch `coarse-double-branch`, HEAD `9ec277c` (= banked ref) at start, clean
tree; all writes under `DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_CDK5_LOW/`
(+ 02_PROVED doc + this report); no source/banked file modified.

## B. HEAD and banked results

CDK4-A (K4-L1, pruning, 7-node, one-bit cert, B-cycle, class proof) + RT2-A +
AJ–AS/DIRECT-U1/DIRECT-CWC preserved with statuses; source hashes unchanged.

## C. Formal restricted theorem

|M|=5 ∧ ∀t |Core_M(B_t)|≤8 ⇒ Q_B≤2A (via Q_B≤2C_K≤2C_X≤2A).

## D. Gate-0 evidence

R1/R2/R3/R4 all PASS (frozen spec; nine-node complement real; mechanism
specified; single theorem; genuine witness). `GATE 0: PASS — AUTHORIZED`.

## E. Strict-class separation

Nine-node witness (core 9, Q−2C_K=+2): inside five-key frontier, outside
CDK5-LOW, B-only uncertifiable there. ≤8 class nonempty (five-key witness,
core ≤7).

## F–G. Source definitions + rotation audit

KEEP/DELETE/a/q/closure per source; K4-L1 single-rotation lemma re-verified
as stated (pivot-subtree argument, arbitrary M).

## H–J. Nine-bound, conservation, key-set change

1+4·2=9 proved (growing-set induction + closure rotation; tight); sizes
constant on closed fixed-M cycles; label swaps refuted-as-constant and handled
by full enumeration + canonical compression.

## K. Pruning commutation

Banked (marked x, arbitrary M); applied to project every KEEP to a graph edge.

## L–O. Graph, inventory, totals, weights

Raw 449,615 (210/3960/45045/400400) → 28,477 valid vertices → 142,385 edges
(54,670 drops); weights exact ints from pre-depths; both engines agreed on all
raw transitions (0 mismatches).

## P–Q. Algorithm + certificate

SPFA longest-path (148,675 relaxations): potentials in {0,1}, 0 violations;
no positive cycle. Independent verifier (tuple-engine-only re-derivation):
vertex set, 28,477 edges, all inequalities PASS.

## R–U. Engines, projection, telescoping, A-charging

Covered above; Q_B≤2C_K≤2C_X≤2A with exact seams; zero-A agreement.

## V–X. Status, novelty, regressions

CDK5L-A proved; five-key witness strictly outside all prior domains; nine-node
boundary control stands; no earlier theorem touched.

## Y. Artifacts, reproducibility, commit status

14 files under 06_CERTIFICATES/DIRECT_CDK5_LOW/ (+ scripts with logs) +
02_PROVED doc + this report; ledger + deps updated. Committed + pushed (SHA
verified below). Deterministic order throughout; exact integers only.

## Z. Final verdict and STOP

```text
CDK5L-A — PROVED; five-key ≤8-core obligation eliminated; nine-core OPEN;
K≥6 OPEN; universal Coarse-Double OPEN; DO OPEN. No CDK5-NINE/CDK6/universal.
STOP.
```
