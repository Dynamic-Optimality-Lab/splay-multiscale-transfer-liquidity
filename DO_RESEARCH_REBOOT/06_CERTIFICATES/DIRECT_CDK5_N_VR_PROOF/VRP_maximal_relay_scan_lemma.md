# VRP maximal relay-scan lemma (PROVED — determinism + termination)

Scan: from j*+1, consume consecutive intervals satisfying (c=1,H=1,q≤2); stop
at first failure; t = count consumed; payer = next interval. Terminates (finite
s; each step advances mod s; loop bounded by s checks). Deterministic (exact
source predicates; no choices). Correct: H3 defines t as THE maximal run, H4
pins the payer as first nonbridge — the scan reproduces exactly this
decomposition. Unique: one j* (H2) ⇒ one scan ⇒ one (t,payer) pair. Distinct:
t+2≤s ⇒ t+2 consecutive mod-s indices pairwise distinct (run length ≤ s; full
t+2=s covers the cycle without repetition). t≥2 excludes S1/S2 relay shapes
(S1: successor H≥2; S2: second H≥2) — disjointness by frozen inequalities. ∎
