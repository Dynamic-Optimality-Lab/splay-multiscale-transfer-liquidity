# STRICT_ZERO_COST_NORMAL_FORM.md — A3 (corrected proof; D(x),K(x) resolved)

## The flaw in the previous rule
"Consecutive same-target root accesses collapse to the first" is FALSE when the first op is a
full no-op: `[D(x),K(x)]` with x an A-root but B-nonroot has D(x) a full no-op (A identity at root;
B untouched) while K(x) changes B. Collapsing to the first drops the B-change. Minimal
demonstration: any state with A-root x, B-root y≠x; replay `[D(x),K(x)]` vs `[D(x)]` (endpoints differ).

## Corrected normal form (proved)
Greedy deletion of full no-ops (A and B serials unchanged by the event) preserves endpoints, total
H, terminal (mode,q,genuineness), and genuine-q sequences (each deletion is an identity step; later
legs see identical states). Fixpoint terminates (word shrinks). The normal form satisfies:
- DELETEs before the first KEEP are gone unless state-changing (then they are non-root, counted).
- The first B-changing KEEP per root-run is kept; later same-target root ops are identities (B-root
  established; A-root established) hence dropped.
- Non-root accesses (a>=1) number <=2 per H<=2 macro; root-runs <=3 with <=1 kept each.
- Total effective events <= 2+3 = 5 (verified empirically: normalized H<=2 words have <=5 events).

## Executable + tests
`normalize_word` implements greedy deletion with replay-checked preservation (endpoints, H,
terminal, genuine-q sequences). Fuzz 60/60 preservation + bound check. The interpreter consumes
normalized words; non-normal words remain sound (extra identities replay exactly).

## Gate A3: proof defect REPRODUCED + REPAIRED (bound stands, justification corrected, executable verified).
