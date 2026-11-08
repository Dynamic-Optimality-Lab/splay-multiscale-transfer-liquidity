# Implemented IAGS-R contract

Each Box in proof_boxes.json records target T, hypotheses H, inherited I,
unresolved children U, parent implication Lambda, measure D and the dual.
Allowed statuses are exactly PROVED, REFUTED, ACTIVE, BLOCKED, or
SUPERSEDED BY PROVED STRONGER LEMMA. Verification status is separate.

Proof routes are alternatives; children on one route are conjunctive.
ROOT35 can be closed by a source proof of PEEL35, or by excluding every
MIN35-normalized countercut, or by the exhaustive source partition into
zero/one/multiple-interior coalitions. Optional routes are not silently
declared necessary assumptions. No graph certificate implies Bank25.

Actual decreases: REM35 deletes a selected macro IF its private capacity
suffices; connected splitting decreases macro count; DELETE-LOOP35
decreases source length while preserving positive deficit. Lexicographic
(|S|,|W|) is well-founded. SHALLOW35 uses a complete three-case source
split, not an infinite helper catalogue. Fixed-source CORE35 termination
is a separate finite algorithm theorem and is not universal source closure.

Reconstruction is attempted after every closed Box. Its exact failure is
retained in C35_ROOT_RECONSTRUCTION.md. A remaining inequality equivalent
to ROOT35 is not renamed as a smaller atomic child. In particular the
promise that every negative set has a smaller negative set is not used
as an assumed source lemma.

The recursion stops a proposed decomposition when it has no proved
descent or complete reconstruction. It does not stop at a positive
restricted case and call that A-SI34. Current unresolved mixed-birth
source compatibility has no further justified decreasing reduction here;
its precise statement, failed routes and dual are COMP35/REAL35.
