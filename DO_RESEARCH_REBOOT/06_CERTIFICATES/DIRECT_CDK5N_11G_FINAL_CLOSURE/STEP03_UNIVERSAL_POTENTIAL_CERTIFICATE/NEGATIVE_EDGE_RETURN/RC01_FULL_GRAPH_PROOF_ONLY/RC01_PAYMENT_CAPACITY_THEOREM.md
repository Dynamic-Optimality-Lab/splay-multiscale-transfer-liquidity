# RC-01 Payment Capacity Theorem (attempted; q-cancellation obstruction)

Attempt: bound restoration cost from below via forced A-work. For return
path P restoring endpoint u from v, structural restoration is required
(exact B/A state equality), but NO universal lower bound on w(P) follows:
restoration splays may have arbitrarily small H' (A-root accesses, zero
events) while generating offsetting q' credits (B-progress), since w' =
2H'-q' has no sign constraint from endpoint equality alone. Concretely:
pushing the accessed key back down its ancestor chain is achievable
through bystander rotations whose individual weights can be zero or
negative (pushback probes: depth-4 recovery at total cost 2 observed).
Hence no H'-floor implies any w-floor. The q'-cancellation is the precise
obstruction: every B-side repair generates B-progress credit that offsets
its A-cost in the frozen weight formula. No payment-capacity theorem
established. (Gate: payment structure + no-double-spend unproved.)
