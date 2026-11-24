# Reproduction and exact preservation

Repository: `C:\Users\Saif malik\OneDrive\Documents\Desktop\Temp\splay-multiscale-transfer-liquidity-k6c2`.

Stage: `DO_RESEARCH_REBOOT\EXP04_UNIVERSAL_RESIDUAL_CONSERVATION\STAGE_UF_M1_SAME_COLUMN_CONSERVATION`.

Original branch `coarse-double-branch`, HEAD `6d532b2c795c0778f57d8023b23b5fedfc48b010`. No tracked file, branch, historical proof, word or manifest is modified. All scripts use `python -B` to suppress bytecode. INPUT_MANIFEST pins the exact M0 seal and all older transitive inputs.

## Read-only delivery verification

```powershell
python -B finalize1.py --verify-only
```

This verifies the exact delivered file set and every hash, historical preservation and unchanged tracked Git state, without writes. The seal excludes only M1_DELIVERY_MANIFEST.json itself. It is an integrity record, not cryptographic authentication against a malicious editor.

## Fresh reproduction

Do not run write-producing stages in a sealed delivery. Copy this stage's Python scripts and PRE_EXECUTION to a fresh sibling under the same EXP04 parent; keep all prior checkpoints unchanged. Run from that fresh directory:

```powershell
python -B base1.py
python -B controls1.py
python -B fresh1.py
python -B certificates1.py
python -B core_screen1.py
```

The first script verifies inheritance. controls1 replays every sealed historical primitive with the independent edge-list updater and checks all C chain/lifetime/payment identities. fresh1 constructs16 complete original sources, verifies all legal prefixes and paired closure with the mutable/immutable machinery, writes full physical/forest records, derives true zero overflow from the unchanged periodic source case, performs the separate edge audit, and independently reconstructs original Pi/cohorts on three specified sources. certificates1 checks exact candidate-obstruction formulas, including target-gain volume, integer-log/indicator alternatives and long-chain cardinalities. core_screen1 is an optional finite structural falsification screen, unused by any positive M1 theorem.

`finalize1.py` assembles the complete witness index and final consistency/resource records and seals a reviewed fresh delivery. It does not generate the mathematical Markdown proofs or prove their universal quantifiers. Build mode refuses to overwrite an existing seal. Reproduction of the scripts alone does not regenerate the prose; retain/copy the reviewed proof files separately before making a fresh complete delivery.

## Evidence layout

M1_SOURCE_WITNESSES contains complete new original words/trees/prefixes and pinned references to complete immutable historical sources. NEW_PHYS_nn stores all primitive IDs/edges, double frames and outputs, complete operation/step states and collision-free child-pointer state pools. NEW_FOREST and NEW_WEIGHTS retain original vertex IDs. HISTORICAL_AUDIT and NEW_AUDIT contain exact flux rows, full rigid components, maximal C chains, marked ancestry lifetimes and actual A donor maps for the scoped payment. Original gap weights remain separate from physical-parent capacity tests. Actual zero overflow can be justified by an existing periodic certificate even with unrun Pi; the scope fields say when that is the reason.

The root-zig counterfamily has no B doubles, so original R6 is empty by definition. Long chains and capacity examples may have zero actual weight; they refute only the stronger explicitly stated physical/potential laws. No simulated shadow redefines original Pi or cohort adjacency.

The allocation was900 measured script CPU seconds,2GiB per-process observed peak aim, at most24 fresh sources and fresh physical population<=1027. RESOURCE_RECORD includes all measured receipts, including the failed core-screen API adapter run. One import-path failure occurred before its meter and is explicitly unmetered. Imports, inspections, prose and final hash passes are not falsely included in measured script CPU. These allocations are operational, not universal theorem hypotheses or host-enforced quotas.
