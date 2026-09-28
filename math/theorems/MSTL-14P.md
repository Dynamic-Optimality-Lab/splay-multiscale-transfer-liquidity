# MSTL-14P (v0.4.1-present route; new ID, broad MSTL-14 untouched)

Domain: PresentLegalPairInstance — LegalPairInstance(T0,H) with every access
occurrence (mode_i,x_i) in H satisfying x_i in keys(T0). By
FIXED_KEY_PAIR_ACCESS_CLOSURE every requested key is present in both A and B
when its occurrence executes; no absent/falloff semantics occur.

Statement: synchronous KEEP repayment on the present domain:
ACTIVE_pre_discharge >= need at every legal present KEEP, with
need = max(y - 2a, 0), a = d_A(x)+1, y = d_B(x)+1, i.e.
need = max(d_B(x) - 2*d_A(x) - 1, 0).

Negation: exists legal present KEEP with paid<need (12-point present
witness certificate; absent accesses excluded).

First consumer: MSTL-15P. Required status before consumption: REVIEWED.
