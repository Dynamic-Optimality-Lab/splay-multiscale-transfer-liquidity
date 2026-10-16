# S01_ENTRY_AUDIT.md — Step 01 entry (PHASE 01)

- Repo `Dynamic-Optimality-Lab/splay-multiscale-transfer-liquidity`, branch
  `coarse-double-branch`, HEAD `a76354b732459259fa096b34de4acd1c8c109fd1` — matches the
  authorized checkpoint. No intervening changes (entry `git status`: clean except
  pre-existing MSINK untracked dirs, untouched).
- Source hashes verified at entry: eventflow `d7cc8060…30053`, coarse_double
  `b47019af…00365f`, splay `3a178c13…3f91d2f01`, legacy_embedding `20284bbb…543e1cb2`.
- Audited: `PC_TYPED_DAG.py` (13 node kinds: const/var/not/and/or/xor/ite/add/sub/eq/lt/le/
  exists; hash-consed; iterative topo/ev/simplify), `PC_SOLVER_BACKEND.py` (DPLL over
  free vars; transparent-EXISTS — the known unsoundness QSolver patched at outer level),
  `CW_QUANTIFIED_BACKEND.py` (pin-strip + bound-exclusion + leaf sub-solve; measured
  bottleneck: full-DAG `ev3_iter` scan per visit, ~2 s/visit at 1.4M nodes → 120 visits
  per 240 s cap), `CW_PRODUCT_COMPILER.py` (1,603,069 nodes; 9 low edges; E_sm/E_mt),
  `CW_SYMBOLIC_OPERATORS.py` (Pre/Post/MinPre over QO/QO2/QM), `CW_SYNTHESIS_RUN.py`
  (3/3 grounded ok, 3/3 synthesis UNKNOWN), both evidence JSONs, FGHIJ verdict, and the
  Gate B/C/E theorem certificates.
- Signed sites: only 5-bit signed weight vars (`CL_w`, `CH _w1`, low selector
  `EQ(w, const(w,5,signed))`, w∈[-4,4]); high q is 4-bit unsigned (used 0..9).
  All other ints unsigned with fixed widths; historical evaluation is exact math-int
  in claimed overflow-free ranges (width audit: `S01_ARITHMETIC_WIDTH_AUDIT.md`).
- Baseline metrics carried: low 240 grounded / high 319 grounded / operators 16+16+0 /
  universal 25/25.
