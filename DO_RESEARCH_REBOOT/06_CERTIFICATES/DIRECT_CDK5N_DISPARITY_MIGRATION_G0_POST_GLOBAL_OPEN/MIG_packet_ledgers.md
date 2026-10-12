# Rotation-packet ledgers: A-paid (P3) and B-driven (P4)

## P3 — A-side packets

An original access with A-depth d_A performs exactly d_A primitive
rotations (splay decomposition: ⌊d/2⌋ double steps ×2 + (d mod 2) zig;
code _rebuild). With a=⌈d_A/2⌉: d_A ≤ 2a ⇒ ≤2a rotations ⇒ ≤4an gross
Ω-coordinate changes per access (P2 bound 2n/rotation). This is a genuine
upper bound on A-side structural packets. It is NOT usable surplus: most
changed coordinates are intermediate (created and destroyed within the same
splay), rearranged rather than discharged, or B-liability-coupled. Counting
them as payment = double-spend (see audit). E3 interval: exactly one a=1
access (L0) ⇒ ≤2 A-rotations for the whole interval (a ZIG; observed: the
nonzero event at depth 1–2).

## P4 — B-side packets (Control B passes explicitly)

On KEEP with B-depth d_B=2q+z (z∈{0,1}): exactly d_B B-rotations in
2q+z... precisely ⌊d_B/2⌋=q double-or-single steps ⇒ d_B rotations, gross
≤2n·d_B coordinate changes. Crucially these occur even when a=0: Control B
idx16 (a=0,q=2) changed 14 Ω-coordinates with ZERO A-rotations. Hence:
B-driven packets exist, are exactly enumerated (P2 tables apply equally —
same rotation code), but are UNPAID by A. Any bridge must carry Control B
as an explicit ledger entry: 14-coordinate migration at (a,q)=(0,2),
v=1 gap 4→0. Treating B-packets as A-paid is refuted (not merely unproved).

## Ledger convention

Packets are (access-index, side, step-type, rotation-list, ΔΩ-set) records
(MIG traces reference them). A-paid vs B-driven provenance is intrinsic
to each packet. No packet is usable surplus without a proved
capacity theorem (none established — see MIG-C1 record).
