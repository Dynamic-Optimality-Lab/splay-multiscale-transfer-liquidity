# PC_EFFECTIVE_MACRO_GRAMMAR.md — bounded effective H≤2 macro grammar (§8, G02)

## Source facts
Zero-cost access ⟺ d_A = 0 ⟺ target is the current A-root (frames empty ⇒ `_rebuild` identity; A-side no-op). DELETE: A-splay + B untouched. KEEP: A-splay + B-splay.

## Root-run collapse lemma
Consecutive same-target root accesses collapse to the first with identical (A,B) trajectory: after the first, the target is root in A (A-identity thereafter); if it was a KEEP, the target is also B-root (B-identity thereafter); DELETEs never touch B. Hence every subsequent same-target root op is a FULL no-op (both trees). Dropping them preserves source/destination boundaries, H (=0 contributed), q (no B change after the first), and B-controller behavior exactly.

## Bounded normal form
In an H≤2 macro: non-root accesses have a≥1 each ⇒ at most 2. Root-runs (maximal consecutive d_A=0 runs) each collapse to ≤1 event by the lemma; runs are separated by non-root accesses ⇒ at most 3 runs (before/between/after ≤2 non-roots). Effective word length ≤ 2 + 3 = 5 events. Each event: (K/D) × exposed target (all low-cost targets exposed by §5: d≤4<7) + terminal genuine-KEEP configuration (marked target, q from B-depth per C2).

## Coverage (§8 checklist)
KEEP ✓ (events); DELETE-then-KEEP ✓ (D/K event pairs); multiple DELETEs within H≤2 ✓ (each a≥0 counted; D-flags preserved); zero-cost DELETE normalization ✓ (root-run collapse; non-root DELETEs kept exactly); zero-cost KEEP behavior ✓ (root KEEP kept as ≤1 event with exact B-update); nongenuine KEEP behavior ✓ (B-splay executed, marked-change absent — B-controller exact); every legal terminal KEEP configuration ✓ (genuine marked target + source q). Exhaustiveness is PROVED (counting argument above), not inferred from observed sequences.

## Gate G02: PASS (grammar) — executable normalization in PC_ROTATION_INTERPRETER.py (root-run collapse pass + 5-event bound enforcement).
