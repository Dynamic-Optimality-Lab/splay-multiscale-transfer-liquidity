# USR35 — unbounded shared-return cuts and distinct earlier repayment

Status: source-uniform mathematical derivation. Independent static review
pending. The fixed m=3 source and its repair were previously checked; this
document supplies a new parameterized proof, not an extrapolation of that
test. JR35 OPEN; reservation compatibility DEFERRED.

## Frozen IAGS Box

Target: decide whether the frozen MFR next-contact return neighborhood can
have bounded collective deficiency, and identify genuine earlier capacity
on the same sources. Conditions: every integer m>=3, physical keys1..N,
N=6m+3, all odd keys marked; ordinary original Pair Access, all preparation
letters original A-only DELETE. Inherit SSI35, the original Gamma source
realization, natural h0, full source-period transport and static Bank25.
Ambiguity: arbitrary original histories need not have this geometry or
these preparation depths. Bridge: literal parameterized B normal forms,
canonical actual A preparations, one shared return event and distinct
earlier actual natural tails. No global root matching premise is used.

Notation: k(L,R) is an ordered node; empty subtrees are suppressed. V+(a,b)
is the right vine on the inclusive interval, V- the left vine. An empty
interval means empty. Put y=2m+1, u=y+1, G_i=2i-1 and X_i=6m+7-4i.
The source is initially on this fixed physical key set, with no additional
keys needed. Off-path rigid hangers may be transported by free-term
identities only where they preserve the displayed paths; active new
ancestors are NOT included by analogy.

## 1. Exact full-B source, before any A preparation

Set

    B0 = G_m(V-(1,G_m-1), u((y-1)(empty,y), V+(y+2,N))).

Let Bprev be the one LL splay of G_m-2 in B0. Start A=BF=BE=Bprev.
The forward genuine word is, in decreasing i order,

    G_m,X_m,G_(m-1),X_(m-1),...,G_1,X_1,y,1,3,...,2m-1.

Every one of these operations is an ordinary genuine SS splay. Its full-B
double counts are

    (1,3), (2,3) repeated m-1 times, m+1, 1,
    then 2 repeated m-1 times.                         (1)

Here SS is eventwise: successive events of one access may use opposite
orientations. None is a mixed double or terminal zig.

### Complete stage induction, including the middle subtrees

Immediately after G_i the tree is

    G_i(L_i, u(T_i, K_i)),       L_i=V-(1,G_i-1).

For i=m, T_m=(y-1)(empty,y), K_m=V+(y+2,N). After X_m define

    D_m=(y+3)((y+2), (y+5)((y+4),empty)).

For every stage i, immediately after X_i the tree is

    X_i(u(G_i(L_i,T_i),D_i), V+(X_i+1,N)).           (2)

For the transition from i to i-1, two LL events at G_(i-1) give

    T_(i-1)=(G_i-1)(empty,G_i(empty,T_i)),
    K_(i-1)=X_i(D_i,V+(X_i+1,N)),

and restore exactly the displayed after-G_(i-1) form. The next X_(i-1)
=X_i+4 is reached along the six-edge path

    G_(i-1),u,X_i,X_i+1,X_i+2,X_i+3,X_i+4.

Three RR events produce (2), with

    D_(i-1)=(X_i+1)(X_i(D_i,empty),(X_i+3)((X_i+2),empty)).

For the first stage the corresponding six-edge path is
G_m,u,y+2,y+3,y+4,y+5,y+6, proving the base D_m formula.
These are literal LL/RR identities, not a list of enumerated BSTs.
Every indicated subtree has its required ordered interval.

The recurrence gives T_1=V+(2,y). Since X_1=N, (2) becomes

    N(u(1(empty,V+(2,y)),D_1),empty).

The access y performs m RR events inside the right vine1..y and one
outer LL event. Its result is

    y(E_m, u(empty,N(D_1,empty))),
    E_m=2(1,4(3,...,2m(2m-1,empty)...)).             (3)

In (3), KEEP1 has one LL event. Each following odd target3,5,...,2m-1
has an inner LL and an outer RR. Induction leaves the unprocessed E
suffix attached beneath y, and proves the final part of (1). Throughout,
every original B grandparent is odd, every parent even, and the complete
marked ancestor core is all N physical keys. This follows directly from
the displayed trees: every even node has an odd descendant. Intermediate
completed accesses preserve this property by the same SS identities.

Append the SSI35 inverse blocks for these 3m+1 forward accesses, in
reverse access order. The full B returns exactly to Bprev. The forward
paths and inverse ancestor letters visit every odd key: low odds G_i and
y, and all higher odds y+2,y+4,...,N from the successive six-edge paths.
Thus the genuine support is exactly r=3m+2. No declared mask substitutes
for an actual visit. The exact complete word totals are

    k=3m+1,
    M=sum 2^q = 16m-4+2^(m+1),
    Q=2M-2k = 26m-10+2^(m+2).                      (4)

## 2. Original A source with m true unpaid demands

Before each original G_i, use the canonical original A-only Gamma to
prepare

    A_i=G_i(V+(1,G_i-1),
             (G_i+1)(empty,X_i(V+(G_i+2,X_i-1),V+(X_i+1,N)))).

KEEP G_i has A0. The next KEEP X_i is the sole operation of its genuine
macro. It has one RR StepEv and full B Q3 by (1). Its first rotation
pivot G_i loses ancestry of BOTH X_i and y. Natural h0 owns its first
two original B doubles; the third is an actual unpaid demand d_i.
Its A destination is

    X_i((G_i+1)(G_i(V+(1,G_i-1),empty),
                          V+(G_i+2,X_i-1)), V+(X_i+1,N)).       (5)

The first loss G_i->X_i is this event's bit0, not an abstract proxy seed.
Between G_i and its later low reset, the ONLY right-side B grandparent
demotions of G_i are at X_i and y. For later high X_j (j<i), G_i is
inside T_j below the off-path hanging side, so is not a grandparent;
intervening low G_j lie to its left. The low resets before G_i are also
to its left. An actual rotation losing right-side ancestry of X_i cannot
simultaneously be the opposite-side first loss for such a low target.
Consequently the NEXT member of d_i's identical-first-loss direct group
is the actual same KEEP y for every i. No other member is discarded.

After X_1, prepare by an actual A-only Gamma

    A_y=y((y-1)(V-(1,y-2),empty), V+(y+1,N)).

Retain KEEP y (A0), then the original DELETE y-1. This is one terminal
zig, resulting in

    (y-1)(V-(1,y-2), y(empty,V+(y+1,N))).           (6)

Both units of that actual StepEv are real credit units, although only
bit0 represents an actual rotation. All following genuine low resets
1,3,...,2m-1 are <y, leave the whole y hanger rigid, and never make y an
ancestor of their own targets. Thus between contact y and each next
genuine G_i reset, EVERY actual loss y->G_i is at the SINGLE event c
of DELETE y-1. This is exhaustive, including original zero-event gaps.

Hence the m distinct h0-unpaid original demands have frozen MFR return
neighborhood contained in

    {(c,1,0),(c,1,1)}.

It has deficiency at least m-2, with even the virtual zig position
relaxed as eligible and all other owners ignored. The deficiency is
unbounded with r=3m+2. One-consumer or one-proxy injectivity cannot imply
joint expansion; neither arbitrary loss choice nor longer lookback
INSIDE these specified next-contact windows repairs it.

Finish all original inverse KEEPs in A as well, and then execute the
canonical actual A-only Gamma back to Bprev. A and full B close exactly.
Erase a specified genuine key (for example y+2) only in the auxiliary
execution; use the inherited true finite erased/chart recurrence on
repetitions, retaining warmup and the actual first recurrent period.
No Gamma word, full inverse A run, or numerical erased recurrence length
has been computed here. They are exact finite source specifications,
whose existence follows from the separately accepted source bridge.
All their actual costs remain in A. This is an exact symbolic source
family, not a numerical replay of an arbitrary large source.

## 3. Distinct earlier donors on EVERY member of this family

At the start of the first preparation the depth of G_m in Bprev is2.
For each later G_i, (5) from the preceding stage gives its depth exactly
G_i+2=2i+1: three outer edges, then the right vine1..G_i. One rotation
decreases a fixed target's depth by at most1; thus the total actual A
preparation cost is H>=ceil(depth/2). With Q from (1), the actual unused
natural tails have the uniform lower bounds

    tail(G_m)>=1,
    tail(G_i)>=2i for 1<=i<m.                      (7)

Any wrapping final reset only increases the first macro's inventory.
Assign d_i to the LAST actual unit of its preceding G_i macro: bit1 of
its last positive original StepEv. By (7) this is outside the fixed h0
prefix; all m supplier macros and all m donors are distinct. Every pair
retains its actual original occurrence IDs. This pays the m simultaneous
claims while preserving every value of h0. It does not assume that a
fixed auxiliary fE regards those bits as free.

The entire source is also funded, preserving these successful new pairs.
Use SSI35's actual even selector, additionally including each last-tail
donor. Include the fixed partial matching P=h0 union these m pairs.
In each genuine macro an owner-inclusive even selection no larger than
2H exists; select at least two units. Equation (4) gives

    selected-Q >= 2M-Q = 2k = 6m+2 >0.

This source identity, independently derived from rotations, licenses
static source streaming. Cancel the fixed pairs from units and demands;
stream only the remaining units/demands. Working queue<=2, every demand
emitted once, every leftover released once, P preserved. Transport both
endpoints to the one original legal period; no adjacent-copy borrowing.
Reflections follow by the order-reversing bijection k->N+1-k, preserving
all physical event indices, costs, source kinds and matching identities.

## 4. Exact conclusion and open bridge

The frozen return-only rule has UNBOUNDED source-valid deficiency, even
on genuine natural h0 residuals. The SAME full sources admit explicit
earlier simultaneous donors and a complete Bank25 full comparison, with
2A-Q>=6m+2. This refutes a sufficient donor mechanism, not CD or JR35.
All statements are uniform in m, original preparation length and source
repetition. Arbitrary new active private ancestors are not asserted.

The universal root still needs a source theorem for histories WITHOUT
the displayed preparation normal form or SSI inverse closure. Equation
(7) is derived for this family; it must not be imported as a bound on
arbitrary creator macros. The next joint bridge is an actual free-endpoint
theorem for saturated creator/return components, including all frozen
owners, mixed cores, other deficit weights and the cyclic seam.
