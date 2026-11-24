# SHARP-02 reproduction

Current exact corpus provenance: branch `coarse-double-branch`, commit
`6d532b2c795c0778f57d8023b23b5fedfc48b010`. Standard-library Python only.
All writes/caches/logs stay here. Run with `-B`; do not execute a script from
SHARP-01 that would rewrite an old receipt. The four vendored SHARP-01 modules
are byte-identical read-only snapshots used by SHARP-02 scripts.

## Standalone principal-counterexample check

The artifact bundle contains everything needed for the new counterexample.
From its extracted directory run:

```powershell
python -B sharp02_standalone_verify.py local_replay_v001
```

Choose a fresh receipt name if repeating. This checks the exact full source,
alternate legal right-vine prefix, both complete endpoints, all 117 primitive
rotations/ancestry changes, original gap costs, ALL eligible named gain units,
fixed Hall failure and explicit repaired maps. It uses a full pointer replay,
an immutable-frame replay and immutable primitive reconstruction. No historical
repo input or installed dependency is needed for this principal check.

`SHARP02_MINIMAL_SOURCE_LEDGER.json` resolves every tree reference in its
`states` table. `SHARP02_MINIMAL_INDEPENDENT_GEOMETRY.json` contains complete
pre/post A trees for each real A rotation. The principal certificate lists
every eligible unit, not just the selected one. Original source identity is
(source name, actor, operation, StepEv, bit); virtual companions are marked.

## Full in-repository reconstruction

Preserve this run. Make a NEW versioned sibling directly under
`DO_RESEARCH_REBOOT`, copy the `*.py` scripts into it, and run there with the
unchanged SHARP-01 directory available beside it:

```powershell
python -B sharp02_common.py
python -B sharp02_reconstruct.py
python -B sharp02_fast.py
python -B sharp02_network_tests.py
python -B sharp02_search.py
python -B sharp02_search.py adversarial_search_v002
python -B sharp02_confirm.py
python -B sharp02_minimize.py
python -B sharp02_certificate.py
python -B sharp02_controls.py
python -B sharp02_episodes.py
python -B sharp02_assemble.py
python -B sharp02_standalone_verify.py independent_replay_v001
python -B sharp02_write_reports.py
python -B sharp02_final_verify.py
```

The two search passes must reproduce proposal 452's same source bytes, costs
and graph. The final driver records all 423 unique complete candidate rows;
the original first-run log recorded only its 214 positive-demand rows. The
authoritative full data are in the v002 log. New timing/peak memory and receipt
names may differ. All numerical results and physical source hashes should agree.
For an exact seeded generator replay, match the Python implementation/version
recorded in `SHARP02_ENVIRONMENT.json`. Direct saved-witness verification uses
only exact operations and does not depend on regenerating the randomized search.
The source minimization is a deterministic local deletion/universe procedure,
not a claim to global source minimality. It returns the 10-key, 17-operation case.

## Exact algorithms and proof checks

Fixed graph resources are original remaining A units after first-min(q,2p)
reservation. Pattern grouping merges ONLY resources with identical demand
neighborhoods, retaining their integer multiplicity and actual-unit catalog.
Integral max-flow gives assignments and deficient cuts. Minimum NONEMPTY Hall
margin is computed by forcing each positive-demand node into the source side
in turn. Cases with zero demand have margin null. Up to 14 demand nodes,
minimum-cardinality deficient sets are also exhaustively checked. Larger
deficient sets are only inclusion-minimized, with that qualification recorded.

Optimized reservation uses ALL original units and a per-gap sink quota c_j.
This is a different exploratory allocation question. The concrete repair swaps
A(2,1,1) with A(2,2,0) within gap 2. The origin-loss repair changes eligibility
instead and preserves every chronological baseline owner. Neither is a proved
universal mechanism or an imported C14/C15 owner certificate.

The numerical pipeline receipts include CPU, wall-clock duration and peak
working set, including repeated versions. Finally blocks persist failures;
longer stages write checkpoints while running. A forced OS termination can
leave an explicitly RUNNING checkpoint, never a fabricated PASS. The new
cumulative ceiling is 900 numerical process CPU seconds, 1 GiB per process,
600 keys and 20,000 operations per period. Search limit is 500 CPU seconds /
50,000 candidates / 32 recurrence iterations, and stops at the first principal
failure. No historical allowance is borrowed/reset. SHARP-01's missing initial
CPU and peak-memory measurements remain missing.

## Artifact map

* `SHARP02_DISCOVERY_REPORT.md`: sixteen-section research report and exact verdict.
* `SHARP02_HALL_RESULTS.json`: reconstructed corpus, exact graphs/cuts, controls and principal result.
* `SHARP02_ANCESTRY_EPISODES.json`: complete relevant cyclic relation streams for 81 sources.
* `SHARP02_SOURCE_WITNESSES.json`: 148 explicit complete source words/states/prefixes and execution hashes.
* `SHARP02_COUNTEREXAMPLE_CERTIFICATES.json`: exact principal, parametric and token obstructions.
* `SHARP02_THEOREM_LEDGER.md`: proofs, refutations, finite exchange scope and open debt.
* `SHARP02_PRINCIPAL_COUNTERCERTIFICATE.json`: full six-unit reservation obstruction.
* `SHARP02_REPAIRED_SOURCE_INJECTION.json`: all 24 original-double owners after the swap.
* `SHARP02_ORIGIN_LOSS_REPAIR.json`: all 24 owners under the separate origin-loss eligibility.
* `controls/`: complete C15 ledgers and independently reconstructed A geometries.
* `SHARP02_INPUT_HASHES.json`, final verification, delivery manifest and `receipts/`: provenance/integrity/resources.

The fixed SHARP-HALL rule is refuted (Type II). Q_B<=2A is not refuted.
The statement that an optimized/expanded physical model works universally is OPEN.
