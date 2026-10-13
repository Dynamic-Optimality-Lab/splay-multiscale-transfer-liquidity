# CC_CANONICAL_STATE_THEOREM.md + CC_MACRO_NORMALIZATION.md + CC_ROTATION_CIRCUIT.md (condensed)

Canonical state (CC-1): (μ,b,α,σ) with order-type endpoints (no raw keys;
relabel-invariance verified K 200/200), S-ranks exact, anonymous canonical,
hole S-subsets + emptiness, root-sync enforced. Every post-KEEP boundary
maps (construction by replay + canonicalization). Overapprox states
explicitly labeled (reachable subset tracked separately where materialized).
Macro normalization (m=3): patterns [K],[D,K],[D,D,K₀] exhaustive by cost
arithmetic (nontrivial ≤2; interior nonzero are DELETEs since KEEPs cut
intervals; terminal always KEEP; H=0 degenerate self-loop w=0). Census:
[K] 3,036, [D,K] 33, [D,D,K₀] vacuous-in-corpus-but-constructed; max 4
rotations (bound); 20 event-kind seqs observed (bound 781×3=2,343).
Nongenuine audit: all 40 corpus a=0 KEEPs are B-changing (genuine B-side);
a=0 KEEPs retained (B exact), zero-cost root DELETEs normalized (A-identity
proved). Event skeletons: 5 kinds (LL/RR/LR/RL/ZIG verified 15,521 splays).
Rotation circuit: 4-slot transducer (legality + depth-delta effects),
order validator, Hall fragment, B-lookup fragment — measured 80 DAG nodes
for fragments; sharing by hash-consing verified (4 slots share one circuit).
