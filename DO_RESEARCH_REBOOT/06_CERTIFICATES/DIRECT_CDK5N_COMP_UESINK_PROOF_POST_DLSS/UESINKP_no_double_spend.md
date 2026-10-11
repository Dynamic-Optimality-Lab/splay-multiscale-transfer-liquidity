# No-double-spend proof (L6, standalone)

{e,p} distinct (E singleton verified; p∉E enforced in code and re-verified:
IN {12,0}). The pair {e,p} plus all remaining singleton intervals partition
the full cyclic interval index set: the others-loop excludes e and p, and
ΣH/Σq/Σc identities verify exhaustiveness (no index dropped or doubled).
The sink reserve R_p is spent once inside the joint inequality
w_e+w_p≤R_p; it is never recharged as a singleton even when p is K/P-
eligible. The exception (w=1,R=0) is never repaid again. K/P overlap on one
interval never duplicates credit (one case suffices; reserves are
per-interval R_j). Every original access lies in exactly one H_j (cyclic
partition; wrap covered). ∎
