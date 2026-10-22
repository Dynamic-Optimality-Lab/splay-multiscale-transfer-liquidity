# CORE-01B Strong Inclusion Attempt (Gate E verdict: BLOCKED, not refuted)

Attempted: prove C_n subset C_0 for all low witnesses via terminal
restoration. Blocked at: no removal guarantee for intermediate unmarked
gains (see terminal-restoration analysis). Minimal dangerous macro:
unmarked B-changing KEEP (entry, x gains marked descendants) then terminal
marked KEEP that bypasses x's branch. No frozen conjunct rules it out;
no certified instance exists (solver/certification forbidden this phase).
Verdict: strong inclusion NEITHER PROVED NOR REFUTED for low edges;
the obstruction is a precise missing lemma (removal guarantee), not a
counterexample. (High edges: strong inclusion PROVED separately via
single-splay + midpoint identity.)
