# Mixed orientations and the exact opposite-side obstruction

## Completed output structure

After each step, follow the right spine of the current left subtree
of x and the left spine of its right subtree. A same-side double on a
side prepends its old parent to that spine, with the completed old
grandparent output hanging off the spine away from x. For example RR
sets x.left=P, P.right=the old x.left, and P.left=the completed G.
The mirror is LL. An opposite-side double prepends one operand to
each spine: its old grandparent on its own key side of x, and its old
parent on the other. The old grandparent output on its side includes
the **entire former component on that side** of x. These equalities
follow by the two pointer rotations, with all middle/hanging
subtrees retained. A terminal zig just prepends its pivot on one side.

Thus earlier same-side old-g outputs are mutually disjoint. Opposite
old-g outputs on either one side form a nested chain in production
order, and can contain earlier same-side outputs on that side. For
any later target y, only outputs on the side of y can already contain
it; at most one same-side output on that side does so. For any k
specified repeated columns, if \(o\) of them are opposite outputs on
y's side, at least \((k-o-1)_+\) must gain the later ancestry. If y=x
then all k must gain it. The exact lower bound is k minus the number
whose completed output already contains y.

## Rigid retargeting changes orientation

Suppose several previously opposite old grandparents are reused at y
on one side, and the full B subtree of the outermost reused one is
untouched internally between the two accesses. It suffices that no
intervening B target enters that subtree. Their relevant local path
to y is the same as just after the earlier access. On the left side,
previous opposite grandparent keys on that path lie on the increasing
right spine until the search turns left, or reaches y. Every such key
and its next path parent before the turning pair are both smaller
than y; if it is again an old grandparent its double is RR. Only
the turn node and the immediately preceding spine node can be
exceptions. These two original path positions are consecutive, so
at most one is a double's old grandparent. On the right side the
mirrored LL statement holds. In this rigid case at most one reused
opposite old grandparent can remain opposite at the later access.

The rigid condition matters. Intervening B demotions can shrink a
subtree while keeping the later target below it, changing the route
even without a promotion of that column. No global cost for such
interactions is supplied by the spine argument.

## Unbounded exact retargeting and local congestion

For each \(k\ge 2\), take \(n=2k+2\), \(x=k+2\), \(y=k+1\).
The initial B tree is the full alternating path
\[
1,n,2,n-1,\ldots,k,k+3,x,y .
\]
Each edge goes to its correct BST side; the last edge is x.left=y.
A starts at y with x its right child, all keys below y in the
left component and all keys above x in x's right component.
The two genuine KEEPs are x then y. A makes one root zig each
time, exactly returning its complete initial tree at the second hit.
The A components at keys 1 through k are untouched.

At K x there are k opposite-side doubles with old grandparents
1 through k. Applying the spine law gives the exact next B path
\[
x,1,2,\ldots,k,y.
\]
At K y exactly \(\lfloor k/2\rfloor\) of those keys are again old
grandparents, now in RR doubles. There is no B operation between
the two B phases. Each shared key is already a strict ancestor of
y at the first post-B boundary, so zero intervening gains suffice.

Reach the desired A from the common B initial tree with actual DELETE
coercion. After the two KEEPs, use measured DELETE synchronization,
actual full-support KEEP visits, KEEP return of both trees to the
B initial tree, and measured DELETE repair of A. These are legal
present-key words by the constructive coercion proof. Each complete
source closes both labelled trees; it has genuinely marked support
n and total A and Q_B of order n. The excluded reaching prefix is
not used to pay the measured restoration.

For these shared keys the first double is the R3 predecessor of
the second, in the all-double forest. All their causal spans have
the SAME sole A StepEv, A(2,1). Therefore any matching or fractional
payment restricted to the causal span of each such dependency
requires load at least \(\lfloor k/2\rfloor\). This refutes every
absolute capacity for that **local donor restriction**. It also
refutes extending P7's \(k-1\) gains to all orientations. It does
not refute global original A payment; measured work elsewhere in
the period is real. It does not assert that these physical parents
survive original Pi/R6, E_old or the hybrid.

Saved k=4,32,257 sources realize 2,16,128 reused columns. The
516-key source has raw periodic cost 19,121 ≤ 150,610, so is already
paid. Its original Pi classification was not run; the smaller
sources have separately checked original SET/Pi/U and cohorts.
This exact physical family supplies an obstruction to the proposed
mechanism, not to the frozen aggregate theorem.
