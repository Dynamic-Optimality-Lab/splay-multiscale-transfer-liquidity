# Complete core10 classification of positive channel flux

This closes a NEW B-source subproblem, not A-dependent Step2 repayment.
Use the two fixed channels and K_0,K_1 from the preceding source theorems.
Put K=K_0+K_1<=4. At EVERY actual primitive B double in an original closed
core10 history, K can increase only by1, and only in one of these forms:

    RR: G=M_0, P=U_0, target=M_1;
    LL: G=M_1, P=U_1, target=M_0.                     (1)

Here M_h/U_h mean the marked/unmarked labels of channel h. These are
actual source operand tags, not new graph fields. A transfer from a
positive U in one channel to a U of the other channel does not increase
K. All mixed doubles and terminal zigs have nonpositive total flux.

## Upper-channel target: full source-height calculation

Let the actual splay target be M_1. At each completed inner frame its
own-channel mass is1; its left subtree may carry lower-channel mass,
and its right subtree carries NO mass in either channel. This follows
from the exact inorder heights: target preheight1, postheight2. Its
rebuilt interval has right endpoint height2 and left endpoint ell in
{0,1}. Put lambda=1 if ell=1, otherwise0. Its lower-channel mass is
1-lambda. Initial/final density and processed-subtree persistence
justify these statements at intermediate frames, just as in the own-
channel proof. Unprocessed ancestor label sets keep their source masses.

For an RR frame the exact inorder sequence is

    A, G, B, P, C, target, D.

Every hanger has nonnegative total mass, so its endpoint heights are
ordered. D has endpoints2,2. Since C ends at target preheight1, P cannot
be M_1. The complete possibilities and lower-channel flux are:

| P | G | Delta K_0 | Delta K_1 |
|---|---|---|---|
|M_0|U_0|-1|0|
|U_0|M_0|+1|0|
|U_0|U_0|-lambda|0|
|U_0|U_1|1-lambda|-1|
|U_1|any admissible G|0|<=0|

Proof of completeness and each value follows from endpoint charges:

* P=M_0 has preheight0. B's end0 forces G's postheight0, hence G=U_0.
  Final G's interval ends0, forcing ell0. Its own mass drops1->0.
* P=U_0 has preheight1,postheight0. B's end1 permits G=M_0,U_0,U_1;
  G=M_1 would have postheight2>1 and is impossible. Final P's lower
  charge is1-lambda. Its old charge is0 for G=M_0 or U_1, and1 for
  G=U_0. If G=M_0, ell=0, so P gains1. If G=U_0, G's own charge is
  unchanged and P changes by-lambda. If G=U_1, G's own U_1 charge
  drops1->0, and P gains1-lambda: this is a transfer or a net loss.
* P=U_1 has preheight2. A possible U_0 grandparent has the SAME lower
  charge before and after, because both its intervals end above threshold0.
  Otherwise no U_0 rotates. The own-channel theorem already gives
  Delta K_1<=0. Thus there is no missing positive foreign term.

For LL, the inorder sequence is A,target,B,P,C,G,D. B ends at P's
preheight, but starts at target postheight2 and is nonnegative. Hence
P=U_1. G can only be M_1,U_0,U_1. Only G=U_0 affects K_0, and its
charge drops from1-lambda to0. Thus Delta K_0<=0; the own-channel law
gives Delta K_1<=0 as well.

For LR the source order is A,P,B,target,C,G,D. C has endpoints2,2,
so G=U_1. If P=U_0, its intervals before/after end at heights2/1;
both have the SAME lower-threshold indicator1. Its lower charge is
unchanged. No other U_0 rotates. For RL the analogous C position
forces P=U_1, and any U_0 grandparent likewise keeps its lower charge.
Therefore both mixed cases have Delta K_0=0 and Delta K_1<=0.
The terminal zig rotates marked roots and no U, so both K values stay.

## Lower-channel target and exhaustive closure

Reverse the inorder axis. Its prefix height is2-H on the reversed
positions, so channel0 and channel1 exchange and left/right exchange.
This is an identity for THESE signed source masses, not a reflection
assumption for the old M3 psi or private certificate. Applying the
actual reflected frame formulas proves the lower-target classification.
The two cases in(1) are the ONLY strictly positive total K events.
Each has Delta K=1; all remaining events have Delta K<=0.

## A complete source flux matching, and its exact limitation

On the exact full period K returns. Let a removal unit be one ordinal
of an actual event's negative total change -Delta K; retain the actual
source occurrence/local-double ID. Cut at an ACTUAL minimum-K boundary.
Create one token at each event in(1), remove -Delta K tokens at each
negative event, and preserve the token count on zero-change transfers.
Induction on the literal increments shows the live count is K-K_min,
always nonnegative and at most4, and starts/ends0. LIFO or FIFO pairs
every creation with a DISTINCT actual removal ordinal inside that one
period. Intra-splay cuts are only a proof-order device: original events
are retained and whole-period source IDs transport bijectively. This
is not a new boundary at which CD5 or an auxiliary debt is evaluated.

This proves exhaustive source coverage and no double spending for the
CHANNEL-FLUX tokens. Those tokens are NOT actual A-bit units. A removal
event is a B event, so matching creations to removals cannot itself pay
an original B demand. No matching here changes fixed auxiliary receipts,
releases any A reservation or provides the required B-demand->A-bit map.

The remaining core10 bridge is to derive a compatible A funding law for
these source creation/transfer/removal patterns and every accompanying
within-channel demand. Adding two CD5 bounds would still reuse A twice.
Thus this theorem must not be called core10 CD or universal Step2 closure.
