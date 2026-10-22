# RC-01 Retained Theorems (exact scope, no promotion)

T1 (rotation inclusion): single rotation whose rotated child is in the
marked ancestor-closure preserves closure (nonincreasing). Covers all
zig/zigzig/zagzag wirings; needs no path validity beyond the child
membership (verified by rewiring analysis).
T2 (DELETE/inactive identity): b_blend with active=False returns old
state; core identical.
T3 (conditional low monotonicity): low witness with all B-changing KEEPs
targeting marked keys satisfies C(t) subset C(s); single-event edges
satisfy it unconditionally (terminal genuine marked).
T4 (universal high monotonicity): every contracted-high edge satisfies
C(t) subset C(s) (single marked splay + t.b == g.b, all weights).
T5 (identities): guard partition, excursion decomposition, deficit
telescoping, birth/death arithmetic, weight formula w=2H-q / 6-q.
OPEN: T6 (universal low monotonicity — blocked on unmarked intermediates).
