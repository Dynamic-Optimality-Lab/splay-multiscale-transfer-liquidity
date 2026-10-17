# S03_WITNESS_SCOPE_AUDIT.md — variable partition, mechanically verified (Gate B)

Per projected edge: interface (sort vars only) vs bound (everything else:
CL/CH/SL/SV/SW/SB/event/port/atom/B-trace/q/H/roots). Audit recomputes
FreeVars(result) - bound_names(result) and asserts ⊆ interface (FAIL CLOSED):
24/24 edges pass (S03_FREE_VARIABLE_AUDIT.json, zero `free_outside`).
Already-bound names are not re-bound (no vacuous shadowing); const-False target
sides contribute no disjunct (exact empty-target identity). Normalization then
assigns unique binder ownership (privatization, validated per edge).
