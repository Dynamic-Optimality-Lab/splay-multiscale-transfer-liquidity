# 26AF mirror-base audit (certificate companion)

## Base computation (exact, from `wp6_staticR` / `wp6_lambda` / `wp6_j4shared`)

- `B_R(∅) = [-5,∅,[-1,[-3,[-4],[-2]],∅]]`: valid BST (asserted), n=5.
- Depths (−2,−4) = (3,3); subsize (1,1); `R_static` = (−1,−1).
- Fold labels via left-singleton probe: (1,1), equal; stable under left insertions
  (T-path fixity — same source argument as Ext-L).
- `Jat` multisets identical ⇒ `c_R = 0`, `β_R = 0` terms (artifact `06_CERTIFICATES/26AF/26AF_D0.json`).

## Comparison to 26AE seed

Same proof shape (mirror-symmetric rows ⇒ zero form), different numbers
(26AE: statics 2/−2 with const −4 + 4-key support; here statics −1/−1 with empty
support). NOT assumed by covariance: computed directly. Structural mirror
correspondence (slot loop identical; Tmap LL↔RR; fold (1,1) both sides) explains
agreement; the computation, not the analogy, carries the proof.

## Ext-R erasure status

Banked: 26AC mirror (symmetry + instances) and REBOOT-01 mirror section (written
proof: path/slot argument verbatim with T right, S left). Applies here:
equal depth + equal fold verified. Shallow negative-offset insertion checked
explicitly (L singleton, δ=−2, D-form zero). Leaf-deletion induction as in 26AB.

## Records

- `06_CERTIFICATES/26AF/af_mirror.py` (procedure), `06_CERTIFICATES/26AF/26AF_D0.json`.
- Erasure spot-checks: ∅ / singleton / vine / branched L, all `(c0=0, 0 terms)`.
