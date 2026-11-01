# Correction to the draft cut direction in CW00

CW00's preflight sketch said to rotate after a MAXIMAL cumulative-sum point. That direction is incorrect for a nonnegative debt queue that cannot bank unused credit. The correct constructive cut is after a MINIMAL cumulative sum. The original gate is preserved append-only. The proposed source generator, lap cap, strictness criterion, source ceilings and already produced synchronization result are unchanged. No output is silently overwritten.

Let v_j be positive delta_j at positive blocks, -2a_j at KEEP-less blocks and zero at other blocks. Total S=E-C_D<=0. Put P_0=0 and P_t=sum_(j<t)v_j. Choose t in {0,...,m} minimizing P_t and cut just before block t mod m.

Every rotated prefix sum R is >=S. Before wrapping, R=P_u-P_t>=0>=S. After wrapping, R=S-P_t+P_u>=S. Therefore every suffix sum of the rotated period is S-R<=0.

The queue starts at zero and updates D'=max(0,D+v). Its final value is max(0, all nonempty suffix sums), hence zero at this cut. This proves the DELETE-only class is old-UD-covered. At a negative step, unused capacity is retired, never banked for a future positive. The minimum-prefix construction is essential to that chronological interpretation.

The independent verifier will reconstruct this cut and its actual unit injection, not use the erroneous maximum-prefix sketch. The theorem E<=C_D implies UD membership survives this correction. The bounded strictness attempt still fails because its source pair synchronizes after ten KEEPs; that fact is independent of the cut lemma and is checked with both source implementations.

Gate audit: rules 1/3/4 and the fixed-generator construction remain as predeclared; the source recurrence and first-neutral-packet basis in rule 2 are unchanged. The ancillary cut proof is now explicit and corrected. This is a proof-sign repair, not a replacement source candidate or a new research pivot. Strict new closed-walk coverage remains NOT ESTABLISHED.
