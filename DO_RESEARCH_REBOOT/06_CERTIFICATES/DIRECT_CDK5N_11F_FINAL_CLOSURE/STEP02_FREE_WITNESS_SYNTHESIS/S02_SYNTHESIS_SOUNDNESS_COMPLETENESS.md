# S02_SYNTHESIS_SOUNDNESS_COMPLETENESS.md — Gate J proof obligations

## Soundness (SAT => full original relation + source replay)
Every SAT passes, in order: replay success (authoritative forward simulator),
A-depth/q filters (relation-entailed), ssertify `ok` (full relation SAT on the
candidate env), abstract-match (derived s/t pins == query pins), Tier-1 SAT on the
shared production handle, 18-item certificate extraction (all asserts), independent
fresh replay agreement. A SAT verdict is never issued from a projection.

## Completeness (where it is claimed)
- B-word space: exhaustive to depth 5 (deterministic transitions; visited prunes
  only exact redundant revisits). H/q splits cover all consistent pairs.
- Negatives N1-N5 UNSAT are B-level/validation exclusions (empty word space or
  violated necessary condition) — complete reasoning, no search needed.
- EXPLICIT LIMIT (recorded, not hidden): A-shape completion (insertion orders) is
  ordering-bounded, not Catalan-exhaustive. A-level exhaustion therefore yields
  UNKNOWN (`a-incomplete`/`word-truncated`), never UNSAT. UNSAT is claimed only
  for B-level/validation exclusions. Global A-contingent UNSAT is out of Step-02
  scope (documented limitation for Steps 03+ or symbolic fallback).

## No fixture leakage
Candidates derive from query pins only (BFS + canonical completion + replay).
Recovered words/keys differ from fixtures (e.g., canonical keys 300/700 vs
fixture 6/7); H/q are measured, never copied. Corpus methodology: fixtures
supply query pins only; engine never sees witnesses.
