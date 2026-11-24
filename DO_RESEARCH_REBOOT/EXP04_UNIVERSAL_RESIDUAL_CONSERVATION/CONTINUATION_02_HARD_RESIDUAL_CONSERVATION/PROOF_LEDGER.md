# Continuation02 proof ledger — aggregate original residual conservation

The target is the unchanged R_next^P<=K A for an absolute K. B3/B4 and every
old budget remain fixed. Statements below are auxiliary theorems, not a
claim that the entire target is paid. Status labels do not follow from tests.

## Z1. Return-free terminal-zig words are monotone — PROVED—UNIVERSAL

Domain:any complete physical BST and a contiguous B word in which every
nonidentity KEEP has depth1 (one original terminal zig). DELETEs freeze B.
No assumption on A, support size, Pi or paired closure is used.

A genuine zig requests the current root's left or right child. If roots
u->v increase, u becomes exactly v's left child. A following decrease must
therefore request u and is the inverse rotation, returning the COMPLETE B
tree to its prior state. The reflected statement holds for a decrease
followed by an increase. Erase adjacent inverse returns repeatedly.
In any nonempty reduced word, consecutive root changes have the same sign,
so targets are strictly monotone. Identity root repeats can be dropped.
Every closed pure-zig word reduces to empty, since a nonempty strict monotone
root sequence cannot return to its initial root.

Consequence for the current obstruction: unprotected pure-zig oscillation
traffic cannot furnish an arbitrary long return-free nonmonotone source.
Frozen G/H protection never marks a pure zig. This eliminates that proposed
cheap-walk construction. It does not bound hard residual consumers, whose
accesses have q>=3 and hence depth>=6.

## Z2. Extreme-spine transport for depth<=2 — PROVED—UNIVERSAL

Let E(T) be the union of the actual root-to-minimum and root-to-maximum
physical node paths. A rotation at the root preserves this SET: its two
old spine portions are reattached to the new root without entering any
old interior hanging subtree. A root-level zig-zig is two such root
rotations and also preserves E.

In a root-level zig-zag g-left-p-right-x, x was not on either extreme spine.
After the two physical rotations, the old left spine continues under p,
the old right spine under g, and x is their new common root. Thus
E(after)=E(before) union {x}. Reflection is identical.

Therefore a B-closed word consisting only of accesses of depth<=2 can
contain no root zig-zag; otherwise E would strictly grow and never shrink.
This is a physical structural exclusion, not a global rank-traffic bound.
Deeper accesses can remove spine nodes. No bounded-load charge from this
spine identity to all original residuals has been established.

## R1. Root-coupled small-support B returns — PROVED quantitative class

Domain:an actual cyclic original operation interval I of at most one lap,
with equal A and B ROOT KEYS at its initial boundary, and exact complete
B closure B_end=B_start. Full A closure and complete A=B equality are not
required. Let M_I be the genuine KEEP target support of this original B
return word. Handle M_I empty separately:then Q_B(I)=0.

The B-only closed-core argument of CD5_BASE01/CD5_PROOF.md section2 uses
only B closure and marked ordinary splay, not A closure. Therefore its
full initial path union J_I is fixed at all B boundaries and

    |M_I|<=|J_I|<=2|M_I|-1.

This is a comparison domain, not a replacement of the source's original S.
Every actual B path lies in J_I with complete original hangers preserved.

At the first genuine KEEP, A must change its initially shared root to the
new B target. After each KEEP, actual A and B roots are that KEEP target.
Each later genuine KEEP therefore forces at least one actual A StepEv in
its preceding original interval, including every DELETE helper. These A
intervals are disjoint and lie in I. Thus K_B(I)<=A(I), including the first
access; there is no uncharged first-boundary root discrepancy.

If |M_I|<=b for a fixed integer b>=2, every actual B access has depth at
most2b-2 and q<=b-1. Hence

    Q_B(I)<=(b-1)K_B(I)<=(b-1)A(I).

Take ALL such eligible actual cyclic intervals. Apply Continuation01 C1's
irredundant subcover of their union, with original A StepEv load<=2. Assign
each original R_next^P occurrence in the union to one selected covering
interval. Its ORIGINAL consuming double is an actual double of that interval;
the original three-slot bound gives

    R_small_return(b)<=3 sum_I Q_B(I)<=6(b-1) A(W).

At b=8 this is42A, uniformly over all populations, fringe geometry, period
lengths, interval counts and seams. No comparison initialization, new shadow
Pi, virtual A work, distinct-donor assumption or unbounded nesting is used.

Corollary for the ORIGINAL R_next^P:the same42A payment covers its consumers
in ANY B-closed return interval with at most8 genuine targets. If the whole
source has at most8 genuine targets, its |S|<=15 and old C7 already makes
R_next^P empty. Otherwise, an interval with at most8 targets cannot contain
every KEEP of the source. Its immediately preceding KEEP lies in its cyclic
complement. Extend the interval leftward to just after that KEEP, adding
only DELETEs. Length stays at most one lap, B pre-state is unchanged and
the initial A/B roots now coincide. Its genuine support is unchanged.
Apply the root-coupled theorem to ALL these constructed extended intervals
and take their load2 subcover. This is an explicit construction, not an
assumed boundary donor. It pays the original residual inside the original
unextended intervals as well.

The root condition cannot simply be dropped from the POINTWISE bound:
the complete3-key source starting at the common left vine and executing
DELETE1,KEEP1,KEEP3 is exactly paired-closed. Its suffix KEEP1,KEEP3 is
B-closed with M={1,3},Q_B=2,A=1 and initially different roots. It violates
Q_B(I)<=(|M|-1)A(I). Extending to include the actual DELETE1 gives A=2
and the valid coupled-root bound. The extra original work is not invented.

Let R_wide be the literal part of original R_next^P outside this union.
The valid new auxiliary partial inequality is

    R_next^P<=42A+R_wide,
    Q_B<=(83+48 C_seq+102 C_DF)A+R_wide.

The original41+... interface with its ORIGINAL R_next^P remains unchanged.
It is not proved that R_wide is bounded or empty. No genuine simultaneous
R_next^P escape in this subclass has been certified; do not call this
Outcome B or universal closure.

## L1. Recurrent local-domain localization — PROVED—RESTRICTED STRUCTURE

Let an original source contain m consecutive exact copies of an actual
paired-closed operation block V, with A(V)=a>0. Its original complete B
comparison is initialized at that block's actual B pre-state. Let J be its
initial path union, N=|J|, and let c=m_cyc+L_cyc be the integer cyclic
target cost on J. All actual KEEP operations are retained; original Pi and
residuals are untouched. The source's global S may be arbitrarily larger.

For k consecutive copies, complete paired return makes their actual cost
ka. Collapsing root repeats gives at most k*m_cyc+1 target blocks and at
most k*L_cyc rank travel. The raw local comparison cost is therefore

    D(V^k)<=N+1+k*c.

If delta=5a-c>0, choose k=ceil((N+1)/delta). Then D(V^k)<=5ka. If the run
contains at least k copies, every operation in that run belongs to some
contiguous k-copy original interval. Thus every original noncheap residual
consumer in the run is already locally paid under frozen C5, regardless of
global rank gaps or later support-restoration work. This is an exact
source-preserving localization proof, not an empirical small-rank assertion.

If a=0, B closure implies Q_B(V)=0 by the original zero-work argument.
If delta<=0 the theorem makes no coverage claim. If fewer than k copies
are present, the initialization cost is not waived. A nonclosed block,
changed copy, hypothetical access or prefix work cannot be substituted.

## G1. Ordered-gap extension of a fixed active source — PROVED invariance

Start with an active BST on an ordered key set. Replace each null gap by
a fixed complete physical BST of private keys strictly inside that gap.
Perform only active-key accesses in both original A and B. No private node
is on an active access path. Each physical splay rotates exactly the old
active operands; every gap subtree is rigid and reattaches at its unique
inorder gap. Thus active paths, StepEv cases/costs and complete active/full
return equivalence are preserved for arbitrary gap populations and shapes.

Assume for SET comparison that both the old active S and extended full S
are their entire respective key sets. A nonempty active subtree interval
[i,j] expands to those active keys and every gap subtree between its two
neighboring outside active keys (including both boundary gaps when they
exist). This expansion E is injective because projection back onto active
keys recovers[i,j]. The labels rooted inside private gaps form one fixed
SET F0 common to A and B. Hence

    J_full(A)=E(J_active(A)) union F0,
    J_full(B)=E(J_active(B)) union F0.

During active-only operations, exact carrier membership, signs and
presence/absence timelines of expanded nonempty labels are preserved.
Frames avoid the global extreme active keys exactly when their originals
do. G guards, actual hard-gap costs and H guards are preserved whenever
the preceding actual KEEP gap is within that unchanged active word.
Complete B return identities are preserved as well.

For any fixed active-only physical interval, raw/G/H retained trajectories
and their INITIAL PATH-UNION domains contain no private gap key. Their
local comparison ranks/costs therefore stay the same. Increasing GLOBAL
rank distances by adding genuinely visited private keys elsewhere cannot
destroy an already eligible such local interval.

Original Pi/U certificates whose entire defining windows and relevant
first-hit cohorts lie in active-only copies can be transported by E.
Extra support-generating operations outside those windows must still be
checked for cohort interference and original R_* selectors. This theorem
does NOT automatically certify full-source R_next^P membership. The larger
sources below are screened/certified at explicitly recorded scopes only.

Corollary excluding a whole counterexample grammar:take at most512 active
keys, any paired-closed active-only word starting and ending at a common
gap-refined diagonal T, and append an all-KEEP physical return R from T to
itself that visits the added gap keys. Cut the full period immediately
before R. During R,A and B run the identical splay execution; every B bit
is decreasing, so there is no G/H guard. The chronological erasure starts
with only T recorded; its complete return removes ALL of R, even if R has
internal returns. What remains is an active-only closed comparison, with
path union on at most512 active keys. Hence L_cyc<=9m_cyc and
m_cyc+L_cyc<=10m_cyc<=10A(full source). This permitted full-period certificate
rules out B4 for the entire grammar, at ANY physical gap population.

This argument deliberately chooses the cut before R. A closed unprotected
detour inserted in the middle of an arbitrary loop-erasure history can
intersect older states and need not leave the same reduced path. No false
cut-independence or guard-monotonicity assumption is used.

## First unresolved aggregate implication — OPEN

None of Z1,Z2,R1,L1,G1 controls the aggregate ORIGINAL residual outside
bounded-support returns and already funded local recurrent blocks. The
missing source-uniform statement is a bounded-load or telescoping physical
payment for residual-bearing, large-local-support, hard-guarded transport
whose possible ancestral-return windows overlap across arbitrarily many
scales. No proportional donor supply, bounded sharing or small rank traffic
is assumed. R_wide<=K'A remains open.

## A1. Prefix-double and current-ancestor payments — PROVED—UNIVERSAL

The current-ancestor payment is the already proved optional EXP04 T7
class, now activated in this partial interface. Its6A is explicitly paid;
it is not a new discovery or an extra free use of the earlier budget.

These are direct actual A-work payments, independent of comparisons or
rank thresholds. G_h is the original cyclic incoming KEEP gap, a_G=A(G_h).
All targets, doubles and original residual occurrences remain unchanged.

Prefix class:at each KEEP h pay the original residual gaps whose consuming
B parent has original StepEv index j<=2a_G. There are at most2a_G such
physical B doubles and at most3 gaps per parent. The actual KEEP-gap A
StepEv inventories are disjoint, so

    R_prefix<=6 sum_h a_G(h)=6A.

This includes EVERY old cheap KEEP-gap case q(h)<=2a_G, while additionally
paying lower parents at hard accesses. It preserves the old6A budget if
used in place of that cheap class. No integer quota is inferred from data.

Current-ancestor class:pay an original residual parent (h,j,g) if g lies
on the actual strict A access path just before original operation h.
Since A actually splays that target x, g->x must be lost during this SAME
A access. A relation g->x can be lost only by a physical rotation demoting
g; select its first such loss in this A access. Distinct B doubles of one
splay have distinct old grandparents, so they select distinct A rotation
bits. Distinct operations have disjoint original A event IDs. Three gap
slots per parent therefore give

    R_current_ancestor<=3 R_A<=6A.

This does not revive the refuted arbitrary-last-loss injection:that old
selector can select one earlier loss at several DIFFERENT consumer times.
Here every selected A bit lies in its consumer's own operation h, and its
demoted key identifies g. There is no claim when g is already A-absent.

The union of prefix and current-ancestor classes has budget12A and contains
the former6A cheap class. Substituting this union into the earlier complete
accounting gives a valid strengthened partial interface

    Q_B <=(47+48 C_seq+102 C_DF) A + R_upper.

R_upper is the literal subset of the original R_next^P outside these new
classes. Its every consuming parent has BOTH j>2a_G(h) and old g absent
from the actual pre-A target path. All old B3/B4 conditions still hold.
Separately, for the IMMUTABLE target residual,

    R_next^P <=12A+R_upper.

Adding the small-return class R1 gives

    R_next^P <=54A+R_upper_wide,
    Q_B <=(89+48 C_seq+102 C_DF)A+R_upper_wide.

These are partial aggregate theorems only. The old41+... interface and
literal R_next^P definition are preserved. No universally empty residual
or universally bounded R_upper_wide is claimed.

## C2. Compulsory protected-return core — PROVED—UNIVERSAL certificate lemma

Use the frozen original H guard set on the entire cyclic source. Let E be
the union of ALL actual cyclic complete-B-return intervals of at most one
lap whose operations contain no H guard. Every operation erased by any
raw/G/H interval normalization belongs to E:its matching pre/post B states
are exact, and the cache reset prevents erasure across a protected KEEP.
Even if earlier loops were already erased, the underlying ORIGINAL interval
between these two equal original states is a guard-free exact return.

Consequently every original KEEP outside E is compulsory:it is retained
by every allowed local comparison through it and every full-period cut,
including G because H is a subset of G. Raw keeps all operations. This
claim does not assume cut-independence of chronological loop erasure.

E has an exact linear construction. Cut just after any H guard and split
at successive guards. In each unprotected segment, group full B boundary
states by EXACT complete-state identity. For each state, the interval from
its first to its last occurrence covers all its return intervals. A range
union produces E. Never join equal states across a guard. If there are no
H guards, the whole B-closed period is unprotected and E is the entire lap.

Let P be the set of compulsory KEEP targets and let Y be their cyclic
target subsequence in original order. Every full-period comparison's
initial path-union domain J contains P. Integer log-rank distance is a
metric; deleting noncompulsory targets cannot increase total cyclic travel,
and restricting rank to P cannot increase distances. Cyclic block count
also cannot increase under deletion. Hence EVERY permitted full-period
cut and variant has

    m_cyc+L_cyc >= m_cyc(Y)+L_cyc,P(Y).

If this explicit lower bound exceeds10A, all periodic alternatives fail
at once. It is only a sufficient negative certificate, not a proof that
some certificate exists when the lower bound is small. All local5A tests
and full original Pi/R_* membership remain separate obligations.

This is a source-uniform way to distinguish unavoidable retained rank
traffic from removable cheap oscillations. It provides no upper bound on
the COST of the original hard residual and is not Outcome A or B by itself.

## D1. Four-double body plus real restoration — PROVED—RESTRICTED FAMILY

Domain:the entire physical source consists of a common-diagonal all-KEEP
prefix P; an arbitrary actual body U in which each KEEP has q_B<=4; and
the real restoration R=KEEP1..N followed by the decreasing active keys
below N. The active set is an equally spaced set of M>=2 keys including
1 and N, with spacing d>=1,N=1+(M-1)d. Initial T is the actual result of
that decreasing active sweep from the complete left vine. The source is
exactly paired-closed, since the full increasing sweep produces the left
vine from any BST and the remaining sweep produces T. All body DELETEs
and restoration work are measured.

P has Q_B(P)<=A(P), since both original executions are identical. The
roots agree at its end. Each genuine body KEEP forces original A work in
its disjoint incoming body gap, so K_B(U)<=A(U). Thus Q_B(U)<=4A(U).

For R's full increasing scan, sequential access gives Q_B<=C_seq N.
For its M-1 decreasing active targets, the full physical initial path union
has size at most N, the target count is M-1, and each internal rank jump
has distance d. Since ceil(log2(1+d))<=d,

    D_reverse<=N+(M-1)+(M-2)d<=3N,
    Q_B(R)<=(C_seq+3C_DF)N.

The increasing scan forces at least N-1 actual A root changes, and the
first decreasing target forces one more. Hence A(R)>=N, with no prefix
or initialization donation. Combining the disjoint actual pieces proves

    Q_B <=(4+C_seq+3C_DF) A,
    R_next^P <=(12+3C_seq+9C_DF) A.

The second inequality uses the safe original three-slot upper bound
R_next^P<=3Q_B. These constants are absolute over ALL populations, body
lengths, helper patterns and histories satisfying this restricted grammar.
Rank traffic may be large, and consumers need not be excluded. The crucial
restriction is the body's ORIGINAL physical four-double cost cap, not a
finite support cap or a fitted comparison threshold. No proof that all
admissible sources admit such a decomposition is claimed. This theorem
does not establish the unrestricted objective or Outcome B without a
genuine independently certified simultaneous escape.

Metadata correction:some earlier screening-family strings said depth8.
The actual enforced predicate was q_B<=4, which permits depth9 with a
terminal zig. Every proof here uses the exact four-double predicate.
