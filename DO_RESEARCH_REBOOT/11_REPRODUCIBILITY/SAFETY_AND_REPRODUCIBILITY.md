# Reproducibility and filesystem safety

All authoring and computation occurred inside the one authorized root DO_RESEARCH_REBOOT/. The initial folder did not exist. No prior reboot contents were overwritten. Source imports were avoided: verification executes only selected pure function AST definitions in a controlled namespace. Source main functions, which write into artifacts/, were never executed.

At entry, branch/HEAD/porcelain status were read with GIT_OPTIONAL_LOCKS=0 / --no-optional-locks. baseline.json records SHA-256, size and mtime_ns for every outside file, including .git, ignored bytecode/test caches and build files, plus directory paths and the complete dirty/untracked list. It covers 4,429 files and 404,217,810 bytes. The baseline was created after the permitted folder and safety script were created; those are excluded by design. The initial outside status was read before that folder existed, and workspace entries are filtered symmetrically in the final comparison.

Commands from repository root:

```powershell
python -B .\DO_RESEARCH_REBOOT\safety_audit.py begin
python -B .\DO_RESEARCH_REBOOT\10_EXPERIMENTS\verify_reboot.py
python -B .\DO_RESEARCH_REBOOT\11_REPRODUCIBILITY\inspect_evidence.py
python -B .\DO_RESEARCH_REBOOT\author_workspace.py
python -B .\DO_RESEARCH_REBOOT\safety_audit.py end
```

`begin` refuses to overwrite its baseline. Authoring refuses to overwrite already authored paths. To reproduce a future run, use a new versioned output directory/script copy within this root; do not replace the old baseline. Existing Python3.13, numpy, sympy and pypdf were used without installation. -B and dont_write_bytecode disable bytecode writes. No pytest, compiler, package manager, lake build or installation was run. Libraries use in-memory arithmetic; no source caches were generated.

Verification inputs: source ASTs in wp6_staticR.py, wp6_lambda.py, wp6_j4shared.py; enumerated T1..6/S0..3 contexts and mirrors; all empty insertion pointers for T4/S0..3; larger family heights0..30. Exact outputs and function hashes/spans: verification_results.json. C0 inputs: saved xclean matrix, old-column support and added-row block. LRF inputs: saved reduced matrix, multipliers and equality list. Exact certificate outputs: 06_CERTIFICATES/. Provenance and paper hash/page count: evidence_metadata.json. The scripts record finite scope and distinguish evidence recovery from the universal written proof.

The local L3 PDF was read and its extracted text saved only here. Online verification used arxiv.org/html/1907.06310v3 for the external reduction/model; no external media/download caches or dependencies were installed.

Final result is authoritative in final_safety_audit.json: added/deleted/changed outside files/directories must all be empty, original outside Git status unchanged and branch/HEAD unchanged. A claim of safety is not based only on Git status, since Git can miss ignored-file writes. The comparison checks content plus mtime and size. The audit does not claim to reconstruct unrelated system-wide platform internals; the complete repository boundary, including pre-existing dirty work, is checked.
