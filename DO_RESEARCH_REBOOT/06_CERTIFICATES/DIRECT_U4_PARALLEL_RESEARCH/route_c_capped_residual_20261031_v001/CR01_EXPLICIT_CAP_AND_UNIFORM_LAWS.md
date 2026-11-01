# Capping the residual discount pays the named starved KEEP

One explicit repair pays the previously failing six-key starved KEEP while retaining universal DELETE, all-size opposite-vine repayment and both established arbitrary-fringe whole-helper laws. It remains a refuted universal potential: CR02 exhibits another required B edge and an architectural obstruction.

## Definition and source conventions

Use the same finite ordered key set in both trees, with present-key accesses and edge depths. KEEP x splays A and then B; DELETE x splays A and freezes B. DELETE does not remove a node, so the key count n is fixed on every edge. The source costs are a=ceil(d_A/2), q=floor(d_B/2) on a KEEP and q=0 on DELETE. The desired whole-edge upper bound is 2a-q.

For n>=1 put N=n-1. Let c be the number of exact common proper subtree key sets. In the endpoint graph, min is compared with min and max with max. Fix all exact pairs first, remove their vertices, and let mu be the maximum residual matching cardinality. The existing functions are

    F=N-c,
    Ehat=N-c-mu=F-mu.

They are explicit functions of the present physical pair. Define

    t_n=max(0,floor(n/2)-2),
    J(A,B)=max(Ehat(A,B),F(A,B)-t_n)
          =F(A,B)-min(mu(A,B),t_n).                    (1)

Set J=0 at the empty pair. Thus Ehat<=J<=F. Relative to Ehat, the explicit correction is

    J-Ehat=max(0,mu-t_n).

The formula caps the matching discount subtracted from F. No potential labels, coefficients or selectors are fitted. The cap is derived from the exact opposite-vine requirement below. Pointwise comparisons alone are not used to transfer source laws.

## Universal DELETE

For one primitive A rotation with B frozen, F and Ehat each change by at most one in absolute value. For F this follows because exactly one proper subtree key set is replaced. For Ehat the constrained rematching argument in FX01 accounts for the changing exact-pair requirements.

The offset t_n is fixed, so

    Ehat_new<=Ehat_old+1,
    F_new-t_n<=F_old-t_n+1

imply J_new<=J_old+1 by taking maxima. Applying the same argument backwards gives absolute change at most one. An actual source A splay uses d_A primitive rotations, hence

    Delta_DELETE J<=d_A<=2a.                           (2)

This holds on every finite same-key pair and every present key, including both orientations and arbitrary fringe shapes. At d_A=0 the value is unchanged. No physical node deletion or varying-n assumption is substituted into (2).

## Full q on opposite vines at every size

Let R_n be the right vine, L_n the left vine on 1 through n, and V_n=S_n R_n. Use (A,B)=(L_n,R_n), KEEP n. Then a=0 and q=floor((n-1)/2). Exact source subtree counts from FX02 give F=Ehat=n-1 at the source. For n>=4 put m=floor(n/2)>=2. At the destination,

    F(L_n,V_n)=2m-2,
    Ehat(L_n,V_n)=m-1.

For even n the B splay creates one exact proper prefix set; for odd n it creates two. The remaining leaf endpoint matches give the displayed Ehat value. With t_n=m-2,

    J_source=n-1,
    J_destination=max(m-1,(2m-2)-(m-2))=m,
    Delta_KEEP J=-q.                                  (3)

This also explains the cap without fitting: the destination must be at most n-1-q=m, and the F branch requires t_n>=m-2. The chosen value is the smallest nonnegative cap in this maximum construction that meets the opposite-vine requirement for n>=4.

At n=2 and n=3, t_n=0 and J=F; the values are respectively 1->0 and 2->0, paying q=0 and q=1. At n=1 there is only a no-op; empty trees have no present-key access. Reflection preserves both functions and n, so the reverse orientation is covered as well.

## Arbitrary-fringe whole-helper compensation

Use the established six-core RA02 helper family with arbitrary same-key U,V on m additional keys, including m=0 and reflections. The source has d_A=1,d_B=4, so a=1,q=2 and budget zero.

The exact-common counts in FX03 give Delta F_L=-1 and Delta F_R=0. That proof also establishes Delta Ehat_L=0 and Delta Ehat_R in {-2,-1} for arbitrary U,V, using an unchanged residual fringe graph and a one-added-vertex rank bound. These are already proved all-size source identities, not finite fitted observations.

On either whole helper, BOTH arguments of the maximum in (1) are nonincreasing. Taking their maximum therefore gives

    Delta_KEEP J_L<=0,
    Delta_KEEP J_R<=0,                                 (4)

for every paired fringe shape and cardinality. More precisely the possible integer changes lie in {-1,0} for L and {-2,-1,0} for R. The cap may depend on n, but n is unchanged across the operation. No new fringe-size test or compatibility premise is needed.

## The requested six-key starved consumer

For the known hook pair

    A=1(empty,left-vine on 2 through 6),
    B=left-vine on 1 through 6,

KEEP 1 has a=0,q=2,z=1. The exact old values are

    (F,Ehat)_source=(5,1),
    (F,Ehat)_destination=(2,2).

Since t_6=1,

    J_source=max(1,5-1)=4,
    J_destination=max(2,2-1)=2,
    Delta_KEEP J=-2=2a-q.                              (5)

The added reserve J-Ehat drops from three to zero. Its -3 change exactly supplies the correction needed for the old Ehat change +1. This proves the specifically requested repair. Reflection gives the mirrored edge.

The previously exposed starved B phase of the empty L helper is also paid: there F,Ehat are (5,2)->(3,2), so J=4->2 at a=0,q=2. This is a fixed derived control, not a claim of universal B repayment.

The four named requirements now hold for the SAME function J. A complete Step 3 potential still needs every other required source edge. CR02 shows why neither this cap nor a broader monotone scalar combination of F and Ehat can supply that global theorem.
