# Unchanged cumulative allowance after SI34 refutation

| Resource | Used | Cap | Remaining including reserve |
|---|---:|---:|---:|
| Global CPU | 4919.984375 | 7200 | 2280.015625 |
| Symbolic CPU | 1212.4375 | 1440 | 227.5625 |
| Independent CPU | 506.171875 | 600 | 93.828125 |
| Source queries | 2999999 | 3000000 | 1 |

The continuation used28 fresh source queries:11 A+3 B in core44 and
the same14 accesses in the independent mutable implementation verify87.
Symbolic source construction/closure audits do not claim numerical
Gamma or whole-period replay. No unaccepted old source was retried.
All continuation phases pass; all historical failures remain charged.

Bank25,50k batches,2m live states,4m DAG,5m edges,32GiB memory,12h wall,
global/controller5/1 reserves and all phase caps remain unchanged.
Every semantic/audit run used the accepted controller. No allowance was
reset or increased. Metadata entry/publication follows the inherited
exclusion and records its CPU separately.

The root is resolved by a mathematical source counterexample, not by a
resource-limit stopping condition. Universal original funding, owner
and Bank25 conclusions remain OPEN; no new cap request is pending.
