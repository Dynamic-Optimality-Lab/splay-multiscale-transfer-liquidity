# One joint policy; universal compatibility remains OPEN

The candidate has no interior/extreme spending priority. Its vertices are
actual original B demand IDs and operation-capacity pools, with each bit
counted once. See POOLED_RETIREMENT_SOURCE_LAW.md (PR/LPR/GPR) and
EXACT_GLOBAL_FEASIBILITY_MODEL.md (MOP). The latter is exact for this
candidate physical layer; it does not purport to enumerate every original
Gate U14 source license.

## New theorem: pooled-policy compatibility on MR partitions

Conditions: maximal closed full core, r>=7, and a disjoint actual macro
partition into the inherited monotone-return (MR) blocks and own-solvent
blocks. Each MR block has synchronized x0, strictly monotone pass targets
x1,...,xk, actual Qi<=2, and closing Qc<=k. All operations remain actual,
including helpers, nongenuine KEEP and zero-event terminal KEEP. These
are hypotheses, not a decomposition of arbitrary B histories.

Conclusion: the PR graph has a full raw injection. Consequently every
macro-coalition GPR inequality holds on these sources. This is proved by
an explicit allocation, not by assuming Hall's inequality.

Proof. Consider a closing target x0. Each of its Qc old marked B ancestors
g is among the pass targets: x0 was root at block entry, and the inherited
marked path-to-star rule allows only a genuinely accessed marked key to
grow its marked descendants. For each such g take its first whole A
operation losing g's ancestry of x0 after that pass's genuine KEEP. Such
an operation exists and belongs to R_c, hence all its physical bits are
in T_c. At most2a_t distinct g choose one operation t by AR1. Select
distinct bits in each such operation for the chosen g.

At most2Hc of these Qc bits are in the closing macro. If its excess is
delta=(Qc-2Hc)_+>0, at least delta selected bits lie in pass macros.
Select any delta of these external bits, preserving their distinct IDs.

For a pass macro i, choose its last positive access to xi, of cost hi*>=1.
All operations after it are zero-event root repeats. The AR2 monotonicity
lemma shows this distinguished access preserves every previously born
pass-key ancestry of x0; a ticket for xi itself is born only after its
genuine KEEP and cannot occur earlier in the same macro. Thus all selected
external bits in macro i lie in its OTHER operations, of total cost
Gi=Hi-hi*. Their number is at most2Gi. Since Qi<=2,

    2Hi-Qi >= 2Gi.

Exclude the chosen external bits and fund all Qi pass demands from distinct
remaining own bits. Each pass has enough remaining capacity. Fund the
closing macro's first min(Qc,2Hc) demands from its own bits, and its delta
remaining demands from the selected external bits. The latter all lie in
T_c. Every edge used is therefore in N of its demand's macro. All bit
IDs are distinct within the block. Ordinary solvent blocks use their
own bits. Disjoint blocks have disjoint original inventories, giving the
full injection. Reflection follows by the exact reflected AR1/AR2 formulas.
No bound on private trees or source length was used. QED.

## Relation to the inherited h0/Bank25 theorem

The construction above may change natural h0 values in the ALTERNATIVE
raw comparison. It is not claimed to be the final fixed-owner map. The
inherited MR theorem separately constructs its own h extending h0 by
relocating selected tickets to each host's natural suffix. That theorem's
source-block license and working-two trace remain its accepted interface.
The new theorem proves that the pooled graph is compatible with this
restricted source class; it does not upgrade an arbitrary PR matching
to an original source license.

## Missing universal step

No proof shows that every original B history has an MR/own-solvent
partition. Nonmonotone interior excursions with multiple high-Q returns
are admitted by the principal source domain. Assuming such a partition
would exclude the required cases. The universal PR coalition theorem,
independent full license, and parent cut/ownership interface remain OPEN.
