# Reproducing the fixed endpoint matching audit

Use the existing Python standard library and frozen source engines; no packages are installed. From the repository root the original invocations were

```powershell
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_endpoint_matching_20261031_v001/audit_endpoint_matching.py
python -X utf8 -B DO_RESEARCH_REBOOT/06_CERTIFICATES/DIRECT_U4_PARALLEL_RESEARCH/route_c_endpoint_matching_20261031_v001/independent_verify.py
```

Outputs use exclusive creation. Do not rerun in this populated directory. To reproduce, copy the scripts into a fresh versioned sibling under DIRECT_U4_PARALLEL_RESEARCH, preserving the prior route_c_clade_correction_20261031_v001 and route_c_analytic_20261030_v001 input directories, and substitute the new directory in the commands.

Only two opposite-vine accesses at n=6,7 and the first empty-fringe six-key helper are tested as candidate controls. Once that helper fails, the producer reuses the saved eleven-operation six-key source word from the earlier analytic audit. No connector BFS, new source-state graph, enlarged corpus or potential fit is performed.

endpoint_matching_countercertificate.json records every full source state and oriented event, all exact graph vertices and adjacencies, and a matching plus equal-size vertex cover for every distinct evaluated graph. independent_verify.py regenerates the graphs and checks those certificates without invoking a matching solver. It verifies the hand-readable helper certificate and the complete closed replay independently through the pointer source engine.

The analytic proofs EM01 and EM02 establish the universal DELETE law and all-size opposite-vine law. The finite checks do not replace their quantifiers. EM03 is an exact in-domain refutation of helper preservation, since the arbitrary-fringe contract includes m=0. No claim is made about every nonempty fringe.

entry_source_pins.json records fourteen inherited file hashes, HEAD and branch. integrity.json checks them after source evaluation. final_integrity.json checks them again at delivery and validates saved reports and certificates. delivery_manifest.json hashes the new output files and excludes itself. The prior certificates, source engines, old research, Stage 11G assets and proof statuses remain read-only.
