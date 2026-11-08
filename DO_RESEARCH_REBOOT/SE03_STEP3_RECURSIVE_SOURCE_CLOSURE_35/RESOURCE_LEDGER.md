# Unchanged cumulative research allowance

| Resource | Used | Cap | Remaining including reserve |
|---|---:|---:|---:|
| Global CPU | 4917.140625 | 7200 | 2282.859375 |
| Symbolic CPU | 1211.25 | 1440 | 228.75 |
| Independent CPU | 504.515625 | 600 | 95.484375 |
| Source queries | 2999971 | 3000000 | 29 |

New C35 queries32:16 actual A splays in core43,16 in verify84. BF/BE
primitive states were reused from the accepted source, with exact identity
checks; no new B replay was disguised. All other C35 phases use zero
fresh primitive queries. No optional C34 failed construction was retried.
All new phases pass; historical failures stay cumulatively charged.

Bank25,50k batch,2m live states,4m DAG,5m edges,32GiB memory,12h wall and
5/1 global/controller reserves are unchanged. Every semantic/audit phase
uses the original accepted controller (default20-second new phase cap).
Metadata-only entry/publication follow the inherited exclusion and record
their CPU separately. No budget is reset or increased; no parallel
controller or implicit allowance is used.

The terminal blocker is mathematical, not resource exhaustion. More
passing finite controls would not close the remaining source implication.
No cap renewal is requested. The exact charges are in resources_checkpoint.json.
