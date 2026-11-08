# A reachable, paired-closed, source-exact counterexample construction

All physical keys are1,...,15; genuine full KEEP support is the8 odd
keys. DELETE is A-only and never physically deletes a key. All splays
are ordinary bottom-up with original ceil(depthA/2),floor(depthB/2) costs.

Let U be the BST on1..13 with marked right spine1,3,5,7,9,11,13 and
each even key2j attached as a leaf LEFT child of2j+1. Let

    As=(15,(14,U,empty),empty).

Let T be the tree formed from U by attaching14 as RIGHT child of13,
then15 as RIGHT child of14. T is the explicit A start tree in
new_A_primitive_rows.json. Initial full B is Z=V+(1,15).

## Exact, finite preparation words

Gamma_K(X,Y) means the shortest ordinary bottom-up splay access word
over K sending X to Y, with lexicographic tie-break in key order. This
is a precise finite word specification, not an invented operation.
Existence for equal key sets of size>=4 is the ACCEPTED Levy--Tarjan
transformation dependency in C33/UNIFORM_A_REALIZATION_OVER_CLOSED_B.md.
Its proof/PDF pins are independently checked. No external numeric cost
convention is used. Every Gamma letter below is an original DELETE.

From As, DELETE1 has depth2 and one LL StepEv. Its first rotation pivots15
and retires15 from every target<=13. Its second rotation pivots14.
Afterward15 is a LEAF, right child of14. Write L0 for the tree on1..14
obtained by removing only this formal off-path leaf15 from the notation,
and L1 for T with that same formal leaf removed. Define G=Gamma_1..14(L0,L1).

Executing G in the ORIGINAL15-key A tree gives exactly T. Proof: attaching
the extra largest leaf15 as right child of the largest low key14 commutes
with every access to a low key. The search never enters15, so15 is never
a rotation operand and stays a leaf; every actual low rotation has its
same rigid hanger. This is a literal off-path lifting, not the refuted
active unary projection and not physical deletion of15.

Let F be the12-KEEP forward subword1,3,1,5,...,1,13, and R the11-KEEP
reverse subword1,11,1,9,...,1,3,1 from SYMBOLIC_B_CLOSURE.md. Define
Av as A's actual tree after F,R from T; this is a deterministic finite
ordinary-splay composition, independent of the following reset. Put
J=Gamma_1..15(Av,As). The original period word is

    KEEP15; DELETE1; DELETE(G); KEEP(F); KEEP(R); DELETE(J).   (W)

All Gamma operation costs are retained, even though their numerical
lengths are not expanded or replayed. Full A returns exactly to As by
definition of J. Full B returns exactly to Z by the source induction;
all DELETEs leave it unchanged. Reach (As,Z,Z) from common diagonal Z
using the finite original A-only word Gamma_1..15(Z,As), outside W.
This proves original reachability, not an abstract state realization.

## Full erased/chart closure and actual period

Erase genuine key3 from BE's processed KEEP subsequence only. Repeat W
from the reachable pair. A/B return word by word; BE with its finite
genuine recent-key chart is deterministic on a finite state set. Define
u,L by its FIRST repeated boundary state after chart warmup. This is a
well-defined finite constructive selection. The actual source interval
I contains the L copies from u through u+L-1 and closes A,BF,BE and both
charts. No numeric u,L or complete Gamma replay is claimed.

Every retained marked key is visited genuinely in this periodic erased
execution; the erased genuine support is7. No smaller-support allocation
is assumed to exist, and no historical fE or a0 is substituted. The raw
SI34 target quantifies over source histories, independently of such maps.

For a legal cut change, apply the original both-endpoint occurrence
bijection to this ONE actual I. The negative cut is invariant because
its pool relations are the exact cyclic ones. No maximum-D cut is
declared legal without its original certificate; the counterexample
does not require choosing a special cut. It survives every permitted
coordinate cut of I, with each physical unit counted once.

## No DELETE-only exact-return loop in the counterexample period

Choose the stated shortest G,J. Each is free of any repeated full tree
along its DELETE word, since removing such a subword would shorten it.
The first DELETE1 starts at root15, whereas all following G targets are
<=14; after it root15 never recurs during that DELETE block. Thus its
concatenation with G has no A-return subword either. The J block is
separated from it and from the next copy by genuine KEEPs. Therefore W,
and the aligned I, have no nonempty contiguous DELETE-only A-return loop.
The reaching prefix is not a donor and need not satisfy this normal form.

This is a mathematical symbolic source construction with canonically
specified finite transformation words. It is not presented as a fully
expanded numerical source stream. All source existence and closure
claims are proved independently of a desired funding inequality.
