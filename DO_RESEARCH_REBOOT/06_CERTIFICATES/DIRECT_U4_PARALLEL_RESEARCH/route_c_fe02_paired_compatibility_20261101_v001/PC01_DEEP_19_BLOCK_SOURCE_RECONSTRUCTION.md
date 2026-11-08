# The19-block walk: two donors, paired gap creation and conflict transfer

All source trees/events and old certificates are frozen. This report studies
their mechanisms; it does not extrapolate FE02 closure from a successful
control. The full new source data are in walk_deep_certificate.json.

Use the unchanged reachable source pair

    A_S=1(.,3(2,7(5(4,6),F))),
    B_S=1(.,2(.,3(.,4(.,5(.,6(.,7(.,F)))))))

and unchanged returning word

    K(7,5,3,1,5,6,4,1,2,1,5,1,6,7,1,2,1,3,1).

F is the inherited arbitrary common upper subtree, empty allowed. Reflection
is also retained. The sole positive block is0, KEEP7, with a=1,q=3. The
whole period has A=25,Q=22 and negative slack29 elsewhere. None of those
known facts is a universal saturated-return exclusion.

## 1. Exact states around the two donors

After KEEP7:

    A=7(3(1(.,2),5(4,6)),F),
    B=7(2(1,4(3,6(5,.))),F).

After KEEP5, block1:

    A=5(3(1(.,2),4),7(6,F)),
    B=5(2(1,4(3,.)),7(6,F)).

After KEEP3, block2:

    A=3(1(.,2),5(4,7(6,F))),
    B=3(2(1,.),5(4,7(6,F))).

After KEEP1, block3:

    A=1(.,3(2,5(4,7(6,F)))),
    B=1(.,2(.,3(.,5(4,7(6,F))))).

The difference is small but source-exact: key2 lies below1 in A's left
root-side structure and above3 in B. Costs cannot be inferred by merely
identifying the roots.

## 2. Why FE01 lends at block2

Immediately after block0, tracked3 has depths1 in A and3 in B. KEEP5 is
the first intervening B change. Its A source path is7,3,5: one LR with
tracked3 the parent, shift0. Its B path is7,2,4,6,5: inner RL then outer
LR. Tracked3 enters the inner RL in grandparent4's outer left subtree.
Its exact entry shift is+1 and the later outer LR shift is-1, total0.

    H_A(...,5,3)=1,
    H_B(...,5,3)=3+1-1=3.

At the following KEEP3, k=1 and FE's B own-work ceiling is floor(3/2)=1.
The actual A source depth is1, so its single A StepEv is a final left zig
and supplies bits0,1. B has source depth3, one RL double followed by a
terminal left zig. Bit0 pays its own double; bit1 pays KEEP7's third double,
whose original B-event index is2. This is FE's actual frozen-suffix loan.
No observed future q selects the source ceiling. PF's old U=4 does not lend.

## 3. Why the independent return mechanism lends at block4

Track key5 after its block1 access. Both depths are0. Departure KEEP3,
block2, has epsilon_A=1 and epsilon_B=1: both old roots5 become children
after their final zigs. Thus g_5=d_B(5)-2d_A(5) changes0 to-1.

The next KEEP1 moves the common root3 to1, AWAY from tracked5. The original
A operation is a single left zig; the B operation is LL. Their old-root
depths are epsilon_A=1,epsilon_B=2. The tracked far-side key5 therefore gains
exactly1 in A and2 in B, so its paired gap stays-1. Its return depths are

    d_A(5)=1+1=2, d_B(5)=1+2=3.

At block4 KEEP5, A has one RR StepEv and B one RR double plus a final right
zig. The capacity2 has a genuine unused bit1. It can pay the same earlier
third KEEP7 double. The inherited gap calculation L=3,eta=1 gives the same
own-work bound q<=1; the new paired proof explains the A/B compatibility
and strict deficit without any fixed short-return assumption.

These are TWO ALTERNATIVE complete injections, not two payments of the
same demand. Each contains22 unique paid B doubles, uses22 of50 units and
borrows nothing from startup/another cut/another traversal. Original event
identity: block2 donor is A-event0 of a zig; block4 donor is A-event0 of an
RR double. Both have a=1 and two distinguishable bits.

## 4. The local equality step already exposes a separator

At block3 KEEP1 the shared old root is3. A leaves3 at depth1, while B's
final LL leaves it at depth2 under original parent2. The pair(3,2), agreed
under root3 before the access, becomes

    3 ancestor_A 2, but 2 ancestor_B 3.

This is a real newly created ancestor inversion. It persists up to the
entering state of block4. It creates no additional A unit. PC02 proves this
separator phenomenon for every paired equality step, all sizes/fringes.

## 5. How the next positive key's gap is restored

Track the ACTUAL positive key7 from its preceding access at block13 to
block0 of the next source period. The paired gap g_7 evolves as follows:

|Block|Root to target|A shift of7|B shift of7|g afterwards|source delta|
|---:|---|---:|---:|---:|---:|
|14|7 to1|+1|+2|0|-3|
|15|1 to2|0|+1|1|-3|
|16|2 to1|+1|+1|0|-2|
|17|1 to3|-1|0|2|-2|
|18|3 to1|+1|+2|2|-1|

At block0, depths d_A=2,d_B=6 give g=2 and the positive(1,3) event. Its
gap-producing approaches are blocks15 and17. They happen to have negative
slack in W. The universal fact is the NECESSITY of approach-side gap creation
with nonincreasing A depth, proved in PC02A. That those helpers must always
be nonsaturated is not proved and cannot be assumed from W.

## 6. A saturated helper really can transfer paired gap

At block1, KEEP5 is saturated: a=1,q=2, no spare own capacity. Yet:

|Tracked key|A entry/whole shift|B entry and outer/whole shift|paired gap increment|
|---:|---|---|---:|
|3|LR parent,0|inner RL outer-fringe+1, outer LR-1:0|0|
|4|LR target-left fringe,-1|inner RL grandparent+1, outer LR-1:0|+2|
|6|LR target-right fringe,-1|inner RL parent0, outer LR-1:-1|+1|

Thus neither coordinatewise nonincrease of d_B-2d_A on every saturated
step nor a rule paying every gap increase from that same step's negative
slack is valid. These are exact failures INSIDE the designated reachable
walk, not invented numeric signatures. Gap growth is not itself a B-double
debt; confusing them would manufacture credit demand.

The scalar ancestor-discordance D nevertheless decreases34->12 at positive
block0 and12->5 at saturated block1 in the physical13-key embedding. The
two relevant nonnegative W steps would therefore misleadingly support its
monotonicity if tested alone. PC03 supplies the separately reachable fixed
counteredge that refutes the universal extension.

## Scope

New paired retreat-only returns in W occur at blocks4,9,11,14,16,18; all
their actual source depths and witnesses are checked. The positive block0
has an overlapping/approaching return. No assertion that arbitrary closed
walks possess a retreat-only return is made. All m>1 W repetitions retain
their inherited FE01 status and are not new exactly-one-positive instances.
FE01, PG02 and all old physical certificates remain untouched.
