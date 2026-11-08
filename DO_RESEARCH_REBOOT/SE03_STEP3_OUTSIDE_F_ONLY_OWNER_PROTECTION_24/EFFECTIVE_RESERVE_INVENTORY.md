# O24-R — actual candidate inventory, before and after ownership

Status: exact conditional-on-input inventory theorem; audit pending.
This constructs candidates from source comparisons, not numerical counts.

For one legal disjoint block collection D, let V be the UNION of its
actual protected bits, after C23's delta_D repair bits are removed.
Let F_D,E_D be its actual full/erased demand IDs, E_D subset F_D.
Use ONE C22/C23 source-derived phi:E\E_D->U\V on the whole union.
Do not union independent per-block free lists as though disjoint.

From every v in V follow fixed inverse fE, then phi, stopping at a
unit outside im(fE) or at an undefined phi demand in E_D. Unique incoming
edges exclude entry cycles/mergers (V is outside im(phi)). Thus terminal
paths give a bijection of V with their distinct terminals R disjoint-union B,
where R is the actual free-fE endpoint set and B subset E_D. In particular

    r=|R|=v-b, v=|V|, b=|B|<=e=|E_D|.

Store every source occurrence and full path. An endpoint in R need not
be born inside D. It is a constructed actual bit, not a fictitious
reserve numeral. All fE assignments remain unchanged.

For each u in V AND each u in R, record fE^{-1}(u), phi^{-1}(u) where
defined, a^{-1}(u), block memberships, actual event, owner receipt stage
and source eligibility. V has no phi owner but can have an fE/a owner.
R has no fE owner but can have a phi/a owner. There is no implication
between the remaining inverse fields without a receipt proof.

Let K be only any separately binding PHYSICAL reservation supplied by
an actual inherited contract, not all comparison images. Avoid double
counting units already in im(a). Then the immediately unoccupied pool is

    R_a=R\im(a); R_av=R\(im(a) union K).

If no extra physical reservation is supplied, K is empty; comparison
immutability instead constrains which proof-map alterations are allowed.
One must not invent K as additional ownership or silently erase a real
reservation. These sets describe occupancy; target-specific eligibility
must still be verified before payment.

All owners on R are F-only, because a extends the common fE values and
R is fE-free. Split them by whether their ACTUAL demand ID is already
charged in F_D. An internal demand with an exterior receipt is still
charged once internally; its exterior provenance is retained separately.
Uncharged F-only owner IDs are the external consumption in the signed
capacity theorem. Physical birthplace alone never decides this split.

The literal C23 source controls have no new computed fE/a fields. This
document does not fabricate those values. It gives a uniform construction
when the actual maps are supplied; it does not prove a universal lower
bound on |R_av| after exterior occupations.
