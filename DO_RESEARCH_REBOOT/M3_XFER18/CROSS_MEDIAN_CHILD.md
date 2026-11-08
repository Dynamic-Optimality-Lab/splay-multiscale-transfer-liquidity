# Two credits on a unique marked child across the central cut

The new public class C_right has a marked synchronized root a<=4,
a real marked Score child b>=5 at A R, V(s)={b}, and core depth(b)<=2.
Every original mask is allowed. In particular a need NOT be the
smallest mark and a,b need NOT be consecutive marked keys. There
are no PORT/nonreal cuts. Other observations may be real anonymous
or unmarked nodes; their unobserved children and private supports
are arbitrary. All unused fields, sigma and original B data are free.
C_left is the actual opposite class: marked root a>=4, marked b<=3
at L, V={b}, core depth(b)<=2. Include both in C.

For corrected D_spread define F=max(D_spread,2*1_C).
THEOREM: each previously valid original LOW row survives, and EVERY
C-source original LOW row holds for F. Thus every original nonnegative
incoming row to C is valid, including all zeros arriving at these
public classes. R1-R4 and the previous range/HIGH/h0 glue remain.

## H1: the return ends in E1

At a fresh C_right source b is an actual child: G cannot invent a
distinct nonroot Score b from source owner a. Its proper A prefix is

       a(A,b(B,C)) -> b(a(A,B),C).

Only b is an eligible marked H1 target by V={b}. Its weight is1/2
because its core depth is1/2. In the B output the old root a has
depth at most2 by the completed old-root lemma. Every core>b belongs
to the new root's right subtree, which contains at most8-b<=3 cores;
ALL such cores therefore have output depth<=3.

Every other marked observation at the full A output is either a or
a label>b. Indeed the A/B block roots were already observed as source
L/RL and hence contain no distinct marked root by V={b}. They keep
their depths or move down; their descendants do not newly rise into
the shadow. Only C's children can be newly exposed, and they exceed b.
G fallbacks read old owner a, or its two children A/B; those roots
are unmarked or read a again. A ghost C parent also reads those same
old children. No marked key between a and b, or below a, is invented.
All full-target marked observations have core depth<=3, so E1 gives
F(t)>=1. Thus 1/2+F(t)-2>=0. No other H1 exit exists.

## Gamma1: all helpers cost at least2

Use the already proved global deep-helper theorem: initial helper
B depth>=3 implies original weight>=2, regardless of A support.
Only initial helper depths1/2 need consideration. We do not erase
Score-bearing helpers or change terminal-only q.

For a MINIMUM helper, the actual A helper can be at L/LL/LR.
After its access an eligible terminal is old a, old b, or a newly
exposed lower marked label y<a. Keys between a,b remain inside B
below terminal depth2; keys>b remain below b.right and are also too
deep. This follows from the three original arbitrary-block identities

 a(f(A,B),b(C,D)) -> f(A,a(B,b(C,D)));
 a(p(f(A,B),C),b(D,E)) -> f(A,p(B,a(C,b(D,E))));
 a(p(A,f(B,C)),b(D,E)) -> f(p(A,B),a(C,b(D,E))).

Here some block roots can be terminals only when their actual depths
allow it; overincluding every y<a makes the B bound stronger.
Minimum-helper depth1 forces source core root a=0, with no lower
terminal. At depth2 source B is a(0(f,Esub),Rsub); old a has depth2,
and the path to any lower y contains at most a+1<=5 cores below f.
Old b lies in a's untouched right subtree; its source B depth<=2
gives new depth<=2+2=4. Hence every eligible terminal has pre-B
depth<=5, q<=2 and H2 weight4-q>=2. This permits other marks below a.

For a MAXIMUM helper, the only eligible A location is RR, below b.
R is the present Score b, and RL lies below b, so neither can be
the maximum helper. The exact A pair is

 a(A,b(B,f(C,D))) -> f(b(a(A,B),C),D).

Eligible marked terminals are a,b, or a newly exposed y>b at C's
root. All marks below a or between a,b are at depth>=3 afterwards.
Helper depth1 would force a=8, contrary to a<=4. At helper depth2,
the proper B is a(L,8(T,f)); if b<8, depth(b)<=2 forces b to be T's
root. Its helper output is f(8(a(L,b(M,N)),E),E). Old a,b have
depth2/3; any y with b<y<8 lies in N and has depth at most
3+(7-b)=10-b<=5. Score8 has depth1. If b=8, no larger Score exists
and the two old marked roots are shallow. Again all original H2
prices are at least2. No restriction on private anonymous counts
or rank ties is added; the count uses only distinct present Scores.

The actual C_left calculation reverses the primitive directions and
ordered roles: its maximum-helper lower terminal count is9-a<=5;
its minimum-helper newly exposed lower count is b+2<=5. It is a
proof on actual opposite source forms, not reflection of a private
witness or a psi label.

## Remaining forms and preservation

Gamma0 is the saved every-psi-floor/range theorem applied to max(F,psi).
This agrees with F at the actual C source (debt2) and actual marked
LOW target (retained psi floor). Gamma1 is range-safe by the previous
section. The completed LOW normal forms exhaust all genuine edges.
HIGH/h0 uses the unchanged range and absorbing-region glue.

If an old source is not raised, its residual only gains a target
increment. If raised, it has new value2 and the foregoing proof covers
every possible original exit. This proves row preservation separately
from global feasibility, plus the fresh-source property required by
EXACT_SOURCE_DEBT.md. All old unmarked-source rows and Gamma0/Gamma1
zeros stay closed. No finite tests or completed-check replays are used.

In particular a zero child access from a marked old root b>=5 to a
marked a<=4 is repaid whenever its FULL destination has V={b}:
old-root core depth<=2 puts that literal destination in C_right,
so its new debt2 pays any range-two source. The actual opposite gives
old root b<=3 to marked a>=4. Other target shadows stay quantified
in the still-open 36-slot partition; this theorem does not silently
discard them or close all marked zero edges. Continue those cases.
