# MSINK universal payment proof L1–L7 (for the frozen JOINT H4–H5 rule)

## L1 (partition + baseline)

Cyclic KEEP intervals disjoint/exhaustive (each access follows one preceding
KEEP; wraparound by closure). ΣH=A, Σq=Q_B, Σc=C_K, Σw=Q_B−2C_K, ΣR=2(A−C_K).
H≥c: c=0 trivial; c=1 via A-root change (A rooted at prev KEEP key, ends at new
key; first changing access has a≥1). R≥0. No-ops allowed (interval-level). ∎

## L2 (debt classification)

Nine-core ⇒ d_B≤8 ⇒ q≤4 (marked paths; labels permute). c=0 ⇒ B still rooted
(same key; DELETEs freeze B) ⇒ q=0 ⇒ w=0. w>0 ⇒ c=1, q∈{3,4} ⇒ w∈{1,2}.
Q_B≤2C_K NOT claimed. ∎

## L3 (exceptions)

Each e∈E: c=1,q=3,H=1 ⇒ w=1,R=0. H=1 excludes K (needs H≥2) and P (needs two
costly accesses) universally. E complete by H2 (any (c=1,q=3,H=1) IS listed;
bridge (q≤2) / payer (H≥2) / other slots reject it structurally). ∎

## L4 (shared sink, full q≤4 range)

Canonical-first p∉E with c=1,H≥3 (joint rule: this p must ALSO satisfy H5).
R=2(H−1)≥4; w=q−2≤2 (exhaust q=0..4: w=−2..2). Joint: 1+1+w_p ≤ 2+2=4 ≤ 0+0+R_p
(worst w_p=2 at q=4 needs R_p≥4 ⟺ H_p≥3 — exactly the frozen bound; H=2 would
fail at q=4, which is why the threshold is three, documented). ∎

## L5 (others)

j∉E∪{p}: w≤0 via R≥0; w>0 via K (H≥2⇒R≥2≥w) or P (same-interval distinct
DELETE+KEEP ⇒H≥2); overlap once. NOTE: H5 is checked ONLY at the selected p
(the joint rule); other H≥3 intervals are ordinary singletons (their own
reserves). ∎

## L6 (disjointness)

{e1,e2,p} distinct (H2: e1≠e2 as indices; H4: p∉E). Partition {triple} +
singletons is disjoint/exhaustive. Sink reserve spent once (even if K/P-eligible
— H5/L5 partition assigns p to the triple only; a K/P-eligible p is still
consumed by the joint inequality, never recharged as a singleton). Exceptions
never recharged. Every StepEv in one H_j. ∎

## L7 (telescoping)

Σw≤ΣR ⇒ Q_B−2C_K≤2(A−C_K) ⇒ **Q_B≤2A**. Arbitrary n/length/DELETEs/order/
prefixes/seams; no packet/E-S/potential/aggregate premise. Mixed relays
(short+long) need no relay arithmetic at all — relays are ϵmpty of payment
obligation beyond their own w≤R (bridges have w≤0... precisely: bridge
intervals inside E-relays are NOT separately charged; the H3 relay structure
only classifies; every bridge still satisfies w≤R individually since w≤0≤R...
wait R=0 for H=1 bridges and w≤0: w≤R=0 ⟺ w≤0 ✓). So relay members are L5
singletons. Correct as stated. ∎
