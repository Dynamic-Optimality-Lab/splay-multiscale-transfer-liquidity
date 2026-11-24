# EXP-03 reproduction

Run in this isolated directory of the existing coarse-double-branch checkout:

`C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2/DO_RESEARCH_REBOOT/EXP03_FINAL_R6_ESCAPE_CONSERVATION`

Only Python standard-library arithmetic and the existing EXP-01/EXP-02 engines are used. No installation is required. Use `-B` so imports do not write bytecode caches into historical directories. The scripts redirect new comparison/trajectory writes to EXP-03 in memory; do not run historical entrypoints that write their old ROOT.

## Canonical dependency order

```powershell
python -B exp03_inheritance.py *> EXP03_INHERITANCE.log
python -B exp03_experiments.py *> EXP03_EXPERIMENTS.log
python -B exp03_adversarial.py *> EXP03_ADVERSARIAL.log
python -B exp03_tests.py *> EXP03_TESTS.log
python -B exp03_finalize.py *> EXP03_FINALIZE.log
python -B exp03_package.py *> EXP03_PACKAGE.log
```

The inheritance stage resets the source archive to the171 historical sources. Experiments resets the new corpus to its63 deterministic constructions. Adversarial appends26 more and deliberately refuses duplicate names: do not run it twice without resetting via the previous stages. Finalize adds metadata and derived tables without changing source words, original events or costs. Package refreshes resource and delivery manifests after the other stages finish. Mathematical prose is supplied alongside these generated results and is not rewritten by the experiments.

Every computation stage has exception-safe atexit measurement of process CPU, wall time and Windows memory counters. Package records its own measurement before hashing the delivery. Pilot stages were exploratory and are not needed for canonical reproduction. Their failed/completed resource records remain in the delivered audit; do not delete failures to improve reported totals. Reproduction time and memory depend on the machine. The1000 recorded-CPU-second bound was a limit for this run, not a promise for all machines or repeated reproductions.

## Expected gates

* All311 EXP-02 delivery hashes match.171 original traces match, with76,474 independent original-operation checks.
* EXP-02's final common-grandparent cover, rather than its stricter whole-frame diagnostic, leaves14 genuine gaps: O10/G4/X0. They use11 original parent occurrences: O7/G4/X0, maximum gap capacity3.
* The mandatory65-key witness has259 operations, A259, Q_B110 and rho `(132,(72,3),(80,1))` at parent `(132,2)`, g18. Its last A ancestry loss is `A(113,1,0)` with SET sign0.
* The four historical G gaps are at392 in the two-period source and392,652,912 in the four-period source. Old shadow has no double at those KEEP3 accesses. Restarted shadow has g18.
* There are89 canonical new source records, including24 sparse-support warmed controls, with maximum population513. They have270 old-unhandled gaps;160 are restart-paid and110 remain. Five additional named complete pilot records are retained separately, two physically duplicating later controls; the resource audit conservatively counts94 named new complete records.
* Combined with historical residuals:284 old-unhandled gaps,164 newly restart-paid,120 explicitly remaining. No universal coefficient for that complement is supplied.
* Xprobe_p4_L3_hitNone_boundary1 has A261/Q_B110, outside gap `(197,(137,3),(145,1))`, parent `(197,2)`, g48.
* mixed_p5_Gcopies2 has A1793/Q_B712. Parents `(785,2)` and `(793,2)` both select `A(740,1,0)` as their last A ancestry loss.
* The naive separated-private candidate fails complete B closure and is excluded. Its repaired full-closing and exact warmed variants pass original closure.

## Inspect an original witness independently

```powershell
@'
from exp03_core import *
a=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
name='Xprobe_p4_L3_hitNone_boundary1'
s=next(s for s in a['new_sources'] if s['name']==name)
r=Replay(s)
assert digest(r.events)==s['trace_hash']
assert r.a.state()==s['closing_A'] and r.b.state()==s['closing_B']
c=current_classification(r)
print(r.A,r.Q,parent_sets(c['unhandled']))
print(c['unhandled'])
'@ | python -B -
```

This inspection regenerates EXP-03 comparison pools, so it is a write within this directory. Repackage if a delivery manifest is needed afterward. For a read-only physical replay, stop before `current_classification`.

To inspect the quantitative partial mechanism:

```powershell
@'
from exp03_restart import *
a=json.loads((ROOT/'EXP03_SOURCE_WITNESSES.json').read_text())
s=next(s for s in a['inherited_sources'] if s['name']=='IH_p4_q1_L3_z1-65_c1_periods2')
r=Replay(s)
c=current_classification(r)
e=actual_mismatch_episodes(r)
z=restart_analysis(r,c['unhandled'],e)
print(z['paid_original_gaps'],z['sum_J'],z['original_A_transition_count'],r.A)
'@ | python -B -
```

## Data conventions and limits

Original IDs are `[actor,t,j,bit]`; parent IDs are `[t,j]`, scoped by source. A StepEv is represented by its bit0, including a terminal zig's one real bit. Negative unrolled primitive times lift genuine original events from the preceding cyclic copy and do not create prefix capacity. Full tree dictionaries retain every physical key and empty child.

EXP02_TRAJECTORIES here is an **EXP-03-local** folder with inherited format names. It stores complete actual/shadow retained and omitted states and independent comparison checks. Original source words and initial/closing pairs reconstruct all original and causal intermediate states. Actual and shadow equal payload hashes do not merge their event namespaces.

The unchanged normalization rule is increasing iff `2*rank_S(initial B root)<|S|`; otherwise decreasing, with increasing for empty S. One fixed direction is used in the new restart budget. The adaptive class retains its inherited separate rules. No unpriced union of both directions is introduced.

The independent tuple engine verifies physical states, StepEv grouping and costs. Pi, first-hit cohorts and residual classifications are recomputed by the inherited exact oracle and matched against historical certificates. This is not two independent symbolic implementations of Pi. Universal proofs remain conditional on the stated inherited interfaces; finite coverage, observed load2 and observed comparison-episode overlap1 are not universal theorems.

The failed pilots were (1) missing classification-summary metadata, (2) treating the inherited frame dictionary as a list, and (3) a sparse-key source that did not close B. Their measured failures are preserved. They were corrected by metadata/value instrumentation and by requiring real complete closure; none was an independent mutable/tuple transition discrepancy.
