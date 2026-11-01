# A single root changing DELETE loses unbounded matching credit

The global root restriction removes the old false credits at starved consumers, but changing that root can invalidate n-3 units in one A zig. Thus P fails universal DELETE, and no uniformly bounded additive correction can repair its all-valid-pair DELETE law.

## An explicit family at every n>=3

Let R_[l,h] denote the right vine on keys l through h, and use

    M=R_[2,n-1],
    A=1(empty,n(M,empty)),
    B=2(leaf1,R_[3,n]).

DELETE n has d_A=1 and a=1. B is frozen; there are no B events. The A destination is

    A'=n(1(empty,M),empty).

This is one ordinary left rotation at the A root, not a deletion of a key. All n keys and the internal shape M remain present.

The complete proper interval collections are

    C0(A) ={[2,n]} union {[k,n-1]:2<=k<=n-1},
    C0(A')={[1,n-1]} union {[k,n-1]:2<=k<=n-1},
    C0(B) ={{1}} union {[k,n]:3<=k<=n}.

There are no exact common intervals either before or after, including at n=3. Therefore F_source=F_destination=n-1. The actual one-clade replacement is [2,n]->[1,n-1]; {1} is NOT an A' subtree because node 1 has the nonempty right child M.

## Exact source matching and cover

Before DELETE, root(A)=1. Exactly the n-2 suffix intervals [k,n],3<=k<=n, are eligible B vertices. Match

    [k,n-1] -- [k,n], 3<=k<=n-1,
    [2,n]   -- {n}.

These are n-2 distinct endpoint edges. The whole eligible B side is a vertex cover of size n-2, proving maximum rank mu_source=n-2. Hence

    P_source=(n-1)-(n-2)=1.

After DELETE, root(A')=n. Every suffix interval contains n and becomes ineligible. The only eligible B vertex is {1}. It has exactly one neighbor, [1,n-1], through the minimum endpoint. That edge and the one-vertex right cover prove mu_destination=1. Consequently

    P_destination=(n-1)-1=n-2,
    Delta_DELETE P=n-3.

The required upper bound is 2a=2. Every n>=6 violates it. These are exact valid pair formulas, proved from full interval lists, matchings and covers, with no larger finite fit. Reflection gives the other orientation. At both endpoints P equals the elementary lower bound d_B(root(A)): 1 before and n-2 after. Global rematching cannot use the ineligible suffix vertices regardless of which maximum matching is selected.

## Bounded corrections and the required repair size

Suppose a correction R is defined on all valid pairs and |R|<=C for one finite constant independent of n. Then on the same family

    Delta(P+R)>=n-3-2C.

Choose an integer n>5+2C to violate the DELETE budget. Thus no such bounded correction repairs P on the full all-valid-pair source domain. Adding a function of n alone also cannot help because n is fixed on every source operation.

More precisely, ANY correction that repairs this family must obey

    R(A',B)-R(A,B)<=5-n.

For n>=6 it must supply a drop of at least n-5 during this single root zig. This is a necessary condition, not an explicit construction or a new premise installed in the CD pipeline. Unbounded structural corrections and other global potentials are not excluded. The all-size correction statement is scoped to all valid pairs; the following six-key replay separately certifies reachability of a concrete failure in the original walk domain.

## A reachable six-key failure inside an actual closed walk

At n=6 start diagonally with

    T0=2(leaf1,R_[3,6]).

The five DELETE requests D4 D6 D3 D6 D1 produce the displayed source A while leaving B=T0. The following DELETE 6 is the failed edge. Its exact data are

    a=1, q=z=0, P=1->4, Delta P=3>2.

One frozen n=6 single-tree BFS located the prefix, visiting 130 of the possible 132 trees; it fit no potential labels and built no pair graph. Both original source engines replay it exactly. The full closed word is

    D4 D6 D3 D6 D1 D6 K1 K2 K3 K4 K5 K6 K5 K4 K3 K2 K1 K2.

After the sixth request, common ascending and descending accesses synchronize both trees at R6; the final KEEP2 restores both to T0. Complete physical replay gives

    A_total=20, Q_B=0, Z_B=12.

Both actual trees return to the initial trees, and summed P changes are zero. This walk is not a Coarse-Double counterexample. The failed DELETE is zero-based position 5. The [source certificate](root_matching_certificate.json) and [independent audit](independent_audit.json) bind the full states, graphs, dual certificates, oriented events and closure.
