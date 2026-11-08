# Complete final +1 / cold q4 exposure conditions

Let y be the final +1 target and x the subsequent ACTUAL cold q4 key.
At the final state A and BF have root y; x!=y. Source-valid NEG2-S
admission requires A-depth(x)=1/2, equivalently an ordinary one-event A
probe to x. Its event may later occur at DELETE x; this does not change
the endpoint criterion by the H1 normal form.

BF-depth(x)=8 by the closed maximal-core source theorem. There are five
marks on that physical path, including its root and leaf x, and one
off-path mark. Hence BF has exactly two marked leaves. Its marked-parent
shape is either a root-degree1 Stem (extra leaf attached within the long
branch) or root-degree2 Fork41 (one leaf branch and one four-mark chain).
No physical binary-child assertion is substituted for marked-parent degree.

Before the final +1 the synchronized root is g. Since g was most recent
immediately before KEEP y, it is second most recent afterwards. Thus x
is distinct from both g and y. Its exact old position is retained: if y
was the old cold key, x was second oldest; otherwise x was already oldest.
There is no fixed-chart assumption. The old/new chart follows actual MRU.

The exact necessary A condition is therefore the THREE-ROOT word

                          g ; y ; x

with one event for each of its two accesses. All six key orders and all
six first-event types must be retained, including private A parents and
the case in which x is itself the first access's parent. Ordered-slot
expansion in TERMINAL_SEEDS.md derives every possible source A term.
BF's four-double probe imposes no independent A-depth constraint.

For a q1 BF access write a=1 when old g loses its last marked child,
b=1 when old y was a marked leaf. Marked leaves change by a-b. Combining
the final two-leaf shape with six genuine marks gives:

| Old BF leaves | Final BF leaves/shape | Source contexts |
|---:|---|---:|
|1|2, Fork41|16|
|2|2, Fork41|32|
|3|2, Stem|96|

If b=1, a=1 would leave only g,y in the entire marked tree, impossible
with six marks. Thus b=1 gives3->2. With b=0, a=0/1 gives2->2 or1->2.
The independently derived144 contexts include72 LL and72 RR BF events.
Their six g,y,x rank-order counts are8,32,32,32,32,8 in lexicographic
permutation order. This is the NEW final+1 classification, not06's table.

All private terms are universally quantified. The complete source grammar
and its lifting, rather than a finite set of concrete A/B populations,
justify the case analysis. Sigma's actual predecessor and its reflection
occur in the three-leaf class; its corrected count3 is preserved.
