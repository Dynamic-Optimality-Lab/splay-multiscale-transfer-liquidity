# Exact scope, allocation ownership, and actual-period IDs

This file is part of the scoped certificate and fixes the interpretation
of all occurrence lists in this directory.

## Actual timestamps rather than period-role loans

The displayed Xi indices1,...,58 identify roles in the displayed original
source word. For any actual unrotated reference copy beginning at t_ref+1,
let Step1's chosen legal cut be after role k, 0<=k<58. Use the actual
comparison period

    I = {t_ref+k+1,...,t_ref+k+58}.

Its occurrence map, applied to BOTH demand and donor roles, is

    tau_k(i)=t_ref+i                if i>k,
    tau_k(i)=t_ref+58+i             if i<=k.

Replace (i,localB) by (tau_k(i),localB), and
(i,localA,bit) by (tau_k(i),localA,bit). This is a bijection onto actual
source occurrences of I, not a second copy available for spending.
The full source pair and aligned erased source pair are both closed;
their own reaching prefixes extend to the cut. The complete auxiliary
macro at roles13..23 is never split by an auxiliary-boundary cut. Its
macro ordinals4,5,6,7 therefore identify actual tail units under this map.

If the cut is after the critical role24, the cyclic packet consists of
role24 late in I and role25 early in I. The ownership obstruction holds
for BOTH actual roles. Its chronologically contiguous version straddles
two successive legal periods; repeating the fixed allocation gives the
same common ownership separately in each period. No donor or receipt is
duplicated or transferred across copies to prove funding on either one.
At role25 debt1 is below the forced maximum2, so no legal maximum-debt
seam lies between its surviving bank bit and the next genuine K5 at50.

This distinction matters: we never assert a zero initial bank at the
convenient displayed R11 seam, whose debt is not needed. The fixed FIFO
bank is initialized only at its actual legal maximum-debt seam. No
startup, warmup QE excess, or neighboring-copy unit pays any demand of I.

## Fixed-erasure chart versus the cold recent-key chart

At Xi's critical K11, the five recent full KEEP keys are {1,3,5,7,9};11
is the omitted cold sixth key. The last V K1 at23 is genuine in full B.
It is also genuine in the actual comparison erasing3, whose stable mark
set is {1,5,7,9,11}. These two charts have DIFFERENT marked sets. The
forced debts0,2,1 belong ONLY to the latter valid fixed auxiliary chart.
No equality or inequality is asserted between its debt and a recent-key
chart debt. In particular the failed Omega normalized recent-chart
residual is not used to calculate a spare bit here.

The guarded theorem assumes that the actual aligned erased history is
in the proven Step1 nine-Score funding domain, with its genuine auxiliary
macros and fixed fE. It makes no additional assertion about auxiliaries
of smaller true core or an unspecified extension of fE. Xi's auxiliary
has exactly nine actual core nodes, so meets this scope directly.

## Do not superimpose alternative receipts

Xi's FULL eight-demand receipt assigns all eight selected bits once.
In particular its critical (24,5) owns (15,4,bit0). It already funds the
whole packet. The fresh guarded packet-only rule, if started from fE(C)
alone, could instead assign (15,2,bit0) to that critical demand. These
are alternatives; the certificate applies ONLY the full Xi receipt to Xi.
After that receipt, the packet module is a no-op there.

Likewise the inherited Omega+ eight-demand receipt and Gamma two-block
receipt retain every old owner. No new module spends their slots. For
any composition with a prior original receipt h_old, apply the guarded
rule ONLY to still-unfunded targets and ONLY if the whole chosen donor
triple is outside im(h_old). The source guard by itself establishes
disjointness from fE, not disjointness from arbitrary other full-demand
allocations. That latter condition is explicit, and is a remaining
universal ownership obligation rather than an assumed theorem.

All units of U and fE(N) are disjoint by inherited Step1. This work uses
only tail units of U; it does not claim that a negative chart residual
releases an actual assigned unit. Negative interference releases only
the actual fE images of unmatched E demands under the existing interface.
