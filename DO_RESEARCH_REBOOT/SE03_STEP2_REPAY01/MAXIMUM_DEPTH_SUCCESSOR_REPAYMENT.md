# Maximum-depth accesses force a shallow successor

Status: universal source structural/packet repayment theorem, not complete
Step2. Dependencies: the separately audited closed-core subtree density
theorem, and the inherited maximal-core even-depth/outer-LL-or-RR theorem.
All claims concern actual full closed B histories; no new finite tests.

## Full-depth source paths have only same-side doubles

Let an actual closed core have r>=3 marked nodes and c=2r-1 total nodes.
Write its sorted labels as

    m1,u1,m2,u2,...,u_(r-1),mr,

as proved by closed-core density. Suppose a genuine target x has maximum
depth2r-2. Its path contains every core node, so S is a Hamiltonian BST
path and all its off-path hanging subtrees have no marked key.

A Hamiltonian BST path removes the minimum or maximum of the remaining
ordered label interval at each step. The root G is marked and its full
remaining interval has odd length and mass1. Its child interval has even
length and mass0. By the subtree-density theorem that child cannot be
marked: a marked-rooted subtree would need mass at least1. Therefore its
child P is the UNMARKED extreme on the same side from which G was removed.
Removing G,P leaves another odd interval with marked endpoints. Repeat.
Consequently every original source pair is LL or RR, with marked G and
unmarked P. This is stronger than the earlier local retention grammar;
it uses actual cyclic source density and cannot be inferred from the
old whole-core cardinality bound alone. Inner mixed doubles are excluded
here only in this full-depth, closed, maximal-core domain.

## The destination is a canonical two-sided fan

Let x=m_k. Starting from x and processing source pairs from inside out,
an RR pair changes its left rebuilt subtree L to

    u_j(m_j(mark-free gaps), L),

and leaves its right rebuilt subtree unchanged. An LL pair changes its
right rebuilt subtree R to

    u_j(R, m_(j+1)(mark-free gaps)),

and leaves its left rebuilt subtree unchanged. These are the exact original
bottom-up formulas with arbitrary ordered gap BSTs, not additional costs.
The left and right updates act independently. Thus their interleaving does
not affect the final core: it is rooted at m_k, with left spine

    u1 --right--> u2 --right--> ... --right--> u_(k-1),

each u_j having marked left child m_j, and right spine

    u_(r-1) --left--> ... --left--> u_k,

each u_j having marked right child m_(j+1). Empty sides are omitted. Every
original gap hanger remains individually unchanged in its inorder gap.

For i<k the exact path to m_i in this fan is

    L R^(i-1) L.

For i>k it is

    R L^(r-i) R.

If i=1 the first path is LL; if i=r the second path is RR. Every other
nonroot marked target has either odd depth or, at even depth, outer LR
or RL. The inherited maximal-closed-core theorem forbids each of those
alternatives for a genuine KEEP in the actual period. Therefore:

    After a maximum-depth genuine KEEP, the next genuine full KEEP
    targets one of the two extreme marks and has exactly q=1.      (1)

DELETEs and nongenuine KEEPs may intervene; they freeze B and are retained
in the actual successor macro's A cost. No future source operation is
selected by the proof. Equation(1) is forced for the given closed word.

## Independent signed repayment of disjoint packets

Let H be the full maximum-depth macro's actual A cost, and Hnext the cost
of its actual next genuine macro, both at least1. Their combined full
double demand is (r-1)+1=r and their actual capacity is2(H+Hnext). Thus
this two-macro packet is independently safe whenever

    H+Hnext>=ceil(r/2).                                  (2)

Both macro intervals and every physical A-event/bit identity are actual
source intervals. Allocate their r full-double demand IDs in ordinal order
to distinct actual capacity units in the packet. Condition(2) proves the
injection. Payment is by the packet end; no native causal matching-terminal
eligibility for its early demands is inferred.

For r>=3 the maximum charge r-1 is at least2, whereas its successor has
charge1. Therefore two maximum-depth macros are never adjacent, and their
two-macro packets are disjoint, including at the cyclic seam. The actual
period can be rotated to a packet boundary for this separate full-packet
allocation. It is not a claim that the already fixed auxiliary allocation
leaves these units unused. A later complete full allocation can be exchanged
against that auxiliary allocation using the proved conditional exchange
lemma, if all remaining full demands are independently funded.

## Six-key consequences and the remaining debt

For full core11, q5 is exactly maximum depth10. Every negative H2/q5 macro
is paid by its forced q1 successor, since H+Hnext>=3. An H1/q5 macro is
also paid if its successor has Hnext>=2. The only remaining q5 packet has

    H=Hnext=1, q=5, qnext=1,
    total weight 2+2-5-1=-2.                             (3)

Thus the possible q5 deficit3 cannot persist unaltered: its actual next
genuine access repays at least one unit. At H2 it repays the entire deficit.
This is an unconditional source theorem with actual disjoint packet capacity.

It does not prove that packets(3), H1/q4, and H1/q3 blocks compensate one
another, nor handle full core10 by the same geometry. Removing a packet
from the COST SUM is not deleting it from the original word: its B and A
endpoints need not agree. The remaining word is not thereby a smaller-support
closed source history. No induction hypothesis is applied to that punctured
word, and no new complete original CD domain is claimed.
