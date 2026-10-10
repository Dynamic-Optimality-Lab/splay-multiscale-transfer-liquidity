# Phase 2: five-key core geometry (PROVED from banked K4-L1)

K4-L1 holds for arbitrary marked sets (its proof quantifies over M; the
rotation tables and pivot-subtree argument use only marked/unmarked status).
Pruning commutation holds for every marked access likewise.

## Nine-node upper bound (PROVED)

Fix M (|M|=5). Linearize one full B-closed period right after a KEEP of k1;
V_1={k1}, C_1={k1} (size 1; root in every nonempty core). New keys add ≤2 each
(K4-L1 unmarked case w.r.t. current V; after the splay the new root lies in
the old core, so C_{k+1}=C_k as sets). Revisits (marked case, nonincreasing)
and DELETEs (frozen) never grow. Hence sizes ≤ 1,3,5,7,9 across first
appearances; end = start by exact B closure gives core_M ≤9 there. Rotating
the argument (every KEEP occurrence is a valid period start; DELETE states
share B with their preceding KEEP) yields |Core_M| ≤9 at every cyclic state.
The four-key proof is the k≤4 prefix of the same induction — generality
verified, not assumed. Nine is tight: the Phase-5 witness attains 9 at every
state (replayed above), so the bound cannot be improved in general.

## Closed-core size conservation (PROVED)

With complete M fixed, every KEEP is marked ⇒ core nonincreasing per KEEP
(banked lemma); DELETEs freeze B ⇒ core unchanged. Sizes along the linearized
closed cycle form a nonincreasing cyclic sequence ⇒ constant. Every
intermediate core has the same size (5–9 for five marks; the ≤8 subclass
restricts to 5–8).

## Labeled key-set constancy (REFUTED as a universal claim — handled)

The SET of core keys need not stay constant: a marked splay can drop an
unmarked Steiner node from all root-to-mark paths while pulling another
unmarked node in (size preserved, labels swapped). Example mechanism: splaying
marked x restructures a path so that an off-path unmarked sibling subtree is
no longer ancestral to any mark, while a previously buried unmarked node
becomes a path node. Therefore the finite graph MUST NOT assume fixed key
labels: enumeration covers all shapes × all marked 5-subsets × all marked
accesses, and transitions are verified for every compressed landing state
(shape', subset') including size-changing ones (harmless over-approximation).
No fixed-key assumption is used; coordinate compression (order-preserving rank
map) is canonical per state and preserves BST comparisons, hence splay
behavior, depths, weights, and potentials. Telescoping evaluates η on actual
projected states, so label swaps are accounted.
