# Transport packet receipts to the fixed auxiliary period

The separate safe-packet allocation may use a packet-boundary cyclic cut,
whereas Step1 uses a maximum-auxiliary-debt cut. They need not coincide.
No assertion that the chosen auxiliary cut avoids every full packet is made.

Let I=[a,a+T) be the actual aligned Step1 period, after recurrence, with
both F and E fully closed. Choose a packet cut a+delta,0<=delta<T, and
the actual full source period J=[a+delta,a+delta+T). Periodicity identifies
each actual occurrence t of J with t if t<a+T, and t-T otherwise. The
result is an actual occurrence in I with identical mode, A input and
event ordinal, and full B demand ordinal. The map is a bijection on
actual source units and on actual full demands. Map BOTH donor and demand
IDs of each receipt through it. This never borrows a unit outside I or
identifies two distinct units; each transported receipt uses the indicated
actual source event in I.

The transported packet may straddle I's seam. Its receipt remains a cyclic
block allocation, and may assign a later-in-I source unit to an earlier
demand. No native causal matching-terminal eligibility is inferred.
Only after an independent allocation of EVERY remaining full demand has
been proved can the complete fF be exchanged against the fixed fE common
assignments. The present packet theorem leaves other demands unfunded
and therefore does not yet supply the Step2 injection.
