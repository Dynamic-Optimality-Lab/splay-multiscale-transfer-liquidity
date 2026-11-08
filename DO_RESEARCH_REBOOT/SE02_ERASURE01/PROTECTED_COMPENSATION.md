# Protected two-run signed erasure compensation

## Source-defined class and exact guard

Choose a key z in an original reachable fully closed walk. Mark pairwise
disjoint cyclic blocks. Every block is a nonempty run of accesses to z followed
by a nonempty run of accesses to y!=z, for a block-specific y. Each run has at
least one KEEP; all other modes in either run may be KEEP or DELETE, with
arbitrarily many root repetitions. All KEEPs of z in the entire period must
belong to these blocks. No assumption is made on outside DELETE support.

At the beginning of each block:

* A and B both have root y (their full trees may differ).
* In B, z is a same-side grandchild: RR if z>y, LL if z<y.
* In A, z is a child, or a same-side grandchild of y. Thus one actual source
  ZIG or one parent-first LL/RR DOUBLE brings z to the root, and splaying y
  afterwards is its exact inverse on the complete A tree.

These are inspectable source geometry/mode conditions. They do not refer to
R, Delta, a potential value, or whether a desired inequality is true. No claim
is made that every six-key walk has such a z or such blocks.

## Full tree identities and direct/indirect marginal

All splays after the first occurrence in a constant-key run are A-root
identities. The first z access performs one A StepEv, independent of its mode;
the first y access performs the inverse A StepEv. Thus each block has exactly
two A events and returns its COMPLETE A tree to its input.

In full B, the first KEEP z performs one LL/RR DOUBLE; subsequent Kz are B-root
identities. The first KEEP y performs the inverse DOUBLE and restores the
complete input B tree; subsequent Ky are identities. DELETEs never alter B.
Hence each block has exactly two B-double demands, even if either is starved
of simultaneous A work because earlier DELETEs already moved A to its root.

In the erased history, all z occurrences are DELETE; B stays rooted at y and
EVERY y access has B charge0. Its complete B tree is unchanged throughout.
A has exactly the same trajectory as in the full history. Both histories
therefore resynchronize in the complete input pair at the end of the block.

Induction over the intervening unchanged operations proves full and erased B
states identical outside the selected blocks. There is no indirect effect on
later outside KEEPs. For m blocks per period,

    D_z=m                 (first Kz in each block),
    J_z=m                 (first Ky in each block),
    Delta_z=2m.

All other KEEPs inside the runs are nongenuine with charge0. At a cut on a block
boundary (or outside the blocks), the erased word closes in ONE period:
u=0,L=1. This does not assert immediate closure at an arbitrary input cut.

If the input cut lies in a block's active B phase, between its first KEEP z
and its first KEEP y, the input B tree is S_z(B_y). The first erased return
KEEP y still costs1 and restores B_y; the rest of that first period follows
the full outside states, and the final erased partial z-run leaves B_y.
Thus the first period costs Q0+1 and does not return to S_z(B_y). At that cut,
each subsequent period starts/ends at B_y and costs Q0: u=1,L=1. If the cut
is in an inactive B phase or outside all blocks, u=0. This proves at most one
transient period for any cut, with exactly the inherited transient subtraction.

For the physical compensation map rotate to a block-boundary cut. Reach it
using the original prefix and the appropriate finite segment; its credits
are not spent. The selected complete period contains every donor and consumer
of each protected block, so no unit crosses that selected period's seam.
Costs and support are cyclically invariant. Aligned L-copy statements multiply
all costs and block counts by L; no startup or auxiliary preperiod unit is used.

## Physical compensation, including reservation from auxiliary demands

Each A StepEv carries two CD counting units, indexed bit0 and bit1, because
the original coefficient is2. This does not change the event or rotation cost.
For a block, take the actual A event on its FIRST z occurrence. It exists by
the guard and is a ZIG or one source LL/RR DOUBLE. The source rule declares
these two units eligible only for this protected block:

    its bit0 -> the B DOUBLE at the first full KEEP z,
    its bit1 -> the B DOUBLE at the first full KEEP y.

The first is the direct erased-key demand; the second is the positive indirect
return demand. The donor is at or before both consumers, even with arbitrary
DELETE prefixes in the runs. The first y A event's two units remain unused by
this map. Every event ID includes original period-copy, block and occurrence;
different blocks/copies have distinct donors and consumers. No unit is reused.

It remains essential to prove the donor pool is not already committed to the
erased B work. Delete WHOLE selected blocks, not merely their KEEPs, to obtain
a contracted history gamma0. Each block was an exact paired identity, so gamma0
is a legal, reachable, fully closed original Pair Access walk. Its outside
states, A events and B-double demands are precisely the original outside ones.
All z KEEPs disappeared, so its genuine support is at most r-1. Let its costs
be A0,Q0. The erased B history has no demands in the blocks and the same outside
demands as gamma0. Therefore source identities give

    A=A0+2m, Q_full=Q0+2m, Q_erased=Q0.

Apply the SMALLER-SUPPORT THEOREM to gamma0, not to the uncontracted erased
word while pretending some of its units are free. If CD(r-1) is available,
Q0<=2A0 uses only events of gamma0, none of which is in a selected block.
Thus the entire4m block units are excluded from that accounting pool. The
explicit map above pays the2m marginal demands from a subset of those reserved
units; no assumption about slack of an unknown auxiliary allocation is used.

Consequently

    Q_full=Q0+2m <=2A0+2m =2A-2m,
    R_full>=2m.

This is a source-derived signed transfer rule, with distinct physical credits
and a proved reservation. It is not an assumption Delta<=R_z. It also does
not alter or assert acceptance by the frozen matching-terminal protocol; it is
a direct certificate for the original counting inequality.

## Scope of the upward connection

With at most SIX genuine KEEP keys, the contracted source has at most five;
the sealed CD(5) theorem makes this a complete unconditional CD theorem on the
protected class. SIX_KEY_CORE8_FAMILY.md gives a nonempty all-fringe family
strictly outside both entry domains CD(5) and core<=7.

The block theorem itself is uniform in support and ambient size: whenever a
smaller-support CD theorem is available and the geometric guard holds, it
reduces that walk without a signed debt loss. Iterating valid disjoint removals
ends at a proved base when a source-defined elimination sequence exists; the
reserved original event sets are disjoint across removals. Existence of such
an elimination for EVERY required walk is not proved or assumed. Nonresetting
interleaved erasures and arbitrary indirect transfers remain outside this law.
No uniform CD(r)=>CD(r+1) promotion is made.
