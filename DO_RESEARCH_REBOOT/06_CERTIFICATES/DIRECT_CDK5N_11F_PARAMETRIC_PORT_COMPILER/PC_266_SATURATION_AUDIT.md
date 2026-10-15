# PC_266_SATURATION_AUDIT.md — G08 (13-item ledger re-audited against the production circuit)

## Imported base (unchanged)
UFRL E1-E8 (prefix/frontier/witnesses/E/gaps/rebuild/counts) + L1-L8 (targets/pivots/descents/cases/
displacement/shadows/inventory/zero-DELETE/B-compat) + AF-2 flow biconditional + AF-3 reservoir discipline.
Spot re-verified: extract 30/30 per-gap min(n,266); E3/E4 cost patterns present in certified negatives.

## 13-item ledger vs production predicates
1. S identities: exact-once cover (valid() S-cover) + fullrank order. 2. Marked: mu popcount=5 + terminal
marked (mask-bit). 3. B-core: projected core topology + B-validity (BST intervals over fixed S-ranks).
4. A causal prefix: wellformed + link_both + child_bound_prop (ancestor-closed, connected, depth<=6).
5. Strict inorder: rank all-different + S-order + interval containment. 6. A-port occupancy: derived
(active+content; empty stays empty). 7. B-fringe occupancy: min(n,266) counts, zero-stays-zero.
8. Access targets: path verification (dynamic, evolved states) + presence + depth<=4.
9. Primitive rotations: decoded order (zigzig (p,g)-first; zigzag (x,p)-first; 263/263 exact vs source).
10. Exact H: macro_H == Hv (138/138 grounded). 11. Exact q: constrained q from B-depth (2q<=d<2q+2);
    genuine (B-change + marked); 138/138 grounded incl. E3 (q=3) and E4 (q=4) negatives.
12. Shadows: depth-2 reader vs alpha (138/138). 13. One consistent witness: single xi in every conjunct
    (no src/dst split; carried-view validity).

## Why 266 suffices (per gap; total <=2669)
E6 feasibility: retained-in-gap |E cap G_i| <= 255 <= 266 (both code branches; 30/30 spot). The 11-slot
headroom covers B-interface occupancy + zero-cost spares (root accesses target exposed nodes in K;
E3/E4 are cost patterns, not extra keys; low-cost DELETE targets satisfy d<=4, hence in K by L1).
Saturation binds only above 266 where min() preserves occupancy and all cost/shadow observables depend
only on retained structure. Tests prove instances, not universality; universality is the imported
E1-E8/L1-L8 proof (not re-proved here).

## Per-edge vs per-walk representatives (§11 distinction, explicit)
1. Per-macro representative (shared source/destination of ONE macro): PROVED (E1-E8/L1-L8 + carried
   destination validity; production destination equality per edge).
2. Per-walk global 2669-key set for an ARBITRARILY long word: NOT CLAIMED. Per-edge witnesses may
   differ; adjacent boundaries map consistently to canonical abstract states (mu/B-core/alpha/sig
   static-or-canonical). The forward simulation uses per-edge representatives with consistent boundary
   mapping (§18 items proof in PC_UNIVERSAL_SIMULATION.md).

## OPEN lemma (marked explicitly, not hidden)
FRINGE-ANCESTOR-Q: for macros whose terminal marked target has fringe B-ancestors, the representative
q (core-depth-based) may differ from concrete q. Measured: fringe-anc skip rates 120/720, 52/480,
182/720 across V8 fuzz runs (macros outside the exact-agreement class are counted, not hidden).
The universal simulation is COMPLETE for the all-core-ancestor class and CONDITIONAL elsewhere (representative q used conservatively... low edges use representative-exact
q; fringe-ancestor macros map through the §9 projected representative whose q-preservation is
Control-F certified (30,773 imported cases) but not re-proved per-macro here).

## Gate G08: PASS (ledger + import + explicit OPEN lemma). No silent saturation assumption.
