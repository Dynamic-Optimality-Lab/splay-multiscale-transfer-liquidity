# EXP-01 reproduction

Run from this directory in the current repository checkout. Preserve all historical inputs listed in EXP01_INPUT_MANIFEST.json, including currently untracked research. Python must be available; no installation is performed. Core mathematics uses the standard library and the existing python/independent/splay.py. The optional scientific-figure step uses the already installed Matplotlib.

## Rebuild the exact 133-source result

```powershell
python -B exp01_run.py *> EXP01_RUN.log
python -B exp01_supplement.py *> EXP01_SUPPLEMENT.log
python -B exp01_adversarial.py *> EXP01_ADVERSARIAL.log
python -B exp01_incidence.py
python -B exp01_analyze.py *> EXP01_ANALYSIS.log
```

Run in that order. The first command resets the generated corpus to the initial 118 sources. The next commands append nine deliberately different nested/private/helper controls and six independent W-derived falsification sources. Do not run an append stage twice against the same generated results. Wall times and CPU measurements vary by machine; source words, physical states, costs, classifications and primitive hashes are deterministic. Generated result files in this isolated folder are replaced; historical inputs are read-only.

The full original G source is G_4_1_L31_r1_z1. Its expected totals are 290 operations, A=323, Q_B=156, R6=1 and closing increasing A cost 86.

## Reconstruct an individual complete physical trace

```powershell
python -B exp01_inspect.py G_4_1_L31_r1_z1 --trace
python -B exp01_inspect.py DH_4_1_at31_c1 --trace
python -B exp01_inspect.py DW_5_1_at31 --trace
```

Each command reads the complete saved source, independently checks both transition engines at every operation, recomputes full cyclic Pi/cohorts/R6, verifies the closing states and canonical trace hash, then writes inspection_<hash>.json here. Omitting --trace keeps event/cost/cohort summaries without the large boundary/event arrays. The original actor/t/j/bit IDs are retained. The negative kappa timestamps in certificates mean previous-period lifts of existing original IDs; map a timeline time t to events[(t-1) mod T].

## Inputs and source semantics

* KEEP is tagged K; DELETE is tagged D and never removes a key.
* Full tree state is a root plus a dictionary of physical key -> [left child,right child]. Null children are real empty pointers.
* M is actual nontrivial B KEEP support; S is its original physical ancestor closure. Full-S labels are integer bitsets indexed by sorted physical keys, with non-S bits zero. Decode J by testing the bit of each key, not by interpreting the bitset integer as a key interval.
* D6 I is fixed once at the original cut. Reflected/cut sources are different complete legal sources with their own declared chronological IDs and stored provenance; historical source records are never modified.
* Reaching prefixes are explicitly saved and replayed. Their A work is reported separately and excluded.
* C15 F-gap strings in saved historical syntax are instantiated as empty physical gaps for these concrete controls. No owner map or historical fixture is edited.

## Verification layers

exp01_validate.py has 25 inherited/hand gates. Replay checks the immutable tuple engine against every operation, original signed identities, exact physical closure, complete full-Pi membership and full cohorts. Supplement independently compares Pi queries with every full A snapshot on G/W_star. It also checks the identical H/DH prefix and H6's actual [11,33]->[19,129] growing relay.

EXP01_THEOREM_CERTIFICATES.json checks every erased B interval's exact complete-state return and zero double count, replays the retained B skeleton and records distinct ORIGINAL A StepEv for each internal rank transition. The original full trace hashes must match. EXP01_G0_GAP_CERTIFICATES.json contains explicit cyclic original KEEP-gap witnesses for representative full/warmed/C15/W sources.

exp01_incidence.py uses exact rational scaling and integer max-flow. A tight Hall set proves a lower bound on maximum fractional load; the stored rational flow proves the upper bound. This applies only to the finite physically justified root-entry graph. It is not a universal payment certificate.

## Main files

* EXP01_DISCOVERY_REPORT.md: source model, G lifecycle, deductions, scoped proof, refutations, ledger and limits.
* EXP01_RESULTS.json: exact complete-source measurements, ratios, original R6 events, windows, physical diagnostics and resources.
* EXP01_SOURCE_WITNESSES.json: complete physical initial/closing states, tagged words, prefix provenance, original R6 certificates and hashes.
* EXP01_G_LIFECYCLE.json: full G operation-boundary trees and every actual primitive rotation, not just selected frames.
* EXP01_THEOREM_CERTIFICATES.json and EXP01_INCIDENCE_CERTIFICATES.json: finite interface/flow certificates.
* EXP01_FULL_MEASUREMENTS.md and EXP01_SCALING.png/.svg: complete table and scientific figure.

No external/formal audit or exhaustive all-source enumeration is claimed. The report's restricted symbolic theorem uses the inherited sequential-access theorem and three-slot lemma. The unrestricted R6/A bound remains open. E2 is not run.
