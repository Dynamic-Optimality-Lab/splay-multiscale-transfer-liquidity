# CW_CYCLIC_KEEP_SUPPORT_THEOREM.md — Gate B: K(W) = G(W) for exactly B-closed words

## Statement
Let W be a legal word with exact B-closure (B_T = B_0 as labeled trees) and |G(W)| = 5, where
G(W) = {x : KEEP(x) changes B} and K(W) = {x : KEEP(x) occurs}. Then K(W) = G(W).

## Proof (from splay semantics; DELETEs arbitrary, all word shapes)
Lemma 1 (root change): splaying a non-root key changes the root (target ends at root, distinct
node), hence changes the tree. Contrapositive: an access leaving B unchanged accessed the current
B-root. In particular every nongenuine KEEP (B-unchanged by definition of genuine) accesses the
current B-root. (Splaying the root is identity: empty frames, verified zero-op.)
Lemma 2 (root provenance): B changes only on genuine KEEPs (DELETE: B untouched per source;
nongenuine: unchanged by definition). After a genuine KEEP(x), x is B-root. Between changes the
root is fixed. Hence at every time t, root(B_t) = target of the most recent genuine KEEP, or the
initial root if none yet.
Lemma 3 (cyclic initial root): |G|>=1 so genuine KEEPs exist. root(B_T) = target of the last
genuine KEEP (subsequent ops change nothing) ∈ G(W). Exact closure B_T=B_0 gives root(B_0) =
root(B_T) ∈ G(W). Thus the "initial root" case of Lemma 2 is always a genuine target (read
cyclically): root(B_t) ∈ G(W) for ALL t.
Conclusion: every KEEP target is either genuine (∈ G by definition) or nongenuine-at-B-root
(∈ G by Lemmas 1-3). So K(W) ⊆ G(W); G(W) ⊆ K(W) immediate. Equal.

## Mandatory checks (all covered, none assumed)
DELETE placement (B-invisible to K/G) ✓; zero-cost KEEP (root identity, nongenuine on G-root) ✓;
consecutive repeats ✓; nongenuine KEEP (the crux, Lemmas 1+3) ✓; long words ✓; leading DELETE/
nongenuine (cyclic Lemma 3) ✓; nonprimitive (unused) ✓; cyclic boundary (B_T=B_0 exact, roots
equal) ✓; pre-first-genuine roots (cyclic) ✓; paired-vs-B closure (B-closure suffices; R1-T pair
closure implies it) ✓; genuine detection = exact tree change ✓ (matches G(W) definition).

## Finite-domain sanity (not the proof)
Bounded exhaustive: n=5,6 universes × sampled starts × KEEP-words ≤5: 5003 B-closed, 164 with
|G|=5, 164/164 K==G, 0 counterexamples (CW_DOMAIN_TESTS.json). DELETEs excluded soundly (B/G/K
invariant under DELETE interleaving: B-evolution depends only on the KEEP subsequence).

## Gate B: PASS (proved + 0/164 counterexamples). K(W)=G(W) authorized for Gate C.
