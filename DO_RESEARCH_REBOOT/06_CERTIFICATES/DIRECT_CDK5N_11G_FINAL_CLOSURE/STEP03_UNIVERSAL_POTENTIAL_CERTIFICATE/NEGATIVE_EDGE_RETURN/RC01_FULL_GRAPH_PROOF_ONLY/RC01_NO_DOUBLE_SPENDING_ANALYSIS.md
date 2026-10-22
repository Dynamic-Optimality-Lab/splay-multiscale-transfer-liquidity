# RC-01 No-Double-Spending Analysis (open; interface rule binding)

A valid scheme needs: debt units with unambiguous identity, single use,
availability at repayment time, and closure with nothing unpaid. The
binding constraint (prompt section 10 interface rule): adjacent edges
share ONLY the 147-field vertex. Consequences derived: (1) vertex-carried
packets impossible in general (history-dependence, shown above);
(2) history-carried packets lack cross-edge compatibility guarantees
(witnesses need not compose; abstract cycles need not lift); (3) endpoint-
forced restoration (return must restore exact state) does NOT by itself
create countable paid units (restoration steps can be free). Therefore
no-double-spending is UNPROVED and, on current evidence, unprovable
without either a new vertex-expressible conserved quantity (none found;
core size is nonincreasing on S but U can grow it) or a path-functional
lower bound (blocked by q'-cancellation). Gap recorded exactly.
