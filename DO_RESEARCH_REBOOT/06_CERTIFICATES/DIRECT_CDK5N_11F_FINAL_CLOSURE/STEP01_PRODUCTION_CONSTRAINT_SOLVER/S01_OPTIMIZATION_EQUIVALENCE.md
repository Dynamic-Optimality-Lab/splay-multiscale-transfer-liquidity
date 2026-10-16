# S01_OPTIMIZATION_EQUIVALENCE.md — reproducible optimization ledger

Only semantics-preserving transformations are used. Each entry: change, equivalence
argument, regression, measured effect.

## O1 — Structural hash-consing reuse (compiler)
- What: one Z3 expr per DAG node id (`cache: nid -> expr`); shared subgraphs
  translated once. No formula regeneration per weight (weights are assumptions).
- Equivalence: identical node = identical subexpression by hash-consing definition.
- Regression: S01_FULL_PRODUCT_BUILD sharing factor (parent_links/cone_nodes =
  measured in JSON); 150/150 agreements computed through the shared cache.
- Effect: low cone 1,384,795 nodes -> 9544 decls; translate ~50-72 s one-time.

## O2 — Exact Tier-1 pre-simplification (solver)
- What: historical exact `simplify` under call pins before Tier-2; decides const
  roots without Z3.
- Equivalence: constant folding only (proved rules per connective); pins are
  asserted equalities; free occurrences inside binders fold correctly as free refs.
- Regression: S2-S4 (SAT==ground truth), S5 (4/4 rejections incl. flipped-H).
- Effect: grounded queries ~2.5 s vs Tier-2-only >120 s UNKNOWN (measured 277 s CPU
  `canceled` on the same query). Cost: one cone scan per query (~3 s at 1.4M).

## O3 — Minimal privatization (frontend)
- What: duplicate only boundary-shared scope-carrying nodes (usually zero: low/high
  roots have 0 binders, growth 0; Q3-shape +5 nodes).
- Equivalence: pure alpha-renaming (scope theorem); growth recorded per compile.
- Regression: Q8 verdict-stability + Q2/Q3/Q6 oracle agreement.
- Effect: measured `norm_growth` per handle (0 on production roots).

## O4 — Z3 internal preprocessing + learning reuse (backend property)
- What: no custom rewriting; Z3 simplifier/preprocessing + clause learning across
  `check(*lits)` calls and push/pop sessions.
- Equivalence: backend-internal, sound by Z3; statistics recorded, not trusted blindly
  (every SAT model independently re-checked by oracle + interpreter on grounded cases).
- Effect: recorded per-handle statistics (conflicts/propagations) in metrics JSON.

## Explicitly NOT done
No constraint removal, no domain restriction to samples, no mask reduction, no
witness assumption, no UNKNOWN coercion. The endpoint-only preview stays UNKNOWN at
60 s — reported, not optimized away.
