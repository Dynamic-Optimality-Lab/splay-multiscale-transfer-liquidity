# MC29-P — exhaustive incoming comb predecessor profiles

Status: symbolic source theorem under the inherited fixed seven-mark,
maximal-core/all-SS source hypotheses. No finite original-BST enumeration
is used as the universal proof. Source reachability of particular cases
is independently certified separately.

Write the comb's old marked chain, root first, as g3,g2,g1,x. Each gi
has precisely two marked children: the path child and one off-path marked
leaf li. This follows from C28's seven-vertex off-path budget. Let p be
the previous GENUINE full macro, whose access made g3 the full B root.
Every intervening DELETE/root repeat is retained in its proper macro.

In the actual marked path-to-star operation, the accessed target's new
marked degree equals its old marked degree plus Qp. The destination g3
has exactly two children, so Qp+d_old(g3)=2. Because p is genuine,
Qp>=1. Its old ancestors become those destination children, and an
ancestor's new marked degree is its old degree minus1.

If Qp=1, d_old(g3)=1,zp=0. The single old ancestor is either the off-path
leaf l3 (new degree0, old degree1, beta_p=0), or g2 (new degree2, old
degree3, beta_p=1). If Qp=2, d_old(g3)=0,zp=1. Both g2 and l3 are old
ancestors; their old degrees are3 and1, respectively, in either source
order. Thus beta_p=1. This exhausts every genuine incoming source:

| predecessor type | Qp | beta_p | zp | rho(p), cp=min(Hp,3) |
|---|---|---|---|---|
|U, unary old ancestor|1|0|0|2cp|
|B, branching old ancestor|1|1|0|2cp-1|
|P, one branching/one unary ancestor|2|1|1|2cp-2|

There is no incoming Qp>=3 source class. Root-repeat KEEPs are not
invented as extra genuine predecessors and cannot change this B argument.
The actual Hp remains a source cost, not a freely chosen compensating term.

## Two-step separation and collective use

The B state before p has root either l3, of marked degree1, or g2, of
marked degree3 with a branching marked child g1. Immediately AFTER a
marked comb, in contrast, the new root x has degree3 and ALL its marked
children are unary (each old gi retained just li). Therefore the macro
before p cannot itself be a marked comb. Nor can p, since Qp<=2.

Any two actual comb occurrences are separated by at least three genuine
macros. Their triples(j,p,comb), with j the pre-predecessor, are disjoint
as cyclic sets of actual macro occurrences. Source keys/private ancestors
may be shared, but their physical event occurrences are not. This supplies
noncollision for the pair/triple theorem, not effective freedom under a.

## Full physical local form

The B path has alternating marked gi and unmarked pi at its six physical
edges, with each double LL or RR. The three off-path marked components
are individual leaves; all other physical terms remain actual ordered
BSTs. Candidate local A forms are a zig from root g3 to x or one of the
four double frames with root g3, middle marked/anonymous parent and x.
If the unique positive A event is an earlier DELETE x, subsequent zero-A
operations are preserved and terminal KEEP x is still processed by B.
No A population cutoff or same-chart representative is substituted.

This is an exhaustive necessary local classification, not a statement
that every key-order/stencil assignment extends to a closed source. The
explicit fixtures establish the P-type H1 and H2 cases in genuine closed
histories; unconstructed globally realizable label subclasses are not
declared either possible or impossible by the profile table alone.
