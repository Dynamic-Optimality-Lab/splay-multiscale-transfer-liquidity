# Original four-key class proof (PROVED) + RT2-A combination

C_X = cyclic changes in the FULL word. Deleting DELETE entries cannot increase
cyclic changes (contracting constant-key runs then deleting DELETE-runs leaves
the KEEP run sequence with ≤ changes): **C_K ≤ C_X**. Each full-word change
accesses a key ≠ current A-root ⇒ pre-A-depth ≥1 ⇒ a≥1; A-root no-ops are not
changes; exact A closure covers the seam; each change charges a distinct access
⇒ **C_X ≤ A** (single-charge; StepEv counted once). With §8: **Q_B ≤ 2A** for
|supp(KEEP)|=4, uniform in n/length/DELETEs/prefix. Zero-A walks agree with the
banked zero-A theorem.

Combined with banked RT2-A (≤3 keys): **|supp(KEEP)| ≤ 4 ⇒ Q_B ≤ 2A**.

**Controls.** D: no four-key round-robin idempotence assumed (unused). E: no
E/S conjectures used anywhere (rotation tables + K4-L1 + finite η only).
Gate-0 witness revalidated (19/10/−28, closure, 15/15 engines, all recognizers
REJECT) — a coverage-gap example, not a counterexample (W<0).

**Not claimed.** Five-key alphabets, universal Coarse-Double, Dynamic Optimality.
