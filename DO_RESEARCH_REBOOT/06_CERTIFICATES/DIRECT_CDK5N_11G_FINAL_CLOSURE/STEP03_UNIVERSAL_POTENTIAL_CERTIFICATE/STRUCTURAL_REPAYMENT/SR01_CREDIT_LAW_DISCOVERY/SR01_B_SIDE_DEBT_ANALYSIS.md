# SR-01 B-Side Debt Analysis

A B-splay never reduces total B-mass (ΔD_B = Σ|S_i| ≥ 0 per rotation;
verified by code reading). The accessed key plunges (dB→0, pays q) while
off-path sibling subtrees are pushed down (charge ε_B ≥ 0 in half-depth
units; measured ΔQ up to +4 at w=3). Candidate B-progress measure
D_B = Q = Σ⌊depth/2⌋ pays q by construction on x but fails exactly where
ε_B dominates (2 ledger edges). Pure rank scaling is PROVABLY impossible:
E4 (ΔR=−5,w=−2) forces c_R ≥ 0.4 while rank-jump cousins (ΔR=+3,w=1) force
c_R ≤ 1/3 — empty interval. Pure depth scaling fails similarly (6 viol).
Rank telescoping has the wrong sign for drops (splay accumulates mass at x
on both sides; classic access lemma bounds growth, but our inequality needs
drops on negative edges). Reversibility: restoring pre-splay B-topology
requires pushing x back down; pushback probe shows depth-4 recovery for
cost 2 (cheap-ish), so weight-based charging of x-motion is impossible in
general (return splays concern other keys). B-side conclusion: no B-only
law; debt must be priced jointly with A-side state change.
