# Pre-execution cumulative-budget guard

Before launching any total4 finite phase, give it CPU budget
min(the unchanged120/300 cap,7200-accounted_CPU-2). The2s margin reserves
reporting/guard overhead. If no positive budget remains, stop UNKNOWN.
This tightens a phase near the existing global ceiling; it never raises
or resets a cap, splits/restarts a failed phase, or changes arithmetic,
constraints, evaluator or backend. Each phase records its allocated CPU.
Existing failed/certified reports stay immutable; *_v2 scripts below are
unexecuted draft successors before the first total4 finite phase.
