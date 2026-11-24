# Direct all-double route and linear physical closure

## Exact closure using real original operations

For any two complete n-key BSTs with the same keys and n≥4,
there is a present-key splay word converting one to the other
with at most \(156(n-1)\) StepEv. Here is the constructive proof
used by the source generator, in the spirit of [Levy–Tarjan
Theorem 3.4](https://arxiv.org/html/1907.06310v3).

1. Flatten to a left vine with restricted rotations. First
   promote left children at the root until the root is minimum.
   Then, while it has a right child, right-rotate at that child
   until its left link is empty, and promote it to root. The
   old root joins the completed left vine. The two types of root
   rotations each occur at most n−1 times. A right rotation at
   the root's right child inserts a new vertex on the right
   extreme spine, keeping the old ones; root rotations preserve
   the union of extreme spines. There are at most n−1 such
   insertions. Thus a flattening uses at most \(3(n-1)\)
   restricted rotations. Flatten the starting tree and reverse
   the target flattening. Inverses are still at a root or child
   pivot and promote a vertex at depth at most two.
2. Realize each restricted rotation by a splay word. Take an
   ancestor-closed hull of exactly four physical keys containing
   the root path to the promoted vertex (at most three keys),
   adding frontier keys if needed. The desired rotation is a
   transition between two of the 14 labelled-rank BSTs on four
   keys. The exact directed transition table in coercion.py
   enumerates all 14 shapes, tests reachability from every one,
   and checks all 196 shortest words with the other pointer
   implementation. The graph is strongly connected, so at most
   13 requests suffice (the verified maximum is five). Each
   request within the hull costs at most two StepEv.
3. Lift the four-key word to the complete original tree. The
   hull is ancestor-closed, so all accessed paths stay within
   its keys. Each outside complete component sits at the one
   inorder gap to which its keys belong. Such components are
   never internally touched, and the final target hull
   uniquely determines their attachments. Thus matching the
   four-key transition performs the intended full rotation.
   There is no physical removal, insertion or uncharged access.

This is an all-size symbolic reduction to one complete fixed
table, not an empirical finite-size cost claim. The bound is
\(6(n-1)\cdot13\cdot2=156(n-1)\). Arbitrary totally ordered
labels lift from ranks. The small cases are treated separately.

For any finite paired fragment P (initial pair a0,b0, ending
a1,b1), append D-only coercion of a1 to b1; a common KEEP
coercion of b1 to b0; then D-only coercion of b0 to a0.
All repair operations count. Exact measured closure costs at
most \(468(n-1)\) additional A StepEv. Any initial pair for
n≥4 is reachable from common b0 using D-only coercion. These
statements use allowed present-key Pair Access; the added
support scan in experimental witnesses is optional and is
charged separately there.

## Direct bound and its still-open premise

If a universal closed-source coefficient C exists, closing any
fragment P as above gives
\[
Q_B(P)\le C A(P)+468C(n-1).
\]
Conversely any absolute multiplier plus a finite fixed-tree
startup term in such a bound implies the closed-source bound
by repeating a complete period and dividing by the number of
laps. A proof could exploit linear startup and avoid computing
any residual. It is equivalent as an existence problem:
\(R_{\rm overflow}\le3Q_B\), and the inherited forward interface
has a fixed absolute base. A bound on Q_B cannot coexist with
an unbounded ratio of the fixed literal overflow.

A useful necessary potential under the hypothesized C is the
supremum of future \(Q_B-C A\) over original finite paths from
each pair. The explicit reset bounds its range between zero
and \(468C(n-1)\). Concatenating one edge gives the Bellman
inequality. This is not an independently constructed potential
and provides no evidence that such C exists. The missing work
is a physical formula or amortization with a uniform edge law.

The exact alternative R3 uses all original doubles and avoids
external residual roots: there are at most \(2A\) roots in a
binary forest with strictly shrinking original frames. A
constant bound on its mean component size would close CD.
Uniform component height and disjoint child-frame hypotheses
are false in this physical forest. Counting all persistent
marked ancestry gains fails even with neutral U restorers
and complete period restoration. Summing the original signed
SET telescope covers decreasing events, not silent B rotations.
These checks eliminate specific proof shortcuts; they do not
refute the aggregate bound.

**Status:** constructive closure is proved; the absolute
direct multiplier on unrestricted fragments or cycles is open.
