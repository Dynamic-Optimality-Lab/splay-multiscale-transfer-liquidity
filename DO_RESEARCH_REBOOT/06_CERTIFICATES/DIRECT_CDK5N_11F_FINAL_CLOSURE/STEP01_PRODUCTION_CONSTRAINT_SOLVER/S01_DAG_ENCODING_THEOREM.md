# S01_DAG_ENCODING_THEOREM.md — translation preserves truth

## Claim
For every supported DAG root R (Bool) and every total assignment ρ respecting width
domains, `Truth_DAG(R,ρ) = Truth_Z3(compile(R),ρ)`.

## Proof (structural induction on the normalized cone)
- Leaves: Bool/Int constants and variables map to identical values; Int bounds in the
  compiled conjunction exactly delimit the historical search domains, and ρ respects
  them by hypothesis.
- Connectives/comparisons/ITE/arithmetic: each Z3 operator is the mathematical
  counterpart of the historical `ev_iter` clause over the same child values (Int
  arithmetic is unbounded on both sides — no wrap to diverge on).
- EXISTS B: normalization guarantees every B-bound var node occurs only inside B's
  body cone and no two binders share a bound name (validated). The single Z3
  declaration per bound name therefore denotes exactly B's witness variable;
  `Exists` is true iff some domain value satisfies the body — the V-semantics of the
  binder. FORALL dual. Vacuous binders (undeclared name, asserted non-occurring)
  compile over Bool: nonempty domain + independence => identity on both sides.
- Normalization itself is pure alpha-renaming (REPLACE-not-add on a per-name-uniform
  basis: one var node per name => all-or-nothing renaming per (binder,name); see
  scope theorem), hence truth-preserving.

## Empirical side
150/150 exhaustive small-domain agreements + 12 adversarial + Q1-Q8 + 3 grounded
production agreements (compiled SAT + oracle witness + interpreter, all True).
