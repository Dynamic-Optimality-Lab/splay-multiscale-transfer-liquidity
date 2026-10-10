# DIRECT-NFKS-RT2: Coarse-Double for ≤3 KEEP keys (PROVED · RT2-A)

**Status: PROVED.** RT2 + idempotence + three-key depth bound + class implication,
all universally quantified; banked-domain audit confirms novelty. Universal
Coarse-Double remains OPEN (arbitrary KEEP alphabets not covered). No J4,
ROW-DIAMETER, J-SELF, potentials, LP, or compactness used.

## RT2 — two-splay root-return conservation (PROVED)

T rooted at y, z≠y, T1=Sz(T), T2=Sy(T1): ∀v, d2(v)≤d0(v)+2. Proof by
orientation (y ends child/same-side grandchild ⇒ return is one StepEv) +
exact return-region tables (F +1; C +1 / T3 +2) + far-side rigidity
(Δ1=−d0(z)≤0 on +2-regions) + near-sibling detach accounting (Δ1=1−d0(z)≤−1
on +1-regions; Δ1≤+1 universally there) + peak-remainder composition for mixed
paths. Corroboration: 52,362 configs n≤9 (0 viol, max exactly 2), 76,168
region checks (0 bad), both engines agree. Full proof:
`06_CERTIFICATES/DIRECT_NFKS_RT2/DIRECT_NFKS_RT2_roundtrip_depth_proof.md`
with rotation tables, orientation, and idempotence files alongside.

## Three-key depth ≤4 (PROVED)

Alternating y/z words revisit post-y/post-z states (idempotence); RT2 caps each
return at +2 over the post-y state (≤2), Sz caps at +2 more: d(x)≤4 for the
third marked key under arbitrary y/z words. (`..._three_key_depth_deduction.md`.)

## Class theorem (PROVED)

Reachable closed γ, |supp(KEEP)|≤3, arbitrary n/length/DELETEs: Q_B≤2C_K
(depth-4 ⇒ q≤2 per KEEP change; exact B closure at seam) ≤2C_X (subsequence
contraction) ≤2A (each full-word change forces an A StepEv; exact A closure).
(`..._coarse_double_class_proof.md`.) Nonvacuity walk verified (A=4,Q=2,W=−6,
exact closure, both engines; dA-column erratum in charter table documented).

## Novelty (Rule 4)

No banked AJ–AS result quantifies over KEEP-support size (§9 audit); the class
is a genuine removed obligation. 26AM Outcome B and all other statuses untouched.

## Scope

KEEP alphabets of size ≥4, general allocation, universal Coarse-Double, and
Dynamic Optimality remain OPEN. Downstream pipeline unchanged.
