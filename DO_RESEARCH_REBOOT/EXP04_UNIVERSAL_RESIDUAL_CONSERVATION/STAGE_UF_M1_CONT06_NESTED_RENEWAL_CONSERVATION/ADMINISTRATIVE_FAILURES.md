# Verification implementation correction

The first finalization run failed at a direct Python equality assertion between an in-memory original predecessor record and its saved JSON representation. The in-memory record has tuples for original IDs; JSON has lists. The full first script is preserved as finalize6_v1_failed.py, and CPU_finalization.json retains its failed measured run. It stopped while reconciling the first fresh source and never wrote a seal.

The correction compares canonical serialized digests of those two original records, matching the stage's existing source-scoped JSON identity convention. It still checks every original field and does not change source data, the physical engine, original predicates, frozen payments, mathematical assumptions or counterexample scope. The independent offline predecessor implementation is also rerun. Later receipts use versioned filenames. Every failed/duplicate measured run contributes to the resource total.

Read-only guessed directory and filename lookups also missed before inventory supplied the correct paths. Those produced no files. A single short independent55-key local/predecessor prototype command was unmetered; its results are rerun in the metered finalizer and its scope is disclosed in RESOURCE_RECORD. No historical file or Git tracked byte was changed.
