# Reproducing the fixed subtree set audit

No packages are installed. The producer and independent verifiers use Python's standard library and the existing frozen source engines. Run from the repository root with Python -X utf8 -B. The original execution order was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/audit_clade_correction.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/independent_verify.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_clade_correction_20261031_v001/verify_sharp_bound.py
```

The scripts create output files exclusively. Do not rerun in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH and use its path in the invocations. Keep the old route_c_alignment_20261031_v001 and route_c_analytic_20261030_v001 input directories in place. The producer checks the tracked tree is clean and records source hashes before evaluation.

Only nine fixed source controls at n=6 or 7 are evaluated, together with a seventeen-access n=6 word. No complete tree corpus or pair graph is generated. The n>=6 failure and scalar exclusion come from the exact parity formulas in CC03, not increasing finite fits. The arbitrary-fringe helper result follows directly from the all-size sharp bound, not an enlarged helper sample.

clade_correction_countercertificate.json contains full source trees, exact key sets, grouped oriented events, primitive rotation snapshots, rational G and R values and the complete original closed replay. independent_verify.py checks those data with independent rank-interval and depth arithmetic. right_vine_closed_rotation.json indexes a cyclic permutation of the same verified replay starting and ending at the right-vine diagonal. sharp_bound_audit.json verifies its composition and the sharper bounds on the same source edges.

entry_source_pins.json records eleven inherited inputs, HEAD and branch. additional_source_pins.json pins the helper-family source read during the audit. final_integrity.json compares all twelve hashes and the tracked Git state at delivery. delivery_manifest.json hashes the new artifacts and excludes itself. Existing proofs, source engines, research failures, graph data, Stage 11G assets and proof statuses remain read-only.
