# pair_access_domain_mapping.md — occurrence-level KEEP/DELETE mask (§3)

Source side (L3): X = (x_1,...,x_m), Y ⪯ X by time-index subset
A ⊆ {1,...,m} (duplicates are distinct times). Same initial tree T.

## Mask construction (occurrence-level, NOT value-set)

For each occurrence index i ∈ {1..m}:

    mode_i = KEEP   iff i ∈ A   (occurrence i retained in the Y-embedding)
    mode_i = DELETE otherwise.

H = ((mode_1,x_1),...,(mode_m,x_m)).

FORBIDDEN alternative: x_i ∈ set(Y) (wrong under duplicates: two occurrences
of the same key with different membership would collapse).

## Pair Access dynamics (frozen)

    A_0 = T, B_0 = T.
    KEEP i:   A_i = S_{x_i}(A_{i-1}),  B_i = S_{x_i}(B_{i-1}).
    DELETE i: A_i = S_{x_i}(A_{i-1}),  B_i = B_{i-1}.

where S_x = ordinary bottom-up splay (present key).

## Correspondence claims (proved in FIXED_KEY lemmas + replay)

C1 (A-side): A_i equals ordinary Splay state after X[1..i] from T.
    Proof: A splays every occurrence in order (both modes). By induction on i
    with the frozen replay equations (WP-1 LEGACY_SEMANTICS_CERTIFIED).

C2 (B-side): B_i equals ordinary Splay state after the retained Y-prefix
    (occurrences {j ≤ i : j ∈ A} in order) from T.
    Proof: B splays exactly the KEEP occurrences in order; DELETEs are B-no-ops.

C3 (closure): keys(A_i) = keys(B_i) = K for all i, where K = keys(T),
    given x_i ∈ K for all i (source domain). Hence every requested x_i is
    present in both trees when occurrence i executes (FIXED_KEY_PAIR_ACCESS_CLOSURE).

C1+C2 say Pair Access really represents Splay(X,T) vs Splay(Y,T). C3 excludes
the absent-key failure family on this route. All three are proved (C1 by
existing replay certification; C2 by construction + replay audit;
C3 in tests/test_present_domain.py over hostile present-only histories plus
the rotation keyset-preservation proof below).
