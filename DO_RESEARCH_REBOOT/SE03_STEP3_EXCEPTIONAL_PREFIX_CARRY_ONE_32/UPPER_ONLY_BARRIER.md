# FR32-U — arbitrary one-event upper words cannot hide debt two at return

Status: uniform symbolic proof for a proper activated source subclass;
static graph arithmetic audit is separate from source replay. Not principal
FR32-CARRY1. All permitted ordered gap terms stay literal, not bounded.

Start with the immediate post-u H1 activation9: it forces the variable A
subtree root9 at physical depth2. A becomes

    9(7(5(L5,R5),L8),11(R10,13(L12,R13))).

The full B subtree below9 is fixed

    L=6(5(lower1..4,F5),8(7(F6,F7),F8)).

Consider ANY finite sequence of genuine upper targets9,11,13, each with
whole macro H1, before the first lower target in{1,3,5}. The unique positive
A access in each such macro is to its terminal upper key. Hence its A
upper skeleton always is one of the ordinary three-key forms determined
by its marked root, with L_A=7(5(...),L8) attached intact to minimum9.
Anonymous terms10/12 remain off-path; no deeper future access is assumed.

## Exhaustive upper B source normal forms

Write a9,p10,b11,q12,c13 and ordered gap terms L,l1,...,l5. The seven forms:

    A=a(L,p(l1,b(l2,q(l3,c(l4,l5)))))
    B=b(p(a(L,l1),l2),q(l3,c(l4,l5)))
    C=c(q(b(p(a(L,l1),l2),l3),l4),l5)
    D=c(p(a(L,l1),q(b(l2,l3),l4)),l5)
    E=a(L,p(l1,c(q(b(l2,l3),l4),l5)))
    F=a(L,q(p(l1,b(l2,l3)),c(l4,l5)))
    G=c(q(a(L,p(l1,b(l2,l3))),l4),l5).

They start at A. Direct symbolic LL/RR substitutions give EXACTLY these
genuine permitted upper edges; other nonroot upper targets have odd or
non-SS paths. Root repetitions are retained in actual macro costs.

|edge|target|Q|sigma at H1|
|---|---|---|---|
|A->B|11|1|0|
|A->D|13|2|-1|
|B->A|9|1|2|
|B->C|13|1|1|
|C->B|11|1|1|
|C->F|9|2|2|
|D->E|9|1|2|
|E->D|13|1|0|
|E->B|11|2|-1|
|F->G|13|1|0|
|G->F|9|1|2|
|G->B|11|2|-1|

All private terms reattach in the displayed positions. E values in order
A..G are1,0,0,0,1,2,1. Thus weights also follow directly from
2-Q+DeltaE. This is a complete source-derived seven-form family; it is
not a newly executed seven-state experiment.

## Arbitrary-length bound and forced lower exit

The static values p(A..G)=(0,0,1,-1,1,3,3) satisfy
sigma(edge)>=p(dest)-p(source) on all12 edges. Hence every finite upper
word from A has sum>=p(current). Minimum9 has EVEN physical B depth in
every displayed form. The remaining path to7 is always LRL of length3.
Therefore KEEP7 would have odd path length and is NOT source-valid. A
legitimate first return must first use at least one lower target1,3,5.
This argument is independent of return length and A-only preprocessing.

At the first lower macro, A5 has depth2,3,4 at roots9,11,13 respectively;
targets1/3 have depth at least3,4,5. Every actual A StepEv performs at most
two rotations and reduces the fixed target's depth by at most2. Therefore
the WHOLE exit macro, including DELETE preprocessing, has H at least the
corresponding ceil-half depth. Only9 can be a high-arity B ancestor here.
For targets5/3 (old degree1), sigma>=2c-1-1[E>0]; for1 (leaf),
sigma>=2c-2-1[E>0]. The smallest lower-exit bounds over all3 choices are

    exit_min(A..G)=(0,2,3,3,0,0,2).

Adding p gives(0,2,4,2,1,3,5), all nonnegative. Thus activation-through-
FIRST LOWER has sigma>=0, uniformly in all finite upper repetitions.
The original helper debt at that boundary is at most1. The transient
debt2 in state D cannot be a valid terminal return state and is compensated
before a legal lower exit.

This DOES NOT bound the later lower-to-return suffix. It also does not
classify upper words containing H>=2 macros or a delayed first9. Those
remain in the principal domain. No unknown normalized owner or bank reset
is assumed. Source reflection transports all terms and stencils literally.
