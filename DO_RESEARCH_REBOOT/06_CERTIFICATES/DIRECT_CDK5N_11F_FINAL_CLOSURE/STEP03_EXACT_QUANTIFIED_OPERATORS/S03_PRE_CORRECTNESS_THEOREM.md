# S03_PRE_CORRECTNESS_THEOREM.md — full two-sort Pre (Gate D/G11)

Pre_w(X)_O = U_O AND (EXISTS t. EOO_w AND X_O OR EXISTS m. EOM_w AND X_M);
Pre_w(X)_M = U_M AND (w==0 ? EXISTS t. EMO_0 AND X_O : FALSE).
Matches the mandatory definition exactly: both O disjuncts, M-only-at-0, no MM,
results over correct source namespaces, universe-conjoined. Midpoint predecessors
never omitted (M-part present for w==0 with X_O target). Evidence: 4070/4070
small-graph membership agreements (exhaustive X subsets x weights, incl. mixed
sorts, empty/full targets) + production J1-J3/J9 memberships + J10a nesting.
