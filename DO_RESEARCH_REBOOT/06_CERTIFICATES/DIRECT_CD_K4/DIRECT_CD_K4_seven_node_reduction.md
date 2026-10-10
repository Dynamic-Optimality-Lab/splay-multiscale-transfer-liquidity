# Seven-node reduction (PROVED for arbitrary KEEP ordering)

Fix M = the walk's four KEEP keys. Track V_k = first k distinct KEEP keys seen
and C_k = Core_{V_k}(B) along one full cyclic period linearized right after a
KEEP of k1 (exists since all four occur; DELETEs freeze B).

- Start: B rooted at k1, V_1={k1}, C_1={k1}, size 1 (root always in a nonempty
  core; path k1→k1 is {k1}).
- New key x=k_{k+1}∉V_k: K4-L1 (unmarked case w.r.t. V_k) gives
  |C_k(after)| ≤ |C_k(before)|+2. After the splay x is root ⇒ x∈C_k(after)
  (root in every nonempty core) ⇒ C_{k+1}(after) = C_k(after) ∪ {x} = C_k(after)
  as sets. Between new-key events only revisits (x∈V_current ⇒ marked case ⇒
  nonincreasing) and DELETEs (frozen) occur, so sizes never exceed the running
  bound. Hence |C_2|≤3, |C_3|≤5, |C_4|≤7.
- End of period = start state (exact B closure): core_M there ≤7.

The occurrence was arbitrary: every KEEP-occurrence state is such a period
start (rotate the cycle; one full period visits all four keys), so every
KEEP-occurrence B-state has core_M ≤7; every DELETE-occurrence B-state shares
B with its preceding KEEP state. Core_M ⊇ M gives ≥4 nodes. Therefore every
cyclic B-state projects to a core U with 4≤|U|≤7. ∎

Arbitrary KEEP ordering/repetition covered (revisits are marked-case
nonincreasing regardless of order). No packet/return/depth assumption.
