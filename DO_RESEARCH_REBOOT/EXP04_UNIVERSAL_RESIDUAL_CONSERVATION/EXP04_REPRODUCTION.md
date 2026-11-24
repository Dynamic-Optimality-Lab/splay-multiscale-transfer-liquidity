# EXP-04 reproduction

Run in this isolated directory on coarse-double-branch. Use Python -B,
standard-library integers/Fraction and the existing physical engines. No
installation or Git mutation is needed. Imports redirect diagnostic writes
to EXP-04 in memory; historical files stay read-only.

Preserve a version of the delivery before regenerating these mutable outputs.
Use new log filenames. Current resource records automatically get unique
versions. Canonical dependency order:

```powershell
python -B exp04_inheritance.py *> REPRO_INHERITANCE_v002.log
python -B exp04_cycles.py *> REPRO_CYCLES_v002.log
python -B exp04_monotone.py *> REPRO_MONOTONE_v002.log
python -B exp04_adversarial.py *> REPRO_ADVERSARIAL_v002.log
python -B exp04_sparse.py *> REPRO_SPARSE_v002.log
python -B exp04_final_cycles.py *> REPRO_FINAL_CYCLES_v002.log
python -B exp04_boundary.py *> REPRO_BOUNDARY_v002.log
python -B exp04_tests.py *> REPRO_TESTS_v002.log
python -B exp04_weighted_potential.py *> REPRO_WEIGHTED_v002.log
python -B exp04_weighted_drift.py *> REPRO_DRIFT_v002.log
python -B exp04_finalize.py *> REPRO_FINALIZE_v002.log
python -B exp04_package.py *> REPRO_PACKAGE_v002.log
```

Inheritance resets to260 old sources. New batches are42,36,12,30 (total120).
The monotone stage handles old R_* sources and the first42; subsequent batches
save their own certificates. Finalize joins these records. Do not append a
batch twice. exp04_density.py is an optional earlier-corpus audit, not a
canonical recorded stage; density was executed in the final30 and final tests.

The initial42 run failed on an Xprobe core-start assumption. Its actual
execution used `exp04_cycles.py --resume` after adding the genuine prefix
KEEP2. The rejected full source/final trees are preserved. Fresh repaired
generation can add an identity KEEP1 to an earlier protected prefix; measured
period words, initial/closing pairs and trace hashes are unchanged. The archive
is authoritative for this run's exact legal prefix. Prefix work is excluded.

Expected canonical totals:380 complete records,184,770 original operations;
120 new records/63,015 operations;499 original R_* gaps. Paid classes are
35 zero/two-direction,276 gappy monotone,136 cycle-rank and52 actual density.
Finite complement0 is not a universal theorem. New types before payment are
O353/G24/X2. Old189 EXP-03 and311 EXP-02 delivery hashes match.

Final focused checks:10,838;12 critical replays/9,862 operations;1,485 separate
tuple checks of pruned operand accesses;380 legal prefixes/19,328 prefix ops.
Numerical timings and repaired identity-prefix counts can differ on rerun.
Weighted potential certificates use exact hex fractions through513 keys.

To inspect a witness without regenerating comparison pools:

```python
from exp04_core import *
a=json.loads((ROOT/'EXP04_SOURCE_WITNESSES.json').read_text())
s=next(s for s in a['new_sources'] if s['name']=='composed_p4_alternating_inside_m256')
r=Replay(s)
assert digest(r.events)==s['trace_hash']
assert r.a.state()==s['closing_A'] and r.b.state()==s['closing_B']
print(r.A,r.Q,r.closed)
```

original_residual recomputes the old classes with local output pools; metrics,
enriched and density_analysis add the new systems. No new selector uses demand
success. Equal state hashes do not merge actual/shadow events or A budgets.

EXP04_MONOTONE_CERTIFICATES.json corrects inherited report-only bound labels
in the early in-flight gappy output; physical states/costs did not change.
EXP04_PHYSICAL_LIFECYCLES.json applies the corrected B-presence test at the
last A loss and supersedes optimistic preliminary per-batch booleans.

Early resource records retain the imported EXP03_RESOURCE_ filename format
inside EXP-04; current ones use EXP04_RESOURCE_. One first cycle10 measurement
was overwritten and is explicitly unmeasured; no value is invented. Interactive
inspection, prose and final hashing are not continuously metered. Reproduction
uses additional resources and does not borrow a prior campaign allowance.

The tuple engine checks states/costs separately from the mutable tree. Full
Pi/cohort/R6 remains the inherited oracle, not a second independent symbolic
classifier. Proofs are same-agent mathematics with the stated classical
dependencies; there is no formal, independent-agent or human theorem audit.
Continue from the current section of EXP04_RESEARCH_FRONTIER.md, preserving
all original occurrences and failed hypotheses.
