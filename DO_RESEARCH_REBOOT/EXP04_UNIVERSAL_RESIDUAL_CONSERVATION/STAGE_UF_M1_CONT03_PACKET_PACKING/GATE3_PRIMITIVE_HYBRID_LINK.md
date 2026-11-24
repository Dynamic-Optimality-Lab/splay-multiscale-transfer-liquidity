# Exact primitive link from A geometry to the frozen raw certificate

This is a source-uniform sufficient condition for the EXISTING hybrid payment. It is not a universal price of the remaining residual, nor a new paid budget. It is derived to explain why the repaired wide packets remain paid.

Fix the original S. If |S|>=2, let l=min S,h=max S and c(A)=LCA_A(l,h) in the complete physical A tree. Define q(A)=#{s in S:s<=c(A)}. At the post-A boundary of a KEEP x in S, A is rooted at x, so q(A)=rank_S(x)+1. All actual A private nodes/DELETE operations are retained.

## Exact primitive law

Consider one A rotation at pivot u promoting child v. Let M be its actual pre-rotation transferred middle subtree and m=|M intersect S|. The physical LCA changes only if u=c(A) and l<=v<=h. Otherwise q is unchanged.

In that moving case:

\[
\Delta q=\begin{cases}
m+1_{v\in S},&v>u,\\
-(m+1_{u\in S}),&v<u.
\end{cases}
\]

Indeed the pivot LCA contains all S. Promoting a child whose key lies between the extremes moves that LCA to the child; the marked keys strictly between the two pivots are exactly M intersect S. The rightward coordinate includes the promoted endpoint; the leftward coordinate includes the old pivot. If the promoted key is outside[l,h], the old pivot retains both extremes and the LCA stays there. A rotation above/below the LCA does not change the extremes' LCA. This proves the rule with private keys as well as marked pivots. Reflection exchanges the two cases.

For |S|<=1 take q constant and all quantities below zero. There is no B-double residual on that degenerate closed source.

Define the original physical quantity

\[
\Lambda_A(W)=\sum_{\substack{e\text{ actual A bit}:\\u=c(A^-),\ l\le v\le h}}
\operatorname{bitlength}(|M_e\cap S|),\qquad \operatorname{bitlength}(0)=0.
\]

It is determined by original pre-primitive states and real bits. It is not selected after seeing S_UU and is not A credit or an approved X. Exact closure gives sum Delta q=0, but does not bound its absolute variation.

## Comparison budget

Let rho(i,j)=0 if i=j and otherwise1+bitlength(|i-j|). This integer metric satisfies the triangle inequality: |i-k|<=|i-j|+|j-k| and bitlength(a+b)<=1+max(bitlength a,bitlength b) for positive a,b.

Each moving primitive has jump at most m+1, hence rho(q^-,q^+)<=2+bitlength(m). Nonmoving bits have zero metric change. Sum the triangle inequality across every original cyclic incoming KEEP gap, retaining DELETEs. The original raw cyclic cost is therefore

\[
\boxed{B_{\rm raw}(W)=m_{\rm cyc}+L_{\rm cyc}\le2R_A+\Lambda_A\le4A+\Lambda_A.}
\]

This is an upper bound, not an equality or a price for Lambda_A. It holds simultaneously for arbitrary source size, private population, period and computational seam.

If Lambda_A=0, each primitive changes q by at most1. For the rank displacement d_h between consecutive KEEP targets, d_h<=R_A(G_h)<=2a_h. Since1+bitlength(d)<=3 ceil(d/2) for positive integers d, the stronger bound is

\[
\boxed{\Lambda_A=0\implies B_{\rm raw}\le3A.}
\]

When A has no nonempty internal S-rooted label at any primitive snapshot, every moving middle subtree's S label is internal and must be empty. Hence Lambda_A=0. The split-vine repair has exactly this property; it is not merely an observed cost fit.

## Exact consequence for original z

If Lambda_A<=6A then B_raw<=10A, so the frozen full-period raw certificate is eligible. Every positive-z parent is noncheap by Gate1, and is H_all-paid, a contradiction. Cheap D packets are entirely quota-selected. Thus

\[
\boxed{\Lambda_A\le6A\implies z_h=0\ \forall h\quad\text{and}\quad\mathcal S_{UU}=\varnothing.}
\]

No additional coefficient is added: this invokes the existing H_all budget. Conversely, a genuine positive z forces Lambda_A>6A, and also every applicable G/H periodic and local exclusion. This is a necessary physical restriction on the unresolved class, not a proof it is empty.

## Why this does not finish M1

Lambda_A is not O(A) on arbitrary sources. In a paired extreme-root two-zig identity with n full marked keys, each A bit moves the extreme LCA across a middle of n-2 keys. Repeating T copies gives at least2T bitlength(n-2) contribution and2T A work. Add one finite all-key support/return phase and choose T dominating that fixed phase; as n grows the ratio is unbounded. All copies have zero B doubles and are correctly erased by G/H normalization. The verified835-key C2 source is an exact paid control of this mechanism.

Thus no constant price for unrestricted Lambda_A is assumed, and it is not handed to M2/M3. The missing packet-frontier implication must use the actual D order and all G/H/local exclusions to force a globally chargeable event, or an eligible comparison. Large unpriced LCA-middle traffic by itself is insufficient.

Proof box: target a physical implication to the frozen raw certificate; conditions original closed source and fixed S; inheritance real rotation tables and cyclic A KEEP gaps. Starting identity is the exact LCA-rank primitive law. Bridge is the integer rank metric triangle inequality. Status PROVED for4A+Lambda and its stated hybrid sufficient conditions. Full silent-packet conservation remains OPEN.
