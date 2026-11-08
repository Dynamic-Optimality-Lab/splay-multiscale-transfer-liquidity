# ATOM35 — exact operation accounting, PROVED

Target: express every coalition contribution without duplicated tickets.
Hypotheses: exact C34 pools. Inheritance: OR34 and disjoint actual C_t.
Dual: an operation whose counted capacity differs from its real bits.
Measure/bridge: finite exhaustive indicator cases below; yields delta and
the exact removal equation used by the |S|-induction. No source sign is
assumed. This is algebra, not a new splay simulation.

Put c_t=2a_t, r_t(S)=#{m in S:t in R_m}, and h_t(S)=1 if the natural host
macro of occurrence t belongs to S, otherwise0. Zero-event operations
have c_t=0. Then

    sigma = sum_t c_t r_t - Q(S),
    overlap = sum_t c_t max(r_t-1,0),
    local_unused = sum_t c_t h_t 1[r_t=0],
    delta = Q(S)-sum_t c_t 1[r_t+h_t>0].

Proof: C_t sets are pairwise disjoint and enter each union exactly when
the stated indicator is1. For r=0, max(r-1,0)=0 and the only capacity
comes from h. For every r>=1, r-(r-1)=1 and own membership adds no new
unit. These exhaustive cases prove all formulas for arbitrary multiplicity.
OR34 ensures rotation retirement is neither lost nor invented by grouping
an operation. QED.

For m in S put p_m(S)=|N_m\N(S\{m})|. Direct cancellation gives

    delta(S)-delta(S\{m})=Q_m-p_m(S).                REM35

For any A subset S the exact cluster version is

    delta(S)=delta(S\A)+Q(A)-|N(A)\N(S\A)|.         CL35

Removing a macro reduces deficit only when its private capacity is at
least its demand. Solvency of A using all of N(A) does NOT prove this
private-capacity premise. Reserving ALL of N(A) when contracting A can
throw away unused capacity; it is not the original full owner exchange.

The source problem is to prove sufficient private or collectively
exchangeable capacity. These identities do not supply its sign.
