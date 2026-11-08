# R22-A — the seventh source predecessor has H>=3

Status: mathematical derivation complete; independent audit pending.
This strengthens C21's H>=2 conclusion without changing its source domain.
Notation/families are EXACTLY C21 EXTREME_NONLOCAL_SUPPLY, part4:

    A_G1=G(A,C(x0,R(D,E)));
    A_G2=G(A,R(C(x0,D),E));
    A_G3=G(A,P(R(C(x0,D),E),F)), P>R;
    A_R1=R(C(G(A,x0),D),E);
    A_R2=R(G(A,C(x0,D)),E);
    A_R3=R(P(A0,G(A1,C(x0,D))),E), P<G;
    x0=x(B0,B1), G<x<C<R.

The actual old marked root before j is K, G<K<C,K!=x. Its destination
after j is the A_Y family, Y=G or R. No total-H<=2 natural macro from K
can produce any member of that family.

## Single changing access

The old root of ONE ordinary splay, regardless of length, ends at depth1
or2 in the final top event. But every allowed K strictly between G,C,
K!=x, lies below x in every displayed family, at depth>=3. Thus one
changing Y access, even costing two events, is impossible.

## Two one-event changing accesses, y then G

Every other operation is an A root repeat and remains in the original
source. The final G event puts its old root y at G.right or at the OUTER
position G.right.right. In A_G1 these positions are C,R; in A_G2 they
are R or keys above R; in A_G3 they are private keys above R. Thus y>=C>K.

The first access y>K cannot enter the initial K.left operand containing
G, so K stays an ancestor of G. To access G next from y in one event,
its path must consequently be y,K,G. An extra ancestor would require
another event. The LL event leaves G.right=K<C, contrary to every A_G
member's right child >=C. This also handles arbitrary anonymous y>R.

## Two one-event changing accesses, y then R

If y>R, both y and R exceed K. The initial K.left operand containing G
stays attached to K under both accesses, whereas every A_R family has G
an ancestor of K. Contradiction.

If y<R, final-root placement in A_R puts y at R.left or R.left.left.
Those positions imply y=C or y<=G, including anonymous keys below G.
If y=C>K, the same rigid K.left argument contradicts the final family.
If y<=G<K, the first access preserves K.right containing R. A subsequent
one-event R access must have path y,K,R and leaves R.left=K. The required
left child is C or <=G, never K. Contradiction. Two changing accesses to
the same final target with no intervening change are impossible.

All distributions of totalH<=2 and all anonymous helpers are exhausted.
Therefore the ACTUAL seventh predecessor j has H_j>=3. It has Q1,u0,
beta1,z1, so its original h_Lambda/h_B own image occupies only its first
two physical bits. At least FOUR later original bits exist. This is
physical source reserve, not effective freedom under a. QED.

## Sharpness of the A-only resource bound (not a global source witness)

For G<x<K<C<R take

    T=K(x(G(A,B),D),C(E,R(F,J))).

The ORIGINAL operation word D_C,K_G has A costs1 and2:

    D_C: C(K(x(G(A,B),D),E),R(F,J));
    K_G: G(A,C(x(B,K(D,E)),R(F,J))).

This is A_G1, with all actual ordered operands retained. A compatible
local B root K with marked-leaf child G gives the desired genuine Q1
final KEEP. Thus pure A geometry cannot force H>=4. No reachable closed
A/B/erased owner embedding is asserted for these arbitrary starting
terms, and this is NOT a refutation of the frozen funding theorem.
