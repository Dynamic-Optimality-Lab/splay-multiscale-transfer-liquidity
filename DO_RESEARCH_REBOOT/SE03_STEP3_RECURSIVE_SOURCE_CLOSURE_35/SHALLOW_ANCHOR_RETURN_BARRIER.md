# SHALLOW35 — three consecutive shallow monotone returns are impossible

Target: test a specific simplest source realization of MODEL35.
Conditions: actual consecutive A accesses a,x1,a,x2,a,x3, with
a<x1<x2<x3, and no intervening positive A event. Zero-event identities
may be retained. Each access to xi is hypothesized to have exactly one
A StepEv. Initial A and all private terms are arbitrary. Reflection
covers a>x1>x2>x3. No original B state or donor map is invented.
Dual: an actual depth-at-most-two path for all three targets.
Bridge: excludes this realization template of three H1 consumer macros;
it is not a proof that every negative coalition has this template.

Before each xi the A root is a. Cost1 means edge depth1 or2. Since xi>a,
the first path is either a->x1, a->p->x1 with a<p<x1 (RR), or a->p->x1
with a<x1<p (RL). These three cases exhaust the hypothesis.

* Depth1: splay x1 and return a by two opposite zigs restore the original
  tree a with direct right child x1. For x2>x1 to have depth<=2, it must
  be the direct right child of x1. The RR splay x2 and LL return a leave
  the a->x1->x2 right chain. Every key x3>x2 then has depth>=3.
* RR depth2: the RR splay x1 and LL return a restore the original
  a->p->x1 right chain. Every x2>x1 already has depth>=3.
* RL depth2: the RL splay x1 and zig return a leave a->x1->p as a right
  chain, with arbitrary off-path terms. For x2>x1 to have depth<=2,
  x2 must equal p. Its RR splay and LL return a again leave the
  a->x1->x2 chain, forcing depth(x3)>=3.

All other internal/private relations are rigid hangers in these exact
frames. Thus at least one xi access costs>=2. Reflection swaps the
directions and preserves the argument. QED.

For a putative three-consecutive-consumer MODEL35 source with Q_i=3,
this forces at least8 own bits instead of6. If the common two-bit pool
also belongs to N(S), total eligible capacity is at least10>=9, so that
specific proposed negative realization fails.

Exact remainder: consumers may be separated by other genuine accesses,
the returning anchor may vary, target order may turn, or extra positive
A operations may appear. None of those changes is known to admit a
source-preserving removal preserving the negative cut. They cannot be
silently included in this lemma or enumerated as if a finite source
catalogue were complete. REAL35 remains unresolved for that complement.
