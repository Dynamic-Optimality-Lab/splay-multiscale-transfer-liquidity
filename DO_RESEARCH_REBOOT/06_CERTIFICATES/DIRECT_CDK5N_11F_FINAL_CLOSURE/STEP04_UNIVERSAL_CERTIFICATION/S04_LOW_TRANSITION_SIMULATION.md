# S04_LOW_TRANSITION_SIMULATION.md — Gate D/E low coverage (F04-16)

Every source-valid low macro maps to E^OO_w: given the macro, its (B-trajectory,
A-paths, depths, H, q, inventory) satisfy each low conjunct by construction
(replay-verified forward simulation + ssertify env construction + Tier-1 root
check — the Step-02 synthesis loop inverts this direction, finding such macros
for queried endpoints). Executable evidence: 13 low witnesses synthesized
(G1-G3 + 10 corpus) + replayed + Tier-1 verified + abstract-matched; conjunct-wise
audit (every low conjunct True under E3 env); B-BFS word derivation for arbitrary
(s,t,w) queries. No low macro family omitted (grammar above); fringe handled by
gap pools + ports (corpus: gap0/multigap/saturated/balanced).
