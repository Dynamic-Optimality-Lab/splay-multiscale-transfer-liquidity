# Step 1 — exact residual inventory identity

Status: PROVED — UNIVERSAL at the inherited raw physical scope.
Use precisely the original Psi and lambda, not a changed projection.
The construction is STEP1_PC35_RELEASE_COMPLETION.md; this file proves
its global bookkeeping without inferring a Coarse-Double sign.

## 1. Per-access physical partition

Write r_t=B_{2,t}+Z_t and define

    d_t=(B_{0,t}-r_t)_+,
    s_t=(r_t-B_{0,t})_+.

The Step 1 injection g_1 preserves g_plus and g_Z. It uses exactly
min(B_{0,t},r_t) release donors for neutral demands of t, including
the ell_t already reserved by ZRC35. Therefore at EACH t:

    paid_t = B_{1,t}+B_{2,t}+min(B_{0,t},r_t) = q_t-d_t,
    unused_B_release_t = r_t-min(B_{0,t},r_t) = s_t,
    s_t-d_t = r_t-B_{0,t}.

Let P count actual +1 A rotations and N actual -1 A rotations over W.
ND35 partitions all original A bits into nonpositive/virtual units,
A-negative release donors, B payment donors and B release donors.
Step 1 uses no first-category or A-negative release bit. Its remaining
raw pool R_1=C_A minus image(g_1) is the DISJOINT union

    (all A units not a positive-rotation bit), size 2A-P;
    (lambda images of A-negative slots),      size N;
    (unused B-release images at each t),      size sum_t s_t.

Hence the exact residual inventory is

    |R_1| = (2A-P)+N+sum_t(B_{2,t}+Z_t-B_{0,t})_+,
    |D_unfunded| = sum_t d_t.

These are physical identities: lambda is injective and surjective onto
all positive A bits, and every decrease slot has exactly one of the
specified original types. No A-negative donor is double-counted with
an A nonpositive unit: its donor is a DIFFERENT positive rotation bit.

## 2. Direct reconciliation with ND35

Put B_i=sum_t B_{i,t}, Z=sum_t Z_t. Original closure and double counting
give, exactly as in ND35,

    P=N+B_1+2B_2+Z,
    Q_B=B_0+B_1+B_2.

Subtract the remaining demand count from the remaining raw inventory:

    |R_1|-sum_t d_t
      = (2A-P)+N+sum_t(s_t-d_t)
      = (2A-P)+N+B_2+Z-B_0
      = 2A-(B_0+B_1+B_2)
      = 2A-Q_B.

Thus the global identity, in all equivalent useful forms, is

    2A-Q_B = (2A-P)+N
             +sum_t(B_{2,t}+Z_t-B_{0,t})_+
             -sum_t(B_{0,t}-B_{2,t}-Z_t)_+;

    |R_1| = 2A-Q_B+sum_t d_t;

    sum_t d_t = |R_1|-(2A-Q_B).

Also |domain(g_1)|=Q_B-sum_t d_t; subtracting this from |C_A|=2A
independently gives the second identity. No nonnegativity of 2A-Q_B
has been proved or assumed. Nonnegativity of |R_1| alone does not
imply |R_1|>=sum_t d_t.

## 3. Access-level PC35 reconciliation

For the unchanged C=S potential the total B decrease in access t is

    delta_t=B_{1,t}+2B_{2,t}+Z_t.

Consequently

    (q_t-delta_t)_+ = (B_{0,t}-B_{2,t}-Z_t)_+ = d_t,
    min(q_t,delta_t)
      = B_{1,t}+B_{2,t}+min(B_{0,t},B_{2,t}+Z_t).

Step 1 attains PC35's access-level slot count while retaining EVERY
original nonneutral payment and EVERY ZRC35 terminal assignment.
It does not recompute crossing pairings or switch potentials.

## 4. What this identity does not claim

There is no transfer of unused release capacity between B accesses.
No first-category unit, A-negative release, new donor rule or arbitrary
frozen-owner permission is used. No source-global compensation, Bank25
storage trace, Gate U, Universal CD or Dynamic Optimality claim follows.
Step 1 is complete once this raw extension and its identities are proved.
