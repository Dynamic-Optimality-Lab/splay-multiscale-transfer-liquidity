# Source realizability, closure and uniform lifting

Status: mathematical source construction and proof; NOT executed;
independent audit pending. No free formal frame is promoted to a source
witness. The explicit controls below are original closed seven-key sources.
Their catcher is DELETE5, not a claimed new H1/Q6 KEEP recovery. The
universal correction theorem also covers the inherited genuine KEEP
catcher when its actual source profile is supplied.

## 1. A common diagonal initial tree and a closed full-B tour

Take marked M={1,3,5,7,9,11,13}, G1,R13,C11,K9,x5. With empty unnamed
children let the COMMON initial A/B tree be

    T0=9(2(1,8(3(.,4(.,7(6(5,.),.))),.)),
          12(10(.,11),13)).

It contains EACH physical key1..13 exactly once. In variants below add
private0 as1.left or private14 as13.right. The marked full core remains13.
All displayed dots are empty, not missing keys. Written unambiguously:

    Left9 = 2(1,8(3(.,4(.,7(6(5,.),.))),.));
    Right9=12(10(.,11),13).

Use the KEEP tour

    U=K1 K3 K9 K7 K3 K5 K3 K7 K9 K3 K1 K9.

It returns full B EXACTLY to T0, with all private terms restored. Here
is a symbolic proof, not a tested assertion. For any ordered free terms,

    T=k(a(g(A,B),b(z(C,D),E)),F), g<a<z<b<k,

the source word g,z,g,k is a whole-tree cycle:

    after g,z: z(a(g(A,B),C),b(D,k(E,F)));
    after next g: g(A,a(B,z(C,b(D,k(E,F)))));
    after k: T.

Its bottom-up splay paths are LL;LL/RR;LL;RR/RR, costing1,2,1,2 doubles.
Reflection gives the right-side cycle. Apply the left cycle at T0 with
(k,a,g,b,z)=(9,2,1,8,3). After its first two accesses, insert the right
cycle(9,7,9,3). After the latter's first two accesses insert the left
cycle(3,5,3,7). The resulting nested word is EXACTLY U. Each nested
cycle returns its complete input, so U returns T0. Every consumed marked
grandparent/target and unmarked parent is named in these formulas; all
other subtrees remain rigid. All source B events are SS and retain all
13 marked-core vertices. U's full-double total is18.

## 2. Two more exact full-B cycles containing the helper

Define

    V_G=K1 K13 K1 K11 K1 K13 K1 K9;
    V_R=K13 K1 K13 K11 K1 K13 K1 K9.

Starting at T0, both return it EXACTLY. Their first seven accesses have
Q values1,2,1,3,1,2,1, respectively, and produce the same full Hamiltonian
path before their last K9:

    1->2->13->12->11->10->9->8->3->4->7->6->5.

The arrows give actual child directions determined by key order; every
off-path child is its original empty/private gap term. K9 performs LL
on11,10,9, LL on13,12,9, then RR on1,2,9. This restores T0, with its
3->7->5 marked chain and C/R leaf arms. Alternatively derive the first
seven operations from the full-B formulas in ERASED_FULL_B_RETURN_CLASSIFICATION.
All are SS, so the marked full core stays13. Each V has14 full doubles.

Thus U followed by either V is a full-B closed source with ALL seven
marked labels accessed genuinely. Extra private0/14 terms commute with
these formulas and remain attached to their extreme-key side.

## 3. A-only source preparation of each endpoint family

For literal physical keys1..N, accesses N,N-1,...,1 reset ANY A tree to
the right vine1..N. Proof: after accessing the current greatest remaining
key, all larger keys form the rigid increasing right chain; descending
induction gives the vine. For the0..13 variant, reset13..0 then access1
to obtain1(left0,right vine2..13). These are ACTUAL DELETE operations;
B_F and B_E do not process them.

On right vine1..13 define the actual DELETE word

    P=D12 D1 D11 D1 D13 D1 D12 D1 D11 D13 D1.

It ends at

    T=1(L,13(11(X,12),E)),
    X=5(3(2,4),9(7(6,8),10)).

L is empty or private0; E is empty or private14. For a direct symbolic
check: after the first four accesses A is1(L,11(X,12(.,13(.,E))));
after the next D13,D1 it is1(L,13(12(11(X,.),.),E));
D12,D1,D11 gives11(1(L,X),12(.,13(.,E)));
D13,D1 gives the stated T. Every ordinary bottom-up rotation is on the
displayed present keys; no private subtree or original event is invented.

Use the following preparations immediately BEFORE V's first KEEP j:

| Desired j endpoint | Physical inventory / reset | DELETE preparation after reset |
|---|---|---|
| G2 |1..13; reset13..1|P|
| R2 |1..13; reset13..1|P then D13|
| G3 |1..14; reset14..1|P then D11 D1 D14 D1|
| R3 |0..13; reset13..0,D1|P then D11 D1 D13 D0 D13|

G3's last four accesses first give U with14 in R.right, then yield
1(.,14(13(11(X,12),.),.)). R3's last five first give U with0 under G,
then R(C(G,X),D), and yield13(0(.,1(.,11(X,12))),.). These are exactly
the anonymous G3/R3 families, not relabelled G2/R2 examples.

The final j KEEP is of the already prepared A root and has A cost0;
its macro includes the actual preceding DELETEs, so it does NOT violate
the H_j>=3 source theorem. Its full B cost is the first1 in V.

## 4. Explicit reachable A/full-B closed periods

For each row let Reset and Prep be its words above and choose V_G or
V_R according to the endpoint root. Define the source period

    W = U ; Reset ; Prep ; first7KEEPs(V) ; D5 ; K9 ; Reset.

All semicolons denote actual concatenation, not suppressed operations.
It has58,59,64,67 original occurrences for G2,R2,G3,R3 respectively.
Starting A at its canonical reset tree and full B at T0:

* U and V close full B; DELETEs do not change it. Thus full B returns T0.
* Reset before Prep fixes the exact j endpoint independently of A after U.
* The final Reset returns A to its canonical starting tree.

The initial pair is REACHABLE from diagonal T0 by the initial Reset.
Hence W is an EXACT original reachable A/full-B closed source. Every KEEP
in U/V is genuine, support is seven, full core13, full-double total32.
The h,g,s,t,v,p A events are exactly the one-event paths in the normal-
form table. D5 immediately after p costs1 in the original A and2 if the
nonidentity helper is naively omitted. It also rejoins the trees exactly.

Relevant relative occurrences (A event time equals KEEP time in these
particular helpers):

| Case | j | g | s | t | v | p | catcher D5 |
|---|---:|---:|---:|---:|---:|---:|---:|
|G2|37|39|40|41|42|43|44|
|R2|38|40|41|42|43|44|45|
|G3|42|44|45|46|47|48|49|
|R3|44|46|47|48|49|50|51|

These source controls realize all four LOCAL helper cases in an actual
seven-key/maximal-core closed word. They do NOT falsely replace D5 by a
genuine Q6 KEEP; strict hard-spine occupancy is not inferred from that
different B word. The universal theorem for any ACTUAL such strict
spine is proved separately by the same source identities, not by this
example census.

## 5. Exact auxiliary closure, without an invented numeric receipt

Erase C11. Let Theta be the deterministic B_E map of ONE explicit W.
Let T_i=Theta^i(T0). There are finitely many BSTs on the literal inventory.
Define u>=1 to be the least index admitting a repeated future T_i, and
L>=1 the least positive repeat at T_u. Finiteness proves both exist and
T_{u+L}=T_u. This is a precise source recipe, not an executed search.

From the common diagonal use prefix Reset,W^u, then period W^L. A and
full B close each W, and erased B closes after L by definition. Every
retained key occurs, so the actual auxiliary closed source has six genuine
KEEP keys. Recency lists close after the first complete copy as well.
The actual aligned interval and every witness operation are fixed by
this deterministic definition; no neighboring copy is borrowed as credit.

No numerical u,L, fE or new independent replay is claimed. This is a
MATHEMATICAL existence-and-construction proof of auxiliary closure using
the accepted original finite-recurrence interface, not a fabricated
machine closure receipt. On any provided certified aligned I the main
projection theorem applies directly without requiring this construction.

## 6. Uniform statements versus example scope

The main proof quantifies over actual inherited histories, arbitrary
original finite length, private trees, repetitions and reflected order.
The controls above prove local-case nonemptiness; they do not prove
uniformity by testing. Every universal claim instead follows from the
free-tree formulas and the proved original occurrence transport.
Literal CD6 remains six-key only. At larger r the same local flip/rejoin
formula holds, but applying an (r-1)-key allocator needs its own proved
source theorem; no Gate U induction is supplied here.
