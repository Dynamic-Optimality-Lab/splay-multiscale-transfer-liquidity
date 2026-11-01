# Reproduction and coverage

Copy evaluate_explicit_potential.py and independent_verify.py to a NEW sibling directory at the same depth. From the pinned repository root run:

    python -X utf8 -B <fresh-run>/evaluate_explicit_potential.py
    python -X utf8 -B <fresh-run>/independent_verify.py

Every output uses exclusive creation. No installation, solver or fitted label assignment is required. Exact integer scaling8^5 represents every six-key G term and metric penalty; rational display is reduced exactly.

The evaluator uses immutable single-rotation construction and validates all graph arcs against the pointer primitives. The independent verifier regenerates the full graph with those pointer operations, proves the supplied distance values using upper/lower path bounds, then recomputes every expression term. The closed source word is independently replayed with tuple/frame splay, including full paired states and actual q/a/z costs.

This is one fixed six-key function evaluation:132 single trees,660 directed arcs and264 expression terms. It is not a larger finite fit or all-size numerical extrapolation. SP02/SP03 contain the arbitrary-n analytic arguments. No evidence from a floating solver, timeout or unknown status is used.

entry_source_pins.json and final_integrity.json pin/check all used physical/proof inputs and the Stage11G rule/low/high sources. Active unrelated untracked work is not claimed frozen. All writes remain in this fresh append-only directory; Python -B prevents cache writes.
