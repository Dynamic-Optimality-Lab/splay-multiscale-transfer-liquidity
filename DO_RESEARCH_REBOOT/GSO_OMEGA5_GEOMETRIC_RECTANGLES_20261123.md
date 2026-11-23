# GSO accounting with empty request rectangles

**2026-11-23. The universal bound remains open.** This checkpoint proves an
absolute A-work budget for separated request rectangles, identifies a physical
condition for surviving signed debt, and records the exact obstruction to
charging every loss to its own rectangle. The remaining step is a packing
proof across different producing KEEPs.

## Original objective and budgets

Take any admissible exactly paired-closed source $W$ on a fixed ordered set of
physical keys. A splays on every KEEP and DELETE. B splays only on KEEP. A
DELETE leaves its key in both trees. Both full labeled trees return to their
initial states. Count all original preparation and restoration. The reaching
prefix supplies no paid work.

Let $A$ count original A double steps and terminal zigs, $R_A\le 2A$ count
individual A rotations, and $Q_B$ count original B doubles. A genuine B KEEP
changes the B root. Its count $K_B$ satisfies $K_B\le A$ by the disjoint cyclic
A gaps between successive genuine B KEEPs.

The frozen $H=5$ bank uses blocks of five consecutive physical ranks and its
greatest clipped cyclic balance. It partitions original B double IDs into
funded $P_5$ and unpaid $\Omega_5$, with

$$
Q_B=P_5+\Omega_5,\qquad P_5\le45A.
$$

An absolute upper bound $\Omega_5\le KA$ gives relaxed Universal
Coarse-Double with $Q_B\le (45+K)A$. The reverse bound on $\Omega_5$ follows
from $\Omega_5\le Q_B$. This is the same universal cost objective throughout.
[Frozen policy and verifier](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/README.md).
[Earlier complete-period accounting](GSO_OMEGA5_COMPLETE_PERIOD_20261123.md).

The existing cap-five straddler calculation bounds the visible unpaid doubles
$V_5\le10A$. Each maximal packet of cap-five-invisible unpaid doubles begins
after a distinct funded or visible double in its KEEP. The first five
doubles of each genuine KEEP are funded if present. Thus the packet entrance
count $M_5\le P_5+V_5\le55A$, and the continuation count $C_5$ satisfies

$$
\Omega_5=V_5+M_5+C_5\le65A+C_5.
$$

The distinct old-grandparent block count $F_5$ is the sum, over those packets,
of the number of distinct old-grandparent blocks minus one. An old grandparent
key occurs at most once per KEEP, and each block has at most five keys.
Consequently $F_5\le C_5\le5F_5+4M_5$ and
$\Omega_5\le285A+5F_5$. This counts original occurrences at a coarser
resolution and is equivalent to bounding the continuations up to the known
linear term.

A counted A-only sweep followed by exact A-only restoration can refill every
block without changing B. Inserting this once before many copies of any
closed period makes previously always-empty blocks historical while the
greatest bank trajectory eventually reproduces the old paid labels. A
uniform estimate restricted to historical encounters after such a refill
would therefore give the full $F_5$ estimate by dividing by the number of
copies. This is why the geometric proof uses the real B rotations that
create or destroy reach. [Original budgets and subsequent records](https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d).

## What the literature supplies

- Chmel et al. prove an ordinary-Splay competitive factor
  $O(\log\log n\,(\log\log\log n)^2)$. Comparing with the original A rotations
  on $r$ copies eliminates the additive initialization term as $r$ tends
  to infinity. The factor in $n$ survives. The public Lean development
  reports a refined ordinary-Splay factor that also depends on $n$. Its
  Cha-Cha result uses Cha-Cha's schedule. [Splay trees are almost dynamically optimal](https://arxiv.org/abs/2607.18498).
  [Public Lean statements](https://github.com/vaclavrozhon/dynamic-optimality#what-is-proved).
- Levy and Tarjan establish the connection between approximate monotonicity
  under taking request subsequences and dynamic optimality. Their splay
  coercion also supplies a way to restore arbitrary fixed-support trees
  with a linear-cost word of actual splays. This is the closure primitive
  used below. [A Foundation for Proving Splay is Dynamically Optimal, Section 3](https://arxiv.org/html/1907.06310v3#S3).
- Jiang et al. give direct-sum theorems for Wilber's Alternation and Funnel
  bounds under access-word composition. The composed objects in those
  theorems are lower-bound counters. Transfer of a physical splay trace
  would require its own argument. [Hardness Amplification for Dynamic Binary Search Trees](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ISAAC.2024.42).
- Demaine et al. show that the points touched by a rooted-subtree BST
  execution are arborally satisfied. Their geometric lower-bound argument
  uses horizontal neighbors across a vertical line. The proof below
  applies that idea to original A work and to repeated-key histories
  using an explicit separation condition.
  [The Geometry of Binary Search Trees, Lemma 2.1 and Section 4.4](https://people.csail.mit.edu/mip/papers/arboral/paper.pdf).

## Exact signed accounting of continuation losses

A key's lower and upper reach are the minimum and maximum of its current B
subtree interval. A right rotation shrinks the lower reach of the demoted key
and expands the upper reach of the promoted key. A left rotation reflects
this. Each continuation has two endpoint losses, one for each demoted old
path key. Associate each loss with the latest actual gain of the same key
and endpoint. Exact B closure guarantees such a gain in the cyclic past.
A repeated lap gives its original occurrence and its chronological offset.

The budgeted gain coordinates are non-target gains from funded doubles,
the last target gain on each side of a genuine KEEP, and non-target gains
from visible unpaid doubles and packet entrances. The total number is at
most $P_5+2K_B+V_5+M_5\le112A$. A target can gain several times while
splaying, but only its last gain of a given direction can be the most
recent gain for a later KEEP.

Fix an integer $b\ge1$ and allow the first $b$ losses at each budgeted gain
coordinate. Write $S$ for the actual number of losses using those slots.
Each continuation can supply at most one non-target gain with a provisional
capacity of one. Write $E$ for those provisional slots that go unused,
including a slot with no physical non-target gain. Let $R$ count the excess
uses after these capacities. With $C=C_5$,

$$
2C=S+(C-E)+R,\qquad C=S+R-E,\qquad S\le112bA.
$$

Every counted loss occurs in one of the three terms. An unused provisional
slot supplies the subtraction $-1$ in this identity. It issues no original A
credit.

In an LL double the old parent loses lower reach and gains upper reach.
A later LL with that same old parent creates a fresh upper gain. If the
previous upper gain served no continuation before being replaced, its slot
is unused. It can cancel the excess from the next lower loss on the same
gain. The chronological predecessor is unique on that key and endpoint,
so one unused output is used at most once in this cancellation. RR
reflects the argument.

## Forced crossings and their failure as local payments

For a lower loss at target $x$, let $m$ be the new minimum of the demoted
key's subtree. The old subtree contained $x$, and the new one has $x<m$.
The next lower loss using the same gain has target $y\ge m$. The A root is
$x$ and $y$ at the two B phases, so a real A root rotation crosses the cut
at $m$ in between. The upper-loss case is symmetric.

The aligned family below refutes bounding the load on those crossings.
For every fixed $b$, after the first $b$ low KEEPs the original surviving
prefix on B's next minimum path has at least $h/2^b-O_b(1)$ vertices.
Each new minimum splay retains the lower old parent of each LL and moves
the old grandparent off that spine, with at most one unpaired old top
vertex. The exceptional paid, visible and entrance events number $O_b(1)$
in this low segment. Therefore the final low KEEP has at least
$h/2^{b+1}-O_b(1)$ continuations whose two old pivots were lower parents
and had continuation losses at all $b$ earlier low KEEPs.

Both pivots still use their original paid lower gains. Both have already
used their entire capacity. The endpoint after the preceding KEEP is
exactly $b+3$ because the pivot survived on the path to that next minimum.
Between the losses the only possible A root crossing is the one moving
the root from $b+2$ to $b+3$. The complete sources thus force unbounded
load on one crossing for any fixed capacity $b$. Their full A cost
includes the earlier paid producers and the final restoration.

The exact 590-key replay at $b=1$ verified 15 such doubles in B(3628,7)
through B(3628,21), with both arms pointing to A(3628,1), primitive 2.
The 1,190-key replay at $b=2$ verified 14 such doubles in B(7329,9)
through B(7329,22), with both arms pointing to A(7329,1), primitive 2.
[Crossing proof and independent replays](https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d).

## Empty rectangles from original B ancestry

Use rank horizontally and genuine B KEEP occurrences vertically. Consider
an upper loss of key $p$ at target $y>p$. Its last actual upper gain was
born in an earlier KEEP at some target $x\le p$. An old path key is
demoted at most once per KEEP. If it is also promoted as the old parent
in its double, that promotion gains the opposite endpoint. Since the
earlier gain the upper endpoint
never increased and has stayed at least $y$. An intervening KEEP of any
$z$ with $p<z\le y$ would find $z$ under $p$ and demote $p$, driving the
upper endpoint below $z$. It would then exclude $y$. Thus there is no
intervening target in $(p,y]$.

Among genuine targets since the producing KEEP and before the consuming
KEEP, choose the last in $[x,p]$. That occurrence and the consuming
occurrence at $y$ give opposite corners of a closed rectangle containing
no other request point. No later target is in the left portion by the
choice of the last request. No intermediate target is in the right
portion by the endpoint argument. Reflect the order for a lower loss.
A gain across the cyclic seam uses its actual copy in the preceding lap.

For non-target upper gains created in one KEEP, the old parents lie on
the final right subtree's left spine. Each earlier lower-rank parent is
in the left subtree of each higher-rank parent on that spine. Hence their
upper ranges $(p,\max I_B(p)]$ are disjoint. Lower gains lie on the
reflected spine and have disjoint lower ranges. The two sides are
separated by the producing target. A single later KEEP can therefore
consume at most one non-target gain from any one producing KEEP.

## Surviving signed debt requires a real reentry

It is enough to control the same-side continuations $C_s$. Use
$S_s,R_s,E_s$ for the signed ledger restricted to their two loss arms.
Opposite-side doubles produce only target gains. The old budget applies,
so $C_s=S_s+R_s-E_s$ with $S_s\le112bA$.

Assign each excess loss to the preceding continuation loss on the same
key, endpoint and actual gain. Each original loss arm receives at most
one such successor. The contribution of a same-side continuation to
$R_s-E_s$ is its number of those successors minus one when its own
non-target output goes unused.

An LL with old parent $p$ and old grandparent $g$ leaves $J=I_B(g)$
as the right subtree of $p$. A successor lower loss of $g$ using the same
gain must target $J$. Any loss spending $p$'s new upper gain must also
target $J$. If there is no later KEEP in $J$, the only possible successor
is the repeat of $p$'s lower loss and the unused upper gain cancels it.
A positive contribution therefore requires a later original KEEP into
$J$. RR uses the reflected interval. A reachable side range supporting
an actual continuation loss has at least 13 keys. The first possible
continuation is double seven, whose nearer old ancestor was at least
13 edges from the target on the original B path.

Until its first interior KEEP, $J$ remains a literal B subtree with
unchanged internal shape. Rotations on a search path to an exterior
target can move its attachment. They cannot pivot at a vertex inside
$J$. The simultaneously pending intervals are consequently laminar.
A fresh interval that overlaps a still-pending one must strictly contain
it. To create a smaller interval with a root inside the older subtree
would require a pivot inside it and an earlier interior hit. Intervals
from one KEEP are disjoint because they hang from the final spines.

For the first real entry into $J$, choose the last preceding genuine
target between the original producing target and $p$, inclusive. This
gives an empty request rectangle by the same argument as for an endpoint
loss. In the signed ledger, use the two loss arms and the one output of
each original double exactly once. Multiple same-side continuations in
different producing KEEPs can still have the same first interior hit.

## A uniform budget for separated rectangles

Let $X_r$ be the genuine B KEEP request points in $r$ copies of a closed
source, cut just after a genuine KEEP. If such KEEPs are absent then
$\Omega_5=0$. Group all original A operations in the cyclic gaps ending
at the genuine KEEPs. For each gap take the union $H_t$ of the actual A
search paths in that gap.

Each union is a rooted hull in A at the beginning of the gap. Inductively,
a new search path follows the existing hull and can extend into a hanging
subtree whose internal tree has stayed fixed. Splaying rearranges the hull
and reattaches the unchanged hanging trees. The final root serves the
genuine KEEP target. Every search adds at most one new key per actual A
rotation, since its starting root is already in the hull. Therefore

$$
\sum_t (|H_t|-1)\le r R_A\le 2rA.
$$

The rooted-subtree geometric representation makes $Y=\{(k,t): k\in H_t\}$
an arborally satisfied set containing $X_r$. This means that the closed
rectangle between any two nonaligned points of $Y$ contains a third point.
Thus the number of horizontal adjacent pairs of points in $Y$ is exactly
$\sum_t(|H_t|-1)$.

Take a collection $\mathcal R_r$ of distinct empty request rectangles
with an order in which the following test holds. Each rectangle has a
cut at a non-key rank strictly inside it, and the segment of that cut
through the rectangle's full closed height is disjoint from every later
rectangle.

For a rectangle with request corners at lower left and upper right, choose
the highest point in $Y$ left of the cut and inside the rectangle, breaking
ties to the right. Then choose the lowest point on the right at or above
the first point, breaking ties to the left. Both choices exist by the
request corners. If their heights differ, the choices leave their closed
subrectangle unsatisfied. They must instead be horizontal neighbors.
Reflect the rank order for the other orientation. The selected pair
crosses the cut inside the current rectangle. A later rectangle cannot
use that pair, since containing it would intersect the earlier cut
segment. It follows that

$$
|\mathcal R_r|\le 2rA.
$$

This argument permits repeated keys and accounts for the original A-only
operations in their actual gaps. It uses the sum of touched hull sizes
as a budget. It imposes no upper bound on what a single root crossing
can expose to B.

## Exact obstruction and replay results

In the aligned preparation, all selected losses at the focus KEEP 3
get their lower gains from exterior high producers. The exterior KEEP
targets descend to $h+1$. For each selected loss, $h+1$ is the last
request on the producing side of its demoted key. The canonical
rectangle is the same rectangle from KEEP $h+1$ to KEEP 3. The number
of original arms mapping to it grows with $h$. The multiple-low-KEEP
variant gives the same collision for excess arms at its final KEEP.

The following counts are for the full original $C_5$ ledger at $b=1$.
Maximum multiplicity counts all endpoint loss arms at one canonical
rectangle. The empty collection has multiplicity zero.

| Complete source | Keys | $A$ | $\Omega_5$ | $C_5$ | $S$ | $R$ | $E$ | $R-E$ | Distinct rectangles | Max multiplicity |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| W257 | 257 | 1,230 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Counted DELETE 4 | 290 | 6,211 | 16 | 14 | 28 | 0 | 14 | -14 | 1 | 28 |
| Split-pivot control | 290 | 6,393 | 16 | 14 | 28 | 0 | 14 | -14 | 1 | 28 |
| Active-ancestry stretch | 377 | 7,112 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| Aligned KEEP 3, KEEP 4 | 590 | 12,699 | 60 | 54 | 78 | 30 | 54 | -24 | 2 | 78 |
| Parallel interval lifetimes | 2,120 | 45,826 | 287 | 7 | 14 | 0 | 7 | -7 | 1 | 14 |

The 30 excess losses of the 590-key source all map to its KEEP 4
rectangle. All 54 provisional slots are unused over the exact period.
That collision refutes assigning every excess a separate payment on the
raw rectangles. Its signed balance is negative. The table checks the
accounting and its adversaries at exact finite values and supplies no
universal packing assertion.

### Aligned family construction

For $h$ a large multiple of ten set $q=h-2$ and $n=h+5q$. Let
$p_j=j+2$ and $x_j=n-4-5(j-1)$ for $1\le j\le q$. The initial
common tree has root 2, left leaf 1 and right subtree $T_1$. The
root $p_j$ of $T_j$ has no left child and has the exterior left chain
$x_j+4,\ldots,x_j$ on its right. Attach $T_{j+1}$ on the left of
$x_j$, with $T_{q+1}$ empty.

Use counted A-only coercion to make the exterior keys a descending
left vine above key 3. At key 3 put the subtree rooted at 1 with
right child 2 to the left, and a right vine $4,\ldots,h$ to the right.
Then request exterior keys from $n$ down to $h+1$, KEEP exactly the
$x_j$ and DELETE all others. The B producer KEEP $x_j$ uses two
exterior LLs followed by the RR with old parent $p_j$ and old
grandparent $j+1$. The RR puts $[1,j+1]$ on a left vine under
$p_j$. A terminal exterior zig can finish the producer. At the end B
is rooted at $h+1$ above the full descending internal left vine.

The high-producer bank calculation applies for any seam. Just before
each main RR, its target block and the block of $p_j$ contain at most
eight credits combined. At $p_j=5i$, for $2\le i<h/5$, the old
internal block is behind the target, the next internal block and
the exterior predecessor block in the frozen priority. It retains
at most two credits. At $p_{j+1}=5i+1$ the next RR sends that old
block to zero. A never refills those middle blocks during the exterior
sweep. The last internal block retains at most two, so at the start
of the B phase of KEEP 3 the total internal stock is at most seven.

Use KEEP 3 for the single-burst obstruction. For the repeated-use
obstruction use consecutive KEEPs $3,\ldots,b+3$. The final LL of
KEEP 3 moves the exterior subtree to the right of $h$ and can import
at most five internal credits. Later low B footprints are internal.
Each additional low A phase and voucher can refill at most 15 internal
credits. The low segment thus has at most $12+15b$ paid doubles.
After each low A phase the right vine $[x+1,h]$ stays under $h+1$.
If six higher internal B ancestors remain at an LL, both primitive
losses leave at least six straddlers in every proper A holder. Only
$O_b(1)$ LLs fail the continuation test across the low segment.
This is also the bound on exceptions used in the surviving-prefix
count for the repeated-use obstruction.

Use actual A-only coercion to align A to the final B tree, then
common KEEP coercion to return both trees exactly to the original
common tree. The reaching prefix is empty. The construction counts
all its splays and has $A=\Theta_b(h)$ for fixed $b$.

### Reproduction

The [tracked W257 certificate](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_002/complete_00.json.gz)
can be verified from the repository root.

```powershell
python -B DO_RESEARCH_REBOOT/GSO_OMEGA_CYCLE_SEARCH_20261122_V001/gso_omega.py verify DO_RESEARCH_REBOOT/GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_002/complete_00.json.gz
```

The larger archived controls have workspace IDs
`CAP_FIVE_290_DELETE_4_CONTROL.json.gz`,
`GSO_OMEGA5_SPLIT_PIVOT_CONTROL_20261123.json.gz`,
`GSO_OMEGA5_ACTIVE_ANCESTRY_STRETCH_20261123.json.gz` and
`GSO_OMEGA5_PARALLEL_INTERVAL_LIFETIMES_20261123.json.gz`.
The [GSO record](https://app.notion.com/p/41f6251839be81d18fd6c910dcaa8a2d)
holds the original construction and replay provenance.

To reproduce the rectangle counts, replay both original trees and the
greatest clipped bank. Compute the two primitive cap thresholds on every
unpaid double and retain all original continuation IDs. Use a preceding
copy of the same period to seed each key's latest actual lower and upper
gain. Follow each retained loss to that gain, then select the last
genuine target in the prescribed range before the loss. Test that the
closed rectangle contains only its two request corners. Count each
original gain slot at its stated capacity and check
$2C=S+(C-E)+R$ before looking at the signed result.

## Exact sufficient packing statement

The existing bend calculation gives
$Z_{\mathrm{opp}}\le S_{\mathrm{all}}+18R_A$, where
$Z_{\mathrm{opp}}$ is the total opposite-side B double count and
$S_{\mathrm{all}}$ is the total same-side B double count. If $U$ is the
unpaid same-side count, then $S_{\mathrm{all}}\le U+45A$,
$U\le C_s+65A$, and

$$
\Omega_5\le U+Z_{\mathrm{opp}}\le 2U+81A\le 211A+2C_s.
$$

Thus a proof of the following assertion would close the fixed universal
goal. Find absolute constants $b\ge1$, $0\le\eta<1$, and $c,d\ge0$.
For arbitrary $W$ and arbitrarily large $r$, choose a separated
collection $\mathcal R_r$ of actual request rectangles with

$$
r(R_s-E_s)\le \eta\,r C_s+c\,r A+d|\mathcal R_r|+O_W(1).
$$

The last term permits a fixed seam adjustment for $W$ independent of
$r$. The term $d|\mathcal R_r|$ allows constant multiplicity.
After the signed cancellations, the packing must account for the
remaining net excess across different producing KEEPs. Same-KEEP
disjointness alone gives no bound on their combined load. A common
first hit may also force the same request corners for many nested
subtrees, as in the aligned construction.

The proved rectangle budget and division by $r$ would give

$$
(1-\eta)C_s\le(112b+c+2d)A,\qquad
\Omega_5\le
\left(211+\frac{2(112b+c+2d)}{1-\eta}\right)A.
$$

There is currently no source-uniform construction of the required
separated collection across overlapping producing KEEPs. The exact
open implication is this packing step after signed cancellation and
original funded use.
