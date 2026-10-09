# Start here

The goal is a universal constant-factor bound for ordinary bottom-up splay against offline optimal BST execution, with the same specified initial tree. The recovered source permits an intermediate startup term depending only on that tree; Levy–Tarjan's eventual-monotonicity theorem removes it in the final dynamic-optimality conclusion.

The original candidate architecture is:

```text
Pair Access (occurrence KEEP/DELETE encoding)
    -> COARSE-DOUBLE Q_B<=2A  [OPEN]
    +  C.ZIG Z_B<=A          [universal mathematical proof; formal assembly open]
    -> B=Q_B+Z_B<=3A         [CONDITIONAL]
    -> PIVOT-2 cycle excision
    -> E_B<=3S_A+g(T0)       [CONDITIONAL]
    -> LT(Y)<=7LT(X)+2g(T0)  [CONDITIONAL]
    -> Levy–Tarjan Theorem 4.3
    -> Dynamic Optimality   [OPEN]
```

Here A,B are StepEv totals on a closed pair walk, not the names of the two trees. E_B,S_A are the corresponding prefix totals. Local depth counts edges, e(d)=ceil(d/2), and LT cost is d+1. DELETE removes an occurrence from the B execution, not a key from a tree. The full definitions and quantifiers are in [ORIGINAL_PIPELINE.md](ORIGINAL_PIPELINE.md).

The J4 route is sufficient, not known necessary: one globally shared assignment must satisfy J-SELF and the adjusted ROW-DIAMETER constraints on all finite BSTs. Finite fitted assignments do not provide that witness. The universal row theorem and COARSE-DOUBLE remain open.

This run proved [equal-signature sibling erasure](02_PROVED/REBOOT_01_SIBLING_ERASURE.md): for same-child u,v at equal ambient depth with equal top fringe coefficient, arbitrary S can be erased without changing H_u-H_v, for every shared J assignment. All odd-depth equal-depth pairs qualify. Both orientations hold. This removes a real independent sibling variable; it does not prove the remaining empty-sibling width <=2. No UG or potential-existence assumption was added.

Exact finite checks also recovered the 970x79 coupling block's rational rank 48/nullity 31 and the LRF template contradiction 9/34. Neither is an all-depth result. Some later 26S–26AB reports described in the supplied directive are absent from this checkout; their summaries are retained with explicit evidence gaps rather than promoted to proofs.

Read [CURRENT_STATE.md](CURRENT_STATE.md), [CLAIM_LEDGER.md](CLAIM_LEDGER.md), and [NEXT_ACTION.md](NEXT_ACTION.md) next. The first pivot is complete; no successor currently passes the four-rule gate. Fresh research must identify a concrete, strictly smaller proof with a real original obligation deleted. Rephrasing global J existence as all-horizon feasibility is prohibited.

The checkout is dirty: branch wp5x-k6c2-specialized, HEAD 88f344d34b155f6cdc0fc4dae9bf0490d0677e1f. Source hashes bind the actual working bytes. Only DO_RESEARCH_REBOOT/ was writable; [the safety audit](11_REPRODUCIBILITY/SAFETY_AND_REPRODUCIBILITY.md) describes the complete digest comparison.
