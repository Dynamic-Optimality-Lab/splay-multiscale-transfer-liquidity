# Reproducibility and preservation

The [producer](audit_contained_terminal.py) and [independent verifier](independent_verify.py) use Python standard-library modules and the read-only tuple and pointer splay engines, respectively. They disable bytecode generation and write all outputs with exclusive mode x. They import neither old evaluators nor Stage 11G code. No package installation, potential fitting or source-state graph is used.

The original commands used Python with `-X utf8 -B`. To reproduce, create a fresh versioned directory under the same DIRECT_U4_PARALLEL_RESEARCH parent, copy the scripts and gate there, run the producer, then the verifier. Do not rerun over sealed outputs; exclusive writes intentionally prevent replacement. A new run's entry pins will additionally include this run.

The corpus consists of exactly two analytically specified members and their reflections: seven-key parity-comb repair and fourteen-key fully fringed-spine counterexample. Eight terminal graphs have maximum matching and minimum cover witnesses of equal cardinality. The independent verifier reconstructs every interval and permitted edge and checks those witnesses without a matching optimizer or producer import. It performs 20 pointer-source accesses, including completion idempotence checks.

The certificate SHA-256 is `a9201d16464d5b67be9c582cefd7d707c82f10a4e8927b270ddd60562c8d8a25`. The all-size theorems are analytic proofs in CT01 and CT02, not extrapolations from the local corpus. No diagonal reachability or actual closed pair walk is asserted for the new counterexample.

Entry/final hashes cover 479 inherited/source/previous-run files and all 125 Stage 11G files and their inventory. HEAD, branch and tracked status are preserved. The final manifest hashes each new artifact except itself. Historical untracked files are retained; the worktree is not described as globally clean.
