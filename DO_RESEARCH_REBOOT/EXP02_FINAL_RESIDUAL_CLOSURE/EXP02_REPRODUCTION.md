# EXP-02 reproduction

Run from this isolated directory in the current coarse-double-branch checkout. EXP-01 and its original immutable tuple engine must be present and unchanged. Core work uses Python standard-library integers/Fraction and existing physical engines; the optional figure uses already installed Matplotlib. No dependency installation or Git mutation is required.

## Canonical stages

```powershell
python -B exp02_g_gate.py *> EXP02_G_GATE.log
python -B exp02_inventory.py *> EXP02_INVENTORY.log
python -B exp02_stageD.py *> EXP02_DISTORTION.log
python -B exp02_frame_bridge.py *> EXP02_FRAME_BRIDGE.log
python -B exp02_common_grandparent.py *> EXP02_COMMON_GRANDPARENT.log
python -B exp02_finalize_data.py *> EXP02_FINALIZE.log
python -B exp02_grandparent_distortion.py
python -B exp02_tests.py
python -B exp02_report_data.py *> EXP02_REPORT_DATA.log
```

Run in order. The inventory stage resets generated results to the133 inherited sources; subsequent stages add27 then11 complete controls. Append stages must not be run twice against already appended data. Wall times/CPU/memory vary; source words, exact costs, full physical states, original classes and hashes are deterministic. Reproduction writes only EXP-02, leaving EXP-01 read-only.

EXP02_FRAME_BRIDGE_CERTIFICATES.json preserves the initially stronger full-frame diagnostic. EXP02_COMMON_GRANDPARENT_CERTIFICATES.json is the stronger proved final cover. A changed full frame can still have a common labelled grandparent, and such a case is paid by the latter injection. Do not substitute the older diagnostic's24-event complement for the final14-event complement.

## Expected gates and totals

* G's exact domain is [1..32] union {34,50}, size34, ell31, threshold18, physical isolation true, actual window Q_B25.
* Published one-orientation EXP-01 pin: 239 inherited R6,144 return-covered,95 R6_other.
* Adaptive rule:92 inherited complement events paid; only the three L3 G cases survive that stage.
* Final171-source corpus:351 R6_other,94 adaptive paid,243 common-grandparent paid,14 unhandled. The133 inherited sources have95 complement events, all paid. The38 new sources have256 complement events,242 paid and14 unhandled.
* Distinct complete-source corpus occurrences:76,474.578 final checks pass in the recorded run.
* Primary omitted-first-hit witness: IH_p4_q1_L2_z5_c1, operations259,A259,Q_B110,R6_other1. Its original rho remains (132,(72,3),(80,1)), consumed at target5.
* Nine-key distortion control: A17,Q_B1, omittedQ0, retaineddelta1, closingdelta0, both B states close. Actual auxiliary control: same A17,Q_B0, complete paired closure.

## Physical data conventions

K/D tags retain original KEEP/DELETE semantics; no physical deletion. Full tree state is a labelled root and dictionary key -> [left,right]. Null means a genuine absent child. Original S is computed once from actual genuine KEEP support and physical ancestry. D6 I is fixed at the original source cut. Chosen outputs, cyclic Pi and full cohorts remain EXP-01's actual original predicates.

EXP-01 stored both orientations. The pinned one-orientation rule is 2*rank_S(initial_B_root)<|S| => increasing, else decreasing; empty S => increasing. The two certificates are not united under a coefficient-six budget. The rule and counts are recorded explicitly; historical data is not edited.

ACTUAL B and SHADOW B have distinct namespaces. Content-addressed tree state pools in EXP02_TRAJECTORIES contain complete before/after trees for all retained accesses and original omitted transitions. Identical payload hashes do not merge their events or A budgets. Original A states and shared-life events are separately referenced in EXP02_ORIGINAL_STATES and the residual inventory. A hash is a compact lookup key for stored/reconstructible complete states, not a substitute for full-Pi certification.

Negative unrolled kappa timestamps refer to previous-period lifts of the same original IDs, not extra prefix resources. Every warm/cut source retains its actual reaching prefix; new sources start on common diagonals. Source costs always include full closing work. Source variants do not share donor budgets.

## Inspect a complete saved source again

```powershell
@'
import json
from exp02_core import ROOT,Replay,digest,residual
a=json.loads((ROOT/'EXP02_SOURCE_WITNESSES.json').read_text())
name='IH_p4_q1_L2_z5_c1'
s=next(s for s in a['new_sources'] if s['name']==name)
r=Replay(s)
assert digest(r.events)==s['trace_hash']
assert r.a.state()==s['closing_A'] and r.b.state()==s['closing_B']
direction,returned,other=residual(r)
print(name,r.A,r.Q,len(other),direction)
'@ | python -B -
```

Replay independently checks the immutable tuple engine at every original operation and reconstructs complete full-Pi/cohort/R6 predicates. The primary witness already has its full consuming bits, A/B states and complete tagged source materialized in EXP02_PRIMARY_OBSTRUCTION.json.

## Main deliverables and limits

EXP02_FINAL_RESIDUAL_REPORT.md contains the two scoped source-uniform proofs, the physical grandparent identity, full coverage audit and explicit open complement. EXP02_THEOREM_AND_COUNTEREXAMPLE_LEDGER.md distinguishes proofs, finite-exact data, refutations and missing universal laws. EXP02_FULL_MEASUREMENTS.md contains every complete-source row with exact reduced ratios. Required JSON artifacts contain the event inventory, domain certificates, trajectory comparisons and whole source witnesses.

Recorded successful-stage CPU, elapsed time and peak working sets are in EXP02_RESOURCE_RECORD.json. Unmetered diagnostic pilots, one failed finalization timer write and an invalid first memory probe are disclosed; the recorded CPU sum is not total campaign CPU. The corrected pipeline above does not repeat those mistakes. No exhaustive all-source enumeration, external/formal audit or universal R6_other/A bound is claimed.
