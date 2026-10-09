# StepEv-to-LT cost translation

STATUS: CONDITIONAL on E_B≤C S_A+g; implication proved by elementary inequalities. The existing Lean file contains the same arithmetic implication, but it was not compiled during this run.

Depth d counts edges, StepEv cost e(d)=ceil(d/2)=floor((d+1)/2), and LT splay cost is d+1 (transition-tree size). For every d≥0, d+1≤2e(d)+1 and e(d)≤d+1. Pair Access for a retained subsequence Y of X starts from the same T0. For P_all, S_A counts every A StepEv and E_B counts every retained B StepEv. Therefore LT(Y)≤2E_B+|Y|, S_A≤LT(X), and |Y|≤|X|≤LT(X). For a universal C≥0,

\[
E_B\le C S_A+g\ \Longrightarrow\
LT(Y)\le(2C+1)LT(X)+2g.
\]

At C=3 this is the intended factor 7. All constants refer to this LT model; literal search-plus-rotation accounting is only equivalent up to constants. There is no absent-key extension here.

Source: lean/WP6/GCStaticKeep2Step.lean:703-716 (stepev_lt_upper, stepev_le_lt, cost_translate); python/liquidity/legacy_embedding.py:71-74; artifacts/v04/wp6_present/present_domain_audit/pair_access_domain_mapping.md:1-42. Counterexample history: the repository's broader absent-key liquidity route is separate and cannot be substituted for the present domain.
