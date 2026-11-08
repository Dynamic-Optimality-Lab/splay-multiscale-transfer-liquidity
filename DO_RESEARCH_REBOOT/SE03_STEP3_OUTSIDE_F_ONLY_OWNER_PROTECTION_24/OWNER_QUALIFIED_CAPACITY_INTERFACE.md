# O24-C — exact ownership debit identity and conditional physical extension

Status: NEW manuscript theorem, independent audit pending. This is not
the complete OWNER24 source-protection theorem.

Use the actual constructed R,B,V,F_D,E_D from EFFECTIVE_RESERVE_INVENTORY.
Write O_in=F_D\E_D, O_out=(F\E)\O_in and define the ACTUAL integers

    v=|V|, q=|F_D|, e=|E_D|, b=|B|;
    p=|dom(a) intersection O_in|;
    x_in=|R intersection a(dom(a) intersection O_in)|;
    x_out=|R intersection a(dom(a) intersection O_out)|;
    z=|(R\im(a)) intersection K|.

Common owners cannot occur on R. Injectivity gives x_in<=p and counts
each outside occupation once. These definitions refer to actual owner
IDs, not raw protected counts or unproved graph edges. Let

    beta=v-q; eta=e-b>=0; gamma=p-x_in>=0.

THEOREM. The unoccupied candidate pool minus the number of still-unpaid
internal F-only demands satisfies the EXACT identity

    |R_av| - |O_in\dom(a)|
       = beta + eta + gamma - x_out - z.              (O24)

Proof. Entry paths give |R|=v-b. Common a owners cannot consume R, and
all other owners there are partitioned into its internal/external F-only
owners. Thus |R_av|=v-b-x_in-x_out-z. Since E_D subset F_D, |O_in|=q-e
and |O_in\dom(a)|=q-e-p. Subtract and rearrange:
v-q+(e-b)+(p-x_in)-x_out-z. Every term is an actual source/map inventory.
No assumed donor matching, source sign, Hall condition or CD7 is used.

Interpretation: eta counts missing auxiliary holes NOT reached by these
entry paths; gamma counts already paid internal F-only demands whose
actual donor is outside R. They are exact conservation corrections, not
new credits. x_out is the actual external locked consumption, not an
upper bound inferred from support size. beta keeps C23's -1/0 intact.

## Physical extension where the inherited block license applies

Let P be k distinct additional unpaid full claims, disjoint from the
internal claims. Suppose the actual source/block eligibility receipt
permits every target in (O_in\dom(a)) union P to use the selected R_av
units. If the RIGHT SIDE of(O24) is at least k, list those target IDs
and candidate units in actual source order and append that many pairs.
The result is an explicit injective extension of a, with no old value
moved; common claims in F_D were already a-paid. The source paths supply
the actual free units before the inequality is applied. This closes
that receipt subclass, including arbitrary finite union collections.

This is the inherited static period/block license only. A target-specific
restriction cannot be replaced by the shared-neighborhood premise. With
different eligibility sets, record N(p)=R_av intersection E_source(p).
No expansion of those N(p), and no new Bank25 schedule, follows from
the scalar identity. Their simultaneous source expansion remains open.

## Exact scope of the pool shortage

Under the shared block license the number of additional units needed
OUTSIDE THIS CONSTRUCTED POOL to pay all internal claims and P is

    max(0,k-beta-eta-gamma+x_out+z).

This is a pool deficit, not a global Coarse-Double violation. Another
legal comparison/region can change R, eta, gamma and x_out. No universal
sign for these quantities is proved here. In particular, computing the
identity for an abstract owner pattern would not certify its source
realizability. The missing universal source bound on external consumption
is still a load-bearing OWNER24 obligation.

## Boundary absorption does not manufacture supply

If a paid exterior F-only owner d with a(d) in R is merely RECLASSIFIED
as internally charged, without a new source block or new credits, then
q and p each increase by1, x_in increases by1, x_out decreases by1.
Thus beta decreases by1, eta/gamma stay unchanged, and(O24) is unchanged.
Equivalently the actual free pool and actual unpaid demand set did not
change. Enlarging an accounting label alone does not repair interception.
C22's genuine larger-block argument added source events/comparison scope;
it did more than rename an outside owner. Any new such enlargement must
likewise establish its actual additional inventory and legal source map.
