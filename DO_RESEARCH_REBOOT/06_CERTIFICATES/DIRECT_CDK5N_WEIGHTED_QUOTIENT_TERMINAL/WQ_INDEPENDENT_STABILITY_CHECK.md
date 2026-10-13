# WQ_INDEPENDENT_STABILITY_CHECK.md + WQ_INDEPENDENT_POTENTIAL_CHECK.md (condensed)

Stability: independent checker (WQ_refine.check_stable/check_reverse:
separate implementation from refinement loop) over 120 small graphs —
stability, uniform reverse lifting, and quotient-vs-detailed negative-cycle
agreement all hold; deliberately invalid (all-in-one) partitions fail
stability/reverse as required (58/60 rejected-or-trivially-valid, 2
genuinely stable). Refinement loop itself validated end-to-end (120/120
converge with all three properties). No symbolic-product stability check
exists (no product).
Potential: no universal potential constructed (honest absence; nothing to
check). Low-only 9-key potentials checked independently (prior campaign:
1,081+673 sampled inequalities; this campaign: 62,228 exhaustive negative
+ 12,212 sampled positive on the completed all-seed low graph — all PASS).
A re-verification that merely replays discovery BF would add nothing;
the checks above regenerate every verified edge independently.
