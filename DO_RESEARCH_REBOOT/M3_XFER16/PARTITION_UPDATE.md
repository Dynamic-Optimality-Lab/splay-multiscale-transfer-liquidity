# Partition interface after the safe ceiling

Do not overwrite Transfer14's partition or Transfer15's update. Keep
their potential names and flags attached to their original results.
The new debt is F=ceil_H(D_exp), where ceil_H here means MINIMUM with1
on H (a ceiling, not a floor). The exact definition is equation(2) of
HIDDEN_GAMMA1_REPAYMENT.md; it introduces no graph coordinate.

All16 Gamma1 slots (8 visible,8 hidden) are now CLOSED for F. Visible
rows transport by the safe-ceiling row theorem. Hidden rows have source
F<=1 and destination F>=psi>=1. No residual Gamma1 zero slot remains.
Gamma0 zero was already proved for any range-two psi-floor debt, and
the helper-depth1/deep-helper/terminal-depth eliminations remain valid.

The36 H1 slots remain OPEN, but their old seed-failure classifier was
proved for the upward D_exp lineage, so it is not silently re-used as
a direct pointwise theorem about an arbitrary smaller F. The correct
bridge is ROW preservation plus the changed-target analysis:

* An H1 row valid for D_exp is valid for F.
* If an H1 target is lowered, every incoming H1 row is directly valid
  for F by the safe-ceiling proof, including rows not previously valid.
* At an unchanged target, lowering a source only helps. Any current
  failure is therefore also an old D_exp failure. The saved critical
  seed/word/depth classifier applies to that OLD failure, with its old
  Lambda quantities. We keep those as immutable indexing functions.

Thus the36 saved H1 schemata still exhaust every possible F failure,
with the ADDITIONAL requirement that the F target was not lowered.
They assert no nonemptiness. New machine metadata records the inherited
old Lambda coordinates and this correct implication, rather than a
false claim that F>=Lambda or that a lower target cannot matter.

Full Step4 remains OPEN precisely at these unproved H1 inequalities.
This campaign does not address the +1 LOW cases needed after Step4
or promote M3/Dynamic Optimality. It certifies no negative cycle.
