# Universal redundancy of initially Score-empty Gamma1 helpers

Status: PROVED--UNIVERSAL REDUCTION, under the previously established
original-source normal forms. Not a construction of a universal debt and
not an unconditional M3 theorem. No finite-population tests are used.

## Statement

Let D be ANY function on the FULL original ordinary shared states, with
0<=D<=2. Suppose every original H1 core-access edge s->t satisfies

    w1+D(t)-D(s)>=0.

Then every original normalized Gamma1 H2 edge whose first anonymous target
has EMPTY initial Score support satisfies the same signed inequality.
This holds for every allowed sigma/mask/private inventory. No invariance
of D under private erasure, anonymous identity exchange, or omitted raw
fields is assumed: the comparison preserves the full shared endpoints.

Proof uses the original positive-charge normal form(f,x), each A charge1,
with the SAME endpoints,H=2 and actual terminal q. Zero KEEP/DELETE events
are covered by the reused source normal-form theorem; they are not silently
fused with a different charged event. Gamma0 remains under its existing
actual-preterminal-floor proof. The Gamma1 changing fringe is in gap0 or9.

Work in gap0; the max/gap9 proof reverses left/right and minimum/maximum
in the real ordered LOW image. No original weak-LE witness, HIGH sentinel
or high claimant scan is reflected.

## 1. Complete source A classification

The source root is a synchronized Score r, and f is a real gap0 target at
depth1/2. Its whole INITIAL subtree has no Score. All gap0 keys precede S0.
Exact Score cover/order and required real active paths give:

* f at L: its subtree is the whole source left subtree, so r=0.
  After the helper, a terminal real core within depth2 is either0 or a
  Score x at the old source R position. Ports/aliases are not actual
  active targets and cannot invent further real Score candidates.
* f at LL under a Score p at L: p must be0, because otherwise all Scores
  below p would have to lie in its supposedly Score-empty left subtree.
  The post-helper core candidates are0 and the old root r.
* f at LL under an anonymous p: p must also be in gap0; if its rank were
  above S0, some smaller Scores would have to be in its empty left subtree.
  The only visible actual terminal core is the old root r.
* f at LR: its parent cannot be Score (f<S0). That parent is gap0 and both
  of its subtrees are Score-empty, so the source root is0. The terminal
  is0 or a Score x at the old source R position.

R/RL/RR are impossible for a gap0 target below a Score root. The corresponding
gap9 cases are R/RR/RL, source root8 in the exceptional case, and terminal
8/entry root/source L. The proof uses only explicit order and private Score
cover, never the literal positions of hidden anonymous payload under weak LE.

## 2. Range-safe terminals

In B the gap0 proxy f is a leaf directly below Score0. Its root path from
the synchronized core root contains h<=9 edges, all LEFT, ending in f.
After splaying f, the old root r is at depth1 if h is odd and depth2 if
h is even. Score0 is at depth ceil(h/2)<=5.

These statements follow by path induction. At the bottom, a zig or pair
puts the old parent Score0 at depth1. Every additional same-direction
pair above the processed subtree increases that depth by1, as does a
remaining final zig. The old source root participates only in the final
zig/pair and ends at depth1/2. Arbitrary side subtrees stay formal variables.

The original compiler charges ONLY the terminal B depth:

    q=floor(d_terminal/2),       w2=4-q.

Thus a terminal old root has q<=1, and terminal Score0 has q<=2. Both
give w2>=2. The range then gives w2+D(t)-D(s)>=2+0-2>=0.
There is no sum of first-helper and terminal B charges in this argument.

## 3. Remaining case: root0 and terminal source-R Score x>0

Let d>=1 be x's depth in the SOURCE B. The first proxy access is just the
zig of f=0.left, so x's new depth is d+1. Original endpoint validity forces
f to be a leaf after the terminal core access.

If d is EVEN, the original core splay consists entirely of paired rotations.
The same core pairs in the helper tree put x immediately below f, with its
left subtree containing Score0. The remaining zig transfers that subtree
to f.right. Then f has a real Score descendant and cannot be a final gap
leaf. This contradicts original b_valid(t), so this parity is impossible.

If d is ODD, peel off the common arbitrary bottom paired rotations. They
lie wholly inside the original0.right subtree and commute with the first
f/0 zig, which changes only0.left. The remaining helper path is f,R0,Rx.
The final two zigs undo the first f/0 zig and then perform the original
final x/0 zig. Therefore ALL B child pairs/root are identical to direct
splay_x of the original B. Other proxies, junk NULL side pairs and inactive
slots travel unchanged. No B bound-field reflection is involved.

Write d=2k+1. The original helper edge and a direct core access have

    q2=k+1, w2=4-(k+1)=3-k;
    q1=k,   w1=2-k;
    w2=w1+1.

This preserves the actual original H2 q and weight; it does not relabel
the H2 edge as H1. We construct a DIFFERENT legal original H1 edge below.

## 4. Same authoritative A shadow and full shared endpoints

Use arbitrary subtree variables A,B,C,D,E. Write each node by its actual
identity; r is Score0, x is a Score>0, f/u are anonymous.

For helper at L, the source is r(f(A,B),x(C,D)). The exact rotation identity is

    splay_x(splay_f(r(f(A,B),x(C,D))))
      = x(r(f(A,B),C),D)
      = splay_x(r(f(A,B),x(C,D))).

The intermediate r/f rotation is exactly undone. All private child pairs,
including irrelevant side-pair junk, are restored before the final core zig.

For helper at LR, the source is r(u(A,f(B,C)),x(D,E)). The helper word ends at

    x(r(f(u(A,B),C),D),E),

while the direct core access ends at

    x(r(u(A,f(B,C)),D),E).

In both, the authoritative depth-two shadow is root x, L=r, R=E, LL=anonymous,
LR=D, and the two observations under E. The only changed private branch root
is f versus u at r.left; both are real anonymous nodes, and their children
are below depth2. The source literal-slot0 owner is r in both witnesses.

This also covers every out-of-range kind0 alias: if E aliases slot0, its
root observation is r, and its child observations read r.left (anonymous
in both) and r.right (D in both). If E is a real node, a bad child reference
only reads r's label, also unchanged. Ports/empty prefixes propagate their
unchanged kinds. The source shadow7 definition therefore gives identical
constrained fields in both cases, including derived beta. Any unused root
kind, anonymous label or opaque-prefix fields keep their ORIGINAL t values.

Keep the original source private witness/inventory, and change its event
description to the one real marked core access x at source R (depth1,H=1).
Its real path is root-terminated and repetition-free, same-key conditions
hold, and no intermediate genuine event exists. Use its true B path and
q1. Endpoint topology is the identical B topology proved above; select the
ORIGINAL target's B lo/hi fields, which remain admissible because they are
fresh endpoint annotations and the topology is identical. These fields
are not asserted copied from stale intermediate replay bounds.

Thus the SAME full original s and t (all147 coordinates) admit a separate
original H1 witness with weight w1=w2-1. No shared states are identified
or weakened. Private witnesses on the two comparison edges may be independent,
as the original graph already allows. Actual midpoint/high semantics remain
unchanged and are not used by this LOW parallel-edge argument.

## 5. Signed conclusion and scope

Apply the hypothesized ORIGINAL H1 inequality on those same endpoints:

    w2+D(t)-D(s) = [w1+D(t)-D(s)]+1 >=1.

All other erased-helper cases were range-safe. This completes the universal
reduction, for arbitrary private inventories, signatures and masks. Once a
public range-two H1 debt is supplied, erased Gamma1 helpers create no extra
signed-preservation obligation. This does not itself construct that debt,
settle Score-bearing helpers, or prove M3. The independent audit checks the
universal term/parity/spine algebra; source normal forms are reused proved
dependencies, not newly assumed completion/existence premises.
