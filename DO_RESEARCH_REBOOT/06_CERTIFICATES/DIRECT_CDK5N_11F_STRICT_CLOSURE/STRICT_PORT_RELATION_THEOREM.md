# STRICT_PORT_RELATION_THEOREM.md — repaired low relation (built, verified)

## Form
`L_w(s,t) <=> Exists xi [SourceExact /\ InventoryValid(+compat) /\ LegalMacro /\ ExactReplay /\
DestinationMatch /\ ExactWeight]` over one shared xi (STRICT_LOW_COMPILER.build_slow, 1,400,081 nodes).
All conjuncts reference the same witness: prefix/inventory/word/paths/rotations/B-trace/states.

## Repairs vs predecessor (all verified, none merely specified)
- Same KEEP identity (A1): S-exact + fringe gap+fungibility; mismatches rejected.
- Root-terminated simple paths (A2): path[dd]==current root + no repeats, A and B; shortened/
  duplicated rejected.
- B tree validity (A4): one-parent/counting/depths/root/gap-presence at all event boundaries
  (intervals at static boundaries, structure-only mid-replay); duplicates/disconnected rejected.
- Compat (A7): necessary rank-overlap per allocated cell; incompatible moves rejected.
- No intermediate genuine (A8): macro segmentation discipline; unsplit 2-genuine rejected.
- Alpha-7 canonical shadows (A6): 7 positions + derived beta; matching on all grounded edges.
- Terminal genuine q + weight (A8/C2): constrained from B-depth; marked; B-change; 5 E3/E4 negatives.

## Evidence
108 grounded edges (0 mismatches) across 9-key bulk + S-multi + fringe phases; 8/8 adversarial
rejections; normalization 60/60. Skip census honest (high-seg/fringe-anc/nontree/gap-match/nongen).

## Scope
Low-cost (H<=2) arbitrary-fringe macros in the all-core-ancestor exactness class; fringe-ancestor-q
class conditional (OPEN lemma, counted skips). High-cost/operator/product layers not recompiled
(HARD STOP at SC10; predecessor artifacts stand for reference).
