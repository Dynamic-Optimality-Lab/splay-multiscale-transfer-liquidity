# SHARP-01 reproduction and artifact map

Use the repository root on `coarse-double-branch`, HEAD
`6d532b2c795c0778f57d8023b23b5fedfc48b010`. Python standard library only.
No installation, old source engine, old audit controller or network is needed.
Run Python with `-B` to avoid caches outside this directory.

The complete finite corpus is in `SHARP01_SOURCE_WITNESSES.json`. Its exact
initial states, KEEP/DELETE words, explicit diagonal prefixes, metadata and
reflection/repetition identities are sufficient for independent replay. Source
IDs are names; operation and rotation IDs are local to those original words.

`SHARP01_GAP_LEDGER.json` indexes full chronological ledgers under `ledgers/`.
Resolve each tree reference through that ledger's `states` object. It records
every operation, StepEv, real rotation, terminal zig, physical middle transfer,
signed full-carrier SET change and cyclic gap. Prefix events are not period events.
No-KEEP sources have no gap and explicitly unpartitioned A, with Q=0.

Read `SHARP01_DISCOVERY_REPORT.md` for the precise scope of the refutations.
`SHARP01_RESULTS.json` contains all reduced-rational family summaries,
gap-level flow graphs and potential constraints. `SHARP01_PHYSICAL_INCIDENCE.json`
gives strict unit eligibility reasons, flows and deficiencies. `SHARP01_COUNTERCERTIFICATES.json`
contains independently reconstructed potential and Hall obstructions.

## Check existing saved results

From this directory, these bounded commands verify the saved records:

```powershell
python -B sharp01_tests.py
python -B sharp01_validate.py
python -B sharp01_certificate_check.py
```

They rewrite only their own NEW SHARP verification receipts. The first checks
222 primitive rotations, every small-H seam including physical bit records,
reflection, copies, empty/zero/no-KEEP cases. The second independently replays
all 79 sources and 25,807 operations and constructs cyclic gaps by a different
algorithm. The third independently evaluates refuting features, replays nine
large cyclic cuts and checks all 288 primitive ancestry changes of the C15
Hall witness before recomputing its first-return eligibility.

## Fresh measurement reproduction

Preserve this run. Create a NEW sibling versioned directory under
`DO_RESEARCH_REBOOT`, copy the `sharp01_*.py` scripts into it, and run there:

```powershell
python -B sharp01_tests.py
python -B sharp01_experiments.py
python -B sharp01_validate.py
python -B sharp01_unit_incidence.py
python -B sharp01_certificate_check.py
python -B sharp01_ancestor_episodes.py
```

The scripts locate repository inputs relative to a directory directly under
`DO_RESEARCH_REBOOT`; do not put the fresh directory one level deeper. A fully
standalone copy outside the repository can verify saved witnesses by using the
three check commands above; source generation needs the pinned C15 fixture files.
Seed is 20261110. Source parameters are explicitly enumerated in `corpus()`.
The generated source-word hash, totals, cases and complete tree endpoints should
match; timing/peak memory and provenance hashes of concurrently edited research
can differ. Different JSON spacing is immaterial. All costs use integers and
ratios use `fractions.Fraction`.

The report is the original campaign manuscript. `sharp01_write_report.py`
renders that manuscript and its original recovery narrative from these records;
it is not required to reproduce numerical findings in a fresh run.

The measurement run caps itself at 220 sources, 600 keys, 20,000 operations
per source and 600 process CPU seconds. The separate verification reserve is
120 seconds. These are new SHARP ceilings, never resets of historical budgets.
This is a finite selected corpus, not exhaustive CD(7) enumeration. A confirmed
positive complete-source deficit stops the driver and exports its complete ledger.

## Recorded recovery and limitations

The actual first run finished all sources but its final hash check detected an
external change to the unused original EXP01 source file. Exact first-run CPU
and peak memory were not persisted before that guard. This defect is disclosed
in `SHARP01_RUN_RECEIPT.json`; a conservative 600-second charge is retained.
The main driver now writes `SHARP01_PROCESS_EXIT_RECEIPT.json` in `finally` on
future runs. The current dataset is recovered from already-saved ledgers using
`sharp01_finalize_saved.py`, WITHOUT replaying any source, and then independently
verified. The recovery script requires the original saved ledgers and is not
part of the normal fresh-run sequence.

`SHARP01_INPUT_MANIFEST.json` records the original pins, concurrent provenance
changes, executed constructor snapshot and immutable-reference hash. Other
agents' later changes cannot be called SHARP edits. The newer Global Boundary
Reuse report stays BLOCKED. No C15 proof seal or frozen owner is modified.

No finite flow proves Universal CD. In particular, a successful gap graph need
not give a successful event-unit graph. First-restoration fails under the
specified chronological reservation; all-restoration survives this finite set.
The universal Hall/episode-sharing argument is absent. Final verdict is TARGETED
REFUTATION of the stated intermediate rules; Q_B<=2A remains open.
