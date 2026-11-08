# Uniform signed preservation for actual A-only preparation distances

Let K be any finite physical key set with |K|>=4. For full BSTs T,U on K,
define ell(T,U) as the minimum total ORIGINAL A StepEv cost of an ordinary
bottom-up splay word transforming T to U. All requests in this auxiliary
definition are A-only. The inspected Levy--Tarjan transformation theorem
ensures the set of such words is nonempty. Nonnegative integer costs give
an attained finite minimum. No hypothetical word supplies physical credit
to a source being studied; ell is only a source-state accounting quantity.

For any fixed0<=lambda<=1 define

    Phi_lambda(A,B)=2lambda*ell(A,B)-2(1-lambda)*ell(B,A).

THEOREM. Every ORIGINAL DELETE access, of actual A cost a, satisfies

    2a+Phi_lambda(A_after,B)-Phi_lambda(A_before,B)>=0.

PROOF. Concatenating this actual access with a minimizing word gives

    ell(A_before,B)<=a+ell(A_after,B),
    ell(B,A_after)<=ell(B,A_before)+a.

Multiply the first rearranged inequality by2lambda and the second by
2(1-lambda), then add. Their nonnegative coefficients give precisely the
asserted source inequality. If a=0 then the access repeats A's root, the
state is identical, and equality holds. No operation or physical key is
deleted by this argument. QED, uniformly in K, anonymous A ancestors,
private populations, access multiplicity and both orientations.

Phi_lambda(A,A)=0. This uses ACTUAL splay-event preparation distance, not
the previously refuted distance in arbitrary single rotations. It can be
negative; on a fixed finite key set it has finite range and can be shifted
by a constant without changing any margin. A support-only range bound is
not asserted. A private-population-dependent range is not silently treated
as an allowed Bank25 carry bank.

Missing target: genuine KEEP or whole-natural-packet preservation,

    2H-Q+Phi_lambda(after)-Phi_lambda(before)>=0.

The directed triangle inequalities above do not prove that assertion.
A source-exact failure on a synchronized natural packet refutes the stated
family as a natural-packet license, even though its A-only theorem remains
valid. A state-dependent lambda or an extra chart correction requires a new
proof; it is not covered by this theorem. Natural packet grouping could
also give a different sufficient architecture and is not refuted by failure
of the unchanged-packet family. C33 and universal funding remain OPEN.
