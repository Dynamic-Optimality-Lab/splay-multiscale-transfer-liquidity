# FE01: exact universal first-entry shifts

**Theorem A — PROVED—UNIVERSAL.** Let T be any finite ordered BST, and x,y
present keys. Use ordinary bottom-up splaying with parent-first LL/RR as in
`python/independent/splay.py::_rebuild` and
`python/liquidity/legacy_embedding.py::splay_trace`. Every first-entry shift
below is exact. No depth, key count, shape, fringe or support bound is used.

## 1. Source sites and the first-entry invariant

Write the ORIGINAL search path as v_0,...,v_d=x, with directions e_0,...,e_(d-1).
The consumed double sites, in execution order, have original top depths
d-2,d-4,...,0 for even d and d-2,d-4,...,1 for odd d. The odd case ends with
a root zig. A double at top depth s uses the unconsumed original nodes
g=v_s and p=v_(s+1), and the rebuilt inner subtree rooted at x. Its case is
e_s e_(s+1). This follows directly by induction through the two-frame pops
in the original tuple source, or through the pointer source's rotations.

Immediately before the double at s, the subtree rooted at x has the SAME
key set as the original subtree T[v_(s+2)]. Earlier operations acted inside
that subtree; they did not consume v_s or v_(s+1), alter their off-path
fringes, or change their global depths. The full current operation-site key
set is exactly the original subtree T[v_s]. After the double the rebuilt
subtree has that set. This proves the invariant inductively. Before a final
zig, the rebuilt x subtree has the original T[v_1] key set and the root is
the original v_0. All sites are nested original subtrees.

For y!=x and d>0, define entry as the FIRST such operation whose ORIGINAL
site subtree contains y. It exists because the last operation has root site
and contains every key. Equivalently choose the first site top s no deeper
than the original LCA depth of x,y. Every earlier site excludes y. A rotation
changes depths only inside its site and leaves its ancestors and outside
subtrees untouched. Therefore y's depth immediately before entry is exactly
h=d_T(y), despite all earlier inner rotations. This proves the required
pre-entry assertion without inspecting an output tree.

## 2. Double identities and complete role table

The actual source formulas are

    LL: g(p(x(A,B),C),D) -> x(A,p(B,g(C,D)))
    RR: g(A,p(B,x(C,D))) -> x(p(g(A,B),C),D)
    LR: g(p(A,x(B,C)),D) -> x(p(A,B),g(C,D))
    RL: g(A,p(x(B,C),D)) -> x(g(A,B),p(C,D)).

At a site of global depth b, a key at internal depth t in a role subtree
R has global depth b+ell_before(R)+t before and b+ell_after(R)+t after.
Subtracting cancels BOTH b and t. The same subtraction for named nodes has
t=0. The relative-depth vectors, in order (x,p,g,A,B,C,D), are:

|Case|Before|After|
|---|---|---|
|LL|(2,1,0,3,3,2,1)|(0,1,2,1,2,3,3)|
|RR|(2,1,0,1,2,3,3)|(0,1,2,3,3,2,1)|
|LR|(2,1,0,2,3,3,1)|(0,1,1,2,2,2,2)|
|RL|(2,1,0,1,3,3,2)|(0,1,1,2,2,2,2)|

Their differences independently give exactly the proposed table:

|Double|x|p|g|A|B|C|D|
|---|---:|---:|---:|---:|---:|---:|---:|
|LL|-2|0|+2|-2|-1|+1|+2|
|RR|-2|0|+2|+2|+1|-1|-2|
|LR|-2|0|+1|0|-1|-1|+1|
|RL|-2|0|+1|+1|-1|-1|0|

The subtree letters belong to EACH row's displayed identity. The three
named nodes and four subtree roles partition every key of that site. If a
subtree is empty, it contains no tracked key; the remaining roles still
partition the keys. A nonempty role may have arbitrarily many nodes and
arbitrarily deep descendants: its shift is independent of t. The formulas
hold for innermost AND outer operations with any rebuilt subtree at x.
Thus there is no unlisted role or hidden leaf-only assumption.

## 3. Source-only selection of an entry role

The local table holds for any current operation. To select its FIRST-entry
role using ONLY original data, use the invariant of section1:

- y=g or y=p is determined by the corresponding original path node.
- The parent's and grandparent's off-path subtrees are still their original
  subtrees. Their roles are respectively (C,D) in LL; (B,A) in RR; (A,D)
  in LR; and (D,A) in RL. Original membership selects between them.
- Otherwise y belongs to the original inner subtree T[v_(s+2)]. If this
  were an OUTER entry, the immediately preceding site at s+2 would already
  have contained y, contradicting first entry. Hence this can happen only
  for the innermost operation, where s+2=d and the original target subtree
  has not yet been modified. Its original left/right child subtrees select
  (A,B) for LL, (C,D) for RR, or (B,C) for LR/RL.
- The case y=x is separately determined and has final depth0.

These are exhaustive, disjoint original-source tests. One does not construct
the rebuilt inner tree, run S_x, look up a post-depth, or query future work
to classify the role. The implementation in `source_first_entry.py` follows
these tests. The independent checker uses original LCA/divergence coordinates
instead, providing a different reconstruction of the same definition.

## 4. Both final-zig identities, including entry at the zig

Use p for the OLD ROOT. There is no separate grandparent in a one-edge zig.
If one calls this old root g, the p column below is its shift; it is not an
additional node or omitted role.

    ZIG_L: p(x(A,B),C) -> x(A,p(B,C))
    ZIG_R: p(A,x(B,C)) -> x(p(A,B),C).

The relative vectors in order (x,p,A,B,C) are (1,0,2,2,1) ->
(0,1,1,2,2) for ZIG_L and (1,0,1,2,2) -> (0,1,2,2,1) for ZIG_R.

|Zig|x|old root p|A|B|C|
|---|---:|---:|---:|---:|---:|
|ZIG_L|-1|+1|-1|0|+1|
|ZIG_R|-1|+1|+1|0|-1|

If entry is the final zig after earlier doubles, y is either the old root
or in its original off-path fringe (C for ZIG_L, A for ZIG_R). Otherwise
y would have been inside the previous original site at depth1. If the
original target depth is1 and no double preceded it, the original target's
child subtrees can also be first-entry roles: (A,B) for ZIG_L or (B,C)
for ZIG_R. Thus zig entry has a completely source-only classification too.
The table includes the target, old root and every fringe and descendant.

## 5. Boundaries and later operations

If x is already the root, no operation is consumed and every depth is
unchanged. For y=x in any tree, source doubles move it up2 and a final zig
up1, giving final depth0. These special cases need no fictitious entry.

For y!=x, after its first containing operation it is a proper descendant
of the rebuilt root x. Its side is determined by key order: left for y<x,
right for y>x. In each later outer operation the previously rebuilt tree
is the target subtree, so y is in one of its child fringes and remains on
that same ordered side afterwards. The table gives these EXACT shifts:

|Later operation|y<x|y>x|
|---|---:|---:|
|LL|-2|-1|
|RR|-1|-2|
|LR|-1|-1|
|RL|-1|-1|
|ZIG_L|-1|0|
|ZIG_R|0|-1|

No later outer operation can make y its original g or p: those unconsumed
ancestors lie outside the previous rebuilt subtree. This proves the side
and role invariant for every remaining operation. Reflection interchanges
LL/RR, LR/RL, left/right and the appropriate role letters, preserving all
claims. FE02 now sums these exact source quantities.
