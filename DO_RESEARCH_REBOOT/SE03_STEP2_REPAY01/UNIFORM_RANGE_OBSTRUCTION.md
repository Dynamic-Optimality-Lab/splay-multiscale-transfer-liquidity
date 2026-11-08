# A source-exact lower bound on a uniform debt range

This is a necessary condition on a candidate potential, not an existence
theorem for that potential and not completion of Step2 or support induction.

Let r>=3 and n=2r-1. Distinguish ordered labels1,...,n with arbitrary
independent BSTs Fi in the n+1 inorder gaps. Write R_n for their right
vine and L_j for the left vine on1,...,j, keeping the same gap variables.
Use only the r odd labels as KEEP targets. Define

    W_r = K3 K5 ... Kn K(n-2) ... K3 K1,
    H_r = Kn K1 K3 K5 ... Kn K(n-2) ... K3 K1.

Both words fix R_n in B. W_r has2r-2 neighbor accesses, all depth2.
H_r has its first Kn at depth2r-2, its next K1 at depth2, its ascending
K3,...,K(n-2) at depth4, the ascending Kn at depth2, and all descending
accesses at depth2. Therefore Q(W_r)=2r-2 and Q(H_r)=4r-4.

## Universal source induction behind these identities

Splaying the largest key in an odd-length right vine gives

    n(E2,Fn),
    E_j = j((j-1)(F_(j-2),F_(j-1)),E_(j+2)),
    E_(n-1) = (n-1)((n-2)(F_(n-3),F_(n-2)),F_(n-1)).

The formula follows by bottom-up induction: after normalizing the suffix
at its maximum n, the next two outer right frames rewrite

    a(A,b(B,n(C,D))) -> n(b(a(A,B),C),D).

This is the original parent-first RR double, with C the entire already
normalized suffix. It makes no assumption about the gap BSTs.

After K1, and after each ascending odd k<=n-2 in H_r, the form is

    k(L_(k-1), (k+1)(Fk,n(E_(k+3),Fn))),              (3)

with the evident F_(n-1) terminal suffix. The next odd k+2 is reached by
RRLL. Its inner LL followed by its outer RR converts (3) into the same
form with k replaced by k+2. The final Kn uses RR, leaving the complete
left vine; each descending odd access uses LL. This proves H_r closure
by induction, conserving each gap individually. W_r uses the simpler
RR ascending/LL descending neighbor-vine induction.

## The closed preparation-and-repair schema

In W_r H_r, replace the first word's final K1 with Dn D1 K1; immediately
after the first Kn of H_r insert D2 Dn. Call the result Gamma_r. Its
26-operation r=6 instance is proved in SOURCE_OBSTRUCTION_AND_TWO_BLOCK_REPAIR.md.
The general preparation has the same fixed local normal forms. At the
end of the W_r prefix the A root is3 with left L2 and right vine4,...,n.
Dn has2r-4 right edges and costs r-2 A events. The maximum-vine induction
above yields

    n(4(3(L2,F3),E6),Fn).

D1 has exactly four left edges. It yields

    1(F0,4(2(F1,3(F2,F3)),n(E6,Fn))).                (4)

For n=5, E6 denotes F4. K1 is an A root identity. The critical Kn has
path RR and yields

    n(4(1(F0,2(F1,3(F2,F3))),E6),Fn).                (5)

D2 has path LLR, with one inner LR double and one left ZIG. Dn is then
one right ZIG. Together they convert (5) to

    n(2(1(F0,F1),4(3(F2,F3),E6)),Fn),                (6)

which is exactly the full B tree after its first Kn in H_r. All remaining
KEEPs therefore execute identically in A and B and return both to R_n.
This is full paired closure from a diagonal for every r and every Fi.

The counts, derived without any numerical instances, are

    A=(2r-3)+[(r-2)+2]+1+[2+1]+(3r-3)=6r-2,
    QF=(2r-2)+(4r-4)=6r-6,
    2A-QF=6r+2>0.                                    (7)

All r odd KEEP labels are genuine; the full core has2r-1 nodes.

Erasing3 gives recurrent right skeleton1,2,5,6,...,n with private
G=4(3(F2,F3),F4) in the gap before5. Its first retained K5 from R_n
has path RRRR; the same K5 from that recurrent skeleton has path RR.
Their full source terms coincide. Subsequent erased W_r,H_r are exactly
W_(r-1),H_(r-1) on the relabeled skeleton. Thus u=1,L=1 and

    QE_recurrent=6r-12, QE_first=6r-11,
    D_z=5, J_z=1, D_z+J_z=6.                         (8)

The B-irrelevant DELETE insertions do not alter those identities. They
are legal A splays retained under erasure, not removed preparations.

## Necessary range; no sufficiency claim

The natural full genuine macro from K1 to the critical Kn contains only
that Kn. It has H=1 and q=r-1, so its actual full weight is3-r.
If a proposed debt D_F takes values in an interval of width K and
certifies every such source macro by

    2H-q >= D_F(before)-D_F(after),

this edge requires D_F(after)-D_F(before)>=r-3, hence K>=r-3.
In particular the old fixed width2 cannot certify all full six-key macros,
and no width independent of r can certify arbitrary support by this law.

A range r-3, a HIGH threshold r-2, or a one-unit correction to auxiliary
debt is only a possible architecture. None is proved by (7)-(8). The
necessary bound contains no preservation rule for repeated signed debt
transfers and supplies no global reserve injection. Gamma_r is already
CD-safe by (7); it is not new original CD coverage.
