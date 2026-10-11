# MSINK universal payment proof L1-L7 (for the frozen JOINT H4-H5 rule)

## L1 (partition + baseline)

Cyclic KEEP intervals disjoint/exhaustive (each access follows one preceding
KEEP; wraparound by closure). Sum-H = A, Sum-q = Q_B, Sum-c = C_K,
Sum-w = Q_B-2C_K, Sum-R = 2(A-C_K). H>=c: c=0 trivial; c=1 via A-root change
(A rooted at prev KEEP key, ends at new key; first changing access has a>=1).
R>=0. No-ops allowed (interval-level). [End L1]

## L2 (debt classification)

Nine-core implies d_B<=8, so q<=4 (marked paths; labels permute). c=0 implies
B still rooted (same key; DELETEs freeze B), so q=0 and w=0. w>0 implies c=1,
q in {3,4}, so w in {1,2}. Q_B<=2C_K NOT claimed. [End L2]

## L3 (exceptions)

Each e in E: c=1,q=3,H=1, so w=1,R=0. H=1 excludes K (needs H>=2) and P (needs
two costly accesses) universally. E complete by H2 (any (c=1,q=3,H=1) IS
listed; bridge (q<=2) / payer (H>=2) / other slots reject it structurally).
[End L3]

## L4 (shared sink, full q<=4 range)

Canonical-first p not in E with c=1,H>=3 (joint rule: this p must ALSO satisfy
H5). R=2(H-1)>=4; w=q-2<=2 (exhaust q=0..4: w=-2..2). Joint: 1+1+w_p <= 2+2=4
<= 0+0+R_p (worst w_p=2 at q=4 needs R_p>=4 iff H_p>=3 - exactly the frozen
bound; H=2 would fail at q=4, which is why the threshold is three, documented).
[End L4]

## L5 (others)

j not in E+{p}: w<=0 via R>=0; w>0 via K (H>=2 implies R>=2>=w) or P
(same-interval distinct DELETE+KEEP implies H>=2); overlap once. NOTE: H5 is
checked ONLY at the selected p (the joint rule); other H>=3 intervals are
ordinary singletons (their own reserves). [End L5]

## L6 (disjointness)

{e1,e2,p} distinct (H2: e1,e2 as indices; H4: p not in E). Partition {triple} +
singletons is disjoint/exhaustive. Sink reserve spent once (even if K/P-eligible
- consumed by the joint inequality, never recharged as singleton). Exceptions
never recharged. Every StepEv in one H_j. [End L6]

## L7 (telescoping)

Relay (bridge) intervals are ordinary L5 singletons: each satisfies w<=R
individually (bridges have w<=0 by the q<=2 bound and R>=0 by L1), so no relay
arithmetic beyond per-interval charging is needed at any relay length. With the
joint triple (L4) and all singletons (L5): Sum-w <= Sum-R implies Q_B-2C_K <=
2(A-C_K) implies **Q_B <= 2A**. Arbitrary n/length/DELETEs/order/prefixes/seams;
no packet/E-S/potential/aggregate premise. Relay lengths classify membership
only. [End L7]
