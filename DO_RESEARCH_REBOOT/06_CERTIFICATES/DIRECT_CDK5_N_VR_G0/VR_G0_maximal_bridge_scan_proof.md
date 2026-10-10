# Maximal bridge-scan proof (deterministic membership, PROVED)

Scan: from j*+1, consume consecutive intervals with (c=1,H=1,q≤2); stop at first
failure; t = count consumed; payer = next interval. Terminates (finite s).
Deterministic (predicates are exact source values; no choices). Correct: by H3
the run after j* IS maximal-creditless by definition of t, and H4 pins the
payer as the first nonbridge — the scan reproduces exactly this decomposition.
Uniqueness: one j* (H2) ⇒ one scan ⇒ one (t,payer). Distinctness: t+2≤s ⇒ all
packet indices distinct mod s (consecutive run of length t+2 ≤ s in a cycle —
distinct unless the run wraps fully with t+2=s, in which case indices are still
pairwise distinct covering the whole cycle). t≥2 excludes S1/S2 relay shapes
(S1: successor H≥2; S2: second H≥2) — disjointness by frozen inequalities. ∎
