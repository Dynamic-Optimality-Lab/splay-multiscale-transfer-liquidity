# Exact C34 definitions — no replacement policy

Authority: C34/POOLED_RETIREMENT_SOURCE_LAW.md and
C34/EXACT_GLOBAL_FEASIBILITY_MODEL.md, pinned in dependency_manifest.json.

U_m is the entire actual A-bit inventory of natural macro m. A natural
macro starts after the preceding genuine full KEEP and includes every
original operation through its terminal genuine KEEP, including DELETE,
nongenuine KEEP and zero-event gaps. Q_m is its actual full B doubles.

C_t={(t,j,b):1<=j<=a_t,b in{0,1}}; |C_t|=2a_t. For each old marked B
ancestor g of m's target, R_m includes EVERY actual A operation losing
g's ancestry of that target between the last genuine g KEEP and m.
Those intervals are the actual cyclic intervals in one closed period.
T_m=union_{t in R_m} C_t and N_m=U_m union T_m. Off-core populations and
anonymous A ancestors are not removed. DELETE never physically deletes.

For S subset M(W), let U_S=union U_m, T_S=union T_m and N(S)=U_S union T_S.
The exact quantities are

    sigma(S)=sum_{m in S}(|T_m|-Q_m),
    overlap(S)=sum_{m in S}|T_m|-|T_S|,
    local_unused(S)=|U_S\T_S|,
    delta(S)=overlap-sigma-local_unused=Q(S)-|N(S)|.

C34 LPR gives sigma>=0. It does not control overlap. Repeated references
to one C_t add no physical capacity. Relative labels transport by ONE
common occurrence bijection; the same bit is not borrowed from another
cyclic copy. A and BF splay every access/every KEEP respectively; erasure
changes only BE's processed subsequence. Costs remain ceil(dA/2),floor(dB/2).

For the fixed-owner layer, owner_stays_outside_N(S) is precisely

    |a0(D_S intersect dom(a0)) \ N(S)|.

MOP is delta(S)<=that term. These are already-paid virtual stays in the
alternative counting comparison, not free tokens. Their addition makes
MOP a different physical-layer condition from ROOT35. Neither condition
alone is the whole original source/Bank25 eligibility system.
