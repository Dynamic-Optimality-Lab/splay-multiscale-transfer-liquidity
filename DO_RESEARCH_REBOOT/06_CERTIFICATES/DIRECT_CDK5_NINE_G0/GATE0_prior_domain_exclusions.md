# GATE0 prior-domain exclusions — DECISIVE FINDING: banked 26AM-G COVERS

Witness: 15-access nine-core walk, sole positive block K3 (idx 2: dA=2, dB=6,
a=1, q=3, δ=+1, genuine, former B-root r=9, h=depth(9)-after-K3=2).

## Analytic AJ–AM audit (from authoritative trace)

- **26AJ: EXCLUDED.** Successor K7 key 7≠9.
- **26AK/26AL-G: EXCLUDED.** Second successor K1 key 1≠9 (capacity moot).
- **26AM-G: COVERED.** Packet {K3,K7,K1,K9} (blocks 2,3,4,5, distinct, m=15):
  G1 δ=+1 ✓; G2 K7,K1 genuine B-changing, keys 7,1≠9 ✓; G3 δ=−4,−2≤0 ✓;
  G4 block led by KEEP(9) ✓; G5 2a=4≥c=3 (h=2) ✓; G6 1≤4+2+1=7 ✓; G7 no
  geometry ✓. Only positive in walk; all others nonpositive ⇒ walk satisfies
  the 26AM-G global class. **This is a proved banked domain (26AM-G/S PROVED;
  only the AM gate's novelty was Outcome B).**
- 26AM-S: excluded (intermediates −4,−2 ≠ 0). 26AL-S: excluded (no S triple).
- Charter §9's AM bullet ("not a permitted B-frozen return configuration") is
  **incorrect**: banked G2 REQUIRES genuine intervening B splays — exactly what
  K7/K1 supply. The deeply-negative intermediates (δ=−4,−2) that motivate Type
  K/P are precisely what satisfy AM-G capacity with margin 7≥1.

## Executable recognizers (authoritative, unmodified)

26AO REJECT · 26AP bad-return REJECT · 26AQ REJECT · 26AR REJECT · 26AS REJECT.
(These cover AN–AS only; none tests 26AM-G, which has no executable recognizer
and was audited analytically above.)

## Baselines + cardinality

n=9 keys (n≤6 ✗), K3 dB=6 (depth≤5 ✗), A=28 (zero-A ✗). RT2-A/CDK4-A N/A (5
keys). CDK5L-A N/A (core 9>8).

## Consequence

γ* ∈ C_26AM-G ⊆ C_old. Strict novelty fails. **Rule 4: FAIL.** No replacement
witness permitted in this prompt. Outcome CDK5N-G0-C.
