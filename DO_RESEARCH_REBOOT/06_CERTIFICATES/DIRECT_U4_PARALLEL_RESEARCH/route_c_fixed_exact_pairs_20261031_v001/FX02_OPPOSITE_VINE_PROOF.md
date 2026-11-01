# Full opposite vine repayment survives exact pair constraints

For every n>=2 the repaired function has the exact opposite-vine change -(q+1), hence pays the full q. The one-key case is a no-op. This is an all-size source calculation.

Let R_n be the right vine on 1 through n, L_n the left vine on the same keys, and V_n=S_n R_n. Use A=L_n,B=R_n and KEEP n. A is already rooted at n, so a=0; B has depth n-1 and q=floor((n-1)/2).

At the source, proper A sets are prefixes [1,k], k<n. Proper B sets are suffixes [j,n], j>1. There are no exact common sets and no equal-minimum or equal-maximum edges. Consequently

    K(L_n,R_n)=0, Ehat(L_n,R_n)=n-1.                    (3)

## Source parity recurrence

Each RR step consumes two outer right-vine ancestors k,k+1 and replaces the target's old left subtree J by (k+1)(leaf k,J). If n is odd, V_n has root n and left subtree with right spine 2,4,...,n-1 and preceding odd singleton left children. If n is even, a final zig produces left-subtree root 1 followed by right spine 3,5,...,n-1 and preceding even singleton left children. The right subtree of n is empty.

This is the actual bottom-up same-side order, not two successive rotations both promoting the target. It is the source recurrence already audited in EM02 and CC03.

## Protected match counts

Write n=2m. The only proper exact common set between L_n and V_n is [1,n-1]; fix that pair. All remaining nonleaf B vertices have maximum n-1 and minimum greater than 1. They have no residual neighbor: A's only prefix with maximum n-1 was fixed and removed, and every remaining A minimum is 1. Each remaining B leaf has one distinct even key in {2,4,...,n-2} and can match the unique A prefix ending there. There are m-1 such disjoint edges. They give both a matching and a vertex cover of size m-1, proving

    mu=m-1, K=1+(m-1)=m,
    Ehat(L_n,V_n)=(2m-1)-m=m-1.                        (4)

Write n=2m+1. The proper exact common sets are [1,n-1] and {1}; fix both. The remaining nonleaf B vertices again have maximum n-1 and minimum greater than 1 and are isolated after A's prefix n-1 is removed. The remaining B leaves have distinct odd keys in {3,5,...,n-2}; each matches its unique A prefix. The m-1 disjoint edges are all residual edges and prove

    mu=m-1, K=2+(m-1)=m+1,
    Ehat(L_n,V_n)=2m-(m+1)=m-1.                        (5)

The displayed counts still apply to n=2 and n=3: the remaining edge collections are empty, and all needed pairs are exact. Thus no asymptotic exception is hidden.

Combining (3)-(5),

    Delta_KEEP Ehat=-(q+1)<=-q, every n>=2.             (6)

At n=1 both values and q are zero; empty trees have no present-key operations. Reflection gives the opposite orientation.

For the fixed n=6 control, Ehat drops from 5 to 2 while q=2. E had dropped from 5 to 1. Protecting exact pairs consumes one unit of E's spare margin but retains full repayment at every size. The proof is by exact source shape and matching counts, not finite extrapolation.
