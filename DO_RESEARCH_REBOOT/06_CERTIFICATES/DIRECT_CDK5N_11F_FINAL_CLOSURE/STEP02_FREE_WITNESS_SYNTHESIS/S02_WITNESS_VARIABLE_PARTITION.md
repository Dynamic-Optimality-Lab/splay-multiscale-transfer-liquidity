# S02_WITNESS_VARIABLE_PARTITION.md — Groups I/II/III (Gate A)

- Group I (295, pinned): SLs_*/SLt_* abstract endpoint fields (mu, B-skeleton refs,
  A-shadow kinds/S-labels/indices, fringe signature) + SL_w requested weight.
- Group II (9249, hidden): SL_H, SLbt_q, event count/modes/targets/depths/paths
  (SLw_*), prefix slots/ports/ranks/bounds (SLv_*), B-trace (SLbt_*), shadow
  structures (SLsb*), inventory auxiliaries. Derived by search, never assumed.
- Group III (solver-internal): Z3 declarations, skolem constants, learned clauses.
  No original-state content.
Machine census: S02_PIN_AUDIT.json (`group1_n: 295`, `group2_n: 9249`).
