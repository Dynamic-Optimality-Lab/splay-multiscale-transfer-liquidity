# Exact obstruction to naive interval-support induction

Status: free-term ordinary-splay identity, source replay pending. This
refutes a proposed reduction, not the scalar theorem or all reductions.

A tempting internal-neutral proof restricts the source to a proper key
interval and applies a smaller-support CD theorem. This requires proving
that the restricted operations are the SAME ordinary bottom-up splays,
with exact physical costs/bits. Single rotations restrict correctly, but
their grouping into splay doubles can change. Here is an exact witness.

Take g<p<x<u and the full source tree

    T=g(empty,p(empty,u(x,empty))).

Restrict to the interval[g,x] by ordinary BST trimming, discarding u.
Then T|I=g(empty,p(empty,x)). In the ORIGINAL tree an access to x uses
RL on p,u,x followed by a terminal zig on g,x, producing

    S_x(T)=x(g(empty,p),u).

Therefore

    S_x(T)|I=x(g(empty,p),empty).

But splaying x in T|I is one RR DOUBLE and produces

    S_x(T|I)=x(p(g,empty),empty).

The complete labelled trees differ. On full keys4,6,7,8 this is the actual
access7 from4(empty,6(empty,8(7,empty))). The full event count is H2,Q1;
the projected ordinary access has H1,Q1, and the two surviving rotations
have the opposite parent/pivot grouping. No synthetic projected splay is
an original source operation merely because it has the same root/key set.

This failing operation embeds in an ACTUAL original paired-closed source.
Start the common pair at T; reach it from the common right vine on
{4,6,7,8} by KEEP8,KEEP6,KEEP4. Use the closed KEEP word

    7; 4,6,7,8; 7,6,4; 8,6,4.

The middle ascending/reverse sweeps restore the right vine; the final
three visits restore T. A=B throughout, so full paired closure is exact
and Q<=A on this source. No statement here refutes Coarse-Double.

Thus an arbitrary-support representation must retain enough event
pairing/parity information to prove a valid lift, or explicitly finance
the projection correction. Subtree-cluster lifetimes by themselves are
a complete FORWARD annotation, not a proved ordinary-splay source
reduction into smaller-support instances. That missing source bridge
must remain separate from the neutral donor-capacity argument.
