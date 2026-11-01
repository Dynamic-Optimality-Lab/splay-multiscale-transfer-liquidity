# Reproducibility and preservation of the source charging result

The [producer](audit_shallow_successor.py) uses the read-only tuple splay. The [independent verifier](independent_verify.py) imports only the pointer source and standard-library modules. Neither imports a matching evaluator, allocation optimizer, old recognizer, or Stage 11G code. Both disable bytecode and create files exclusively with mode x.

The original run used Python with `-X utf8 -B`. To reproduce, create a fresh versioned sibling directory, copy the two scripts and preexecution gate files there, run the producer, then the verifier. Do not overwrite these sealed outputs. The new run will also pin this run's artifacts as prior research.

Finite scope is exactly one fixed seven-key diagonal prefix and 22-access closed word plus reflection, and the sharp four-key root-child transport control plus reflection. There is no witness search, size sweep, larger finite fit, potential table or source graph. The verifier performs 92 pointer-source accesses. It checks 44 cycle rows, four reachability-prefix rows, all 44 cyclic cuts, and 22 distinct B-demand/A-credit assignments across orientations. Every demand is paid once; every credit is used at most once.

The certificate SHA-256 is `b8d1ea8b9a902c04072054e16aef45cad00bc82b4f5eff975b20e0647d6edc5a`. The all-size restricted charging theorem and unbounded-support family are analytic proofs in SC01 and SC02, not extrapolations from this corpus. The comparison with banked AJ-AS classes uses directly checked necessary conditions from the pinned definitions; no old recognizer execution is claimed.

Entry/final checks preserve 522 inherited/source/previous-run/theorem-definition files, all 125 Stage 11G files and their inventory, branch/HEAD and tracked status. The user-imposed matching-terminal freeze notice is pinned and unchanged. Historical untracked material is retained. The final delivery manifest hashes each new artifact except itself.
