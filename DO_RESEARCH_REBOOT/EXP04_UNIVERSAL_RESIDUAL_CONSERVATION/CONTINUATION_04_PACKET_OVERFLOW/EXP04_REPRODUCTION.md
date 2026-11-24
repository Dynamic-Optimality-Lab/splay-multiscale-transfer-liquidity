# Reproduction and preservation

Run with existing Python and -B from an isolated NEW sibling of this
directory under EXP04_UNIVERSAL_RESIDUAL_CONSERVATION. Keep this sealed
delivery and all older checkpoints immutable. Copy these Python scripts
into that sibling; campaign4.py resolves the existing C3B/C3/C2/C1 readers
and redirects producer ROOTs only in memory. No installation, Git mutation,
external account change or modification of historical proofs is needed.

Repository HEAD6d532b2c795c0778f57d8023b23b5fedfc48b010,
branch coarse-double-branch. Preservation is rechecked transitively.

Fresh full run, in this order:

    python -B campaign4.py
    python -B verify_storage.py
    python -B width_attack.py
    python -B packet_geometry.py
    python -B same_side_batch.py
    python -B structural_checks.py
    python -B failuremode_checks.py
    python -B verify_width.py
    python -B trace_replay.py
    python -B export_checkpoint.py
    python -B finalize4.py

Supply the accompanying reports/ledgers before finalization in the fresh
directory. Producing stages replace their own generated files there.
width_attack writes the1027/2051-key family records; structural_checks
writes the1025-key A-spine control separately; export_checkpoint unifies
all three in SOURCE_WITNESSES.json after verification. Do not append the
spine source to the width results or treat its unrun Pi as zero.

The default verification replays original R_* selectors again. The saved
run also has a recovery command:

    python -B verify_width.py --reuse-primary-selection

The prior full selection had already reproduced exactly before the
independent primitive checker hit Python's default recursion limit. The
recovery raises ONLY the local runtime recursion limit to10000. It freshly
replays the complete original source, binds the exact primitive hash, all U
and all original pairs using canonical JSON normalization, then recomputes
the independent primitive SET/Pi/U and separate cohort/R6 checks. No saved
independent phase is substituted. The completed original selectors remain
the pinned primary implementations; an independent implementation of every
historical selector is not claimed. A preempted tuple/list controller check
and its qualified missing CPU measurement are retained in the resources.

packed_states.py stores exact full child-pointer dictionaries as lossless
integer-backed mappings, implements canonical serialization, and updates
subtree labels only at the two actual rotating vertices. Old label
dictionaries stay immutable for pre-state comparisons. verify_storage.py
compares dense and adapted original replay through every complete boundary,
primitive event, U, pair, canonical state hash and original R_* selector on
small complete controls. The large separate immutable primitive checker is
the further SET/Pi check. No original predicate or physical key is removed.

ORIGINAL_EVENT_TRACE.json is a LOSSLESS delta encoding, not an omitted
physical witness: it contains the complete source/initial pair, ALL actual
primitive rotation IDs, pivots, middle/external attachments, deleted/added
edges, full SET labels, signs and original operation phase offsets/paths.
Starting from the full labelled initial pair, these deltas uniquely recover
every full A/B state at every primitive and boundary. TRACE_CHECK.json
checks that reconstruction and the stream hash. The source contains both
full final labelled dictionaries; exact closure is independently verified.
No original occurrence is renumbered, filtered, or reclassified on a shadow.

The new exact obstruction's five critical gaps are in the certificate and
COUNTEREXAMPLE_LEDGER. PACKET_GEOMETRY.json includes full A components and
ALL actual cyclic ancestry changes/demotion bits for its three grandparents
against the critical target. PHYSICAL_PACKET_LIFECYCLES also pins the
unchanged577-key repeated-grandparent witness. No ancestry reappearance is
automatically treated as new A work.

All arithmetic deciding eligibility is integer exact. Positive old raw
periodic certificates put these sources in the periodic source case;
the fallback all-local-arc case is inactive for their exact H_all partition.
No negative all-cuts or all-interval certificate is claimed. New source
parameterization proves legality/closure for unbounded support, not an
all-parameter original Pi/width formula.

finalize4.py validates all deliverables, original IDs, independent-check
counts, accounting identities, resources and old manifest hashes, then
seals every new file except its own delivery manifest. Wait for every run
to finish before sealing; do not write logs afterward. CPU receipts include
failed runs. RESOURCE_RECORD distinguishes measured CPU, the interrupted
phase's conservative bound and unmetered startup/inspection costs; it is
not falsely presented as exact total campaign CPU or an observed host quota.
