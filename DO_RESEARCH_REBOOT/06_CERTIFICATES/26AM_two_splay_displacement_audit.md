# 26AM audit: displacement probe + hunt record (OUTCOME B — coverage open)

## L1 composition probe (supporting only; proof is analytic apply-twice of 26AL-L1)

- Exhaustive n≤7 (all T0 shapes × all splay pairs × all tracked keys) + random n≤10.
- 216884 checks; every two-splay depth change d'−d ≤ 4; max EXACTLY +4.
- Tight example: n=5, splays 3 then 5, tracked key 1: depth 0→4.
- No stronger two-splay constant claimed; probe corroborates, does not prove.

## Local signature arithmetic (no obstruction)

- Block i (1,3,+1): needs d_B∈{6,7}, d_A∈{1,2} — realized individually (26AJ witness has (1,3)).
- Blocks i+1,i+2 (1,2,0): need d_B∈{4,5}, d_A∈{1,2} — arithmetically plausible.
- Block i+3: a≥2, q≤3 (displacement) ⟹ δ≤−1 — plausible.
- No local arithmetic obstruction to the (1,0,0,−1) signature found.

## Bounded hunt record (negative; NOT a refutation)

- Script: `DO_RESEARCH_REBOOT/06_CERTIFICATES/26AM/am_hunt.py`; log: `am_hunt.log`.
- Bounds honored: n=7..10; T0s vine + 7 shapes; prefixes ≤3; ONE search script;
  histories=3758 (≤100000); quad-BFS whitelist triedBFS=12; no replay verifier
  needed (no candidate to replay).
- Result: 0 closures (WIN=False). Per charter §22 this does NOT refute the
  signed-displacement walk form; the gap is closure luck, not a proved obstruction.

## §15 realizability levels

- Algebraic consistency of (1,0,0,−1) with capacities: ✓.
- Local-state feasibility of all four blocks jointly: plausible, NOT exhaustively proved.
- Diagonal full-config reachability + nonpositive closure: ✗ NOT found.
