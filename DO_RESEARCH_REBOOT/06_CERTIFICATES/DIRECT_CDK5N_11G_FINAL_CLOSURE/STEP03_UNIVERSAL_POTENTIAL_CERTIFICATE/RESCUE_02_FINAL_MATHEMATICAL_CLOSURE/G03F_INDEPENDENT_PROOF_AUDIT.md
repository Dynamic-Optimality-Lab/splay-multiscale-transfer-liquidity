# G03F Independent Proof Audit

Independent verifier (fresh process, separate BF/canon/rank
implementations): F01–F15 all PASS (entry, hashes, query budget,
empty-return honesty, controls, joint-LP recompute, guard purity, killer
confirmation, no false certification, hunt recompute, open-deps explicit,
verdict intact, caps). Dependency graph (`G03F_THEOREM_DEPENDENCY_GRAPH.json`):
proved {return-path equivalence, chaining soundness, BF/SCC correctness,
joint-LP telescoping-by-construction, guard vertex-purity};
evidence-only {183 closed walks ≥ +2, witnessed acyclicity};
explicitly OPEN {universal-Vw, A/B-credit lemmas, symbolic returns}.
No bounded observation used as universal premise; no source-only q
restriction imposed; UNKNOWN maintained as UNKNOWN throughout.
