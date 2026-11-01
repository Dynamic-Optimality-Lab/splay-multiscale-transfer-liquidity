# The envelope has the universal DELETE law but loses B repayment

## 1. Universal A-motion law

Each function A->G(T,B)-rho(A,T) is1-Lipschitz in the rotation metric by triangle inequality. The maximum over T is therefore1-Lipschitz:

    |Psi(A',B)-Psi(A,B)| <= rho(A,A').

Taking T=A also proves Psi>=G>=0. Since G(T,B)<(4/3)max_y d_B(y), Psi is finite with range allowed to grow with n. It is the least1-Lipschitz majorant of G in the A variable: any such majorant dominates every term G(T,B)-rho(A,T), hence dominates their maximum.

An ordinary source splay from A to S_xA uses exactly d_A(x) primitive rotations. Thus

    Psi(S_xA,B)-Psi(A,B) <= d_A(x) <=2 ceil(d_A(x)/2).

This proves the required DELETE inequality for EVERY finite A,B and present x.

If the root-conditioned B-splay law also held for Psi, the actual A-then-B execution of a KEEP would give the whole source bound by addition. There is no extra unknown capacity theorem. But the B law is false.

## 2. Analytic counterexample for every n>=6

Use the same A,B family as SP02: A root1, its right child n, arbitrary M on2..n-1 below n.left; B root2,left child1,right vine3..n. Access x=1 with KEEP. Then a=0, d_B(1)=1, q=0,z=1. The required potential change is<=0.

Let T* maximize the SOURCE value G(T,B)-rho(A,T). We first show root(T*)!=1.

For any T rooted at1, its root contribution is d_B(1)=1. The remaining A-style weights total<1/3, and every B depth is<=n-2. Therefore

    G(T,B)-rho(A,T) <=1+(n-2)/3.

On the other hand, let Tn be obtained from A by the single root zig splaying n. Its rotation distance from A is1 and its G value is at least d_B(n)=n-2. Hence

    Psi(A,B) >= n-3.

For n>=6, n-3>1+(n-2)/3. Every maximizing T* is therefore rooted away from1.

After the B zig at1, key1 rises one level and EVERY other B key descends one level. For ANY T rooted away from1, r^{d_T(1)}<=r while total weight is>=1. Consequently

    G(T,S_1B)-G(T,B)
      = sum_y r^{d_T(y)} -2r^{d_T(1)}
      >=1-2r=3/4.

Evaluate the DESTINATION maximum at the old maximizer T*. The metric penalty uses the same A and cancels:

    Psi(A,S_1B) >= Psi(A,B)+3/4.

This violates the required nonincrease for a=q=0. The failure is a genuine legal whole KEEP, not a proposed micro-step condition or a mismatched symbolic endpoint. It is analytically uniform in n>=6 and arbitrary M. A fixed n6 source replay embeds it in an exactly closed Pair Access walk from a diagonal.

Mechanism: the Lipschitz maximum suppresses expensive A-root changes by allowing a different auxiliary root to dominate the reserve. That root does not equal the access target. Its positive bystander motion reverses the raw reserve's target-conditioned repayment. The same maximizing T can be reused at the destination, so no compatibility or existence gap remains in the contradiction.

## 3. Same-family parameter corollary, without tuning or another search

For any fixed0<r<1/4 and fixed metric coefficient lambda>=0, the envelope max_T[G_r(T,B)-lambda rho(A,T)] fails for sufficiently large n. Put s=2r/(1-2r)<1. Root1 candidates score at most1+s(n-2), while the one-rotation root-n candidate scores at least n-2-lambda. Choose (1-s)(n-2)>1+lambda. A maximizing root is again different from1, and the B zig increases its score by at least1-2r>0.

This is an immediate algebraic corollary of the same witness, not a parameter fit or a second campaign. The fixed audited candidate remains r=1/8,lambda=1. No replacement parameters were tested.

## 4. Scope

This refutes this explicit least-majorant construction and the stated fixed-parameter family. It does not refute every A-Lipschitz potential, every possible nonlinear repair, an unbounded structural reserve, or Route C. Pointwise domination Psi>=G does NOT preserve transition differences. A larger majorant could have different differences; no such construction is asserted.

The raw positive lemmas and the envelope's positive DELETE lemma are separate true statements. Combining them across two different functions is invalid. Universal Coarse-Double remains OPEN.
