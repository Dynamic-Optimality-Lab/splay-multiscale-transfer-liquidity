# Cyclic interval proof + A-root-change baseline (L1/L2a)

## Partition (L1)

KEEP occurrences cut the cyclic access sequence; I_j = accesses strictly
after K_{j-1} through K_j (wraparound for j=0 by closure). Every access has
exactly one KEEP at-or-after it, so membership is unique and exhaustive.
Summation gives ΣH=A, Σq=Q, Σc=C_K, hence Σw=Q−2C_K, ΣR=2(A−C_K). Verified
on IN (56/36/16) and OUT (53/36/16) by fresh replay.

## Baseline H≥c (L2a)

c=0: H≥0=c trivially. c=1 with H=0: all a_t=0 in I_j, i.e., d_A=0, i.e.,
targets the current A-root. Splaying the root is a structural no-op, so the
A-tree (hence its root) never changes during I_j. The root at I_j's start is
x_{j-1} (the preceding KEEP splayed it there). The terminal KEEP therefore
targets x_{j-1}, contradicting x_j≠x_{j-1}. Hence c=1 ⇒ H≥1=c. So
R=2(H−c)≥0 for every interval, with no-ops and arbitrary DELETEs allowed.
(IN: all 16 intervals satisfy H≥c; OUT: all 16 satisfy it; verified.)
