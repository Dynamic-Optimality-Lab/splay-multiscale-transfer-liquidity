# RC-01 Exact Low/High Weight Accounting (identities, not theorems)

Low: w(e) = 2*H_e - q_e with H_e = sum_active ceil(d_A/2) (any event kind),
q_e from terminal B-depth (floor(dB/2) bounds). Contracted high:
w(e) = 6 - q_e with shared midpoint m (E^OM_w(s,m) AND E^MO_0(m,t), same m).
Closed walk: w(C) = 2*sum H + 6*N_high - sum q. Capacities 2H_e and 6 are
FORMAL (nonnegative by construction); no physical A-cost interpretation is
claimed for the high constant beyond the compiler's w1 = 6-q definition.
Abstract q ranges are as-interpreted (no source-only bound imposed).
These identities organize the charging problem; they prove nothing about
signs by themselves.
