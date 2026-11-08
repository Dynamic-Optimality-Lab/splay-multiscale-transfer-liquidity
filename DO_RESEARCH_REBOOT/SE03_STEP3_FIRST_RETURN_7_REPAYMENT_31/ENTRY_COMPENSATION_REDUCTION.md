# FR31-EN — source-forced entry compensation, with the precise exceptional branch

Status: uniform symbolic derivation in the frozen PREFIX post-comb frame,
including original A-only operations and ordered private terms. This is a
child theorem about ENTRY compensation, not all subsequent return paths.
The principal PREFIX law is refuted by the separate closed counterexample.

Write P_low=sum(2min(H,3)-Q) over the genuine low macros after the comb
and before the first upper. Every Q<=2,H>=1, so P_low is nonnegative.
Low-only accesses leave the entire right subtree attached to marked5.
Marked7 and11 there remain unary,9 and13 remain leaves. Low marked1/3
have degree<=2. Marked5 retains its two high children7,11 and may have
zero, one or two lower marked children. Hence

    theta=E(first upper source)=degree_marked(5)-2 in{0,1,2}.

The exact low identity is Sigma_low=P_low+theta-1. Including the helper
and comb gives the pre-upper signed total P_low+theta-2. Thus the actual
positive entry debt is D=max(0,2-theta-P_low). Earlier positive balances
are not erased by this max when computing the COMPLETE signed sum.

Let r=depth_low_B(5)/2 in{0,1,2}, using the inherited even-depth barrier.
The first upper paths append RR (11) or RRRR (13), so Q11=r+1,Q13=r+2.
The target11 remains degree1, target13 degree0, and the only high-arity
ancestor can be5, present exactly when theta>0. For c=min(H_upper,3),

    sigma11=2c-1-1[theta>0],
    sigma13=2c-2-1[theta>0].

These are exact separate branch laws. No assumption that their signs or
actual A costs agree is made. The post-upper E value in either case is
theta+r-1[theta>0], but the B topologies and original Q costs differ.

## The actual A cost is source-forced when entry debt is positive

D>0 implies P_low<=1. If ANY low macro had H>=2, its contribution
2min(H,3)-Q would be at least2, impossible. Thus every low macro has H1.
Its unique positive A access must be to its genuine terminal lower key:
otherwise another positive event would be needed to synchronize to that
key. Zero/root-repeat operations and an earlier DELETE of that terminal
key are retained, not omitted.

Consequently all positive A accesses in this low phase target<=5. The
post-comb A right subtree5->7->11->13 stays attached intact to5. At the
start of the upper macro, depth_A(13)>=3. A whole upper macro with H1
could only make its single positive access to13, which cannot be splayed
from depth>=3 in one event. All original DELETE preprocessing is already
inside H_upper. Therefore first-upper13 has H_upper>=2 whenever D>0.

It follows that sigma13>=2 when theta0, and>=1 when theta>0. Since D is
at most2 or1 respectively, the FIRST13 ALONE repays all positive entry
debt. This does NOT prove later return transitions cannot create new debt.

If theta0,5 has no lower marked descendant, so the previous genuine low
root cannot be5 (keys1/3 would then lie below5). The synchronized A root
is1 or3, hence depth_A(5)>=1 and depth_A(11)>=3. The same one-event
argument forces H_upper11>=2. Then sigma11>=3>=D. This covers every
positive-debt theta0 entry, including the possible worst debt2 case.

If theta1 and D>0, then P_low=0,D1. Every genuine low transition would
have to be H1/Q2. From the actual initial lower5-chain, the only first
such genuine access is1. Its SS result has theta0; then the other low
target3 has odd RLR path and5 is Q1, which would add positive price.
Thus theta1/P_low0 entails NO genuine low transition. The first upper11
may have H1, giving sigma11=0. If it has H>=2 it repays at least2.

Therefore the ONLY positive-debt branch not necessarily paid at the
FIRST UPPER event is:

    no genuine low phase, first upper11, H_upper1, debt1.

The counterexample lies exactly in this branch and carries its debt
through a source-valid9,5,7 continuation. This is an exhaustive ENTRY
compensation reduction, not a new universal first-return theorem.

There is no hidden loss from truncating positive entry balance. Keeping
the UNTRUNCATED pre-upper total P_low+theta-2, its sum with the exact
upper term is nonnegative on EVERY other source branch. For P_low>=2,
use c>=1: branch11 gives P_low+theta-1-1[theta>0]>=0, and branch13 gives
P_low+theta-2-1[theta>0]>=0 except theta0's base is still0 at P_low2.
For theta1 at P_low2 the branch13 base is0, for theta2 it is1. For
P_low<=1 use the source-forced c>=2 on13, and on11 when theta0. The
only negative remainder is theta1,P_low0,first-upper11,c1, exactly-1.
Thus all first-upper13 branches pay the ORIGINAL helper/low prefix;
the later upper-to-return suffix still needs its own proof.

## Sharpness and remaining bridge

The low bound-1 is attained in an admitted instance exactly if theta0 and
P_low0; the source lower grammar then requires one genuine H1 KEEP1 and
no other genuine lower access. This is an equality classification, not
a claim that every deeper A parameter realizes it. No complete new
reachable equality witness was constructed here; FIX has its saved deep1
geometry and is not silently varied.

All derivations concern intrinsic E on original source states, so no
physical donor or new bank operation is created. Original normalized
owners/retirement/period hypotheses remain separate. Reflection and
ordered external-gap terms obey the same anchor/one-event argument.
