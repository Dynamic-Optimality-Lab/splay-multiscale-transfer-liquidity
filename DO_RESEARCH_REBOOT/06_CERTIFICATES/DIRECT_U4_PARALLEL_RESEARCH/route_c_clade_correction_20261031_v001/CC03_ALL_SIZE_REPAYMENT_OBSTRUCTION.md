# Full B repayment and every scalar rescaling fail

The corrected potential F lowers by only one or two on an opposite-vine starved KEEP, even though q grows with n. This refutes full B repayment for every n>=6. A diagonal DELETE then excludes every scalar rescaling c_n F, even if its coefficient is chosen separately for each size.

## Opposite vines

Let R_n be the right vine 1,2,...,n, rooted at 1. Let L_n be the left vine n,n-1,...,1, rooted at n. Their subtree sets are respectively all suffix intervals [k,n] and all prefix intervals [1,k]. For n>=2 their only shared set is the full set, so

    F(L_n,R_n)=n-1.

Take A=L_n, B=R_n and KEEP n. A is already rooted at n: a=0. B has depth n-1, hence q=floor((n-1)/2) and z=(n-1) mod 2. Denote V_n=S_n R_n.

The source RR recurrence is explicit. When two outer right-vine ancestors k,k+1 are consumed, the rebuilt target remains n and its old left subtree J is replaced by

    (k+1)(leaf k,J).

For odd n the final left subtree of V_n has a right spine 2,4,...,n-1, with the preceding odd singleton attached at each left child. For even n there is one final zig at 1: the final left subtree has root 1, then right spine 3,5,...,n-1, with singleton 2,4,...,n-2 at their left children. V_n has root n and empty right subtree in both cases.

For n>=3, the proper prefix sets shared by L_n and V_n are exactly:

| Parity | Newly shared proper prefix sets | Count m_n |
| --- | --- | --- |
| n even | [1,n-1] | 1 |
| n odd | [1,n-1] and {1} | 2 |

Every other right-spine subtree has minimum at least 2, and every other singleton has key at least 2, so none can be a prefix [1,k]. The two sets in the odd row are distinct for n>=3. Thus the exact source change is

    Delta_KEEP F=-m_n.

For even n>=6, q=(n-2)/2>=2>m_n=1. For odd n>=7, q=(n-1)/2>=3>m_n=2. Hence Delta F>-q for EVERY n>=6. This is an all-size algebraic proof, not extrapolation from the fixed six- and seven-key controls. The mirrored counterexample follows by reversing key order and interchanging children.

## Scalar rescaling cannot fix the deficit

Let c_n be ANY real number fixed over all states and operations of size n, and consider Psi_c=c_n F, or equivalently R_c=c_n F-G. The preceding KEEP necessarily requires

    c_n >= q/m_n.                                       (9)

Now use the diagonal source (R_n,R_n) and DELETE n. The destination is (V_n,R_n). All proper V_n subtree sets exclude n; all proper R_n sets contain n. They share only the full set, so

    Delta_DELETE F=n-1,
    2a=2 ceil((n-1)/2).

The DELETE bound therefore necessarily requires

    c_n <= 2 ceil((n-1)/2)/(n-1).                       (10)

For odd n>=7, (10) gives c_n<=1 while (9) gives c_n>1. For even n>=6, (10) gives c_n<=n/(n-1)<=6/5 while (9) gives c_n>=(n-2)/2>=2. These constraints are disjoint at every n>=6. They use the same size and a single coefficient, so size dependence does not help. They are necessary inequalities, with no coefficient fitted.

This refutes unit F and its complete registered scalar family. It does not refute arbitrary corrections, variable subtree-set weights, state-dependent functions, or unrelated nonlinear mechanisms. No such alternative is asserted or launched.

## Source reachability and exact closure

The starved pair (L_n,R_n) is reached from the diagonal (R_n,R_n) by DELETE 2, DELETE 3,...,DELETE n. Each is a single right-child zig in A. Thus all counterexamples are physical reachable source states without a separate reachability theorem.

For every n>=6 an explicit closed source word from the right-vine diagonal is

    D2 D3 ... Dn ; Kn ; K1 K2 ... Kn ; K(n-1) K(n-2) ... K1.

The first block reaches (L_n,R_n), then Kn is the failed edge. An ascending pass 1 through n transforms ANY present-key BST into L_n: after the pass has accessed k, the accessed prefix is the left spine k,k-1,...,1; promoting the next successor retains that spine below its new root. A descending pass analogously yields R_n. Therefore the last two blocks restore the diagonal exactly. This connector argument asserts endpoints only, not a sign or cost bound.

CC04 independently replays the n=6 word. Its totals obey Coarse-Double. Refuting the candidate's edge inequality does not refute the original closed-walk theorem.
