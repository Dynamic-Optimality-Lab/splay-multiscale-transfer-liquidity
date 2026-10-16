# S01_QUANTIFIER_SCOPE_THEOREM.md — lexical binders, no global stripping

## Claim
`normalize` is pure alpha-renaming: it preserves the truth value of every formula
under lexical (V-) semantics, and afterwards each bound name is owned by exactly one
binder (free occurrences keep original names and stay independently addressable).

## Proof
Per binder B (outermost-first): let S be B's body cone, R the nodes reachable from
the root avoiding B, C = {n in S : cone(n) mentions B-bound vars} ∩ R. Only C-nodes
are duplicated, and only B-bound var occurrences inside them take fresh names; B's
record REPLACEs exactly the renamed names. Uniformity: hash-consing gives one var
node per name, so per (B,name) either all interior occurrences are renamed or none
— never a mix, hence no weakening (no decoupled double-binding). Outside-S nodes
keep original child references except B's ancestors, which are relinked (skip-set
remapped through the pass id-map, so noBinder is processed twice and none is lost).
Nested-binder records inside S are renamed with the same fresh map exactly when
their body occurrences are — shadowing preserved (Q3 evidence: outer keeps `a`,
inner becomes `a#q1`, +5 nodes). Free occurrences outside all bodies are untouched.
Validation asserts pairwise-disjoint bound names and cone-containment (FAIL CLOSED).

## Evidence
Q1-Q8 all pass on the compiled backend with independent oracle agreement, incl. Q2
(free/bound collision, model `z=0`), Q3 (shadowing), Q4/Q5 (alternation), Q6
(MinPre exclusion on a hand-built two-weight graph with a binder-shared
subexpression), Q7 (vacuous), Q8 (alpha-equivalence verdict-stability).
