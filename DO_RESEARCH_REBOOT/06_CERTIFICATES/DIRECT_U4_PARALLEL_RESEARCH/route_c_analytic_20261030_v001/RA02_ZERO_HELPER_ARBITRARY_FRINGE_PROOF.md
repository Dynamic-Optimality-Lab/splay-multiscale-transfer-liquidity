# Zero-helper arbitrary-fringe identity and exact nonclosure theorem

**Status: source-exact universal family identity; deterministic summary-update claim REFUTED.**

Let c1<...<c6 be ordered core keys. Let U,V be ANY two BSTs on the same m additional keys in the open interval (c4,c5); m may be zero. A tree is written k(left,right), and omitted children are empty.

Define

    A = c6( c2(c1, c3(empty,c4(empty,c5(U,empty)))), empty ).

Both B variants have outer skeleton c6.left=c5, c5.left=c4, c4.right=V, and all other outer children empty. Their c4.left trees differ:

    L: c1.right=c2, c2.right=c3;
    R: c3.left=c2, c2.left=c1.

Access x=c2 with KEEP. In both variants d_A(x)=1 and d_B(x)=4, hence a=1,q=2 and 2a-q=0. A performs one left-oriented zig. B_L performs LR then LL; B_R performs LL then LL, in exactly the source order. The input root labels are the SAME c6,c6; the output root labels are the SAME c2,c2.

Put C(z,w)=H_{additional keys} before the access. More explicitly C=z^5 w^3 J_{U,V}, where J is the internal paired-depth profile of U,V. The roots/internal shapes of U and V may differ; only the common ordered key set is required. No access descends into them.

## Depth tables prove the identity

|Core key|A before|B_L before|B_R before|A after|B_L after|B_R after|
|---|---|---|---|---|---|---|
|c1|2|3|5|1|1|1|
|c2|1|4|4|0|0|0|
|c3|2|5|3|2|3|2|
|c4|3|2|2|3|2|3|
|c5|4|1|1|4|1|1|
|c6|0|0|0|1|2|2|

The c1/c3 swap has equal A depth, so both input global histograms are identical. The A fringe root stays at depth5. In B_L it stays at depth3, whereas in B_R it moves to depth4. Every fringe key moves rigidly by the same amount; its internal structure is untouched.

Consequently, with H0 the common input and HL/HR the two outputs,

    H0(C)=1+z*w^4+z^2*(w^3+w^5)+z^3*w^2+z^4*w+C,
    HL(C)=1+z*w+z*w^2+z^2*w^3+z^3*w^2+z^4*w+C,
    HR(C)=1+z*w+z*w^2+z^2*w^2+z^3*w^3+z^4*w+w*C.

Subtracting gives the exact uniform identity

    HR(C)-HL(C) = (w-1)[C+z^2*w^2*(z-1)].

This is an identity in the formal polynomial ring Z[z,w,C], so substitution of ANY realizable fringe polynomial C is permitted. It was also independently checked symbolically. Arbitrary m/internal geometry enter only through C; there is no finite-n induction guess.

## What is refuted

There is no deterministic successor-histogram rule using only (n,rootA,rootB,H,accessed key,dA,dB,a,q). All these inputs agree between the variants for each fixed U,V, yet the output histograms differ. Even C=0 suffices: the remaining 2x2 mixed term is nonzero. For C nonempty, its A exponents are>=5 and cannot cancel the core difference at rows2/3.

This does NOT refute an arbitrary nonlinear potential F(n,rootA,rootB,H): one potential can satisfy inequalities for more than one successor. The previous quotient construction correctly retained this nondeterminism. At m=1, reading the existing seven-key table gives Phi7=-2 at both inputs and -3 at both outputs, also after reflection. No table was refitted; the zero edge has potential drop1, and that is legal.

## Physical-domain reachability and closure

These are real present-key BSTs, not symbolic abstract-only witnesses. For any m, n=6+m>=4. Levy–Tarjan v3 Theorem3.4 provides splay request sequences between any same-key BSTs of that size. Starting from a common diagonal, KEEP requests can reach (B,B), then DELETE requests reach (A,B). After the selected KEEP, DELETE requests align A' to B', and KEEP requests return both to the common diagonal. Thus these helpers occur inside admissible exactly closed original Pair Access walks. This argument uses existence of connecting source requests, not a sign bound.

Primary source: [Levy–Tarjan, Theorem3.4](https://arxiv.org/html/1907.06310v3#S3). The theorem was checked directly. Independently, the m=0 controls include complete explicit connecting words and full pointer/frame replays. Their totals are (A,Q)=(16,4) and (20,5), so neither is a Coarse-Double counterexample.

Controls at m=0,1,2,5 and both mirrors verify the algebra/source wiring only; they do not replace this arbitrary-fringe proof. There were zero finite fits and zero larger finite graph searches.
