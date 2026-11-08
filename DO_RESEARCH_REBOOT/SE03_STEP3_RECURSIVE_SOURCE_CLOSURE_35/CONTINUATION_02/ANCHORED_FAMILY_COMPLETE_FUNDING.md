# AF35 — complete source funding for the anchored family, all r>=4

Mathematical scope: the following explicitly constructed family, not all
sources of a given support. Frozen-owner promotion is conditional on the
original compatible E_r1/E_r3 input. See GLOBAL_FULL_H_AND_FROZEN_EXCHANGE.md.

## Exact source

Use As,T,n,m of RC35, physical keys 1..n, genuine marked keys all odds,
and initial full B the integer right vine Z on 1..n. The original word is

    KEEP n; DELETE 1; DELETE G;
    KEEP (1,3,1,5,...,1,m);
    KEEP (1,m-2,1,m-4,...,1,3,1); DELETE J.             (AF)

G is the inherited shortest-lex ordinary-splay word on 1..n-1 taking the
low tree after DELETE1 to T with leaf n removed. Leaf n at the right of
n-1 remains rigid throughout G. J is the inherited shortest-lex reset
from the actual post-reverse A to As. DS35 proves that input is exactly T.
Existence/reachability uses the inherited finite source transformation
lemma, as in CONTINUATION_01/SOURCE_CONSTRUCTION.md. None of G,J or the
diagonal reaching prefix is numerically expanded here. All their original
DELETE costs are retained. Shortestness is not used to lower-bound cost.

The full B closure induction in CONTINUATION_01/SYMBOLIC_B_CLOSURE.md
has the same free frames with 15 replaced by n and i<=r-2. Its forward
states Fi and reverse states Ui, with C(i+2,r-1), give exact return to Z.
They include all physical integers, not a marked quotient. A returns to
As by J. The original source is therefore paired-closed and reachable.
Erasing 3 in B alone and taking the actual eventual recurrence aligns
an actual period of L copies, with every occurrence kept. This alone
does not invent a certified smaller-support allocator fE.

## All natural macro classes

Let xi=2i+1, 1<=i<=r-2. Apart from the first anchor, all non-reset macros
are single KEEP operations. The g=n macro contains the previous J.

| Class | Number per word | Full Q | Actual A H |
|---|---:|---:|---:|
| J;KEEP n | 1 | r-1 | >=ceil(r/2) by RC35 |
| DELETE1;G;KEEP1 | 1 | 1 | >=1 from DELETE1 |
| first forward consumer x1=3 | 1 | 2 | 1 |
| forward anchor 1 before xi, i>=2 | r-3 | 1 | 1 |
| forward consumer xi, even i>=2 | floor((r-2)/2) | 3 | 1 |
| forward consumer xi, odd i>=3 | floor((r-3)/2) | 3 | 2 |
| reverse anchor 1 | r-2 | 1 | >=1 |
| reverse nonanchor consumer | r-3 | 2 | >=1 |

The counts give Q=(r-1)+1+2+4(r-3)+3(r-3)+1=8r-18.
For r=8, Q=46 and every one of the 24 KEEP operations is included.

### Uniform A forward geometry

The first access 3 and its following access 1 are inverse single zigs,
so just before x2 the original T is restored. Put a=1, p=x(i-1),
x=xi, y=x(i+1), and Ei the even singleton 2i. Just before an even i,
the active tree has form

    (a,0,(p,L,(x,Ei,R))).

One RR gives (x,(p,(a,0,L),Ei),R), H=1. The next anchor a is one LL
and gives (a,0,(p,L,(x,Ei,R))). If the next consumer exists, substitute
R=(y,E(i+1),R'). Its path has depth3: bottom RR then a final zig gives

    (y,(a,0,(x,(p,L,Ei),E(i+1))),R'), H=2.

The next anchor is one zig and leaves

    (a,0,(y,(x,(p,L,Ei),E(i+1)),R')),

the next even case with a larger opaque L. These identities are ordinary
bottom-up frames and prove the cost row for arbitrary r, without a bounded
tree inventory. Rigid even leaves and the high term are never accessed.
All reverse targets differ from the previous root; hence H>=1 is enough
there. The exact full B costs come from the separately inherited symbolic
integer-tree induction, not these A frames.

## Complete original-source license and literal h

Start with natural h0: within each natural macro pair its first
min(Q,2H) demand slots to its first physical bits in chronological
(t,j,b) order. RC35 shows the g macro is own-solvent. All classes are
own-solvent except even forward consumers, each missing ONLY its third
slot. For such a consumer v let u be its IMMEDIATELY PRECEDING actual
anchor KEEP1. Its H=1,Q=1 leaves bit (u,1,1) unused by h0. Define

    h((v,3))=(u,1,1),

and keep every h0 entry. The anchor and consumer are one consecutive
two-macro source block. Different even consumers have different anchors;
their actual operation inventories are disjoint. Every other macro is a
one-macro block. This is a complete partition of ONE physical period,
including all G,J operations. It supplies all B slots exactly once and
extends h0. No bit is assumed free under a0: h is INDEPENDENT comparison.

This is original Type A: source-forced distinct anchor spares at the exact
family geometry. Equivalently, coarsen the three/every-even pairs and use
Type B with D identically0 and c=H on each block. RC35 and the table prove
2c-Q>=0 on every block, independently of CD or fE. All h0 units are among
the selected 2H original units. This is not the false blanket adjacent
predecessor rule: its hypotheses include the FULL AF source geometry.

## Bank25, no support-dependent carry

Apply the accepted static-within-SOURCE-block convention of C33
SOURCE_SOLVENT_BLOCK_AUGMENTATION.md. Before a block, its complete literal
h pairs are fixed by the above source rule. For each actual A StepEv in
that block admit its two original bits ONCE, emit each selected h pair
under that license and release any unused bit. The unassigned bank trace
is 0 -> 2 -> 0 at every event. Demand endpoint time is recorded literally;
this is NOT an added chronological demand-payment restriction. No unused
bit is hidden in assigned output, admitted again, or borrowed across copies.
Each block closes empty. Thus working<=2 at every support r and any G/J
length, even though c for the reset block can grow. Bank25 is respected
by an explicit trace, not the sufficient bound 2max(c)<=25.

Cut internally after the final reverse KEEP1, just before J. Constant D=0
makes every full block cut maximal. This internal construction cut does
NOT replace the separately fixed auxiliary Step1 cut. Transport BOTH h
endpoints by C14's actual occurrence bijection onto the supplied I. If the
erased recurrence uses L copies, choose these disjoint blocks in each
actual copy, using absolute offsets; no previous/next copy is borrowed.

## What this establishes and what it does not

AF35 proves an independent complete h, its Type A/B source law and Bank2
for arbitrary finite support in this family. At r=8 it repairs the ENTIRE
SI34 source, not merely its nine selected demands. The old SI34 negative
pool cut remains true because the new anchor bits lie outside those pools.

No legitimate fE,a0,Gamma is fabricated for arbitrary smaller support.
Frozen-owner extension follows only when the original compatibility and
retirement/transport hypotheses are supplied. The theorem gives no
partition or charging rule for sources outside AF. Consequently UCF35,
E_r2/E_r3 on arbitrary sources and unconditional Gate U remain OPEN.
