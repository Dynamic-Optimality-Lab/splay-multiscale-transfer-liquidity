# Lemma 2 — nine-core B-debt bound (PROVED)

**Claim.** On the class: c_j=0 ⇒ q_j=0 (hence w_j=0); w_j>0 ⇒ c_j=1,
q_j∈{3,4}, 1≤w_j≤2.

**Proof.** Banked CDK5L-A geometry (reused, not re-proved): every marked key's
root-to-key path lies in the nine-node core ⇒ d_B(x_j)≤8 for marked x_j
(regardless of nodes outside the core; labels may permute — depth counts
ancestors, all on the marked path). Thus q_j≤4. If c_j=0, x_j equals the
previous KEEP key; B has been rooted there since that KEEP (KEEP splays B;
intervening DELETEs freeze B) ⇒ d_B=0 ⇒ q_j=0 ⇒ w_j=0−0=0. If w_j>0 then
c_j=1 (else w=0) and q_j>2, i.e. q_j∈{3,4} ⇒ w_j=q_j−2∈{1,2}. ∎

**Non-claim.** Q_B≤2C_K is NOT asserted (nine-node obstruction refutes it:
Q−2C_K=+2 there). The debt bound is per-interval and uniform; A-side payment
(Lemmas 3–4) is still required.
