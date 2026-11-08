# Reproduction and evidence boundaries

All new files are append-only in this versioned directory. All historical
sources/reports/certificates and Git state are read-only. Python is invoked
with -B and scripts disable bytecode writes before importing source engines.

The campaign gate AD00_FOUR_RULE_GATE.md predates its source computation.
AD00A_FIXED_CONNECTOR_SCOPE.md predates the base fixed-target reachability
audit. AD00B_OVERLAP_SCOPE_GATE.md predates the two fixed overlap variants
and authorizes the same13-key provenance audit for their declared diagonal
successor states if the known connector fails. No other overlap was tested.

Build order in a FRESH directory, after copying the scripts and exact
gates/pins and preserving original read-only source paths:

    python -X utf8 -B build_discharge.py
    python -X utf8 -B find_fixed_connector.py
    python -X utf8 -B build_overlap.py
    python -X utf8 -B find_overlap_connector.py
    python -X utf8 -B build_closed_controls.py
    python -X utf8 -B independent_verify_discharge.py
    python -X utf8 -B seal_delivery.py

Do not rerun a producer over the current artifacts: all output creation
uses exclusive x-mode, and existing files are deliberately preserved.
For relocation, retain the directory depth relative to the source root
or explicitly adapt a COPIED script in a new versioned research directory.
The final seal additionally requires the finished reports and status ledger.

Historical false flags are intentional:

- source_discharge_certificate.json records that its first proposed
  connector FAILED, so its initial closed-embedding status is historical.
- overlap_discharge_certificate.json records that the base connector
  FAILED from the u=2 diagonal successor.
- fixed_connector_certificate.json and overlap_connector_certificate.json
  contain the independently replayed replacement source words.
- closed_discharge_certificate.json supplies the completed exact closed
  provenance for all three cases, superseding ONLY those historical
  incomplete embedding statuses, without modifying old certificates.

independent_verify_discharge.py imports neither producer nor their tree
helpers. It separately loads both original engines, constructs tuple and
pointer trees from recorded sources, checks parent links, exact events,
edge-depth costs, full destinations, all source chains and the one-period
injections. Opaque subtrees are indivisible tokens and no search enters
them during core accesses. The checker also uses the exhaustive source
gap-root table with f=2v+p to verify the unrestricted-depth formulas.
There is no growing-n/fringe-depth fit.

The producer computes certificates with the original tuple engine; the
independent pointer replay is the distinct implementation check. Scripts
and source engines remain exact integer code; no floating solver is used.
The20,549 checks concern a pinned corpus and proof arithmetic. They are
not evidence that all arbitrary FE02 states have been enumerated.

Reflection is the source symmetry k->14-k with left/right swapped,
extended by order-preserving relabeling for arbitrary fringe keys. The
complete closed core controls were reflected and independently replayed.
Mathematically both primitive rotations and all stated inequalities are
invariant under this symmetry. Empty common gaps and both target-depth
parities are included; unequal paired fringe interiors are not assumed away.

The old19-block source rows were read and independently replayed. No old
certificate writer, larger W repetition, old finite fit, or original
FI/PF/FE algorithm was altered or rerun to change its outputs.

The final preservation seal must check ALL1043 inherited file hashes,
the exact897-file prior campaign inventory, all125 Stage11G hashes and
inventory, matching-terminal's freeze text, the original Git branch/HEAD
and clean tracked state. It then records the new file hashes. These are
integrity claims, distinct from mathematical theorem status.
