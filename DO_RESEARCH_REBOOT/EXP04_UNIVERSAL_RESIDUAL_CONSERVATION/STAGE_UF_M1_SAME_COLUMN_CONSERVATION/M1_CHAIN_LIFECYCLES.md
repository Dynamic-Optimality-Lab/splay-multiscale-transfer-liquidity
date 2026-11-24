# Maximal C chains and their physical lifecycles

## Canonical chain partition

Retain the entire M0 forest, including zero-weight and already-paid vertices. Each vertex has at most one incoming edge and at most one C child. Delete P edges only for the purpose of listing maximal C paths; do not change any vertex's original type or predecessor. Every maximal path begins at an R or P vertex and follows successive global uses of one fixed g. The paths partition V as vertices. This does not make their physical components or A resources disjoint.

For a chain v_0,...,v_k, the union of its C intervals has no A demotion or B promotion of g. It traverses at most one cyclic column lap, since an all-C cyclic column would contradict strict frame descent. The post-head A component at g is a fixed complete physical tree throughout the chain's accesses. P branches may leave a vertex toward a different key's chain, without becoming additional copies of the old A component or credit.

## Target ordering

At every step F(v_{i+1}) is a physical key interval containing g inside J_g(v_i), which excludes x_i. Every later chain frame lies inside it. Therefore no later target equals x_i. If x_i>g, every later target on that side is strictly less than x_i; otherwise an interval containing g and that target would also contain x_i. If x_i<g the reflected inequality holds. Thus the chain targets are all distinct, with a strictly increasing left subsequence and strictly decreasing right subsequence. They may interleave sides. Reflections and middle-subtree transport do not alter this argument.

Distinct consecutive chain targets require some real A StepEv between their KEEP boundaries. This gives a per-chain bound by the actual A work in its full span. **It does not give a sum over chains:** the same A transition can lie in arbitrarily many spans, as the516-key C05 alternating-path family proves. We do not revive that refuted local-span capacity rule.

## Retired-target tickets

For each C child v of u, take the old-grandparent demotion bit of u: bit0 in LL/RR, bit1 in LR/RL. It destroys B ancestry (g(u),x_u). The key x_u is marked and is absent from the A subtree at g at that moment because A's root is x_u. Associate v with that original physical loss occurrence. If v consumes w(v) literal residual gaps, keep those distinct original gap IDs as at most three slots on this one ticket. They are still consumed at v, not at u; their original beta is never moved.

There is at most one such ticket per u because u has at most one C child. On the complete cyclic B word, the lost relation has a unique current ancestry lifetime: its last gain before the loss and the first ensuing loss of that pair. Complete closure guarantees an opener even across the seam. Pair labels alone are not IDs; opener and closer are actual primitive occurrences.

The opener is a B promotion of g, either as the accessed target or as a non-target old parent in bit0 of LL/RR. One opener can supply many different marked descendants and hence many different tickets. Unique forest edges do not give unit capacity to that opener. Ticket capacity is proved in M1_PHYSICAL_TRANSFER_INVARIANT, without a constant price per opener.

## Long-chain control and why it is not an unpaid counterexample

C05's full-return family, for k>=2 on n=2k+1, has first k KEEPs with targets n,n-2,...,3 and old grandparent1 in double1. For i=1,...,k,

\[
F_i=\{1,\ldots,2(k-i+1)+1\},\quad
J_i=\{1,\ldots,2(k-i)+1\},\quad D_A(1)=\{1\}.
\]

The first vertex is a chain head and the next k-1 vertices are C. Thus chain length is unbounded. The mismatch cardinality at key1 drops by two per critical double; its nonempty-column indicator stays1 until the last double. Exact legal reaching prefixes and measured complete restoration are part of the source, not omitted startup work.

Fresh k=4,16,64,256 instances realize3,15,63,255 C edges. The private-hanger lifts at physical populations259 and1027 retain the same marked chain while making the full A component at key2 have three real keys rather than one. Full-word repetition preserves closure and repeats histories; new original IDs are regenerated for each longer source. Their old periodic certificates remain active and every actual prescribed R_C is zero. None refutes a theorem restricted to positive original unpaid weights.

**First missing long-chain implication:** a globally bounded original-A payment for the *deep, original-Pi-qualified, hybrid-escaping* retired-target tickets, or a restoration transfer with independently bounded/usable ownership. Shrinking intervals, target distinctness, cyclic ancestry-lifetime existence and vertex-disjoint chains alone do not prove it.
