# 26AL post-gate strict-novelty certificate

## Witness (exact, source-valid)

- Keys 1..7; T0 = right vine; diagonal start; prefix `D5,D7,D3,D2`.
- Cycle-start pair states (verified exact): A `(2(1..)(3.(7(5(4..)(6..)).)))`,
  B `(1.(2.(3.(4.(5.(6.(7..)))))))`.
- 17-access closed cycle (verified closed on both trees, exact serial equality):
  `K7,K5,K1,D4,D1,D2,D5,D1,K3,K6,K5,K3,K1,D5,D7,D3,D2`.
- Per-access costs: 16/17 match the supplied table exactly; leg 16 (final
  DELETE 2) is `(a,q,δ)=(1,0,−2)`, not `(2,0,−4)` — see corrigendum below.
  Consistent totals: **A=26, Q=13, Q−2A=−39**.
- Engine cross-check (pointer vs frame implementations): **21/21 transitions
  agree** (shapes, depths, costs) — `26AL_postgate_engine_comparison.json`.

## Signed triple (cycle legs 0–2), all values measured

| Leg | Access | dA/a | dB/q | δ | role |
|---|---|---|---|---|---|
| 0 | KEEP 7 | 2/1 | 6/3 | **+1** | positive; former B-root r=1 (≠7) |
| 1 | KEEP 5 | 2/1 | 4/2 | **0** | genuine (dB>0); B-root==7 at entry; same-side (1−7)(5−7)=+12 |
| 2 | KEEP 1 | 3/2 | 2/1 | **−3** | delayed r; h=depth(r)after block0 =2; q≤2 holds |

- S1 (δ∈{1,2}): +1 ✓. S2 (genuine, y≠x,r): 5≠7,1; dB=4>0 ✓.
- S3 (δ=0 ⟺ q=2a): 2=2·1 ✓. S4 (delayed r): K1 ✓. S5 (a≥2): a=2 (dA=3) ✓.
- S6 (no side restriction; same-side verified above) ✓.
- Triple sum −2 ≤ 0; G-capacity: 1 ≤ (2−2)+(4−2) = 2 ✓.
- Global: exactly ONE positive block in all 17 (rest ≤0) ⇒ disjointness trivial;
  total −39 ≤ 0.

## Exclusions (exact)

- 26AJ: successor accesses 5 ≠ former root 1 ✓ (immediate-repayment hypothesis fails).
- 26AK: same-side (+12>0) violates opposite-branch hypothesis ✓.
- n≤6 closure: n=7 ✓. Zero-A: A=26 ✓. Bounded-depth-5: d_B(7)=6 ✓.
- Hence `γ* ∈ C_26AL-S ⊆ C_26AL-G` but `γ* ∉ C_26AJ ∪ C_26AK`;
  with banked `C_26AK ⊆ C_26AL-G`: **`C_26AK ⊂neq C_26AL-G`**. Strict extension proved.

## Corrigendum to the supplied cost table (load-bearing content unaffected)

Leg 16 (final DELETE 2): verified `(a,q,δ)=(1,0,−2)` by two agreeing engines;
supplied table said `(2,0,−4)`. All other 16 legs, both pair states, closure,
triple legs, and totals (A=26/Q=13/W=−39, which are consistent with the
CORRECTED row) check out. The S-signed triple (legs 0–2), single-positive
status, and novelty verdicts are independent of this tail row (its deficit
stays ≤0 under both readings).
