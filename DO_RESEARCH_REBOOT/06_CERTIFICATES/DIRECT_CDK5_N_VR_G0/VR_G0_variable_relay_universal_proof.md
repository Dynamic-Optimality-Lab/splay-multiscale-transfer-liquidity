# VR universal proof L1–L8 (for every finite permitted t — no witness dependence)

## L1 (partition + baseline)

Cyclic KEEP intervals disjoint/exhaustive (each access follows one preceding
KEEP; wraparound by closure). ΣH=A, Σq=Q_B, Σc=C_K, Σw=Q_B−2C_K, ΣR=2(A−C_K).
H≥c: c=0 trivial; c=1 via A-root change (A rooted at prev KEEP key, ends at new
key; first changing access has a≥1). R≥0. Baselines distinct accesses. No-ops
(a=0) allowed — baseline is interval-level. ∎

## L2 (debt classification)

Nine-core ⇒ d_B≤8 ⇒ q≤4 (marked paths; labels may permute). c=0 ⇒ B still rooted
(same key; DELETEs freeze B) ⇒ q=0 ⇒ w=0. w>0 ⇒ c=1, q∈{3,4} ⇒ w∈{1,2}.
Q_B≤2C_K NOT claimed (nine-node +2 refutation cited). ∎

## L3 (exception)

c=1,q=3,H=1 ⇒ w=1,R=0. H=1 excludes K (needs H≥2) and P (needs two costly
accesses) universally. Genuine underfunded debt; outside CDK5NP-A. ∎

## L4 (bridges, arbitrary t)

Each bridge: c=1,H=1,q≤2 ⇒ w=q−2≤0 (covers q=0,1,2), R=0. Summation over the
run (finite t, no induction on trees — plain addition): Σw≤0, ΣR=0. Independent
of t; t=2 of the witness is one instance. ∎

## L5 (payer, full q≤3 range)

c=1,H≥2,q≤3 ⇒ w≤1 (q=0..3 ⇒ w=−2..1), R=2(H−1)≥2. Worst case q=3: w=1≤R. ∎

## L6 (relay inequality, every finite t≥2)

w_* + Σ_bridges w + w_p ≤ 1+0+1 = 2 ≤ 0+0+2 ≤ R_* + ΣR_bridges + R_p. ∎

## L7 (others)

w≤0 via R≥0; w>0 via K (H≥2⇒R≥2≥w) or P (same-interval distinct DELETE+KEEP ⇒
H≥2); overlap charged once (fixed H). Hypotheses exhaust positives outside P_*. ∎

## L8 (partition + global)

t≤s−2 ⇒ packet has t+2≤s distinct cyclic indices (no seam self-overlap:
t+2 positions among s≥t+2 slots, consecutive mod s — distinct since length ≤ s;
if t+2=s the packet is the whole cycle, still a valid partition with no
singletons). {packet}+singletons disjoint/exhaustive; packet charged once;
singletons own reserves. Σw≤ΣR ⇒ Q_B−2C_K≤2(A−C_K) ⇒ **Q_B≤2A**. Arbitrary
n/length/DELETEs/order/prefixes/seams; no packet/potential/aggregate premise. ∎
