# Preserve every compatible committed receipt after a complete source proof

This generalizes the already proved common-assignment exchange to all
fixed original owners. Its source-funding premise is essential.

Let D be the set of ALL original B-double demand IDs and X the set of
actual A-event/bit units in ONE actual legally aligned full closed
period. Suppose an independent source theorem has constructed a complete
injective allocator g:D->X. Let F subset D contain the already funded
demands, with a fixed injective receipt h:F->X. In particular h contains
fE(C) and any compatible committed cold receipts. Incompatible alternative
family constructions are not united and called one h.

For every p in D minus F, start at d_0=p and put u_i=g(d_i).
If u_i is outside im(h), stop and assign this terminal u_i to p.
Otherwise there is a UNIQUE d_(i+1) in F with h(d_(i+1))=u_i;
continue. Do not move h or spend an intermediate fixed unit.

The path must terminate. If a fixed demand repeated, injectivity of g
and h forces its predecessor to repeat, and iterating backwards would
identify initial p outside F with a demand in F, contradiction. Since
the actual period is finite, an infinite nonrepeating path is impossible.
Two paths from different unpaid p cannot meet: their first common node
and injectivity again force identical predecessors back to their starts.
Thus their terminal units are distinct. Keeping h and adding these
terminal assignments gives a complete injection extending h.

Because fE(C) is fixed, terminal units belong to

    X minus fE(C) = U disjoint_union fE(N),

and avoid all other fixed paid owners as well. Every edge of the donor
rule is an actual receipt from independently proved g or fixed h. No
assumption |P|<=|U|+|N|, no unspecified free unit and no desired CD
inequality is used. Negative-interference units are actual retired
fE(N) assignments, not newly minted bits.

All IDs must FIRST be transported together into the same actual period.
That bijection preserves actual occurrences and local event/bit ordinals;
it does not borrow another copy. Exchanged payments are cyclic block
counting, as in the inherited exchange theorem, not a new native
matching-terminal eligibility statement.

Active UNUSED reservations are not paid-demand receipts. They cannot
be silently discarded: either the independent g excludes those slots,
or an explicit release is recorded after the reserving module's own
packet demands have all been paid, as its existing rule permits. This
does not change any already committed payment. No actual allocator or
reservation is changed merely by stating this theorem.

EXTREME_SWEEP_REPAYMENT.md supplies the required COMPLETE source g on
its whole source class, so this theorem there proves full global donor
ownership. On arbitrary six-key histories g remains unconstructed;
this conditional exchange is not a substitute for that missing theorem.
