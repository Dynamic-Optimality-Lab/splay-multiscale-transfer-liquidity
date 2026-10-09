# Repository map

| Area | Meaning for this reboot |
|---|---|
| IMPLEMENTATION_SPEC*, WorkPlan.md, Path.md, planning/, prereg/ | normative liquidity program and historical gates; kept read-only |
| python/independent/, python/liquidity/ | splay/cost/ledger implementations; distinguish LT costs from event counts |
| scripts/ | most current J4, cycle, transport and solver probes; many untracked; entry points often write outside the allowed folder |
| audits/ | recurrent/coarse/coupled/J4 narrative proofs and conditional-state reports |
| math/theorems/, math/proofs/, math/proof_status.json | MSTL/LIQ registry; not a proof of every later J4 claim |
| lean/WP6/ | tree mechanics and arithmetic source; no isolated build run here |
| artifacts/v04/wp6_present/0909c74a/ | finite present-domain experiments, matrices and certificates |
| artifacts/v04/wp6_present/present_domain_audit/ | occurrence masks and fixed-key closure |
| v03/history/ | preserved prior program and local papers, including L3 v3 |
| historical/ | superseded normative material |
| .git/, .lake/, .pytest_cache/ | Git/build/test state; read only; included in outside-file audit |
| DO_RESEARCH_REBOOT/ | the single permitted writable research workspace |

Sibling zip in the parent Temp directory was not extracted or modified. No alternate repository/worktree was created. No README exists at this repository root; WorkPlan/Path/specs provide the project entry documentation.
