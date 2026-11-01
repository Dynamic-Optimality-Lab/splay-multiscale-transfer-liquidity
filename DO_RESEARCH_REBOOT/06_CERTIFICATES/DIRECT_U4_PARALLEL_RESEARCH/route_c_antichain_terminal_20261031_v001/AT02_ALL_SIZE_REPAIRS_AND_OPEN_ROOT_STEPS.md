# Both known all-size DELETE obstructions are repaired and root steps remain open

The antichain terminal function repairs the two analytic DELETE families, not just their finite samples. A source decomposition then reduces the remaining universal DELETE proof for this fixed potential to root accesses at A depth1 or2. That root-step inequality is OPEN and is not assumed.

## Equal-root right-vine-middle family

For n>=4 use

    A_n=1(empty,n(R_[2,n-1],empty)), B=R_n,
    T_n=n(1(empty,R_[2,n-1]),empty).

At the source the roots agree, exactly [2,n] is common and F=n-2. After fixing it, the nonzero endpoint edges are [k,n-1]--[k,n],3<=k<=n-1. Their B vertices form one nested chain. At least one edge exists, and no two selected right intervals can be disjoint. Hence alpha_source=1 and

    K_source=Phi_source=n-3,
    R_source=K_source-P_source=n-4,

using the previously proved P_source=1. This is an unbounded reserve on equal-root, internally different pairs.

DELETE n is one A zig, giving A=T_n while B stays R_n. The potential completes B to V_n=S_n R_n. The actual operation still has a=1 and q=z=0.

For even n=2m, the proper V_n intervals shared with T_n are [1,n-1] and the suffixes [k,n-1] at even k=2,4,...,n-2. There are m common sets. The residual T_n suffixes have odd minima, while all residual V_n intervals are singletons at even keys below n-1. Their endpoint graph has no edges. Thus alpha=0, K=m-1 and Q=m-1, giving Phi_destination=n-2.

For odd n=2m+1, the shared intervals are [1,n-1] and suffixes at odd k=3,5,...,n-2, again m sets. Residual T_n suffixes have even minima; residual V_n singletons are1 and odd keys below n-1. Again there are no residual endpoint edges. Now K=m and Q=m, giving Phi_destination=n-1.

Therefore the one-zig increment is1 for even n and2 for odd n, both within budget2. These are direct parity/interval counts using the source RR recurrence, not extrapolation from six- and seven-key checks.

## Odd left-vine-middle family

For n=2m+1>=7 use the previous CP obstruction

    A^-_n=1(empty,n(L_[2,n-1],empty)), B=R_n,
    T^-_n=n(1(empty,L_[2,n-1]),empty).

At the equal-root source, [2,n] is the only common interval and the residual prefix/suffix endpoint graph has no edges. Thus alpha_source=0 and Phi_source=F_source=n-2=2m-1.

After DELETE n, completion is V_n. Exactly [1,n-1] is common and terminal F=2m-1. The residual A intervals are prefixes [2,k]. The residual B singleton {1} is isolated. All other residual B intervals lie in the right-comb subtree on keys3,...,n-1, whose B leaves are the m-1 odd keys3,5,...,n-2.

Any antichain of these active B subtrees has at most m-1 members: choose one B leaf inside each selected subtree; disjointness makes those leaves distinct. Conversely match each singleton {k}, for odd k=3,5,...,n-2, to the distinct A prefix [2,k]. These m-1 disjoint endpoint edges attain the bound. Hence alpha_destination=m-1,

    K_destination=(2m-1)-(m-1)=m,
    Phi_destination=K_destination+Q=m+m=2m=n-1.

The formerly unbounded increment is now1, within budget2. At n=7 the terminal F values remain5 at both ends, but K changes5->3 and Phi changes5->6. This is the structural distinction unavailable to any scalar f_n(F).

## Exact reduction to root steps

Define the following fixed-candidate root-step condition for EVERY finite valid A,B and present x with d_A(x) in {1,2}. Write r=root(A) and A'=S_x A. Require

    K(A',S_x B)-K(A,S_r B)+Q_x(B)-Q_r(B)<=2.           (R)

There are two zig orientations and four double types at the A root. All B shapes and all hanging fringes remain quantified. Condition (R) is OPEN; the finite controls do not prove it.

If (R) holds universally, the full DELETE bound for this Phi follows. During bottom-up A splay, all primitive rotations before the final StepEv preserve the GLOBAL A root. B is frozen, so their completion S_r B and charge Q_r(B) stay fixed; AT01's terminal theorem bounds each such primitive increment by1.

For even A depth d>=2, there are d-2 internal primitive rotations and a final root double. Applying (R) to the final depth-two state gives total increment at most(d-2)+2=d=2a. For odd d>=1, there are d-1 internal primitive rotations and a final root zig, giving at most(d-1)+2=d+1=2a. Depth0 is a no-op. This uses the actual source same-side order and counts the final double jointly.

Conversely universal DELETE implies (R), because a depth-one or depth-two access has exactly one A StepEv and budget2. Thus, given the proved fixed-C stability, universal DELETE for this explicit candidate is equivalent to (R). The source domain has been reduced from arbitrary A depth to1 or2; no unknown potential function has been substituted.

## The first unsupported implication

The fixed-C matching proof preserves residual antichains when only A changes. It gives no bound for changing the right completed tree from S_r B to S_x B at the same time. The charge difference Q_x(B)-Q_r(B) can be unbounded even for an A root child. A proof must relate lost and gained antichain coupons across those different completed B trees, including changes in forced exact pairs and shared left capacities. Counting coupons independently or silently replacing S_x B by S_x S_r B would not establish (R).

This audit has not proved that exchange estimate and has found no counterexample in the frozen controls/word. It therefore stops with universal DELETE OPEN. Condition (R) is recorded as the first unsupported lemma, not an additional assumed theorem in the original CD pipeline. If it were proved, the already established exact B law for the SAME Phi would give the original whole source bound and closed telescoping; that conclusion remains conditional.
