# CC_A_BOUNDARY_SHADOW.md — finite canonical A boundary-shadow (STEP 07)

## Definition

At post-KEEP boundaries (A/B roots synced at marked u), α(A) records:
1. Rooted A shape through depth D=2 (7 slots; each: empty-hole,
   opaque-hole, or visible node).
2. Visible-node identities: S-keys by exact label; non-S by canonical
   ordered anonymous symbols (β_1<β_2<… left-to-right; same symbol never
   twice; S labels unique; all nine S keys exist somewhere, visible or
   constrained-hidden).
3. For each opaque hole: the subset of nonvisible S keys it must contain
   + BST interval constraint (low, high) from surrounding visible keys.
4. Empty vs opaque distinction per slot.
5. Common marked root u (= B root; enforced in products).
6. Static fringe inventory: per each of the ten S rank-gaps, count of
   non-S keys saturated at N(h) with terminal class "≥N(h)+1", where
   N(h)=2^(R(h)+1)−1 (h=2: R=6, N=127; h=4: R=10, N=2047).

## Finiteness

Depth-2 slots finite; visible labels from finite symbol set (9 S + bounded
anonymous: at most 7 visible ⇒ ≤7 anonymous); hole S-subsets ⊆ 2^9;
interval constraints from visible-key order; inventories (N(h)+2)^10.
Total finite per h (exact count computed at build; caps §17 enforced).

## Soundness role

Shadows OVERAPPROXIMATE: a concrete boundary maps to exactly one canonical
shadow (canonicalization); a shadow denotes all consistent concretions.
Transitions may overapproximate (extra symbolic edges) but never omit a
legitimate original transition (coverage proof via cone lemma: every
H≤h interval's effective word + R(h)-completion appears among enumerated
macros — STEP 09 obligation).
