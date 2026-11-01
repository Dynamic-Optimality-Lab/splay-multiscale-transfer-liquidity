# Reproducibility of the delayed source charge

Use the corrected [producer version 002](audit_delayed_shallow_v002.py), then the [independent pointer verifier](independent_verify.py), with Python `-X utf8 -B`. Both use the standard library, disable bytecode and create every output exclusively with mode x. The original producer and entry record are preserved after the serialization mismatch documented in DS00A; no initial artifact is overwritten.

To reproduce, copy version 002, the verifier, the two gate/correction records and the original producer used for the static two-change audit to a fresh versioned sibling directory. Run version 002, then the verifier. It writes `entry_source_pins_v002.json`; do not rerun over sealed outputs. The original producer need not be executed. The final seal also checks the initial entry record when present.

The finite corpus is exactly the new 23-access seven-key delayed cycle and reflection, the unchanged 22-access SC cycle and reflection, and the three literal three-key depth-tax controls plus reflection. There are 90 cycle rows, eight diagonal-prefix rows, 90 cut checks and 46 exact demand-credit assignments. The verifier performs 186 pointer-source accesses. It checks earliest payer selection, actual intervention counts, disjoint intervals and every individual source event/credit identity. Neither producer nor verifier imports a matching evaluator or allocation optimizer.

The certificate SHA-256 is `264d91e8dc6ea524cf1a242ecd871dda7ef65f1708baac4200957ed4a0d45809`. The all-size bound, no-reuse theorem and unbounded-support family are analytic arguments, not extrapolations from the fixed corpus. Older recognizers are not run; their necessary predicates are compared directly with source data.

Entry/final hashes preserve 538 inherited/source/previous-run files, all 125 Stage 11G files and their inventory, Git HEAD/branch and tracked status. The initial and corrected producer versions and entry files remain in this run. The manifest hashes every new artifact except itself. No Stage 11G code, old status writer, source graph search, package installation or larger finite instance is used.
