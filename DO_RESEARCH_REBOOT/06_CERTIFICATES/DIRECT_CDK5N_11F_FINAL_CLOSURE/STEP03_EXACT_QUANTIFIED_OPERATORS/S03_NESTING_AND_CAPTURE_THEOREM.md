# S03_NESTING_AND_CAPTURE_THEOREM.md — nesting + capture avoidance (Gate G/G16)

Nested results are renamed to target position via canonical suffix maps before
reuse as inner predicates (Pre/Post position discipline documented in code).
Two capture defects found by the oracle and repaired additively: (1) post_O used
the source-side universe on destination results (repaired with U_O2); (2) Step-01
privatization dropped outer free variables on shared non-leaf scope-carrying
nodes (node-keyed remap leaked copies outward; repaired by inside/outside edge
distinction in S03_SCOPE_REPAIR, Step-01/02 files untouched, their evidence
scopes unaffected since the pattern needs shared non-leaf bound-carrying nodes).
Re-verified to 4070/4070 incl. Pre(Post), MinPre(Pre), shadowed/colliding names.
