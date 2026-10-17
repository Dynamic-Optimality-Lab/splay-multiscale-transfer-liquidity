# S03_LOW_PROJECTION_THEOREM.md — E^OO_w(s,t) <=> exists source-valid witness (Gate B)

## Claim
For every (s,t,w): projected E^OO_w(s,t) holds iff a source-valid low macro
witness realizes that edge (BFS word + canonical completion + replay + ssertify).

## Argument
Projection binds exactly the hidden macro/B-trace/A-prefix/inventory/cost vars,
preserving membership (existential closure over edge-local variables). Forward:
Step-02 engine witnesses satisfy the full low root (Tier-1 verified), hence the
projection. Backward: a satisfying assignment restricts to s/t pins + witness
values that replay/verify (engine inverts: B-words from topos, completions
canonical-first). No free hidden variables (audit); no witness shared across
edges (per-root binders + privatization). Evidence: J1-J3/J9 SAT + Tier-1 +
replays; 150/150 + 4070/4070 operator agreements on the same construction.
