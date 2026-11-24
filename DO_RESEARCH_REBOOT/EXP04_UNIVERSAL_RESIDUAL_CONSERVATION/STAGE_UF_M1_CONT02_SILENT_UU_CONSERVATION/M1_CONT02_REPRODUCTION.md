# Reproduction and evidence map

Run with Python3.13 and -B from this continuation directory. All old source modules are read-only. No installation, network, Git mutation or subagent is required.

## Delivered seal, read-only

    python -B finalize2.py --verify-only

This verifies the exact delivery file inventory/hash set, all14 required artifacts, C1/M1/M0 and full transitive pins, HEAD/branch and unchanged tracked files.

## Experimental reconstruction

Writer scripts should be run only in a fresh isolated sibling, copying this stage's .py sources and retaining parent layout. Do not rerun writers in the sealed delivery. Run sequentially:

    python -B base2.py
    python -B audit2.py
    python -B audit_variants2.py A
    python -B audit_variants2.py B
    python -B account2.py
    python -B inherit2.py
    python -B boost2.py
    python -B expand_events2.py --audit
    python -B fan2.py

audit2 is deliberately the original failed all-L candidate. It writes its completed L1 control, then stops at the L2 R6 assertion. Preserve its failure; proceed with the explicitly versioned scripts that record all original candidates and the repaired odd-L theorem. Do not edit it into a passing test.

The final script sequence may use different CPU/wall timings. Original reported resource receipts include failed and duplicate audits. Import/inspection/prose/manifest overhead is separately disclosed; resource limits are not mathematical hypotheses.

## Exact long original events

BOOST_SHORT_PHYS contains the complete independent short event stream and collision-free full A/B state pool. BOOST_EVENT_EXPANSION gives exact primitive and operation-ID shifts for repeated two-zig copies. To materialize every long primitive to a new path:

    python -B expand_events2.py --jsonl ORIGINAL_LONG_EVENTS.jsonl

Do this in the fresh sibling, not the sealed delivery. EXPANDED_EVENT_AUDIT gives its canonical JSONL hash,622928 real primitive events,314555 original actual A StepEv and4324 B doubles. Repeated template events are actual original occurrences with distinct IDs, not virtual A resources.

## Evidence files

INHERITED_SOURCE_CATALOG/INHERITED_SIGNATURE_RESULTS:52 complete sealed sources, all referenced hashes, original known-R_* signatures, pre-A physical paths and exact current-zero reasons.

NEW_SOURCE_CATALOG and NEW_*_00: original six all-L candidates and first completed control before the failure.

RUN_A_SOURCE_CATALOG/RESULTS and RUN_A_PHYS/FOREST/WEIGHTS/M1_AUDIT/BIRTH_00..05: complete original all-L audit, including parity failure.

RUN_B equivalents: six odd-L/control sources, full original independent/native U/cohorts/R6 and explicit native R_* scope.

ORDERED_00..02 and ORDERED_RESULTS: exact carrier/skipped/E_old/periodic-H/D/quota assignments on three original native-R_* sources; counterfactual no-H pool labelled separately.

BOOST_SOURCE_CATALOG: both complete original short/long words, initial trees and legal prefix. BOOST_SHORT_*: full short physical/forest/Pi/R6. BOOST_LONG_FAST_STATES: every original long operation's B state/steps/guards and full-code pool. BOOST_EVENT_EXPANSION and EXPANDED_EVENT_AUDIT: lossless full original stream. BOOST_RESULTS: exact costs, scope and actual positive G/H certificates.

FAN_SOURCE_CATALOG/FAN_*: two complete local packing attempts and their actual cyclic Pi/creator failures.

SILENT_UU_SOURCE_WITNESSES: final canonical source/evidence/hash index. FINAL_VERIFICATION, RESOURCE_RECORD and M1_CONT02_DELIVERY_MANIFEST: scopes, resources, preservation and seal.

No native R_* null is interpreted as empty. The finite packing screen is not a theorem. The universal construction proofs, invariant-replication argument and OPEN conservation/transfer boundaries are in their named proof files.
