# Candidate outline: LIQ_BRANCH_A_001@C2

Config: P=P_keep k=3 C=2 rho=FLAT(2) (label RHO_REQUIRED)
Identity hash: 3f92fafddbc8af195c6dd528e0ab0432322a79fc2960c9d9100cfd7ad6d4c693
Dev: violations=0 worst_shortfall=0 reg_ok=True
Validation: violations=0 episodes=5000
Adversarial: {"anneal": {"best_shortfall": 0, "engine": "anneal", "final_violations": 0, "restarts": 5, "seed": 104, "steps": 20000}, "generalize": {"engine": "generalize", "episodes": 8, "per_witness": 8, "seed": 109, "witnesses": 1}, "genetic": {"best_shortfall": 0, "engine": "genetic", "final_violations": 0, "gens": 200, "pop": 100, "restarts": 3, "seed": 105}, "hillclimb": {"best_shortfall": 0, "engine": "hillclimb", "final_violations": 0, "restarts": 5, "seed": 103, "steps": 20000}, "motif": {"engine": "motif", "episodes": 4000, "per_scale": 1000, "scales": 4, "seed": 108}, "rotneigh": {"engine": "rotneigh", "episodes": 10000, "neighborhoods": 10000, "seed": 106}, "splice": {"engine": "splice", "episodes": 5000, "seed": 107, "splices": 5000}, "structured": {"engine": "structured", "episodes": 12000, "families": 12, "per": 250, "seed": 102, "sizes": [8, 16, 32, 64]}, "uniform": {"draws": 50000, "engine": "uniform", "episodes": 50000, "seed": 101}}
Eligibility:
- REG-001 fidelity green (SYN-00)
- zero dev violations (screen+full)
- matched FLAT(1) baseline computed
- label RHO_REQUIRED via decision tree
- zero validation violations (5000 episodes)
- zero adversarial violations (9 engines)
- identity frozen (30 fields, schema-checked)
Non-claims: no universality, no C-minimality, finite survival only.
