# Positive-surplus donor construction

Use the source-defined own-packet surplus

    Splus = sum_e max(2H_e-Q_e,0).

This counts actual bits left after the independent h0 selection. It is
not an assumed lower bound on Wstar or the desired original CD inequality.
In the one-slot class, all macros except e* are balanced and h0 has domain
D minus{r}. Each packet's A-bit list is in ORIGINAL replay order, including
both bits of actual events at DELETE and nongenuine KEEP occurrences.

Suppose Splus>0. Select the FIRST positive-surplus macro e+ in the cyclic
macro order induced by the fixed actual interval I. Let its own list be
u1,...,u_(2H). Since Q<2H, v=u_(Q+1) exists. This is a constructively
specified actual(t,j,b) bit, not a numerical credit. It is outside im(h0)
because that macro uses only its first Q bits and other macros have disjoint
source events. No claim that v is already free under fE or a is made.

Define an independent full map

    h(d)=h0(d) for d!=r,    h(r)=v.

Its domain is exactly D; h0 is injective; v is outside im(h0). Thus h is
injective and uses only actual original A bits. This is a SOURCE CONSTRUCTION,
not an inference that an injection exists from QF<=2A. The latter inequality
has not been assumed at any step.

Source timing: choose a separate full-packet cut just before e+. From
that cut, v is minted before the unique deficit r is demanded. Keep v
apart while every other packet pays its own first Q demands from its
selected actual own bits. At e*, its two own bits pay the first two doubles
and v pays its third. Every other A bit is reserve, not a second payment.
The bank starts/ends empty and holds at most one carried bit plus Q<=3
local selected bits, at most4. The original Bank25 and fixed E bank are
not altered. This is a complete source-event-by-event full receipt at a
legal full cut, with original A replay before BF replay at each KEEP.

Transport BOTH donor and demand IDs through the inherited bijection into
the fixed actual Step1 interval I. The chosen full cut does not replace
the E maximum-debt cut. No reaching-prefix or adjacent-copy bit is used.
The resulting h is a certified source/block-cyclic full map on I.

Finally apply NONLOCAL_DONOR_LEMMA.md to h and the EXISTING all-paid partial
map a. If Pstar={p}, it produces a terminal u in Wstar with a legal exchange
receipt and returns a union{p->u}. Every old a value, including all frozen
common fE values, remains unchanged. u may differ from v and may lie in
another source macro. The source theorem guarantees a valid donor without
assuming that positive raw surplus is directly accessible under locked
ownership. Empty Pstar requires no extension at all.

This proves the positive-surplus branch for EVERY period in the declared
source class. The incoming-Hamiltonian source argument separately proves
Splus>=1 on ALL actual members, so no positivity premise remains unproved
in the assembled C7-ONE-SLOT theorem.
