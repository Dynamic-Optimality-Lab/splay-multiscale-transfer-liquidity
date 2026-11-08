# AO35 — whole-period active-operand projection

Status: mathematical derivation; independent check pending. This is a
source representation theorem, not a repayment theorem.

## Box: exact source representation

**Target.** Represent a complete paired-closed original period with r marked
KEEP keys and k anonymous A operands by a native A tree on r+k anchors,
without changing any original operation, event or cost.

**Conditions.** Cut immediately after a genuine KEEP. Let M be all genuine
KEEP targets in the period. Let K contain every unmarked node that is an
A rotation operand or a positive-cost A target anywhere in that period.
Set S=M union K. Ordinary bottom-up splays; finite period; every M target
occurs. Tree nodes outside S are retained physically, not deleted.

**Inheritance.** Original source semantics, ordinary rotations, and the
accepted rigid external-gap lifting of CP35.

**Ambiguities.** This gives no bound on k in arbitrary sources. A certificate
at k=1 does not cover k=2 or larger. No new universal bound is assumed.

**Bridge.** The initial ancestor core of S contains only S. Thus all omitted
nodes occupy rigid external gaps, so exact ordinary splays reduce to the
native anchor action table and lift back operation by operation.

## Proof of the bridge

At the cut A's root is marked. Every original access target belongs to S:
a positive-cost unmarked target belongs to K; a zero-cost target is the
current root, which is either the marked initial root or an earlier
positive-cost target. Induction over original operations proves the claim.

Suppose a node v outside S initially lies above s in S. Until v participates
in a rotation its set of descendants does not change: rotations strictly
inside or outside its subtree do not change that set. Choose the first
source access at which s is either accessed or is a rotation operand.
Such an access exists by the definition of S. If v has not already been
an operand, it still lies above s and hence on that access's full search
path. Ordinary splaying of the target to the root consumes every nonroot
node on the original path as a target, parent or grandparent operand.
In particular v participates, contradicting v outside S. Therefore no
such v exists. All initial ancestors of S belong to S.

Every omitted subtree is consequently S-free. No subsequent search for
an S target enters it. Each rotation reattaches it intact at its ordered
external port. CP35 proves that all native operands, depths, StepEv
counts and destinations are exact. Arbitrary original repetitions and
zero-cost operations remain in the source word. Native closure with the
same external-port assignments implies full A closure, with no credit
from a prefix or another period. This proves the representation.

## Two different source views

When k=1, write the additional A anchor h. Its rank relative to M has
r+1 possible gaps, including the two exterior gaps. B's unmarked core
labels need not be active A operands. Conversely h need not be in B's
marked ancestor core. Separate A and B projections are legitimate because
only M is accessed in B; every other B node stays in its actual rigid
gap. A's h is accessed only by A-only operations in this source class.

For every actual source, its actual order and actual node aliases induce
one of these models. The projected costs depend only on the respective
ordered native shapes. This is a cost-preserving overrepresentation of
actual histories; it does not identify different physical node IDs or
authorize exchanging their donor units. Any negative model walk still
requires a single explicit common physical embedding and closure receipt
before becoming a source counterexample.

Reflection is the exact order-reversing bijection of all source keys,
tree pointers and access targets. It preserves depth, H, q, physical
occurrence identity and closure. Hence for seven marks the eight h gaps
reduce to four pairs g and 7-g, with no unoriented assertion by analogy.

## Exact natural-boundary compression

After a genuine KEEP the A and B roots are the same marked target. Between
two such boundaries B is fixed until the next genuine KEEP x. For fixed
native A endpoints s,t with root(t)=x, the least possible A event cost is
the shortest-path distance delta(s,t) in the full native A access graph.
Every legal macro has cost at least delta. Conversely, take a shortest
native access word from s to t. Its final access is x (or append x if
necessary), label that final access KEEP and all preceding accesses
DELETE. This is an actual natural macro with the specified B transition
and the same A cost. Genuine x differs from B's old root. Nongenuine
KEEPs of B's current root, if present in the original macro, have q=0
and the same A effect as DELETE; relabeling is used only for minimum-cost
realization, never to omit an original operation from a positive proof.

Therefore a state debt on synchronized boundaries satisfying
2 delta(s,t)-q+D(t,B')-D(s,B)>=0 proves the untruncated inequality for
EVERY actual intervening helper word. Identity operations add zero cost
without affecting the boundary. The natural graph may be evaluated by
an A-only shortest-path envelope; it need not store all operation-level
A/B pairs. This changes representation, not the source theorem.
