# Adversarial audit (task N) — 40 attacks, dispositions with evidence

1. Entry/source mismatch — source SHAs recomputed equal to authorized table (4/4 True). PASS.
2. Sibling divergence — sibling SHA `31dc3058…ebd55`; committed appendix verbatim-identical (wrapping only). PASS.
3. H4/H5 misimplementation — existential-sink implementation (`strict_msink` enumerates all p); min-vs-exists equivalence proved on IN (8 sinks) + global census. PASS.
4. First-sink assumed — never assumed; all H4-eligible tested, joint required. PASS.
5. K→H≥2 — strict d_A≥3 used in all 5 interval predicates + MSINK-H5; 0/384 corpus discrepancies vs old proxies. PASS.
6. P→any-DELETE — strict immediately-preceding-DELETE + a≥1-both used; 0/384 discrepancies. PASS.
7. Seam DELETE loss — cyclic intervals verified by A/Q identities per certificate (B4 additive holds everywhere). PASS.
8. Root no-op misclassified — a=0 continuation rule with key assertion; c=0&q>0 scan: 0/384. PASS.
9. B-depth>8 — 9-node trees ⇒ dB≤8 structurally; observed max dB=6, max q=3. PASS.
10. Same-key KEEP q>0 — c=0⇒q=0 verified 384/384 (zero violations). PASS.
11. Hidden third exception — E-complete by construction; strict count enforced. PASS.
12. Non-maximal relay — stop-at-first-failure maximal scans; E-relay pairs exhaustive. PASS.
13. Short/long changed — exactly {0,1} vs ≥2 per frozen text. PASS.
14. Sink==exception — p∉E enforced in code and certificates. PASS.
15. Sink H=2 — H≥3 enforced; joint inequality needs R≥4. PASS.
16. Sink q=4 omitted — full q≤4 range in joint check form w≤R−2 (no q-range premise beyond nine-core). PASS.
17. Sink double-spend — partition {triple}+singletons disjoint in code (p excluded from others). PASS.
18. K/P overlap double-count — same partition; each interval charged once. PASS.
19. Bridge as extra reserve — bridges are w≤R singletons; no relay credit exists. PASS.
20. A/B divergence suppressed — engines tracked separately; pair serials compared whole-tree. PASS.
21. Prefix as cycle cost — cycle-accesses-only accounting (rotated frames re-derived). PASS.
22. Finite replay as universal proof — explicitly disclaimed (R2 assessment); no promotion. PASS.
23. Missing validity — ReplayError fail-closed; 0 SOURCE-INVALID (all 384 replay clean). PASS.
24. Root-only closure — full nested-tuple serial equality everywhere. PASS.
25. SHA/fixture substitution — all 420 row SHAs recomputed-equal; fixture SHAs gated. PASS.
26. Banked theorem wrongly rejected — G4 controls: NP/S1/S2/VR/MR each DIRECT-BANKED under exactly their mechanism, zero cross-firing. PASS.
27. AS incomplete push — T1 synth ACCEPTS here via same module; my blocks field-superset of synth format; 384 clean executions; dual-push blocks present corpus-wide (384/384 words) yet 0 AS firings for structural reasons (geometry/capacity/snap rejections, not plumbing). PASS.
28. Rotation-hidden decomposition — the core correction: all r tested; 21 non-anchored decompositions found (incl. IN at r=1). PASS.
29. Interior repeat dismissed — repeats enumerated per word; segments fresh-replayed + tested (IN loops S1/VR-covered disclosed; DP complete regardless). PASS.
30. P0-split absence = nondecomposability — REFUTED as general claim (the erratum); corrected DP used instead. PASS (with historical defect documented, files untouched).
31. Aperiodicity as novelty proof — never used (F7 = verified pair-state simplicity + mandatory battery). PASS.
32. Non-diagonal start ignored — segments replayed from live/rebuilt actual states; frozen domains allow reachable states. PASS.
33. VR rotated start confused — P1==VR-post-D5 verified equal; transitions matched per-access. PASS.
34. True decomposition dismissed as non-anchored — DP covers all r; non-anchored certificates recorded. PASS.
35. String similarity vs applicability — state+transition verification required alongside strings. PASS.
36. Missing recognizer as REJECT — all 5 recognizers executed (never missing); exact predicates elsewhere; 0 INDETERMINATE. PASS.
37. Candidate modified after failure — corpus read-only (archive untouched; git status confirms). PASS.
38. Gate-0 cert overwritten — Gate-0/PROOF files untouched (worktree clean except new audit dir). PASS.
39. Ledger promotion — no ledger/deps/02_PROVED writes (verified pre-commit). PASS.
40. Universal claimed — explicitly disclaimed; no promotion regardless of outcome. PASS.

No FAIL, no OPEN. One real historical defect surfaced by design (attack 30 = the erratum itself).
