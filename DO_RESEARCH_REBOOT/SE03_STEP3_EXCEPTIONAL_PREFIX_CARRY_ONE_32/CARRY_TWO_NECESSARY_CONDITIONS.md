# Complete necessary signed mechanisms for carry two in EXC

Start with the exact debt definition. EXC begins the suffix after u with
balance-1 and E0. Thus no entry-zero or entry-two case belongs to EXC;
those are separate broader PREFIX entry classes. The only carry-two
mechanism here is cumulative additional suffix R<=-1, with all corrections.

For any genuine macro let d be its old target marked degree, and k3 the
number of its old marked ancestors of degree>=3. Original path-to-star gives

    sigma=2c-k3                 (d>=2),
          2c-1-k3               (d=1),
          2c-min(Q,2)-k3         (d=0).

The seven-mark source off-path bound is

    Q+1+beta+k3+d<=7,  k3<=beta, k3<=Q.

For H>=2, c>=2: sigma>=0 by these bounds. For H1,d>=2 the same bounds
give k3<=1 and sigma>=1. For d1, k3<=1 and sigma>=0; for d0,Q1,
k3<=1 and sigma>=0. Hence the ONLY negative macros are:

|Class|Actual source conditions|sigma|
|---|---|---|
|N1|H1, old marked leaf d0, Q>=2, exactly one degree>=3 ancestor|-1|
|N2|H1,d0,Q2,beta2,k3=2, both ancestors degree3|-2|

N1 also has Q<=4; if Q4 equality forces beta1,k3=1 and the full off-path
budget is tight. N2 follows because k3>=2 forces Q2,beta2 at seven marks.
These are NECESSARY structural classes, not independently realizable graph
states. Their path parity, SS geometry, reachable A and full core must still
be proved before using an instance. Physical marked projection alone does
not decide whether a future full access is source-valid.

Let n1,n2 count their ACTUAL occurrences in T, and let Rplus be the sum
of all positive sigma contributions. Zero edges and every original helper
remain in T. Then the exact finite-length identity is

    R=Rplus-n1-2n2.

Thus carry>=2 iff n1+2n2>=Rplus+1. Equivalently P+E(tau)<=-1. This is a
complete structurally parameterized signed-necessity list for arbitrary
finite suffix length. It is not a sufficient source-realization criterion,
not proof of Hall capacity and not a global cardinality replacement.

Other apparent mechanisms (hybrid chart switch, merged obligations,
nonidentity A flip) must contribute through their actual sigma identity or
belong to a DIFFERENT global debt coordinate. No term is silently dropped.
Within the exact inherited local coordinate they cannot create an extra
unrecorded unit. Generic repeated-interval global debt remains separate.

Status: uniform symbolic algebra/source-budget derivation; arithmetic will
be checked without compiling a new source relation. Terminal exclusion is
still the principal missing implication until proved or refuted.
