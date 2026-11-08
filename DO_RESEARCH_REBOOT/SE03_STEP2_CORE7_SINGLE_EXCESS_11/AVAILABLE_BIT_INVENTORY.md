# Exhaustive actual-bit inventory and eligibility

All inventory is on the ONE already authorized aligned source interval I.

| Object | Exact meaning |
|---|---|
|U|All actual(t,j,b),1<=j<=a_t,b0/1; actual A replay only|
|D|All actual full BF double IDs(t,k)|
|l(C)|Locked common fE image; original values unchanged|
|U_E|Original E-unused reserve, with original source labels|
|fE(N)|E-only claims retired in the alternative full allocation, not new credit|
|a(D minus Pstar)|Every already paid full demand, including successful old paths|
|Wstar=U minus image(a)|Actual bits currently unused by the partial FULL map|
|r in R|Excess full demand, NEVER an A donor|
|v|A bit unused by h0 in a positive macro; may still be locked/used by a|
|u|Free terminal of the certified h/a path; actual eligible donor selected|

By the existing cancellation theorem,

    U = l(C) disjoint_union U_E disjoint_union fE(N),
    U = image(a) disjoint_union Wstar.

Since l(C) is contained in image(a), any selected u in Wstar is either
an original unused bit or an already retired E-only bit. No new retirement
is performed, no refined gE protection is presumed free under fE, and no
common or previously paid full assignment is displaced.

As an exact inventory check, one physical excess slot gives
|U|-|D|=Splus-1. If Pstar={p}, a uses |D|-1 distinct units and therefore
|Wstar|=Splus; if Pstar is empty, |Wstar|=Splus-1. These identities do
not establish eligibility by themselves. Source geometry proves positivity
and the explicit receipt path supplies an eligible terminal.

Inventory covers every original event, including DELETE-origin bits and
events at nongenuine full KEEPs. A full qF0 root repeat can have qE>0;
those actual auxiliary claims stay in C/P/N accounting. H0 mints no bit.
One cannot count a bit twice under two charts, macros or cyclic labels.
Comparison-only/padded/erased-run events never enter U.

Eligibility is the inherited physical COUNTING-bit/block-cyclic interface,
not an invented target-key match or a strict fixed-seam chronological
policy. It was frozen before construction. A selected u is certified by:

* an independently source-funded complete map h on D using actual I bits;
* a finite path p,h(p),owner_a(h(p)),... in that same actual-ID graph;
* a terminal u outside image(a), with all prior values kept;
* the accepted period transport of BOTH endpoints and fixed-owner exchange.

NONLOCAL_DONOR_LEMMA.md proves these conditions for the computed endpoint.
It does not infer eligibility just from a positive count or declare every
free bit permissible under every possible policy. No new native online,
matching-terminal liquidity eligibility result is claimed; the original
source matching-terminal replay conditions remain intact.

The sealed fE can remain a supplied symbolic map: for EVERY such injection
its exact common values are preserved. This stronger parametric statement
covers its actual image without replacing it by a numerical test map.
The public from_frozen_auxiliary entry point validates actual auxiliary
ID domains and unit uniqueness, builds the accepted partial map and then
extends it. It requires the original source/cut/fE certificate as input;
it never synthesizes missing fE values or a different auxiliary history.
