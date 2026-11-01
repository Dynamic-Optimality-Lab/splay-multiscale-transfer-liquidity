# A genuine delayed payer gives strict source coverage

Start diagonally at R7 and use the unchanged reachable prefix D7,D6. The new fixed cycle is

    K7 K3 K2 K3 K4 K5 K6 K7
    K1 K2 K3 K4 K5 K6 K7
    K6 K5 K4 K3 K2 K1 D7 D6.

Both full trees close exactly. Independent pointer replay gives A=30,Q_B=12,Z_B=16 and 2A-Q_B=48. Its sole positive block is the first KEEP7; every cycle access is a positive-A leader in this witness.

| Role | Request | a | q | delta=q-2a |
| --- | --- | ---: | ---: | ---: |
| Positive anchor | KEEP7 | 1 | 3 | +1 |
| Genuine B intervener | KEEP3 | 2 | 1 | -3 |
| Private delayed payer | KEEP2 | 1 | 0 | -2 |

Before the positive B splay, B=R7 has root 1 and child 2. Its immediate successor key is 3, at depth 2, so SC's immediate source condition fails. The later payer key 2 is an old root child. Its depth immediately after KEEP7 is h=1. There is one genuine intervening B splay, KEEP3, so k=1 and c=floor(h/2)+k=1. The threshold binds:

    delta_anchor+c=1+1=2=2a_payer.

This is not a frozen-B DELETE detour. The intervener genuinely changes B and performs a double. The canonical scan rejects the immediate key 3 for not being in the original shallow set, then accepts the first delayed key 2. The three-block deficit sum is -4.

The 12 individual B-double demands are assigned distinct units among the 60 A-credit units. The anchor uses its two local units and one unit from the payer's two-unit pool. The intervener pays its own demand locally; none of its unused capacity is borrowed. The other blocks also pay locally. There is no duplicated payer or credit.

The reflected witness has the same costs. Every cyclic cut preserves the physical anchor/payer choice and the identical source credit identities. The old SC witness and its reflection are also replayed unchanged and accepted, certifying preservation as well as the analytic containment proof.

## Source synchronization behind the family

After KEEP7, the source A/B trees are the same two trees as in SC's witness. After the new KEEP3 they are

    A=3(2(1,empty),6(4(empty,5),7)),
    B=3(2(1,empty),7(4(empty,6(5,empty)),empty)).

KEEP2 makes each root 2 with left child 1 and retains its old root 3 as the right child. They need not be identical yet. The following KEEP3,KEEP4,KEEP5,KEEP6 grow the common left prefix; at KEEP6 they coincide:

    6(5(4(3(2(1,empty),empty),empty),empty),7).

The source certificate checks this equality, and all later common KEEPs remain diagonal. Full ascending and descending passes restore R7; the final D7,D6 restore its initial A while B remains R7.

## Unbounded size, support and arbitrary rigid fringes

As before, an arbitrary unrequested finite BST of keys greater than 7 may be grafted to key 7's right child. Every request in the fixed word is <=7; the graft remains attached to 7 and commutes with all source rotations. The prefix, synchronization, every requested depth and full closure are preserved for arbitrary fringe size and shape.

For genuinely unbounded KEEP support, start at R_n for any n>=7, retain prefix D7,D6, and use

    K7 K3 K2 K3 ... Kn
    K1 K2 ... Kn
    K(n-1) ... K1 D7 D6.

This has 3n+2 cycle accesses. Before synchronization at KEEP6, the extra right vine 8,...,n is untouched, so the same local source calculation applies. Thereafter all KEEPs operate on identical full trees. A full ascending pass yields L_n and a descending pass yields R_n by the established exact prefix-spine invariant. Final D7,D6 restore the cycle's starting A, so the whole family closes from the stated diagonal prefix.

Every key 1,...,n is genuinely requested by KEEP. There is still exactly one positive block, with the same delayed payer and binding threshold. No larger finite n is evaluated: this family follows from the source graft identity and common-pass invariant.

## Strict named-domain comparison

The new cycle fails old SC because the immediate successor key 3 had pre-positive B depth 2. The positive's former B root is 1, but its first three successors are 3,2,3, and its first return to 1 is at offset 8. Thus the named 26AJ/AK/AL/AM former-root return conditions fail. One isolated positive rules out the two-positive AN/AO packets and the multi-positive AQ/AR/AS components. AP's sole unit-run return also fails because its next key is 3 rather than the former root 1. Seven genuine KEEP keys rule out the <=5-support classes. For the n-family, the former-root return is at offset n+1 and support is n.

These are direct necessary-condition exclusions from pinned old definitions, not claims that old recognizer programs were executed. They establish strict restricted coverage and preservation; they do not claim that every source walk is covered or that every possible consequence of older work has been classified.
