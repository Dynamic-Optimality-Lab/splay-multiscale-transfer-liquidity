# Shared A-loss continuation

Read GLOBAL_R6_CONTINUATION.md first.

Status: the universal R6<=cA target remains OPEN. Finite witnesses and counterexamples to charging rules do not refute it.

All new files are isolated here. Old sources, owners, engines and Git are read-only. No commit/push was performed.

## Reproduction

Use a NEW sibling folder directly under DO_RESEARCH_REBOOT, copy the three Python files there, and keep the inspected EXP01_PHYSICAL_RESIDUAL_DISCOVERY inputs available read-only. Use Python -B. Do not overwrite the preserved certificates here.

Accepted campaign phases, in their original order:

    python -B shared_loss.py pilot
    python -B shared_loss.py expand
    python -B shared_loss.py attacks
    python -B shared_loss.py dense
    python -B shared_loss.py bands
    python -B shared_loss.py repeat_lift
    python -B shared_loss.py even_cycles
    python -B audit_saved.py
    python -B verify_witnesses.py

The original campaign also performed intermediate saved-data audits. Their CPU is recorded. The rejected even_lift construction is preserved in RESULTS_even_lift.json and RESOURCE_RECEIPT.json; it is not required to regenerate accepted sources. Final source words, costs and event IDs are authoritative, not their display names.

The verification script refers to source_069.json (the genuine R6 witness) and source_106.json (the returning-block prototype), so preserve phase order for those names. Source constructors are deterministic. The current maximum retained-ticket bracketing load TWO is finite evidence only.

## Main files

GLOBAL_MULTIPLICITY_AUDIT.json contains the finite all-R6 event-load audit.
GENUINE_R6_COUNTERCONFIGURATION.json contains the fully checked R6 coverage counterconfiguration.
PERIODIC_BRACKET_COUNTEREXAMPLE.json supplies literal words and complete states for the all-m charging-rule counterexample.
WITNESS_VERIFICATION.json contains the additional full-window and periodic-block checks.
RESOURCE_RECEIPT.json includes accepted and failed semantic work.

No all-source proof certificate or unbounded R6/A family is supplied.

