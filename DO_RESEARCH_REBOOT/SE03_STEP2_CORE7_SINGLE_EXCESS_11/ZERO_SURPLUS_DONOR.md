# Zero-surplus regime is universally impossible

## Incoming-path source lemma

Let T be ANY ordered BST skeleton on a fixed finite Score set S. A genuine
ordinary bottom-up Score-target splay ending in a Hamiltonian skeleton
(one path through ALL S) has at most one double, Q<=1.

Proof for BOTH orientations. The new root x of a path skeleton is the
minimum or maximum Score; otherwise Scores on both sides would force two
nonempty root children. Hence its original Score search path is all L or
all R. Every double is therefore LL or RR, with any terminal zig retained.

For LL the exact source formula is

    G(P(x(A,R),C),D) -> x(A,P(R,G(C,D))).

It updates the rebuilt target-right subtree R to P(R,G(C,D)). After ONE
double R is nonempty. A SECOND outer LL makes a permanent Score fork at P:
its left R and its right G both contain Scores. Every later outer frame
reattaches this processed subtree rigidly, and a terminal zig also keeps
the fork. The final skeleton cannot be a path.

For RR the separate formula is

    G(A,P(B,x(L,D))) -> x(P(G(A,B),L),D).

It updates rebuilt L to P(G(A,B),L). After ONE double L is nonempty; a
SECOND RR makes a fork at P, with nonempty G and L. All subsequent outer
frames and a terminal zig keep it. Thus Q>=2 is impossible in either
orientation. Mixed-path cases cannot have an extremal target and are
excluded by that source-order fact, not by an all-SS assumption on core7.

This is a free-tree induction with arbitrary hangers. Its number-of-Scores
parameter is unrestricted. The same structural proof appeared for nine
Scores in the inherited Hamiltonian artifact; no refuted debt normalization
or fixed-chart changing-chart inference is reused.

## Application to the actual core7 predecessor

At the unique H1/Q3 macro e*, the full BF target has depth6: BF paths
stay in the actual fixed seven-node core. Consequently the path contains
ALL seven Scores, so its actual input skeleton is Hamiltonian.

Take the immediately preceding GENUINE full macro e-. All nongenuine
KEEPs/DELETEs between its end and e* freeze BF; their A work remains in
the original e* segment. Core constancy gives the SAME labeled seven
Scores at both ends of e-. That actual splay ends in the Hamiltonian
input of e*, so the lemma gives Q_-<=1. Its actual H_->=1 gives

    2H_- - Q_- >=1.

Hence the actual positive own-packet surplus Splus is at least1. This is
an independently derived SOURCE bit supply condition, not an assumption
of the original total inequality or a Hall condition.

In the zero-surplus candidate all other macros would be H1/Q2, and e-
could not be e* since its Q differs. The forced Q_-<=1 contradicts that
candidate. Equivalently the actual preceding macro already supplies a
positive term in Splus. Thus NO actual member of P_(7,1) has Splus=0.

The conclusion is UNIVERSAL IMPOSSIBILITY of the zero branch, not a
donor invented from a zero inventory. Positive-surplus funding plus the
all-paid endpoint theorem now cover every actual source period. No
positive anonymous helper is assumed or required. The proof uses only
actual full BF geometry, not BE shape, recent-key charts or finite words.
