-- WP-6 STEPS C127 (Hall program): matching-theory cores for the Mode-A assembly
-- (hall_lemmas.md 8Q / 8AC-ZONE) + positional edge interface seed (8AC-TO Layer-B
-- pin). Q-sizes only for counting cores; set reasoning is Layer-A prose.
-- Positional part: time-indexed edge interface with the arrow as hypothesis
-- (Layer A proves it from build_tagged construction, C125; finite face: 51,292
-- placements loader-newer-or-same, wcharge.json). The multi-session build
-- (tree-state evolution, co-location dynamics) instantiates this interface.
-- Forbidden: sorry, admit, axioms. Kernel-check via direct `lean` exit 0.

-- WP-6 STEP 8Q-CORE: conditional mindeg-safety counting (hall_lemmas.md 8Q).
-- Q with min-degree source a* of degree d <= 3; R its Q-neighborhood (|R| = d);
-- Q' = Q \ R strictly smaller with Hall (q' <= 3n'); N(Q') ⊆ N(Q) \ {a*}
-- (so n' + 1 <= n). Then Hall(Q): q <= 3n.
-- Proof: q = q' + d <= 3n' + d <= 3(n-1) + d = 3n - (3-d) <= 3n.
theorem mindeg_safe (q n q' n' d : Nat)
    (hIH : q' ≤ 3 * n') (hQ : q = q' + d) (hN : n' + 1 ≤ n) (hd : d ≤ 3) :
    q ≤ 3 * n := by
  omega

-- 8Q-corollary: min-degree exactly 3 removal is tight-or-safe.
-- With the same hypotheses and d = 3: q <= 3n still (boundary: 3-d = 0).
theorem mindeg_three (q n q' n' : Nat)
    (hIH : q' ≤ 3 * n') (hQ : q = q' + 3) (hN : n' + 1 ≤ n) :
    q ≤ 3 * n := by
  omega

-- WP-6 STEP ZONE-ASSEMBLY: 8AC-ZONE + strong induction step (hall_lemmas.md
-- 8AC-Z, Mode-A assembly). Q splits at latest access L: q = q0 + qL,
-- n = n0 + u (disjoint new sources); IH closes the strict past (q0 <= 3n0);
-- 8AC-ZONE closes the latest block (qL <= 3u). Then Hall(Q).
theorem zone_step (q n q0 n0 qL u : Nat)
    (hQ : q = q0 + qL) (hN : n = n0 + u)
    (hIH : q0 ≤ 3 * n0) (hZ : qL ≤ 3 * u) :
    q ≤ 3 * n := by
  omega

-- Zone membership arithmetic: a minimal violator (Delta = 1, mindeg >= 4)
-- lies in the violator zone (the exact 8AC-ZONE target shape).
-- Given q = 3n + 1: the zone obligation at (q, n) is q <= 3n (open);
-- this records the target equation (used by falsifiers: q >= 3n+1 = kill).
theorem zone_target (q n : Nat) (h : q = 3 * n + 1) : 3 * n < q := by
  omega

-- Positional edge interface seed (8AC-TO Layer-B pin).
-- An edge is time-indexed by (site access, bev access, channel tag).
-- Channels: 0 = E1 (same-access), 1 = E2, 2 = K (E3 rotated-old),
-- 3 = W (E3 grazed), 4 = E4 (setup), 5 = E7 (pump-chain).
structure TEdge where
  siteAcc : Nat
  bevAcc : Nat
  chan : Nat

-- The arrow: no edge points forward in time (Layer A: build_tagged index
-- bounds, C125; E1 same, E2/E4/K/W/E7 older-or-same).
def arrowOk (e : TEdge) : Prop := e.siteAcc ≤ e.bevAcc

-- E1 edges are same-access (Layer A: accA[idx] only).
def isE1 (e : TEdge) : Prop := e.chan = 0 ∧ e.siteAcc = e.bevAcc

-- Old-channel edges point strictly backward (Layer A: setup/E2-window/E7-chain
-- bounds give ai < idx; K-def adds acc_of < acc).
def isOld (e : TEdge) : Prop := e.siteAcc < e.bevAcc

-- PRISTINE interface theorem: under the arrow, every edge incident to a site
-- plotted at access t comes from a bev at access >= t. Hence past bevs
-- (acc < t) carry zero load on sites_t: own-E1 opens pristine (8AC-PRISTINE).
theorem pristine_of_arrow (e : TEdge) (t : Nat)
    (hArr : arrowOk e) (hSite : e.siteAcc = t) : t ≤ e.bevAcc := by
  unfold arrowOk at hArr
  omega

-- E1 edges satisfy the arrow (same-access).
theorem e1_arrow (e : TEdge) (h : isE1 e) : arrowOk e := by
  unfold isE1 arrowOk at *
  omega

-- Old edges satisfy the arrow (strictly backward).
theorem old_arrow (e : TEdge) (h : isOld e) : arrowOk e := by
  unfold isOld arrowOk at *
  omega

-- Arrow dichotomy at a site: an arrow-ok edge with site t is E1-position
-- (same, t = bevAcc) or old (bevAcc strictly later). Pins the two-case
-- structure of the 8AC-IND step (pristine-E1 vs backward spill).
theorem arrow_cases (e : TEdge) (t : Nat)
    (hArr : arrowOk e) (hSite : e.siteAcc = t) :
    e.bevAcc = t ∨ t < e.bevAcc := by
  unfold arrowOk at hArr
  omega
