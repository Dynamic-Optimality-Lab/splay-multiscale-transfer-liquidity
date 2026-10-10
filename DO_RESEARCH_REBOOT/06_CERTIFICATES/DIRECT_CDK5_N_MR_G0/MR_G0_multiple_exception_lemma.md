# MR universal proof L1–L9 (for arbitrary m≥2 and all finite permitted t_e)

## MR-L1 (partition + baseline)

Cyclic KEEP intervals disjoint/exhaustive (each access follows one preceding
KEEP; wraparound by closure). ΣH=A, Σq=Q_B, Σc=C_K, Σw=Q_B−2C_K, ΣR=2(A−C_K).
H≥c: c=0 trivial; c=1 via A-root change (A rooted at prev KEEP key, ends at new
key; first changing access has a≥1). R≥0. No-ops allowed (interval-level). ∎

## MR-L2 (debt classification)

Nine-core ⇒ d_B≤8 ⇒ q≤4 (marked paths; labels permute). c=0 ⇒ B still rooted
(same key; DELETEs freeze B) ⇒ q=0 ⇒ w=0. w>0 ⇒ c=1, q∈{3,4} ⇒ w∈{1,2}.
Q_B≤2C_K NOT claimed (nine-node +2 refutation cited). ∎

## MR-L3 (exceptions)

Each e∈E: c=1,q=3,H=1 ⇒ w=1,R=0. H=1 excludes K (needs H≥2) and P (needs two
costly accesses) universally. All exceptions enumerated (E complete by
definition); VR-singleton walks excluded by m≥2. ∎

## MR-L4 (bridges, arbitrary t_e)

Each bridge: c=1,H=1,q≤2 ⇒ w=q−2≤0 (q=0,1,2 exhausted), R=0. Finite summation
per exception (plain addition, no tree induction): Σw≤0, ΣR=0. Independent of
t_e. ∎

## MR-L5 (payers, full q≤3 range)

Each payer: c=1,H≥2,q≤3 ⇒ w≤1 (q=0..3 ⇒ w=−2..1), R=2(H−1)≥2. ∎

## MR-L6 (per-packet solvency, every e and permitted t_e)

w_e+Σ_bridges+w_p ≤ 1+0+1 = 2 ≤ 0+0+2 ≤ R_e+ΣR_bridges+R_p. Joint charge, once
per packet. ∎

## MR-L7 (global disjointness)

H5 gives pairwise disjoint P_e (verified index sets incl. wraparound; no shared
payer/bridge; no second exception inside). Summation over the packet family:
Σ_{e}Σ_{P_e}w ≤ Σ_{e}Σ_{P_e}R (finite sums; no matching/allocation problem —
packets are disjoint by hypothesis). ∎

## MR-L8 (others)

j∉P: w≤0 via R≥0; w>0 via K (H≥2⇒R≥2≥w) or P (same-interval distinct DELETE+KEEP
⇒H≥2); overlap charged once. Hypotheses exhaust positives outside packets. ∎

## MR-L9 (partition + telescoping)

Disjoint packets + singleton rest partition all cyclic indices ⇒ Σw≤ΣR ⇒
Q_B−2C_K≤2(A−C_K) ⇒ **Q_B≤2A**. Arbitrary n/length/m/t_e/DELETEs/order/prefixes/
seams; no packet/potential/aggregate premise. ∎
