# Constructive funding with a two-unit boundary bank

For every source history pi in SOURCE_BRIDGE.md there is an explicitly
defined allocation of ALL its actual auxiliary B-double demands to distinct
actual A-event/bit units. After a legal cyclic rotation the allocation has
zero initial and final bank, at most TWO actual carried units between
macros, and no source unit borrowed from the preperiod or another copy.
All unused actual A units are explicitly released into a disjoint reserve.

## 1. Source units and the canonical cyclic cut

Give each A StepEv its actual copy/occurrence/event identity e and its
two C=2 capacity units (e,0),(e,1). Modes changed by erasure leave these
A trees, rotations and IDs unchanged in the full history. These are counting
units of original source events; no native matching-terminal rule is changed.

Let d_star=max_i d_i, where d_i is the actual sealed M3 debt at the source
ordinary boundary. Choose the earliest boundary attaining d_star in the
given aligned period and rotate the WHOLE closed comparison period there.
This same rotation is legal for full and erased histories. Reachability
is obtained by extending each history's own reaching prefix to that cut.
Full labeled paired closure is preserved. The rotated period is one actual
source period with fresh copy labels; it does not spend the reaching prefix.

At macro entry i require exactly

    b_i=d_star-d_i in {0,1,2}                              (4)

actual units in the working bank. The chosen cut has b_0=0. No virtual
two-unit initialization is assumed. A fixed arbitrary input seam would
need a separately supplied initial bank; zero-start causality is claimed
at the legal maximum-debt cyclic cut only.

## 2. Actual event-by-event allocation

In macro i, list its H_i actual A events in source replay order. The FIRST
c_i=min(H_i,3) events each put their two distinct units into the auxiliary
bank, after any carried units. Every later A event immediately releases
both units into the tail reserve, excluded from auxiliary funding.

At the terminal auxiliary KEEP, list its q_i actual DOUBLE event IDs in
replay order. Assign the oldest bank unit to each and remove it. Auxiliary
ZIGs have no double demand but keep their full state transition. All A
events, including those at that KEEP, precede its B replay in the source.

The number of bank units after paying all q_i is

    b_i+2c_i-q_i
       = (d_star-d_(i+1)) + s_i
       = b_(i+1)+s_i >=0,                                (5)

using the independently proved signed source inequality(2). Thus every
payment is possible and no demand sees an empty bank. Keep the oldest
b_(i+1) units and release the remaining s_i newest units into the surplus
reserve. This release is irrevocable; no future auxiliary demand needs
those units, because invariant(4) is restored for the next macro.

This proves the algorithm inductively for every finite word length and
every legal source macro. At a boundary the bank has at most2 units;
during a macro it has at most2+6=8 before paying demands. This is a bound
on the working token queue, not on stored source input or output records.
The zero-double genuine cases and all root no-ops obey the same formula.

## 3. Complete allocation and explicit unused capacity

The final boundary has d_T=d_star and bank0. Hence every actual A unit
is in exactly ONE of three places: assigned to one actual auxiliary B
double, tail reserve, or surplus reserve. No unit occurs twice and every
auxiliary double has one assigned source unit.

Per macro the disjoint reserve released is

    r_i=2(H_i-3)_+ + s_i,
    s_i=2min(H_i,3)-q_i+d_(i+1)-d_i >=0.                  (6)

The exact local conservation identity is

    2H_i+b_i = q_i+r_i+b_(i+1).                           (7)

Summing with empty endpoint banks gives

    |reserve| = sum r_i = 2A(pi)-Q_E(pi).                 (8)

Equation(8) is a CONSEQUENCE of the source-valid allocation, not an assumed
slack or a proof that the original marginal fits it. The actual reserve
IDs are constructed by the procedure before examining any full B costs,
direct erased charge, indirect interference or desired unrestricted CD
conclusion. The reserves may be zero on a tight history; no positive
universal spare-credit hypothesis is introduced.

## 4. Uniformity and the exact Step1 outcome

All quantifiers in the source bridge remain: ambient size, macro/word
length, DELETE support/timing, anonymous A helpers, fringe populations,
all original mu/sigma, repeated accesses, zero operations and primitive
or repeated periods. Original full closure, not equality of roots or debt,
supplies the cycle. Arbitrary actual A event IDs remain distinct under
all repetitions and the aligned period factor L.

For a full six-key core10/11 history whose aligned erased auxiliary has
five keys/core9, this proves Step1's auxiliary funding and exposes EXACT
source units available for subsequent signed repayment. The B histories
may disagree at every retained access. M3 is never applied to the larger
full core. The no-duplication interface is given in SIGNED_CANCELLATION.md.

This is a constructive consequence of sealed M3, not new original CD-domain
coverage. It does not prove that original extra demands fit the reserve,
nor universal erasure selection, CD(6), unrestricted CD or DO.
