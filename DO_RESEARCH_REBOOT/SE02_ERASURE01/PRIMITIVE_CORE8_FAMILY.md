# A paired-simple six-key/core8 family with nonresetting A pulses

Use the same ordered skeleton z<p<b1<b2<b3<b4<b5<b6 and nine arbitrary
mark-free gap hangers F0,...,F8 as before:

    S=b1(p(z(F0,F1),F2),
         b2(F3,b3(F4,b4(F5,b5(F6,b6(F7,F8)))))).

Write y=b1, V=the key word(b2,b3,b4,b6), V^-=the word(b4,b3,b2,b1).
All K/D symbols below are actual source modes. Define the23-occurrence period

    G = Db2,Dz,Kz,Db1,Kb1,
        K(V), D(V^-), Dp,Db1, D(V), K(V^-).

Start at the diagonal (S,S). No population or numeric tree instance is run.
The proof is the following universal source-term derivation.

## A pulse is not a paired identity

Db2 is a child ZIG and puts A at S_b2(S), while B stays S. In this A state,
z has path L,L,L. Dz uses an inner LL double followed by a ZIG, producing

    A_z=z(F0,b2(p(F1,b1(F2,F3)),tail(b3,...,b6))).

Kz is then an A-root identity and a full B LL double. Db1 has path R,L,R;
an inner LR double and ZIG give

    T=b1(z(F0,p(F1,F2)), b2(F3,tail(b3,...,b6))).

Kb1 is an A-root identity and the inverse B RR double. B is exactly S again,
but A is T, whose left child is z rather than p. The B pulse Kz,...,Kb1
therefore changes A's full input/output state. Both B-double consumers have
a=0,q=1. The earlier Db2 source ZIG is the first A event of a repeat-key
erased KEEP gap, and its two unreserved bits pay the two marginal demands.

## Exact full-period closure

On any b1-rooted tree of this fixed right-spine form, V acts by R,R,R,RR and
V^- acts by LL,L,L,L. They are exact inverses for arbitrary left/fringe terms.
K(V) consequently reaches (V(T),V(S)). D(V^-) brings A back to T with B
remaining V(S). Dp is an LR double and Db1 a child ZIG, restoring A from T to S.
D(V) then puts A at V(S), producing the diagonal (V(S),V(S)). Finally K(V^-)
returns both trees exactly to S. All hangers are restored.

The actual A event counts by stage are

    Db2:1, Dz:2, Kz:0, Db1:2, Kb1:0,
    K(V):4, D(V^-):4, Dp+Db1:2, D(V):4, K(V^-):4,

so A(G)=23. B has one double at Kz, one at Kb1, one at Kb6 in V and one at
the returning Kb4 in V^-, hence Q_full=4. Erasing Kz makes the first Kb1 a
B-root identity, leaving Q_E=2. There are8 erased KEEP-key changes; the first
Kb1 repeats the final retained b1 from the previous period. Thus

    C_E=8, D=J=1, Delta=2,
    A=23, Q_full=4, Q_E=2, R=42, R_z=44.

For every m>=1, G^m has these quantities multiplied by m, with distinct actual
event IDs. In each copy Db2 supplies bit0 to Kz and bit1 to Kb1, inside that
same recurrent period. No startup or other-lap unit is used.

## Genuine support and strict separation

Every full KEEP changes its B root, giving genuine support
{z,b1,b2,b3,b4,b6}. The initial marked paths to z and b6 cover exactly all
eight skeleton nodes; no hanger contains a mark. Full closure forces fixed
core8 throughout. Thus all G^m are outside CD(5) and core<=7.

Moreover, G itself has NO proper repeated paired vertex. This is an analytic
symbolic distinction, not a numeric primitivity test. Group its states by B:

* B=S occurs initially, during the first A-only setup, after the B return and
  at the end. Their A states have roots b1,b2,z, or the two different b1-left
  subtrees p(z(...)) versus z(p(...)); only the endpoint equals the start.
* B at z occurs once before and once after Db1; the A roots z and b1 differ.
* The B spine states rooted at b2,b3,b4 are visited on the outgoing and return
  paths. Before the middle repair, A carries T's z-before-p left subtree;
  after it A carries S's p-before-z subtree. They are unequal full trees.
* During the B-root-b6 middle bridge, A roots run through
  b6,b4,b3,b2,b1,p,b1,b2,b3,b4,b6. Repeated root roles on the two sides of p
  have the distinct T/S left subtrees. The p-root state occurs only once.

Consequently the only equal paired vertices in the closed source term are
the first and last. Arbitrary mark-free hanger substitution cannot identify
different skeleton-key positions. G cannot be partitioned, at any cyclic cut,
into proper paired-closed CD(5)/core<=7 components. This removes the automatic
concatenation explanation of the first family. G^m for m>1 repeats the NEW
support6/core8 paired-simple period, rather than introducing a small-support
component. Novelty against every historical non-compositional packet class
is not asserted. Bank25 stays25.
