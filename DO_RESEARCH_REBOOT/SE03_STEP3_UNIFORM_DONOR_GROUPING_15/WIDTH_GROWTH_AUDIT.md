# Width growth and Bank25 remain explicit

The inherited modified Gamma_r source is reachable/fully closed with
arbitrary private gaps. Its ACTUAL deepest/q1 pair has H=2,Q=r, price4-r.
Any debt inequality on these unchanged packets needs width>=r-4. A width3
extension fails at r>=8. Its natural h0 uses3 of4 local bits, leaving r-3
unpaid demands and1 local spare, so a one-bank local-carry implementation
requires>=r-4 incoming bits; at r>=30 that exceeds Bank25. These source
facts are preserved, not applied to other packetizations by analogy.

The new D=L proposal has support-dependent range1..r-1, so it does not
violate that lower bound numerically, but the zero-edge source witness
refutes its signed preservation. No local exception patch is promoted.

The channel mechanism uses direct per-key matching, not a claimed width3
debt. A source-relative implementation may track one reserved bit per key,
at most r records, plus branch/repair bookkeeping. For the explicit family
a conservative bookkeeping bound is r+6 (r channels,<=2 local branch units,
<=4 reset repair records). These are support-dependent PROOF/OWNER records,
not a proved <=25 original-order physical bank. Some channels point to
future-in-I donors under the permitted cyclic/block accounting.

Every new executed witness is at r7/r8 and all actual unit capacities are
checked; no original controller buffer or Bank25 is changed. A native
constant-bank schedule for arbitrary r is NOT obtained by storing an
unbounded reserve implicitly, and not inferred merely because the final
static source injection exists. The strong I(r) storage clause remains
an explicit open interface. The directive permits investigating C(r),S(r),
but it does not justify discarding the retained Bank25 source contract.
