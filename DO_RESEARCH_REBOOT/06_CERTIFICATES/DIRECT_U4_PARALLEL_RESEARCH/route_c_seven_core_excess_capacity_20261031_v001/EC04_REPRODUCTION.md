# Reproduction and preserved sources

Repository: `splay-multiscale-transfer-liquidity-k6c2`, branch `coarse-double-branch`, pinned HEAD `fea2a25b05e97f726b6e1891cebb12c4cfca821a`. Existing source, tests, configuration, Git and previous research are read-only. All output files in this directory are exclusive creations.

The inherited source basis is the sibling directory `route_c_seven_core_return_obstruction_20261031_v001`:

|Input|SHA-256|
|---|---|
|source_transition_table.json|2b5721768b2f88d66da6940de68406f8c534ae3482a3ec4c5781323dba406198|
|reachable_relation_certificate.json|30d1d724817d3f2ecb5a687428793a62d0b275d0195932adc3ad4f322ff839f9|

The scripts use only the Python standard library. They import no repository module, run no source-table writer, create no bytecode and install no dependency. The old table already covers both orientations in actual thirteen-key source contexts; this run uses exact table composition rather than new engine calls.

Read the pre-execution gates before reproducing. To avoid overwriting history, copy only the new scripts and gate notes into a fresh versioned sibling directory and run from the repository root, in this order:

    python -X utf8 -B <fresh-directory>/analyze_capacity.py
    python -X utf8 -B <fresh-directory>/build_joint_return.py
    python -X utf8 -B <fresh-directory>/independent_check.py
    python -X utf8 -B <fresh-directory>/verify_event_units.py

Each generated output is opened in exclusive mode. Do not rerun writers in this completed directory. Copy reports and the ledger to the fresh directory only after checking they agree with its results. `seal_delivery.py` is a final exclusive integrity check and manifest writer after all artifacts are ready.

The producer computes SCCs by iterative Kosaraju. The independent checker validates each component by forward/reverse reachability and validates the quotient is acyclic. It reconstructs every source graph edge from the pinned table, then checks every concrete path, full source word, reflected event row, physical reset, cyclic block, helper-pair J calculation and all-m boundary condition. The separate physical-unit checker constructs and validates the explicit demand-to-unit injection without importing either previous script.

`full_source_replays.json` contains the full actual source and destination A/B trees for W and H_5, with mirrored replays. `uniform_return_identity.json` gives the all-m formulas and the complete34-row record for the optional fixed recurrent-input subcheck. `event_unit_injection_certificate.json` gives all176 distinct assignments. The final manifest hashes all deliverables except itself. `final_integrity.json` records preservation of all841 inherited source/prior files, the prior research inventory, HEAD/branch/tracked status, and all125 Stage11G files.

No FI/UD classifier, larger source fit, new post-reset relation or automatic follow-up is part of this reproduction.
