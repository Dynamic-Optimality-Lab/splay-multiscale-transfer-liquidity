# BG35 — exhaustive maximal-core grammar, uniformly in support

Inheritance: the accepted closed maximal-core all-SS/density theorem fixes
the sorted marked/unmarked labels m1,u1,m2,...,u(r-1),mr. Every marked
subtree has signed mass1; every unmarked core subtree mass0. A marked
vertex therefore has only mass0 child terms. An unmarked vertex has
EXACTLY one marked child and one unmarked-or-empty child. These facts
characterize the following ordered grammar; no finite sampling proves it.

T_n is a marked-rooted tree on n marks and n-1 unmarked labels, starting
and ending marked in inorder. Z+_n has n of each, starting marked and
ending unmarked. Z-_n is its reflected counterpart. Z+_0=Z-_0=empty.

    T_n = mark(Z+_a,Z-_b),       a+b=n-1;
    Z+_n = unmark(T_a,Z+_b),     a>=1, a+b=n;
    Z-_n = unmark(Z-_b,T_a),     a>=1, a+b=n.

Inorder fixes every actual label and all displayed orientations. Each
valid source tree has a unique parse by root and child intervals. Conversely
each generated tree has exactly the required signed masses and label
order. This is a necessary complete STATIC representation of closed
maximal source states, not a claim every grammar tree occurs in a closed
history or every target preserves maximality.

With z0=1, the counts obey

    t_n=sum_(a+b=n-1) z_a*z_b;
    z_n=sum_(a+b=n,a>=1) t_a*z_b.

Thus Z=1+x Z^3, T=x Z^2. At r7 the exact number is3876. There are at
most6 genuine targets per state, so a complete original B transition table
needs at most23256 source actions per implementation. Already accepted
cached actions are reused, not counted as fresh source queries.

For every fresh candidate the ordinary source engine executes the full
bottom-up splay, counts actual doubles, and records whether EVERY event
is SS with marked grandparent/unmarked parent. Only these edges can occur
in a closed maximal-core source by the inherited theorem. Their destination
must again parse in the grammar. Other ordinary transitions are excluded
from the CLOSED MAXIMAL domain, not from the original overall problem.

Any genuine closed maximal-core source normalizes into this graph, with
arbitrary original unaccessed gap subtrees remaining rigid. Conversely
a graph cycle genuinely visiting all marks is an original B-closed word,
not a fictitious quotient path: its edges are actual full-tree splays.
CP35 supplies the corresponding original A/B source path when an A cache
walk and its rigid-gap assignment are given. Full paired closure,
reachability and actual erased/chart alignment remain mandatory.
