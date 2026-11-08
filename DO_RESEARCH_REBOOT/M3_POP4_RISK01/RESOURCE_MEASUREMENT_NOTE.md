# CPU measurement and the capped audit

The unchanged7200-second ceiling uses the inherited recorded PHASE CPU
ledger. Phase timers begin inside main after imports and snapshot before
final artifact serialization; they are not aggregate OS CPU including all
startup/output costs. The same definition is carried from the prior runs.
Read-only process observations additionally record whole-process CPU;
they are diagnostic and do not replace historical phase measurements.

The final audit was allocated2.579 phase CPU seconds. It logged2.594 at
the end of a word family, then stopped at the next existing guard with
UNKNOWN independent query/CPU cap. It had not completed the full audit.
The process ended between monitor snapshots, so its exact whole-process
CPU is UNKNOWN. The full remaining4.579 allowance is RESERVED, not claimed
as measured consumption. Reported phase CPU before that failure is
7195.421 including the prior4495.056; the budget charge is7200 exactly.
The capped candidate is excluded from every certified scope. No phase
was retried/split, no ceiling reset/raised, and no UNKNOWN became PASS.
