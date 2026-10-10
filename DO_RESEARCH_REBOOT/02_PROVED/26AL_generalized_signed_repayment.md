# 26AL: universal one-splay displacement + generalized/signed repayment (PROVED)

**Status: PROVED** — three universal statements (structural bound, generalized
repayment, signed repayment) with exact proofs. Strict same-side closed-walk
coverage is NOT established here (witness hunt negative within budget; outcome B).

## 26AL-L1 — universal one-splay depth displacement (PROVED)

For every finite valid BST B and present keys y ≠ r: `d_{S_y(B)}(r) ≤ d_B(r)+2`,
where S_y is ordinary bottom-up splay (authoritative rotations:
`scripts/wp6_eventflow.py:111-182`; identical cases in
`python/independent/splay.py:92-152`).

Proof (frames, exact). Bottom-up splay consumes search-path frames
innermost-first, two per double operation (single final zig only when the depth
is odd); consecutive operation sites lie exactly two levels apart. A node r is
affected only by operations consuming its region. On first consumption r sits at
relative depth ≥0 to the operation site and reattaches at relative depth ≤3
(LL/RR far-sibling slot; +2 or less elsewhere), and strictly below-site cases
give at most +2 overall: in every rotation case the increase is ≤+2 with the
site top as reference. On every LATER operation, r lies strictly below the new
operation site (sites ascend by exactly 2; rebuilt units root at y≠r), so with
reattach roles ≤+3 the change is ≤0. Hence at most +2 once, never again;
`d'(r) ≤ d(r)+2`. Tight: vine-3 splay-3 moves key 1 from 0 to 2 (final zig-zig
as grandparent). Absent keys no-op (engine returns unchanged); pair-access
present-key scope assumed.

Corroboration (supporting only): 103100 exhaustive n≤8 + 51026 random n≤10 =
154126 checks, max gain exactly +2; tuple-vs-ptr engine agreement 400/400.
Same-side configurations CONFIRM the bound holds there too (this is a universal
inequality); what fails same-side is only 26AK's stronger exact identity
(counterexamples measured, d'=5 observed).

## 26AL-G — generalized repayment (PROVED)

Same 26AK three-block setup, H1/H2/H4/H5 and capacity H6 as stated in the gate
prompt §8, but NO opposite-branch hypothesis (H3 dropped). By 26AL-L1,
`d'(r_i) ≤ h_i+2` after the intervening splay (h_i ≤ 2 from 26AJ), so
`q_{i+2} ≤ c_i = floor((h_i+2)/2) ∈ {1,2}`, giving δ_{i+2} ≤ c_i−2a_{i+2} ≤ 0.
Then δ_i+δ_{i+1}+δ_{i+2} ≤ 0 by H5+H6 exactly as in 26AK. Disjointness,
wraparound, m=1,2 degenerates: identical combinatorial proof (shared slot-≥1
block forced nonpositive; self-overlap makes positivity jointly inconsistent).
Hence Q_B ≤ 2A on the stated class. 26AK domain ⊆ 26AL-G domain (fewer
hypotheses, same rest) — non-strict inclusion PROVED.

## 26AL-S — signed repayment (PROVED)

Under S1 (δ_i∈{1,2}), S2 (genuine intervening splay), S3 (δ_{i+1}=0, i.e.
q_{i+1}=2a_{i+1}), S4 (delayed r-access), S5 (a_{i+2}≥2), S6 (no side
restriction): q_{i+2} ≤ 2 (L1 with h≤2) gives δ_{i+2} = q_{i+2}−2a_{i+2} ≤ −2;
with δ_i ≤ 2 and δ_{i+1} = 0, the triple sums ≤ 0. Disjointness as above.
Containment C_S ⊆ C_G: δ_i ≤ 2 ≤ 0 + (2a_{i+2}−c_i) since 2a_{i+2}−c_i ≥ 4−2 = 2
(a≥2, c≤2) — the G-capacity follows automatically. So 26AL-S closed walks
satisfy 26AL-G hypotheses; both theorems proved.

## Scope (exact)

26AL-G/S cover closed walks whose every positive block meets the stated
H/S-conditions (single-intervening-splay, capacity/signed arithmetic,
disjoint triples). NOT covered: multi-splay delays, deficits beyond capacity,
indirect repayment, unrestricted Coarse-Double. No J4/ROW claim. Strict
same-side novelty (C_26AK ⊂neq C_26AL-G with witness) NOT established here.
