# 26AF: Ext-R numerical ROW identity (PROVED)

**Status: PROVED** — direct finite source computation + banked Ext-R sibling-erasure.
No UG/SELF/DIAMETER/DTQ premises, no J witness, no fitted values.

## Fixed configuration

- `T_R = [-1,[-3,[-4],[-2]],∅]` (valid BST), root `p=-5`, `B_R(L) = [-5,L,T_R]`
  with L any finite valid BST with keys < −5 (∅ allowed).
- Pair `(u_R,v_R) = (-2,-4)`: depths 3,3; leaves (subsize 1,1); fold labels 1,1
  (measured via left-singleton probe; stable under left insertions by T-path fixity).

## Base identity (exact, machine-verified from source definitions)

On `B_R(∅)`: `R_static(−2) = R_static(−4) = −1`; subsize equal; row-charge
multisets `Jat(B_R(∅),−2) = Jat(B_R(∅),−4)` (mirror children of −3). Hence:

\[
\boxed{D_J(B_R(\varnothing);-2,-4) = 0 + 0^{\mathsf T}J = 0 \qquad\forall J.}
\]

So `c_R = 0`, `β_R = 0` with no premises beyond arithmetic.

## Infinite extension (banked Ext-R erasure)

Equal depth + equal fold ⇒ per-insertion fresh occurrences share identical keys
both sides (26AC mechanism; REBOOT-01 proves the mirror orientation explicitly).
Spot-checked: D-form stays `(c0=0, 0 terms)` for L ∈ {∅, singleton, vine, branched}.
By leaf-deletion induction:

\[
\boxed{D_J(B_R(L);-2,-4) = 0 \qquad \forall L,\ \forall J,}
\]

hence `|·| = 0 ≤ 2` on the whole right-child family with one (arbitrary) global J.

## Scope

Covers `T=T_R`, pair (−2,−4), all finite left-sibling BSTs. Distinct contexts from
26AE (negative keys, right child, left siblings — no ledger overlap; verified by
grep over all proved artifacts). Does NOT cover: other pairs/trees, T-growth,
cross-child/root-vs-child, global J existence.
