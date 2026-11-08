# Exact aligned signed marginal, arbitrary genuine support

Fix any original reachable fully closed Pair Access period gamma of length N,
with r>=6 distinct genuine KEEP keys. All keys are present. Define M=G by the
sealed cyclic-root-provenance theorem, and choose any z in M. The general
identities below impose no favorable geometric condition on this choice.

Let F repeat gamma from its reached start (A0,B0). Let E use the same starting
pair and every same requested key, changing KEEP z only to DELETE z. Original
DELETEs remain DELETEs. A splays on every occurrence in both histories; its
entire trajectory, rotations, a-cost and period boundary A0 agree exactly.
B_E evolves by a deterministic one-period map on a finite fixed-key tree set.
Reuse the proved erasure closure: after u periods, choose L>=1 divisible by
its recurrent period, so B_E returns exactly after L more periods. Original
B_F returns after each period. Use precisely the aligned interval

    I=[uN,(u+L)N).

Both histories close in both full labeled trees over I. E is independently
reachable via the original reaching prefix and then its changed-mode history.
Its beginning B state need not equal B0 or B_F's; only the A states are shared.
No preperiod credits are present in I.

Let A,Q denote one original period's totals and let Q_E(I) be the actual erased
B charge on I. Define actual-block quantities

    A_I=LA, Q_F(I)=LQ,
    R_I=2LA-LQ, R_z,I=2LA-Q_E(I),
    Delta_z,I=LQ-Q_E(I).

Then source accounting, with no inequality premise, gives

\[
R_I=R_{z,I}-\Delta_{z,I}.
\]

Dividing ALL three terms by the same L yields the per-original-period identity
R=R_z-Delta_z, where R=2A-Q, R_z=2A-Q_E(I)/L and Delta_z=Q-Q_E(I)/L. An auxiliary
p_z-period total must never be compared with a single original-period total.

## Direct/indirect decomposition on the actual aligned block

Charges are pre-access source charges. On original KEEP z, E freezes B and
has charge0, whereas F has its actual q_t^F, possibly0. On original KEEP y
with y!=z, both histories splay y but their pre-access trees can differ. On
DELETE both B charges and B changes are0. Therefore exactly

\[
\Delta_{z,I}
=\underbrace{\sum_{t\in I:\,Kz}q_t^F}_{D_{z,I}}
+\underbrace{\sum_{t\in I:\,Ky,\ y\ne z}(q_t^F-q_t^E)}_{J_{z,I}}.
\]

The same formula per original period divides BOTH sums by L. D is nonnegative;
J is signed. A nongenuine original KEEP y can be genuine in E and contribute
a negative summand; a genuine original KEEP y can become a root identity in E
and contribute positively. Original nongenuine Kz has q_t^F=0. No operation,
zero event, rotation or positive A charge is dropped by this decomposition.

## Explicit transient correction

Let Q_E[0,k) denote erased B charge on the first k complete periods from the
chosen start. The aligned difference is

    Delta_z,I = LQ - Q_E[0,u+L) + Q_E[0,u)
              = ((u+L)Q-Q_E[0,u+L)) - (uQ-Q_E[0,u)).

Thus using the whole preperiod-plus-period comparison without subtracting
the transient marginal is incorrect. The same subtraction applies separately
to its direct and indirect sums. No sign is assumed for the transient term.
Once aligned, both full endpoint pairs repeat; a genuine telescoping boundary
term would cancel there, but a sum of queried depths does not telescope merely
because all final depth discrepancies repeat. Initial/transient units cannot
pay an aligned demand. All event IDs retain the copy/occurrence indices.

This proves the exact accounting and closure bridge. It does not control the
signed interference J and is not by itself a support induction.
