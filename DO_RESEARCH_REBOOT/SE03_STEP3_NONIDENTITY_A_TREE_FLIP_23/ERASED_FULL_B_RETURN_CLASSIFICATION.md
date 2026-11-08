# FLIP23-B — exact full/erased B separation

Status: mathematical derivation; independent audit pending. This proof
uses actual full/erased trees, never a projection chosen by recency.

## 1. Full B normal forms at the helper cuts

Let a,b,c be the actual unmarked core operands on the access path, with
G<a<K<c<C<b<R. The full B hanging trees F0..F7 are globally consistent
source operands, different from the A hangers. The remaining marked
chain containing x is inside F2 or F3 as dictated by actual order.

At the G helper cut:

    B_G^- = G(F0,a(F1,R(b(K(F2,c(F3,C(F4,F5))),F6),F7))).

Its actual C path is RR,LL,RR from the root, three bottom-up SS doubles.
After C the full tree is

    B_C = C(a(G(F0,F1),c(K(F2,F3),F4)), b(F5,R(F6,F7))).

The next G access is LL and gives

    B^+ = G(F0,a(F1,C(c(K(F2,F3),F4),b(F5,R(F6,F7))))).

Thus Q_F(I_G)=3+1=4 and full B is NOT neutral.

At the R helper cut, before g:R:

    V0=K(F2,c(F3,C(F4,F5)));
    B_R^- = G(F0,b(a(F1,V0),R(F6,F7))).

The initial R access is RR and produces

    R(b(G(F0,a(F1,V0)),F6),F7).

The following C access has three SS doubles (RR,RR,LL in BOTTOM-UP
execution order), yields the SAME B_C, and the final G yields B^+.
Therefore Q_F(I_R)=1+3+1=5. The actual word, every core operand and every
private subtree is retained in these formulas. C22's actual root-degree
classification forces these paths; no abstract B-state realization is
inferred from them.

Thereafter v:R has2 full doubles and p:G has1, yielding the inherited
Hamiltonian full chain before e:x. Hence Q_F(D_G)=7,Q_F(D_R)=8. Under
the frozen deep source profile Q_F(e)=6. All demands remain at their
ORIGINAL final KEEP occurrences, which need not equal the A-event times.

## 2. Erased B — a top-root return theorem

After ordinary access G from an old root R>G, R is either the direct
right child of G or an outer right grandchild through P. Consequently
the R,G word is either zig/zig or RR/LL, and restores the WHOLE erased
tree. Its double counts are epsilon,epsilon with epsilon in{0,1}.

For I_G, B_E starts rooted at G after g:G. Every s:C KEEP is erased;
t:G is an auxiliary root repeat. All intervening nongenuine KEEPs are
current-root identities or erased C. Thus B_E^+=B_E^- and Q_E(I_G)=0.
The earlier retained h:R,g:G put R in the required top G frame, so the
subsequent v:R,p:G pair returns that same erased tree, Q_E=2epsilon.

For I_R, B_E starts at G after h:G from retained j:R. g:R and t:G form
that exact top-root return with s:C erased between them. Q_E(I_R)=2epsilon.
The next v:R,p:G pair repeats it on the SAME erased input, with the SAME
epsilon. Thus Q_E(D_R)=4epsilon, Q_E(D_G)=2epsilon.

The full and erased costs at each retained R/G KEEP satisfy q_E<=q_F;
C contributes no erased demand. Thus E_D is a SUBSET of F_D at actual
occurrence/ordinal IDs. This is proved here, not inferred from equal sums.

## 3. Optional outer pairs, without assuming their erased neutrality

The earlier h,g pair in the anonymous endpoint cases is erased-neutral
IFF its first opposite target is already a direct/outer grandchild of
the current erased root. Necessity: after the return splay, that target
has depth<=2; depth>=3 initially cannot be restored. A mixed depth2
first access followed by a zig changes the middle parent, whereas the
direct/outer cases are the inverse formulas. This gives an exact test.

The inherited spine does NOT force this guard at j's erased state, so
no automatic B_E return is claimed there. Retain such intervals directly
unless their exact guard is supplied. Their full h/g costs remain2+1=3;
their erased cost must be read from the actual B_E state when nonneutral.
Even where erased-neutral, their A anonymous outer flip remains nonidentity.

Reflection reverses the complete physical order/child sides and proves
the opposite orientation with identical costs and explicit original IDs.

## 4. Complete erased-neutrality test for inherited phase subwords

Throughout h..p the actual erased root is G or R; C is erased. Remove
only erased C commands and KEEP identities of the current erased root
from a proposed phase subword. Its remaining KEEP targets alternate
between the two keys. Let ell be their number and r the input root.

The whole erased tree returns IFF either ell=0, OR ell is positive and
even and the opposite key is initially a direct/OUTER grandchild of r.
Odd ell changes the root. For even ell=2m, let P_r be one opposite/root
pair. After that pair, the opposite key is a direct/outer grandchild by
ordinary final-root placement. Hence P_r is idempotent: P_r^2=P_r.
If its first pair did not return, further identical pairs cannot restore
the original input. The direct/outer test above is thus necessary AND
sufficient, not just a sufficient guard. Private populations are included.

In the returning case Q_E=2m*epsilon with epsilon0/1 given by the initial
direct/outer shape. In the nonreturning case every step remains exactly
the original ordinary splay on its actual tree; no neutrality or zero
cost is assigned. Together with A's finite endpoint table this classifies
all erased-neutral/nonidentity inherited helper subwords without assuming
all flips have the same physical A normal form. Noncanonical/overlapping
ones can be retained directly in the corrected comparison.
