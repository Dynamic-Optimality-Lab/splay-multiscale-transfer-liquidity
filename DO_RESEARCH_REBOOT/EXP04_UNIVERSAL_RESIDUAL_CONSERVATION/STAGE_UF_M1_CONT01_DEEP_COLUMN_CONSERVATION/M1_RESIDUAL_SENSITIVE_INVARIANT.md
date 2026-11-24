# A bounded extreme-ancestry invariant

This invariant prices creator exceptions. It does not price all internal U-to-U histories. In contrast, M1's sum over all ancestor-descendant pairs has a root-zig A-flux/A=n/2 obstruction.

Let K be the physical keys. If S is nonempty, write l=min S, h=max S. For q in {l,h}, use the complete-state quantity
\[
Z_q(A,B)=\sum_{g\in K}{\bf1}\{q\in B_g,\ q\notin A_g\}.
\]
B_g,A_g mean full physical descendant sets, including g. There is one summand per physical root, and only the single fixed extreme q is tracked. Private ancestors and duplicate A S-labels are not discarded.

## Exact primitive law

In a rotation at pivot u promoting v, let L be the keys lost from u's subtree and G the keys gained at v. No other rooted descendant set changes. For an A primitive:
\[
\Delta Z_q
 ={\bf1}\{q\in L,\ q\in B_u\}
 -{\bf1}\{q\in G,\ q\in B_v\}.
\]
For a B primitive:
\[
\Delta Z_q
 ={\bf1}\{q\in G,\ q\notin A_v\}
 -{\bf1}\{q\in L,\ q\notin A_u\}.
\]
Let F_q be total signed A change, G_q the positive B terms, L_q the negative B terms. Complete paired closure gives
\[
L_q=G_q+F_q,\qquad F_q\le R_A.
\]
The positive A term is at most one per actual primitive, regardless of the number of descendants. A terminal A zig contributes its one actual bit.

During B, A is rooted at the access target x. A target promotion has zero positive term because A_x=K. A non-target promotion is bit 0 of an SS double.

For q=l, a positive term requires an RR at an old grandparent whose subtree contains l, with x on the right side. This is the unique divergence on the original B search paths to x and l: below it the x branch excludes l, and above it l is already in the child being promoted. Thus at most one positive B term occurs per nonidentity KEEP. The h proof is the reflection (LL). Therefore
\[
G_q\le K_B,\qquad L_q\le R_A+K_B.
\]
This is a symbolic first-turn argument on each original search path; it is not inferred from the finite event checks.

## All extreme-touching doubles

Consider doubles whose frame contains l. If x<g, the old-grandparent demotion loses l. Because A is rooted at x<=g with x!=g and l<=x, l is absent from A_g. This gives a distinct negative B term, so at most L_l such doubles exist.

If x>g, a frame containing l occurs only at the same unique divergence of the target and l paths. At most one such double occurs per KEEP, hence at most K_B. Thus
\[
|\{v:l\in F_v\}|\le R_A+2K_B.
\]
Reflect for h and take the union:
\[
|\{v:F_v\cap\{l,h\}\ne\varnothing\}|
 \le2R_A+4K_B.
\]
Neither branch disjointness nor the number of all rooted descendant pairs is used.

## Nonneutral and Pi-exposed internal doubles

Original signed SET conservation gives D_B=P_A-N_A<=R_A, where D_B counts decreasing B bits. Every nonneutral double contains a distinct decreasing bit, so their number is <=R_A.

For a neutral internal double v that fails whole-frame Pi, let F=F_v. At its previous B loss kappa, the B target is in F, and so proper F is absent from post-A SET. It is again absent at postA(v). If A sees F between these boundaries, there is a genuine A SET creation. Select the first after kappa.

A single actual A rotation creates at most one SET label, even when private carriers duplicate labels. Different labels cannot share this event. Same-label whole-frame Pi windows belong to disjoint proper B membership lifecycles: an inside hit destroys that proper frame, and within one access no two ancestor frames coincide. Hence the selected creation is globally unique, modulo the original period. The number of such exposed neutral internal doubles is <=R_A. This donor lies in the original Pi window; no root-entry matching is asserted.

The exact U definition now gives a disjoint priority partition:
1. nonneutral;
2. neutral boundary-touching;
3. neutral internal whole-frame A-exposed;
4. original U.
It follows on every original source that
\[
\boxed{|V\setminus U|\le R_A+(2R_A+4K_B)+R_A
=4R_A+4K_B\le12A.}
\]

If A=0, R_A=K_B=0. In fact exact B closure and a constant A root imply every measured KEEP is an identity, hence Q_B=0 and all demands vanish. Empty S, no KEEP and singleton effective support are handled without defining a two-extreme denominator. The inequality never divides by A.

Proof box — Target: globally price creators outside U. Conditions: original signed SET law, original full Pi, fixed S extremes, exact closure. Inheritance: R_A<=2A, cyclic K_B<=A (disjoint incoming KEEP gaps). Ambiguity resolved: raw ancestry volume is replaced by single-extreme membership; the cost of boundary frames is bounded by the unique first divergence. Bridge: exact primitive telescope plus the two actual SET injections gives 12A. The identity does not by itself control internal blind creators.
