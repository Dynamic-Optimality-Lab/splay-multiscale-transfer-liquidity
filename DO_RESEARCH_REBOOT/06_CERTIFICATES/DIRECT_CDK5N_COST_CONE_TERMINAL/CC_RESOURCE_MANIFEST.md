# CC_RESOURCE_MANIFEST.md (§17 caps vs actuals)

Caps (frozen): 1M A-states; 15M macro transitions; 10M product states;
100M product transitions; 12 CPU-h; 32 GiB. Seeds 9/25/126/20261012;
n∈[9,20]; len 1..80; 10k/seed (40k); 10k mutants.

Actuals (prototype, odd-mask 9-key): A-states (At) ≈ 4.9k shapes… (see
CC_CERT.json: states 388,096 incl. 337 mids; low_edges 5.41M;
hi_edges 1.72M; total 7.12M transitions; BFS 211s; BF 0.4s; peak RAM
≈ 2–3 GiB). All caps respected on this scope (states 3.9% of cap;
transitions 7.1% of cap; CPU ≈ 0.3h incl. verification/regressions).

Measured scaling blockers for universal scope: completions Catalan(12)=
208,012/1.24s, Catalan(17)≈13min each (single big-hole shadow needs hours
with word patterns); post-KEEP symbolic UB 44M/mask (5.5B all masks);
612,612 diagonal seeds; per-mask reachable ~233k (concrete) ⇒ ~29M states
all-mask concrete (2.9× state cap) before fringe lifting. Universal
symbolic closure exceeds frozen caps by orders of magnitude; saturated
representative-sufficiency lifting unproved. No cap was actually
triggered (work stopped at the verdict, not at limits); the obstruction
is demonstrated infeasibility-within-budget, recorded as open.
