# Reproduction and preservation

This run uses the unchanged `coarse-double-branch` at HEAD `fea2a25b05e97f726b6e1891cebb12c4cfca821a`, with clean tracked status. All sources, tests, configuration, existing research and Git are read-only. New output stays in this fresh append-only directory.

The old KC source table and relation are hash-pinned:

|Input|SHA-256|
|---|---|
|source_transition_table.json|2b5721768b2f88d66da6940de68406f8c534ae3482a3ec4c5781323dba406198|
|reachable_relation_certificate.json|30d1d724817d3f2ecb5a687428793a62d0b275d0195932adc3ad4f322ff839f9|

The EC capacity labels, source audit, old manifest and the established reset-input record are also pinned. There is no new source-table generation or engine import. The old source table already independently executed every required ordinary and reflected context.

To reproduce without overwriting history, copy only NI00 and the new scripts into a fresh versioned sibling directory under the same parallel-research parent. Read NI00, then run from the repository root:

    python -X utf8 -B <fresh-directory>/audit_return.py
    python -X utf8 -B <fresh-directory>/independent_verify.py

All output uses exclusive creation; do not rerun writers in the completed directory. The Python standard library is sufficient, no dependency is installed and no bytecode is written. The first script pins all inherited source/prior files and Stage11G, enumerates the fixed local predicate and constructs the exact word. The independent script imports no producer and rebuilds the local classification, source compositions, both orientations, all-m seams and the physical cut.

After validating results, place checked reports and ledger in the fresh directory and run its `seal_delivery.py` once. The entry pin count in this delivery is862; a later reproduction may inherit additional completed runs and must report its actual count. The sealer checks exact old research inventory, all125 Stage11G files, all prior/source hashes and unchanged Git state, then writes the final integrity record and manifest exclusively. The manifest hashes every artifact except itself.

The principal deliverables are NI01(the explicit word and proof), `uniform_nowhere_identity.json`(all-m identities), `full_source_replays.json`(actual trees and events in both orientations), `immediate_helper_cut.json`(the25-to24 restricted cut), and `independent_audit.json`(10,706 passing checks and hashes). FI/UD protocol classification and universal CD are not outputs of this reproduction.
