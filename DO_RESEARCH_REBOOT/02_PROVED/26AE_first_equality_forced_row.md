# 26AE: First equality-forced ROW family (PROVED)

**Status: PROVED** — exact rational linear algebra + source-defined identities + banked sibling-erasure. No LP witness, no fitted values, no new premises.

## Fixed configuration

- `T_* = [1,None,[3,[2],[4]]]` (valid BST, |T_*|=4), root `p=5`, `B_S = [5,T_*,S]`.
- Pair `(u,v) = (2,4)`: depths 3,3 in every `B_S` (T-side fixed); fold labels equal (measured `f^u=f^v` via S-probe; stable under sibling insertion by T-path fixity).
- `S` any finite valid sibling BST with keys > 5 (∅ allowed: `B_0=[5,T_*,None]` valid).

## Base identity (exact)

On `B_0` (machine-verified from `wp6_staticR`/`wp6_lambda`/`wp6_j4shared` definitions):

- `R_static(B_0,4) − R_static(B_0,2) = 0`, `subsize(4)−subsize(2) = 1−1 = 0`.
- `Jat(B_0,2)` and `Jat(B_0,4)` coincide as multisets (mirror children of node 3).

Hence as a linear form in J:

\[
\boxed{D_0(J) = 0 + 0^{\mathsf T}J = 0 \qquad\forall J.}
\]

In the §7 mechanism: `β_P = 0 ∈ rowspan(E_P)` with multipliers `α_P = 0`, so `C_P = c_P = 0`, and `|0| ≤ 2`.

## Infinite extension (banked 26AC mechanism)

Equal depth + equal fold ⇒ per-insertion fresh occurrences have identical keys both sides (verified form `(F_{d−1},λ,δ,d)`, λ equal), so `Ξ_e(J) = 0` ∀J; key-set freezing holds (26AB, 15/15 positions). Spot-checked here: D-form stays `(c0=0, 0 terms)` for ∅/singleton/vine/branched S. By leaf-deletion induction (REBOOT-01):

\[
\boxed{D_J([5,T_*,S];2,4) = 0 \qquad \forall S,\ \forall J.}
\]

In particular `|D_J| = 0 ≤ 2` for every sibling BST, with the SAME (in fact arbitrary) J. No UG equation, normalization, SELF, DIAMETER, DTQ, or witness is used.

## Scope (exact)

Covers `T=T_*`, pair (2,4), all finite S. Does NOT cover: other pairs/Trees, T-growth, cross-child/root-vs-child, global J existence. Nonvacuous: T_* valid, 2≠4 same child, depths/folds agree, ∅ valid, arbitrary S exist (vines).
