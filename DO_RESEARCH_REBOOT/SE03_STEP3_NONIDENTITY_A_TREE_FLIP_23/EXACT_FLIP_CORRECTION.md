# FLIP23-E — exact rejoining, signed correction and physical repair

Status: mathematical derivation complete at the frozen source scope;
independent audit pending. This is a source transformation theorem,
not a new funding theorem under arbitrary full owners.

Let T=G(L,R(C(x(B0,B1),D),E)) and U=G(L,C(x(B0,B1),R(D,E))). The source
helper I_G or I_R transforms T to U. Consider its EXTENDED block

    D_G=[s,t,v,p], H_A=4, Q_F=7;
    D_R=[g,s,t,v,p], H_A=5, Q_F=8.

The last v:R,p:G pair is a whole-A return in U. Both extended blocks
are WHOLE-B_E returns with erased C. Delete D in an INDEPENDENT auxiliary
proof word, leaving the next original e:x macro and every other operation.
The original source itself is never edited.

## 1. Exact discrepancy and rejoining

Deleting D leaves the comparison A at T, whereas original A is at U.
The retained e macro's zero-event prefix targets G in both executions.
At its unique positive original occurrence tau_e, both access x:

Original, path G,C,x (RL,2 edges):

    U -> V=x(G(L,B0),C(B1,R(D,E))).               cost1.

Shadow, path G,R,C,x (RLL,3 edges):

    T --LL on R,C,x--> G(L,x(B0,C(B1,R(D,E))))
      --terminal zig--> V.                      cost2.

EVERY actual physical subtree, including the private P hangers canonicalized
in A_FLIP_NORMAL_FORM, is in the SAME slot in V. No projected skeleton
identity is used. The two A histories rejoin exactly at tau_e. Their B_E
histories were identical at the deletion endpoint and execute the same
retained KEEPs, hence agree at every corresponding retained operation.
All subsequent source events and costs therefore agree until another
selected correction block begins.

The same proof works for an original DELETE x catcher. In the frozen
hard spine e is a genuine KEEP with full Q6; its positive A event can
still occur at an earlier DELETE x. No invented operation is required.

## 2. Minimal helper deletion and the intervening R,G suffix

If only I_G or I_R is omitted, retain v and p as well. Original U gives
R/RR then G/LL; shadow T gives R/zig then G/zig. Both pairs cost2 events
and return to THEIR respective input trees. They do NOT rejoin there.
The next x access is exactly the rejoining calculation above. This shows
why neither auxiliary return nor the later R,G A-return pair permits a
zero state correction.

For minimal-helper omission the exact original-minus-shadow cost is

    Delta_A=H_A(I)-1 =1 for I_G, 2 for I_R.

For preferred extended-block omission it is

    Delta_A=H_A(D)-1 =3 for D_G, 4 for D_R.

The MINUS ONE is the extra actual-shadow StepEv at the retained tau_e.
It is not discarded or declared nonnegative without proof. Pointwise at
tau_e the original-minus-shadow cost is -1.

## 3. Every shadow credit receives an ACTUAL original unit

Let tau_p be the unique positive A occurrence in original macro p (it
may be a DELETE preceding its KEEP). It has one actual event and lies
in deleted D. Reserve the two ACTUAL bits

    delta_D={(tau_p,1,0),(tau_p,1,1)}.

Map the shadow inventory to the ORIGINAL inventory by psi:

    (tau_e,2,b) -> (tau_p,1,b), b=0,1;
    every other retained shadow unit(t,j,b) -> original(t,j,b).

At tau_e the shadow's first event maps to the original's sole event.
This is an injection of COST UNITS; it does not assert equality of the
two differently shaped rotations. Both target units are genuine original
StepEv bits. The repair bits cannot collide with identity images because
their occurrence lies in D, which was omitted. The A counts at all other
retained occurrences agree, including all original zero operations.

No shadow second event is ever called original(tau_e,2,b): that tuple
does not belong to the original inventory. Old a/fE/common values are
unchanged. psi is a new independent comparison transport, not an owner
reassignment or a claim that delta_D is effectively free.

The protected original set V_D=U_A(D)\delta_D is outside the ENTIRE image
of psi on the whole shadow inventory, not just outside one chosen map:

    |V_D|=6 for D_G; |V_D|=8 for D_R.

For minimal helper compression use tau_t instead and obtain2/4 protected
bits. These are different OPTIONS, not cumulative reserves.

## 4. Exact period equations and the downstream debit

For disjoint selected extended blocks (m_G,m_R), composition proves

    A_shadow=A_original -4m_G-5m_R +(m_G+m_R),
    Q_E,shadow=Q_E,original -sum_D Q_E(D).

Thus the original auxiliary slack minus shadow slack is exactly

    (6m_G+8m_R)-sum_D Q_E(D).

CD6 is applied ONLY after its legitimate source-domain/closure proof in
CD6_LEGAL_TRANSFER_INTERFACE. Its lifted map is an injection on the
retained auxiliary demands into the ACTUAL original bits, avoiding V_D.

The following is the exact DESIGNATED reserve ledger, before exterior
owners or more source funding are considered:

| Block | Raw bits | Repair bits | Protected bits | Full Q | Protected minus Full Q |
|---|---:|---:|---:|---:|---:|
| D_G identity (C22) |8|0|8|7|+1|
| D_G nonidentity |8|2|6|7|-1|
| D_R identity (C22) |10|0|10|8|+2|
| D_R nonidentity |10|2|8|8|0|

Every auxiliary removed demand is a common full slot here. Subtracting
Q_E(D) from protected endpoint count AND from internal F-only slot count
leaves exactly the last column. The nonidentity correction is TWO physical
units, not zero. These are guaranteed construction balances; a particular
CD6 map might leave additional repair units unused, which can be released
only from its actual receipt. Negative balance is not a CD counterexample.

## 5. Outer flips and valid direct retention

The anonymous outer flips in A_FLIP_NORMAL_FORM may leave a residual
shadow discrepancy even after x. They are NOT deleted by this theorem.
Keep their actual original operations (and, if necessary, an overlapping
helper component) in the auxiliary source. Then A is literally the
original A there, every event/bit remains, and CD6 on the actual closed
auxiliary history is legal. The state flip and full/erased B discrepancy
are recorded in the ledger, not assigned zero cost or zero reserve debit.
No reserve-by-excision is promised for such retained components.

This direct route has no unproved rejoining premise. It is deliberately
an exact comparison interface for later owner/funding theorems, not a
claim that retaining a flip proves its full demands funded.
