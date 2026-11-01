# A cheap DELETE changes the completion charge without changing terminal F

For every odd n>=7, a single A zig raises the root-completion potential by (n-1)/2 against budget2. The two terminal F values are identical, so replacing F by any scalar function of that same terminal statistic cannot repair the failure.

## Fixed analytic family

Let n=2m+1 with m>=3. Let L_[2,n-1] be the left vine on keys 2 through n-1, and use

    A^-_n=1(empty,n(L_[2,n-1],empty)), B=R_n,
    T^-_n=n(1(empty,L_[2,n-1]),empty).

DELETE n changes A^-_n to T^-_n by one root zig. The actual source costs are a=1,q=z=0 because B is frozen. The budget is2. Both source roots are1, so the source potential completion is a no-op with Q=0.

The proper source intervals are

    C0(A^-_n)={[2,n]} union {[2,k]:2<=k<=n-1},
    C0(R_n)  ={[k,n]:2<=k<=n}.

Exactly [2,n] is common, so the source terminal F is n-2. After the A zig the actual B remains R_n, but evaluating the new potential completes it at the NEW A root n. This completed tree is V_n=S_n R_n, and the evaluation charge is Q=(n-1)/2=m. This charge is not an actual B cost on the DELETE edge.

## Exact terminal sets after completion

The ordinary odd-vine RR recurrence, already proved in [CC03](../route_c_clade_correction_20261031_v001/CC03_ALL_SIZE_REPAYMENT_OBSTRUCTION.md), gives V_n root n with left-subtree right spine 2,4,...,n-1 and preceding odd singleton left children. Its proper sets consist of

    [1,n-1], {1},
    [k,n-1] and {k}, for odd k=3,5,...,n-2.

There are 2+2(m-1)=n-1 distinct proper sets. By contrast

    C0(T^-_n)={[1,n-1]} union {[2,k]:2<=k<=n-1}.

Their intersection is exactly [1,n-1]. The other T^-_n intervals all start at2, while V_n's remaining intervals start at1 or an odd key at least3. Thus the destination terminal F is ALSO n-2.

Consequently

    Phi_source=n-2,
    Phi_destination=n-2+(n-1)/2,
    Delta_DELETE Phi=(n-1)/2>2.

This proves the failure for every odd n>=7; it is not an extrapolation from a larger finite fit. The seven-key control checks the smallest member: Phi=5->8 with a=1 and budget2. Reflection supplies the opposite orientation.

The raw P source at that member is5 and destination6. At the source [2,7] is forced and the remaining prefix/suffix endpoint graph has no edges; at the destination every proper R7 interval contains the new A root7 and is ineligible. The correction R changes 0->2, creating the excessive increment even though raw P changes by only1. These graphs have direct empty matching/cover certificates, with no matching solver.

## No scalar terminal reparametrization fixes the source law

Consider ANY finite real function f_n of one scalar statistic, with arbitrary size dependence, and define

    Phi_f(A,B)=f_n(F(A,C_root(A)(B)))+Q_root(A)(B).

No monotonicity, linearity, normalization or range restriction on f_n is needed. On the SAME odd family, the two terminal F arguments are both n-2. The f_n contributions therefore cancel exactly and Delta Phi_f=(n-1)/2. At n=7 this is3 against budget2, for every f_7. Hence no member of this stated terminal-F-only class satisfies universal DELETE, despite its exact B identity.

This is a same-witness symbolic cancellation, not a fit of f_n. It does not exclude terminal functions using more joint information than F, nonminimal B reserves or general joint corrections. Introducing an unknown terminal function with the desired A law would be another unproved construction burden; no such premise is adopted here.

## Reachable seven-key source witness

Start both actual trees at R7. The fixed single-tree connector is

    D4 D1 D6 D5 D1 D7 D1.

It reaches (A^-_7,R7). The following DELETE7 is the failed edge. A single n=7 source-tree BFS located this prefix, visiting at most the complete 429-tree set; it evaluated NO potential values during search and fitted no labels. Its purpose is only explicit reachability of the already analytic all-size witness, not a larger potential-fit campaign.

The complete closed word is

    D4 D1 D6 D5 D1 D7 D1 D7 K1 K2 K3 K4 K5 K6 K7 K6 K5 K4 K3 K2 K1.

The registered failed DELETE is zero-based position7. Common ascending then descending accesses return both actual trees to R7. Independent replay gives A_total=27,Q_B=0,Z_B=12, so the walk is not a Coarse-Double counterexample. Directly recomputed potential increments sum to zero on this actual closed walk. The source certificate retains every row and inequality verdict; no assertion is made that the registered edge is its only failing edge.
