# Coarse-Double for KEEP support ≤3 (PROVED from depth-4 bound)

Let γ be diagonally reachable, exactly closed (both trees), KEEP keys ⊆ {at
most 3 distinct}, DELETEs arbitrary present keys, arbitrary n/length.

## B side: Q_B ≤ 2C_K

Cyclic KEEP word K (ignore DELETEs; they freeze B). If adjacent KEEPs (cyclically)
share the key, the later has q=0 (B already rooted there). Else key changes to
x: consider the last previous KEEP of x in the cyclic word; B was then rooted
at x, and intervening KEEPs use only the other ≤2 keys. By §6 with marked keys
{x + other two} (root(T)=x at that moment), d_B(x)≤4 now, so q=⌊d/2⌋≤2. Exact B
closure covers the cyclic seam (last→first transition obeys the same bound).
Summing over the C_K cyclic KEEP-key changes (non-changes contribute 0):
Q_B ≤ 2C_K.

## A side: C_K ≤ C_X ≤ A

C_X = cyclic key-changes in the FULL word (KEEP+DELETE). Deleting the DELETE
entries (subsequence) cannot create new adjacencies beyond C_X: each KEEP-change
pair corresponds to a distinct full-word change or a contracted run — formally,
contracting maximal constant-key runs then deleting DELETE-runs leaves the KEEP
run sequence, whose cyclic changes ≤ those of the full run sequence. Hence
C_K ≤ C_X. Each full-word key change accesses a key ≠ current A-root, so pre-A
depth ≥1, contributing a≥1 (a=⌈d/2⌉≥1). A-root no-ops contribute 0 but are not
changes. Exact A closure covers the seam. Hence C_X ≤ A (each counted change
supplies a distinct StepEv; one StepEv is charged at most once since changes
are per-transition).

## Conclusion

Q_B ≤ 2C_K ≤ 2C_X ≤ 2A, i.e. Q_B(γ) ≤ 2A(γ) for the entire ≤3-KEEP-key class,
uniform in n, length, DELETE pattern. No token matching, no packet hypothesis,
no pairwise-credit reuse (each A StepEv charged once). Zero-A walks: banked
zero-A theorem (Q_B=0) agrees.
