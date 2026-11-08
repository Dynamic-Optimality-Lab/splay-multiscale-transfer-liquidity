# What scalar smaller-support CD actually supplies on open segments

This is a conditional uniform source theorem. It uses the already known
cycle-excision argument, not a new graph computation. It supplies a valid
alternative to assuming spare credit from scalar CD. The remaining global
coverage is explicitly OPEN.

Fix a finite ordered key set of n nodes and an integer r>=6. Assume CD(r-1).
Fix any marked set M0 with at most r-1 keys. Consider any finite original
Pair Access segment H reached by an arbitrary original legal prefix, whose
KEEP targets in H lie in M0. DELETEs in H may target ANY present key; its
start need not be a diagonal or paired closed. Define source weight

    w(H)=2A(H)-Q(H),
    qmax=floor((n-1)/2),
    F_n=(Cat_n^2-1)*qmax.                                 (1)

For n<=1 take F_n=0. Then

    w(H)>=-F_n.                                          (2)

Proof: there are at most Cat_n^2 full labeled A/B states. If H repeats a
full paired state, the intervening loop is original, fully closed and
reachable, with KEEP support<=r-1. Its weight is nonnegative by the induction
hypothesis. Remove it: full state equality makes the remaining segment
legal and preserves its starting reachability. Continue mathematically to
a simple path of at most Cat_n^2-1 edges. Each original edge has a>=0 and
q<=qmax, hence weight>=-qmax. Its total is at least-F_n; adding back all
nonnegative removed loops proves(2). No pair-state graph is built, queried,
enumerated or executed. This is a source proof over arbitrary finite n.

The dependence on n, including all private fringe nodes, is explicit.
Equation(2) is not a private-inventory-independent uniform debt formula.
It does not say a nonclosed segment has nonnegative weight. The same
argument proves the stronger bound-F_reachable if a smaller independently
proved reachable-state count exists; no such count is assumed here.

## A valid uniform conditional covering principle

Choose z in an original closed walk with r genuine KEEP keys. Partition
the cyclic word into source pieces P1,H1,...,Pk,Hk so every Kz lies in a
P_i. Every H_i therefore has KEEP support<=r-1 and satisfies(2), regardless
of full/erased B disagreement. Let K_i count KEEP occurrences of P_i.
If actual source A capacity gives the independently checkable guard

    2A(P_i) >= F_n+qmax*K_i       for EVERY i,              (3)

then Q(P_i)<=qmax*K_i gives w(P_i)>=F_n. Add(2)-(3) over the disjoint
source pieces to conclude w(gamma)>=0. Every original A event and B
double belongs to one piece; no physical capacity is reused. This argument
is uniform in r,n,length, DELETE timing and exact fringe topology. It
does not require any B resynchronization or stronger B-only funding.

For r=6 the induction premise is the sealed CD(5), so this is a valid
restricted CD consequence at its stated SOURCE CAPACITY GUARD. No claim
is made that it provides genuinely new coverage beyond all inherited
compositions; no suitable new six-key paired family has passed that audit.

## Why this still does not close the induction

There is no theorem that every source walk admits a z and a partition
satisfying(3). A short low-cost z episode can have much less than F_n
capacity. Scalar CD bounds only a whole closed auxiliary history and
cannot eliminate the per-segment startup deficit by assertion.

Repetition does not solve this: repeating gamma m times repeats its k
separations and can require mk startup payments. Adding one bounded-cost
preparation to the entire repeated word does not fund mk independent
boundaries. Grouping all z occurrences into one piece instead leaves
that piece's weight uncontrolled and may simply restate the original
target. A proof needs a shared state potential or a source-complete
nonduplicating transfer that amortizes these boundaries. That obligation
remains OPEN; equation(2) alone is not the requested uniform implication.
