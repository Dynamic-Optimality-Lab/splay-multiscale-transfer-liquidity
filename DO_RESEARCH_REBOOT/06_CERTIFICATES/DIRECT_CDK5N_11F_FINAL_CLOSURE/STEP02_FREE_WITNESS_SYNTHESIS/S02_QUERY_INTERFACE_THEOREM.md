# S02_QUERY_INTERFACE_THEOREM.md — strict (s,t,w) contract (Gates A/G04/G05)

## Claim
Every Step-02 synthesis query pins exactly the Group-I allowlist (147 SLs_* +
147 SLt_* + SL_w = 295 pins, allowlist sha16 `6622c3cdd68a4861`) and nothing else.
H (SL_H), q (SLbt_q), event/mode/target/depth/path/port/inventory vars are never
assumed; bound variables cannot occur (low/high roots are quantifier-free; the
engine additionally rejects bound-name pins through the frozen API).

## Evidence
S02_PIN_AUDIT.json (allowlist hash, cone membership, no-bound proof); engine code
pins only Group-I + source-derived case splits; every evidence JSON records
`no_hidden_pins: True`; certificates' H/q are recovered from models, never inputs.
