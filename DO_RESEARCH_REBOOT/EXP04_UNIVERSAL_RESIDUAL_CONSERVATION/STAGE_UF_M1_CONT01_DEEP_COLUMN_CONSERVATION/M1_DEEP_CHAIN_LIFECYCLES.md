# Whole-frame birth and arbitrary-depth lifecycles

Write F_r for an original double's full B S-frame, J_r for its completed old-grandparent output, and P_r for its completed old-parent output. Actual full trees remain available throughout; label statements use the original S.

## Lemma 1: proper-label runs and birth bits

For a proper B subtree label containing a marked root, all KEEPs outside that labelled component leave it intact. A first KEEP inside it splays a marked target to the B root and removes that proper label by the end of the phase: a proper subtree containing the target cannot remain a subtree when the target is root. Inside one B access the ancestor frames of its doubles are strictly nested. Therefore a particular proper B membership run has only one first-inside consumer whose pre-double whole frame is that label.

A rotation promoting v over pivot u preserves u's old subtree label at v; its only possible new SET label is the demoted u output. In B, both operands are marked and each primitive loses and creates one proper S label. The lost child label contains the current target, so is absent from post-A SET. Consequently a B birth whose new label is A-absent is neutral. This also explains why all B signs are 0 or -1.

For an original U consumer v, let Gamma be the last B SET creation of F_v before the post-A boundary, and kappa its preceding B loss, lifting across the original seam. These exist: the consuming inside hit removes F_v, and closure restores its current run. U's full Pi says F_v is A-absent throughout [kappa,postA(v)], including Gamma. Hence the birth bit is neutral.

The birth cannot be a terminal zig: that demoted root output contains one of the global S extremes, whereas F_v is internal. Gamma thus belongs to an original B double r. Its pivot is g(v), since the run's marked subtree root remains fixed until its first inside hit. The bit is either r's old-grandparent demotion (birth of J_r) or its old-parent demotion (birth of P_r). In either case F_v is strictly contained in F_r: the current target of r is omitted by the completed output.

## Lemma 2: exact C dichotomy

Let u be the previous global same-g double of a C consumer v. Before u, the marked node g has the strictly larger frame F_u. A label F_v containing g and properly contained in F_u cannot already be carried by an ancestor (which includes F_u) or descendant (which excludes g). Thus Gamma is at or after u's g-demotion, not an older run that happens to share a set.

If Gamma is an old-grandparent output, its creator uses old g and must be u: there is no intervening global old-grandparent use. The g subtree is off the remaining path after u, so later doubles of that same B phase cannot rewrite it.

If Gamma is an old-parent output, an LL/RR creator would non-target-promote g at bit 0, violating C's no-promotion interval. It is therefore an intervening LR/RL creator, with p(r)=g and birth at bit 0. Its full B phase lies between the two column uses. This proves G/O in the geometry document.

## Lemma 3: global output capacity

A double creates at most its two distinct completed output labels, at distinct physical bits. Each output run has at most one U frame consumer, by Lemma 1. Thus a creator has at most two U successors, with source-scoped original consumer IDs, including seam-crossing successors.

For C successors, an SS creator has at most its grandparent-output successor: its old-parent output promoted that root. An opposite creator may have one G and one O successor. Its two completed physical output subtrees are disjoint, hence so are the two consumer frames. This disjointness concerns the **new birth graph** only. M0 sibling frames need not be disjoint; its historical overlapping-sibling example is retained.

Every birth edge r -> v satisfies F_v proper-subset F_r. Consequently the finite graph on original double IDs has no directed cycle, even across the seam. A U-to-U ancestry followed backwards eventually reaches a creator outside U. This termination gives no absolute bound on the number of intervening G edges.

## What telescopes and what does not

A fixed-g C chain inherits a rigid full A component and strictly shrinking B frames, as in M1. Repeated B edge destruction/recreation is represented by distinct SET runs and distinct Gamma/kappa IDs. An old edge tuple is not a lifetime or a credit.

The birth graph resolves ownership: a frame belongs to its actual creating bit and first inside consumer. Two sibling outputs are charged separately only under their proved two-output capacity. It does not assign the entire descendant tree to a single A event. Iterating the 72A first-layer bound down arbitrary U chains would count the same original physical A resources without a new load theorem.

Long U/R6 chains exist (guarded construction in M1_ADVERSARIAL_COUNTEREXAMPLES.md). Thus neither label shrinkage, U qualification, nor an acyclic finite birth graph bounds chain height by an absolute constant. Finiteness at fixed |S| does not give source-uniform conservation.

Proof box — Target: mandatory physical birth alternatives and global creator capacity. Conditions: original U and C, actual cyclic SET runs, proper output first hits. Inheritance: original marked-core rigidity and M0 no-reset/no-promotion interval. Ambiguity resolved: C frame births may be old-parent outputs and creator U membership is not inherited. Bridge: local rotation identities, first-inside uniqueness and strict frame inclusion prove Lemmas 1–3 at arbitrary depth. The weighted-chain payment bridge remains OPEN.
