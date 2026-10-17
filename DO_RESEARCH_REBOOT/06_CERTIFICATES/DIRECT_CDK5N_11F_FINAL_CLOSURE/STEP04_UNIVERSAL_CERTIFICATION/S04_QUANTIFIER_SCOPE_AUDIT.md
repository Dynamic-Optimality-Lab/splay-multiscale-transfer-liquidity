# S04_QUANTIFIER_SCOPE_AUDIT.md — F04-21 (Gate B re-audit)

Lexical scopes with per-binder unique ownership (privatization validated per
root: pairwise-disjoint bound names + cone containment, FAIL CLOSED). In-scope
finite-domain bounds at every quantifier (B1 repair, re-verified). Vacuous
binders sound (nonempty default domains). Nesting via canonical renames with
position discipline (post namespace defect found + fixed). Two capture defects
found by oracle, repaired additively in Step 03, re-verified (4070 + production
scope tests + 23 projections normalize clean on fresh rebuild). No global
name-stripping anywhere in the frozen path.
