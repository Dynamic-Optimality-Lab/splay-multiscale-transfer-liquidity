# SOURCE_DOMAIN_AUDIT.md — present-key DO domain (§2, 20 questions)

Scope: domain audit ONLY (which requests the source theorems quantify over).
NOT the MSTL-19 bridge consumption (exact L2 bytes still frozen-absent;
MSTL-19 stays BLOCKED_BY_SOURCE). Sources inspected:

- L3: Levy & Tarjan, "A Foundation for Proving Splay is Dynamically Optimal",
  arXiv:1907.06310v3 (LOCAL BYTES: v03/history/external/papers/
  L3_levy_tarjan_foundation_1907.06310.pdf, 732837 bytes,
  sha256 f7aa79010984db5104c81846d7d0862bb4b83c1f13cbc84c922757e340c36f1c,
  matches repo SHA256SUMS). AUTHORITATIVE ACCESSIBLE SOURCE for domain.
- L2: Levy & Tarjan, SODA 2019 (SIAM paywall; Princeton OAR bot-blocked):
  NOT inspected byte-wise. L3 is its direct arXiv successor covering the same
  framework (approximate monotonicity ⟺ DO, simulation embedding); any L2-only
  deviation is recorded as residual risk, not as premise.
- L1: Sleator & Tarjan 1985: paywall per repo manifest (PENDING). NOT
  inspected; L3 re-derives needed premises with explicit ST85 citations.
- Parent specs (v0.3 + DECIDE-v0.4 reference): program-side bridge checkpoints
  (Q41 subsequence match, occurrence semantics, fixed key sets).

## Answers (L3 section references are to the v3 PDF text)

1. Key universe: finite node sets; transition digraph Gn(A) vertices are
   "every binary search tree with keys {1,...,n}". Fixed finite universe.
2. T contains all requests: "An instance ... comprises a sequence
   X = (x1,...,xm) of requested keys and an initial tree T containing
   these keys."
3. Every request is a stored-element access: "If ri = search then xi must be
   in Ti-1" (mutating model); digraph arcs exist "for every T and x in T".
4. Unsuccessful searches: NOT in the quantified request domain (0 hits for
   unsuccessful/absent; "missing" hits are null child pointers and mutation
   neighborhoods only).
5. X = (x1,...,xm), requested keys, time-indexed.
6. Y ⪯ X by choosing "a subset A of {1,...,m} and keeping the requests in X
   at times in A". Non-contiguous allowed; X ⪯ X.
7. Occurrence-level: YES (time-indexed; duplicates handled: same key at two
   times are distinct occurrences by construction).
8. Splay(X,T), Splay(Y,T): same initial tree T ("for every request sequence
   X, subsequence Y, and initial tree T").
9. Yes (same T in costA(Y,T) vs costA(X,T)).
10. Cost = access-path nodes (+1 rotation each); depth+1 compatible.
11. Additive: A(n)=0 target; L3 treats eventual-optimality/startup overhead as
    a SEPARATE notion (Sleator-Tarjan allow none) — no additive term in the
    AM⟺DO core (Thms 3.1/3.2/3.5).
12. Constants b,c independent of n (suprema f(n),h(n) compared up to
    n-independent factors, Thm 3.3).
13. AM: costA(Y,T) ≤ b·costA(X,T) ∀X,Y,T.
14. Thm 3.2/3.5: coercible AM ⟺ DO (both directions).
15. Successful-access only: YES for the search model. Insert/delete exist ONLY
    as separate §5 mutating-instance request types, not in X/Y search
    sequences.
16. No extra ops in X/Y: insert/delete are distinct request kinds
    (ri ∈ {search,insert,delete}) outside search-only sequences.
17. Fixed key set: YES ("transform this rooted hull into a tree on the same
    set of keys"; rotations preserve K; digraph fixed {1..n}).
18. BST-node insert/delete: NO in search model (only §5 mutating instances).
19. "Deletion": node removal ONLY in mutating instances; in AM context
    "removing searches from the sequence" = request/occurrence deletion.
    Pair Access DELETE matches the latter, never node removal.
20. Absent reintroduction: NONE FOUND. Insert requests (xi ∉ Ti-1) are a
    different request type, not searches; PA has no insert mode.

## Verdict

PRESENT_DOMAIN_BRIDGE_PASS — scoped: "domain audit established from
authoritative accessible source (L3 bytes above)". This is NOT "exact MSTL-19
bridge source frozen and consumed" (L2 still absent; MSTL-19 stays blocked).
Residual risks: L2-only domain deviation (none indicated; L3 supersedes L2
framework); L1 premise drift (L3 cites ST85 explicitly for used bounds).
