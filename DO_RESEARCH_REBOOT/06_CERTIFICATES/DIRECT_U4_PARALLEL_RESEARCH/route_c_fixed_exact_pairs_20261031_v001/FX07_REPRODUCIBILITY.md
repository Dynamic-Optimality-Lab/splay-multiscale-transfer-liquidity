# Reproducing the fixed exact pair audit

The scripts use Python's standard library and the frozen source engines. No packages are installed. From the repository root, the original invocations were

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_fixed_exact_pairs_20261031_v001/audit_fixed_pairs.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_fixed_exact_pairs_20261031_v001/independent_verify.py
```

Outputs use exclusive creation. Do not rerun in this populated directory. To reproduce, copy these scripts and helper_boundary_certificate.json into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH and substitute its path in the invocations. Preserve the prior E, F and analytic input directories.

The primary audit evaluates one n=6 opposite-vine access, both helper branches at m=0 and m=1, the two reflected m=0 helpers, and one fixed n=6 hook-vine safeguard. It then uses one single-tree n=6 BFS only to locate a DELETE prefix for an explicit closed witness. There is no potential fit, larger tree corpus, source-state pair graph or parameter search.

fixed_exact_pair_certificate.json saves the complete trees, a,q,z and oriented source events; all exact common pairs; the residual graph for each distinct evaluated pair; and a matching plus equal-size cover proving every residual maximum. It also includes the full fourteen-operation paired replay.

helper_boundary_certificate.json is a SYMBOLIC five-core-vertex/port certificate. independent_verify.py checks all four reductions with distinct fringe extrema, coincident extrema and the empty substitution, and verifies the actual core endpoint tables in the fixed source controls. These checks support the structural proof in FX03; they do not enumerate or fit arbitrary fringes. The only rank inequality for the unknown-size interior is the proved one-added-vertex lemma, valid for every finite graph.

The independent verifier does not import the producer or invoke a matching algorithm. It regenerates residual graphs, checks all forced exact pairs, validates matching/cover equality, replays the pointer source and checks exact full paired closure. independent_audit.json is its PASS record.

entry_source_pins.json records fourteen inherited inputs, HEAD and branch. integrity.json checks them after the source audit. final_integrity.json checks them again at delivery and validates report/certificate links. delivery_manifest.json hashes every new file except itself. Existing research, sources, solver data, Stage 11G assets and proof statuses remain read-only.
