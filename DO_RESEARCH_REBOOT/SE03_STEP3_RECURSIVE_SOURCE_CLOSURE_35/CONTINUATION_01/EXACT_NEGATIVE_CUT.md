# The exact three-macro C34 cut

Use the original source W,I from SOURCE_CONSTRUCTION.md. Let ell be the
actual finite LENGTH of G (not its event cost), and let b be the absolute
source offset before KEEP15 in any one chosen copy inside I. Put

    c=b+2,             v_i=b+ell+2+2i.

c is the original DELETE1 immediately after KEEP15. v_i is the original
KEEP x_i in F. Select i=2,4,6, with targets5,9,13. These formulas specify
actual absolute occurrences once the canonical finite words and u,L
are selected; no donor in a different cyclic copy is used.

Each selected full natural macro starts immediately after its preceding
genuine KEEP1 and contains only that KEEP x_i. It has H=1, as verified
by two distinct ordinary-splay implementations on the true local A word.
The symbolic B proof and independent critical replays give Q=3 and old
marked B ancestors {1,x_(i-1),15}.

## Exhaustive retirement pools: no other operation is omitted

1. For g=15, its last genuine KEEP before v_i is the initial KEEP15.
   At c the original A loses15's ancestry of all three targets. Thereafter
   15 remains an off-path leaf throughout G and the forward word, since
   every accessed key is<15. Thus R_m(15)={c}, exactly. The costs of G
   are real but none of its operations retires15's ancestry again.
2. For g=1, its last genuine KEEP is immediately before v_i. The birth
   interval contains only v_i. Its ancestry is lost there: R_m(1)={v_i}.
3. For g=x_(i-1), its last genuine KEEP is the preceding consumer in F,
   AFTER G. The only subsequent operations before v_i are KEEP1 and
   KEEP x_i. By reflected AR2, splaying1 preserves that key's ancestry
   of x_i (1<x_(i-1)<x_i). The selected splay loses it. Hence
   R_m(x_(i-1))={v_i}.

The last two births occur after G, so no preparation/reset or earlier
word occurrence lies in their intervals. The reset J is after every
selected consumer and before the NEXT genuine KEEP15, so it is outside
all three selected birth-to-demand intervals. The same proof applies
within the recurrent L-word period and after legal coordinate transport.

Consequently, with C_t={(t,1,0),(t,1,1)} at these cost1 operations,

    U_m=C_(v_i),      T_m=N_m=C_c union C_(v_i).

This computes the ENTIRE C34 pool, not just a chosen first-ticket subset.
All slot choices in N_m remain permitted. The three demands of each
macro are the actual full B double IDs(v_i,1),(v_i,2),(v_i,3).

## Strict signed violation

There are9 demands and only8 distinct physical bits in the joint pool:
the common pair C_c and the three distinct own pairs C_(v_i). Exactly

    sigma=3, overlap=4, local_unused=0,
    overlap-sigma-local_unused=1>0.

Every pair has6 bits for6 demands and every singleton4 bits for3 demands.
The full coalition is connected and inclusion-minimal deficient; each
macro has private capacity2<3 and own-excess Q3>2H2. All targets are
interior. SOURCE_CONSTRUCTION also removes the A-only-return-loop escape.

The operation and physical IDs are true original occurrences, not chart
labels or a source-independent negative graph. No original cost is
discarded. In particular unselected deep A accesses and the real G/J
preparation have units outside THIS cut's defined neighborhoods.

## This source is Coarse-Double safe

The full B word has Q=46. The11 forward A accesses after the initial
KEEP1 cost13; DELETE1 costs1; the11 reverse KEEPs have distinct successive
targets and each costs at least1. Thus A(W)>=25, regardless of all extra
G/J costs. Therefore 2A(W)-Q(W)>=4, and on I it is at least4L.
The failure is the proposed restricted donor-pool law, not Coarse-Double.
No full original owner/Bank25 architecture impossibility is asserted.
