# GSO complete-period accounting for Omega5

**2026-11-23. Universal Relaxed Coarse-Double remains open.**

The original domain is all admissible exactly paired-closed sources. The frozen
H=5 policy counts each original B double as either paid or unpaid at its
greatest clipped cyclic balance. Its established accounting is

$$
Q_B(W)=P_5(W)+\Omega_5(W),\qquad P_5(W)\le 45A(W).
$$

Here $A$ counts original A steps, including the work of preparation and
restoration. An absolute finite bound $\Omega_5(W)\le K A(W)$ would give
$Q_B(W)\le (45+K)A(W)$. The complete-period calculations below record where
this attempt to establish $K$ stops. [Frozen policy and witness format](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/README.md).

## Signed ancestry-depth accounting

Write $I_T(v)$ for the full physical subtree interval at key $v$ in tree
$T$, and $J(T)$ for the set of these intervals. For a key interval $I$,
set

$$
\ell_B(I)=\bigl|\{v\in I:I_B(v)\not\subseteq I\}\bigr|.
$$

The ancestry-depth measure is

$$
F(A,B)=\sum_v\left(\operatorname{depth}_A(v)-
          \min_{u\in I_B(v)}\operatorname{depth}_A(u)\right)
      =\sum_{I\in J(A)}\ell_B(I).
$$

The first depth sum counts proper A ancestors of all vertices. The second
counts proper A ancestors of the unique shallowest A key of each B interval.
That key is the lowest common ancestor of the interval's two endpoints and
is an ancestor of all its keys. In the interval expression, both counts also
include the vertex itself, giving one extra count per vertex in each sum.

During B's phase of a KEEP, the target $x$ is already the A root. Each
physical B rotation replaces one proper B interval containing $x$ with a
new interval excluding $x$. For every proper A interval, the straddler count
decreases by one if it contains the new interval and stays equal otherwise.
The full interval is constant. Thus $F$ is nonincreasing on all B rotations.
Exact closure of both trees gives

$$
\sum_{\text{A rotations}}\Delta F
=-\sum_{\text{B rotations}}\Delta F.
$$

For the archived $H_{3,q}$ history with $q\ge 1$, put $N=16(q+1)+1=2m+1$. Start
from a common right vine with empty reaching prefix. Execute DELETEs from
$2$ through $N$, then a descending sweep from $N$ through $1$ that
keeps $N,N-1,N-3,N-7$ and marks the other accesses DELETE. Follow
this by the full increasing KEEP sweep and then the decreasing KEEP sweep
from $N-1$ through $1$. Here DELETE is A-only splay and retains the
physical key. A maintains a descending vine on keys smaller than its root
and an ascending vine on larger keys. Each adjacent move costs one A unit,
so $A=4(N-1)=8m$. The restoring
increasing scan puts every already processed smaller key on the left vine
of the current root. Each next key is the successor, so its final one or
two rotations place the previous root directly on that vine. The mirrored
decreasing scan restores the common right vine. [Original source constructor](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/sources.py).

At the first KEEP of $N$, A is the left vine and B is the right vine.
The $j$-th RR double, $1\le j\le m$, has old grandparent $g=N-2j$.
The two replaced proper B intervals contain $N$. Their replacements are
$\{g\}$ and $[g,N-1]$, whose minimum A depths are $2j$ and $1$.
The signed A sum therefore obeys

$$
\frac{\sum_{\text{A rotations}}\Delta F}{A(W)}
\ \ge\ \frac{\sum_{j=1}^{m}(2j+1)}{8m}
\ =\ \frac{m+2}{8}.
$$

The first burst is fully funded. The ascending DELETE sweep refills every
block. The lowest rank in the successive RR footprints is
$\max(1,N-2j-1)$. Each group of steps with the same lowest block has
length at most three. The first step of such a group encounters a full
block, and target-first pooling leaves at least four credits in the target
bank after payment. These credits cover the later steps in that group.
The resulting unbounded **signed recharge of $F$** is overcharging of a
potential on paid work. The aggregate unpaid-cost inequality remains open.

## Preorder and capped interval accounting

For the previous preorder potential $T(A,B)$, evaluate the B-double cost
of splaying A's root-first preorder from B. Every whole B phase subtracts
exactly its double count because its target is the first key of that
preorder. Thus the signed A-phase sum on a closed period is $Q_B$, and
subtracting $P_5$ from it gives exactly $\Omega_5$.

Capping each physical interval's straddler count at an integer $c\ge1$
gives

$$
\Psi_c=\sum_{I\in J(A)}\min(c,\ell_B(I)).
$$

A real A rotation replaces a single interval in $J(A)$, so its increase
in $\Psi_c$ is at most $c$. B rotations are nonincreasing. The total
recorded B decrease therefore satisfies
$D_c(W)\le cR_A(W)\le2cA(W)$, where $R_A$ is the number of actual A
rotations. This counts A work once across the complete period.

Conversion of this decrease to a bound on unpaid occurrences is the missing
step. On the verified 257-key period with $A=989$, $Q_B=519$ and
$\Omega_5=2$, the unpaid event $B(99,14)$ creates $[135,138]$ and
$[135,225]$. Any proper A interval containing either new interval also
contains key $134$, which remains a B ancestor of the target $226$.
That surviving straddler keeps every such interval at the cap of one.
The decrease in $\Psi_1$ is zero. The cap of two registers the drop from
two to one in the A interval $[134,138]$ at key $137$.
[Complete original period](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_003/complete_00.json.gz)
and [independent replay](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/run_003/INDEPENDENT_VERIFICATION.json).

A bound on the total amount of unpaid work hidden above a fixed cap is still
missing under arbitrary interleavings and recreated ancestry. The
$\Omega_5$ acceptance condition and the Universal Relaxed Coarse-Double
conclusion remain open. [Prior root acceptance record](GSO_OMEGA_CYCLE_SEARCH_20261122_V001/ROOT_ACCEPTANCE.json).
