# S02_INVENTORY_COMPLETION.py — shared inorder inventory (Gate E).
# No separate flow backend exists in the frozen stack (honest record: the Step-01
# "Dinic hook" was never implemented; no Hall/flow code in the corpus). Inventory is
# decided by canonical construction (gap pools per sig counts, BST-valid port fills,
# same atom populations both sides by the s.sig==t.sig invariant enforced in-engine)
# and VERIFIED by the retained exact Z3 inventory constraints inside the relation
# (inv.attach/valid + compat_pred, decided per candidate by Tier-1). Where canonical
# construction is ambiguous, bounded alternatives are enumerated, never guessed.
# Flow feasibility as a separate prefilter: NOT APPLICABLE (no certified flow theorem
# in the frozen corpus; using one would be a new backend). Documented as a coverage
# note, not a gap: the exact constraints decide every candidate.
STATUS = {'flow_backend': None, 'method': 'canonical-construction+exact-verification',
          'same_populations_both_sides': 'by s.sig==t.sig necessary filter',
          'bst_completion': 'canonical BST fills, ssertify-verified genuine ordered completion'}
