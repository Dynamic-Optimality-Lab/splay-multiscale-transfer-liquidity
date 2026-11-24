# Reproduction and safe continuation

Repository:
`C:/Users/Saif malik/OneDrive/Documents/Desktop/Temp/splay-multiscale-transfer-liquidity-k6c2`

Pinned HEAD:`6d532b2c795c0778f57d8023b23b5fedfc48b010`.
Branch:`coarse-double-branch`. No dependency installation is needed.
Use the existing Python and `python -B`; all scripts are isolated orchestration
of the read-only physical engines. No Git mutation is authorized or needed.

Preserve this delivered checkpoint. For a fresh run, copy its Python scripts
to a NEW versioned sibling below EXP04_UNIVERSAL_RESIDUAL_CONSERVATION and
set its core.ROOT to that sibling automatically through __file__. Its parent
must remain the original EXP04 directory. Copy the relevant input JSONs for
a verification-only run, or execute the producing stages below in order.
Do not rerun producers over the delivered result files.

From repository root, with D the fresh child path, run:

    python -B D/core.py
    python -B D/backward.py
    python -B D/oscillation_attack.py
    python -B D/rescue_attack.py
    python -B D/ownership_attack.py
    python -B D/all_intervals.py
    python -B D/column_attack.py
    python -B D/return_normalization.py
    python -B D/gap_payment.py
    python -B D/interior_loop_attack.py
    python -B D/guard_contamination.py
    python -B D/wide_guard_attack.py
    python -B D/intrinsic5_attack.py
    python -B D/periodic_payment.py
    python -B D/verify_checkpoint.py
    python -B D/verify_large_source.py

The exhaustive65-key interval script historically printed a long materialized
certificate to its log. The JSON is the authoritative result; inspect only
metadata or redirect stdout. No floating arithmetic decides eligibility.

Important corrected controller behavior: intrinsic5_attack.py now audits one
targeted DISTINCT consumer, not once per original gap. The interrupted first
run spent532.578125 measured CPU seconds before this correction. Its other
unfinished searches provide NO negative certificate. The corrected full source
and trace were independently replayed, saved and verified; source count treats
this as ONE unique source, while resource totals count both executions.

The large trace is lossless: its states dictionary is keyed by complete state
SHA256; each operation boundary references pre_A,post_A,pre_B,post_B hashes.
All original events/IDs and paths are retained. verify_large_source.py expands
these references, hashes every state, checks all links/costs/closure, and
independently replays both retained comparisons on their projected domains.
Snapshot interning uses full exact tuples as keys, not hash-only equality.

Verification-only inputs for the critical witness are OWNERSHIP_SOURCES.json,
OWNERSHIP_RESULTS.json,ALL_INTERVALS_ESCAPE_AUDIT.json and INPUT_MANIFEST.json.
verify_checkpoint.py reruns the original R_* and all frozen selectors, all
824970 intervals, the independent primitive SET/Pi/U reconstruction, and the
small arc-family implementation check. These finite checks verify the saved
witness; C1–C7 have separate source-uniform mathematical proofs.

finalize.py builds the unified source/inventory/resource indexes and rechecks
the transitive historical input pins. It hashes every delivered child artifact
except the delivery manifest itself. Do not run it until all producing scripts
have ended and reports are finalized. The parent manifest is never rewritten.

Next research must start from EXP04_RESEARCH_FRONTIER.md, review the staged
resource ceilings, and attack hard, return-free rank traffic with larger
genuine support. More coverage counts at the present support limit cannot
replace the missing universal physical conservation proof.
