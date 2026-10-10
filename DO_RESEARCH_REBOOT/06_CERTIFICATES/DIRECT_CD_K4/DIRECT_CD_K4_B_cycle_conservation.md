# Closed B-cycle conservation (PROVED)

Let C_K = cyclic key-changes in the KEEP-only word. Linearize the exact B-closed
cycle right after a KEEP; then at each KEEP, root(B_t) = previous KEEP key, so
1[x_t≠root(B_t)] is the cyclic change indicator (seam included by closure).

Project B_t to U_t = Core_M(B_t) (4≤|U_t|≤7 by §5; same root; marked depths
agree by §6). Each KEEP applies the certified core inequality to (U_t, x_t):
q_t − 2c_t + η_{t+1} − η_t ≤ 0, where q_t is the full-tree B-double count
(= core-tree count: marked depths agree, and q depends only on d(x) for marked
x) and c_t the change indicator. DELETEs freeze B, U, η and contribute q=0.

Sum over the cycle: Σq_t + ΣΔη = Q_B + 0 ≤ 2Σc_t = 2C_K (telescoping uses exact
B closure ⇒ U returns to start ⇒ η returns). Hence **Q_B ≤ 2C_K**. No startup
correction is needed beyond linearizing at a KEEP boundary (the cyclic sum is
boundary-independent); a nonclosed prefix is excluded from the cycle totals by
definition. Control B exemplifies tightness (Q=10, C_K=6).
