# Exact local core retention for a full-depth marked access

Status: universal local source grammar, not a global reachable-state quotient
or a signed repayment proof. It addresses the hardest six-key H2/q5 geometry
without testing any core shapes. It also explains why simply requiring all
path marks to alternate is not justified by the existing core-size bound.

Let the original marked B-core S consist entirely of the root-to-x path,
with x marked at its deepest vertex. Off-path hangers have no marked key.
During bottom-up splaying x, track two Boolean facts L,R: whether its
CURRENT rebuilt left and right proper subtrees contain a marked key.
Initially L=R=false, since x is a leaf in S. Let G,P be the marked bits
of the next original grandparent and parent. Their original off-path
hangers remain mark-free by the nested-source-site theorem.

For each double, the following are exactly the conditions that both newly
consumed original vertices remain ancestral to some mark after that event:

| Event | Condition retaining both vertices | New L | New R |
|---|---|---|---|
| LL | G | L | true |
| RR | G | true | R |
| LR | (P or L) and (G or R) | true | true |
| RL | (G or L) and (P or R) | true | true |

For example LL gives x(A,p(B,g(C,D))). C,D are original off-path
mark-free hangers. Thus g's subtree contains a mark exactly when G is
true; if G is true p automatically has a marked descendant. The previous
x-left subtree A is unchanged, and its right subtree now contains marked
g. RR is its reflection. For LR, p's new subtree is p(A,B), where A
has no mark and B has old left-presence L; g's subtree is g(C,D), with
old right-presence R and mark-free D. This gives the displayed tests.
RL follows directly from its own source roles, interchanging which old
ancestor receives L and R. No reflection of an unrelated debt is used.

If a consumed unmarked vertex fails its test, its subtree becomes mark-
free. Later outer operations treat that subtree rigidly and never enter
it, so it cannot recover a marked descendant in this splay. Conversely,
when the tests pass, previously retained rebuilt subtrees remain intact,
the two consumed vertices have marked descendants, and all unconsumed
ancestors still lead to marked x. Induction therefore proves that the
entire original core survives this full splay if and only if all these
local tests pass (with the terminal zig test below if needed).

For a final ZIG_L with old root marked bit G, retention requires G or R;
the new sides are L,true when valid. For ZIG_R it requires G or L and
gives true,R. A full-depth access in a CLOSED MAXIMAL core2r-1 separately
has no terminal zig and an outer LL/RR by the deficiency theorem; that
global restriction is stronger than these local retention tests.

In particular, an innermost mixed double needs BOTH its ancestors marked,
because L=R=false. Later mixed doubles can retain unmarked ancestors
after both sides contain marks. Consequently the shortcut "every double
in a deepest maximal-core access must be same-side, with alternating
marked/unmarked path vertices" has not been proved and cannot be inferred
from counting alone. This grammar retains the actual source possibility
of later cross-side marked descendants.

The two bits are sufficient ONLY for this local ancestor-retention
predicate, given the actual source event word and mark bits. They do not
determine full tree destinations, reachability, signed interference,
actual A funding, or closure of a larger walk. No two-bit controller or
universal CD certificate is claimed.
