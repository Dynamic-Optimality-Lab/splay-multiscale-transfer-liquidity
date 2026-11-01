# Reproducing the bounded root alignment audit

The scripts use the Python standard library and the existing frozen source engines. No dependency installation is required. From the repository root, the original producer invocation was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_alignment_20261031_v001/verify_root_aligned_repair.py
```

The independent verifier invocation was

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_alignment_20261031_v001/independent_verify.py
```

Both scripts use exclusive creation for their outputs. Do not rerun them in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling directory under DIRECT_U4_PARALLEL_RESEARCH and invoke the producer, then the independent verifier there. Keep the prior route_c_potential_20261031_v001 input directory in place. The producer also checks the tracked tree is clean; neither script changes it.

The proof files AL01 through AL03 are analytic. Their universality is proved by the binary mass bound, the source displacement bound and two fixed symbolic source operations, not by extending the six-key computation. In particular, n>=13 is derived algebraically. No n>=7 corpus is generated.

root_aligned_countercertificate.json records all changed metric data, exact values, source edges and complete closed replay. The inherited 132-tree/660-arc metric corpus is referenced by filename and pinned hash in entry_source_pins.json. independent_verify.py independently validates the inherited arcs, both distance rows, all 396 candidate scores, all six maxima and all oriented source replay events. independent_audit.json is its saved PASS result.

entry_source_pins.json records ten original input hashes and the actual HEAD and branch. additional_source_pins.json pins the displacement proof used during this audit. external_source_record.json identifies the primary reachability theorem. final_integrity.json compares the pinned inputs and Git state at delivery. delivery_manifest.json hashes the delivered files, excluding itself. Existing source, reports, failures, Stage 11G assets, and proof statuses remain read-only.
