# 26AL depth/signed/capacity audit (certificate companion)

## 26AL-L1 verification record

- Exhaustive n≤8 (all shapes, all (y,r) pairs): 103100 checks, max gain **+2**;
  tight example vine-3/splay-3/key-1 (0→2, final zig-zig as grandparent).
- Random n=9,10 (6000 configs): 51026 checks, max gain +2 (no new maximum).
- Engine agreement tuple-vs-ptr (paired trials): 400/400.
- Same-side falsification of STRONGER claims: exact identity fails commonly from
  n=3; `d'=5` observed at n=6 (samples in `ak_disp.log`) — opposite-branch
  hypothesis is load-bearing for 26AK's identity but NOT needed for the +2 bound.
- Records: `06_CERTIFICATES/26AL/ak_falsify.py`, `ak_falsify.log`,
  `26AL_falsify.json`, `ak_deep.py`, `ak_deep.log/json`.

## Signed/capacity arithmetic (exact, no computation needed)

- `q_{i+2} ≤ 2` from `d'(r) ≤ h+2 ≤ 4` (L1 + `h ≤ 2` from 26AJ): δ_{i+2} ≤ 2−2a ≤ −2
  given a_{i+2} ≥ 2. With δ_i ≤ 2, δ_{i+1} = 0: triple sums ≤ 0. Exact.
- Containment C_S ⊆ C_G: `2a_{i+2}−c_i ≥ 4−2 = 2 ≥ δ_i` — G-capacity follows.
- 26AK domain ⊆ 26AL-G domain: identical H1/H2/H4/H5/capacity, minus opposite-branch.

## Witness-hunt record (bounded, all negative for novelty)

- Random closed walks (~270k sampled: 15k + 120k + 150k runs): ~135 closed,
  none with delayed triple (opposite or same-side).
- Targeted S-triples: 7419 enumerated (n=7,8 all shapes); 25 BFS-closed (8k nodes);
  0 closures. G-hunt script had a state-threading bug (VOID run — disclosed, not
  counted); fixed rerun: 15 same-side BFS, 0 closures.
- Cycle-enumeration BFS (diagonal starts): 0 returns within caps.
- Total: no same-side closed walk with S-signed triple found; no G-capacity
  same-side closed walk found. NOT proof of nonexistence (bounded effort only).

## Disclosed defect (evidence hygiene)

`akG_hunt.py` first version never advanced simulation state (missing
reassignment) and logged vacuous 100%-closure output. Caught by rate sanity
check; fixed version rerun; the void output is not cited anywhere as evidence.
Lesson recorded: closure-rate sanity check is mandatory for hunt scripts.
