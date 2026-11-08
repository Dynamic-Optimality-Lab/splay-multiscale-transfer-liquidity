# Signed repayment for all eight source-visible Gamma1 zero profiles

Status: universal analytic proof on the stated original subclass;
publication requires the separate new symbolic/source audit to pass.
No finite tests or new evaluations of psi establish this result.

Keep the CURRENT explicit debt D=D_exp from Transfer13 unchanged.
It has range0<=D<=2, the floor D(s)>=psi(core(B_s)), and all original
negative H1 rows are valid. These are completed prerequisites, not an
assumption of global H1 or LOW feasibility. The complete original Step4
target is unchanged; this theorem deletes the eight named visible profiles.

## 1. The missing destination floor comes from a pure core comparison

The completed negative-core theorem applies to EVERY proper ordered
nine-core tree C and every core target y of depth6,7 or8. Writing
C^y for its ordinary bottom-up core splay, it gives

    2-floor(depth_C(y)/2)+psi(C^y)-psi(C)>=0,
    0<=psi(C)<=2.                                      (1)

This is the complete core law from LDR01, already independently audited
in COMB_AUD01 and reused in E1 OUTSIDE_E1.md. Its domain is all ordered
core trees, not just original A-shallow sources. In particular C need
not be realized as a new original shared state. No bank entry is read
or fitted in this campaign.

Let s->t be ANY original normalized Gamma1 edge of weight0. Reuse
Transfer14: H=2,q=4, the terminal pre-B depth is exactly8, and its first
extreme helper has initial B depth1/2. The exclusion of depth>=3 uses
final proxy validity, not Score-emptiness. Terminal depth9 was also
excluded using final validity. All zero/DELETE normalizations retain
the SAME full endpoints and original H/q.

Consider the ACTUAL minimum-gap helper f. After it is splayed, f is
the intermediate B root, with empty actual left child; its right child
is Score0 and Score0 has empty actual left child. For initial helper
depth1 this is the single f/0 zig. For depth2 it is the exact form

    r(0(f(E,E),T),R) -> f(E,0(E,r(T,R))).               (2)

All other gap proxies are still side leaves: the first helper path
contained only cores and f. Every original core is in f.right. Its
core projection, obtained by forgetting the other gap leaves, is a
proper ordered tree on ALL nine cores. Denote that mathematical tree
by C. In particular its root is0. This operation defines a core-tree
argument of the ALREADY EXISTING psi; it does not erase private A
helpers, change D, create an ordinary graph vertex or identify endpoints.

The terminal has expanded pre-B depth8. Apart from the single helper
root, all its ancestors are cores: the other proxies are leaves. Hence

    depth_C(y)=7.                                      (3)

The first three paired steps of the terminal access lie entirely inside
f.right. All rotating operands are cores. The completed original local
core-projection identity therefore commutes with EACH such pair, with
all raw middle child pairs, proxies and arbitrary subtrees transported
unchanged. In C these are precisely its first three bottom pairs; its
initial odd path length7 leaves one final zig. In the expanded tree,
the initial even path length8 leaves one final pair involving f,0,y.

After those common pairs the expanded term has the form

    f(E,0(E,y(B,Cb))).

The unchanged 0.left is empty because all three pairs are below0.right.
The original last RR pair and the ordinary core last zig are

    f(E,0(E,y(B,Cb))) -> y(0(f(E,E),B),Cb),
        0(E,y(Bc,Cc)) -> y(0(E,Bc),Cc).                (4)

Here B,Cb are arbitrary compatible expanded subtrees and Bc,Cc their
core projections. The FINAL f in the first term is a valid leaf below0.
Projecting that FINAL term gives exactly the second output. Thus

    core(B_t)=C^y.                                    (5)

Only the first three pairs are projected while f is an invalid internal
proxy root. We NEVER invoke the old valid-tree projection theorem on a
rotation whose active operand is f; that last step is verified explicitly
in (4). Nor do we discard an arbitrary Score-bearing helper subtree:
the B proxy f is a leaf in the valid endpoints, while the actual anonymous
A helper can contain any allowed private Score support.

For the ACTUAL maximum-gap helper, the intermediate term is

    f(8(r(L,T),E),E)

at helper depth2 (or the corresponding depth1 zig). Remove root f and
project its left child, obtaining a proper core tree C rooted at8,
again with terminal depth7. The common three core pairs leave

    f(8(y(A,B),E),E) -> y(A,8(B,f(E,E))),
        8(y(Ac,Bc),E) -> y(Ac,8(Bc,E)).                (6)

This is the actual LL pair compared with a right zig. Its FINAL core
outputs agree. It proves (3)-(5) on this second original domain directly;
no reflection of psi, weak-LE private ranks, B annotations or HIGH data
is assumed.

Apply (1) to the pure core tree C at depth7. Its auxiliary CORE weight
is-1, and (5) gives

    psi(core(B_t)) >= psi(C)+1 >=1.                   (7)

This is a GLOBAL DESTINATION FLOOR for original Gamma1 zero edges.
It uses neither source A visibility nor an inventory-invariant debt.
The auxiliary core price-1 is not substituted for the original H2
price0; (7) is a consequence of a separate already proved core inequality.
All full target annotations/G/unused fields remain the original t.

## 2. Visible source cap and exact signed repayment

Now suppose the terminal y was ACTUALLY source-visible, at original
A depth1/2. Transfer14's eight residual profiles are precisely:

| Original profile | Source core root r | Terminal order | Original terminal B depth |
|---|---:|---|---:|
| G1-MIN-V-r1 |1|y>r|6|
| G1-MIN-V-r2 |2|y>r|6|
| G1-MIN-V-r7 |7|0<y<r|7|
| G1-MIN-V-r8 |8|0<y<r|7|
| G1-MAX-V-r6 |6|y<r|6|
| G1-MAX-V-r7 |7|y<r|6|
| G1-MAX-V-r0 |0|r<y<8|7|
| G1-MAX-V-r1 |1|r<y<8|7|

Each source has the SAME full static original completion as the H2
source, and y is a real eligible marked node. The completed visible-
target realization theorem constructs a DISTINCT original negative
H1 KEEP of y on that SAME full source, with destination t'. Its B
depth6/7 gives weight-1. Original H1 validity and the range give

    r'=-1+D(t')-D(s)>=0,
    1-D(s)=[2-D(t')]+r'>=0.                         (8)

No equality t'=t is claimed or needed. No original source field,
private inventory, sigma or source H2 event is altered by this comparison.
Original target annotations for the separate H1 edge exist by the
completed source realization theorem; they are not imposed on t.

The original zero edge therefore satisfies the exact nonnegative-sum
identity

    w_H2+D(t)-D(s) = D(t)-D(s)
      = [D(t)-psi(core(B_t))]
        + [psi(core(B_t))-psi(C)-1]
        + psi(C) + [1-D(s)] >=0.                    (9)

The first term is the saved floor, the second is (1),(3),(5), the third
is the saved nonnegative psi range, and the fourth is (8). This proves
ALL eight source-visible profiles, for the current D_exp with no new
clause, saturation, fixed point or recursive obligation.

## 3. Scope, nonvacuity, and original-graph bridge

Every original mask consistent with the edge, every admissible sigma
and every compatible private completion are quantified. The helper may
be initially Score-bearing. Newly exposed anonymous nodes and arbitrary
hidden port supports are retained. Root mark status, other core topology,
G aliases, unused root/opaque fields and final B bounds are not fixed
by a proposed new guard. The destination floor depends ONLY on its
original core; it holds even if its full alpha cannot be a fresh source.
There is no use of a necessary U upper bound as a lower floor.

The deleted classes have proper realizations, rather than being declared
closed through an empty illustrative shape. At the minimum end use the
source core families below, with their one extreme gap leaf f below0.
Up[a,b] is the ascending right chain a,...,b; E is empty.

    r1: 1(0(E,E),Up[2,8]), terminal7;
    r2: 2(0(E,1(E,E)),Up[3,8]), terminal8;
    r7: 7(0(E,Up[1,6]),8(E,E)), terminal6;
    r8: 8(0(E,Up[1,7]),E), terminal6.

For r1/r2 choose an A prefix r(f(A,B),y(Cb,D)), with B carrying the
lower cores and Cb/D the remaining between/upper groups. For r7/r8
choose r(f(A,y(B,Cb)),D), with B/Cb carrying the proper lower groups.
The first helper is at L; the terminal is originally R or LR and then
RR or RL. Both original charges are1. The displayed original B depths
are6/7; after the helper they are8. Standard completed port realization
supplies compatible finite-in-cap inventories/annotations. All these
helpers are Score-bearing. The actual maximum constructions use the
opposite proper rank groups and actual R helper with terminals L/RL;
they have roots7,6,1,0 respectively. These are ordered-symbol existence
constructions, not tested states, and assert no evaluated psi/D labels.

Because D and the original graph are UNCHANGED, every previously valid
row remains valid literally. Add the eight proved zero rows to the saved
guarded walk certificate, retaining its endpoint bound-7 and fully closed
bound0 under its stated row coverage. Original HIGH/h0 glue needs no
new proof: range, floor and all states/weights are unchanged. Full147-O,
127-M, SAME actual midpoint, independent scopes, free high v, weak LE,
G/raw unused fields and h0(actual0,declared18,q9,w=-3) remain intact.

The stronger global floor (7) also rules out target debt0 on EVERY
Gamma1 zero, including the eight originally hidden profiles. It does
NOT prove hidden source2 repayment: their only remaining possible drop
is2->1. This is a corollary of the SAME theorem, not a new hidden-case
campaign or a claim those cells are nonempty.

BEFORE: eight visible Gamma1 zero profiles lacked destination repayment.
RESULT: the original final core is a depth7 core-access target from C;
the completed negative-core law supplies the missing floor, and (9)
proves every visible row. AFTER: all eight visible profiles are CLOSED;
the prior52 schematic slots reduce to36 H1 plus8 hidden Gamma1 slots,
whose hidden residual is restricted to2->1. Full Step4/M3/Dynamic
Optimality remain OPEN. No original negative cycle or new whole-signature
certificate is claimed. NET ADVANCEMENT is original signed row coverage,
not merely a partition update. No finite tests or saved psi queries ran.
