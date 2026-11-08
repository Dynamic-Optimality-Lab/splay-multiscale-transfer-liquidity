# DL35 — degree-layer channels, uniformly in support

## Box

Target: a source-exact degree-layer comparison and signed identity on every
original closed maximal core of size2r-1. Conditions: the inherited all-SS
and path-to-star source theorems; literal full period I. Inheritance: C15
path-to-star/leaf-channel proof. Ambiguity: the remaining high-degree holes
need new source supply. Bridge: if no local hole remains, this is a full
comparison; its source inequality gives an original Type B construction.

Let T be the nearest-marked-ancestor tree on r genuine keys. For access x,
let q be its actual B-double count and d the old number of marked children
of x. Each of its q old marked ancestors loses exactly one marked child;
x gains q children. All other marked degrees are unchanged. This is the
inherited original-frame path-to-star theorem, not abstract reachability.

For 1<=k<=r-1 define

    F_k(T)=sum_v min(deg_T(v),k),
    L_k(T)=(r-1)-F_k(T)=sum_v (deg_T(v)-k)_+.

Thus 0<=L_k<=r-1-k. Write b_k for the number of old marked ancestors
whose OLD degree exceeds k and

    kappa_k=min(d+q,k)-min(d,k)=min(q,(k-d)_+).

Every old ancestor of degree<=k decreases F_k by1. Each old ancestor of
degree>k leaves F_k unchanged. x increases F_k by kappa_k. Consequently

    Delta L_k = q-b_k-kappa_k,
    2c-q+Delta L_k = 2c-b_k-kappa_k.                 (DL1)

This identity retains the actual full q and the actual source/destination
trees. There is no chart switch or erased q substitution.

## Literal threshold channels

For a fixed marked key v and threshold j<=k consider the Boolean status
deg(v)>=j on the actual cyclic period. A birth occurs when v is accessed
and its degree increase crosses j. A death occurs at the original B double
whose old ancestor v has degree j and loses its path child. These status
changes alternate by literal vertex/threshold identity on the closed period.

At each macro reserve its first kappa_k actual A-bit units, ordered by
the increasing crossed thresholds. This requires kappa_k<=2H at that
macro; in particular it ALWAYS holds for k=2 because H>=1 for every
genuine natural macro. Pair each low-degree B-double death with the
immediately preceding birth of the SAME (v,j), cyclically in ONE I.

The paired birth has one specified reserved physical bit. Distinct births
at one target use different bits. Different targets occur in different
macros. Alternation gives a bijection on each (v,j). Therefore ALL these
low-degree demands receive distinct original units simultaneously, with
arbitrary repetition, source length and private populations. A wrapping
channel uses one actual occurrence in I, not another symbolic copy.

All remaining doubles are high-degree ancestor demands, b_k per macro.
Use that macro's remaining actual bits, excluding its threshold reserves,
in full-double index order until exhausted. This independent partial map
is injective and has exactly

    R_k(e)=(b_k+kappa_k-2H)_+                       (DL2)

holes when kappa_k<=2H. These are COMPARISON holes, not necessarily unpaid
physical claims under a0. The map is not asserted to contain natural h0;
when complete, the inherited full-map normalization supplies h0 without
changing actual frozen owners. Alternatively DL1 gives a Type B law directly
using selected units that contain h0, under its nonnegative-margin condition.

## Structural path budget

The q old ancestors each have degree>=1. The b_k high ancestors have
degree>=k+1. The total degree of these ancestors and x is at most the
total r-1 edges of T. Hence

    q+k*b_k+d <= r-1.                              (DL3)

This is a necessary source-tree bound, not a realization theorem for
arbitrary degree tuples. It remains true in both ordered orientations.

## Storage and owner limits

Channel IDs alone are not a bounded physical bank trace. When DL1 is
nonnegative on every packet, use the ORIGINAL signed Type B construction
with its actual L_k range and selected c; then prove the appropriate bank
bound. If the comparison is completed by another source law, the accepted
static source-block construction may apply only with that source license.
No locked bit is called free. Original common/E-only/Gamma, chart and cut
compatibility remain as stated in the reservation theorem.
