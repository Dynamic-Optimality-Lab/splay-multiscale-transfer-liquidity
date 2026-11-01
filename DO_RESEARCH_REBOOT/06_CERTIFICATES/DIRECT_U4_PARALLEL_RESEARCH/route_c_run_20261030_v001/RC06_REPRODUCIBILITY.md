# Reproduction

From the repository root, use a NEW sibling directory at the same depth. Copy only the two new test scripts there. They compute ROOT by parent depth and exclusively create their outputs; never rerun a writer against an existing result path.

    python -X utf8 -B <fresh-run>/rc_histogram_test.py
    python -X utf8 -B <fresh-run>/verify_histogram_certificate.py

No dependency installation is required. Both physical engines are existing repository modules. The first script constructs all429 BSTs independently of saved graph files, verifies3,003 tuple/pointer splay destinations AND event traces, computes concrete reachability/recurrence, builds exact complete summaries and every maximal reward edge, and verifies the produced integer inequalities. The second imports only the pointer engine and independently regenerates all concrete rows; it does not trust graph construction, solver termination or sampling.

The summary uses all joint depth cells, not separate marginals. Parallel source transitions are combined by MAX reward, preserving the strongest required inequality. Solver labels are negated exactly: if d[v]>=d[u]+reward, Phi=-d gives Phi[u]-Phi[v]>=reward. No floating signs/rounding are involved.

result.json records dimensions, passes, edge scans and CPU time. independent_certificate_audit.json records all2,576,574 checks, residual histogram, full saved-word potential values and certificate SHA256. The original U4 matching and symbolic Stage11G certificates are not test dependencies or proof premises.

entry_source_pins.json pins1,888 pre-existing source/input files. integrity.json compares those hashes and branch/HEAD/tracked state. Active untracked Stage11G population work is outside the source-freeze claim. New scripts use Python -B to avoid bytecode caches. No old result path is written.

Coverage limits: n=7 finite source domain only. Arbitrary path lengths follow by exact telescoping inside this domain. No nine-key potential, all-size formula, general histogram theorem, Coarse-Double counterexample or new universal Dynamic Optimality theorem is claimed.
