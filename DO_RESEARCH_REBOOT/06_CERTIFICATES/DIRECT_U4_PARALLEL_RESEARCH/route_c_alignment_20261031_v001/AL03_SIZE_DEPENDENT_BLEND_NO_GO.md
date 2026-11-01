# Every size dependent convex blend fails the two required laws

For each n choose any theta_n in [0,1], held fixed over all states and operations of that size. Define the registered family

    P_theta(A,B) = (1-theta_n)L(A,B)+theta_n U(A,B).

No sequence of such coefficients satisfies both the DELETE and B-repayment inequalities on all sizes. In fact, for each n>=13 no coefficient works even on the following two operations from the SAME source state. This is an analytic obstruction; no coefficient or larger finite system was fitted.

## The second operation from the source family

Use the A,B of AL02, and KEEP 1. A is already rooted at 1, so a=0. B has 1 at depth one, giving q=0 and z=1. The B zig gives the right vine on 1 through n, denoted B_k. This whole KEEP has budget 2a-q=0.

Key 1 rises one B level and every other key descends one B level. For every auxiliary tree T, the exact difference is

    G(T,B_k)-G(T,B) = W(T)-2r^{d_T(1)},
    W(T)=sum_y r^{d_T(y)}.

If T is rooted at 1, then 1<=W(T)<4/3, so every such term changes by an amount between -1 and -2/3. The penalty and feasible set in L stay fixed. Maxima preserve both common bounds, proving

    -1 <= Delta_KEEP L <= -2/3.                            (3)

## The unrestricted envelope moves the other way

Every auxiliary T rooted at 1 has source score at most 1+(n-2)/3. But T=A_d is one primitive rotation from A and has G(T,B)>=n-2, so

    U(A,B) >= n-3 > 1+(n-2)/3, for n>=6.

Therefore EVERY source maximizer T* in U has root different from 1. Its weight at 1 is at most r, while W(T*)>=1. Keeping that same maximizer at the destination gives

    Delta_KEEP U >= 1-2r = 3/4.                            (4)

This reuses a source maximizer; it does not require it to maximize after the operation. It is the same all-size U failure proved in the preceding audit, included here to make the tradeoff explicit.

From (3)-(4),

    Delta_KEEP P_theta >= -(1-theta_n)+(3/4)theta_n
                       = -1+(7/4)theta_n.

Nonincrease on this KEEP therefore NECESSARILY implies

    theta_n <= 4/7.                                        (5)

This necessary inequality is not claimed sufficient for any other edge.

## DELETE requires an incompatible coefficient

The DELETE n of AL02 changes A by one primitive rotation. U is 1-Lipschitz in A in BOTH directions, hence Delta_DELETE U>=-1. Combining this with (2),

    Delta_DELETE P_theta >= (1-theta_n)ell(n)-theta_n.

For n>=6 the right side decreases with theta_n. Condition (5) consequently forces

    Delta_DELETE P_theta >= (3/7)ell(n)-4/7
                         = (2n-11)/7.

For every integer n>=13 this is at least 15/7>2, contradicting the DELETE budget. Equivalently, the DELETE necessary bound for n>=7 is

    theta_n >= (ell(n)-2)/(ell(n)+1) = (2n-13)/(2n-4),

which exceeds 4/7 as soon as n>=13. Both inequalities concern the same source A,B at that fixed n and arbitrary M. Allowing theta to depend on n cannot reconcile them.

This theorem makes no assertion for n<=12. The actual n=6 necessary interval is nonempty (AL04), so it cannot substitute for this proof. The integer 13 is a threshold of these conservative analytic estimates, not a computed least failure size.

## Scope of the exclusion

Both endpoints and all size-dependent convex blends are eliminated. The failure uses genuine whole source operations, including a KEEP with a=q=0 and an active B zig. Ignoring q=0 operations would discard a required transition.

Theta depending on A or B is outside this theorem. Such a definition adds a transition term Delta theta times U-L (with the appropriate endpoint); choosing it is a new substantive construction problem. No unproved selector, compatible labeling, all-size finite-fit premise, or surrogate potential-existence assertion is supplied as a repair. A blend that fails these stronger sufficient laws is not a counterexample to Coarse-Double or to unrelated potentials.
